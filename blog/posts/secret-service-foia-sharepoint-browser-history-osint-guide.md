---
title: "How to FOIA an Official's Browser History, SharePoint Files and Teams Messages"
og_title: "Map the Tenant, Name the Custodian: How OSINT Unlocks Agency SharePoint, Teams and Browser Logs"
seo_title: "How to FOIA Browser History, SharePoint and Teams"
dek: "A seven-step guide to finding an agency's SharePoint, naming a custodian and requesting web logs, documents and Teams messages under the Freedom of Information Act, with Secret Service records as the worked example."
description: "A seven-step FOIA guide: find an agency's SharePoint with public DNS, name a custodian, and request browser logs, documents and Teams chats."
date: 2026-10-20
slug: secret-service-foia-sharepoint-browser-history-osint-guide
canonical: https://www.octoprobe.ai/blog/secret-service-foia-sharepoint-browser-history-osint-guide/
section: Public Journalism Guide
tags: [Public Journalism Guide, FOIA, OSINT, Secret Service, Microsoft 365]
keywords: [how to FOIA browser history, Secret Service FOIA, SharePoint FOIA request, Microsoft Teams FOIA, Microsoft 365 tenant OSINT, FOIA custodian search, OneDrive FOIA, FOIA fee waiver, FOIA expedited processing, FOIA exemption (b)(7)(E), Cause of Action v. OMB, agency records]
og_image: https://www.octoprobe.ai/blog/secret-service-foia-sharepoint-browser-history-osint-guide/assets/og-cover.png?v=1
hero_alt: "Street map of downtown Washington with a pin on Secret Service headquarters and the Secret Service star"
byline: Colin Aamot
author: Colin Aamot
primary_question: How do you request a federal official's browser history, SharePoint files or Teams messages under FOIA?
answer_first: Find the agency's real Microsoft 365 systems with public DNS and Microsoft's sign-in metadata, name a custodian by name and title, and ask for each record type by the system that holds it. Results vary. The Secret Service processed requests for five senior officials' browser histories and released records in part, but a federal appeals court has held that browsing histories an agency neither keeps nor uses are not agency records.
faq:
  - q: Is an official's browser history an agency record under FOIA?
    a: It depends on the agency. In Cause of Action Institute v. OMB (2021), the D.C. Circuit held that browsing histories at the Office of Management and Budget and the Agriculture Department were not agency records, because the agencies did not use them and employees could delete them. The Secret Service, by contrast, processed five requests for senior officials' browser histories and closed each as granted or denied in part.
  - q: Do I need an official's email address to request their records?
    a: No. Agencies search by custodian. A full name and title, such as "Ronald L. Rowe Jr., Deputy Director," is enough. Do not guess an email address; if a release shows a username, quote only what the agency released.
  - q: Can an agency refuse a "last 100 documents" request as creating a new record?
    a: It may try. Courts have held that running a search or query on existing data is not creating a record, but a federal judge in Washington ruled in 2012 that a bare listing or index of a database's contents can be. Ask for the documents themselves, sorted by last-modified date, rather than a list.
  - q: Where does Microsoft store Teams chats?
    a: Microsoft's eDiscovery documentation says messages in 1:1 and group chats are stored in the Exchange Online mailbox of every chat participant, channel posts in the mailbox associated with the team, files shared in chats in the sharer's OneDrive and channel files in the team's SharePoint site.
  - q: What do FOIA exemptions (b)(6), (b)(7)(C) and (b)(7)(E) mean?
    a: Exemption (b)(6) covers files whose release would be a clearly unwarranted invasion of personal privacy. (b)(7)(C) covers law-enforcement records whose release could reasonably be expected to invade personal privacy. (b)(7)(E) covers law-enforcement techniques and procedures. The Secret Service used all three in the releases described here.
  - q: How long do agencies keep web and system logs?
    a: Many logs are short-lived. The National Archives' general schedule for system access records, including log-in files and system usage files, allows agencies to destroy them when business use ceases. File requests for logs soon after the period you care about.
