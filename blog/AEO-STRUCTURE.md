# Recurring AEO structure (OctoProbe News)

Aligned with answer-engine optimization practice ([What is AEO](https://www.searchable.com/blog/what-is-aeo)): get **cited inside** ChatGPT, Perplexity, Gemini / AI Overviews—not only ranked in blue links.

AEO builds on SEO. Every Findings post uses this scaffold.

## Engines we optimize for

| Engine | How it retrieves | OctoProbe scaffolding |
| --- | --- | --- |
| **ChatGPT** | Training + live (Bing / GPTBot / OAI-SearchBot) | `llms.txt`, answer-first lede, FAQ JSON-LD, robots allow GPTBot / ChatGPT-User / OAI-SearchBot |
| **Perplexity** | Live retrieval, citation-first | Quotable opening + lists/tables; robots allow PerplexityBot / Perplexity-User |
| **Gemini / AI Overviews** | Google index + entity graph | Strong SEO + Organization `sameAs`; robots allow Googlebot / Google-Extended |
| **Claude** | Crawl + retrieval where enabled | robots allow ClaudeBot / anthropic-ai; same answer-first pages |

## Required page shape (every post)

1. **Answer first (40–60 words)** — front matter `answer_first:` becomes the first prose block under the H1 (before narrative). Must stand alone if a model lifts only that passage.
2. **Question-style H2/H3** — e.g. “What is an identifier graph?” not “Overview”.
3. **First sentence under each H2 answers that heading** — inverted pyramid.
4. **TL;DR / Key takeaways** — bulleted, near the top.
5. **Lists & tables** for comparisons and loops (easy extraction).
6. **No FAQ / next-steps sections** — end-user posts omit FAQ, FAQPage JSON-LD, and analyst to-dos. *(FAQ part under review: see OPEN QUESTION below.)*
7. **HowTo** (when procedural) — `howto:` front matter → HowTo JSON-LD.
8. **Entity consistency** — OctoProbe AI, Redwing Technologies LLC, product one-liner matches `llms.txt` / `ai.txt`.
9. **Internal corroboration** — link homepage FAQ, capabilities, related posts.
10. **Crawler doors open** — `robots.txt`, `llms.txt`, `/.well-known/llms.txt`, `ai.txt`.
11. **Freshness** — set `date_modified` when substance changes.
12. **Measurement note** — after ship, spot-check ChatGPT / Perplexity / Gemini for presence, share of voice, and accuracy (AEO ≠ only Analytics traffic).
13. **Featured-snippet shape** ([Google: featured snippets](https://developers.google.com/search/docs/appearance/featured-snippets)) — Google states there is no markup or opt-in (“How can I mark my page as a featured snippet? You can't”); its systems pick passages from the page, and a click scrolls the reader to that passage. The only levers Google documents are opt-outs (`nosnippet`, `data-nosnippet`, low `max-snippet`), so: **check** the page uses none of them (items 15, 18). House shape that makes a passage liftable (OctoProbe rule, not a Google spec): at least 2 H2/H3s are phrased as real user questions (end in `?`); the first `<p>` under each of those headings answers it directly in 40–60 words, answer first, no throat-clearing; procedures are `<ol>`, sets are `<ul>`, and comparisons or reconstructed sequences are a `<table>` with a header row.
14. **Publication dates** ([Google: publication dates](https://developers.google.com/search/docs/appearance/publication-dates)) — **check all of:** (a) one user-visible, labelled date near the H1 (“Published …”, plus “Updated …” only if the page was materially changed); (b) BlogPosting JSON-LD `datePublished` (and `dateModified` when set) whose calendar date equals the visible date(s); (c) values in full ISO 8601 with time and a correct UTC offset for the publish moment, DST included (e.g. `2026-10-20T21:45:00-04:00`; Google requires the date and recommends time + timezone); (d) `datePublished` ≤ `dateModified`; (e) no date later than the build time; (f) the dates describe the page’s publication/update, never the events the post covers; (g) no other prominent publish-style dates in the page chrome (event dates inside the body/timeline table are fine). Material updates set front matter `date_modified` and never change `datePublished`.
15. **Snippet / meta description** ([Google: snippets](https://developers.google.com/search/docs/appearance/snippet)) — Google builds snippets mainly from page text and uses the meta description when it describes the page better. **Check:** `<meta name="description">` exists, is unique across the site (no two pages share it), is a human-readable summary of *this* page (not a keyword list or boilerplate), and is ~150–160 characters (house length target; Google sets no limit and truncates to device width) with the key entity and finding in the first ~100 characters. Key content is visible text, not hidden behind tabs/accordions (helps “Read more” deep links); no script forces scroll position or strips the URL `#fragment` on load. Robots meta keeps `max-snippet:-1`; no page-level `nosnippet`; `data-nosnippet` appears only on elements deliberately excluded (list each one in the PR description), never on the answer-first lede, TL;DR, or question-heading answers.
16. **Sitelinks-friendly structure** ([Google: sitelinks](https://developers.google.com/search/docs/appearance/sitelinks)) — sitelinks are fully automated (no markup, no opt-in); Google derives them from site link structure. What helps, as checks: `<title>` and H1/H2 text are informative, relevant and compact (title ≤ ~60 chars, per the README checklist front-matter rules); each `<title>` is unique site-wide; one H1 and a logical H2 → H3 hierarchy with no skipped levels; the post links up to `/blog/` and home and is linked from `/blog/` (card) and at least one related page; internal anchor text is concise and describes the target (no “click here” / “here” / “read more” / bare URLs); nav is the shared template nav; no duplicated sections or near-duplicate pages. To suppress a sitelink, remove the page or `noindex` it.
17. **Favicon in Search** ([Google: favicon in search](https://developers.google.com/search/docs/appearance/favicon-in-search)) — Google uses one favicon per hostname, read from the **home page** `<head>` (`rel="icon"`, `shortcut icon`, `apple-touch-icon` or `apple-touch-icon-precomposed`). **Check:** `https://www.octoprobe.ai/` has `<link rel="icon" …>`; every linked icon returns 200 with an image content type; icons are square (1:1), at least 8×8 and preferably larger than 48×48, in a supported format (BMP, GIF, ICO, PNG, JPEG, PPM, TIFF — SVG is fine for browsers but keep an ICO/PNG alongside it); the icon is the brand mark; URLs are stable (don’t rename or move `/favicon.ico`, `/favicon-32x32.png`, `/apple-touch-icon.png`, `/favicon.svg`); `robots.txt` blocks neither the home page (Googlebot) nor the icon files (Googlebot-Image). New pages copy the icon links from `blog/_template.html` so the icon is consistent sitewide.
18. **AI features (AI Overviews / AI Mode)** ([Google: AI features](https://developers.google.com/search/docs/appearance/ai-features)) — Google: no extra requirements and no special schema or “AI text files”; to be a supporting link a page must be **indexed and eligible to show with a snippet**. **Check:** the URL is in `sitemap.xml`; not disallowed in `robots.txt` (for `*` or Googlebot) or blocked by Cloudflare/hosting; no `noindex`; the robots meta is the template default `<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">` (so no `nosnippet` and no `max-snippet:0`/low value) unless Colin explicitly asks to keep a page off AI surfaces; important content is in text (item 19 for document images); every JSON-LD block parses and its claims (headline, dates, author, Q&A if any) match visible text; the page is reachable through internal links (item 16). Answer-first structure (items 1–5, 13) is what makes a passage usable. (`llms.txt` / `ai.txt` stay for non-Google engines; Google says they are not needed for its AI features.)
19. **Screenshots aren’t quotable text** — every key document image is paired with a short HTML transcription or summary that carries the document ID in visible text, descriptive `alt` text, and a caption naming the document, its date, and its source; link the primary source wherever one exists.
20. **Timeline table** — when a post reconstructs a sequence of events, include a dated timeline/summary **table** (one row per event: date, event, source document).
21. **Personal-info inventory** — even for public / FOIA-released documents, inventory at review any visible personal info (names, phone numbers, personal emails) so the owner can make an explicit call with Google’s personal-info removal policies in mind. Redaction is the owner’s (Colin’s) decision; his standing default is **no redaction** of public / FOIA-released material.

> **OPEN QUESTION — Colin to decide (FAQ / HowTo).** Item 6 above, README checklist item 4 and the `octoprobe-investigation-blog-draft` skill (“No FAQ section and no analyst to-dos; BlogPosting JSON-LD only.”) say posts carry no FAQ and no FAQPage JSON-LD, but item 7 allows HowTo JSON-LD, the engine table above credits “FAQ JSON-LD” for ChatGPT, and recent shipped posts carry visible FAQ sections with FAQPage JSON-LD (and some HowTo) under a standing directive to keep them. Until Colin decides, this framework does **not** pick a side: don’t add or strip FAQ/HowTo on existing posts because of item 6, and flag the choice in each new post’s review. Whatever the decision, Google’s rules still apply: FAQPage/HowTo JSON-LD only when the same Q&A or steps are visible on the page (item 18).

## Google Search appearance docs (standing compliance set)

Items 13–18 codify these six (Google-stated rules vs. OctoProbe house targets are marked in each item); check every post against all of them. Each “How to verify” cell is meant to be scriptable against the built `index.html`:

| Google doc | What it requires of a post | How to verify |
| --- | --- | --- |
| [Snippets / meta description](https://developers.google.com/search/docs/appearance/snippet) | Unique, page-specific, fact-first description (~150–160 chars house target); no snippet suppression (item 15) | `meta[name=description]` present, length 140–170, unique across `blog/**/index.html`; robots meta contains `max-snippet:-1`; no `nosnippet`; every `data-nosnippet` listed in the PR |
| [Sitelinks](https://developers.google.com/search/docs/appearance/sitelinks) | Informative, compact, unique titles/headings; logical hierarchy; descriptive internal anchors (item 16) | `<title>` unique site-wide and ≤ ~60 chars; exactly one `<h1>`; no H2→H4 skips; no internal `<a>` text in {click here, here, read more, link} |
| [Featured snippets](https://developers.google.com/search/docs/appearance/featured-snippets) | Not markable; question headings + 40–60 word answer-first paragraphs + lists/tables (house shape, item 13) | ≥ 2 H2/H3 ending in `?`; first `<p>` after each is 40–60 words; ≥ 1 `<ol>`/`<ul>`; `<table>` with `<th>` when the post compares or reconstructs a sequence |
| [Favicon in search](https://developers.google.com/search/docs/appearance/favicon-in-search) | Home-page `<link rel="icon">`, square, > 48×48 preferred, supported format, stable URL, crawlable (item 17) | `index.html` has `rel="icon"`; each icon URL returns 200 + `image/*`; width = height; `robots.txt` doesn’t disallow `/` or icon paths |
| [Publication dates](https://developers.google.com/search/docs/appearance/publication-dates) | One visible labelled date = JSON-LD dates, ISO 8601 with offset, published ≤ modified, no future dates (item 14) | parse `datePublished`/`dateModified`: match `\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?[+-]\d{2}:\d{2}`; published ≤ modified ≤ now; calendar date equals visible “Published …” text |
| [AI features](https://developers.google.com/search/docs/appearance/ai-features) | Indexed + snippet-eligible; crawlable; text content; structured data matches visible text (item 18) | URL in `sitemap.xml`; no `noindex`; robots meta equals template default; every `application/ld+json` block parses; JSON-LD `headline` equals the H1 |

**Current site status (checked 2026-10-20):** live `https://www.octoprobe.ai/` serves `<link rel="icon" href="/favicon.ico" sizes="any">`, `/favicon.svg`, `/favicon-32x32.png` and `apple-touch-icon` (180×180), all 200 with image content types; `favicon.ico` holds 16/32/48/64 px square frames; `robots.txt` allows `/` and the icon paths; robots meta is the template default. So item 17 already passes at the hostname level. Gap: `blog/index.html` and most post pages link only `favicon.svg` + `favicon-32x32.png` (no `/favicon.ico` line) — not a Google-eligibility problem (Google reads only the home page) but not byte-identical to `_template.html`; align when those pages are next touched. All posts currently emit date-only `datePublished`/`dateModified` (see tooling note), so item 14(c) fails sitewide until fixed.

**Tooling note (dates):** `scripts/build-blog.py` currently formats the visible date only from a `YYYY-MM-DD` `date` and copies `date` / `date_modified` verbatim into `datePublished` / `dateModified`, so built posts emit date-only values. Until the build accepts full ISO 8601 timestamps, hand-built posts set the offset form directly; markdown-built posts need a build-script change to meet item 14.

## Front matter extras

```yaml
answer_first: >
  40–60 word standalone answer to the primary question.
primary_question: "What is an identifier graph in OSINT?"
howto:
  name: "How to build an identifier graph from a public lead"
  steps:
    - name: Seed
      text: "…"
    - name: Expand
      text: "…"
```

## Build

```bash
python3 scripts/build-blog.py
```

Injects BlogPosting (+ speakable), BreadcrumbList, optional HowTo, Organization with `sameAs`, and `<link rel="alternate" href="/llms.txt">`.
