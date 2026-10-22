"""Shared card order for the homepage latest block and each post's more-from list.

Card order on blog/index.html is the source of truth (newest first), the same
order scripts/build-search-index.py and scripts/build-author-page.py use.
"""
from __future__ import annotations

import re
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG_INDEX = ROOT / "blog" / "index.html"
HOME = ROOT / "index.html"

HOME_START = "<!-- home-latest:start -->"
HOME_END = "<!-- home-latest:end -->"
POST_START = "<!-- latest:start -->"
POST_END = "<!-- latest:end -->"
HOME_COUNT = 8
POST_COUNT = 5

_CARD_RE = re.compile(
    r'<a class="post-card[^"]*" href="(/blog/([^"/]+)/)">(.*?)</a>\s*(?=<a class="post-card|</div>)',
    re.S,
)
_POST_MARK_RE = re.compile(re.escape(POST_START) + r".*?" + re.escape(POST_END), re.S)
_HOME_MARK_RE = re.compile(re.escape(HOME_START) + r".*?" + re.escape(HOME_END), re.S)
_ASIDE_RE = re.compile(r'<aside\b[^>]*\brelated-reading\b[^>]*>.*?</aside>', re.S)
_NOTE_RE = re.compile(r'<p class="author-note\b[^>]*>.*?</p>', re.S)


def _plain(html: str) -> str:
    text = unescape(re.sub(r"<[^>]+>", " ", html))
    return re.sub(r"\s+", " ", text).strip()


def cards() -> list[dict]:
    html = BLOG_INDEX.read_text(encoding="utf-8")
    out = []
    for m in _CARD_RE.finditer(html):
        url, slug, body = m.groups()
        h2 = re.search(r"<h2>(.*?)</h2>", body, re.S)
        excerpt = re.search(r'<p class="excerpt">(.*?)</p>', body, re.S)
        if h2:
            h2_html = re.sub(r'<span class="card-kicker">.*?</span>', "", h2.group(1), flags=re.S)
        time = re.search(r'<time datetime="([^"]+)">([^<]*)</time>', body, re.S)
        if not (h2 and excerpt and time):
            raise SystemExit(f"ERROR: blog index card {slug} is missing a title, excerpt, or date")
        out.append({
            "slug": slug,
            "url": url,
            "title": _plain(h2_html),
            "dek": _plain(excerpt.group(1)),
            "date": time.group(1),
            "date_label": _plain(time.group(2)),
        })
    if not out:
        raise SystemExit("ERROR: no post cards found on blog/index.html")
    return out


def live_posts() -> list[Path]:
    """Published articles only. Skips the template, trust pages, and redirect stubs."""
    out = []
    for path in sorted((ROOT / "blog").glob("*/index.html")):
        if path.parent.name.startswith(("_", ".")):
            continue
        html = path.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in html:
            continue
        if '<meta property="og:type" content="article">' not in html:
            continue
        out.append(path)
    return out


def _home_section(items: list[dict]) -> str:
    cards_html = []
    for card in items:
        cards_html.append(
            "      <a class=\"latest-card\" href=\"{url}\">\n"
            "        <time datetime=\"{date}\">{label}</time>\n"
            "        <p class=\"latest-title\">{title}</p>\n"
            "        <p class=\"latest-dek\">{dek}</p>\n"
            "      </a>".format(
                url=escape(card["url"], quote=True),
                date=escape(card["date"], quote=True),
                label=escape(card["date_label"], quote=False),
                title=escape(card["title"], quote=False),
                dek=escape(card["dek"], quote=False),
            )
        )
    inner = "\n".join(cards_html)
    return (
        f"{HOME_START}\n"
        "<section class=\"pad latest-news\" id=\"latest-news\" aria-labelledby=\"latest-news-title\">\n"
        "  <div class=\"wrap\">\n"
        "    <span class=\"eyebrow\">OctoProbe News</span>\n"
        "    <h2 class=\"sec\" id=\"latest-news-title\">Latest from OctoProbe News</h2>\n"
        "    <div class=\"latest-grid\">\n"
        f"{inner}\n"
        "    </div>\n"
        "    <a class=\"latest-all\" href=\"/blog/\">All investigations →</a>\n"
        "  </div>\n"
        "</section>\n"
        f"{HOME_END}"
    )


