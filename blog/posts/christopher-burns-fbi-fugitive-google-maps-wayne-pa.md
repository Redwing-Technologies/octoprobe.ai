---
title: "Christopher W. Burns (FBI Most Wanted Fraudsters): Public Google Maps Activity Dated After His Last Sighting, Wayne, PA Area"
date: 2026-10-15
slug: christopher-burns-fbi-fugitive-google-maps-wayne-pa
tags: [Investigation, OSINT, Fugitives, Identifier Graph]
excerpt: "A Google Maps account allegedly attributed to FBI Most Wanted Fraudster Christopher W. Burns shows activity in Wayne and Wynnewood, PA (~2021 and ~2023), after his last known sighting on September 24, 2020."
cover: assets/cover.png
status: DRAFT (do not publish until approved)
---

# Christopher W. Burns: Public Google Maps Activity Dated After His Last Sighting, Wayne, PA Area

![Cover: Christopher W. Burns, FBI Most Wanted Fraudsters, last seen September 24, 2020](assets/cover.png)

**Summary:** A Google Maps contributor account allegedly attributed to Christopher W. Burns shows activity in the Wayne, PA area after the FBI's last known sighting. The FBI says Burns "has not been seen since he left his home on September 24, 2020." The "Chris Burns" profile, which OctoProbe's identifier graph ties to Burns's name variants and personal email, carries a review at PrimoHoagies in Wayne dated "5 years ago" (~2021) and a rating at Target in Wynnewood dated "3 years ago" (~2023). Both sites sit on the Lancaster Avenue / Main Line corridor, roughly 7 miles apart, in the same area as Burns's FBI-listed birthplace and the Wayne addresses and employer in his identifier graph. Assessment: moderate-confidence indicator of post-flight presence on the Philadelphia Main Line, strongest for the ~2023 data point.

## Key finding

- **Timeline:** FBI last sighting September 24, 2020 (Georgia). Maps activity ~2021 (Wayne) and ~2023 (Wynnewood). Both fall after the disappearance.
- **Geography:** PrimoHoagies (Wayne) and Target (Wynnewood) are about 7 miles apart on the same Lancaster Avenue corridor, inside the Main Line area where his birthplace, two graph addresses, and a linked employer also sit.
- **Indication:** Repeat, everyday consumer activity (food, retail) in his home region, spaced about two years apart, is consistent with residence or recurring presence on the Main Line rather than a one-off pass-through.
- **Confidence:** Moderate. The account links to Burns through shared identifiers in the graph; the ~2023 rating is the stronger timing signal because the ~2021 review sits closer to the 2020 boundary once Google's rounding is applied.

## FBI public information

