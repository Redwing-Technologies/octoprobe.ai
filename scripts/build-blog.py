#!/usr/bin/env python3
"""Build OctoProbe blog posts from Markdown into HTML shells.

SEO / AEO / chat-engine aware:
  - Requires title, description, date, tags (warns/fails on gaps)
  - Injects BlogPosting + BreadcrumbList (no FAQPage; posts have no FAQ section)
  - Validates title/description length
  - Regenerates sitemap.xml via scripts/gen-sitemap.py (from all built HTML)
  - Refreshes the Blog section in llms.txt and .well-known/llms.txt
  - Adds the default social share bar under the byline of EVERY built post
    (markdown and hand-built), see "Share bar" below

Usage (from landing repo root):
  python3 scripts/build-blog.py
  python3 scripts/build-blog.py blog/posts/identifier-graph-osint-methodology.md
  python3 scripts/build-blog.py --share-only          # only (re)insert the share bar in every post
  python3 scripts/build-blog.py --share-only --check  # exit 1 if any post's share bar is missing/stale
  python3 scripts/build-blog.py --lightbox-only        # screenshot lightbox on every post
  python3 scripts/build-blog.py --lightbox-only --check  # exit 1 if include/exclude/ratio markup is stale

No remote deploy — write local HTML only. Requires no third-party packages.
"""
from __future__ import annotations

import json
import re
import sys
import warnings
from datetime import datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "blog" / "posts"
TEMPLATE = ROOT / "blog" / "_template.html"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import authors as AU  # noqa: E402  shared author defaults (Colin Aamot) + overrides
SITEMAP = ROOT / "sitemap.xml"
LLMS_PATHS = [ROOT / "llms.txt", ROOT / ".well-known" / "llms.txt"]
SITE = "https://www.octoprobe.ai"
OG_DEFAULT = f"{SITE}/og-image.png"
TITLE_SOFT_MAX = 60
DESC_SOFT_MIN = 120
DESC_SOFT_MAX = 165


# ── Front matter ─────────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse a pragmatic YAML subset: scalars, [lists], and faq: - q:/a: blocks."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    fm_raw = text[3:end].strip("\n")
    body = text[end + 4 :].lstrip("\n")
    meta: dict = {}
    lines = fm_raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        # faq list block
        if re.match(r"^howto:\s*$", line):
            howto: dict = {"name": "", "steps": []}
            i += 1
            current_step: dict | None = None
            while i < len(lines):
                fl = lines[i]
                if fl and not fl.startswith(" ") and not fl.startswith("\t"):
                    break
                m_name = re.match(r"^\s+name:\s*(.*)$", fl)
                m_step = re.match(r"^\s+-\s+name:\s*(.*)$", fl)
                m_text = re.match(r"^\s+text:\s*(.*)$", fl)
                if m_name and current_step is None and not howto.get("name"):
                    howto["name"] = _strip_yaml_str(m_name.group(1))
                elif m_step:
                    if current_step:
                        howto["steps"].append(current_step)
                    current_step = {"name": _strip_yaml_str(m_step.group(1)), "text": ""}
                elif m_text and current_step is not None:
                    ans = _strip_yaml_str(m_text.group(1))
                    i += 1
                    while i < len(lines):
                        cont = lines[i]
                        if re.match(r"^\s{4,}\S", cont) and not re.match(r"^\s+-\s+", cont) and not re.match(r"^\s+name:\s*", cont) and not re.match(r"^\s+text:\s*", cont):
                            ans += " " + cont.strip()
                            i += 1
                        else:
                            break
                    current_step["text"] = ans
                    i -= 1
                i += 1
            if current_step:
                howto["steps"].append(current_step)
            meta["howto"] = howto
            continue
        if re.match(r"^faq:\s*$", line):
            faqs = []
            i += 1
            current: dict | None = None
            while i < len(lines):
                fl = lines[i]
                if fl and not fl.startswith(" ") and not fl.startswith("\t"):
                    break
                m_item = re.match(r"^\s*-\s+q:\s*(.*)$", fl)
                m_q = re.match(r"^\s+q:\s*(.*)$", fl)
                m_a = re.match(r"^\s+a:\s*(.*)$", fl)
                if m_item:
                    if current:
                        faqs.append(current)
                    current = {"q": _strip_yaml_str(m_item.group(1)), "a": ""}
                elif m_q and current is not None:
                    current["q"] = _strip_yaml_str(m_q.group(1))
                elif m_a and current is not None:
                    ans = _strip_yaml_str(m_a.group(1))
                    # continuation lines indented under a:
                    i += 1
                    while i < len(lines):
                        cont = lines[i]
                        if re.match(r"^\s{4,}\S", cont) and not re.match(r"^\s+-\s+q:", cont) and not re.match(r"^\s+q:", cont) and not re.match(r"^\s+a:", cont):
                            ans += " " + cont.strip()
                            i += 1
                        else:
                            i -= 1
                            break
                    current["a"] = ans
                i += 1
            if current:
                faqs.append(current)
            meta["faq"] = faqs
            continue
        if ":" not in line:
            i += 1
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            meta[k] = [p.strip().strip("\"'") for p in inner.split(",") if p.strip()]
        else:
            meta[k] = _strip_yaml_str(v)
        i += 1
    return meta, body


def _strip_yaml_str(v: str) -> str:
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    return v


# ── Markdown → HTML ──────────────────────────────────────────────────────────

