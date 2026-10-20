#!/usr/bin/env python3
"""Build the static search index for the OctoProbe News blog index (/blog/).

The blog index cards (blog/index.html) are the source of truth for which posts are
searchable and in what order; each card's post page (blog/<slug>/index.html) supplies the
body text, keywords and section. The browser search (assets/js/blog-search.js) filters and
ranks those same cards, so the page works unchanged without JavaScript.

Writes (deterministic, so --check can diff it in CI):
  blog/index.html                data-search-version="<hash>" on #blogSearch, a short
                                 content hash of the two files below, used as their ?v=
                                 cache-buster (only that attribute is touched)
  assets/search/index.json       title, slug, url, description, category, date, tags,
                                 keywords and plain body text per post (lexical engine)
  assets/search/vectors.json     semantic vectors per post (title+description vector and
                                 one vector per body passage), int8-quantised, base64.
                                 Only written when the vendored static embedding model
                                 (assets/search/model/) is present.

Semantic model: a Model2Vec static embedding model (minishlab/potion-base-8M, MIT),
vendored as int8 under assets/search/model/. A text embedding is the mean of its WordPiece
token vectors, L2-normalised, so the same tokenizer + lookup runs here in pure Python and in
the browser in plain JS, with no ONNX/WASM runtime.

Usage (repo root):
  python3 scripts/build-search-index.py          # write the index files
  python3 scripts/build-search-index.py --check  # exit 1 if they are stale
No third-party packages.
"""
from __future__ import annotations

import base64
import hashlib
import json
import math
import re
import sys
import unicodedata
from array import array
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG_INDEX = ROOT / "blog" / "index.html"
OUT_DIR = ROOT / "assets" / "search"
INDEX_JSON = OUT_DIR / "index.json"
VECTORS_JSON = OUT_DIR / "vectors.json"
MODEL_DIR = OUT_DIR / "model"
BODY_CAP = 16000        # chars of body text kept per post for the lexical index
PASSAGE_WORDS = 120     # target words per semantic passage
MAX_PASSAGES = 64       # per post

# ── HTML helpers ─────────────────────────────────────────────────────────────

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "figcaption", "blockquote", "td", "th",
         "dt", "dd", "pre", "summary", "caption"}
SKIP = {"script", "style", "svg", "noscript", "button", "template", "nav"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source",
        "track", "wbr"}


