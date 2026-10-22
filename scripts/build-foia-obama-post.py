#!/usr/bin/env python3
"""Build the Obama Library FOIA how-to (Public Journalism Guide) from markdown.
Same pattern as scripts/build-usss-post.py (reuses its typography helpers and NEWS_FRAME,
scripts/build-blog.py, scripts/authors.py and blog/_template.html), with:
  * {{MODULE:name}} -> figure/table modules from scripts/foia-obama-modules.py (post-local foia.css)
  * {{ANSWER}}, {{FAQ}} (+ FAQPage JSON-LD), {{AUTHOR_NOTE}} (default author Colin Aamot)
  * NewsArticle + BreadcrumbList + HowTo + FAQPage JSON-LD
Source: blog/posts/foia-how-to-obama-situation-room-photos-presidential-records.md
Usage (repo root):  python3 scripts/build-foia-obama-post.py
Writes blog/<slug>/index.html; assets/ files are committed as-is. No third-party packages.
"""
import importlib.util, json, re, sys
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "blog" / "posts" / "foia-how-to-obama-situation-room-photos-presidential-records.md"
def _load(name, file):
    s = importlib.util.spec_from_file_location(name, REPO / "scripts" / file)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
U = _load("usss_build", "build-usss-post.py")   # smart(), smart_html(), inline_em(), no_em(), NEWS_FRAME
MODS = _load("foia_obama_modules", "foia-obama-modules.py")
bb = U.bb

HOWTO = [
    ("Find who holds the records", "Ask the office that has them: an agency's FOIA office, or the presidential library for presidential records. Search its reading room first.", "step-1-find-who-holds-the-records"),
    ("Describe the records precisely", "Name the record type, the people, the place and the time, and ask for the metadata that describes each record.", "step-2-describe-the-records-precisely"),
    ("File it and log the case number", "Submit in writing, keep the acknowledgment and use the case number for status checks, appeals and finding the release.", "step-3-file-it-and-log-the-case-number"),
    ("Read the response line by line", "Note how much was processed and released and which restriction or exemption code covers each withheld item.", "step-4-read-the-response-line-by-line"),
    ("Download the free copies, then order what you need", "Download released records free from the library and the National Archives Catalog; order high-resolution copies by frame number.", "step-5-download-the-free-copies-then-order-what-you-need"),
    ("Push for what was withheld", "Appeal within ninety days, request declassification review of specific items, contact the FOIA Public Liaison or OGIS, and track when restrictions expire.", "step-6-push-for-what-was-withheld"),
]