From the [FBI Most Wanted Fraudsters page for Christopher W. Burns](https://www.fbi.gov/wanted/most-wanted-fraudsters/christopher-w-burns), viewed October 15, 2026:

- **Charge:** Mail fraud. A federal arrest warrant was issued October 23, 2020, in the U.S. District Court for the Northern District of Georgia (Atlanta).
- **Alleged conduct:** Burns allegedly defrauded dozens of victims of at least $10 million through a purported "peer to peer" lending program secured by collateral that did not exist or was worth substantially less than represented.
- **Last seen:** September 24, 2020, when he left his home, one day before he was due to provide business documents to the SEC. His vehicle was later found abandoned in Dunwoody, Georgia. Last known residence: Berkeley Lake, Georgia.
- **Description:** Date of birth used December 11, 1982. Place of birth Wayne, Pennsylvania. 6'2", about 240 lb, brown hair, brown eyes. Tattoo of three interlaced black triangles on the left forearm. Former Registered Investment Advisor.
- **Reward:** Up to $150,000.

![FBI Most Wanted Fraudsters page for Christopher W. Burns](assets/fbi-christopher-w-burns.png)

*FBI Most Wanted Fraudsters page for Christopher W. Burns, captured October 15, 2026. Source: [fbi.gov](https://www.fbi.gov/wanted/most-wanted-fraudsters/christopher-w-burns).*

## OSINT analysis

### Identifier graph

Starting from public identifiers, OctoProbe built a graph of 25 nodes and 47 edges connecting the FBI wanted page to:

- **Name variants:** Christopher Burns, Chris Burns, Christopher L Burns
- **Two Wayne, PA addresses** (street numbers withheld)
- **Two email addresses** (one personal ISP address, one corporate) and **two phone numbers**, all withheld
- **An organization:** a Wayne-area pharmaceutical company, linked through the corporate email, phone, and address
- **Five usernames and six profile URLs:** LinkedIn, Foursquare, Pandora, Myspace, and a Google Maps contributor profile

![OctoProbe identifier graph export, privacy mode on](assets/graph-export-privacy.png)

*OctoProbe identifier graph for Burns: 25 nodes, 47 edges, centered on the Wayne, PA cluster. Privacy Mode on.*

### Google Maps contributor activity

The "Chris Burns" profile (Local Guide Level 2, 1 review, 1 rating) sits in the same graph cluster as Burns's name variants and personal email: [Google Maps contributor profile](https://www.google.com/maps/contrib/105840687400535390640/reviews). Captured October 15, 2026:

| Place | Contribution | Date shown by Google | Approx. year | After Sep 24, 2020? |
|---|---|---|---|---|
| PrimoHoagies, Wayne, PA | 1-star review (owner reply also "5 years ago") | "5 years ago" | ~2021 | Yes |
| Target, Wynnewood, PA (Lancaster Ave corridor) | 1-star rating | "3 years ago" | ~2023 | Yes |

### Timeline

- **Sep 24, 2020:** Burns leaves his home in Berkeley Lake, GA; vehicle later found abandoned in Dunwoody, GA.
- **Oct 23, 2020:** Federal arrest warrant issued (N.D. Georgia).
- **~2021:** Review posted at PrimoHoagies, Wayne, PA, with an owner reply from the same period.
- **~2023:** Rating posted at Target, Wynnewood, PA.

### Geography

Both sites sit on the Lancaster Avenue (Main Line) corridor west of Philadelphia, about 7 miles apart. Wayne is Burns's FBI-listed birthplace, and the graph's two addresses and linked employer are also in the Wayne area. The post-2020 activity lands in the same tight cluster as his pre-flight footprint, not in Georgia.

![Google Maps contributor profile "Chris Burns," contributions near Wayne and Wynnewood, PA](assets/google-maps-contrib.png)

*Google Maps contributor profile “Chris Burns,” captured October 15, 2026: Wayne (~2021) and Wynnewood (~2023) contributions, both after the September 24, 2020 last sighting.*

## Method

- **Sources:** The FBI wanted page, the public Google Maps contributor profile, and other public profile pages, correlated into an OctoProbe identifier graph.
- **Capture date:** October 15, 2026.
- **Timestamps:** Google Maps shows rounded relative dates, so "5 years ago" reads as ~2021 and "3 years ago" as ~2023.
- **Graph image:** A direct export from the OctoProbe app with Privacy Mode on.

## Disclaimer

Burns is wanted by the FBI on a federal mail-fraud charge. A criminal complaint or indictment is an accusation, not proof; every defendant is presumed innocent unless and until proven guilty in a court of law. Attribution of the Maps account to him is unconfirmed; tips should go to the FBI.

## Run investigations like this in OctoProbe

Seed an identifier, expand through premium APIs and public records, and keep evidence on every link, all on one live investigation graph.

[Get Access →](https://www.octoprobe.ai/#access) · [Visit homepage](https://www.octoprobe.ai/)

## Related Reading

- [Heather Zhang Case: OSINT Trail From a 2024 Reddit Allegation](/blog/heather-zhang-prc-agent-case-reddit-allegation/)
- [Whose Coffee? An Anti-Bot Developer’s Handle Turns Up on Archive.today’s Donate Link](/blog/archive-today-donate-link-takion-api-developer/)
