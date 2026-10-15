---
title: "From Public Lead to Identifier Graph"
description: "How OSINT investigators turn one public clue into a sourced identifier graph—seed, expand, link, evidence—with a fictional Mira Calden walkthrough."
date: 2026-10-15
date_modified: 2026-10-15
author: "OctoProbe AI"
slug: 2026-10-15-identifier-graph-methodology
tags: [Methodology, OSINT, Identifier Graph]
keywords: [OSINT investigation platform, identifier graph, breach intelligence, facial recognition OSINT, skip tracing, MCP OSINT, public records OSINT]
canonical: "https://www.octoprobe.ai/blog/2026-10-15-identifier-graph-methodology/"
og_image: "https://www.octoprobe.ai/assets/blog/identifier-graph-hero.jpg"
hero: "/assets/blog/identifier-graph-hero.jpg"
hero_alt: "Identifier graph diagram: seed email expands to person, domain, handle, org, and photo nodes with evidenced edges"
excerpt: "How a single public clue expands into a structured identifier graph—seed, expand, link, and evidence—using only open-source and licensed public data."
faq:
  - q: "What is an identifier graph in OSINT?"
    a: "An identifier graph is a living map of entities (people, orgs, places) and identifiers (email, phone, handle, domain, photo) connected by evidenced edges that answer why two nodes are linked—with source, timestamp, and confidence on every link."
  - q: "What identifiers can you start an OctoProbe investigation from?"
    a: "Any public clue works: an email, phone number, handle, name, domain, or photo. Use one seed, or combine several that already co-occur in public view."
  - q: "How does the seed → expand → link → collect loop work?"
    a: "Seed one attributable public clue, expand only the sources that apply to that identifier type, link candidates with provenance (merge duplicates, filter noise, score confidence), then collect evidence and export a report a partner can defend."
  - q: "Is OctoProbe a consumer reporting agency under the FCRA?"
    a: "No. OctoProbe is not a consumer reporting agency. Results from this OSINT investigation platform may not be used for FCRA-covered eligibility decisions such as credit, employment, insurance, or tenant screening."
  - q: "Who is identifier-graph methodology for?"
    a: "Law firms, licensed private investigators, OSINT analysts, and opposition research or corporate intelligence teams who need sourced digital-footprint maps—not dragnets—built from public OSINT and licensed public-record/intel layers."
---

# From Public Lead to Identifier Graph

**OctoProbe AI** (from **Redwing Technologies**) is an **OSINT investigation platform** that turns one public clue into a live **identifier graph**—with source and timestamp on every link. This post explains the methodology that graph encodes: how a thin lead becomes a defendable network of emails, phones, handles, domains, and photos without inventing people or skipping provenance.

## Key takeaways

