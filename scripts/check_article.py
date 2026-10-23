#!/usr/bin/env python3
"""Fail a post that misses the share, title, description, hero, or in-body link bar.

Title, description, and share tags are read from <head>. The in-body link count
uses only the <article> element, and it ignores a More-from box or Related
Reading list that sits inside that element.

The two-link minimum applies to posts whose JSON-LD datePublished is on or
after 2026-10-22. Older investigations are not failed for link count: adding
new sentences to them was outside the posts this audit asked to cross-link.

  python3 scripts/check_article.py
"""
from __future__ import annotations

import re
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.octoprobe.ai"
TITLE_MAX = 60
DESC_MAX = 160
HERO_MAX = 500 * 1024
LINK_MIN = 2
LINK_MIN_FROM = "2026-10-22"
SKIP_SLUGS = {"about", "standards", "corrections", "contact", "authors"}
SHARE_TAGS = (
    "og:site_name",
    "og:title",
    "og:description",
    "og:image",
    "og:image:alt",
    "og:url",
    "og:type",
    "twitter:card",
    "twitter:site",
    "twitter:title",
    "twitter:description",
    "twitter:image",
    "twitter:image:alt",
)


def meta_map(html: str) -> dict[str, str]:
    found: dict[str, str] = {}
    for m in re.finditer(r"<meta\s+(?:name|property)=\"([^\"]+)\"\s+content=\"([^\"]*)\"", html):
        found[m.group(1)] = unescape(m.group(2)).strip()
    for m in re.finditer(r"<meta\s+content=\"([^\"]*)\"\s+(?:name|property)=\"([^\"]+)\"", html):
        found.setdefault(m.group(2), unescape(m.group(1)).strip())
    return found


def local_file(url: str, html_path: Path) -> Path | None:
    raw = unescape(url).split("?", 1)[0].split("#", 1)[0].strip()
    if raw.startswith(SITE + "/"):
        raw = raw[len(SITE):]
    if raw.startswith("/"):
        return ROOT / raw.lstrip("/")
    if raw.startswith(("http://", "https://")):
        return None
    return (html_path.parent / raw).resolve()


def article_html(html: str) -> str:
    m = re.search(r"<article\b.*?</article>", html, re.S)
    if not m:
        return ""
    chunk = m.group(0)
    chunk = re.sub(r"<aside\b[^>]*class=\"[^\"]*more-from[^\"]*\"[^>]*>.*?</aside>", "", chunk, flags=re.S)
    chunk = re.sub(r"<aside\b[^>]*class=\"[^\"]*related-reading[^\"]*\"[^>]*>.*?</aside>", "", chunk, flags=re.S)
    return chunk


def internal_slugs(chunk: str, slug: str) -> set[str]:
    slugs: set[str] = set()
    for href in re.findall(r"href=\"([^\"]+)\"", chunk):
        raw = unescape(href).split("#", 1)[0].split("?", 1)[0]
        if raw.startswith(SITE):
            raw = raw[len(SITE):]
        if not raw.startswith("/blog/"):
            continue
        parts = [p for p in raw.strip("/").split("/") if p]
        if len(parts) < 2 or parts[0] != "blog":
            continue
        other = parts[1]
        if other in SKIP_SLUGS or other == slug or "." in other:
            continue
        slugs.add(other)
    return slugs


def hero_bytes(html: str, html_path: Path) -> tuple[int, str]:
    im = re.search(r"<img\b[^>]*fetchpriority=\"high\"[^>]*>", html)
    if not im:
        return -1, "no fetchpriority=high hero"
    pre = html[max(0, im.start() - 1500):im.start()]
    srcset = re.search(r"srcset=\"([^\"]+)\"", pre)
    if srcset and "image/webp" in pre:
        largest = 0
        missing = ""
        for part in srcset.group(1).split(","):
            url = part.strip().split(" ")[0]
            f = local_file(url, html_path)
            if f is None or not f.is_file():
                missing = url
                continue
            largest = max(largest, f.stat().st_size)
        if missing and largest == 0:
            return -1, f"hero file missing: {missing}"
        return largest, "webp srcset"
    src = re.search(r"src=\"([^\"]+)\"", im.group(0))
    if not src:
        return -1, "hero img has no src"
    f = local_file(src.group(1), html_path)
    if f is None or not f.is_file():
        return -1, f"hero file missing: {src.group(1)}"
    return f.stat().st_size, f.name


def check(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    slug = path.parent.name
    if 'http-equiv="refresh"' in html[:800] or "NewsArticle" not in html:
        return []
    errors: list[str] = []
    rel = str(path.relative_to(ROOT))
    title_m = re.search(r"<title>(.*?)</title>", html, re.S)
    title = unescape(title_m.group(1)) if title_m else ""
    title = re.sub(r"\s+", " ", title).strip()
    title = re.sub(r"\s+·\s+OctoProbe News$", "", title)
    if len(title) > TITLE_MAX:
        errors.append(f"{rel}: <title> is {len(title)} characters")
    metas = meta_map(html)
    desc = metas.get("description", "")
    if len(desc) > DESC_MAX:
        errors.append(f"{rel}: meta description is {len(desc)} characters")
    for key in ("og:description", "twitter:description"):
        if key in metas and len(metas[key]) > DESC_MAX:
            errors.append(f"{rel}: {key} is {len(metas[key])} characters")
    missing = [key for key in SHARE_TAGS if not metas.get(key)]
    if missing:
        errors.append(f"{rel}: missing share tags: {', '.join(missing)}")
    size, note = hero_bytes(html, path)
    if size < 0:
        errors.append(f"{rel}: {note}")
    elif size > HERO_MAX:
        errors.append(f"{rel}: hero is {size} bytes ({note})")
    published = re.search(r"\"datePublished\"\s*:\s*\"(\d{4}-\d{2}-\d{2})", html)
    day = published.group(1) if published else ""
    if day >= LINK_MIN_FROM:
        chunk = article_html(html)
        if not chunk:
            errors.append(f"{rel}: no <article> element")
        else:
            n = len(internal_slugs(chunk, slug))
            if n < LINK_MIN:
                errors.append(f"{rel}: {n} in-article links to other posts")
    return errors


def main() -> int:
    errors: list[str] = []
    posts = 0
    for path in sorted((ROOT / "blog").glob("*/index.html")):
        if path.parent.name.startswith("_"):
            continue
        found = check(path)
        if path.read_text(encoding="utf-8").find("NewsArticle") != -1 and 'http-equiv="refresh"' not in path.read_text(encoding="utf-8")[:800]:
            posts += 1
        errors.extend(found)
    if errors:
        for msg in errors:
            print(f"ERROR: {msg}", file=sys.stderr)
        print(f"{len(errors)} article check(s) failed", file=sys.stderr)
        return 1
    print(f"article checks passed for {posts} posts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
