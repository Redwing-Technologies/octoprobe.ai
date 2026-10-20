#!/usr/bin/env python3
"""Build the author page blog/authors/colin-aamot/index.html (ProfilePage + Person entity home).

Inputs:
  * scripts/author-data/colin-aamot.person.jsonld  ProfilePage + Person + BreadcrumbList graph.
    Person @id https://www.octoprobe.ai/blog/authors/colin-aamot/#person; every bylined post's
    JSON-LD author references this @id (scripts/authors.py person_ld()). The build stamps
    dateCreated/dateModified and refuses to run if Person.description differs from
    scripts/authors.py CANONICAL_BIO (the same text as every post's bio box).
  * blog/_template.html  nav, footer, head boilerplate (blog.css ?v= stays the template's).
  * built posts (blog/<slug>/index.html with <meta name="author" content="Colin Aamot">)
    -> the "Articles at OctoProbe News" list in blog/index.html card order (newest first;
    headline = the post's <h1>).
  * blog/authors/colin-aamot/assets/  headshot: colin-aamot.webp (1000) / -800 / -400 / -192 WebP
    srcset + colin-aamot.jpg (1000px, also og:image and Person.image). Committed as-is.

Deterministic (no "today"): dateModified = max(DATE_CREATED, newest bylined post dateModified).
Usage (repo root):
  python3 scripts/build-author-page.py          # write the page
  python3 scripts/build-author-page.py --check  # exit 1 if it is stale
Then run scripts/gen-sitemap.py. No third-party packages.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import authors as AU  # noqa: E402

SLUG = "colin-aamot"
PAGE_DIR = ROOT / "blog" / "authors" / SLUG
OUT = PAGE_DIR / "index.html"
SRC = ROOT / "scripts" / "author-data" / f"{SLUG}.person.jsonld"
TEMPLATE = ROOT / "blog" / "_template.html"
URL = AU.AUTHOR_PAGE
ASSETS = f"/blog/authors/{SLUG}/assets"
DATE_CREATED = "2026-10-20"
NAME = AU.DEFAULT_AUTHOR["name"]
ROLE = "Founder, Redwing Technologies"
TITLE = f"{NAME}: {ROLE} | OctoProbe News"
DESCRIPTION = ("Colin Aamot is the founder of Redwing Technologies, publisher of OctoProbe News. "
               "Bio, background, profiles, press coverage and his investigations.")
SRCSET = (f"{ASSETS}/colin-aamot-192.webp 192w, {ASSETS}/colin-aamot-400.webp 400w, "
          f"{ASSETS}/colin-aamot-800.webp 800w, {ASSETS}/colin-aamot.webp 1000w")
SIZES = "(max-width: 520px) 152px, 200px"

PROFILES = [  # same URLs as Person.sameAs (Rook links its homepage; sameAs uses its #colin-aamot node)
    ("LinkedIn", "https://www.linkedin.com/in/colinaamot/", True),
    ("X", "https://x.com/ColinAamot", True),
    ("Rook Intelligence", "https://rook-intel.com/", False),
    ("TechCongress profile", "https://techcongress.io/colin-aamot", False),
    ("The Daily Signal (previous bylines)", "https://www.dailysignal.com/author/colin-aamot/", False),
]
BACKGROUND = [
    "U.S. Army: 173rd Airborne Brigade; selected for the Special Operations Psychological Operations "
    "Regiment (2016); counterterrorism information operations planner who served with USASOC and SOCCENT "
    "supporting Operation Inherent Resolve and Operation Spartan Shield",
    "TechCongress Congressional Innovation Fellow (June 2022 cohort), office of Rep. Darrell Issa",
    "Investigator, The Heritage Foundation's Oversight Project; investigative columnist, The Daily Signal",
    "Founder, Redwing Technologies, which publishes OctoProbe News, builds a portfolio of SaaS products, "
    "and runs Rook Intelligence (licensed DC private detective agency)",
    "MA, Global Security Studies, Johns Hopkins University · MBA, UNC Kenan-Flagler · Levantine Arabic, "
    "Defense Language Institute",
]
PRESS = [
    ("https://www.propublica.org/article/have-government-employees-mentioned-climate-change-voting-or-gender-identity-the-heritage-foundation-wants-to-know",
     "ProPublica", "Oct. 1, 2024",
     "Heritage Foundation Staffers Flood Federal Agencies With Thousands of Information Requests"),
    ("https://techcongress.io/blog/meet-colin-aamot", "TechCongress", "July 27, 2022",
     "Meet the June 2022 Fellows: Colin Aamot"),
]

STYLE = """<style>
.author-hero .wrap{display:flex;align-items:center;gap:2rem}
.author-hero picture{display:block;flex:none;line-height:0}
.author-hero .author-photo{display:block;width:200px;height:200px;border-radius:50%;object-fit:cover;background:var(--panel-2);box-shadow:0 0 0 1px var(--line-2)}
.author-hero .author-id{min-width:0}
.author-hero .post-crumb{margin-bottom:.6rem}
.author-hero h1{margin:0}
.author-hero .author-role{margin:.55rem 0 0;font-family:var(--fd);font-weight:500;font-size:1.12rem;color:var(--soft)}
.page-body .prose{max-width:760px;margin:0 auto}
.page-body .prose h2{scroll-margin-top:90px}
.page-body .prose ul.author-profiles{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin-left:0}
.page-body .prose ul.author-profiles li{margin:0;padding:0}
.page-body .prose ul.author-profiles li::before{content:none}
.page-body .prose ul.author-profiles a{display:inline-block;font-family:var(--fm);font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;font-weight:500;color:var(--soft);background:var(--panel-2);border:1px solid var(--line-2);padding:7px 12px;border-radius:999px;text-decoration:none;white-space:nowrap}
.page-body .prose ul.author-profiles a:hover,.page-body .prose ul.author-profiles a:focus-visible{color:var(--blue);border-color:rgba(2,136,209,.35);background:rgba(2,136,209,.06)}
.page-body .prose ol.author-posts{padding-left:1.4em}
.page-body .prose ol.author-posts li + li{margin-top:.55em}
.page-body .prose ol.author-posts time{display:block;font-family:var(--fm);font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--soft-2);margin-top:.15em}
@media(max-width:640px){
  .author-hero .wrap{flex-direction:column;align-items:flex-start;gap:1.25rem}
  .author-hero .author-photo{width:152px;height:152px}
}
</style>"""


def fmt_date(d: str) -> str:
    return date.fromisoformat(d[:10]).strftime("%b %-d, %Y")


def posts() -> list[dict]:
    res = []
    for p in sorted((ROOT / "blog").glob("*/index.html")):
        html = p.read_text(encoding="utf-8")
        if f'<meta name="author" content="{NAME}">' not in html or 'http-equiv="refresh"' in html:
            continue
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', html).group(1)
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S).group(1)
        h1 = unescape(re.sub(r"<[^>]+>", "", h1)).strip()
        pub = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', html).group(1)
        mod = (re.search(r'"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})', html) or [None, pub])[1]
        res.append({"url": canon.replace("https://www.octoprobe.ai", ""), "title": h1, "pub": pub, "mod": mod})
    # Order = the blog index's card order (newest first, the editors' order for same-day posts);
    # any bylined post not carded on /blog/ goes last, newest first.
    cards = []
    for u in re.findall(r'href="(/blog/[a-z0-9-]+/)"', (ROOT / "blog" / "index.html").read_text(encoding="utf-8")):
        if u not in cards:
            cards.append(u)
    res.sort(key=lambda d: d["pub"], reverse=True)
    res.sort(key=lambda d: cards.index(d["url"]) if d["url"] in cards else len(cards))
    return res


def graph(modified: str) -> dict:
    g = json.loads(SRC.read_text(encoding="utf-8"))
    page = next(n for n in g["@graph"] if n["@type"] == "ProfilePage")
    person = next(n for n in g["@graph"] if n["@type"] == "Person")
    assert person["@id"] == AU.DEFAULT_AUTHOR["id"], person["@id"]
    assert person["url"] == URL and page["url"] == URL
    if person["description"] != AU.CANONICAL_BIO:
        raise SystemExit("ERROR: Person.description differs from scripts/authors.py CANONICAL_BIO")
    page["dateCreated"] = DATE_CREATED
    page["dateModified"] = modified
    return g


def build() -> str:
    items = posts()
    if not items:
        raise SystemExit(f"ERROR: no posts bylined {NAME}")
    modified = max([DATE_CREATED] + [d["mod"] for d in items])
    ld = json.dumps(graph(modified), indent=2, ensure_ascii=False)
    tpl = TEMPLATE.read_text(encoding="utf-8")

    head_meta = "\n".join([
        f"<title>{escape(TITLE)}</title>",
        f'<meta name="description" content="{escape(DESCRIPTION)}">',
        f'<meta name="author" content="{NAME}">',
        '<link rel="alternate" type="text/plain" title="LLM context (llms.txt)" href="/llms.txt">',
        '<link rel="alternate" type="text/plain" title="AI discovery (ai.txt)" href="/ai.txt">',
        f'<link rel="canonical" href="{URL}">',
        '<meta property="og:type" content="profile">',
        '<meta property="og:site_name" content="OctoProbe News">',
        f'<meta property="og:url" content="{URL}">',
        f'<meta property="og:title" content="{escape(TITLE)}">',
        f'<meta property="og:description" content="{escape(DESCRIPTION)}">',
        f'<meta property="og:image" content="https://www.octoprobe.ai{ASSETS}/colin-aamot.jpg">',
        '<meta property="og:image:width" content="1000">',
        '<meta property="og:image:height" content="1000">',
        f'<meta property="og:image:alt" content="{NAME}">',
        '<meta property="profile:first_name" content="Colin">',
        '<meta property="profile:last_name" content="Aamot">',
        '<meta name="twitter:card" content="summary">',
        '<meta name="twitter:site" content="@octoprobeai">',
        '<meta name="twitter:creator" content="@ColinAamot">',
        f'<meta name="twitter:title" content="{escape(TITLE)}">',
        f'<meta name="twitter:description" content="{escape(DESCRIPTION)}">',
        f'<meta name="twitter:image" content="https://www.octoprobe.ai{ASSETS}/colin-aamot.jpg">',
        '<link rel="me" href="https://www.linkedin.com/in/colinaamot/">',
        '<link rel="me" href="https://x.com/ColinAamot">',
        f'<link rel="preload" as="image" type="image/webp" imagesrcset="{SRCSET}" imagesizes="{SIZES}">',
        f'<script type="application/ld+json">\n{ld}\n</script>',
        STYLE,
    ])

    li_posts = "\n".join(
        f'<li><a href="{escape(d["url"])}">{escape(d["title"], quote=False)}</a>'
        f'<time datetime="{d["pub"]}">{fmt_date(d["pub"])}</time></li>' for d in items)
    li_bg = "\n".join(f"<li>{escape(x, quote=False)}</li>" for x in BACKGROUND)
    li_prof = "\n".join(f'<li><a{" rel=\"me\"" if me else ""} href="{escape(u)}">{escape(l)}</a></li>'
                        for l, u, me in PROFILES)
    li_press = "\n".join(f'<li><a href="{escape(u)}">{escape(o)}</a>, {escape(d)}: <cite>{escape(t, quote=False)}</cite></li>'
                         for u, o, d, t in PRESS)
    main = f"""<main id="main">
  <header class="post-hero author-hero">
    <div class="wrap">
      <picture>
        <source type="image/webp" srcset="{SRCSET}" sizes="{SIZES}">
        <img class="author-photo" src="{ASSETS}/colin-aamot.jpg" width="200" height="200" alt="{NAME}" decoding="async" fetchpriority="high">
      </picture>
      <div class="author-id">
        <div class="post-crumb">
          <a class="back-link" href="/blog/">← OctoProbe News</a>
          <span class="crumb-sep" aria-hidden="true">/</span>
          <span class="eyebrow">{NAME}</span>
        </div>
        <h1>{NAME}</h1>
        <p class="author-role">{ROLE}</p>
      </div>
    </div>
  </header>
  <article class="post-body page-body">
    <div class="wrap">
      <div class="prose">