def inline_md(s: str) -> str:
    s = escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+|/[^\)]+)\)",
        r'<a href="\2">\1</a>',
        s,
    )
    return s


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    in_ul = False
    in_ol = False
    in_table = False
    table_rows: list[list[str]] = []

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("|") and stripped.endswith("|"):
            close_lists()
            cells = [c for c in stripped.strip("|").split("|")]
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            i += 1
            continue
        elif in_table:
            rows = [r for r in table_rows if not all(re.match(r"^:?-+:?$", c.strip()) for c in r)]
            if rows:
                t = ["<table>"]
                for ri, row in enumerate(rows):
                    tag = "th" if ri == 0 else "td"
                    t.append("<tr>" + "".join(f"<{tag}>{inline_md(c.strip())}</{tag}>" for c in row) + "</tr>")
                t.append("</table>")
                out.append("\n".join(t))
            table_rows = []
            in_table = False

        if stripped == "---":
            close_lists()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith("### "):
            close_lists()
            out.append(f"<h3>{inline_md(stripped[4:])}</h3>")
            i += 1
            continue
        if stripped.startswith("## "):
            close_lists()
            heading = stripped[3:]
            # Key takeaways → callout-friendly class hook via h2 id
            hid = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
            out.append(f'<h2 id="{escape(hid)}">{inline_md(heading)}</h2>')
            i += 1
            continue
        if stripped.startswith("# "):
            # title usually in frontmatter / hero — skip duplicate H1 in body
            i += 1
            continue

        m = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if m:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{inline_md(m.group(2))}</li>")
            i += 1
            continue

        if stripped.startswith("- "):
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_md(stripped[2:])}</li>")
            i += 1
            continue

        if stripped.startswith("> "):
            close_lists()
            out.append(f"<blockquote><p>{inline_md(stripped[2:])}</p></blockquote>")
            i += 1
            continue

        if not stripped:
            close_lists()
            i += 1
            continue

        close_lists()
        para = [stripped]
        i += 1
        while i < len(lines):
            n = lines[i].strip()
            if (
                not n
                or n.startswith("#")
                or n.startswith("- ")
                or n.startswith("|")
                or n.startswith(">")
                or n == "---"
                or re.match(r"^\d+\.\s+", n)
            ):
                break
            para.append(n)
            i += 1
        out.append("<p>" + inline_md(" ".join(para)) + "</p>")

    close_lists()
    if in_table:
        rows = [r for r in table_rows if not all(re.match(r"^:?-+:?$", c.strip()) for c in r)]
        if rows:
            t = ["<table>"]
            for ri, row in enumerate(rows):
                tag = "th" if ri == 0 else "td"
                t.append("<tr>" + "".join(f"<{tag}>{inline_md(c.strip())}</{tag}>" for c in row) + "</tr>")
            t.append("</table>")
            out.append("\n".join(t))

    html = "\n".join(out)
    # Wrap Key takeaways section list in a callout if present
    html = re.sub(
        r'(<h2 id="key-takeaways">[^<]+</h2>\s*)(<ul>.*?</ul>)',
        r'\1<div class="callout takeaways"><strong>TL;DR · Key takeaways</strong>\2</div>',
        html,
        count=1,
        flags=re.S,
    )
    return html


def tag_class(tag: str) -> str:
    t = tag.lower()
    if "osint" in t:
        return "tag blue"
    if "graph" in t or "identifier" in t:
        return "tag teal"
    return "tag"


# ── Validation ───────────────────────────────────────────────────────────────

class BuildError(Exception):
    pass


def validate_meta(meta: dict, md_path: Path, *, strict: bool = True) -> list[str]:
    warnings_out: list[str] = []
    required = ["title", "date", "tags"]
    # description required; accept excerpt as legacy alias only with loud warn
    desc = meta.get("description") or ""
    if not desc:
        if meta.get("excerpt"):
            warnings_out.append(
                f"{md_path.name}: missing description — using excerpt (add description: for AEO)"
            )
            meta["description"] = meta["excerpt"]
            desc = meta["description"]
        else:
            msg = f"{md_path.name}: REQUIRED front matter field missing: description"
            if strict:
                raise BuildError(msg)
            warnings_out.append(msg)

    for key in required:
        val = meta.get(key)
        if val is None or val == "" or val == []:
            msg = f"{md_path.name}: REQUIRED front matter field missing: {key}"
            if strict:
                raise BuildError(msg)
            warnings_out.append(msg)

    if not meta.get("canonical"):
        slug = meta.get("slug") or md_path.stem
        warnings_out.append(
            f"{md_path.name}: missing canonical — will default to {SITE}/blog/{slug}/"
        )

    title = meta.get("title") or ""
    # Title tag will be "{title} · OctoProbe News" — warn on long primary title
    full_title = f"{title} · OctoProbe News"
    if len(full_title) > TITLE_SOFT_MAX + 20:
        warnings_out.append(
            f"{md_path.name}: title tag ~{len(full_title)} chars (aim ≤~{TITLE_SOFT_MAX} for primary title alone; full tag includes brand)"
        )
    elif len(title) > TITLE_SOFT_MAX:
        warnings_out.append(
            f"{md_path.name}: title {len(title)} chars (soft max ~{TITLE_SOFT_MAX})"
        )

    if desc:
        if len(desc) < DESC_SOFT_MIN:
            warnings_out.append(
                f"{md_path.name}: description {len(desc)} chars (soft min ~{DESC_SOFT_MIN})"
            )
        elif len(desc) > DESC_SOFT_MAX:
            warnings_out.append(
                f"{md_path.name}: description {len(desc)} chars (soft max ~{DESC_SOFT_MAX})"
            )


    af = (meta.get("answer_first") or "").strip()
    if not af:
        warnings_out.append(
            f"{md_path.name}: missing answer_first: (40–60 word standalone lede for AEO / ChatGPT / Perplexity / Gemini)"
        )
    else:
        wc = len(af.split())
        if wc < 35 or wc > 75:
            warnings_out.append(
                f"{md_path.name}: answer_first is {wc} words (aim ~40–60 for extractability)"
            )

    if not meta.get("primary_question"):
        warnings_out.append(
            f"{md_path.name}: missing primary_question: (the question this page answers)"
        )

    return warnings_out


