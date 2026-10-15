# OctoProbe Findings (blog)

Local static blog for methodology writeups. Matches the landing design tokens, fonts, glass nav, and footer.

## Preview

From the landing repo root:

```bash
python3 -m http.server 8765
```

Then open:

- http://127.0.0.1:8765/blog/
- http://127.0.0.1:8765/blog/2026-10-15-identifier-graph-methodology/

Do **not** push or open a PR until Colin approves.

**Sitemap:** generated, never hand-edited. Run `python3 scripts/gen-sitemap.py` after adding or changing a post (CI runs `--check` and fails if stale).

---

## SEO / AEO / Chat-engine checklist (REQUIRED for every post)

Full recurring pattern: see [AEO-STRUCTURE.md](./AEO-STRUCTURE.md) (aligned with answer-engine optimization for ChatGPT, Perplexity, Gemini / AI Overviews).

Before writing or shipping a post, complete all of the following:

0. **`primary_question` + `answer_first` (40–60 words)** — standalone lede a model can cite without the rest of the page.
1. **Primary query + 3 secondary queries** the post should answer (e.g. “what is an identifier graph”, “OSINT investigation platform”, “breach correlation methodology”).
2. **Definitional opening** — first 2–3 sentences answer “OctoProbe is…” / the core concept before narrative. Answer engines pull this.
3. **TL;DR / Key takeaways** box near the top (bullets).
4. **No FAQ or "next steps" section** — posts are for end users; no FAQ, FAQPage JSON-LD, or internal analyst to-dos/placeholders.
5. **Front matter required fields:**
   - `title` (aim ≤ ~60 chars for the primary title)
   - `description` (~150–160 chars)
   - `date` (`YYYY-MM-DD`)
   - `tags` (list)
   - `canonical` (full https URL)
   - `slug`
   - `keywords` (list of entities/queries)
   - `og_image` / `hero` (featured image under `/assets/blog/…`)
   - `hero_alt`
   - optional: `date_modified`, `author`, `excerpt`
6. **Entity mentions** (natural, no stuffing): OctoProbe AI, Redwing Technologies, OSINT, identifier graph, breach intelligence, facial recognition OSINT, MCP OSINT as relevant.
7. **Internal links** to homepage sections (`/#capabilities`, `/#faq`, `/#access`, `/#audiences`, `/#integration`), other posts, and listing FAQ. App login only as gated CTA.
8. **Disclaimer** — public OSINT; not a consumer reporting agency / not FCRA.
9. **No passport numbers**; minimize PII; teaching examples stay fictional.
10. **Run the build** so llms.txt + sitemap stay current:

```bash
python3 scripts/build-blog.py
```

The build **fails** if `title`, `description`, `date`, or `tags` are missing; **warns** on missing `canonical`, short/long description, missing hero .

---

## Add a post

1. Create Markdown in `blog/posts/` with the front matter above (see sample `2026-10-15-identifier-graph-methodology.md`).
2. Add a featured hero under `assets/blog/` (JPG/PNG, ~16:9) and set `hero` + `og_image`.
3. Build:

```bash
python3 scripts/build-blog.py
# or one file:
python3 scripts/build-blog.py blog/posts/YYYY-MM-DD-slug.md
```

This writes `blog/<slug>/index.html`, injects BlogPosting + BreadcrumbList, regenerates `sitemap.xml`, and refreshes the Blog section in `llms.txt` and `.well-known/llms.txt`.

4. Add a card on `blog/index.html` (thumb, title, date, tags, excerpt, link). Update listing FAQ JSON-LD if you add site-wide questions.
5. Preview locally. Deploy only after approval.

## Conventions

- Fictional / example names only in teaching posts.
- Keep GA `G-6T6HW79ZP0` on blog pages (in the template).
- Styles: `/assets/css/blog.css` (Space Grotesk headings, Inter body).
- Chat / answer-engine discoverability: `llms.txt`, `/.well-known/llms.txt`, `ai.txt`; `robots.txt` allows GPTBot, OAI-SearchBot, ChatGPT-User, PerplexityBot, Google-Extended, ClaudeBot, and related agents.
- Recurring AEO structure: [AEO-STRUCTURE.md](./AEO-STRUCTURE.md).
- Twitter: `@octoprobeai`.
