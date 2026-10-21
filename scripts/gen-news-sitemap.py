#!/usr/bin/env python3
"""Regenerate sitemap-news.xml (Google News sitemap) from the same article discovery as
scripts/gen-feed.py: every live blog post with an article-type JSON-LD node published in the
48 hours before --now (default: the current time). Google ignores entries older than two days,
so old ones are dropped. With no fresh articles it writes a valid, empty <urlset>.

This file depends on the clock, so it is NOT diffed in PR CI (no --check). The feed workflow
regenerates it on every push to main and on the daily schedule and commits it if it changed.

Usage (repo root):
  python3 scripts/gen-news-sitemap.py                              # write sitemap-news.xml
  python3 scripts/gen-news-sitemap.py --now 2026-10-20T21:45:00-04:00
  python3 scripts/gen-news-sitemap.py --stdout
"""
from __future__ import annotations

import importlib.util
import sys
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("gen_feed", HERE / "gen-feed.py")
feed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(feed)

OUT = feed.ROOT / "sitemap-news.xml"
PUBLICATION = "OctoProbe News"  # must match the publication name Google News shows; see GOOGLE-NEWS-COMPLIANCE.md
LANGUAGE = "en"
WINDOW = timedelta(hours=48)


def main() -> None:
    now = datetime.now(timezone.utc)
    if "--now" in sys.argv:
        now = datetime.fromisoformat(sys.argv[sys.argv.index("--now") + 1])
    items = [i for i in feed.collect() if now - WINDOW <= i["pub"] <= now]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">']
    for i in items:
        out += ["  <url>",
                f"    <loc>{escape(i['url'])}</loc>",
                "    <news:news>",
                "      <news:publication>",
                f"        <news:name>{escape(PUBLICATION)}</news:name>",
                f"        <news:language>{LANGUAGE}</news:language>",
                "      </news:publication>",
                f"      <news:publication_date>{i['pub'].isoformat(timespec='seconds')}</news:publication_date>",
                f"      <news:title>{escape(i['title'], quote=False)}</news:title>",
                "    </news:news>",
                "  </url>"]
    out += ["</urlset>", ""]
    xml = "\n".join(out)
    if "--stdout" in sys.argv:
        sys.stdout.write(xml); return
    old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    if old != xml:
        OUT.write_text(xml, encoding="utf-8")
        print(f"updated sitemap-news.xml ({len(items)} articles in the last 48 h)")
    else:
        print(f"sitemap-news.xml unchanged ({len(items)} articles)")


if __name__ == "__main__":
    main()