def render_home(items: list[dict] | None = None) -> str:
    picked = (items if items is not None else cards())[:HOME_COUNT]
    if len(picked) < 6:
        raise SystemExit(f"ERROR: homepage latest block needs at least 6 posts, found {len(picked)}")
    section = _home_section(picked)
    html = HOME.read_text(encoding="utf-8")
    if HOME_START in html:
        new, n = _HOME_MARK_RE.subn(section, html, count=1)
        if n != 1:
            raise SystemExit("ERROR: homepage latest markers are missing or duplicated")
        return new
    anchor = "<!-- ================================================================ FAQ -->"
    if anchor not in html:
        raise SystemExit("ERROR: homepage has no FAQ marker to place the latest section before")
    return html.replace(anchor, section + "\n\n" + anchor, 1)


def _post_block(items: list[dict]) -> str:
    lis = []
    for card in items:
        lis.append(
            "<li><a href=\"{url}\">{title}</a> "
            "<time datetime=\"{date}\">{label}</time></li>".format(
                url=escape(card["url"], quote=True),
                title=escape(card["title"], quote=False),
                date=escape(card["date"], quote=True),
                label=escape(card["date_label"], quote=False),
            )
        )
    body = "\n".join(lis)
    return (
        "<aside class=\"more-from\" aria-label=\"More from OctoProbe News\">\n"
        "<h2 id=\"more-from-octoprobe-news\">More from OctoProbe News</h2>\n"
        "<ul>\n"
        f"{body}\n"
        "</ul>\n"
        "</aside>"
    )


_ARTICLE_END_RE = re.compile(r"</article>")
# Drop an existing block, including the blank lines around it, so a second run is stable.
_POST_STRIP_RE = re.compile(r"\n*" + re.escape(POST_START) + r".*?" + re.escape(POST_END) + r"\n*", re.S)


def render_post(html: str, slug: str, items: list[dict] | None = None) -> str:
    """Place More from OctoProbe News immediately after </article>.

    Article checkers count copy inside <article>. The five links stay in the
    same aside, between the latest markers, outside that element.
    """
    picked = [c for c in (items if items is not None else cards()) if c["slug"] != slug][:POST_COUNT]
    if len(picked) < POST_COUNT:
        raise SystemExit(f"ERROR: {slug} needs {POST_COUNT} newer-or-other posts, found {len(picked)}")
    if html.count(POST_START) > 1 or html.count(POST_END) > 1:
        raise SystemExit(f"ERROR: {slug} latest markers are duplicated")
    wrapped = f"{POST_START}\n{_post_block(picked)}\n{POST_END}"
    html = _POST_STRIP_RE.sub("\n", html, count=1)
    art = _ARTICLE_END_RE.search(html)
    if not art:
        raise SystemExit(f"ERROR: {slug} has no </article> to place the latest list after")
    return html[:art.end()] + "\n" + wrapped + "\n" + html[art.end():]


def refresh_home(check: bool = False) -> bool:
    new = render_home()
    old = HOME.read_text(encoding="utf-8")
    if new == old:
        return False
    if check:
        return True
    HOME.write_text(new, encoding="utf-8")
    return True


def refresh_posts(check: bool = False) -> list[str]:
    stale = []
    index_cards = cards()
    for path in live_posts():
        slug = path.parent.name
        old = path.read_text(encoding="utf-8")
        new = render_post(old, slug, index_cards)
        if new != old:
            stale.append(str(path.relative_to(ROOT)))
            if not check:
                path.write_text(new, encoding="utf-8")
    return stale