<h2 id="bio">About</h2>
<p>{escape(AU.CANONICAL_BIO, quote=False)}</p>
<h2 id="background">Background</h2>
<ul>
{li_bg}
</ul>
<h2 id="profiles">Elsewhere</h2>
<ul class="author-profiles">
{li_prof}
</ul>
<h2 id="press">In the press</h2>
<ul>
{li_press}
</ul>
<h2 id="articles">Articles at OctoProbe News</h2>
<ol class="author-posts">
{li_posts}
</ol>
      </div>
    </div>
  </article>
</main>"""

    html = tpl.replace("{{HEAD_META}}", head_meta)
    html = re.sub(r"<main id=\"main\">.*?</main>", lambda m: main, html, count=1, flags=re.S)
    # No nav item is "current" on an author page; the TOC script is for long posts only.
    html = html.replace(' class="nav-cta nav-investigations" aria-current="page"', ' class="nav-cta nav-investigations"')
    html = html.replace('<a href="/blog/" class="active" aria-current="page">Investigations</a>', '<a href="/blog/">Investigations</a>')
    html = re.sub(r'\n<script src="/assets/js/blog-toc\.js[^"]*" defer></script>', "", html)
    assert "{{" not in html, re.findall(r"\{\{[A-Z_]+\}\}", html)
    for f in ("colin-aamot.webp", "colin-aamot-800.webp", "colin-aamot-400.webp", "colin-aamot-192.webp", "colin-aamot.jpg"):
        assert (PAGE_DIR / "assets" / f).is_file(), f"missing asset {f}"
    return html


def main() -> None:
    new = build()
    if "--check" in sys.argv:
        old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if old != new:
            print("author page is stale. Run: python3 scripts/build-author-page.py", file=sys.stderr)
            sys.exit(1)
        print("author page is up to date")
        return
    OUT.write_text(new, encoding="utf-8")
    print(f"built {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
