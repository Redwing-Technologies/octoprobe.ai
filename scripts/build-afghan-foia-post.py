#!/usr/bin/env python3
"""Build the Afghanistan withdrawal / Kabul evacuation FOIA post from markdown.
Same pattern as scripts/build-foia-obama-post.py (reuses build-usss-post.py typography helpers
and NEWS_FRAME, scripts/build-blog.py, scripts/authors.py and blog/_template.html), with:
  * {{MODULE:name}} -> figure/table modules from scripts/afghan-foia-modules.py (post-local afghan.css)
  * NOTE: paragraphs -> <p class="editor-note">Editor’s note: …</p>
  * {{ANSWER}}, {{FAQ}} (+ FAQPage JSON-LD), {{AUTHOR_NOTE}} (default author Colin Aamot)
  * NewsArticle + BreadcrumbList + HowTo + FAQPage JSON-LD
  * Publication dates: front matter `published_iso` (and optional `modified_iso`) are full ISO 8601
    with offset; they feed JSON-LD datePublished/dateModified, article:*_time and <time datetime>,
    and the visible "Published Mon D, YYYY" label is derived from the same value.
Source: blog/posts/afghanistan-withdrawal-foia-kabul-evacuation-record.md
Usage (repo root):  python3 scripts/build-afghan-foia-post.py
Writes blog/<slug>/index.html; assets/ and docs/ files are committed as-is. No third-party packages.
"""
import importlib.util, json, re, sys
from datetime import datetime
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "blog" / "posts" / "afghanistan-withdrawal-foia-kabul-evacuation-record.md"
def _load(name, file):
    s = importlib.util.spec_from_file_location(name, REPO / "scripts" / file)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
U = _load("usss_build", "build-usss-post.py")
MODS = _load("afghan_foia_modules", "afghan-foia-modules.py")
bb = U.bb
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$")