def build():
    meta, body_md = bb.parse_frontmatter(SRC.read_text(encoding="utf-8"))
    for wmsg in bb.validate_meta(meta, SRC, strict=True):
        print("WARNING:", wmsg, file=sys.stderr)
    slug = meta["slug"]; title = meta["title"]; date = meta["date"]; description = meta["description"]
    dt = bb.datetime.strptime(date[:10], "%Y-%m-%d"); date_display = f"{dt.strftime('%b')} {dt.day}, {dt.year}"
    tags_html = '<div class="tags">' + "".join(f'<span class="{bb.tag_class(t)}">{escape(t)}</span>' for t in meta["tags"]) + "</div>"
    for f in meta.get("faq") or []:
        f["q"], f["a"] = U.smart(f["q"]), U.smart(f["a"])
    meta["primary_question"] = U.smart(meta.get("primary_question", "")); meta["answer_first"] = U.smart(meta.get("answer_first", ""))
    html = bb.md_to_html(body_md)
    html = U.smart_html(html.replace("&quot;", '"').replace("&#x27;", "'"))
    html = re.sub(r"\[([^\]]+)\]\(mailto:([^)\s]+)\)", r'<a href="mailto:\2">\1</a>', html)  # inline_md has no mailto links
    html = re.sub(r"(?<!<div class=\"table-wrap\">)\n<table>(.*?)</table>", r'\n<div class="table-wrap"><table>\1</table></div>', html, flags=re.S)
    def h3id(m):
        sid = re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", m.group(1)).lower()).strip("-")
        return f'<h3 id="{sid}">{m.group(1)}</h3>'
    html = re.sub(r"<h3>(.*?)</h3>", h3id, html)
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
    for _, _, anchor in HOWTO:
        assert f'id="{anchor}"' in html, anchor

    ld = bb.build_json_ld(meta, slug, description)
    canonical = meta["canonical"]
    section = meta.get("section") or "Investigations"
    ld[0]["articleSection"] = section
    ld[0]["about"] = [{"@type": "Thing", "name": n} for n in ["Freedom of Information Act", "Presidential Records Act", "presidential records", "White House Situation Room", "declassification"]]
    ld[0]["mentions"] = [
        {"@type": "GovernmentOrganization", "name": "Barack Obama Presidential Library", "url": "https://www.obamalibrary.gov/"},
        {"@type": "GovernmentOrganization", "name": "National Archives and Records Administration", "url": "https://www.archives.gov/"},
        {"@type": "Legislation", "name": "Freedom of Information Act, 5 U.S.C. § 552", "url": "https://www.law.cornell.edu/uscode/text/5/552"},
        {"@type": "Legislation", "name": "Presidential Records Act, 44 U.S.C. §§ 2201–2209", "url": "https://www.law.cornell.edu/uscode/text/44/2204"},
        {"@type": "Legislation", "name": "Executive Order 13526", "url": "https://www.archives.gov/isoo/policy-documents/cnsi-eo.html"},
    ]
    ld.append({"@context": "https://schema.org", "@type": "HowTo", "name": "How to file a FOIA request that gets records released",
        "description": description,
        "supply": [{"@type": "HowToSupply", "name": "A written FOIA request (online form, email or letter)"}],
        "tool": [{"@type": "HowToTool", "name": "Obama Library digital research room"}, {"@type": "HowToTool", "name": "National Archives Catalog"}],
        "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t, "url": f"{canonical}#{a}"} for i, (n, t, a) in enumerate(HOWTO)]})
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": U.no_em(f["q"]), "acceptedAnswer": {"@type": "Answer", "text": U.no_em(f["a"])}} for f in faq]})
    ld_scripts = "\n".join(f'<script type="application/ld+json">\n{json.dumps(b, indent=2, ensure_ascii=False)}\n</script>' for b in ld)
    og_title = bb.social_title(meta)
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
<meta property="article:published_time" content="{escape(date)}">
<meta property="article:modified_time" content="{escape(meta.get('date_modified') or date)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@octoprobeai">
<meta name="twitter:title" content="{escape(og_title)}">
<meta name="twitter:description" content="{escape(description)}">
<meta name="twitter:image" content="{escape(og)}">
<meta name="twitter:image:alt" content="{escape(meta.get('hero_alt') or meta.get('image_alt') or title)}">
{ld_scripts}"""
    byline_html = bb.AU.byline_html(person, meta.get("byline") or "OctoProbe Staff")
    tpl = bb.TEMPLATE.read_text(encoding="utf-8")
    out = (tpl.replace("{{HEAD_META}}", head).replace("{{TITLE}}", escape(title)).replace("{{DATE}}", escape(date))
           .replace("{{DATE_DISPLAY}}", escape(date_display)).replace("{{TAGS_HTML}}", tags_html)
           .replace("{{BYLINE_HTML}}", byline_html)
           .replace("\n      {{HERO_HTML}}", "").replace("{{HERO_HTML}}", "").replace("{{BODY}}", html))
    out = out.replace('<span class="eyebrow">Investigations</span>', f'<span class="eyebrow">{escape(section)}</span>', 1)
    out = out.replace("</h1>", "</h1>\n      <p class=\"post-dek\">" + escape(U.smart(meta["dek"])) + "</p>", 1)
    out = out.replace('<link rel="stylesheet" href="/assets/css/blog.css?v=news8">',
        '<link rel="stylesheet" href="/assets/css/blog.css?v=news8">\n' + U.NEWS_FRAME +
        f'\n<link rel="stylesheet" href="/blog/{slug}/assets/foia.css?v=1">', 1)
    out = re.sub(r'\s*<p class="post-disclaimer">.*?</p>', "", out, count=1, flags=re.S)
    dest = REPO / "blog" / slug / "index.html"; dest.write_text(out, encoding="utf-8"); print("built", dest.relative_to(REPO))
    return out

if __name__ == "__main__":
    build()
