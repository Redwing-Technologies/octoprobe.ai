#!/usr/bin/env python3
"""Regenerate blog/feed.xml (RSS 2.0) from the built site, the same way scripts/gen-sitemap.py
builds sitemap.xml: the published HTML is the source of truth, so hand-built posts are included.

Discovery (identical to gen-sitemap.py): every blog/<slug>/index.html except _/. dirs and
http-equiv="refresh" redirect stubs. Of those, only pages whose JSON-LD carries an article type
(Article, BlogPosting, NewsArticle, AnalysisNewsArticle, OpinionNewsArticle, ...) become items,
so /blog/about/, /blog/standards/, /blog/corrections/, /blog/contact/ and author pages stay out.

Per item it reads: canonical URL, JSON-LD headline (falls back to og:title), meta description
(falls back to og:description / JSON-LD description), JSON-LD datePublished/dateModified,
JSON-LD author name(s), og:image (+ og:image:width/height/alt), and the tag chips on that post's
card in blog/index.html (as <category>).

Order: newest datePublished first; same instant -> blog index card order (the editors' order
for same-day posts, as build-author-page.py uses), then URL. Newest MAX_ITEMS items.

Dates: RFC 822 in RSS (RFC 3339 in Atom). A JSON-LD date that is a bare YYYY-MM-DD has no time
or zone; it is read as 00:00 America/New_York (the newsroom's zone) and reported as a warning.
--strict turns that warning into an error (turn it on in CI once every post carries a full
ISO 8601 timestamp with offset).

Output is deterministic: lastBuildDate = newest item dateModified, never "now".
Channel title, description, and accent are the constants below. The description is the
newsroom line, not the blog-index meta description.

Usage (repo root):
  python3 scripts/gen-feed.py            # write blog/feed.xml (and blog/atom.xml if it exists or --atom)
  python3 scripts/gen-feed.py --check    # exit 1 if a committed feed is stale
  python3 scripts/gen-feed.py --strict   # also fail on date-only (timezone-less) dates
  python3 scripts/gen-feed.py --verbose  # list every timezone-less date
No third-party packages (Python 3.9+ for zoneinfo).
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from html import escape, unescape
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.octoprobe.ai"
BLOG_URL = f"{SITE}/blog/"
RSS_PATH = ROOT / "blog" / "feed.xml"
ATOM_PATH = ROOT / "blog" / "atom.xml"
RSS_URL = f"{SITE}/blog/feed.xml"
ATOM_URL = f"{SITE}/blog/atom.xml"
HUB = "https://pubsubhubbub.appspot.com/"   # WebSub hub announced in the feed (ping it after deploy)
NEWSROOM_TZ = ZoneInfo("America/New_York")
MAX_ITEMS = 50
FEED_TITLE = "OctoProbe News"
# Newsroom line for the channel. Not scraped from blog/index.html, so a homepage
# meta edit cannot silently change the feed. Facts already published on /blog/about/.
FEED_DESCRIPTION = (
    "Investigative reporting on national security, intelligence, digital targeting and online "
    "influence operations. Published by Redwing Technologies LLC."
)
FEED_ICON = f"{SITE}/icon-512.png"            # square, used by Feedly (webfeeds:icon) and Atom <icon>
RSS_IMAGE = (f"{SITE}/feed-icon-144.png", 144, 144)  # RSS <image> must be <= 144 px wide
COPYRIGHT = "© 2026 Redwing Technologies LLC"
MANAGING_EDITOR = "press@octoprobe.ai (OctoProbe News)"
ARTICLE_TYPES = re.compile(r"^(Article|BlogPosting|[A-Za-z]*NewsArticle|Report|ScholarlyArticle|TechArticle)$")

warnings: list[str] = []


# ── HTML helpers (same regex style as gen-sitemap.py) ──────────────────────────────────────────
def meta(html: str, prop: str) -> str | None:
    m = re.search(r'<meta\s+(?:property|name)="%s"\s+content="([^"]*)"' % re.escape(prop), html)
    return unescape(m.group(1)) if m else None


def jsonld_nodes(html: str) -> list[dict]:
    out: list[dict] = []

    def walk(x):
        if isinstance(x, dict):
            out.append(x)
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            walk(json.loads(block))
        except json.JSONDecodeError as e:
            raise SystemExit(f"ERROR: invalid JSON-LD: {e}")
    return out


def types(node: dict) -> list[str]:
    t = node.get("@type", [])
    return [t] if isinstance(t, str) else list(t)


def article_node(html: str) -> dict | None:
    for n in jsonld_nodes(html):
        if any(ARTICLE_TYPES.match(t) for t in types(n)) and n.get("datePublished"):
            return n
    return None


def parse_date(value: str, where: str) -> datetime:
    value = value.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        warnings.append(f"{where}: date-only '{value}' (no time/timezone); read as 00:00 America/New_York")
        return datetime.fromisoformat(value).replace(tzinfo=NEWSROOM_TZ)
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        warnings.append(f"{where}: '{value}' has a time but no UTC offset; read as America/New_York")
        dt = dt.replace(tzinfo=NEWSROOM_TZ)
    return dt


def card_index() -> tuple[list[str], dict[str, list[str]]]:
    """Card order and tag chips from blog/index.html, keyed by absolute URL."""
    html = (ROOT / "blog" / "index.html").read_text(encoding="utf-8")
    order, tags = [], {}
    for m in re.finditer(r'<a class="post-card[^"]*" href="(/blog/[^"]+)">(.*?)</a>', html, re.S):
        url = SITE + m.group(1)
        if url not in tags:
            order.append(url)
            tags[url] = [unescape(t).strip() for t in re.findall(r'<span class="tag[^"]*">([^<]+)</span>', m.group(2))]
    return order, tags


def live_pages() -> list[Path]:
    out = []
    for p in sorted((ROOT / "blog").glob("*/index.html")):
        if any(part.startswith(("_", ".")) for part in p.relative_to(ROOT / "blog").parts[:-1]):
            continue
        if 'http-equiv="refresh"' in p.read_text(encoding="utf-8"):
            continue
        out.append(p)
    return out


def local_file(url: str) -> Path | None:
    if not url.startswith(SITE + "/"):
        return None
    p = ROOT / url[len(SITE) + 1:].split("?")[0]
    return p if p.is_file() else None


def item(path: Path, tags: dict[str, list[str]]) -> dict | None:
    html = path.read_text(encoding="utf-8")
    rel = str(path.relative_to(ROOT))
    art = article_node(html)
    if not art:
        return None  # AboutPage / ContactPage / WebPage etc.
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    if not canon:
        raise SystemExit(f"ERROR: {rel} has no canonical link")
    url = canon.group(1)
    if not url.startswith(BLOG_URL):
        raise SystemExit(f"ERROR: {rel} canonical {url} is not under {BLOG_URL}")
    title = (art.get("headline") or meta(html, "og:title") or "").strip()
    desc = (meta(html, "description") or meta(html, "og:description") or art.get("description") or "").strip()
    if not title or not desc:
        raise SystemExit(f"ERROR: {rel} needs a headline and a description")
    pub = parse_date(art["datePublished"], rel)
    mod = parse_date(art.get("dateModified") or art["datePublished"], rel)
    authors = art.get("author") or []
    authors = authors if isinstance(authors, list) else [authors]
    names = [a.get("name", "").strip() for a in authors if isinstance(a, dict) and a.get("name")]
    img = meta(html, "og:image")
    image = None
    if img:
        f = local_file(img)
        image = {
            "url": img,
            "width": meta(html, "og:image:width"),
            "height": meta(html, "og:image:height"),
            "alt": meta(html, "og:image:alt") or "",
            "type": {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}.get(
                img.split("?")[0].rsplit(".", 1)[-1].lower(), "image/png"),
            "length": f.stat().st_size if f else None,
        }
    return {"url": url, "title": title, "desc": desc, "pub": pub, "mod": max(mod, pub),
            "authors": names, "image": image, "tags": tags.get(url, [])}


def collect() -> list[dict]:
    order, tags = card_index()
    items = [i for i in (item(p, tags) for p in live_pages()) if i]
    pos = {u: n for n, u in enumerate(order)}
    # newest first; ties (e.g. date-only posts on the same day) follow the blog index card order
    items.sort(key=lambda i: (-i["pub"].timestamp(), pos.get(i["url"], len(pos)), i["url"]))
    return items[:MAX_ITEMS]


def rfc822(dt: datetime) -> str:
    return format_datetime(dt)  # keeps the post's own offset, e.g. "Tue, 20 Oct 2026 19:16:57 -0400"


def rfc3339(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def x(s: str) -> str:
    return escape(s, quote=False)


def a(s: str) -> str:
    return escape(s, quote=True)


def channel_description() -> str:
    return FEED_DESCRIPTION


def build_rss(items: list[dict]) -> str:
    last_build = max(i["mod"] for i in items)
    newest_pub = items[0]["pub"]
    o = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<rss version="2.0"',
         '     xmlns:atom="http://www.w3.org/2005/Atom"',
         '     xmlns:dc="http://purl.org/dc/elements/1.1/"',
         '     xmlns:media="http://search.yahoo.com/mrss/"',
         '     xmlns:webfeeds="http://webfeeds.org/rss/1.0">',
         "  <channel>",
         f"    <title>{x(FEED_TITLE)}</title>",
         f"    <link>{x(BLOG_URL)}</link>",
         f"    <description>{x(channel_description())}</description>",
         f'    <atom:link href="{a(RSS_URL)}" rel="self" type="application/rss+xml"/>',
         f'    <atom:link href="{a(HUB)}" rel="hub"/>',
         "    <language>en-us</language>",
         f"    <copyright>{x(COPYRIGHT)}</copyright>",
         f"    <managingEditor>{x(MANAGING_EDITOR)}</managingEditor>",
         f"    <webMaster>{x(MANAGING_EDITOR)}</webMaster>",
         f"    <pubDate>{rfc822(newest_pub)}</pubDate>",
         f"    <lastBuildDate>{rfc822(last_build)}</lastBuildDate>",
         "    <docs>https://www.rssboard.org/rss-specification</docs>",
         "    <ttl>60</ttl>",
         "    <image>",
         f"      <url>{x(RSS_IMAGE[0])}</url>",
         f"      <title>{x(FEED_TITLE)}</title>",
         f"      <link>{x(BLOG_URL)}</link>",
         f"      <width>{RSS_IMAGE[1]}</width>",
         f"      <height>{RSS_IMAGE[2]}</height>",
         "    </image>",
         f"    <webfeeds:icon>{x(FEED_ICON)}</webfeeds:icon>",
         "    <webfeeds:accentColor>0288D1</webfeeds:accentColor>",
         "    <webfeeds:analytics id=\"G-6T6HW79ZP0\" engine=\"GoogleAnalytics\"/>"]
    for i in items:
        o += ["    <item>",
              f"      <title>{x(i['title'])}</title>",
              f"      <link>{x(i['url'])}</link>",
              f'      <guid isPermaLink="true">{x(i["url"])}</guid>',
              f"      <description>{x(i['desc'])}</description>",
              f"      <pubDate>{rfc822(i['pub'])}</pubDate>"]
        o += [f"      <dc:creator>{x(n)}</dc:creator>" for n in i["authors"]]
        o += [f"      <category>{x(t)}</category>" for t in i["tags"]]
        im = i["image"]
        if im:
            if im["length"]:
                o.append(f'      <enclosure url="{a(im["url"])}" length="{im["length"]}" type="{im["type"]}"/>')
            dims = "".join(f' {k}="{a(im[k])}"' for k in ("width", "height") if im[k])
            o.append(f'      <media:content url="{a(im["url"])}" medium="image" type="{im["type"]}"{dims}>')
            if im["alt"]:
                o.append(f'        <media:description type="plain">{x(im["alt"])}</media:description>')
            o.append("      </media:content>")
        o.append("    </item>")
    o += ["  </channel>", "</rss>", ""]
    return "\n".join(o)


def build_atom(items: list[dict]) -> str:
    o = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en-us">',
         f"  <title>{x(FEED_TITLE)}</title>",
         f"  <subtitle>{x(channel_description())}</subtitle>",
         f"  <id>{x(BLOG_URL)}</id>",
         f'  <link rel="alternate" type="text/html" href="{a(BLOG_URL)}"/>',
         f'  <link rel="self" type="application/atom+xml" href="{a(ATOM_URL)}"/>',
         f'  <link rel="hub" href="{a(HUB)}"/>',
         f"  <updated>{rfc3339(max(i['mod'] for i in items))}</updated>",
         f"  <icon>{x(FEED_ICON)}</icon>",
         f"  <rights>{x(COPYRIGHT)}</rights>"]
    for i in items:
        o += ["  <entry>",
              f"    <title>{x(i['title'])}</title>",
              f'    <link rel="alternate" type="text/html" href="{a(i["url"])}"/>',
              f"    <id>{x(i['url'])}</id>",
              f"    <published>{rfc3339(i['pub'])}</published>",
              f"    <updated>{rfc3339(i['mod'])}</updated>"]
        for n in i["authors"] or [FEED_TITLE]:
            o.append(f"    <author><name>{x(n)}</name></author>")
        o += [f'    <category term="{a(t)}"/>' for t in i["tags"]]
        o.append(f"    <summary>{x(i['desc'])}</summary>")
        if i["image"]:
            o.append(f'    <link rel="enclosure" type="{i["image"]["type"]}" href="{a(i["image"]["url"])}"'
                     + (f' length="{i["image"]["length"]}"' if i["image"]["length"] else "") + "/>")
        o.append("  </entry>")
    o += ["</feed>", ""]
    return "\n".join(o)


def main() -> None:
    check, strict = "--check" in sys.argv, "--strict" in sys.argv
    items = collect()
    if not items:
        raise SystemExit("ERROR: no article pages found under blog/")
    uniq = list(dict.fromkeys(warnings))
    if uniq and "--verbose" in sys.argv:
        for w in uniq:
            print(f"warning: {w}", file=sys.stderr)
    elif uniq:
        files = len({w.split(":", 1)[0] for w in uniq})
        print(f"warning: {files} post(s) carry timezone-less dates (read as America/New_York); "
              "--verbose lists them, --strict fails on them", file=sys.stderr)
    if strict and warnings:
        raise SystemExit("ERROR: --strict: every post needs a full ISO 8601 datePublished/dateModified with offset")
    outputs = {RSS_PATH: build_rss(items)}
    if "--atom" in sys.argv or ATOM_PATH.exists():
        outputs[ATOM_PATH] = build_atom(items)
    stale = False
    for path, new in outputs.items():
        rel = path.relative_to(ROOT)
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        if check:
            if old != new:
                print(f"{rel} is stale. Run: python3 scripts/gen-feed.py", file=sys.stderr)
                stale = True
            else:
                print(f"{rel} is up to date")
        elif old != new:
            path.write_text(new, encoding="utf-8")
            print(f"updated {rel} ({len(items)} items)")
        else:
            print(f"{rel} unchanged ({len(items)} items)")
    sys.exit(1 if stale else 0)


if __name__ == "__main__":
    main()
