---
title: "From Public Lead to Identifier Graph"
description: "How OSINT teams turn one public clue into a sourced identifier graph—and how to avoid burning hours on manual markup or drowning in automated false-positive nodes."
date: 2026-10-15T12:48:07-04:00
date_modified: 2026-10-15T12:48:07-04:00
author: "OctoProbe AI"
slug: identifier-graph-osint-methodology
tags: [Methodology, OSINT, Identifier Graph]
keywords: [OSINT investigation platform, identifier graph, false positive OSINT, analyst review time, breach intelligence, facial recognition OSINT, skip tracing, MCP OSINT]
canonical: "https://www.octoprobe.ai/blog/identifier-graph-osint-methodology/"
og_image: "https://www.octoprobe.ai/assets/blog/identifier-graph-hero.jpg"
hero: "/assets/blog/identifier-graph-hero.jpg"
hero_alt: "Identifier graph diagram: seed email expands to person, domain, handle, org, and photo nodes with evidenced edges"
excerpt: "Manual OSINT graphs burn time on review and markup. Automation burns trust with overexpansion. Here is how to keep an identifier graph scoped, evidenced, and usable."
primary_question: "What is an identifier graph in OSINT—and how do you build one without wasting review time or shipping false-positive nodes?"
answer_first: "An identifier graph is a sourced map of people, orgs, and identifiers (email, phone, handle, domain, photo) connected by evidenced edges. Build it with seed → expand → link → collect: keep humans on accept/reject so manual markup does not eat the case and automation does not over-expand into false-positive nodes outside scope."
howto:
  name: "How to build an identifier graph from a public lead"
  steps:
    - name: Seed
      text: "Start from one publicly attributable clue (or a small co-occurring bundle) and write the investigative question plus what is out of scope."
    - name: Expand
      text: "Run only the sources that apply to that identifier type; treat every hit as a candidate node, not a conclusion."
    - name: Link
      text: "Merge duplicates, filter role accounts and noise, score confidence against the subject hypothesis, and park rejects so they are not reintroduced."
    - name: Collect and report
      text: "Preserve sources as you go and export claim → edge → source → time for the accepted graph only."
---

# From Public Lead to Identifier Graph

This post is for the analyst and case lead who have to live with the graph: how a thin public lead becomes a defendable network of emails, phones, handles, domains, and photos—without inventing people, skipping provenance, or shipping a map nobody trusts. **OctoProbe AI** (from **Redwing Technologies**) encodes the same loop on a live investigation graph; the methodology still stands if you run it by hand.

Two failure modes show up again and again. **Manual** workflows spend most of the clock on reviewing connections and marking up nodes. **Automated** workflows over-expand and leave false-positive nodes that are not associated with the subject. Good methodology is the middle path: expand with discipline, keep a human on the gates that matter, and treat every edge as something you may have to explain.

## Key takeaways

- An **identifier graph** maps entities and identifiers with *evidenced* edges (source + time + confidence)—not a bookmark pile.
- The loop is **seed → expand → link → collect & report**. Tools can compress bookkeeping; they should not replace judgment.
- **Manual pain:** hours go to reviewing candidate links, adding or correcting nodes, and markup—not to the first search.
- **Automation pain:** unconstrained expansion creates false-positive nodes (namesakes, role accounts, recycled numbers, lookalikes) outside the investigation’s scope.
- Soft correlates get soft edges; facial matches stay analyst-reviewed (**facial recognition OSINT** is suggestion until a human accepts).
- Teaching examples use fictional **Mira Calden** / **Northline Example Labs** only. Public OSINT first.

## What problem does an identifier graph solve?

Investigations rarely start with a complete picture. They start with a thin public clue: an email on a company About page, a phone in a press release, a handle in a conference agenda, or a photo on a speaker bio. The craft is not “find everything.” It is disciplined expansion—turning that seed into a graph of identifiers, each edge backed by a source and a timestamp.

