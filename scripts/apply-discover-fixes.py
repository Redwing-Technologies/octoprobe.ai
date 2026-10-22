#!/usr/bin/env python3
"""Pad Discover image variants and patch built blog posts in place.

Does not rebuild posts. Covers keep their full frame: 16:9, 4:3 and 1:1 canvases
are a blurred extension of the same image, with the sharp cover centered.
Original PNG/JPG files stay. WebP siblings are what browsers load.

Idempotent. Run from the repo root:

  python3 scripts/apply-discover-fixes.py
"""
from __future__ import annotations

import json
import re
from html import escape, unescape
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.octoprobe.ai"
BRAND = " · OctoProbe News"
ARTICLE_TYPES = {
    "NewsArticle", "AnalysisNewsArticle", "OpinionNewsArticle", "ReportageNewsArticle",
    "Article", "BlogPosting", "TechArticle", "Report",
}
ORPHANS = {
    "a", "an", "the", "of", "and", "or", "to", "for", "in", "on", "at", "by",
    "with", "from", "into", "over", "its", "their", "was", "as",
}
RASTER = {".png", ".jpg", ".jpeg", ".webp"}
# Slugs whose <title> is already inside 50–60. Left unchanged.
UNCHANGED = {
    "gaza-now-telegram-hamas-fundraising-sanctions-sabassi",
    "identifier-graph-osint-methodology",
    "isis-media-survives-takedowns",
    "north-korea-it-worker-personas-backstopping",
    "signal-osint-sigtop-endpoint-collection",
}
# Drop the brand suffix only. og:title / twitter:title stay.
DROP_SUFFIX = {
    "afghanistan-withdrawal-foia-kabul-evacuation-record",
    "cefc-china-energy-pla-base-311-public-record",
    "crowdfunding-hamas-chuffed-gofundme-gaza",
    "dia-islamic-jihad-foia-intelligence-reports-osint",
    "fbi-cell-phone-location-silent-sms-cast-guide",
    "foia-how-to-obama-situation-room-photos-presidential-records",
    "iran-hormuz-mine-strike-claims-fall-apart",
    "machiaveli-dark-web-cocaine-spokane-nabi",
}
# New <title>, and whether og:title / twitter:title should match it.
REWRITES = {
    "archive-today-donate-link-takion-api-developer": (
        "Archive.today’s Donate Link Names an Anti-Bot Developer", True),
    "christopher-burns-fbi-fugitive-google-maps-wayne-pa": (
        "Christopher W. Burns: Google Maps After His Last Sighting", True),
    "dhs-phone-location-data-legal-opinion-foia": (
        "DHS Withheld Its Legal Case for Buying Location Data", True),
    "foia-assessments-redacted-logs-osint-pivots": (
        "Redacted, Not Useless: FOIA Logs Used as OSINT Pivots", False),
    "heather-zhang-prc-agent-case-reddit-allegation": (
        "Heather Zhang Case: OSINT From a 2024 Reddit Allegation", True),
    "hexane-afd-leak-actor-scope-access": (
        "Hexane’s AfD Dump: The Actor, the Scope, and the Access", True),
    "help-tds-hotejka-tech-support-scam-new-server": (
        "Help TDS Tech-Support Scam Still Running From a New Server", True),
    "iraq-international-development-bank-ofac-iran-dollars-shadow-banking": (
        "AML Conference Sponsor Sent Iran Dollars, Treasury Says", False),
    "karnakis-and-karnakis-panama-law-firm-iran-shadow-fleet-ofac": (
        "Karnakis Panama Firm Linked to Iran’s OFAC Shadow Fleet", True),
    "myrotvorets-informnapalm-ned-grant": (
        "NED Grants to Myrotvorets and InformNapalm Projects", True),
    "north-korean-laptop-farm-texas-gmail-accounts": (
        "North Korea’s Texas Laptop Farms and Tied Gmail Accounts", True),
    "saudi-intelligence-spy-list-leak-houthi": (
        "Alleged Saudi Spy List Leaked by Houthi-Tied Group", True),
    "secret-service-foia-sharepoint-browser-history-osint-guide": (
        "How to FOIA Browser History, SharePoint, and Teams", False),
    "subpoena-warrant-online-accounts-three-branches": (
        "Subpoena vs. Warrant: What Each Branch of Government Gets", False),
    "whales-shipping-line-ofac-iran-shadow-fleet-dubai-agent": (
        "Whales Shipping Line: Sanctioned, and Its Staff Still Named", True),
    "white-house-vetting-leak-press-clips": (
        "Leaked White House Vetting File: 25 Pages of Press Clips", True),
}
SET_TITLE_TO_H1 = {
    "centcom-war-orders-anvil-chart-foia",
    "pegasus-nso-capabilities-historical-data-attribution",
}
BURNS_H1 = (
    "Christopher W. Burns (FBI Most Wanted): Public Google Maps Activity "
    "After His Last Sighting, Wayne, PA Area"
)


