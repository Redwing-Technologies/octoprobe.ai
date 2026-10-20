"""Shared author defaults for OctoProbe News posts (used by build-blog.py and build-adtech-post.py).

Default author for every post is Colin Aamot: top byline with circular headshot, bottom
.author-note bio box (same headshot, larger, left of the text) with profile-link pills, and a JSON-LD Person (name, url, image,
description, sameAs). The Organization stays the JSON-LD publisher.

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

DEFAULT_AUTHOR = {
    "name": "Colin Aamot",
    "url": "https://www.linkedin.com/in/colinaamot/",
    "image": "/assets/authors/colin-aamot-192.jpg",
    "bio": ("Colin Aamot is a former U.S. Army counterterrorism information operations (CT-IO) planner who "
            "deployed with several joint task forces in support of Operations Inherent Resolve and Spartan "
            "Shield. He subsequently worked at the Heritage Foundation and in the office of Rep. Darrell Issa, "
            "with portfolios spanning foreign policy, technology, and innovation. He holds an MA in Global "
            "Security Studies from Johns Hopkins University and an MBA from UNC Kenan-Flagler Business School."),
    "links": [
        ("LinkedIn", "https://www.linkedin.com/in/colinaamot/"),
        ("X", "https://x.com/ColinAamot"),
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
        a = {"name": name, "url": None, "image": None, "bio": None, "links": []}
    if meta.get("author_url"):
        a["url"] = meta["author_url"]
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