# ── JSON-LD ──────────────────────────────────────────────────────────────────

def build_json_ld(meta: dict, slug: str, description: str) -> list[dict]:
    title = meta.get("title") or slug
    date = meta.get("date") or ""
    date_mod = meta.get("date_modified") or date
    og_image = meta.get("og_image") or OG_DEFAULT
    keywords = meta.get("keywords") or meta.get("tags") or []
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    canonical = meta.get("canonical") or f"{SITE}/blog/{slug}/"
    author_name = meta.get("author") or "OctoProbe News"

    org = {
        "@type": "Organization",
        "name": "OctoProbe AI",
        "alternateName": ["OctoProbe", "OctoProbe.ai"],
        "url": f"{SITE}/",
        "logo": {
            "@type": "ImageObject",
            "url": f"{SITE}/icon-512.png",
            "width": 512,
            "height": 512,
        },
        "description": (
            "OctoProbe AI is an OSINT investigation platform from Redwing Technologies LLC "
            "that maps identifiers (email, phone, handle, domain, photo) onto a live "
            "investigation graph with evidence on every link."
        ),
        "email": "team@octoprobe.ai",
        "sameAs": [
            "https://x.com/octoprobeai",
            "https://www.octoprobe.ai/",
            "https://app.octoprobe.ai/",
        ],
        "parentOrganization": {
            "@type": "Organization",
            "name": "Redwing Technologies LLC",
            "url": "https://rook-intel.com/",
        },
    }

    blog_posting = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": title,
        "description": description,
        "datePublished": date,
        "dateModified": date_mod,
        "author": (AU.person_ld(_person) if (_person := AU.resolve_author(meta))
                   else {"@type": "Organization", "name": author_name, "url": f"{SITE}/blog/"}),
        "publisher": {"@type": "NewsMediaOrganization", "@id": f"{SITE}/blog/#newsroom", "name": "OctoProbe News", "url": f"{SITE}/blog/", "logo": org["logo"], "parentOrganization": org["parentOrganization"]},
        "image": [og_image],
        "keywords": ", ".join(keywords) if isinstance(keywords, list) else str(keywords),
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canonical,
        },
        "url": canonical,
        "isPartOf": {
            "@type": "Blog",
            "name": "OctoProbe News",
            "url": f"{SITE}/blog/",
        },
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [".answer-first", ".callout.takeaways", ".prose h2"],
        },
        "about": [
            {"@type": "Thing", "name": "OSINT"},
            {"@type": "Thing", "name": "identifier graph"},
            {"@type": "Thing", "name": "breach intelligence"},
            {"@type": "Thing", "name": "facial recognition OSINT"},
        ],
        "mentions": [
            {"@type": "Organization", "name": "OctoProbe AI"},
            {"@type": "Organization", "name": "Redwing Technologies"},
            {"@type": "Thing", "name": "MCP OSINT"},
        ],
    }

    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": canonical},
        ],
    }

    blocks = [blog_posting, breadcrumb]

    # FAQ / FAQPage intentionally not emitted: end-user posts carry no FAQ section.

    howto = meta.get("howto") or {}
    steps = howto.get("steps") if isinstance(howto, dict) else None
    if isinstance(steps, list) and steps:
        howto_steps = []
        for i, step in enumerate(steps, 1):
            if isinstance(step, dict):
                name = step.get("name") or f"Step {i}"
                text = step.get("text") or step.get("text") or ""
            else:
                name, text = f"Step {i}", str(step)
            howto_steps.append(
                {
                    "@type": "HowToStep",
                    "position": i,
                    "name": name,
                    "text": text,
                }
            )
        blocks.append(
            {
                "@context": "https://schema.org",
                "@type": "HowTo",
                "name": howto.get("name") or title,
                "description": description,
                "step": howto_steps,
            }
        )
    return blocks


# ── Build one post ───────────────────────────────────────────────────────────

