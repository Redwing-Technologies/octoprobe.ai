#!/usr/bin/env python3
"""Build 'Inside the FBI's CAST Guide' (Investigations) from markdown.
Same pattern as scripts/build-adtech-post.py (reuses scripts/build-blog.py helpers,
scripts/authors.py and blog/_template.html), with:
  * NOTE: paragraphs -> <p class="editor-note">Editor’s note: …</p>
  * {{MODULE:name}} -> static modules from scripts/fbi-cell-geo-modules.py (page-image figures, source-document
    cards; small post-local CSS in the news-frame style block, no JS)
  * {{ANSWER}}, {{FAQ}} (+ FAQPage JSON-LD), {{AUTHOR_NOTE}} (default author Colin Aamot, Person JSON-LD)
  * og_title front-matter field for og:/twitter: titles; `section` sets the crumb eyebrow and
    NewsArticle.articleSection
Source: blog/posts/fbi-cell-phone-location-silent-sms-cast-guide.md
Usage (repo root):  python3 scripts/build-fbi-cell-geo-post.py
Writes blog/<slug>/index.html; assets/ (cover.png, og-cover.png, figs/) and docs/ (hosted PDFs) are committed as-is. No third-party packages.
"""
import importlib.util, json, re, sys, shutil
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "blog" / "posts" / "fbi-cell-phone-location-silent-sms-cast-guide.md"
_ms = importlib.util.spec_from_file_location("fcg_modules", REPO / "scripts" / "fbi-cell-geo-modules.py")
MODS = importlib.util.module_from_spec(_ms); _ms.loader.exec_module(MODS)
spec = importlib.util.spec_from_file_location("bb", REPO / "scripts" / "build-blog.py")
bb = importlib.util.module_from_spec(spec); spec.loader.exec_module(bb)

NEWS_FRAME = ('<style id="news-frame">.post-dek{max-width:46rem;margin:.6rem 0 0;font-size:1.15rem;line-height:1.5;color:#475569}'
 '.post-hero .byline{margin:1rem 0 0;font-weight:600;color:#334155;font-size:.98rem}.post-hero .byline a{color:inherit;text-decoration:underline;text-decoration-color:rgba(51,65,85,.35);text-underline-offset:3px}.post-hero .byline a:hover{color:var(--blue)}.table-wrap{overflow-x:auto}'
 '.table-wrap table{border-collapse:collapse;width:100%;font-size:.92rem}.table-wrap th,.table-wrap td{border:1px solid #e2e8f0;padding:.45rem .6rem;vertical-align:top;text-align:left}'
 '.related-reading{border-top:1px solid #e2e8f0;margin-top:2rem;padding-top:.5rem}.related-reading h2{margin-top:1rem}.related-reading li{margin:.4rem 0}'
 '.prose .faq h3{font-size:1.02rem;margin-top:1.2em}.prose .faq p{margin-top:.35em}'
 '.prose .doc-fig{margin:1.6em 0}.prose .doc-fig img{display:block;width:100%;height:auto;border:1px solid #e2e8f0;border-radius:8px;background:#fff}'
 '.doc-cards ul{list-style:none;margin:1.4em 0;padding:0;display:grid;gap:14px}.doc-cards .doc-card{display:grid;grid-template-columns:132px 1fr;gap:16px;align-items:start;border:1px solid #e2e8f0;border-radius:12px;padding:14px;margin:0;background:#f8fafc}'
 '.doc-cards .doc-thumb img{display:block;width:132px;height:auto;border:1px solid #e2e8f0;border-radius:6px;background:#fff}.doc-cards p{margin:0}.doc-cards .doc-title{font-weight:700;line-height:1.35}'
 '.doc-cards .doc-meta{font-size:.88rem;color:#475569;margin-top:.25rem}.doc-cards .doc-prov{font-size:.88rem;color:#475569;margin-top:.35rem}.doc-cards .doc-actions{font-size:.9rem;font-weight:600;margin-top:.5rem}'
 ' @media (max-width:760px){.doc-cards .doc-card{grid-template-columns:84px 1fr;gap:12px}.doc-cards .doc-thumb img{width:84px}.prose .table-wrap table{display:table;width:auto;min-width:100%;margin:0}.prose .table-wrap{margin:1.2em 0;border-radius:12px}.prose .table-wrap th,.prose .table-wrap td{min-width:8.5rem}.prose .table-wrap td:last-child{min-width:17rem}}</style>')

def smart(t):
    t = re.sub(r'(^|[\s(\[{—–/-])"', "\\1“", t); t = t.replace('"', "”")
    t = re.sub(r"(^|[\s(\[{—–/-])'", "\\1‘", t); return t.replace("'", "’")

def smart_md(md):
    parts = re.split(r"(`[^`]*`|\]\([^)]*\)|\{\{[^}]*\}\}|^\|.*$)", md, flags=re.M)
    return "".join(p if i % 2 else smart(p) for i, p in enumerate(parts))