- An **identifier graph** maps entities and identifiers with *evidenced* edges (source + time + confidence)—not a bookmark pile.
- The loop is **seed → expand → link → collect & report**. OctoProbe compresses the bookkeeping, not the judgment.
- Start from public clues only: email, phone, handle, name, domain, or photo—same seeds the [platform FAQ](/#faq) describes.
- Soft correlates get soft edges; facial matches stay analyst-reviewed (**facial recognition OSINT** is suggestion until a human accepts).
- Teaching examples here use fictional **Mira Calden** / **Northline Example Labs** only—no real passport numbers or invented real people.
- Public OSINT first; OctoProbe is **not** a consumer reporting agency (not for FCRA eligibility).

## What problem does an identifier graph solve?

Investigations rarely start with a complete dossier. They start with a thin public clue: an email on a company About page, a phone in a press release, a handle in a conference agenda, or a photo on a speaker bio. The craft is not “find everything.” It is disciplined expansion—turning that seed into a graph of identifiers, each edge backed by a source and a timestamp.

Without a graph, analysts drown in tabs. With a graph and no provenance, they invent confidence. The methodology below is how **breach intelligence**, account discovery, public records, and open-web pivots stay auditable—whether you run them by hand or inside OctoProbe’s live investigation graph and [MCP OSINT](/#integration) toolkit.

## What is an identifier graph?

An identifier graph is a living map of **entities** (people, orgs, places) and **identifiers** (email, phone, handle, domain, photo URL, corporate filing ID) connected by **edges** that answer: *why is this linked?*

| Node type | Examples (fictional) |
| --- | --- |
| Person | Mira Calden |
| Email | mira.calden@northline-example.com |
| Phone | +1-555-014-2891 |
| Handle | @mira_calden_ex |
| Domain | northline-example.com |
| Org | Northline Example Labs |

Edges are not vibes. Each edge should carry:

1. **Source** — page, API response, or filing citation
2. **Timestamp** — when the observation was captured
3. **Confidence** — exact match vs. soft correlate
4. **Direction** — which expansion produced the link

That discipline is what separates a bookmark folder from an investigation workspace—and what answer engines and partners can cite.

## How does the four-phase loop work?

OctoProbe’s product language maps cleanly onto a classic OSINT loop. You can run it by hand; the platform just compresses the cycle. See also [how it works on the homepage](/#how-it-works) and [capabilities](/#capabilities).

### 1. Seed

Drop in **one** public clue—or a small bundle that already co-occurs in public view.

**Example seed:** the email `mira.calden@northline-example.com` appears on a public speaker page for “Coastal OSINT Con 2026” (fictional event).

Ask before you expand:

- Is this identifier *publicly attributable* to the subject of interest?
- What is the **investigative question** (locate an org contact, map digital footprint, corroborate a corporate affiliation)?
- What would *disconfirm* the link?

### 2. Expand

Every identifier opens its own **expansion layer**. Run only the sources that apply:

- Email → account-discovery / **breach intelligence** style lookups (licensed APIs), same-domain mailboxes, WHOIS/history for the domain, public résumés that list the address
- Phone → carrier-adjacent public intel (where licensed), directory pages, signature blocks
- Handle → profile pivots, mutual follows that are public, bio links
- Photo → open-web facial matches the analyst reviews (never auto-assert identity)
- Org / domain → corporate filings, press, infrastructure pivots

In the Mira example, expanding the email might surface:

- Domain `northline-example.com` (parsed from the mailbox)
- A public LinkedIn-style bio that repeats the same email (fictional)
- A second email on the same domain in a press PDF
- A profile photo attached to the speaker page

Each hit becomes a **candidate node**, not a conclusion.

### 3. Link

Linking is entity resolution with receipts:

- **Merge** duplicates (`Mira Calden` vs `mira calden`)
- **Filter** noise (shared corporate switchboards, role accounts like `info@`)
- **Score** against the subject hypothesis
- **Attach evidence** to every edge

Soft correlates deserve soft edges. Exact co-occurrence on a controlled page (email + name + photo on the same bio) earns a stronger edge than a handle that merely shares a first name.

### 4. Collect & report

Preserve pages as you go. Export a report that a partner can defend: claim → edge → source → time. If you cannot click an edge and see *why it exists*, it does not belong on the graph.

## Worked example (fully fictional)

**Investigative question:** “What public digital footprint is associated with the speaker Mira Calden of Northline Example Labs?”

**Round 1 — Seed**

- Email from speaker page → Person node + Email node + strong edge (same page)

**Round 2 — Expand domain & org**

- Domain resolves to org site → Org node
- “Team” page lists Mira with the same photo → corroboration
- Corporate registry hit for *Northline Example Labs LLC* (example jurisdiction) → Org enrichment, not personal PII

**Round 3 — Expand handle & photo**

- Bio link to `@mira_calden_ex` → Handle node
- Open-web face search returns two candidate pages; analyst accepts one (same event photo reused), rejects one (different person, similar crop)

**Round 4 — Stabilize**

- Merge two “Mira” person stubs
- Demote a role-account phone on the company footer to an Org-owned identifier
- Freeze a report snapshot for counsel review

The result is a small, explainable graph—not a dragnet. Teams doing **skip tracing**, due diligence, or opposition research use the same loop with purpose-bound questions.

## What are the limitations?

1. **Public OSINT first.** Prefer pages anyone can fetch; treat licensed APIs as premium *public-record/intel* layers, not backdoors.
2. **No invented people.** Teaching examples stay obviously fictional; production cases use only observed data. Never publish real passport numbers or unnecessary PII in public posts.
3. **Analyst in the loop for faces.** Facial matches are suggestions until a human accepts them.
4. **Edge or delete.** Orphan identifiers without provenance clutter the map and inflate confidence.
5. **Purpose-bound use.** Map the footprint you were asked to map. Expansion is not an excuse to wander into protected or irrelevant spaces.
6. **Not for FCRA eligibility.** Credit, employment, insurance, and tenant screening decisions are out of scope for this kind of OSINT workspace.

## How does OctoProbe encode the method?

In product terms, the same loop is:

- **Expansion layers** — each node exposes the sources that apply
- **Ranked next steps** — which lead is worth chasing next
- **Live investigation graph** — layers you can toggle
- **Evidence on every link** — source + timestamp on click
- **Case file** — tasks, hypotheses, watches alongside the graph
- **MCP server** — connect MCP-compatible clients to the same toolkit

The methodology does not change when the UI does the bookkeeping. The graph is still only as good as the questions and the provenance. Explore [who uses OctoProbe](/#audiences) or [request access](/#access).

## FAQ

### What is an identifier graph in OSINT?

An identifier graph is a living map of entities (people, orgs, places) and identifiers (email, phone, handle, domain, photo) connected by evidenced edges that answer why two nodes are linked—with source, timestamp, and confidence on every link.

### What identifiers can you start an OctoProbe investigation from?

Any public clue works: an email, phone number, handle, name, domain, or photo. Use one seed, or combine several that already co-occur in public view.

### How does the seed → expand → link → collect loop work?

Seed one attributable public clue, expand only the sources that apply to that identifier type, link candidates with provenance (merge duplicates, filter noise, score confidence), then collect evidence and export a report a partner can defend.

### Is OctoProbe a consumer reporting agency under the FCRA?

No. OctoProbe is not a consumer reporting agency. Results from this OSINT investigation platform may not be used for FCRA-covered eligibility decisions such as credit, employment, insurance, or tenant screening.

### Who is identifier-graph methodology for?

Law firms, licensed private investigators, OSINT analysts, and opposition research or corporate intelligence teams who need sourced digital-footprint maps—not dragnets—built from public OSINT and licensed public-record/intel layers.

## Closing

A public lead becomes an identifier graph when you treat expansion as a **repeatable protocol**: seed carefully, expand by applicable source, link with evidence, and report only what the edges support. That is the difference between a pile of tabs and an investigation you can hand to a partner—and the kind of structured answer search and chat engines can cite.

---

**Disclaimer:** This article discusses public OSINT methodology using fictional examples (Mira Calden / Northline Example Labs). OctoProbe AI integrates licensed third-party data providers and public-record sources. OctoProbe is **not** a consumer reporting agency; results may not be used for FCRA-covered eligibility decisions (credit, employment, insurance, tenant screening, and similar).