def build_one(md_path: Path, *, strict: bool = True) -> dict:
    meta, body_md = parse_frontmatter(md_path.read_text(encoding="utf-8"))
    for w in validate_meta(meta, md_path, strict=strict):
        print(f"WARNING: {w}", file=sys.stderr)

    title = meta.get("title") or md_path.stem
    date = meta.get("date") or "1970-01-01"
    date_mod = meta.get("date_modified") or date
    slug = meta.get("slug") or md_path.stem
    tags = meta.get("tags") or []
    description = meta.get("description") or meta.get("excerpt") or title
    excerpt = meta.get("excerpt") or description
    canonical = meta.get("canonical") or f"{SITE}/blog/{slug}/"
    og_image = meta.get("og_image") or OG_DEFAULT
    keywords = meta.get("keywords") or tags
    if isinstance(keywords, list):
        keywords_str = ", ".join(keywords)
    else:
        keywords_str = str(keywords)

    try:
        dt = datetime.strptime(date[:10], "%Y-%m-%d")
        date_display = f"{dt.strftime('%b')} {dt.day}, {dt.year}"
    except ValueError:
        date_display = date

    tags_html = (
        '<div class="tags">'
        + "".join(f'<span class="{tag_class(t)}">{escape(t)}</span>' for t in tags)
        + "</div>"
    )

    body_html = md_to_html(body_md)

    answer_first = (meta.get("answer_first") or "").strip()
    primary_q = (meta.get("primary_question") or "").strip()
    if answer_first:
        # Avoid duplicating if author already pasted the same lede as first paragraph
        af_plain = re.sub(r"\s+", " ", answer_first).strip().lower()
        first_p = re.search(r"<p>(.*?)</p>", body_html, flags=re.S)
        first_plain = re.sub(r"<[^>]+>", "", first_p.group(1) if first_p else "")
        first_plain = re.sub(r"\s+", " ", first_plain).strip().lower()
        if af_plain not in first_plain:
            q_html = (
                f'<p class="primary-question"><strong>{escape(primary_q)}</strong></p>\n'
                if primary_q
                else ""
            )
            body_html = (
                f'{q_html}<p class="answer-first">{escape(answer_first)}</p>\n'
                + body_html
            )

    hero_src = meta.get("hero") or ""
    # Allow absolute site URL in og_image to imply local hero path
    if not hero_src and og_image and "/assets/blog/" in og_image:
        hero_src = "/" + og_image.split(".ai/", 1)[-1] if ".ai/" in og_image else og_image
        if hero_src.startswith("https://"):
            hero_src = ""
    hero_alt = meta.get("hero_alt") or title
    if hero_src:
        hero_html = (
            f'<figure class="post-featured">'
            f'<img src="{escape(hero_src)}" alt="{escape(hero_alt)}" '
            f'width="1280" height="720" loading="eager" decoding="async">'
            f'<figcaption class="sr-only">{escape(hero_alt)}</figcaption>'
            f'</figure>'
        )
    else:
        hero_html = ""
        print(f"WARNING: {md_path.name}: no hero/featured image — add hero: under assets/blog/", file=sys.stderr)

    # Author: Colin Aamot by default (byline + avatar, bio box, Person JSON-LD); see scripts/authors.py.
    # Front matter `author: OctoProbe Staff` (or OctoProbe / OctoProbe News) keeps the Organization byline.
    person = AU.resolve_author(meta)
    body_html = AU.insert_author_note(body_html, AU.author_note_html(person))

    ld_blocks = build_json_ld(meta, slug, description)
    ld_scripts = "\n".join(
        f'<script type="application/ld+json">\n{json.dumps(block, indent=2, ensure_ascii=False)}\n</script>'
        for block in ld_blocks
    )

    # Prefer a short browser title; keep brand
    browser_title = title if len(title) <= TITLE_SOFT_MAX else title[: TITLE_SOFT_MAX - 1].rstrip() + "…"
    page_title = f"{browser_title} · OctoProbe News"

    head_meta = f"""<title>{escape(page_title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="keywords" content="{escape(keywords_str)}">
<meta name="author" content="{escape(person['name'] if person else (meta.get('author') or 'OctoProbe News'))}">
<link rel="alternate" type="text/plain" title="LLM context (llms.txt)" href="/llms.txt">
<link rel="alternate" type="text/plain" title="AI discovery (ai.txt)" href="/ai.txt">
<link rel="alternate" type="application/rss+xml" title="OctoProbe News" href="https://www.octoprobe.ai/blog/feed.xml">
<meta name="ai-content-declaration" content="human-authored; product documentation and OSINT methodology">
<link rel="canonical" href="{escape(canonical)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="OctoProbe News">
<meta property="og:url" content="{escape(canonical)}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:image" content="{escape(og_image)}">
<meta property="og:image:alt" content="{escape(title)}">
<meta property="article:published_time" content="{escape(date)}">
<meta property="article:modified_time" content="{escape(date_mod)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@octoprobeai">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(description)}">
<meta name="twitter:image" content="{escape(og_image)}">
{ld_scripts}"""

    # Visible byline: the resolved author (with headshot); for Organization authors the
    # staff line, `byline:` overrides the visible name.
    byline_html = AU.byline_html(person, meta.get("byline") or "OctoProbe Staff")
    tpl = TEMPLATE.read_text(encoding="utf-8")
    html = (
        tpl.replace("{{HEAD_META}}", head_meta)
        .replace("{{TITLE}}", escape(title))
        .replace("{{DATE}}", escape(date))
        .replace("{{DATE_DISPLAY}}", escape(date_display))
        .replace("{{TAGS_HTML}}", tags_html)
        .replace("{{BYLINE_HTML}}", byline_html)
        .replace("{{SHARE_HTML}}", "\n      ".join(share_bar_html().split("\n")))
        .replace("{{HERO_HTML}}", hero_html)
        .replace("{{BODY}}", body_html)
    )

    out_dir = ROOT / "blog" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"built {out_path.relative_to(ROOT)}")

    return {
        "slug": slug,
        "title": title,
        "date": date,
        "date_modified": date_mod,
        "description": description,
        "excerpt": excerpt,
        "canonical": canonical,
        "og_image": og_image,
        "hero": hero_src,
        "tags": tags,
        "path": md_path,
    }


# ── Share bar ────────────────────────────────────────────────────────────────
# Default social share bar, injected directly under the top byline of EVERY post at build time.
# The build emits only the static container: inline SVG icons, aria labels, target/rel. It
# carries no per-post URLs or text. /assets/js/blog-share.js reads the page's own
# <link rel="canonical"> and <h1> (fallback og:title) at runtime, URL-encodes them and assembles
# every share href, the mailto, the copy-link value, the utm params and the GA4 `share` event,
# so each article is correct automatically. No third-party share scripts or trackers.
# The bar starts `hidden` and the JS reveals it (no JS = no dead buttons). Styles: `.share-bar`
# in /assets/css/blog.css. Idempotent: the block lives between SHARE_START / SHARE_END and is
# re-rendered in place, so markdown posts (via the template) and hand-built posts (via the
# refresh pass in main) carry byte-identical markup.

SHARE_START = "<!-- share-bar -->"
SHARE_END = "<!-- /share-bar -->"
SHARE_JS = "/assets/js/blog-share.js?v=share1"
SHARE_JS_TAG = f'<script src="{SHARE_JS}" defer></script>'