def smart_html(h):
    """Typographic quotes in text nodes only; quote direction follows the last visible character."""
    out, last, in_code = [], " ", False
    for tok in re.split(r"(<[^>]+>)", h):
        if tok.startswith("<"):
            out.append(tok)
            if re.match(r"<(code|pre)\b", tok): in_code = True
            elif re.match(r"</(code|pre)>", tok): in_code = False
            elif re.match(r"</?(p|li|h\d|td|th|blockquote|div|tr)\b", tok): last = " "
            continue
        if in_code:
            out.append(tok); last = tok[-1:] or last; continue
        buf = []
        for ch in tok:
            if ch in "\"'":
                opening = last.isspace() or last in "([{—–/-"
                buf.append(("“" if opening else "”") if ch == '"' else ("‘" if opening else "’"))
            else:
                buf.append(ch)
            last = ch if ch not in "\"'" else buf[-1]
        out.append("".join(buf))
    return "".join(out)



def inline_em(t):
    """*Case v. Name* in FAQ text -> <em>Case v. Name</em> (visible HTML only)."""
    return re.sub(r"\*([^*\n]+)\*", r"<em>\1</em>", t)

def no_em(t):
    """Strip *...* italics markers where markup is not allowed (JSON-LD)."""
    return re.sub(r"\*([^*\n]+)\*", r"\1", t)