---

{{MODULE:cover}}

{{ANSWER}}

{{MODULE:can-request}}

You can ask a federal agency for an official's web activity, the files the official made and the chats the official sent. Requests for those records can come back empty when they don't name the system, the person or the place the data lives. This guide fixes that in seven steps, with copy-paste language for each record.

The method is a loop. Public internet records tell you where an agency keeps its files. A records request names those systems and a custodian. Each release then hands you new names, offices and systems for the next request.

The worked example throughout is two rounds of requests to the U.S. Secret Service, in 2023 and 2025. Here is what one page of the first round looks like.

:::example The page that started this guide
The page is a printout of a computer log. Each row has a timestamp, a username that begins "ron.rowe" and a box stamped "(b)(6); (b)(7)(C)" where something else used to be. Fifteen rows at 2:16 p.m. on Oct. 10, 2023, list Microsoft 365 servers, among them `unitedstatessecretservice.sharepoint.com`. The rest, logged between 10:33 and 10:38 p.m. on Oct. 4, list the Daily Mail, the New York Post and a run of advertising exchanges.

The user was Ronald L. Rowe Jr., who had been the agency's deputy director since April 2023, according to the [Homeland Security Department](https://www.dhs.gov/archive/news/2024/07/23/statement-secretary-homeland-security-alejandro-n-mayorkas-appointment-ronald-l). He went on to run the agency as acting director after Kimberly Cheatle resigned in July 2024. A federal law-enforcement agency treated a senior official's web activity as a record it could search, review and release.
:::

{{MODULE:rowe}}

NOTE: The author filed these requests in a personal capacity: five requests received by the Secret Service on Nov. 3, 2023 (log numbers 20240109 through 20240113), and a request received on April 21, 2025. OctoProbe News reviewed the releases and posts them with two redactions, described under Primary documents.

{{MODULE:takeaways}}

## How does the OSINT–FOIA loop work?

Records requests fail for boring reasons. Yours names the wrong office. It asks for "all communications" and gets a steep fee estimate. It asks for "SharePoint files" and gets "no records," because nobody searched SharePoint.

Open-source intelligence, the research discipline built on public information, fixes much of that. It can tell you the name of an agency's Microsoft 365 tenant, which cloud it runs in, which offices have their own sites and who holds which job. A request that carries those facts is harder to misread and harder to dodge.

The loop runs the other way, too. Every release is a lead sheet for the next request.

{{MODULE:loop}}

## Step 1: Identify the agency's Microsoft 365 tenant and SharePoint hosts

Many federal agencies run on Microsoft 365. Every Microsoft 365 customer has a tenant, and the tenant's original name becomes its SharePoint address. Microsoft spells this out: "[When you first sign up for Microsoft 365, you create an onmicrosoft.com domain. Even if you later add a custom domain, all your SharePoint and OneDrive URLs use the original onmicrosoft.com domain.](https://learn.microsoft.com/en-us/sharepoint/change-your-sharepoint-domain-name)"

So don't guess the address from the agency's email domain. Confirm it with three public checks. None of them touches the agency's servers.

