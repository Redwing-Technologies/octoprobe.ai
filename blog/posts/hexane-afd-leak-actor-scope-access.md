---
title: "Hexane’s AfD Dump: Assessing the Actor, the Scope, and the Access"
description: "Three-part assessment of Hexane’s AfD dump: a privacy-focused cyber actor, a 281 GB archive of ~421,000 emails, and how deep the system access went."
date: 2026-10-21
date_modified: 2026-10-21
slug: hexane-afd-leak-actor-scope-access
canonical: https://www.octoprobe.ai/blog/hexane-afd-leak-actor-scope-access/
author: Colin Aamot
tags: [Investigation, OSINT, Leak, Germany]
keywords: [Hexane, hexane.cc, AfD, Alternative für Deutschland, data breach, BitTorrent, DDoSecrets, Cloudflare, cock.li, Monero, mbox, DKIM, hacktivism, OSINT, identifier graph, OctoProbe]
og_image: /blog/hexane-afd-leak-actor-scope-access/assets/og-cover.png
hero: /blog/hexane-afd-leak-actor-scope-access/assets/cover.png
hero_alt: "OctoProbe cover — Hexane’s AfD Dump: Actor, Scope, Access"
status: LOCAL DRAFT — DO NOT PUBLISH
---

# Hexane’s AfD Dump: Assessing the Actor, the Scope, and the Access

**LOCAL REVIEW DRAFT. DO NOT PUBLISH.** Hand-built HTML is canonical: `wt/blog/hexane-afd-leak-actor-scope-access/index.html`.

## Primary question
What should investigators make of the Hexane AfD dump — the actor who published it, the archive’s scope, and the access that made it possible?

## Answer-first (assessment)
Treat it as a three-part assessment. **The actor** is Hexane: a sophisticated, privacy-focused cyber operator that stood up a purpose-built, anonymized, one-time-dump stack — Cloudflare-fronted domain, cock.li contact plus PGP, Monero-only donations, BitTorrent and a DDoSecrets mirror — engineered to resist attribution and takedown. **The scope** is a 281 GB primary-source archive (MANIFEST: 301,876,945,879 bytes / 102,985 files; Hexane briefing ~421,000 messages / 10 mailboxes). **The access** looks deeper than a few dusty inboxes: “outdated website” entry, several web servers plus at least one mail server (heise), live campaign mail contradicting AfD’s “mostly inactive” claim, plus SQL/WordPress dumps and a credentials-and-keys trove.

## Pillars
1. **The Actor** — privacy-focused cyber actor; tradecraft; one-time-dump infra; self-presentation; hacktivism frame (Mirko Ross / Asvin).
2. **Scope of the Leak** — 281 GB directory structure (on-page viz from MANIFEST); mailboxes; for-journalists pack; verification via DKIM/torrent.
3. **Access** — outdated website; multi-server source; AfD claim vs early-September/live campaign data; credentials depth.

## Headline options (for Colin)
1. Hexane’s AfD Dump: Assessing the Actor, the Scope, and the Access *(current H1)*
2. Anatomy of a One-Time Dump: How Hexane Built Privacy Infrastructure Around a 281 GB AfD Archive
3. 281 GB, Ten Mailboxes, One Anonymous Actor: Assessing the Hexane AfD Leak

See built HTML for full prose, figures, tables, FAQ, JSON-LD.
