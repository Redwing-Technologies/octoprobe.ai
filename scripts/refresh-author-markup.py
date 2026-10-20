#!/usr/bin/env python3
"""Re-render the author markup in every built post bylined by the default author (Colin Aamot).

Most bylined posts are hand-built HTML (no markdown source), and the markdown builders' output has
since been hand-edited, so a full rebuild is not byte-safe. This script rewrites ONLY the three
author surfaces from scripts/authors.py, leaving the rest of each page untouched:
  * the top byline   <p class="byline ...">...</p>       -> authors.byline_html()
  * the bio box      <p class="author-note ...">...</p>  -> authors.author_note_html()
  * JSON-LD "author" object (Person, name == default)     -> authors.person_ld()
    (@type, @id https://www.octoprobe.ai/blog/authors/colin-aamot/#person, name, url)
A post is in scope when it has <meta name="author" content="Colin Aamot">. Idempotent.
Also updates the reference JSON-LD sources in blog/posts/*.jsonld.json.

Usage (repo root):
  python3 scripts/refresh-author-markup.py          # rewrite in place
  python3 scripts/refresh-author-markup.py --check  # exit 1 if any post is stale
No third-party packages.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import authors as AU  # noqa: E402

A = AU.resolve_author({})
NAME = A["name"]
BYLINE_RE = re.compile(r'<p class="byline(?: has-avatar)?">.*?</p>', re.S)
NOTE_RE = re.compile(r'<p class="author-note(?: has-avatar)?">.*?</p>', re.S)
LD_AUTHOR_RE = re.compile(r'^(?P<ind>[ \t]*)"author": \{\n(?P<body>.*?)^(?P=ind)\}', re.S | re.M)


def ld_author(ind: str) -> str:
    txt = json.dumps(AU.person_ld(A), indent=2, ensure_ascii=False)
    lines = txt.split("\n")
    return f'{ind}"author": ' + "\n".join([lines[0]] + [ind + ln for ln in lines[1:]])


def fix_ld(text: str) -> tuple[str, int]:
    n = 0

    def sub(m: re.Match) -> str:
        nonlocal n
        body = m.group("body")
        if '"@type": "Person"' not in body or f'"name": "{NAME}"' not in body:
            return m.group(0)
        n += 1
        return ld_author(m.group("ind"))

    return LD_AUTHOR_RE.sub(sub, text), n


def refresh(html: str, path: Path) -> str:
    bylines = BYLINE_RE.findall(html)
    notes = NOTE_RE.findall(html)
    if len(bylines) != 1 or len(notes) != 1:
        raise SystemExit(f"ERROR: {path.relative_to(ROOT)}: expected 1 byline + 1 author-note, "
                         f"found {len(bylines)} + {len(notes)}")
    out = BYLINE_RE.sub(lambda m: AU.byline_html(A), html, count=1)
    out = NOTE_RE.sub(lambda m: AU.author_note_html(A), out, count=1)
    out, n = fix_ld(out)
    if n < 1:
        raise SystemExit(f"ERROR: {path.relative_to(ROOT)}: no JSON-LD Person author for {NAME}")
    return out


def targets() -> list[tuple[Path, str, str]]:
    res = []
    for p in sorted((ROOT / "blog").glob("*/index.html")):
        html = p.read_text(encoding="utf-8")
        if f'<meta name="author" content="{NAME}">' in html:
            res.append((p, html, refresh(html, p)))
    for p in sorted((ROOT / "blog" / "posts").glob("*.jsonld.json")):
        txt = p.read_text(encoding="utf-8")
        new, n = fix_ld(txt)
        if n:
            res.append((p, txt, new))
    return res


def main() -> None:
    check = "--check" in sys.argv
    stale = 0
    for p, old, new in targets():
        if old != new:
            stale += 1
            if not check:
                p.write_text(new, encoding="utf-8")
                print(f"refreshed {p.relative_to(ROOT)}")
    if check:
        if stale:
            print(f"{stale} file(s) have stale author markup. Run: python3 scripts/refresh-author-markup.py",
                  file=sys.stderr)
            sys.exit(1)
        print("author markup is up to date")


if __name__ == "__main__":
    main()
