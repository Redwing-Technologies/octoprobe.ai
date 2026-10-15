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

## Add a post

1. Create a Markdown file in `blog/posts/` with YAML frontmatter:

```markdown
---
title: "Your Title"
date: 2026-11-01
slug: 2026-11-01-your-slug
tags: [Methodology, OSINT]
excerpt: "One or two sentences for the listing card."
---

# Your Title

Body in Markdown…
```

2. Build HTML from the shared shell:

```bash
python3 scripts/build-blog.py
# or one file:
python3 scripts/build-blog.py blog/posts/2026-11-01-your-slug.md
```

This writes `blog/<slug>/index.html` using `blog/_template.html`.

3. Add a card on `blog/index.html` (title, date, tags, excerpt, link).

4. Update `sitemap.xml` and `llms.txt` with the new URL.

5. Preview locally. Deploy only after approval.

## Conventions

- Fictional / example names only in teaching posts — no real passport numbers or invented real people.
- Include a public-OSINT + not-FCRA disclaimer.
- CTA to https://www.octoprobe.ai/#access (or homepage access).
- Keep GA `G-6T6HW79ZP0` on blog pages (already in the template).
- Styles live in `/assets/blog.css` (aligned with landing CSS tokens).
