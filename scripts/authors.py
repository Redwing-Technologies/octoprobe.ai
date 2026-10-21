"""Shared author defaults for OctoProbe News posts (used by build-blog.py and build-adtech-post.py).

Default author for every post is Colin Aamot: top byline with circular headshot, bottom
.author-note bio box (same headshot, larger, left of the text) with profile-link pills, and a JSON-LD
Person reference ({"@type": "Person", "@id": AUTHOR_PAGE#person, "name", "url"}). The byline name and the
bio-box name link (rel="author") to the on-site author page /blog/authors/colin-aamot/, which carries the
full ProfilePage + Person node (scripts/build-author-page.py). The Organization stays the JSON-LD publisher.
After changing anything here, run scripts/refresh-author-markup.py (hand-built posts) and the post
builders, then scripts/build-author-page.py and scripts/gen-sitemap.py.

Per-post override (front matter):
  * another person: author: Name, author_url:, author_bio:, author_image:
    (/assets/authors/<name>-192.jpg, with -96/-192 .webp/.jpg siblings), author_links:
    ["Label | https://url", ...]; byline: overrides the visible name only.
  * staff / organization byline: author: OctoProbe Staff (or OctoProbe / OctoProbe AI / OctoProbe News)
    -> no avatar, no bio box, JSON-LD author is the Organization (the pre-2026-10-20 behaviour).
"""
from html import escape
import re

SITE = "https://www.octoprobe.ai"
ORG_AUTHOR_NAMES = {"OctoProbe", "OctoProbe AI", "OctoProbe News", "OctoProbe Staff"}

# Canonical bio: byte-identical to Person.description on the author page and in every post's
# bio box (source of truth: this string; scripts/build-author-page.py reads it from here).
CANONICAL_BIO = (
    "Colin Aamot is an Investigative Journalist & OSINT Domain Expert and Founder of Redwing "
    "Technologies, which publishes OctoProbe News, runs a portfolio of other SaaS products, and "
    "operates Rook Intelligence, a licensed Washington, DC private detective agency. A U.S. Army "
    "veteran, he began in the 173rd Airborne Brigade and was selected "
    "for the Special Operations psychological operations regiment, then served as a counterterrorism "
    "information operations planner with USASOC and SOCCENT supporting Operation Inherent Resolve and "
    "Operation Spartan Shield. He was a TechCongress Congressional Innovation Fellow in the office of "
    "Rep. Darrell Issa and later an investigator for The Heritage Foundation's Oversight Project and "
    "an investigative columnist for The Daily Signal. He holds an MA in Global Security Studies from "
    "Johns Hopkins University and an MBA from UNC Kenan-Flagler Business School."
)

AUTHOR_PAGE = SITE + "/blog/authors/colin-aamot/"

DEFAULT_AUTHOR = {
    "name": "Colin Aamot",
    # Stable entity id: the full Person node lives on the author page; posts reference it by @id.
    "id": AUTHOR_PAGE + "#person",
    "url": AUTHOR_PAGE,
    "image": "/assets/authors/colin-aamot-192.jpg",
    "bio": CANONICAL_BIO,
    "links": [
        ("LinkedIn", "https://www.linkedin.com/in/colinaamot/"),
        ("X", "https://x.com/ColinAamot"),
        ("TechCongress", "https://techcongress.io/colin-aamot"),
        ("Rook Intelligence", "https://rook-intel.com/"),
        ("Daily Signal (previous bylines)", "https://www.dailysignal.com/author/colin-aamot/"),
    ],
}


def resolve_author(meta: dict) -> dict | None:
    """Return the Person author for a post, or None for an Organization/staff byline."""
    name = (meta.get("author") or "").strip()
    if name in ORG_AUTHOR_NAMES:
        return None
    if not name or name == DEFAULT_AUTHOR["name"]:
        a = dict(DEFAULT_AUTHOR)
    else:
        a = {"name": name, "id": None, "url": None, "image": None, "bio": None, "links": []}
    if meta.get("author_url") and meta["author_url"] != a.get("url"):
        a["url"] = meta["author_url"]
        a["id"] = None  # a different entity home: don't claim the default Person @id
    if meta.get("author_image"):
        a["image"] = meta["author_image"]
    if meta.get("author_bio"):
        a["bio"] = meta["author_bio"]
    if meta.get("author_links"):
        a["links"] = [tuple(p.strip() for p in x.split(" | ", 1)) for x in meta["author_links"]]
    assert all(len(x) == 2 and x[1].startswith("https://") for x in a["links"]), a["links"]
    a["byline"] = meta.get("byline") or a["name"]
    return a