class ProseText(HTMLParser):
    """Collect block-level text inside the first <div class="prose"> of <article>.

    Skips scripts/styles/SVG, the author bio box (.author-note) and Related Reading
    (.related-reading), which are boilerplate shared across posts."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, bool]] = []   # (tag, opens-a-skip-region)
        self.in_article = 0
        self.prose_depth = None
        self.skip = 0
        self.blocks: list[str] = []
        self.buf: list[str] = []

    def _flush(self):
        t = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if t:
            self.blocks.append(t)
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        if tag == "article":
            self.in_article += 1
        opens_skip = False
        if self.prose_depth is None and self.in_article and tag == "div" and "prose" in cls:
            self.prose_depth = len(self.stack) + 1
        elif self.prose_depth is not None and (
                tag in SKIP or "author-note" in cls or "related-reading" in cls
                or "toc" in cls or a.get("aria-hidden") == "true"):
            opens_skip = True
            self.skip += 1
        self.stack.append((tag, opens_skip))
        if tag in BLOCK:
            self._flush()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        # pop to the matching tag (tolerates sloppy nesting)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for t, s in self.stack[i:]:
                    if s:
                        self.skip -= 1
                    if t == "article":
                        self.in_article -= 1
                del self.stack[i:]
                break
        if tag in BLOCK:
            self._flush()
        if self.prose_depth is not None and len(self.stack) < self.prose_depth:
            self._flush()
            self.prose_depth = -1   # done: only the first prose block

    def handle_data(self, data):
        if self.prose_depth not in (None, -1) and not self.skip:
            self.buf.append(data)


def strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def meta(html: str, name: str) -> str:
    m = re.search(r'<meta\s+(?:property|name)="%s"\s+content="([^"]*)"' % re.escape(name), html)
    return unescape(m.group(1)).strip() if m else ""


def cards(html: str) -> list[dict]:
    """Parse the post cards on blog/index.html, in page order."""
    out = []
    for m in re.finditer(r'<a class="post-card[^"]*" href="(/blog/([^"/]+)/)">(.*?)</a>\s*(?=<a class="post-card|</div>)',
                         html, re.S):
        url, slug, body = m.groups()
        h2 = re.search(r"<h2>(.*?)</h2>", body, re.S).group(1)
        h2 = re.sub(r'<span class="card-kicker">.*?</span>', "", h2, flags=re.S)
        out.append({
            "slug": slug,
            "url": url,
            "title": strip_tags(h2),
            "description": strip_tags(re.search(r'<p class="excerpt">(.*?)</p>', body, re.S).group(1)),
            "date": re.search(r'<time datetime="([^"]+)"', body).group(1),
            "tags": [strip_tags(t) for t in re.findall(r'<span class="tag[^"]*">(.*?)</span>', body, re.S)],
        })
    if not out:
        raise SystemExit("ERROR: no post cards found on blog/index.html")
    return out


def post_doc(card: dict) -> dict:
    path = ROOT / "blog" / card["slug"] / "index.html"
    if not path.exists():
        raise SystemExit(f"ERROR: card links to missing post {path.relative_to(ROOT)}")
    html = path.read_text(encoding="utf-8")
    p = ProseText()
    p.feed(html)
    p.close()
    blocks = [b for b in p.blocks if len(b) > 1]
    if not blocks:
        raise SystemExit(f"ERROR: no article prose found in {path.relative_to(ROOT)}")
    sec = re.search(r'"articleSection"\s*:\s*"([^"]+)"', html)
    kw = [k.strip() for k in meta(html, "keywords").split(",") if k.strip()]
    body = " ".join(blocks)
    return {
        **card,
        "category": sec.group(1) if sec else (card["tags"][0] if card["tags"] else ""),
        "keywords": kw,
        "dek": meta(html, "description"),
        "body": body[:BODY_CAP].rsplit(" ", 1)[0] if len(body) > BODY_CAP else body,
        "_blocks": blocks,
    }


# ── Model2Vec static embeddings (pure Python; mirrors assets/js/blog-search.js) ──

class WordPiece:
    """BERT uncased tokenizer: clean, lowercase, strip accents, split on whitespace and
    punctuation (CJK chars as their own words), then greedy longest-match WordPiece."""

    def __init__(self, vocab: list[str], unk="[UNK]", max_chars=100):
        self.ids = {t: i for i, t in enumerate(vocab)}
        self.unk = self.ids.get(unk)
        self.max_chars = max_chars

    @staticmethod
    def _is_punct(ch: str) -> bool:
        cp = ord(ch)
        if 33 <= cp <= 47 or 58 <= cp <= 64 or 91 <= cp <= 96 or 123 <= cp <= 126:
            return True
        return unicodedata.category(ch).startswith("P")

    @staticmethod
    def _is_cjk(cp: int) -> bool:
        return (0x4E00 <= cp <= 0x9FFF or 0x3400 <= cp <= 0x4DBF or 0x20000 <= cp <= 0x2A6DF
                or 0x2A700 <= cp <= 0x2B73F or 0x2B740 <= cp <= 0x2B81F or 0x2B820 <= cp <= 0x2CEAF
                or 0xF900 <= cp <= 0xFAFF or 0x2F800 <= cp <= 0x2FA1F)

    def words(self, text: str) -> list[str]:
        out, cur = [], []
        text = unicodedata.normalize("NFD", text.lower())
        for ch in text:
            cp = ord(ch)
            if cp == 0 or cp == 0xFFFD or unicodedata.category(ch) == "Mn":
                continue
            if ch.isspace() or (unicodedata.category(ch) in ("Cc", "Cf") and ch not in "\t\n\r"):
                if cur:
                    out.append("".join(cur)); cur = []
            elif self._is_punct(ch) or self._is_cjk(cp):
                if cur:
                    out.append("".join(cur)); cur = []
                out.append(ch)
            else:
                cur.append(ch)
        if cur:
            out.append("".join(cur))
        return out

    def encode(self, text: str) -> list[int]:
        ids = []
        for w in self.words(text):
            if len(w) > self.max_chars:
                if self.unk is not None:
                    ids.append(self.unk)
                continue
            start, pieces, bad = 0, [], False
            while start < len(w):
                end, hit = len(w), None
                while start < end:
                    sub = w[start:end] if start == 0 else "##" + w[start:end]
                    if sub in self.ids:
                        hit = self.ids[sub]; break
                    end -= 1
                if hit is None:
                    bad = True; break
                pieces.append(hit); start = end
            if bad:
                if self.unk is not None:
                    ids.append(self.unk)
            else:
                ids.extend(pieces)
        return ids


class StaticModel:
    """Loads assets/search/model/{meta.json,vocab.txt,embeddings.i8,scales.f32}: int8 rows
    with a per-row float32 scale (row_i = int8_i * scale_i)."""

    def __init__(self, d: Path):
        m = json.loads((d / "meta.json").read_text(encoding="utf-8"))
        self.meta = m
        self.dim = m["dim"]
        vocab = (d / "vocab.txt").read_text(encoding="utf-8").split("\n")
        if vocab and vocab[-1] == "":
            vocab.pop()
        self.tok = WordPiece(vocab, unk=m.get("unk_token", "[UNK]"))
        raw = (d / "embeddings.i8").read_bytes()
        n = len(vocab)
        if len(raw) != n * self.dim:
            raise SystemExit("ERROR: model embeddings size does not match vocab x dim")
        self.q = memoryview(raw).cast("b")
        sc = array("f")
        sc.frombytes((d / "scales.f32").read_bytes())
        if sys.byteorder != "little":
            sc.byteswap()
        if len(sc) != n:
            raise SystemExit("ERROR: model scales size does not match vocab")
        self.scale = sc
        self.skip = set(m.get("skip_ids", []))

    def embed(self, text: str) -> list[float]:
        acc = [0.0] * self.dim
        n = 0
        for i in self.tok.encode(text):
            if i in self.skip:
                continue
            s = self.scale[i]
            row = self.q[i * self.dim:(i + 1) * self.dim]
            for k in range(self.dim):
                acc[k] += row[k] * s
            n += 1
        if not n:
            return acc
        norm = math.sqrt(sum(x * x for x in acc)) or 1.0
        return [x / norm for x in acc]


def pack(vec: list[float]) -> str:
    """L2-normalised float vector -> int8 (x127) -> base64."""
    b = bytes((max(-127, min(127, round(x * 127))) & 0xFF) for x in vec)
    return base64.b64encode(b).decode("ascii")


def passages(blocks: list[str]) -> list[str]:
    out, cur, n = [], [], 0
    for b in blocks:
        w = len(b.split())
        if cur and n + w > PASSAGE_WORDS:
            out.append(" ".join(cur)); cur, n = [], 0
        cur.append(b); n += w
    if cur:
        out.append(" ".join(cur))
    return out[:MAX_PASSAGES]


# ── main ─────────────────────────────────────────────────────────────────────

def dumps(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n"


def build() -> dict[Path, str]:
    docs = [post_doc(c) for c in cards(BLOG_INDEX.read_text(encoding="utf-8"))]
    index = {
        "version": 1,
        "fields": ["title", "description", "category", "tags", "keywords", "body"],
        "posts": [{k: d[k] for k in ("slug", "url", "title", "description", "category", "date",
                                     "tags", "keywords", "body")} for d in docs],
    }
    out = {INDEX_JSON: dumps(index)}
    if (MODEL_DIR / "meta.json").exists():
        model = StaticModel(MODEL_DIR)
        vec = {"version": 1, "model": model.meta["name"], "dim": model.dim, "posts": []}
        for d in docs:
            head = " ".join([d["title"], d["description"], d["dek"], d["category"],
                             " ".join(d["tags"]), " ".join(d["keywords"])])
            vec["posts"].append({
                "slug": d["slug"],
                "head": pack(model.embed(head)),
                "passages": [pack(model.embed(p)) for p in passages(d["_blocks"])],
            })
        out[VECTORS_JSON] = dumps(vec)
    return out


VERSION_RE = re.compile(r'(id="blogSearch"[^>]*?data-search-version=")([^"]*)(")')


def stamp_version(out: dict[Path, str]) -> None:
    """Point the search UI at the current index files via a content-hash cache-buster."""
    h = hashlib.sha256("".join(out[p] for p in sorted(out)).encode("utf-8")).hexdigest()[:10]
    html = BLOG_INDEX.read_text(encoding="utf-8")
    if not VERSION_RE.search(html):
        raise SystemExit('ERROR: blog/index.html has no id="blogSearch" ... data-search-version="" attribute')
    out[BLOG_INDEX] = VERSION_RE.sub(lambda m: m.group(1) + h + m.group(3), html, count=1)


def main() -> int:
    check = "--check" in sys.argv[1:]
    out = build()
    stamp_version(out)
    stale = []
    for path, text in out.items():
        cur = path.read_text(encoding="utf-8") if path.exists() else None
        if cur == text:
            continue
        if check:
            stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)} ({len(text.encode()):,} bytes)")
    if check:
        if stale:
            print("STALE (run python3 scripts/build-search-index.py): " + ", ".join(stale), file=sys.stderr)
            return 1
        print("search index up to date (" + ", ".join(str(p.relative_to(ROOT)) for p in out) + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
