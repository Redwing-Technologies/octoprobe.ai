#!/usr/bin/env python3
"""Build OctoProbe blog posts from Markdown sources into HTML shells.

Usage (from landing repo root):
  python3 scripts/build-blog.py
  python3 scripts/build-blog.py blog/posts/2026-10-15-identifier-graph-methodology.md

No remote deploy — write local HTML only. Requires no third-party packages.
"""
from __future__ import annotations

import re
import sys
from datetime import datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "blog" / "posts"
TEMPLATE = ROOT / "blog" / "_template.html"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    fm_raw = text[3:end].strip()
    body = text[end + 4 :].lstrip("\n")
    meta: dict = {}
    for line in fm_raw.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            meta[k] = [p.strip().strip("\"'") for p in inner.split(",") if p.strip()]
        else:
            meta[k] = v.strip("\"'")
    return meta, body


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

    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows:
            return
        # drop separator row
        rows = [r for r in table_rows if not all(re.match(r"^:?-+:?$", c.strip()) for c in r)]
        if not rows:
            table_rows = []
            in_table = False
            return
        out.append("<table>")
        for ri, row in enumerate(rows):
            tag = "th" if ri == 0 else "td"
            out.append("<tr>" + "".join(f"<{tag}>{inline_md(c.strip())}</{tag}>" for c in row) + "</tr>")
        out.append("</table>")
        # style tables lightly via prose — add class wrapper
        # wrap last table
        table_rows = []
        in_table = False

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
            # wrap table in a figure-like block by rewriting last emission — simpler: flush now
            # Convert accumulated rows
            rows = [r for r in table_rows if not all(re.match(r"^:?-+:?$", c.strip()) for c in r)]
            if rows:
                html = ['<div class="callout"><strong>Identifier examples</strong>']
                # Actually render as real table inside prose
                t = ["<table>"]
                for ri, row in enumerate(rows):
                    tag = "th" if ri == 0 else "td"
                    t.append("<tr>" + "".join(f"<{tag}>{inline_md(c.strip())}</{tag}>" for c in row) + "</tr>")
                t.append("</table>")
                out.append("\n".join(t))
            table_rows = []
            in_table = False
            # fall through to process current line

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
            out.append(f"<h2>{inline_md(stripped[3:])}</h2>")
            i += 1
            continue
        if stripped.startswith("# "):
            # title usually in frontmatter / hero — skip duplicate H1 in body
            i += 1
            continue

        m = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if m:
            close_lists() if in_ul else None
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

        # paragraph — gather consecutive non-empty non-special lines
        close_lists()
        para = [stripped]
        i += 1
        while i < len(lines):
            n = lines[i].strip()
            if not n or n.startswith("#") or n.startswith("- ") or n.startswith("|") or n.startswith(">") or n == "---" or re.match(r"^\d+\.\s+", n):
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
    # light table styling hook
    html = html.replace("<table>", '<table style="width:100%;border-collapse:collapse;font-size:.92rem;margin:1.2em 0">')
    html = re.sub(r"<th>", '<th style="text-align:left;font-family:var(--fm);font-size:.58rem;letter-spacing:.1em;text-transform:uppercase;color:var(--soft-2);padding:8px 10px;border-bottom:1px solid var(--line);font-weight:500">', html)
    html = re.sub(r"<td>", '<td style="padding:10px;border-bottom:1px solid var(--line);color:var(--text)">', html)
    return html


def tag_class(tag: str) -> str:
    t = tag.lower()
    if "osint" in t:
        return "tag blue"
    if "graph" in t or "identifier" in t:
        return "tag teal"
    return "tag"


