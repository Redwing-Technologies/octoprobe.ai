#!/usr/bin/env python3
"""Build the Secret Service FOIA x OSINT guide (Public Journalism Guide) from markdown.
Same pattern as scripts/build-adtech-post.py (reuses scripts/build-blog.py helpers,
scripts/authors.py and blog/_template.html), with:
  * NOTE: paragraphs -> <p class="editor-note">Editor’s note: …</p>
  * {{MODULE:name}} -> figure modules from scripts/usss-modules.py (post-local usss.css / usss.js)
  * {{ANSWER}}, {{FAQ}} (+ FAQPage JSON-LD), {{AUTHOR_NOTE}} (default author Colin Aamot, Person JSON-LD)
  * og_title front-matter field for og:/twitter: titles; `section` sets the crumb eyebrow and
    NewsArticle.articleSection; HowTo and Dataset JSON-LD for the seven steps and the hostname table
Source: blog/posts/secret-service-foia-sharepoint-browser-history-osint-guide.md
Usage (repo root):  python3 scripts/build-usss-post.py
Writes blog/<slug>/index.html and blog/<slug>/assets/hostfinder-data.json; other assets/ and docs/
files are committed as-is. No third-party packages.
"""
import importlib.util, json, re, sys, shutil
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "blog" / "posts" / "secret-service-foia-sharepoint-browser-history-osint-guide.md"
_ms = importlib.util.spec_from_file_location("usss_modules", REPO / "scripts" / "usss-modules.py")
MODS = importlib.util.module_from_spec(_ms); _ms.loader.exec_module(MODS)
spec = importlib.util.spec_from_file_location("bb", REPO / "scripts" / "build-blog.py")
bb = importlib.util.module_from_spec(spec); spec.loader.exec_module(bb)

NEWS_FRAME = ('<style id="news-frame">.post-dek{max-width:46rem;margin:.6rem 0 0;font-size:1.15rem;line-height:1.5;color:#475569}'
 '.post-hero .byline{margin:1rem 0 0;font-weight:600;color:#334155;font-size:.98rem}.post-hero .byline a{color:inherit;text-decoration:underline;text-decoration-color:rgba(51,65,85,.35);text-underline-offset:3px}.post-hero .byline a:hover{color:var(--blue)}.table-wrap{overflow-x:auto}'
 '.table-wrap table{border-collapse:collapse;width:100%;font-size:.92rem}.table-wrap th,.table-wrap td{border:1px solid #e2e8f0;padding:.45rem .6rem;vertical-align:top;text-align:left}'
 '.related-reading{border-top:1px solid #e2e8f0;margin-top:2rem;padding-top:.5rem}.related-reading h2{margin-top:1rem}.related-reading li{margin:.4rem 0}'
 '.prose .faq h3{font-size:1.02rem;margin-top:1.2em}.prose .faq p{margin-top:.35em}</style>')

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