# Brand marks: Simple Icons paths (CC0-1.0, simple-icons 16.35.0; LinkedIn from 9.x, which still
# shipped it). 24x24 viewBox, single path, painted with currentColor (monochrome).
SHARE_ICONS = {
    "x": "M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 1.329 7.754 11.09h-3.182z",
    "facebook": "M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z",
    "linkedin": "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z",
    "reddit": "M12 0C5.373 0 0 5.373 0 12c0 3.314 1.343 6.314 3.515 8.485l-2.286 2.286C.775 23.225 1.097 24 1.738 24H12c6.627 0 12-5.373 12-12S18.627 0 12 0Zm4.388 3.199c1.104 0 1.999.895 1.999 1.999 0 1.105-.895 2-1.999 2-.946 0-1.739-.657-1.947-1.539v.002c-1.147.162-2.032 1.15-2.032 2.341v.007c1.776.067 3.4.567 4.686 1.363.473-.363 1.064-.58 1.707-.58 1.547 0 2.802 1.254 2.802 2.802 0 1.117-.655 2.081-1.601 2.531-.088 3.256-3.637 5.876-7.997 5.876-4.361 0-7.905-2.617-7.998-5.87-.954-.447-1.614-1.415-1.614-2.538 0-1.548 1.255-2.802 2.803-2.802.645 0 1.239.218 1.712.585 1.275-.79 2.881-1.291 4.64-1.365v-.01c0-1.663 1.263-3.034 2.88-3.207.188-.911.993-1.595 1.959-1.595Zm-8.085 8.376c-.784 0-1.459.78-1.506 1.797-.047 1.016.64 1.429 1.426 1.429.786 0 1.371-.369 1.418-1.385.047-1.017-.553-1.841-1.338-1.841Zm7.406 0c-.786 0-1.385.824-1.338 1.841.047 1.017.634 1.385 1.418 1.385.785 0 1.473-.413 1.426-1.429-.046-1.017-.721-1.797-1.506-1.797Zm-3.703 4.013c-.974 0-1.907.048-2.77.135-.147.015-.241.168-.183.305.483 1.154 1.622 1.964 2.953 1.964 1.33 0 2.47-.81 2.953-1.964.057-.137-.037-.29-.184-.305-.863-.087-1.795-.135-2.769-.135Z",
    "whatsapp": "M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z",
    "telegram": "M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z",
    "bluesky": "M5.202 2.857C7.954 4.922 10.913 9.11 12 11.358c1.087-2.247 4.046-6.436 6.798-8.501C20.783 1.366 24 .213 24 3.883c0 .732-.42 6.156-.667 7.037-.856 3.061-3.978 3.842-6.755 3.37 4.854.826 6.089 3.562 3.422 6.299-5.065 5.196-7.28-1.304-7.847-2.97-.104-.305-.152-.448-.153-.327 0-.121-.05.022-.153.327-.568 1.666-2.782 8.166-7.847 2.97-2.667-2.737-1.432-5.473 3.422-6.3-2.777.473-5.899-.308-6.755-3.369C.42 10.04 0 4.615 0 3.883c0-3.67 3.217-2.517 5.202-1.026",
}
# Line icons (email, link, share, check): 24x24, stroked with currentColor.
SHARE_LINE_ICONS = {
    "email": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
    "copy": '<path d="M10 13.5a4.5 4.5 0 0 0 6.4.4l3-3a4.5 4.5 0 0 0-6.4-6.4l-1.6 1.6"/><path d="M14 10.5a4.5 4.5 0 0 0-6.4-.4l-3 3a4.5 4.5 0 0 0 6.4 6.4l1.6-1.6"/>',
    "share": '<path d="M12 3v12"/><path d="m7.5 7.5 4.5-4.5 4.5 4.5"/><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
}

# (key, aria label, bare endpoint). Display order. The static href is only the network's bare
# share endpoint (identical on every post, keeps the markup valid); blog-share.js replaces it
# with the full URL built from the page's canonical + headline.
# Not included by design: any upgrade/support button, Truth Social, Gettr.
SHARE_NETWORKS = [
    ("x", "Share on X", "https://x.com/intent/post"),
    ("facebook", "Share on Facebook", "https://facebook.com/sharer/sharer.php"),
    ("linkedin", "Share on LinkedIn", "https://www.linkedin.com/sharing/share-offsite/"),
    ("reddit", "Share on Reddit", "https://www.reddit.com/submit"),
    ("whatsapp", "Share on WhatsApp", "https://api.whatsapp.com/send"),
    ("telegram", "Share on Telegram", "https://t.me/share/url"),
    ("bluesky", "Share on Bluesky", "https://bsky.app/intent/compose"),
    ("email", "Share by email", "mailto:"),
]


def _svg(key: str) -> str:
    if key in SHARE_ICONS:
        return (f'<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false">'
                f'<path d="{SHARE_ICONS[key]}"/></svg>')
    return (f'<svg class="share-ico-line" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" '
            f'focusable="false">{SHARE_LINE_ICONS[key]}</svg>')


def share_bar_html() -> str:
    """The static share bar block (between SHARE_START / SHARE_END). Same for every post."""
    items = []
    for key, label, endpoint in SHARE_NETWORKS:
        ext = "" if key == "email" else ' target="_blank" rel="noopener noreferrer"'
        items.append(f'<li><a class="share-link" href="{endpoint}" data-share="{key}"{ext} aria-label="{label}">'
                     f'{_svg(key)}</a></li>')
    items.append(f'<li class="share-copy-item"><button type="button" class="share-link share-copy" '
                 f'data-share="copy" aria-label="Copy link">{_svg("copy")}{_svg("check")}</button></li>')
    return (
        f'{SHARE_START}\n'
        f'<div class="share-bar" role="group" aria-label="Share this article" hidden>'
        f'<span class="share-label" aria-hidden="true">Share</span>'
        f'<button type="button" class="share-native" aria-label="Share this article">{_svg("share")}<span>Share</span></button>'
        f'<ul class="share-list">{"".join(items)}</ul>'
        f'<span class="share-status" role="status" aria-live="polite"></span>'
        f'</div>\n'
        f'{SHARE_END}'
    )