def posts() -> list[Path]:
    out = []
    for p in sorted((ROOT / "blog").glob("*/index.html")):
        html = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in html:
            continue
        if '<meta property="og:type" content="article">' not in html:
            continue
        out.append(p)
    return out


def local_path(url: str, html_path: Path) -> Path | None:
    url = unescape(url).split("#", 1)[0].split("?", 1)[0].strip()
    if not url or url.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None
    if url.startswith(SITE + "/"):
        url = url[len(SITE):]
    elif url.startswith("http://") or url.startswith("https://"):
        return None
    if url.startswith("/"):
        return ROOT / url.lstrip("/")
    return (html_path.parent / url).resolve()


def to_rgb(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im)
    if im.mode == "RGB":
        return im
    if im.mode == "RGBA":
        bg = Image.new("RGB", im.size, (15, 27, 45))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def fit_pad(im: Image.Image, tw: int, th: int) -> Image.Image:
    """Contain the full frame on a blurred extension. Never crops the sharp image."""
    im = to_rgb(im)
    scale = min(tw / im.width, th / im.height)
    nw, nh = max(1, round(im.width * scale)), max(1, round(im.height * scale))
    sharp = im.resize((nw, nh), Image.Resampling.LANCZOS)
    cover = max(tw / im.width, th / im.height)
    bw, bh = max(tw, round(im.width * cover)), max(th, round(im.height * cover))
    bg = im.resize((bw, bh), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(radius=28))
    left, top = max(0, (bw - tw) // 2), max(0, (bh - th) // 2)
    bg = bg.crop((left, top, left + tw, top + th))
    if bg.size != (tw, th):
        canvas = Image.new("RGB", (tw, th), (15, 27, 45))
        canvas.paste(bg, (0, 0))
        bg = canvas
    bg.paste(sharp, ((tw - nw) // 2, (th - nh) // 2))
    return bg


def to_og(im: Image.Image) -> Image.Image:
    im = to_rgb(im)
    if abs((im.width / im.height) - (1200 / 630)) < 0.015:
        return im.resize((1200, 630), Image.Resampling.LANCZOS)
    return fit_pad(im, 1200, 630)


def save_jpg_under(im: Image.Image, dest: Path, limit: int = 300 * 1024) -> int:
    q = 85
    dest.parent.mkdir(parents=True, exist_ok=True)
    while q >= 50:
        im.save(dest, "JPEG", quality=q, optimize=True, progressive=True)
        if dest.stat().st_size <= limit:
            return q
        q -= 5
    return q


def save_webp(im: Image.Image, dest: Path, q: int) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=q, method=4)


def variant_name(src: str, width: int) -> str:
    bare = src.split("?", 1)[0]
    stem = bare.rsplit(".", 1)[0]
    return f"{stem}-{width}.webp"


def attr(tag: str, name: str) -> str | None:
    m = re.search(r'\s' + name + r'="([^"]*)"', tag)
    return m.group(1) if m else None


def set_attr(tag: str, name: str, value: str) -> str:
    if re.search(r'\s' + name + r'="', tag):
        return re.sub(r'\s' + name + r'="[^"]*"', f' {name}="{value}"', tag, count=1)
    if tag.endswith("/>"):
        return tag[:-2].rstrip() + f' {name}="{value}" />'
    return tag[:-1] + f' {name}="{value}">'


def del_attr(tag: str, name: str) -> str:
    return re.sub(r'\s' + name + r'="[^"]*"', "", tag, count=1)


def referenced_bytes(html: str, html_path: Path) -> int:
    seen: set[Path] = set()
    total = 0
    urls = re.findall(r'<img\b[^>]*\ssrc="([^"]+)"', html)
    og = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    if og:
        urls.append(og.group(1))
    for url in urls:
        if "/assets/authors/" in url:
            continue
        f = local_path(url, html_path)
        if f is None or f.suffix.lower() not in RASTER or f in seen or not f.is_file():
            continue
        seen.add(f)
        total += f.stat().st_size
    return total


def page_title(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    return unescape(re.sub(r"\s+", " ", m.group(1))).strip() if m else ""


def page_h1(html: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    text = re.sub(r"<[^>]+>", "", m.group(1)) if m else ""
    return unescape(re.sub(r"\s+", " ", text)).strip()


def assert_title(slug: str, text: str) -> None:
    if not (50 <= len(text) <= 60):
        raise SystemExit(f"{slug}: title {text!r} is {len(text)} chars")
    last = re.sub(r"[^\w’']+$", "", text.split()[-1]).lower().replace("’", "'")
    if last in ORPHANS:
        raise SystemExit(f"{slug}: title ends with orphan word {last!r}: {text}")


def replace_tag_text(html: str, tag: str, value: str) -> str:
    new, n = re.subn(
        rf"<{tag}[^>]*>.*?</{tag}>",
        f"<{tag}>{escape(value, quote=False)}</{tag}>",
        html,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit(f"could not replace <{tag}>")
    return new


def replace_meta(html: str, kind: str, prop: str, value: str) -> str:
    esc = escape(value, quote=True)
    pat = rf'(<meta\s+{kind}="{re.escape(prop)}"\s+content=")[^"]*(")'
    new, n = re.subn(pat, lambda m: m.group(1) + esc + m.group(2), html, count=1)
    if n != 1:
        raise SystemExit(f"could not replace {prop}")
    return new


def upsert_after(html: str, anchor_pat: str, line: str) -> str:
    if line.split("content=", 1)[0] in html and re.search(
        re.escape(line.split(" content=", 1)[0]), html
    ):
        return html
    m = re.search(anchor_pat, html)
    if not m:
        raise SystemExit(f"anchor missing for {line[:40]}")
    return html[: m.end()] + line + "\n" + html[m.end() :]


def patch_titles(slug: str, html: str) -> tuple[str, str, str]:
    old = page_title(html)
    h1 = page_h1(html)
    new = old
    set_og = False
    if slug in UNCHANGED:
        pass
    elif slug in DROP_SUFFIX:
        if not old.endswith(BRAND):
            raise SystemExit(f"{slug}: expected brand suffix, got {old!r}")
        new = old[: -len(BRAND)]
        assert_title(slug, new)
    elif slug in SET_TITLE_TO_H1:
        new = h1
        assert_title(slug, new)
    elif slug in REWRITES:
        new, set_og = REWRITES[slug]
        assert_title(slug, new)
    else:
        raise SystemExit(f"{slug}: no title rule")
    if slug == "christopher-burns-fbi-fugitive-google-maps-wayne-pa":
        if len(BURNS_H1) > 110:
            raise SystemExit("burns H1 is over 110")
        html = replace_tag_text(html, "h1", BURNS_H1)
    if new != old:
        html = replace_tag_text(html, "title", new)
    if set_og:
        html = replace_meta(html, "property", "og:title", new)
        html = replace_meta(html, "name", "twitter:title", new)
    return html, old, new if new != old else ""


def patch_jsonld(html: str, urls: list[str], headline: str | None) -> str:
    def repl(m: re.Match) -> str:
        data = json.loads(m.group(1))
        changed = False

        def walk(node) -> None:
            nonlocal changed
            if isinstance(node, dict):
                types = node.get("@type")
                types = types if isinstance(types, list) else [types]
                if any(t in ARTICLE_TYPES for t in types):
                    node["image"] = list(urls)
                    if headline and "headline" in node:
                        node["headline"] = headline
                    changed = True
                for v in node.values():
                    if isinstance(v, (dict, list)):
                        walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)

        walk(data)
        if not changed:
            return m.group(0)
        return '<script type="application/ld+json">\n' + json.dumps(data, indent=2, ensure_ascii=False) + "\n</script>"

    return re.sub(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', repl, html, flags=re.S)


def patch_images(html: str, html_path: Path, made: dict[Path, list[int]]) -> str:
    out = []
    pos = 0
    hero_done = False
    for m in re.finditer(r"<img\b[^>]*>", html):
        out.append(html[pos:m.start()])
        tag = m.group(0)
        pos = m.end()
        src = attr(tag, "src") or ""
        if "/assets/authors/" in src or not src:
            out.append(tag)
            continue
        f = local_path(src, html_path)
        if f is None or f.suffix.lower() not in RASTER or f not in made:
            out.append(tag)
            continue
        widths = made[f]
        is_hero = not hero_done
        hero_done = True
        if not attr(tag, "width") or not attr(tag, "height"):
            with Image.open(f) as im:
                tag = set_attr(tag, "width", str(im.size[0]))
                tag = set_attr(tag, "height", str(im.size[1]))
        if is_hero:
            tag = del_attr(tag, "loading")
            tag = set_attr(tag, "fetchpriority", "high")
        elif attr(tag, "loading") != "lazy":
            tag = set_attr(tag, "loading", "lazy")
        if not attr(tag, "decoding"):
            tag = set_attr(tag, "decoding", "async")
        pre = html[max(0, m.start() - 2500):m.start()]
        in_picture = pre.rfind("<picture") > pre.rfind("</picture")
        if in_picture:
            out.append(tag)
            continue
        parts = [f"{variant_name(src, w)} {w}w" for w in widths]
        figure = pre.rfind("<figure")
        figure_html = pre[figure:] if figure >= 0 else ""
        phone = "shot-open" in figure_html or "shot-mobile" in figure_html
        sizes = "(max-width: 600px) 60vw, 241px" if phone else "(min-width: 900px) 760px, 100vw"
        srcset = escape(", ".join(parts), quote=True)
        out.append(
            '<picture style="display:contents">'
            f'<source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
            f"{tag}</picture>"
        )
    out.append(html[pos:])
    return "".join(out)


def main() -> None:
    Image.MAX_IMAGE_PIXELS = None
    pages = posts()
    before = {p.parent.name: referenced_bytes(p.read_text(encoding="utf-8"), p) for p in pages}
    title_changes = []
    qualities = {}
    for page in pages:
        slug = page.parent.name
        html = page.read_text(encoding="utf-8")
        hero_src = None
        made: dict[Path, list[int]] = {}
        for m in re.finditer(r'<img\b[^>]*\ssrc="([^"]+)"', html):
            src = m.group(1)
            if "/assets/authors/" in src:
                continue
            f = local_path(src, page)
            if f is None or f.suffix.lower() not in RASTER or not f.is_file():
                continue
            if hero_src is None:
                hero_src = (src, f)
            if f in made:
                continue
            with Image.open(f) as im:
                im = to_rgb(im)
                widths = [w for w in (800, 1200, 1600) if w < im.width]
                if not widths:
                    widths = [im.width]
                q = 80
                if hero_src and f == hero_src[1]:
                    q = 80
                    largest = widths[-1]
                    while q >= 55:
                        test = im.resize(
                            (largest, max(1, round(im.height * largest / im.width))),
                            Image.Resampling.LANCZOS,
                        ) if largest != im.width else im
                        tmp = f.with_name(f".tmp-{f.stem}.webp")
                        save_webp(test, tmp, q)
                        if tmp.stat().st_size <= 300 * 1024:
                            tmp.unlink()
                            break
                        tmp.unlink()
                        q -= 5
                    qualities[slug] = q
                for w in widths:
                    dest = f.with_name(f"{f.stem}-{w}.webp")
                    frame = im if w == im.width else im.resize(
                        (w, max(1, round(im.height * w / im.width))), Image.Resampling.LANCZOS)
                    save_webp(frame, dest, q if f == hero_src[1] else 80)
            made[f] = widths
        if hero_src is None:
            raise SystemExit(f"{slug}: no hero image")
        with Image.open(hero_src[1]) as hero:
            hero.load()
            assets = page.parent / "assets"
            assets.mkdir(parents=True, exist_ok=True)
            save_webp(fit_pad(hero, 1920, 1080), assets / "cover-16x9.webp", 80)
            save_webp(fit_pad(hero, 1600, 1200), assets / "cover-4x3.webp", 80)
            save_webp(fit_pad(hero, 1200, 1200), assets / "cover-1x1.webp", 80)
            og_url_m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
            og_file = local_path(og_url_m.group(1), page) if og_url_m else None
            source = og_file if og_file and og_file.is_file() else hero_src[1]
            with Image.open(source) as og_im:
                q = save_jpg_under(to_og(og_im), assets / "og-cover-1200.jpg")
            qualities[slug] = (qualities.get(slug), q)
        urls = [
            f"{SITE}/blog/{slug}/assets/cover-16x9.webp",
            f"{SITE}/blog/{slug}/assets/cover-4x3.webp",
            f"{SITE}/blog/{slug}/assets/cover-1x1.webp",
        ]
        html, old, new = patch_titles(slug, html)
        if new:
            title_changes.append((slug, old, new))
        headline = BURNS_H1 if slug == "christopher-burns-fbi-fugitive-google-maps-wayne-pa" else None
        html = patch_jsonld(html, urls, headline)
        html = patch_images(html, page, made)
        og_url = f"{SITE}/blog/{slug}/assets/og-cover-1200.jpg"
        html = replace_meta(html, "property", "og:image", og_url)
        if 'name="twitter:image"' in html:
            html = replace_meta(html, "name", "twitter:image", og_url)
        else:
            raise SystemExit(f"{slug}: no twitter:image")
        if 'property="og:image:width"' in html:
            html = replace_meta(html, "property", "og:image:width", "1200")
            html = replace_meta(html, "property", "og:image:height", "630")
        else:
            html = html.replace(
                f'<meta property="og:image" content="{escape(og_url, quote=True)}">\n',
                f'<meta property="og:image" content="{escape(og_url, quote=True)}">\n'
                '<meta property="og:image:width" content="1200">\n'
                '<meta property="og:image:height" content="630">\n',
                1,
            )
        hero_alt = ""
        hm = re.search(r'<img\b[^>]*\salt="([^"]*)"', html) or re.search(r'<img\b[^>]*alt="([^"]*)"', html)
        # first content image alt, after the patch
        for im in re.finditer(r"<img\b[^>]*>", html):
            src = attr(im.group(0), "src") or ""
            if "/assets/authors/" in src:
                continue
            hero_alt = unescape(attr(im.group(0), "alt") or "")
            break
        if not hero_alt:
            raise SystemExit(f"{slug}: hero has no alt")
        if len(hero_alt) > 420:
            hero_alt = hero_alt[:417].rsplit(" ", 1)[0]
        if 'name="twitter:image:alt"' in html:
            html = replace_meta(html, "name", "twitter:image:alt", hero_alt)
        else:
            html = upsert_after(
                html,
                r'<meta name="twitter:image" content="[^"]*">\n',
                f'<meta name="twitter:image:alt" content="{escape(hero_alt, quote=True)}">',
            )
        if slug in {
            "archive-today-donate-link-takion-api-developer",
            "heather-zhang-prc-agent-case-reddit-allegation",
            "christopher-burns-fbi-fugitive-google-maps-wayne-pa",
        } or 'property="og:image:alt"' not in html:
            if 'property="og:image:alt"' in html:
                html = replace_meta(html, "property", "og:image:alt", hero_alt)
            else:
                anchor = r'<meta property="og:image:height" content="[^"]*">\n'
                if not re.search(anchor, html):
                    anchor = r'<meta property="og:image" content="[^"]*">\n'
                html = upsert_after(
                    html, anchor,
                    f'<meta property="og:image:alt" content="{escape(hero_alt, quote=True)}">',
                )
        page.write_text(html, encoding="utf-8")
        print(f"patched {slug} hero-q={qualities[slug][0]} og-q={qualities[slug][1]}")

    after_pages = posts()
    delivered = {}
    for page in after_pages:
        html = page.read_text(encoding="utf-8")
        total = 0
        seen = set()
        for pic in re.finditer(r'<picture\b[^>]*>\s*<source\b[^>]*srcset="([^"]+)"', html):
            parts = [p.strip().split() for p in pic.group(1).split(",") if p.strip()]
            best = None
            best_w = -1
            for part in parts:
                w = int(part[-1][:-1]) if part[-1].endswith("w") else 0
                if w > best_w:
                    best_w = w
                    best = part[0]
            f = local_path(unescape(best), page) if best else None
            if f and f.is_file() and f not in seen:
                seen.add(f)
                total += f.stat().st_size
        og = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        if og:
            f = local_path(og.group(1), page)
            if f and f.is_file() and f not in seen:
                total += f.stat().st_size
        delivered[page.parent.name] = total
    heaviest = sorted(before, key=lambda s: before[s], reverse=True)[:5]
    print("\nTITLES")
    for slug, old, new in title_changes:
        print(f"{len(old):3d}->{len(new):3d} {slug}\n  OLD {old}\n  NEW {new}")
    print("\nHEAVIEST before-referenced -> after-delivered")
    for slug in heaviest:
        print(f"{before[slug]:10d} -> {delivered[slug]:10d}  {slug}")
    report = {
        "titles": title_changes,
        "before": before,
        "delivered": delivered,
        "heaviest": heaviest,
        "qualities": {k: list(v) for k, v in qualities.items()},
    }
    Path("/tmp/discover-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("wrote /tmp/discover-report.json")


if __name__ == "__main__":
    main()
