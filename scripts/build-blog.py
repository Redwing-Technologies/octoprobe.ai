#!/usr/bin/env python3
"""Build OctoProbe blog posts from Markdown into HTML shells.

SEO / AEO / chat-engine aware:
  - Requires title, description, date, tags (warns/fails on gaps)
  - Injects BlogPosting + BreadcrumbList (no FAQPage; posts have no FAQ section)
  - Validates title/description length
  - Regenerates sitemap.xml via scripts/gen-sitemap.py (from all built HTML)
  - Refreshes the Blog section in llms.txt and .well-known/llms.txt

Usage (from landing repo root):
  python3 scripts/build-blog.py
  python3 scripts/build-blog.py blog/posts/identifier-graph-osint-methodology.md

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
        dt = datetime.strptime(date, "%Y-%m-%d")
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
    args = [Path(a) for a in sys.argv[1:]]
    strict = "--no-strict" not in sys.argv
    args = [a for a in args if str(a) != "--no-strict"]

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