_BYLINE_RE = re.compile(r'(?P<ind>[ \t]*)<p class="byline(?: has-avatar)?">.*?</p>', re.S)
_SHARE_BLOCK_RE = re.compile(r"\n?[ \t]*" + re.escape(SHARE_START) + r".*?" + re.escape(SHARE_END), re.S)


def _page_title(html: str) -> str:
    from html import unescape
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if not m:
        raise BuildError("share bar: post has no <h1>")
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", m.group(1)))).strip()


def inject_share_bar(html: str, label: str = "") -> str:
    """Insert (or refresh) the share bar directly under the top byline, plus the share JS."""
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    if not canon:
        raise BuildError(f"{label}: share bar: no canonical link")
    if not canon.group(1).startswith(SITE + "/"):
        raise BuildError(f"{label}: share bar: canonical {canon.group(1)!r} is not on {SITE}")
    _page_title(html)  # blog-share.js reads the headline from the <h1>; fail the build if absent
    block = share_bar_html()
    html = _SHARE_BLOCK_RE.sub("", html)
    bylines = list(_BYLINE_RE.finditer(html))
    if len(bylines) != 1:
        raise BuildError(f"{label}: share bar: expected 1 top byline, found {len(bylines)}")
    m = bylines[0]
    ind = m.group("ind")
    html = html[: m.end()] + "\n" + "\n".join(ind + ln for ln in block.split("\n")) + html[m.end():]
    html = re.sub(r'<script src="/assets/js/blog-share\.js[^"]*" defer></script>\n?', "", html)
    if "</body>" not in html:
        raise BuildError(f"{label}: share bar: no </body>")
    html = html.replace("</body>", SHARE_JS_TAG + "\n</body>", 1)
    return html


def share_bar_targets() -> list[Path]:
    """Every live post: blog/<slug>/index.html with og:type article and a top byline
    (skips _template, redirect stubs, and the about/standards/... pages)."""
    out = []
    for p in sorted((ROOT / "blog").glob("*/index.html")):
        if p.parent.name.startswith(("_", ".")):
            continue
        html = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in html:
            continue
        if '<meta property="og:type" content="article">' in html and _BYLINE_RE.search(html):
            out.append(p)
    return out


def refresh_share_bars(check: bool = False) -> int:
    """Re-render the share bar in every built post (markdown-built and hand-built). Returns stale count."""
    stale = 0
    for p in share_bar_targets():
        old = p.read_text(encoding="utf-8")
        new = inject_share_bar(old, str(p.relative_to(ROOT)))
        if new != old:
            stale += 1
            if not check:
                p.write_text(new, encoding="utf-8")
                print(f"share bar: refreshed {p.relative_to(ROOT)}")
    return stale


# ── Screenshot lightbox ──────────────────────────────────────────────────────
# Phone and app screenshots, plus other images that render about 800px tall or more at the
# 722px column (height/width >= SHOT_RATIO), are shown at ~1/3 of the column (~60% on phones)
# and open in the shared modal (/assets/css/blog-lightbox.css, /assets/js/blog-lightbox.js):
#   <figure class="shot-mobile"><a class="shot-open" href="IMG" aria-haspopup="dialog"><img …></a>…
# The <img> (src, alt, width, height, loading) is left byte-identical. Idempotent: the pass
# unwraps its own markup and re-applies it, including on hand-built posts. It only rewrites a
# plain <figure> whose image is a direct child or the sole child of an <a href> pointing at
# that same file. Classed figures (doc-fig, fig-pad, doc-page, portrait, ixm-fig, post-featured)
# are left alone, so document layouts and the Secret Service lightbox stay as they are.
# LIGHTBOX_INCLUDE forces a screenshot the ratio misses (near-square phone captures, or an
# <img> with no width/height). LIGHTBOX_EXCLUDE keeps a tall figure full width (a scanned
# page, a graph, a narrow sidebar). --lightbox-only --check fails if either list is stale.

SHOT_RATIO = 1.2
# Basename of the img src (query string ignored).
LIGHTBOX_INCLUDE = {
    "archive-today-donate-link-takion-api-developer": {
        "bmc-glizzykingdreko-disclaimer.png",  # mobile Buy Me a Coffee page, 980x1160, no width/height attrs
    },
    "christopher-burns-fbi-fugitive-google-maps-wayne-pa": {
        "fbi-christopher-w-burns.png",  # mobile FBI wanted page, 692x950, no width/height attrs
    },
    "gaza-now-telegram-hamas-fundraising-sanctions-sabassi": {
        "telegram-gaza-now-egypt-donation-numbers.jpg",  # near-square Telegram capture, 1000x1042
    },
    "heather-zhang-prc-agent-case-reddit-allegation": {
        "reddit-allegation-ludepress.png",  # mobile article screenshot, 717x880, no width/height attrs
    },
    "machiaveli-dark-web-cocaine-spokane-nabi": {
        "telegram-machiaveli-channel.png",  # Telegram channel card, 542x612 (ratio 1.13)
    },
}
LIGHTBOX_EXCLUDE = {
    "foia-how-to-obama-situation-room-photos-presidential-records": {
        "foia-24-09538-f-response-letter-p1-redacted.png",  # one US-letter response page, not a phone capture
    },
    "myrotvorets-informnapalm-ned-grant": {
        "foia-fl-2020-00028-sytnyk-uglava-counterespionage-email.png",  # one FOIA email page
        "myrotvorets-our-projects-sidebar-identigraf-ordilo.png",  # 212px-wide sidebar, stays at intrinsic size
        "myrotvorets-sidebar-help-the-project-donations-site-mirrors-tor.png",  # 246px-wide sidebar
        "octoprobe-myrotvorets-informnapalm-ned-investigation-graph.png",  # investigation graph
    },
    "white-house-vetting-leak-press-clips": {
        "giuliani-business-ties-research-page-1.png",  # one scanned research page
    },
}
LIGHTBOX_CSS_TAG = '<link rel="stylesheet" href="/assets/css/blog-lightbox.css?v=lb1">'
LIGHTBOX_JS_TAG = '<script src="/assets/js/blog-lightbox.js?v=lb1" defer></script>'
_SHOT_WRAPPED_RE = re.compile(r'<figure class="shot-mobile"><a class="shot-open" href="[^"]*" aria-haspopup="dialog">(<img\b[^>]*>)</a>')
# Plain figure: direct <img>, or <a href="THE IMAGE"><img></a>. No other figure class.
_PLAIN_FIG_RE = re.compile(
    r'<figure>(?:\s*<a href="([^"]*)">\s*(<img\b[^>]*>)\s*</a>|\s*(<img\b[^>]*>))'
)