def build():
    meta, body_md = bb.parse_frontmatter(SRC.read_text(encoding="utf-8"))
    for wmsg in bb.validate_meta(meta, SRC, strict=True):
        print("WARNING:", wmsg, file=sys.stderr)
    slug = meta["slug"]; title = meta["title"]; description = meta["description"]
    pub = meta["published_iso"]; mod = meta.get("modified_iso") or pub
    assert ISO_RE.match(pub) and ISO_RE.match(mod), (pub, mod)
    dpub, dmod = datetime.fromisoformat(pub), datetime.fromisoformat(mod)
    assert dpub <= dmod <= datetime.now().astimezone(), "published <= modified <= now"
    assert meta["date"] == pub[:10], "front matter date must equal the calendar date of published_iso"
    date_display = f"{dpub.strftime('%b')} {dpub.day}, {dpub.year}"
    tags_html = '<div class="tags">' + "".join(f'<span class="{bb.tag_class(t)}">{escape(t)}</span>' for t in meta["tags"]) + "</div>"
    for f in meta.get("faq") or []:
        f["q"], f["a"] = U.smart(f["q"]), U.smart(f["a"])
    meta["primary_question"] = U.smart(meta.get("primary_question", "")); meta["answer_first"] = U.smart(meta.get("answer_first", ""))
    title = U.smart(title); meta["title"] = title
    html = bb.md_to_html(body_md)
    html = U.smart_html(html.replace("&quot;", '"').replace("&#x27;", "'"))
    html = re.sub(r"<p>NOTE:\s*(.*?)</p>", r'<p class="editor-note">Editor’s note: \1</p>', html, flags=re.S)
    html = re.sub(r"(?<!<div class=\"table-wrap\">)\n<table>(.*?)</table>", r'\n<div class="table-wrap"><table>\1</table></div>', html, flags=re.S)
    def hid(m):
        lvl, inner = m.group(1), m.group(2)
        sid = re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", inner).lower().replace("’", "")).strip("-")
        return f'<h{lvl} id="{sid}">{inner}</h{lvl}>'
    html = re.sub(r"<h([23])>(.*?)</h\1>", hid, html)
    html = re.sub(r"<p>\{\{MODULE:([a-z0-9-]+)\}\}</p>", lambda m: MODS.MODULES[m.group(1)].rstrip(), html)
    q = escape(meta["primary_question"]); a = escape(meta["answer_first"])
    html = html.replace("<p>{{ANSWER}}</p>", f'<p class="primary-question"><strong>{q}</strong></p>\n<p class="answer-first">{a}</p>')
    faq = meta.get("faq") or []
    faq_html = '<section class="faq" aria-labelledby="frequently-asked-questions">\n<h2 id="frequently-asked-questions">Frequently Asked Questions</h2>\n' + "\n".join(
        f"<h3>{U.inline_em(escape(f['q']))}</h3>\n<p>{U.inline_em(escape(f['a']))}</p>" for f in faq) + "\n</section>"
    html = html.replace("<p>{{FAQ}}</p>", faq_html)
    person = bb.AU.resolve_author(meta)
    html = bb.AU.insert_author_note(html, bb.AU.author_note_html(person))
    assert "{{" not in html, re.findall(r"\{\{[^}]+\}\}", html)
    for _, _, anchor in MODS.HOWTO:
        assert f'id="{anchor}"' in html, anchor

    ld = bb.build_json_ld(meta, slug, description)
    canonical = meta["canonical"]
    ld[0]["headline"] = title
    ld[0]["datePublished"] = pub; ld[0]["dateModified"] = mod
    ld[0]["articleSection"] = meta.get("section") or "Investigations"
    ld[1]["itemListElement"][2]["name"] = title
    ld[0]["about"] = [{"@type": "Thing", "name": n} for n in [
        "2021 Afghanistan withdrawal", "Evacuation of U.S. Embassy Kabul", "Noncombatant evacuation operation",
        "Freedom of Information Act", "Operation Allies Refuge"]]
    ld[0]["mentions"] = [
        {"@type": "GovernmentOrganization", "name": "U.S. Department of State Office of Inspector General", "url": "https://www.stateoig.gov/"},
        {"@type": "GovernmentOrganization", "name": "U.S. Embassy Kabul"},
        {"@type": "GovernmentOrganization", "name": "U.S. Navy"},
        {"@type": "GovernmentOrganization", "name": "U.S. Central Command"},
        {"@type": "Report", "name": "AUD-MERO-23-15, Review of Emergency Action Planning Guiding the Evacuation of U.S. Embassy Kabul, Afghanistan", "url": "https://www.stateoig.gov/report/aud-mero-23-15"},
        {"@type": "Report", "name": "AUD-MERO-23-33, OIG’s Review of the Department of State’s Evacuation of U.S. Embassy Kabul, Afghanistan", "url": MODS.M33},
        {"@type": "Report", "name": "ISP-S-23-05A, Classified Annex to the Inspection of the Afghanistan Affairs Unit", "url": "https://www.stateoig.gov/report/isp-s-23-05a"},
        {"@type": "Report", "name": "ISP-I-23-05, Inspection of the Afghanistan Affairs Unit", "url": MODS.I05},
        {"@type": "Legislation", "name": "Freedom of Information Act, 5 U.S.C. § 552", "url": "https://www.law.cornell.edu/uscode/text/5/552"},
    ]
    ld.append({"@context": "https://schema.org", "@type": "HowTo", "name": "How to reconstruct military events from FOIA documents",
        "description": "Seven steps for rebuilding a dated record of a military or diplomatic event from records released under the Freedom of Information Act.",
        "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t, "url": f"{canonical}#{a}"} for i, (n, t, a) in enumerate(MODS.HOWTO)]})
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": U.no_em(f["q"]), "acceptedAnswer": {"@type": "Answer", "text": U.no_em(f["a"])}} for f in faq]})
    ld_scripts = "\n".join(f'<script type="application/ld+json">\n{json.dumps(b, indent=2, ensure_ascii=False)}\n</script>' for b in ld)
    og_title = U.smart(bb.social_title(meta))
    og = bb.light_og_url(slug); kw = ", ".join(meta.get("keywords") or meta["tags"])
    head = f"""<title>{escape(bb.compose_page_title(meta.get("seo_title") or title))}</title>
<meta name="description" content="{escape(description)}">
<meta name="keywords" content="{escape(kw)}">
<meta name="author" content="{escape(person['name'] if person else 'OctoProbe Staff')}">
<link rel="alternate" type="text/plain" title="LLM context (llms.txt)" href="/llms.txt">
<link rel="alternate" type="text/plain" title="AI discovery (ai.txt)" href="/ai.txt">
<link rel="alternate" type="application/rss+xml" title="OctoProbe News" href="https://www.octoprobe.ai/blog/feed.xml">
<meta name="ai-content-declaration" content="human-authored; investigative reporting from public records">
<link rel="canonical" href="{escape(canonical)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="OctoProbe News">
<meta property="og:url" content="{escape(canonical)}">
<meta property="og:title" content="{escape(og_title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:image" content="{escape(og)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{escape(meta.get('hero_alt') or title)}">
<meta property="article:published_time" content="{escape(pub)}">
<meta property="article:modified_time" content="{escape(mod)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@octoprobeai">
<meta name="twitter:title" content="{escape(og_title)}">
<meta name="twitter:description" content="{escape(description)}">
<meta name="twitter:image" content="{escape(og)}">
<meta name="twitter:image:alt" content="{escape(meta.get('hero_alt') or meta.get('image_alt') or title)}">
{ld_scripts}"""
    byline_html = bb.AU.byline_html(person, meta.get("byline") or "OctoProbe Staff")
    tpl = bb.TEMPLATE.read_text(encoding="utf-8")
    tpl = tpl.replace('<time datetime="{{DATE}}">{{DATE_DISPLAY}}</time>',
                      '<span class="date-label">Published</span> <time datetime="{{DATE}}">{{DATE_DISPLAY}}</time>', 1)
    out = (tpl.replace("{{HEAD_META}}", head).replace("{{TITLE}}", escape(title, quote=False)).replace("{{DATE}}", escape(pub))
           .replace("{{DATE_DISPLAY}}", escape(date_display)).replace("{{TAGS_HTML}}", tags_html)
           .replace("{{BYLINE_HTML}}", byline_html)
           .replace("\n      {{HERO_HTML}}", "").replace("{{HERO_HTML}}", "").replace("{{BODY}}", html))
    out = out.replace("</h1>", "</h1>\n      <p class=\"post-dek\">" + escape(U.smart(meta["dek"]), quote=False) + "</p>", 1)
    out = out.replace('<link rel="stylesheet" href="/assets/css/blog.css?v=news13">',
        '<link rel="stylesheet" href="/assets/css/blog.css?v=news13">\n' + U.NEWS_FRAME +
        f'\n<link rel="stylesheet" href="/blog/{slug}/assets/afghan.css?v=1">', 1)
    out = re.sub(r'\s*<p class="post-disclaimer">.*?</p>', "", out, count=1, flags=re.S)
    dest = REPO / "blog" / slug / "index.html"; dest.write_text(out, encoding="utf-8"); print("built", dest.relative_to(REPO))
    return out

if __name__ == "__main__":
    build()
    import runpy
    from pathlib import Path
    _root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(_root / "scripts" / "refresh-home-latest.py"), run_name="__main__")
    runpy.run_path(str(_root / "scripts" / "refresh-latest-links.py"), run_name="__main__")
