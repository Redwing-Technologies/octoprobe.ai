#!/usr/bin/env python3
"""Regenerate sitemap.xml from the built site (homepage, /blog/, every blog/<slug>/index.html except redirect stubs,
and every author page blog/authors/<name>/index.html, which sits two directory levels under blog/).

The published HTML is the source of truth, so hand-built posts are included too.
Per page it reads: canonical URL, og:title, og:image (query string stripped) and the
JSON-LD dateModified (falls back to datePublished). /blog/ lastmod = newest post.
Output is deterministic (no "today" dates), so CI can diff it.

Usage (repo root):
  python3 scripts/gen-sitemap.py          # write sitemap.xml
  python3 scripts/gen-sitemap.py --check  # exit 1 if sitemap.xml is stale
No third-party packages.
"""
from __future__ import annotations

import re
import sys
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITEMAP = ROOT / "sitemap.xml"
SITE = "https://www.octoprobe.ai"


def meta(html: str, prop: str) -> str | None:
    m = re.search(r'<meta\s+(?:property|name)="%s"\s+content="([^"]*)"' % re.escape(prop), html)
    return unescape(m.group(1)) if m else None


def page(path: Path) -> dict:
    html = path.read_text(encoding="utf-8")
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    if not canon:
        raise SystemExit(f"ERROR: {path.relative_to(ROOT)} has no canonical link")
    mod = re.search(r'"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})', html) or re.search(
        r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', html)
    img = meta(html, "og:image")
    return {
        "loc": canon.group(1),
        "lastmod": mod.group(1) if mod else None,
        "title": meta(html, "og:title") or "",
        "image": img.split("?")[0] if img else None,
        "published": (re.search(r'"datePublished"\s*:\s*"([^"]+)"', html) or [None, ""])[1],
    }


def live_pages(pattern: str) -> list[dict]:
    """Pages matching blog/<pattern>, minus _/. dirs and redirect stubs."""
    out = []
    for p in sorted((ROOT / "blog").glob(pattern)):
        if any(part.startswith(("_", ".")) for part in p.relative_to(ROOT / "blog").parts[:-1]):
            continue
        if 'http-equiv="refresh"' in p.read_text(encoding="utf-8"):
            continue  # redirect stub for a moved URL; only live URLs go in the sitemap
        d = page(p)
        if not d["lastmod"]:
            raise SystemExit(f"ERROR: {p.relative_to(ROOT)} has no JSON-LD dateModified/datePublished")
        out.append(d)
    return out


def build() -> str:
    home = page(ROOT / "index.html")
    posts = live_pages("*/index.html")
    # Author pages are two levels deep (blog/authors/<name>/index.html), so the one-level glob above
    # never sees them. lastmod = the ProfilePage dateModified (stamped by scripts/build-author-page.py).
    authors = sorted(live_pages("authors/*/index.html"), key=lambda d: d["loc"])
    posts.sort(key=lambda d: (d["published"], d["lastmod"], d["loc"]))
    blog_last = max(d["lastmod"] for d in posts) if posts else home["lastmod"]
    urls = [
        dict(loc=f"{SITE}/", lastmod=home["lastmod"], cf="monthly", pr="1.0",
             img=(home["image"], home["title"])),
        dict(loc=f"{SITE}/blog/", lastmod=blog_last, cf="weekly", pr="0.8", img=None),
    ] + [dict(loc=d["loc"], lastmod=d["lastmod"], cf="monthly", pr="0.7",
              img=(d["image"], d["title"]) if d["image"] else None) for d in posts] + [
        dict(loc=d["loc"], lastmod=d["lastmod"], cf="monthly", pr="0.6",
             img=(d["image"], d["title"]) if d["image"] else None) for d in authors]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"',
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for u in urls:
        out += ["  <url>", f"    <loc>{escape(u['loc'])}</loc>"]
        if u["lastmod"]:
            out.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        out += [f"    <changefreq>{u['cf']}</changefreq>", f"    <priority>{u['pr']}</priority>"]
        if u["img"]:
            out += ["    <image:image>", f"      <image:loc>{escape(u['img'][0])}</image:loc>",
                    f"      <image:title>{escape(u['img'][1], quote=False)}</image:title>", "    </image:image>"]
        out.append("  </url>")
    out += ["</urlset>", ""]
    return "\n".join(out)


def main() -> None:
    new = build()
    if "--check" in sys.argv:
        old = SITEMAP.read_text(encoding="utf-8") if SITEMAP.exists() else ""
        if old != new:
            print("sitemap.xml is stale. Run: python3 scripts/gen-sitemap.py", file=sys.stderr)
            sys.exit(1)
        print("sitemap.xml is up to date")
        return
    SITEMAP.write_text(new, encoding="utf-8")
    print(f"updated {SITEMAP.relative_to(ROOT)} ({new.count('<url>')} URLs)")


if __name__ == "__main__":
    main()