def _attr(tag: str, name: str) -> str | None:
    m = re.search(r'\s' + name + r'="([^"]*)"', tag)
    return m.group(1) if m else None


def _src_name(src: str) -> str:
    return src.split("?", 1)[0].rsplit("/", 1)[-1]


def apply_lightbox(html: str, label: str = "", slug: str = "") -> str:
    """(Re)apply the screenshot thumbnail + lightbox markup to one post."""
    include = LIGHTBOX_INCLUDE.get(slug, ())
    exclude = LIGHTBOX_EXCLUDE.get(slug, ())
    html = _SHOT_WRAPPED_RE.sub(r"<figure>\1", html)
    html = html.replace(LIGHTBOX_CSS_TAG + "\n", "").replace(LIGHTBOX_JS_TAG + "\n", "")

    def wrap(m: re.Match) -> str:
        href, img = (m.group(1), m.group(2)) if m.group(2) else (None, m.group(3))
        src = _attr(img, "src") or ""
        name = _src_name(src)
        if href and _src_name(href) != name:
            return m.group(0)  # the link opens a different file than the one shown
        if name in exclude:
            return m.group(0)
        w, h = _attr(img, "width"), _attr(img, "height")
        tall = bool(w and h and w.isdigit() and h.isdigit() and int(w) > 0 and int(h) / int(w) >= SHOT_RATIO)
        if name not in include and not tall:
            return m.group(0)
        if not (_attr(img, "alt") or "").strip():
            raise BuildError(f"{label}: lightbox: figure image {src!r} has no alt text")
        return f'<figure class="shot-mobile"><a class="shot-open" href="{src}" aria-haspopup="dialog">{img}</a>'

    html, n = _PLAIN_FIG_RE.subn(wrap, html)
    for name in sorted(include):
        if not re.search(
            r'<figure class="shot-mobile"><a class="shot-open" href="[^"]*' + re.escape(name) + r'"',
            html,
        ):
            raise BuildError(
                f"{label}: lightbox: included screenshot {name!r} is not wrapped "
                "(missing from the post, or not a plain <figure><img>)"
            )
    for name in sorted(exclude):
        if re.search(r'class="shot-open" href="[^"]*' + re.escape(name), html):
            raise BuildError(f"{label}: lightbox: excluded image {name!r} was wrapped")
    if 'class="shot-mobile"' not in html:
        return html
    css = re.search(r'<link rel="stylesheet" href="/assets/css/blog\.css[^"]*">\n?', html)
    if not css:
        raise BuildError(f"{label}: lightbox: no blog.css link to anchor the lightbox CSS")
    html = html[: css.end()] + ("" if css.group(0).endswith("\n") else "\n") + LIGHTBOX_CSS_TAG + "\n" + html[css.end():]
    # Sit just before the share-bar script, which inject_share_bar() keeps last before </body>,
    # so the two passes leave each other's output unchanged.
    if SHARE_JS_TAG in html:
        return html.replace(SHARE_JS_TAG, LIGHTBOX_JS_TAG + "\n" + SHARE_JS_TAG, 1)
    if "</body>" not in html:
        raise BuildError(f"{label}: lightbox: no </body>")
    return html.replace("</body>", LIGHTBOX_JS_TAG + "\n</body>", 1)


def refresh_lightbox(check: bool = False) -> int:
    """Apply the lightbox pass to every live post. Returns the stale count."""
    stale = 0
    posts = share_bar_targets()
    for p in posts:
        slug = p.parent.name
        old = p.read_text(encoding="utf-8")
        new = apply_lightbox(old, str(p.relative_to(ROOT)), slug)
        if new != old:
            stale += 1
            if not check:
                p.write_text(new, encoding="utf-8")
                print(f"lightbox: refreshed {p.relative_to(ROOT)}")
    return stale


# ── Sitemap + llms.txt ───────────────────────────────────────────────────────

def regenerate_sitemap(posts: list[dict]) -> None:
    """Keep homepage; rewrite blog index + post URLs from built posts."""
    today = datetime.now().strftime("%Y-%m-%d")
    # Prefer newest post date for blog index lastmod
    blog_last = max((p.get("date_modified") or p.get("date") or today for p in posts), default=today)

    urls = [
        {
            "loc": f"{SITE}/",
            "lastmod": today,
            "changefreq": "monthly",
            "priority": "1.0",
            "image": (OG_DEFAULT, "OctoProbe AI — Every OSINT tool. One investigation graph."),
        },
        {
            "loc": f"{SITE}/blog/",
            "lastmod": blog_last,
            "changefreq": "weekly",
            "priority": "0.8",
            "image": None,
        },
    ]
    for p in sorted(posts, key=lambda x: x.get("date") or "", reverse=True):
        urls.append(
            {
                "loc": p["canonical"],
                "lastmod": p.get("date_modified") or p.get("date") or today,
                "changefreq": "monthly",
                "priority": "0.7",
                "image": (p.get("og_image") or OG_DEFAULT, p["title"]),
            }
        )

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(u['loc'])}</loc>")
        lines.append(f"    <lastmod>{escape(u['lastmod'])}</lastmod>")
        lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        lines.append(f"    <priority>{u['priority']}</priority>")
        if u.get("image"):
            loc, title = u["image"]
            lines.append("    <image:image>")
            lines.append(f"      <image:loc>{escape(loc)}</image:loc>")
            lines.append(f"      <image:title>{escape(title)}</image:title>")
            lines.append("    </image:image>")
        lines.append("  </url>")
    lines.append("</urlset>")
    lines.append("")
    SITEMAP.write_text("\n".join(lines), encoding="utf-8")
    print(f"updated {SITEMAP.relative_to(ROOT)}")