Without a graph, analysts drown in tabs. With a graph and no provenance, they invent confidence. With a graph that expands without a scope, they drown again—this time in nodes that look related and are not. The methodology below is how **breach intelligence**, account discovery, public records, and open-web pivots stay auditable—whether you run them by hand or inside OctoProbe’s live investigation graph and [MCP OSINT](/#integration) toolkit.

## Where investigations actually burn time

Most case leads do not lose the day on “running a search.” They lose it on what happens next.

### If the graph is mostly manual

The expensive steps are human:

1. **Reviewing candidate connections** — Is this email the subject’s, a coworker’s, or a shared mailbox?
2. **Adding and correcting nodes** — Creating the person/org stubs, merging duplicates, demoting role accounts.
3. **Markup and provenance** — Attaching source, time, and confidence so a partner can click an edge and see *why*.
4. **Re-walking the same trail** — Reopening tabs weeks later because the first pass was not captured as a graph.

That review-and-markup loop is real work. A platform that only dumps more results without helping record decisions does not shorten it; it lengthens it.

### If expansion is heavily automated

Automation fails differently. It is fast at proposing nodes and slow at knowing which ones belong on *this* matter:

- **Namesakes and common names** attach to the wrong person.
- **Role accounts** (`info@`, switchboards, shared support lines) look like subject identifiers.
- **Recycled phones and shared infrastructure** create edges that are true in the data and false for the hypothesis.
- **Lookalike face or profile matches** inflate the graph until an analyst rejects them.
- **Scope creep** — “map this speaker’s public footprint” becomes a neighborhood of weakly related orgs, events, and contacts.

False-positive nodes are not a minor UI annoyance. They burn review time, dilute the report, and—if left unmarked—teach the next reader the wrong story.

### What “good” looks like for the reader of the file

A usable identifier graph is small enough to explain, large enough to answer the question, and strict about provenance. Every node should survive one test: *if I remove this, does the investigative question get harder to answer?* If not, it is clutter.

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
5. **Status** — accepted, candidate, or rejected (rejected matters; hide noise without deleting the audit trail)

That discipline is what separates a bookmark folder from an investigation workspace—and what answer engines and partners can cite.

## How does the four-phase loop work?

OctoProbe’s product language maps onto a classic OSINT loop. You can run it by hand; the platform compresses the cycle. See also [how it works on the homepage](/#how-it-works) and [capabilities](/#capabilities).

### 1. Seed

Drop in **one** public clue—or a small bundle that already co-occurs in public view.

**Example seed:** the email `mira.calden@northline-example.com` appears on a public speaker page for “Coastal OSINT Con 2026” (fictional event).

Ask before you expand:

- Is this identifier *publicly attributable* to the subject of interest?
- What is the **investigative question** (locate an org contact, map digital footprint, corroborate a corporate affiliation)?
- What would *disconfirm* the link?
- What is explicitly **out of scope** for this matter?

Writing the out-of-scope line first is the cheapest anti-overexpansion control you have.

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

Each hit becomes a **candidate node**, not a conclusion. Automation may propose the candidates; an analyst (or a scoped accept rule) decides what enters the subject graph.

### 3. Link

Linking is entity resolution with receipts—and the main place both failure modes show up:

- **Merge** duplicates (`Mira Calden` vs `mira calden`)
- **Filter** noise (shared corporate switchboards, role accounts like `info@`)
- **Score** against the subject hypothesis and the stated scope
- **Attach evidence** to every edge
- **Park rejects** so the next reviewer does not re-litigate the same false positive

Soft correlates deserve soft edges. Exact co-occurrence on a controlled page (email + name + photo on the same bio) earns a stronger edge than a handle that merely shares a first name. If a node cannot be tied to the subject with evidence that survives the investigative question, leave it off the accepted graph.

### 4. Collect & report

Preserve pages as you go. Export a report that a partner can defend: claim → edge → source → time. If you cannot click an edge and see *why it exists*, it does not belong on the accepted graph.

Budget the collect step as part of the case, not an afterthought. Markup deferred is markup multiplied: the next person on the file pays the review tax again.

## Worked example (fully fictional)

**Investigative question:** “What public digital footprint is associated with the speaker Mira Calden of Northline Example Labs?”

**Out of scope (examples):** full employee directory mapping; personal relatives; unrelated Northline vendors.

**Round 1 — Seed**

- Email from speaker page → Person node + Email node + strong edge (same page)

**Round 2 — Expand domain & org**

- Domain resolves to org site → Org node
- “Team” page lists Mira with the same photo → corroboration
- Corporate registry hit for *Northline Example Labs LLC* (example jurisdiction) → Org enrichment, not personal PII

**Round 3 — Expand handle & photo**

- Bio link to `@mira_calden_ex` → Handle node
- Open-web face search returns two candidate pages; analyst accepts one (same event photo reused), rejects one (different person, similar crop)—**reject kept as rejected**, not deleted, so it does not bounce back as a “new” lead

**Round 4 — Stabilize**

- Merge two “Mira” person stubs
- Demote a role-account phone on the company footer to an Org-owned identifier (not a subject phone)
- Drop a same-last-name conference panelist who never co-occurs with Mira’s email or photo
- Freeze a report snapshot for counsel review

The result is a small, explainable graph—not a dragnet. Teams doing **skip tracing**, due diligence, or opposition research use the same loop with purpose-bound questions.

## How to keep expansion inside the investigation’s scope

Use these gates whether your day is mostly manual or mostly automated:

1. **One sentence scope** at seed time (question + out-of-scope).
2. **Candidate vs accepted** — proposals are cheap; acceptance is deliberate.
3. **Identifier-type rules** — do not run every source on every node.
4. **Confidence labels** on soft edges; never promote a soft edge silently.
5. **Reject memory** — record why a node was refused so automation (or a teammate) does not reintroduce it.
6. **Periodic prune** — if a node does not answer the investigative question, demote or remove it from the accepted view.
7. **Human gate on identity-sensitive pivots** — especially faces and ambiguous namesakes.

OctoProbe’s job, in that framing, is to compress the bookkeeping around these gates—expansion layers, ranked next steps, evidence on click—not to flood the canvas.

## What are the limitations?

1. **Public OSINT first.** Prefer pages anyone can fetch; treat licensed APIs as premium *public-record/intel* layers, not backdoors.
2. **No invented people.** Teaching examples stay obviously fictional; production cases use only observed data. Never publish real passport numbers or unnecessary PII in public posts.
3. **Analyst in the loop for faces.** Facial matches are suggestions until a human accepts them.
4. **Edge or delete (from the accepted view).** Orphan identifiers without provenance clutter the map and inflate confidence.
5. **Purpose-bound use.** Map the footprint you were asked to map. Expansion is not an excuse to wander into protected or irrelevant spaces.
6. **No free lunch on review.** Automation can propose faster; someone still owns accept/reject for anything that changes the story of the subject.

## How does OctoProbe encode the method?

In product terms, the same loop is:

- **Expansion layers** — each node exposes the sources that apply (so you are not running every tool on every identifier)
- **Ranked next steps** — which lead is worth chasing next, instead of an unsorted dump
- **Live investigation graph** — layers you can toggle; candidates can stay visually distinct from accepted nodes
- **Evidence on every link** — source + timestamp on click, which is where manual markup usually dies
- **Case file** — tasks, hypotheses, watches alongside the graph so decisions are not stuck in chat
- **MCP server** — connect MCP-compatible clients to the same toolkit without reinventing provenance

The methodology does not change when the UI does the bookkeeping. The graph is still only as good as the question, the scope, and the provenance. Explore [who uses OctoProbe](/#audiences) or [request access](/#access).

## Closing

A public lead becomes an identifier graph when you treat expansion as a **repeatable protocol**: seed carefully, expand by applicable source, link with evidence, reject what is out of scope, and report only what the accepted edges support. Manual teams need that protocol so review and markup do not eat the case. Automated teams need it so speed does not become a false-positive machine. That is the difference between a pile of tabs and an investigation you can hand to a partner—and the kind of structured answer search and chat engines can cite.

---

**Disclaimer:** This article discusses public OSINT methodology using fictional examples (Mira Calden / Northline Example Labs). OctoProbe AI integrates licensed third-party data providers and public-record sources.