def build(md_path: Path, out_root: Path):
    meta, body_md = bb.parse_frontmatter(md_path.read_text(encoding="utf-8"))
    for wmsg in bb.validate_meta(meta, md_path, strict=True):
        print("WARNING:", wmsg, file=sys.stderr)
    slug = meta["slug"]; title = meta["title"]; date = meta["date"]
    description = meta["description"]
    dt = bb.datetime.strptime(date[:10], "%Y-%m-%d"); date_display = f"{dt.strftime('%b')} {dt.day}, {dt.year}"
    tags_html = '<div class="tags">' + "".join(f'<span class="{bb.tag_class(t)}">{escape(t)}</span>' for t in meta["tags"]) + "</div>"

    # :::example Title ... ::: blocks -> worked-example boxes (inner markdown rendered separately)
    examples = []
    def ex_block(m):
        examples.append((m.group(1).strip(), m.group(2)))
        return f"EXBLOCK§{len(examples) - 1}"
    body_md = re.sub(r"(?ms)^:::example (.+?)\n(.*?)\n:::[ \t]*$", ex_block, body_md)
    # NOTE: lines -> sentinel, so md_to_html keeps them as paragraphs we can re-class
    body_md = re.sub(r"(?m)^NOTE: ", "EDNOTE§ ", body_md)
    for f in meta.get("faq") or []:
        f["q"], f["a"] = smart(f["q"]), smart(f["a"])
    meta["primary_question"] = smart(meta.get("primary_question", "")); meta["answer_first"] = smart(meta.get("answer_first", ""))
    html = bb.md_to_html(body_md)
    html = smart_html(html.replace("&quot;", '"').replace("&#x27;", "'"))
    html = re.sub(r"<p>EDNOTE§ (.*?)</p>", r'<p class="editor-note">Editor’s note: \1</p>', html, flags=re.S)
    html = re.sub(r"(?<!<div class=\"table-wrap\">)\n<table>(.*?)</table>", r'\n<div class="table-wrap"><table>\1</table></div>', html, flags=re.S)
    def tbl(m):  # header row -> <thead> with scope="col"; body rows -> <tbody> (html-validate prefer-tbody, wcag/h63)
        rows = re.findall(r"<tr>.*?</tr>", m.group(1), flags=re.S)
        head = rows[0].replace("<th>", '<th scope="col">')
        return "<table>\n<thead>" + head + "</thead>\n<tbody>\n" + "\n".join(rows[1:]) + "\n</tbody>\n</table>"
    html = re.sub(r"<table>(.*?)</table>", tbl, html, flags=re.S)

    def ex_html(m):
        t, inner = examples[int(m.group(1))]
        ih = smart_html(bb.md_to_html(inner).replace("&quot;", '"').replace("&#x27;", "'"))
        return (f'<aside class="example-box" aria-label="Example: {escape(smart(t))}">\n<p class="ex-k">Example</p>\n'
                f'<p class="ex-t">{escape(smart(t))}</p>\n{ih.strip()}\n</aside>')
    html = re.sub(r"<p>EXBLOCK§(\d+)</p>", ex_html, html)
    def h3id(m):
        sid = re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", m.group(1)).lower()).strip("-")
        return f'<h3 id="{sid}">{m.group(1)}</h3>'
    html = re.sub(r"<h3>(.*?)</h3>", h3id, html)  # body subsections only; FAQ is added later
    assert "EXBLOCK§" not in html
    def mod(m):
        return MODS.MODULES[m.group(1)].rstrip()
    html = re.sub(r"<p>\{\{MODULE:([a-z0-9-]+)\}\}</p>", mod, html)
    q = escape(meta.get("primary_question", "")); a = inline_em(escape(meta.get("answer_first", "")))
    html = html.replace("<p>{{ANSWER}}</p>", f'<p class="primary-question"><strong>{q}</strong></p>\n<p class="answer-first">{a}</p>')
    faq = meta.get("faq") or []
    faq_html = '<section class="faq" aria-labelledby="frequently-asked-questions">\n<h2 id="frequently-asked-questions">Frequently Asked Questions</h2>\n' + "\n".join(
        f"<h3>{inline_em(escape(f['q']))}</h3>\n<p>{inline_em(escape(f['a']))}</p>" for f in faq) + "\n</section>"
    html = html.replace("<p>{{FAQ}}</p>", faq_html)
    person = bb.AU.resolve_author(meta)
    html = bb.AU.insert_author_note(html, bb.AU.author_note_html(person))
    assert "{{" not in html, re.findall(r"\{\{[^}]+\}\}", html)

    ld = bb.build_json_ld(meta, slug, description)
    canonical_url = meta["canonical"]
    section = meta.get("section") or "Investigations"
    ld[0]["articleSection"] = section
    ld[0]["about"] = [{"@type": "Thing", "name": n} for n in ["cell site location information", "silent SMS", "cell phone tracking", "Communications Assistance for Law Enforcement Act", "Fourth Amendment"]]
    ld[0]["mentions"] = [
        {"@type": "GovernmentOrganization", "name": "Federal Bureau of Investigation", "url": "https://www.fbi.gov/"},
        {"@type": "GovernmentOrganization", "name": "National Domestic Communications Assistance Center", "url": "https://ndcac.fbi.gov/"},
        {"@type": "GovernmentOrganization", "name": "Federal Communications Commission", "url": "https://www.fcc.gov/"},
        {"@type": "Legislation", "name": "Communications Assistance for Law Enforcement Act", "legislationIdentifier": "Pub. L. No. 103-414"},
        {"@type": "CreativeWork", "name": "Carpenter v. United States, 585 U.S. 296 (2018)", "url": "https://www.supremecourt.gov/opinions/17pdf/16-402_h315.pdf"},
        {"@type": "DigitalDocument", "name": "FBI CAST Cellular Analysis & Geo-Location Field Resource Guide (March 2019)", "url": f"{bb.SITE}/blog/{slug}/docs/fbi-cast-cellular-analysis-geolocation-field-resource-guide-2019-redacted.pdf", "encodingFormat": "application/pdf"},
        {"@type": "DigitalDocument", "name": "NDCAC Program Update, April 11, 2018", "url": "https://ndcac.fbi.gov/file-repository/ndcac-director-eab-briefing-april-2018.pdf", "encodingFormat": "application/pdf"},
        {"@type": "DigitalDocument", "name": "FCC 05-153, CALEA and Broadband Access and Services, First Report and Order", "url": f"{bb.SITE}/blog/{slug}/docs/fcc-05-153-calea-broadband-first-report-and-order-2005.pdf", "encodingFormat": "application/pdf"},
    ]
    if person is None:
        ld[0]["author"] = {"@type": "Organization", "name": "OctoProbe Staff", "url": f"{bb.SITE}/blog/"}
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": no_em(f["q"]), "acceptedAnswer": {"@type": "Answer", "text": no_em(f["a"])}} for f in faq]})
    ld_scripts = "\n".join(f'<script type="application/ld+json">\n{json.dumps(b, indent=2, ensure_ascii=False)}\n</script>' for b in ld)
    og_title = meta.get("og_title") or title
    canonical = meta["canonical"]; og = meta["og_image"]; kw = ", ".join(meta.get("keywords") or meta["tags"])
    head = f"""<title>{escape(meta.get("seo_title") or title)} · OctoProbe News</title>
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
{ld_scripts}"""
    byline_html = bb.AU.byline_html(person, meta.get("byline") or "OctoProbe Staff")
    tpl = bb.TEMPLATE.read_text(encoding="utf-8")
    out = (tpl.replace("{{HEAD_META}}", head).replace("{{TITLE}}", escape(title)).replace("{{DATE}}", escape(date))
           .replace("{{DATE_DISPLAY}}", escape(date_display)).replace("{{TAGS_HTML}}", tags_html)
           .replace("{{BYLINE_HTML}}", byline_html)
           .replace("\n      {{HERO_HTML}}", "").replace("{{HERO_HTML}}", "").replace("{{BODY}}", html))
    out = out.replace('<span class="eyebrow">Investigations</span>', f'<span class="eyebrow">{escape(section)}</span>', 1)
    out = out.replace("</h1>", "</h1>\n      <p class=\"post-dek\">" + escape(meta["dek"]) + "</p>", 1)
    out = out.replace('<link rel="stylesheet" href="/assets/css/blog.css?v=news7">',
        '<link rel="stylesheet" href="/assets/css/blog.css?v=news7">\n' + NEWS_FRAME, 1)
    out = re.sub(r'\s*<p class="post-disclaimer">.*?</p>', "", out, count=1, flags=re.S)
    # <title> uses seo_title when set
    dest = REPO / "blog" / slug / "index.html"; dest.write_text(out, encoding="utf-8"); print("built", dest.relative_to(REPO))
    return out

if __name__ == "__main__":
    build(SRC, None)