HOWTO = [
    ("Identify the agency’s Microsoft 365 tenant and SharePoint hosts", "Confirm the tenant with public DNS, Microsoft’s OpenID Connect discovery metadata and certificate or passive-DNS logs. Stay passive.", "step-1-identify-the-agency-s-microsoft-365-tenant-and-sharepoint-hosts"),
    ("Identify the custodian by name or title", "Use leadership pages, press releases, testimony and FOIA logs to get the person’s full name, title and dates in the job. No email address is needed.", "step-2-identify-the-custodian-by-name-or-title"),
    ("Choose the record types", "Pick browser history and web-proxy logs, SharePoint documents created or edited, Teams messages, channel files, chat files, card statements or a sitemap, and name the system that holds each.", "step-3-choose-the-record-types"),
    ("Write the request", "One sentence per item with a date range, custodian and system; state format, fee category, any fee waiver and, where it applies, expedited processing.", "step-4-write-the-request"),
    ("Anticipate the agency’s answers", "Plan for exemptions (b)(6), (b)(7)(C) and (b)(7)(E), the no-duty-to-create-records objection to lists, and the not-an-agency-record argument.", "step-5-anticipate-the-agency-s-answers"),
    ("Track and follow up", "Log the receipt date and number, check the agency’s FOIA log, file log requests before disposal, and consider OGIS mediation for disputes.", "step-6-track-and-follow-up"),
    ("Use what comes back", "Read site names, hosts, hubs and redaction patterns in the release and turn them into the next requests.", "step-7-use-what-comes-back"),
]


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
    q = escape(meta.get("primary_question", "")); a = escape(meta.get("answer_first", ""))
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
    ld[0]["about"] = [{"@type": "Thing", "name": n} for n in ["Freedom of Information Act", "open-source intelligence", "Microsoft SharePoint", "Microsoft Teams", "agency records"]]
    ld[0]["mentions"] = [
        {"@type": "GovernmentOrganization", "name": "United States Secret Service", "url": "https://www.secretservice.gov/"},
        {"@type": "Person", "name": "Ronald L. Rowe Jr.", "jobTitle": "Deputy Director, U.S. Secret Service (2023–2025)",
         "sameAs": ["https://www.secretservice.gov/newsroom/releases/2023/04/secret-service-welcomes-veteran-special-agent-ronald-rowe-deputy-director"]},
        {"@type": "Legislation", "name": "Freedom of Information Act, 5 U.S.C. § 552", "url": "https://www.law.cornell.edu/uscode/text/5/552"},
        {"@type": "Organization", "name": "Microsoft"},
    ]
    ld.append({"@context": "https://schema.org", "@type": "HowTo", "name": "How to FOIA an official’s browser history, SharePoint files and Teams messages",
        "description": description,
        "supply": [{"@type": "HowToSupply", "name": "A FOIA request letter or portal submission"}],
        "tool": [{"@type": "HowToTool", "name": "Public DNS-over-HTTPS resolver"}, {"@type": "HowToTool", "name": "Microsoft OpenID Connect discovery metadata"}, {"@type": "HowToTool", "name": "Certificate-transparency search (crt.sh)"}],
        "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t, "url": f"{canonical_url}#{a}"} for i, (n, t, a) in enumerate(HOWTO)]})
    ld.append({"@context": "https://schema.org", "@type": "Dataset", "name": "Federal FOIA components and SharePoint hostnames",
        "description": "431 FOIA components with SharePoint base, OneDrive, sub-agency, office and admin hostnames, with a passive DNS check of every hostname on Oct. 20, 2026.",
        "creator": {"@type": "Organization", "name": "Redwing Technologies"}, "dateModified": "2026-10-20", "isAccessibleForFree": True,
        "url": f"{canonical_url}#fig-hostfinder",
        "distribution": [
            {"@type": "DataDownload", "encodingFormat": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "contentUrl": f"{bb.SITE}/blog/{slug}/docs/federal-foia-sharepoint-hostnames.xlsx"},
            {"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": f"{bb.SITE}/blog/{slug}/docs/federal-foia-sharepoint-hostnames.csv"}]})
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
    out = out.replace('<link rel="stylesheet" href="/assets/css/blog.css?v=news6">',
        '<link rel="stylesheet" href="/assets/css/blog.css?v=news6">\n' + NEWS_FRAME +
        f'\n<link rel="stylesheet" href="/blog/{slug}/assets/usss.css?v=4">', 1)
    out = re.sub(r'\s*<p class="post-disclaimer">.*?</p>', "", out, count=1, flags=re.S)
    out = out.replace('<script src="/assets/js/blog-toc.js?v=toc7" defer></script>',
        f'<script src="/assets/js/blog-toc.js?v=toc7" defer></script>\n<script src="/blog/{slug}/assets/usss.js?v=3" defer></script>', 1)
    # <title> uses seo_title when set
    dest = REPO / "blog" / slug / "index.html"; dest.write_text(out, encoding="utf-8"); print("built", dest.relative_to(REPO))
    return out

if __name__ == "__main__":
    build(SRC, None)