def avatar_html(a: dict, size: int = 44, alt: str | None = None, lazy: bool = False,
                pic_class: str = "") -> str:
    """Circular headshot <picture>. Top byline: 44px box, alt = name. Bio box: 96px box,
    alt="" (the linked name sits right next to it), lazy-loaded."""
    img = a.get("image")
    if not img:
        return ""
    assert re.fullmatch(r"/assets/authors/[a-z0-9-]+-192\.jpg", img), img
    stem = img[: -len("-192.jpg")]
    alt = escape(a["name"]) if alt is None else escape(alt)
    cls = f' class="{pic_class}"' if pic_class else ""
    load = ' loading="lazy"' if lazy else ""
    return (f'<picture{cls}><source type="image/webp" srcset="{stem}-96.webp 1x, {stem}-192.webp 2x">'
            f'<img class="author-avatar" src="{stem}-96.jpg" srcset="{stem}-96.jpg 1x, {stem}-192.jpg 2x" '
            f'width="{size}" height="{size}" alt="{alt}"{load} decoding="async"></picture>')


def byline_html(a: dict | None, staff_name: str = "OctoProbe Staff") -> str:
    if a is None:
        return f'<p class="byline">By {escape(staff_name)}</p>'
    name = (f'<a href="{escape(a["url"])}" rel="author">{escape(a["byline"])}</a>'
            if a.get("url") and a["byline"] == a["name"] else escape(a["byline"]))
    pic = avatar_html(a)
    if pic:
        return f'<p class="byline has-avatar">{pic}<span>By {name}</span></p>'
    return f'<p class="byline">By {name}</p>'


def author_note_html(a: dict | None) -> str:
    if a is None or not a.get("bio"):
        return ""
    bio = a["bio"]
    rest = bio[len(a["name"]):] if bio.startswith(a["name"]) else " " + bio
    name = f'<a href="{escape(a["url"])}" rel="author">{escape(a["name"])}</a>' if a.get("url") else escape(a["name"])
    links = ('<span class="author-links">' + "".join(f'<a href="{escape(u)}">{escape(l)}</a>' for l, u in a["links"])
             + "</span>") if a.get("links") else ""
    # Same headshot as the top byline, larger, to the left of the bio text (blog.css .author-note.has-avatar).
    pic = avatar_html(a, size=96, alt="", lazy=True, pic_class="author-note-avatar")
    if pic:
        return (f'<p class="author-note has-avatar">{pic}'
                f'<span class="author-note-text">{name}{escape(rest)}{links}</span></p>')
    return f'<p class="author-note">{name}{escape(rest)}{links}</p>'


def person_ld(a: dict) -> dict:
    """JSON-LD author for a post. An author with an on-site entity home (DEFAULT_AUTHOR: id + url)
    gets only a reference: @type, @id, name, url. The full Person node (description, image,
    sameAs, jobTitle, ...) lives once on the author page, so posts can't drift from it."""
    if a.get("id"):
        return {"@type": "Person", "@id": a["id"], "name": a["name"], "url": a["url"]}
    p = {"@type": "Person", "name": a["name"]}
    if a.get("url"):
        p["url"] = a["url"]
    if a.get("bio"):
        p["description"] = a["bio"]
    if a.get("image"):
        p["image"] = SITE + a["image"]
    if a.get("links"):
        p["sameAs"] = [u for _, u in a["links"]]
    return p


def insert_author_note(body_html: str, note: str) -> str:
    """Place the bio note just before Related Reading if present, else at the end of the body."""
    if not note:
        return body_html.replace("<p>{{AUTHOR_NOTE}}</p>\n", "").replace("<p>{{AUTHOR_NOTE}}</p>", "")
    if "<p>{{AUTHOR_NOTE}}</p>" in body_html:
        return body_html.replace("<p>{{AUTHOR_NOTE}}</p>", note, 1)
    m = re.search(r'<aside[^>]*class="related-reading"|<h2[^>]*>Related Reading</h2>', body_html)
    if m:
        return body_html[: m.start()] + note + "\n" + body_html[m.start():]
    return body_html.rstrip("\n") + "\n" + note + "\n"