1. **Check DNS.** Look up the candidate name, such as `[tenant].sharepoint.com`, through a public DNS-over-HTTPS service. A name that resolves exists. NXDOMAIN means no such name. Run a made-up control name too. If it fails and yours resolves, your result means something.
2. **Read Microsoft's public sign-in metadata.** Microsoft publishes an [OpenID Connect discovery document](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc) for every tenant so that apps can sign users in. Ask for it by the agency's email domain, and it returns the tenant's ID. Ask again with `[tenant].onmicrosoft.com`. If the IDs match, the SharePoint name belongs to the agency. A region field reading "GCC" marks Microsoft's government community cloud.
3. **Search passive DNS and certificate logs.** Services such as [SecurityTrails](https://securitytrails.com/), owned by Recorded Future since [January 2022](https://www.prnewswire.com/news-releases/recorded-future-acquires-securitytrails-301453543.html), keep histories of DNS names. Certificate-transparency logs, searchable at [crt.sh](https://crt.sh/), list the certificates issued for an agency's own domains. Both are better at finding an agency's websites than its SharePoint, which sits behind Microsoft's certificates.

{{MODULE:cli}}

Know what each result proves. A name that resolves shows that a Microsoft customer by that name exists. It does not show who the customer is. Anyone can register a tenant with a government-sounding name. The tenant-ID match is what ties a SharePoint name to an agency's own email domains. A name that fails to resolve is a dead end for now, but it may be a typo, a renamed tenant or a retired host. Check again before you write it into a request.

:::example The Secret Service tenant
The Secret Service's email domain is `secretservice.gov`. Its SharePoint is not `usss.sharepoint.com`. That name does not exist. It is `unitedstatessecretservice.sharepoint.com`, with personal OneDrive storage at `unitedstatessecretservice-my.sharepoint.com`.

Both Secret Service names resolve. `usss.sharepoint.com` and a made-up control name return NXDOMAIN. For `secretservice.gov`, `usss.dhs.gov` and `unitedstatessecretservice.onmicrosoft.com`, the tenant ID in Microsoft's sign-in metadata is the same, and the region field reads "GCC."
:::

Start with the host-finder table. A spreadsheet compiled by Redwing Technologies lists 431 FOIA components, nearly all federal, with their known SharePoint hosts. OctoProbe checked every host in it by DNS on Oct. 20, 2026. Of 334 unique names, 282 resolved and 52 did not. Treat it as a starting list, not an answer. Search your agency, then run the three checks yourself.

{{MODULE:hostfinder}}

:::example Why every name needs checking
The sheet's own Secret Service row lists `usss.sharepoint.com`, which does not exist, alongside DHS headquarters' `usdhs` tenant. The live Secret Service tenant is the one named in the author's request and in the Rowe log.
:::

NOTE: OctoProbe hosts the spreadsheet unaltered and flags known errors in the table above rather than changing the file. The Secret Service row's `usss.sharepoint.com` does not resolve; the live tenant is `unitedstatessecretservice.sharepoint.com`. The Cybersecurity and Infrastructure Security Agency is misnamed as the "Cybersecurity and Information Security Agency." The Bureau of Reclamation row's `doamspp` should read `doimspp`. The U.S. Chamber of Commerce and District of Columbia rows are not covered by the federal FOIA. In 10 cells, the hyperlink and the displayed text name different hosts: C334–C336, C338, C343, C372, D362, D381, D398 and D405.

NOTE: Every check in this guide is passive. The Computer Fraud and Abuse Act makes it a crime to anyone who "[intentionally accesses a computer without authorization or exceeds authorized access](https://www.law.cornell.edu/uscode/text/18/1030)" and obtains information. Looking up a public name is not access. Signing in is.

## Step 2: Identify the custodian by name or title

You don't need an email address. Agencies search by custodian, the person whose records are at issue, and a name with a title is enough. If you don't know the name, a title can work; Cause of Action Institute [named two of its officials by position](https://law.justia.com/cases/federal/appellate-courts/cadc/20-5006/20-5006-2021-08-20.html). A name and title together leave the least room for error.

Start with the agency's own words. Leadership pages, testimony, org charts and press releases give titles and dates. Those dates matter, because your request should cover a period when the person held the job.

FOIA logs are a second source. Many agencies post them, and they show which custodians other requesters have named and what came back.

If a release shows a username, note it. Don't build on it. An address pattern guessed from one partial username is a guess, and your request doesn't need it.

:::example Naming Ronald L. Rowe Jr.
The 2023 requests named "Ronald L. Rowe, Jr., Deputy Director," and the agency found his records. The Secret Service announced his appointment in an [April 18, 2023, release](https://www.secretservice.gov/newsroom/releases/2023/04/secret-service-welcomes-veteran-special-agent-ronald-rowe-deputy-director) that said, "His tenure will begin in the coming months." His [congressional witness biography](https://www.congress.gov/118/meeting/house/117738/witnesses/HHRG-118-ZT00-Bio-RoweR-20241205.pdf) from December 2024 says he was "Appointed in April 2023."

Titles change, and the request should follow them. In the fall of 2023, Rowe was the deputy director, and the requests said so. By April 2025, he was no longer acting director; Sean M. Curran took over the agency on [Jan. 22, 2025](https://www.secretservice.gov/about/leadership/director). That request named Rowe as the custodian for documents and a year of card statements covering 2024, when he served as deputy director and then as acting director. The release page shows a username beginning "ron.rowe." Neither request needed it.
:::

## Step 3: Choose the record types

Once you know the tenant and the person, these records come into reach. Ask for each one by the system that holds it.

### Browser history and web-proxy logs

Ask for both the history and the logs. Request the browser history itself, and request any web-proxy, secure-gateway, DNS or endpoint logs that record what the custodian's accounts and devices visited. *Cause of Action* turned partly on employees' freedom to delete their own histories. A log kept centrally by the agency's network or security tools stands on different footing.

:::example What the Secret Service returned
Each of the five 2023 requests asked first for "A copy of the individual's browser history (whether exported from Chrome, Safari, Windows Explorer, Mozilla, etc), to include all file attachments regardless of type and the entire email chain for completeness."

The Rowe page is not a file exported from a browser. It has host names but no page addresses, a username column and background Microsoft traffic. It looks more like a log kept by the agency's network or security tools than a history stored on one laptop. The agency sent the records on paper. By the author's count, the stack ran about 500 pages.
:::

NOTE: The 10/4/2023 rows on the Rowe page list host names for ad auctions and ad verification, among them `fastlane.rubiconproject.com`, `ssum-sec.casalemedia.com`, `eb2.3lift.com`, `match.adsrvr.org`, `acdn.adnxs.com`, `x.bidswitch.net` and `cdn.doubleverify.com`. These are the kind of real-time-bidding systems explained in OctoProbe's [report on DHS and phone location data](/blog/dhs-phone-location-data-legal-opinion-foia/). The log shows only that a browser on the account contacted them. It does not show what was read, what was shown or what data left the session.

### SharePoint documents created and edited

Ask for documents by who made or changed them. Microsoft's eDiscovery tools, which agencies use to search their own systems, track a document's "[Created by](https://learn.microsoft.com/en-us/purview/edisc-ref-document-metadata-fields)" value and "Last modified by," described as "The user who last modified the document." The audit log records "Modified file" and "Uploaded file" events, among others, according to [Microsoft's activity list](https://learn.microsoft.com/en-us/purview/audit-log-activities).

Name both hosts: the main SharePoint and the custodian's OneDrive at `[tenant]-my.sharepoint.com`. Ask for the documents themselves, sorted by last-modified date, over a fixed period. Step 5 explains why.

For documents a custodian commented on, ask for the documents. OctoProbe found no comment event for SharePoint files in Microsoft's audit activity list, so a request for a comment log may come back empty even when the documents exist.

### Teams messages, channel files and chat files

Teams chats are easy to miss in a records search. Microsoft's eDiscovery guide says "[Teams data is stored in Azure Cosmos DB. Exchange Online stores Teams compliance records](https://learn.microsoft.com/en-us/purview/edisc-search-teams)" that eDiscovery searches. In practice, chat messages are copied into mailboxes, and shared files land in OneDrive or SharePoint. Name each place:

- **Chats** (1:1 and group): the custodian's Exchange Online mailbox.
- **Channel posts:** the team's mailbox, by team name.
- **Channel files:** the team's SharePoint site.
- **Files shared in chats:** the sharer's OneDrive.

{{MODULE:m365}}

:::example Other requesters already ask
At least a dozen entries in the Secret Service's FY 2024 log seek "[any chats in the relevant virtual platforms (e.g., Microsoft Teams, Zoom, Webex, etc.)](https://www.secretservice.gov/sites/default/files/reports/2025-02/FOIA-Log-FY-2024.pdf#page=107)." You can go further by naming the custodian's mailbox for chats, the team's mailbox and SharePoint site for channels and the custodian's OneDrive for files shared in chats.
:::

### Card statements and sitemaps

Two more records round out a request. An official's agency card statements show spending. A sitemap of the agency's SharePoint shows how the agency organizes its work, and its site names tell you which offices and systems to name next.

:::example The 2025 request
The Secret Service received a four-part request on April 21, 2025. It asked for the last 100 documents Rowe edited and the last 100 he created on the agency's SharePoint, a year of his agency card statements and a current sitemap of the agency's SharePoint. Each item named the agency's real SharePoint addresses. The release ran 117 pages. It held a sitemap of roughly 660 internal sites and 105 pages of blacked-out card statements. The PDF contains no records for the two document items.
:::

## Step 4: Write the request

Keep each item to one sentence. Give every item a date range, a custodian with a title and a system. Then add the parts that decide cost and speed.

- **Scope and date range.** One record type per numbered item. A fixed start and end date on each.
- **Custodian.** Full name and title.
- **Systems.** SharePoint, OneDrive, Exchange Online and Teams, by host name where you have it.
- **Format.** FOIA requires agencies to provide records "[in any form or format requested by the person if the record is readily reproducible](https://www.law.cornell.edu/uscode/text/5/552)" in that form. Ask for electronic copies or native files.
- **Fee category.** If you're a reporter, say so. Fees for "a representative of the news media" are limited to "reasonable standard charges for document duplication" when records are not sought for commercial use. The law defines that requester as one who "gathers information of potential interest to a segment of the public, uses its editorial skills to turn the raw materials into a distinct work, and distributes that work to an audience."
- **Fee waiver.** Ask for one if the records are newsworthy. The standard is disclosure that "is likely to contribute significantly to public understanding of the operations or activities of the government and is not primarily in the commercial interest of the requester." Explain how you will publish.
- **Expedited processing, where it applies.** A requester "primarily engaged in disseminating information" can ask for it by showing "urgency to inform the public concerning actual or alleged Federal Government activity." The request must be "certified by such person to be true and correct to the best of such person's knowledge and belief." Use it only when the urgency is real.
- **A search description.** Ask the agency to describe where it looked. A "no records" answer means more when you know.

:::example The 2025 wording
The Secret Service's [letter](/blog/secret-service-foia-sharepoint-browser-history-osint-guide/docs/usss-final-response-excerpt.png) quotes the request's first item this way: "The last 100 documents edited by the custodian on the Secret Service Sharepoint (https://unitedstatessecretservice.sharepoint.com OR https://unitedstatessecretservice-my.sharepoint.com)." The second item was the same, with "created" in place of "edited." The fourth asked for "A current sitemap of the Secret Service Sharepoint (https://unitedstatessecretservice.sharepoint.com)." The request did this in four numbered items, and the response letter restates them.
:::

Use the builder to turn those into your own request. Fill in the brackets, tick the records you want and copy the text.

{{MODULE:builder}}

A few rules of thumb:

- Use keywords for Teams and email. A year of chats with no search terms invites a delay or a fee estimate.
- Split big asks into separate numbered items, so one problem item doesn't stall the rest.
- Keep the request about records, not people's private lives. Expect exemptions (b)(6) and (b)(7)(C) on names and personal details.

## Step 5: Anticipate the agency's answers

Three answers come back again and again. Plan for each before you file.

### "Exempt"

In the Secret Service releases, three codes cover nearly everything withheld. Exemption (b)(6) protects files whose release would be "[a clearly unwarranted invasion of personal privacy](https://www.law.cornell.edu/uscode/text/5/552)." Exemption (b)(7)(C) protects law-enforcement records whose release "could reasonably be expected to constitute an unwarranted invasion of personal privacy." Exemption (b)(7)(E) protects material that "would disclose techniques and procedures for law enforcement investigations or prosecutions."

How to word around them: ask for records about official work, not private details. Expect names of staff and account numbers to come out blacked out. Ask for what a withheld column would show in the aggregate, such as site names without addresses, when the addresses are the sensitive part.

:::example How the Secret Service used them
The first two codes explain the boxes over names and account digits. The third is the agency's basis for withholding the sitemap's URLs and much of the card statements. On the sitemap, the agency withheld the entire URL column under (b)(7)(E) on every page. It released the names.
:::

### "No duty to create a record"

The legal risk is the word "list." FOIA requires agencies to "[make reasonable efforts to search for the records in electronic form or format](https://www.law.cornell.edu/uscode/text/5/552)," and to provide records "in any form or format requested … if the record is readily reproducible." Courts have said a database query is a search. The U.S. Court of Appeals for the Ninth Circuit held in 2021 that "[using a query to search for and extract a particular arrangement or subset of data already maintained in an agency's database does not amount to the creation of a new record](https://www.justice.gov/oip/ctr-investigative-reporting-v-doj-no-18-17356-2021-wl-4314789-9th-cir-sept-23-2021-wardlaw-j)." The court added, "It makes no difference if the query produces a set of documents, a list, a spreadsheet, or some other form of results that the agency has not previously viewed."

A federal judge in Washington drew a line in 2012. The court held that "[sorting a pre-existing database of information to make information intelligible does not involve the creation of a new record](https://www.justice.gov/archive/oip/courtdecisions/oct-19-2012.html)." But a request for a "listing or index of a database's contents that does not seek the contents of the database, but instead essentially seeks information about those contents, is a request that requires the creation of a new record, insofar as the agency has not previously created and retained such a listing or index." In a later ruling in the same litigation, the D.C. Circuit [sided with the CIA](https://www.justice.gov/oip/natl-sec-counselors-v-cia-969-f3d-406-dc-cir-2020-srinivasan-j) on a request for one such listing.

That is a real risk for both "last 100" requests and sitemap requests. How to word around it: ask for the documents themselves, sorted by date, over a fixed period, not a list of them. For a sitemap, ask for an existing site inventory or admin report if one exists.

:::example Where the objection bites
The PDF contains no records for items 1 and 2, the last 100 documents the custodian edited and created. The Secret Service, for its part, did produce a sitemap.
:::

### "Not an agency record"

Under FOIA, the public can get "agency records." The law defines a record broadly, as information "[maintained by an agency in any format, including an electronic format](https://www.law.cornell.edu/uscode/text/5/552)." The harder question is whether something on a government computer belongs to the agency at all.

In 2021, the U.S. Court of Appeals for the D.C. Circuit said browsing histories did not, at least in one case. A watchdog group, Cause of Action Institute, had asked the Office of Management and Budget and the Agriculture Department for senior officials' web histories. The court ruled for the agencies.

> "[In light of the foregoing, we hold that the internet browsing histories requested by Cause of Action are not agency records subject to disclosure under FOIA.](https://law.justia.com/cases/federal/appellate-courts/cadc/20-5006/20-5006-2021-08-20.html)"

The court's reasons were practical. "[OMB and USDA did not use the officials' browsing histories for any purpose, much less a purpose connected to agency decisionmaking](https://law.justia.com/cases/federal/appellate-courts/cadc/20-5006/20-5006-2021-08-20.html)," the court wrote. And "[employees of OMB and USDA could freely delete their browsing histories, a practice incompatible with integration of these documents into the agencies' record systems](https://law.justia.com/cases/federal/appellate-courts/cadc/20-5006/20-5006-2021-08-20.html)."

*Cause of Action* turned on control and use: whether the agency kept the data, relied on it and let employees erase it. A centrally kept web log is a different animal. The National Archives' [general records schedule for IT systems](https://www.archives.gov/files/records-mgmt/grs/grs03-2.pdf) treats "log-in files," "audit trail files and extracts" and "system usage files" as federal records with a set disposition: "Destroy when business use ceases." The schedule does not mention browser history by name, and it carves out monitoring for agency missions such as law enforcement. But it shows that logs of this kind are records an agency is expected to manage.

How to word around it: ask for the browser history and for any centrally retained proxy, gateway, DNS or endpoint logs in the same item. If the agency calls the history personal, the logs are a separate question.

:::example The Secret Service's practice points the other way
On five requests received the same day, the Secret Service searched for an official's browser history, processed what it found and released it in part, withholding some information under privacy and law-enforcement exemptions. The Rowe page looks more like a centrally kept log than a history stored on one laptop.
:::

## Step 6: Track and follow up

Write down the date the agency received your request and the log number it assigns. The clock starts there. Agencies must "[determine within 20 days (excepting Saturdays, Sundays, and legal public holidays)](https://www.law.cornell.edu/uscode/text/5/552)" whether to comply. The law lets agencies extend that deadline in "[unusual circumstances](https://www.law.cornell.edu/uscode/text/5/552)," and they must tell you in writing when they do.

Check the agency's FOIA log. Many agencies post them. A log entry confirms what the agency recorded as your request, when it arrived and how it closed. It also shows you how other requesters worded similar asks.

:::example The Secret Service's FY 2024 log
The Secret Service's [FOIA log for fiscal 2024](https://www.secretservice.gov/sites/default/files/reports/2025-02/FOIA-Log-FY-2024.pdf#page=12), posted on the agency's website, lists five requests received Nov. 3, 2023, from the author. Each sought records "from the last month of October 2023" for one official: Director Kimberly A. Cheatle; "Ronald L. Rowe, Jr., Deputy Director"; Chief Operating Officer Cynthia Sjoberg Radway; David M. Smith, assistant director for investigations; and Gloria R. Armstrong, assistant director for professional responsibility. The log records the result for all five in three words: "Granted/Denied in Part." The photographed page comes from the return for Rowe, request 20240110. Its dates, Oct. 4 and Oct. 10, fall inside the request's October window.
:::

{{MODULE:fig-log}}

NOTE: Requester name redacted by OctoProbe; the requester is the author. The full log is linked as the agency posted it.

Watch the disposal clock. The National Archives' schedule lets agencies destroy many system logs "when business use ceases," so a request for last month's web log has better odds than one for last year's. File log requests fast.

If you hit a dispute you can't resolve with the FOIA office, the Office of Government Information Services at the National Archives is one option. The law says [OGIS](https://www.archives.gov/ogis) "shall offer mediation services to resolve disputes between persons making requests under this section and administrative agencies as a nonexclusive alternative to litigation."

## Step 7: Use what comes back

Each release is raw material. Read it for names, systems and redaction patterns, and turn them into the next set of requests.

- **Sites become systems.** A site that holds audit logs or a card-program portal points to records you can name.
- **Hosts become clouds.** Microsoft host names in a log confirm which cloud the agency runs in.
- **Hubs become offices.** Each hub in a sitemap is an office with its own records, staff and leaders. Those leaders are your next custodians.
- **Withholdings become questions.** An entire column withheld under (b)(7)(E) tells you what the agency considers sensitive. That is worth knowing when you write the next request.

:::example Reading the April 2025 release
The release is 117 image-only pages. The PDF itself holds no cover letter; the agency's response letter, sent separately, opens by restating the four items.

**Card statements, pages 1–105.** The pages make up 44 statement fragments. Every one starts at "Page 2." Page 1 of each statement, normally the summary page, is absent, and page 3 of one four-page statement is missing (pages 101–102). Every page is blacked out except the page number and, on each final page, a line reading "Account: XXXX-XXXX-XXXX" followed by an exemption box. No merchant, amount or date is visible on any page.
:::

{{MODULE:fig-statement}}

:::example The sitemap, pages 106–117
The sitemap is headed "USSS - Standard Sensitive Info" and has four columns: site name, URL, hub and "Active/Accessable." The agency withheld the entire URL column under (b)(7)(E), the exemption for law-enforcement techniques and procedures, on every page. It released the names.

Those names are a map of the agency. There are hubs for administration, investigations and protection, with sites named for presidents' protective divisions ([p. 107](/blog/secret-service-foia-sharepoint-browser-history-osint-guide/docs/usss-foia-release-two-redactions.pdf#page=107)). There are sites a records requester will want to know about: "Freedom of Information Act" and "Enterprise Records and Knowledge Management Division" ([p. 113](/blog/secret-service-foia-sharepoint-browser-history-osint-guide/docs/usss-foia-release-two-redactions.pdf#page=113)), and "SP 2016 Audit Logs" and "Travel Card Portal" ([p. 116](/blog/secret-service-foia-sharepoint-browser-history-osint-guide/docs/usss-foia-release-two-redactions.pdf#page=116)). Event sites run from "RNC 2024" and "DNC 2024" to "2025 Presidential Inauguration."
:::

{{MODULE:fig-sitemap}}

{{MODULE:explorer}}

:::example The next round
"SP 2016 Audit Logs" suggests the agency keeps SharePoint audit records in a site of their own. Ask for the audit entries for a named custodian and date range. "Travel Card Portal" points to the card program's guidance and records. The Rowe page lists `gcc.thor.aesir.office.com` and other Microsoft government-cloud hosts. That confirms what the sign-in metadata showed: the agency runs in Microsoft's government community cloud.

Two lessons follow. First, a sitemap request can work even with the addresses withheld, because the site names tell you which offices and record systems to name next. Second, the document items are where the listing-or-index objection bites. A future request should ask for the documents, sorted by last-modified date, over a fixed period.
:::

NOTE: The release contains some site names that point to sensitive operations. OctoProbe quotes only names that illustrate what a sitemap request returns, and posts the rest as the agency released them.

Then map again. The method doesn't end with one release.

## Before you file

{{MODULE:before-file}}

## Primary documents

The files below are hosted on this page. The explorer above links each release page to the PDF.

{{MODULE:docs-table}}

NOTE: OctoProbe redacted two apparent employee first names that the agency left unredacted in the sitemap: one on page 110 and one on page 114. Neighboring rows of the same kind, sites such as "[name] Playground" and "[name] Sandbox," carry (b)(6) boxes where the agency withheld a name. Those two black boxes are the only changes to the hosted PDF. Every other page is as released, and the page images outside the two boxes are unchanged. The original file is not posted. SHA-256 checksums are in the [SHA256SUMS file](/blog/secret-service-foia-sharepoint-browser-history-osint-guide/docs/SHA256SUMS.txt).

NOTE: The browser-history page is a photograph of one printed page, posted without the original file's metadata. The response-letter excerpt is shown as provided, with file metadata removed. The spreadsheet is posted as received. The FOIA-log figure is a crop with the requester name redacted; the full log is linked, not hosted.

## What terms should FOIA requesters use?

Agencies and Microsoft use their own vocabulary. A request that speaks it is easier to route.

{{MODULE:glossary}}

{{FAQ}}

{{AUTHOR_NOTE}}

{{MODULE:related}}

## Disclaimer

This guide relies on FOIA releases, agency records, court opinions, statutes and Microsoft's public documentation. It is not legal advice.
