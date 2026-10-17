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
6. **No FAQ / next-steps sections** — end-user posts omit FAQ, FAQPage JSON-LD, and analyst to-dos.
7. **HowTo** (when procedural) — `howto:` front matter → HowTo JSON-LD.
8. **Entity consistency** — OctoProbe AI, Redwing Technologies LLC, product one-liner matches `llms.txt` / `ai.txt`.
9. **Internal corroboration** — link homepage FAQ, capabilities, related posts.
10. **Crawler doors open** — `robots.txt`, `llms.txt`, `/.well-known/llms.txt`, `ai.txt`.
11. **Freshness** — set `date_modified` when substance changes.
12. **Measurement note** — after ship, spot-check ChatGPT / Perplexity / Gemini for presence, share of voice, and accuracy (AEO ≠ only Analytics traffic).

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