def refresh_llms_blog_section(posts: list[dict]) -> None:
    """Replace or append the ## Blog / Findings section from post metadata."""
    blog_lines = [
        "## Blog / Findings",
        "",
        "Methodology notes on identifier graphs, breach correlation, and public OSINT practice. "
        "Each post leads with a definitional answer so search and chat engines can cite it.",
        "",
        f"- Blog index: {SITE}/blog/ — OSINT investigation platform findings: identifier graphs, expansion layers, evidence discipline",
    ]
    for p in sorted(posts, key=lambda x: x.get("date") or "", reverse=True):
        abstract = (p.get("excerpt") or p.get("description") or "").strip()
        # one-line abstract
        abstract = re.sub(r"\s+", " ", abstract)
        if len(abstract) > 180:
            abstract = abstract[:177].rstrip() + "…"
        blog_lines.append(f"- {p['title']} — {p['canonical']} — {abstract}")
    blog_block = "\n".join(blog_lines) + "\n"

    for path in LLMS_PATHS:
        if not path.exists():
            print(f"WARNING: {path.relative_to(ROOT)} missing — skip llms refresh", file=sys.stderr)
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"^## Blog / Findings\b", text, re.M):
            text = re.sub(
                r"^## Blog / Findings\b.*?(?=^## |\Z)",
                blog_block + "\n",
                text,
                count=1,
                flags=re.M | re.S,
            )
        else:
            text = text.rstrip() + "\n\n" + blog_block
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)} blog section")


def load_all_post_metas() -> list[dict]:
    """Parse all posts for sitemap/llms without rebuilding HTML."""
    posts = []
    for md_path in sorted(POSTS_DIR.glob("*.md")):
        meta, _ = parse_frontmatter(md_path.read_text(encoding="utf-8"))
        slug = meta.get("slug") or md_path.stem
        description = meta.get("description") or meta.get("excerpt") or meta.get("title") or slug
        posts.append(
            {
                "slug": slug,
                "title": meta.get("title") or slug,
                "date": meta.get("date") or "",
                "date_modified": meta.get("date_modified") or meta.get("date") or "",
                "description": description,
                "excerpt": meta.get("excerpt") or description,
                "canonical": meta.get("canonical") or f"{SITE}/blog/{slug}/",
                "og_image": meta.get("og_image") or OG_DEFAULT,
                "tags": meta.get("tags") or [],
                "path": md_path,
            }
        )
    return posts


def main():
    flags = {"--no-strict", "--share-only", "--lightbox-only", "--check"}
    strict = "--no-strict" not in sys.argv
    args = [Path(a) for a in sys.argv[1:] if a not in flags]

    # --share-only: refresh just the share bar in every built post (no markdown rebuild; the
    # markdown builders' output has been hand-edited since, so a full rebuild is not byte-safe).
    # --share-only --check: exit 1 if any post is missing the bar or carries a stale one (CI).
    if "--share-only" in sys.argv:
        try:
            stale = refresh_share_bars(check="--check" in sys.argv)
        except BuildError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        if "--check" in sys.argv:
            if stale:
                print(f"{stale} post(s) have a missing or stale share bar. Run: python3 scripts/build-blog.py --share-only",
                      file=sys.stderr)
                sys.exit(1)
            print(f"share bar is up to date on {len(share_bar_targets())} posts")
        return

    # --lightbox-only: (re)apply the screenshot lightbox on every live post.
    # --lightbox-only --check: exit 1 if a plain-figure screenshot is missing its markup,
    # or an include/exclude override does not match the page (CI preflight).
    if "--lightbox-only" in sys.argv:
        try:
            stale = refresh_lightbox(check="--check" in sys.argv)
        except BuildError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        if "--check" in sys.argv:
            if stale:
                print(f"{stale} post(s) have screenshot lightbox markup that does not match the pass. "
                      "Run: python3 scripts/build-blog.py --lightbox-only", file=sys.stderr)
                sys.exit(1)
            print(f"lightbox markup is up to date on {len(share_bar_targets())} post(s)")
        return

    if args:
        paths = [a if a.is_absolute() else ROOT / a for a in args]
    else:
        paths = sorted(POSTS_DIR.glob("*.md"))
    if not paths:
        print("No markdown posts found in blog/posts/", file=sys.stderr)
        sys.exit(1)

    built: list[dict] = []
    errors = 0
    for p in paths:
        try:
            built.append(build_one(p, strict=strict))
        except BuildError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            errors += 1
    if errors:
        sys.exit(1)

    # Share bar on every post, including hand-built posts that have no markdown source.
    try:
        refresh_share_bars()
        refresh_lightbox()
    except BuildError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Always regenerate sitemap/llms from the full posts corpus so a one-file
    # build does not drop other URLs.
    all_posts = load_all_post_metas()
    # Prefer freshly built description/title if present
    by_slug = {p["slug"]: p for p in all_posts}
    for b in built:
        by_slug[b["slug"]] = b
    corpus = list(by_slug.values())
    # Sitemap comes from the built HTML (covers hand-built posts too); see scripts/gen-sitemap.py
    import runpy
    runpy.run_path(str(ROOT / "scripts" / "gen-sitemap.py"), run_name="__main__")
    refresh_llms_blog_section(corpus)


if __name__ == "__main__":
    main()