def build_one(md_path: Path) -> Path:
    meta, body_md = parse_frontmatter(md_path.read_text(encoding="utf-8"))
    title = meta.get("title") or md_path.stem
    date = meta.get("date") or "1970-01-01"
    slug = meta.get("slug") or md_path.stem
    tags = meta.get("tags") or []
    excerpt = meta.get("excerpt") or ""

    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
        date_display = dt.strftime("%b %-d, %Y") if sys.platform != "win32" else dt.strftime("%b %d, %Y")
        # macOS %-d works; fallback
    except ValueError:
        date_display = date
    # Normalize day without leading zero portably
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
        date_display = f"{dt.strftime('%b')} {dt.day}, {dt.year}"
    except ValueError:
        pass

    tags_html = '<div class="tags">' + "".join(
        f'<span class="{tag_class(t)}">{escape(t)}</span>' for t in tags
    ) + "</div>"

    body_html = md_to_html(body_md)

    # Append disclaimer callout if not already in body
    if "FCRA" not in body_html:
        body_html += (
            '\n<div class="callout"><strong>Public OSINT · not FCRA</strong>'
            "This writeup covers public-OSINT methodology with fictional examples. "
            "OctoProbe is not a consumer reporting agency; results may not be used for "
            "FCRA-covered eligibility decisions.</div>"
        )

    head_meta = f"""<title>{escape(title)} · OctoProbe Findings</title>
<meta name="description" content="{escape(excerpt or title)}">
<link rel="canonical" href="https://www.octoprobe.ai/blog/{escape(slug)}/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="OctoProbe AI">
<meta property="og:url" content="https://www.octoprobe.ai/blog/{escape(slug)}/">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(excerpt or title)}">
<meta property="og:image" content="https://www.octoprobe.ai/og-image.png">
<meta property="article:published_time" content="{escape(date)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(excerpt or title)}">
<meta name="twitter:image" content="https://www.octoprobe.ai/og-image.png">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": {escape(title)!r}.replace("\\\\'", "'"),
  "datePublished": "{escape(date)}",
  "description": {escape(excerpt or title)!r}.replace("\\\\'", "'"),
  "author": {{"@type": "Organization", "name": "OctoProbe AI"}},
  "publisher": {{"@type": "Organization", "name": "OctoProbe AI", "url": "https://www.octoprobe.ai/"}},
  "mainEntityOfPage": "https://www.octoprobe.ai/blog/{escape(slug)}/"
}}
</script>"""
    # Fix JSON-LD properly
    import json
    ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "datePublished": date,
        "description": excerpt or title,
        "author": {"@type": "Organization", "name": "OctoProbe AI"},
        "publisher": {"@type": "Organization", "name": "OctoProbe AI", "url": "https://www.octoprobe.ai/"},
        "mainEntityOfPage": f"https://www.octoprobe.ai/blog/{slug}/",
    }
    head_meta = f"""<title>{escape(title)} · OctoProbe Findings</title>
<meta name="description" content="{escape(excerpt or title)}">
<link rel="canonical" href="https://www.octoprobe.ai/blog/{escape(slug)}/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="OctoProbe AI">
<meta property="og:url" content="https://www.octoprobe.ai/blog/{escape(slug)}/">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(excerpt or title)}">
<meta property="og:image" content="https://www.octoprobe.ai/og-image.png">
<meta property="article:published_time" content="{escape(date)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(excerpt or title)}">
<meta name="twitter:image" content="https://www.octoprobe.ai/og-image.png">
<script type="application/ld+json">
{json.dumps(ld, indent=2)}
</script>"""

    tpl = TEMPLATE.read_text(encoding="utf-8")
    html = (
        tpl.replace("{{HEAD_META}}", head_meta)
        .replace("{{TITLE}}", escape(title))
        .replace("{{DATE}}", escape(date))
        .replace("{{DATE_DISPLAY}}", escape(date_display))
        .replace("{{TAGS_HTML}}", tags_html)
        .replace("{{BODY}}", body_html)
    )

    out_dir = ROOT / "blog" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"built {out_path.relative_to(ROOT)}")
    return out_path


def main():
    args = [Path(a) for a in sys.argv[1:]]
    if args:
        paths = [a if a.is_absolute() else ROOT / a for a in args]
    else:
        paths = sorted(POSTS_DIR.glob("*.md"))
    if not paths:
        print("No markdown posts found in blog/posts/", file=sys.stderr)
        sys.exit(1)
    for p in paths:
        build_one(p)


if __name__ == "__main__":
    main()
