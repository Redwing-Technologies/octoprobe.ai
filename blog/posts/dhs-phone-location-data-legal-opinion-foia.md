---
title: "DHS Lawyers Wrote 24 Pages on Buying Your Phone’s Location Data. They Withheld Every Page of the Analysis."
seo_title: "DHS Withheld Its Legal Case for Buying Location Data"
dek: "A 2020 Homeland Security legal opinion weighed whether CBP and ICE could use advertising-ID location data without a warrant. Released under the Freedom of Information Act, it comes back as a cover page and 23 pages stamped “(b)(5).”"
description: "A DHS legal opinion on buying phone ad-ID location data came back under FOIA as one page and 23 withheld pages. How the trade works and what is still secret."
date: 2026-10-20
slug: dhs-phone-location-data-legal-opinion-foia
canonical: https://www.octoprobe.ai/blog/dhs-phone-location-data-legal-opinion-foia/
tags: [Investigation, FOIA, Surveillance, Privacy, Adtech]
keywords: [commercial telemetry data, advertising ID location data, DHS FOIA, Venntel, CBP, ICE, FBI, real-time bidding, MAID, IDFA, Carpenter, Fourth Amendment Is Not For Sale Act]
og_image: https://www.octoprobe.ai/blog/dhs-phone-location-data-legal-opinion-foia/assets/og-cover.png?v=2
byline: Colin Aamot
author: Colin Aamot
author_url: https://www.linkedin.com/in/colinaamot/
author_image: /assets/authors/colin-aamot-192.jpg
author_bio: "Colin Aamot is a former U.S. Army counterterrorism information operations (CT-IO) planner who deployed with several joint task forces in support of Operations Inherent Resolve and Spartan Shield. He subsequently worked at the Heritage Foundation and in the office of Rep. Darrell Issa, with portfolios spanning foreign policy, technology, and innovation. He holds an MA in Global Security Studies from Johns Hopkins University and an MBA from UNC Kenan-Flagler Business School."
author_links: ["LinkedIn | https://www.linkedin.com/in/colinaamot/", "X | https://x.com/ColinAamot", "Daily Signal (previous bylines) | https://www.dailysignal.com/author/colin-aamot/"]
primary_question: How does the U.S. government use commercial phone advertising data to track location?
answer_first: Federal agencies have bought location data harvested from phone apps and ad auctions, keyed to each phone's advertising ID, without warrants. DHS lawyers analyzed the legal risks in a 24-page 2020 opinion. A FOIA release shows the department withheld all of its legal reasoning, while oversight bodies found agencies skipped required privacy reviews.
faq:
  - q: What is commercial telemetry data?
    a: It is the Homeland Security Department's term for location and device data bought from commercial brokers, usually collected by smartphone apps and advertising systems and keyed to a phone's advertising ID. The Defense Department and GAO use a related term, collateral telemetry data.
  - q: Do federal agencies need a warrant to buy phone location data?
    a: No court has squarely decided it. The Supreme Court's 2018 Carpenter decision requires a warrant to compel cell-site records from carriers, but agencies including DHS, ICE and the Defense Intelligence Agency have taken the position that purchasing commercially available data is different. The House passed a bill to ban such purchases in April 2024; it did not become law.
  - q: What did the DHS legal opinion on advertising IDs conclude?
    a: The public does not know. DHS released only the first page of the Sept. 25, 2020 opinion, which says it reviews Fourth Amendment and Privacy Act challenges and proposes measures to mitigate legal risks. The remaining 23 pages were withheld under FOIA exemption (b)(5) for privileged deliberations.
  - q: Is an advertising ID anonymous?
    a: Not in practice. The FTC has said such location data can be used to identify consumers and is not anonymized, and a 2022 intelligence-community report found it is often possible to deanonymize commercially available data. A phone's nightly location usually points to a home. Analysts weigh where a device sits in the evenings and early mornings to estimate its "bed-down location," or BDL, the place where its owner typically sleeps.
  - q: How can I turn off my phone's advertising ID?
    a: On iPhones, deny apps permission to track under Settings, Privacy and Security, Tracking. On Android, delete the advertising ID under Settings, Privacy, Ads (labels vary by device). Limiting location permission to apps that need it, and to while the app is in use, reduces what apps can collect.
---

{{MODULE:cover}}

{{ANSWER}}

On Sept. 25, 2020, the Department of Homeland Security's top lawyer signed a memo with a plain subject line: "[Legal Implications of Advertising Identifier Geolocation Data Use by CBP and ICE](/blog/dhs-phone-location-data-legal-opinion-foia/docs/dhs-ogc-adid-legal-opinion-2020-09-25.pdf#page=1)." It went to the department's chief privacy officer. Its opening paragraph promised a review of "potential challenges under the Fourth Amendment and the Privacy Act of 1974" and of "some proactive measures" the department "may implement to mitigate certain legal risks."

That paragraph is all the public gets. When DHS released the opinion under the Freedom of Information Act, pages 2 through 24 came back blank except for a stamp reading "(b)(5)," the exemption for privileged internal deliberations. Four other legal memos in the same release, on social media monitoring, open-source intelligence and the Privacy Act, got the same treatment. Of 93 pages, 87 were withheld in full.

The missing pages matter because the practice is not hypothetical. DHS's inspector general found that Customs and Border Protection ran [more than 55,000 queries](https://www.oig.dhs.gov/sites/default/files/assets/2023-09/OIG-23-61-Sep23-Redacted.pdf#page=13) of what the department calls "commercial telemetry data" in fiscal 2019 and 2020, and that Immigration and Customs Enforcement ran [more than 16,000](https://www.oig.dhs.gov/sites/default/files/assets/2023-09/OIG-23-61-Sep23-Redacted.pdf#page=14) in fiscal 2020 alone. The FBI bought its own seat on the same kind of portal in February 2020. The legal reasoning that let these agencies skip a warrant is still secret.

This report reads the released pages, the FBI's contract file and the public oversight record side by side. Interactive explainers show, with made-up data, how an app's ad slot becomes a location feed and how a buyer turns that feed into a list of phones. All six primary documents are posted unaltered at the end.

NOTE: The DHS records in this report were obtained through FOIA request 2024-HQFO-00696, filed in January 2024 by the author in a personal capacity. OctoProbe News reviewed the full release and posts it as received. Maps, device records and identifiers in the interactive figures are generated illustrations; no real person, device or location history is depicted.

{{MODULE:takeaways}}

## What did DHS lawyers say about buying phone location data?

The opinion was written by Chad R. Mizelle, then the senior official performing the duties of DHS general counsel, for Dena Kozanas, the chief privacy officer. Its first page is marked "ATTORNEY-CLIENT & DELIBERATIVE PROCESS PRIVILEGED." The released executive summary describes the scope in a single paragraph:

> "This memorandum analyzes use by U.S. Customs and Border Protection ('CBP') and U.S. Immigration and Customs Enforcement ('ICE') of commercially available geolocation data associated with the advertising identifier ('AdID') present on many modern mobile electronic devices. It assesses the potential legal issues associated with using AdID data as a law enforcement tool."

The next sentence says it "reviews potential challenges under the Fourth Amendment and the Privacy Act of 1974." Then the text stops. A large "(b)(5)" fills the rest of the page, and the next 23 pages, Bates numbers 2024-HQFO-00696-000002 through -000024, carry nothing else ([PDF pp. 2–24](/blog/dhs-phone-location-data-legal-opinion-foia/docs/dhs-ogc-adid-legal-opinion-2020-09-25.pdf#page=2)).

{{MODULE:fig-foia-p1}}

The release does not say what the lawyers concluded, which risks they ranked highest, or which "proactive measures" they recommended. It does not show whether anyone acted on the advice.

The question the opinion answers was already on the table inside DHS. On June 19, 2019, more than a year earlier, a DHS Privacy Office official wrote to colleagues about a program buying data from the broker Venntel. "The PTA was never approved because we had and continue to have significant concerns with this technology," the official wrote, referring to a privacy threshold analysis. "Prior to receiving the information, did OGC conduct an analysis under the Carpenter case to ensure that we are able to legally acquire it?" That email surfaced in records the American Civil Liberties Union obtained by lawsuit ([ACLU release, PDF p. 100](https://assets.aclu.org/live/uploads/legal-documents/DHS_HQ_21_09_Records.pdf#page=100)). Another page in the same set says a DHS unit had been "instructed to refrain from using any Venntel data until a legal and Privacy ruling has been determined" ([PDF p. 115](https://assets.aclu.org/live/uploads/legal-documents/DHS_HQ_21_09_Records.pdf#page=115)).

Exemption 5 covers "inter-agency or intra-agency memorandums or letters that would not be available by law to a party other than an agency in litigation with the agency." Since 2016, the [FOIA statute](https://www.law.cornell.edu/uscode/text/5/552) also says an agency may withhold information only if it "reasonably foresees that disclosure would harm an interest protected by an exemption," and it must consider releasing the parts that can be separated out. DHS released one paragraph out of 24 pages.

## What is ad-tech location data?

Every modern iPhone and Android phone carries a resettable string of letters and numbers meant for advertisers. Apple calls its version the [Identifier for Advertisers](https://developer.apple.com/documentation/adsupport/asidentifiermanager/advertisingidentifier), or IDFA. Google calls Android's the [advertising ID](https://support.google.com/googleplay/android-developer/answer/6048248). The industry's umbrella term is mobile advertising ID, or MAID; the DHS opinion says "AdID."

The ID exists so that ad systems can recognize the same phone across different apps without a name or phone number. That is also what makes it useful to an investigator. An app that shows ads, or that embeds a data-collection kit from a third party, can attach the ID to the phone's location, the time, the network and a long list of hardware details. A broker that buys enough of those records can draw one phone's movements over weeks.

Agencies insist the data is anonymous. Regulators disagree. In a January 2024 order against the broker X-Mode Social, the Federal Trade Commission said its location data was "[not anonymized](https://www.ftc.gov/news-events/news/press-releases/2024/01/ftc-order-prohibits-data-broker-x-mode-social-outlogic-selling-sensitive-location-data)." In December 2024 the FTC said Venntel's parent, Gravy Analytics, collected "[more than 17 billion signals from around a billion mobile devices daily](https://www.ftc.gov/news-events/news/press-releases/2024/12/ftc-takes-action-against-gravy-analytics-venntel-unlawfully-selling-location-data-tracking-consumers)" and that the data "can be used to identify consumers and is not anonymized." After an intruder reached Gravy's cloud storage in January 2025 and a sample of its data surfaced on a dark-web forum, its parent company, Unacast, described what it licenses: "[mostly … mobile advertising IDs (MAIDs), longitude/latitude, and timestamps](https://cdn.prod.website-files.com/661d3eb71206816721de67f8/67c5dda5d34d66734fb2ab24_Unacast%20Incident%20Fact%20Sheet_03032025.pdf)."

The explorer below shows 56 categories of data that ad exchanges may measure when serving an ad. The list is a wide lens, compiled across multiple exchanges; not every exchange measures every field. Each category is sorted by where it typically comes from: the ad auction's own bid request, a commercial device database, a data-collection kit inside an app, or a broker's later enrichment.

{{MODULE:fields}}

Some of the most sensitive identifiers on such lists, including the IMEI hardware serial and the SIM card's ICCID, are not part of the public auction standard at all. They come from apps with deeper device access, or from a lookup that matches a phone model to a catalog. A buyer rarely sees the difference. A delivered record looks like one flat row.

NOTE: On terms: In intelligence-community usage, "AAID" is shorthand for Apple's advertising identifier, the IDFA. Elsewhere the same letters often refer to Android: a 2024 CBP privacy assessment writes that Google refers to its identifier as "[Google Advertising ID (AAID)](https://www.dhs.gov/sites/default/files/2024-08/24_0812_priv_pia-cbp-080-commercial-telemetry.pdf#page=5)." FOIA requesters should spell out which they mean.

## How does an app turn into a location feed?

Location gets into the market two ways. The first is through software development kits, or SDKs: code libraries that app makers bundle for ads, analytics or payments. Some SDKs read the phone's GPS position directly whenever the app has location permission and send it, with the advertising ID, to the kit's maker. The Electronic Frontier Foundation reported that the broker X-Mode paid app developers "[around 3 cents per user per month](https://www.eff.org/deeplinks/2022/08/inside-fog-data-science-secretive-company-selling-mass-surveillance-local-police)" for access to location data.

The second is the ad auction itself. When an app has an empty ad slot, it asks an exchange to fill it. The exchange packages a "bid request," described in the industry's [OpenRTB 2.6 specification](https://github.com/InteractiveAdvertisingBureau/openrtb2.x/blob/main/2.6.md), and sends it to many bidders at once, typically within a fraction of a second. The request's `device.ifa` field carries the advertising ID "in the clear (i.e., not hashed)," the specification says. A `geo` object can carry latitude and longitude along with a `type` code that tells bidders whether the position came from GPS, an IP address lookup, or the user.

Every bidder that receives the request sees those fields, including bidders that lose the auction. Nothing in the protocol makes them forget. The stepper below walks one bid request from an app to a broker.

{{MODULE:auction}}

The arithmetic is why brokers can claim enormous scale. A phone that loads a few hundred ads a day, each offered to a dozen bidders, can produce thousands of copies of its position. Use the calculator to change the assumptions.

{{MODULE:fanout}}

Not every record is equally precise. A GPS fix can place a phone in one room; an IP-derived location may only name a city. Buyers sort and discount records by that precision, as the ladder below shows.

{{MODULE:ladder}}

Platforms have narrowed the pipe without closing it. Since Apple's [iOS 14.5](https://www.apple.com/newsroom/2021/04/ios-14-5-offers-unlock-iphone-with-apple-watch-diverse-siri-voices-and-more/) in April 2021, apps must ask permission before tracking users across other companies' apps, and a phone that declines returns a string of zeros for the IDFA. Android lets users delete the advertising ID. Many people never change the defaults, and a location SDK with permission does not need the auction at all.

## What can one advertising ID reveal?

A single location point says little. Thirty days of them say a great deal. Where a phone sits between midnight and 5 a.m. is almost always a home. Analysts call that spot the device's "bed-down location." Where it sits from 9 to 5 on weekdays is usually a workplace. Repeat visits show a gym, a clinic, a place of worship, a lawyer's office. Overlap between two phones, night after night, suggests a partner. A phone that appears at the same address as a known person's car or home network can be tied to that person without a subpoena to anyone. The picture also ages. People upgrade and change phones and reset or replace their advertising IDs, so bid-stream records lose relevance over time.

The EFF, describing records it obtained about the police vendor Fog Data Science, put it this way: device searches allow "'pattern of life' analyses that reveal where the device owner sleeps, works, studies, worships, and associates. [This can tie an 'anonymous' device to a specific, named individual](https://www.eff.org/deeplinks/2022/08/inside-fog-data-science-secretive-company-selling-mass-surveillance-local-police)." A declassified 2022 report to the director of national intelligence reached the same conclusion: "Although CAI may be 'anonymized,' it is often possible (using other CAI) to deanonymize and identify individuals" ([ODNI report](https://www.dni.gov/files/ODNI/documents/assessments/ODNI-Declassified-Report-on-CAI-January2022.pdf)). CAI is the government's abbreviation for commercially available information.

The figure below is entirely fictional. It shows one invented advertising ID over 30 days near a made-up town. Hover over or tap the points, switch layers, and watch the dwell profile pick out the "home" and "work" clusters with no name attached.

{{MODULE:device}}

Each dot on that map began as one row of a delivered file. The bid-request view breaks a single row into the fields a buyer receives.

{{MODULE:bidrequest}}

## How does a geofence turn a place into a list of phones?

Investigators can also start from a place. Draw a polygon around a building, choose a time window, and the system returns every advertising ID seen inside it. The EFF called these "area searches" and said they "[can be used to gather device IDs for everyone in an area](https://www.eff.org/deeplinks/2022/08/inside-fog-data-science-secretive-company-selling-mass-surveillance-local-police)," while device searches "can be used to learn where those people live and work."

The capability is not theoretical. In 2024, 404 Media and the Atlas Privacy team described a demonstration of Babel Street's Locate X tool in which a map of an abortion clinic in the southern United States showed "[more than 700 red dots over the clinic itself](https://www.404media.co/inside-the-u-s-government-bought-tool-that-can-track-phones-at-abortion-clinics/), each representing a phone." In its Gravy action, the FTC said the company used geofencing to build and sell lists of people seen at particular places.

The example below uses a fictional community center. Step through the time window and watch the device list grow.

{{MODULE:geofence}}

Area and device searches work as a pair. The first turns a place into a list of IDs; the second turns each ID into a home address. That is the same two-step logic as a "geofence warrant" served on Google, except that a purchased tool needs no judge. The toggle below shows both directions over the same fictional data. In the forward direction, an analyst starts with one ID and gets its places. In the reverse direction, the analyst starts with one place and gets every ID that passed through.

{{MODULE:directions}}

## How does the government buy it?

Federal agencies generally do not buy location data from app makers. They buy subscriptions from brokers or resellers, who buy from aggregators, who buy from apps and ad exchanges. The FBI's own contract file shows how ordinary the final step looks.

The file, released under FOI/PA request 1491075-000 and posted on the [FBI Vault](https://vault.fbi.gov/contract-with-venntel), concerns "Venntel Portal Access" for the bureau's Operational Technology Division. Its statement of work, dated Jan. 9, 2020, begins: "This is a contract to provide access (an account) to an online portal … for the Federal Bureau of Investigation" ([p. 7](/blog/dhs-phone-location-data-legal-opinion-foia/docs/fbi-foipa-1491075-000-venntel-portal-contract.pdf#page=7)). It says "the intended procurement is for unclassified product that is sold by the vendor to their customers" ([p. 8](/blog/dhs-phone-location-data-legal-opinion-foia/docs/fbi-foipa-1491075-000-venntel-portal-contract.pdf#page=8)).

A market-research memo in the file explains where the product comes from: "Location information is gathered by applications running on a wireless device," and "access to the location information is resold to marketing firms for various types of analysis" ([p. 11](/blog/dhs-phone-location-data-legal-opinion-foia/docs/fbi-foipa-1491075-000-venntel-portal-contract.pdf#page=11)). The request for quotes sought one item: "Venntel Portal, from Venntel Inc, for 1 user-annual fee includes 12,000 queries per year" ([p. 20](/blog/dhs-phone-location-data-legal-opinion-foia/docs/fbi-foipa-1491075-000-venntel-portal-contract.pdf#page=20)).

{{MODULE:fig-fbi-rfq}}

The order, number 15F06720F0000659, was dated Feb. 13, 2020 ([p. 22](/blog/dhs-phone-location-data-legal-opinion-foia/docs/fbi-foipa-1491075-000-venntel-portal-contract.pdf#page=22)), with a period of performance from March 1, 2020, to Feb. 28, 2021 ([p. 24](/blog/dhs-phone-location-data-legal-opinion-foia/docs/fbi-foipa-1491075-000-venntel-portal-contract.pdf#page=24)). Federal spending records show it went to a reseller, GovPlace LLC, for [$22,346.37](https://www.usaspending.gov/award/CONT_AWD_15F06720F0000659_1549_NNG15SC77B_8000). A Justice Department clause attached to the order is blunt: "Under this contract, the Department obtains personally identifiable information about individuals from the contractor" ([p. 30](/blog/dhs-phone-location-data-legal-opinion-foia/docs/fbi-foipa-1491075-000-venntel-portal-contract.pdf#page=30)).

The spending record adds two details. The order was placed under NASA's governmentwide acquisition contract number NNG15SC77B, a vehicle agencies use to buy information-technology products from approved resellers, and it lists one offer received. For the bureau's technology division, a year of searchable phone locations was bought the way an office buys a software license.

DHS bought on a larger scale. A Science and Technology Directorate order [posted by DHS](https://www.dhs.gov/sites/default/files/2021-12/Venntel%20Contract%20Document-ocr-_0.pdf#page=5) lists a "Venntel Portal annual license for 5 named users with 12,000 queries per year, per user," and another page in the set describes a portal that "brings together 80,000 mobile applications into a single source" with "geo-fencing capabilities" ([p. 37](https://www.dhs.gov/sites/default/files/2021-12/Venntel%20Contract%20Document-ocr-_0.pdf#page=37)). The Wall Street Journal [first reported](https://www.wsj.com/articles/federal-agencies-use-cellphone-location-data-for-immigration-enforcement-11581078600) in February 2020 that CBP and ICE were buying Venntel data for immigration and border enforcement.

The inspector general's 2023 audit found that CBP had six contracts for access to two such databases in fiscal 2019 and 2020, and that ICE had nine. It found that "ICE has used CTD since September 2018 without an approved PIA," meaning a privacy impact assessment ([OIG-23-61, PDF p. 14](https://www.oig.dhs.gov/sites/default/files/assets/2023-09/OIG-23-61-Sep23-Redacted.pdf#page=14)).

The flow below links each stage to the public record that documents it.

{{MODULE:flow}}

The trade did not end with the audit. CBP's 2024 [privacy impact assessment](https://www.dhs.gov/sites/default/files/2024-08/24_0812_priv_pia-cbp-080-commercial-telemetry.pdf#page=2) was written for past use and says the agency no longer collects such data; it adds that CBP "did not ingest bulk commercial telemetry data" and that "no single commercial telemetry data vendor has comprehensive coverage." ICE told FedScoop in January 2024 that it had [stopped using the data](https://fedscoop.com/ice-says-its-stopped-using-phone-location-data/). In September 2025, 404 Media reported that ICE had [bought access to a Penlink tool](https://www.404media.co/ice-to-buy-tool-that-tracks-locations-of-hundreds-of-millions-of-phones-every-day/) updated daily with location data from "hundreds of millions of mobile phones," and in January 2026 it described that tool, [Webloc](https://www.404media.co/inside-ices-tool-to-monitor-phones-in-entire-neighborhoods/).

## What are DHS and the FBI still withholding?

The DHS release covers five legal memos written from 2018 to 2022. Only six of its 93 pages carry any text: the first page of each memo, plus a second page of a 2021 Privacy Act memo. The other 87 carry the "(b)(5)" stamp and a Bates number.

The surviving text sketches what the department's lawyers were asked. A Nov. 16, 2018 memo from General Counsel John M. Mitnick to the secretary says "DHS senior leadership asked the Office of the General Counsel (OGC) what legal authorities permit DHS to access social media websites in order to conduct intelligence collection on domestic threats associated with ideologically motivated violence" ([p. 1](/blog/dhs-phone-location-data-legal-opinion-foia/docs/dhs-ogc-social-media-domestic-threats-memo-2018-11-16.pdf#page=1)). A March 1, 2019 overview says components "may (and, in many cases, do) rely on these authorities" ([p. 1](/blog/dhs-phone-location-data-legal-opinion-foia/docs/dhs-ogc-social-media-legal-authorities-2019-03-01.pdf#page=1)). An April 7, 2022 memo from General Counsel Jonathan E. Meyer, titled "Constitutional and Statutory Restrictions on Open Source Intelligence Activities," is withheld below its subject line ([p. 1](/blog/dhs-phone-location-data-legal-opinion-foia/docs/dhs-ogc-osint-restrictions-memo-2022-04-07.pdf#page=1)).

The most legible pages are in the Dec. 6, 2021 memo to the Science and Technology Directorate's privacy officer. It quotes the Privacy Act's ban on keeping records of how people exercise First Amendment rights and concludes: "Unless S&T can avail itself of one of the aforementioned exceptions to subsection (e)(7) of the Privacy Act, S&T may not independently collect or maintain records that contain First Amendment Information" ([p. 2](/blog/dhs-phone-location-data-legal-opinion-foia/docs/dhs-ogc-privacy-act-e7-st-memo-2021-12-06.pdf#page=2)). Presence at a protest, a mosque or a union hall is the kind of thing location data can record. Whether DHS lawyers applied that limit to the location data the department was buying is one of the questions the withheld pages could answer.

{{MODULE:fig-foia-st}}

The FBI file is redacted differently. Its statement of work is marked "SECRET//NOFORN" with a declassification date of Dec. 31, 2045 ([p. 6](/blog/dhs-phone-location-data-legal-opinion-foia/docs/fbi-foipa-1491075-000-venntel-portal-contract.pdf#page=6)), and the background and objectives paragraphs, the reasons the bureau wanted the data, are blacked out under national-security and law-enforcement exemptions. The bureau's own cover sheet lists 13 pages deleted in full ([p. 1](/blog/dhs-phone-location-data-legal-opinion-foia/docs/fbi-foipa-1491075-000-venntel-portal-contract.pdf#page=1)). Yet a checklist near the end answers "Is this a classified acquisition?" with "No" ([p. 32](/blog/dhs-phone-location-data-legal-opinion-foia/docs/fbi-foipa-1491075-000-venntel-portal-contract.pdf#page=32)). The purchase is unclassified; the reason for it is classified.

ICE's thinking is a little more visible. In January 2026 the ACLU published a [two-page ICE legal memo](https://www.aclu.org/news/privacy-technology/dhs-is-circumventing-constitution-by-buying-data-it-would-normally-need-a-warrant-to-access) that, it said, tries to distinguish purchased data from the records in *Carpenter* because it is tied to advertising IDs "instead of to phone numbers or names." That memo, too, is heavily redacted.

NOTE: Only the opinion's first page is public, so this report does not characterize its conclusions. A FOIA requester may challenge (b)(5) withholdings in an administrative appeal and, after that, in court.

## Is buying the data legal without a warrant?

In *[Carpenter v. United States](https://www.supremecourt.gov/opinions/17pdf/16-402_h315.pdf)* (2018), the Supreme Court held that the government generally needs a warrant to compel a wireless carrier to hand over a customer's historical cell-site location records. "When the Government tracks the location of a cell phone it achieves near perfect surveillance, as if it had attached an ankle monitor to the phone's user," Chief Justice John Roberts wrote ([PDF p. 17](https://www.supremecourt.gov/opinions/17pdf/16-402_h315.pdf#page=17)). He also wrote: "Our decision today is a narrow one" ([PDF p. 21](https://www.supremecourt.gov/opinions/17pdf/16-402_h315.pdf#page=21)).

The narrowness is about what the court left alone. For decades, under the so-called third-party doctrine, the government could get bank and phone-company records without a warrant because customers had handed that information to a business. *Carpenter* declined to apply that rule to a carrier's location records, but it said nothing about data a company sells on the open market, or about a buyer that never compels anyone to produce anything. That gap is where the purchases sit.

Agencies have read that narrowness as room to buy. In a January 2021 response to questions from Sen. Ron Wyden, D-Ore., the Defense Intelligence Agency wrote that it "[does not construe the Carpenter decision to require a judicial warrant endorsing purchase or use of commercially-available data for intelligence purposes](https://www.wyden.senate.gov/imo/media/doc/011521%20CTD%20Discussion%20RFI%20Response.pdf)." The ICE memo the ACLU published rests on the advertising-ID distinction. DHS's own 2020 analysis of the same question is the one withheld.

The intelligence community's outside advisers were less comfortable. The 2022 report to the director of national intelligence observed that "the same type of information on millions of Americans is openly for sale to the general public," and warned that "the government would never have been permitted to compel billions of people to carry location tracking devices on their persons at all times" ([ODNI report](https://www.dni.gov/files/ODNI/documents/assessments/ODNI-Declassified-Report-on-CAI-January2022.pdf)). In May 2024 the office issued a [framework](https://www.dni.gov/files/ODNI/documents/CAI/Commercially-Available-Information-Framework-May2024.pdf) for how agencies should handle such data. It sets rules for handling; it does not ban purchases.

Congress has come close. On April 17, 2024, the House passed the Fourth Amendment Is Not For Sale Act, [H.R. 4639](https://www.congress.gov/bill/118th-congress/house-bill/4639), by [219 to 199](https://clerk.house.gov/Votes/2024136). The bill would bar law-enforcement and intelligence agencies from buying certain data about Americans that would otherwise require a court order. The Senate did not take it up, and it died with the 118th Congress.

## Why hasn't oversight stopped it?

Because each layer of the trade answers to a different rulebook, and the buying agency's rulebook is mostly procurement.

The supply chain is built in layers. App makers and ad exchanges sell to aggregators. Aggregators license to brokers. Brokers sell subscriptions through resellers that already hold government contract vehicles, as GovPlace did for the FBI. At the end, an agency is buying access to a commercial web portal that charges per seat and per query. That looks like software, not surveillance, and it moves through contracting offices rather than courts. Each company in the chain can say it never sold anything to the government directly, and each agency can say it bought only what any customer could.

The vendors' terms reinforce the distance. Babel Street's Locate X terms, as reported by Protocol in 2020 and [summarized by Inverse](https://www.inverse.com/input/tech/cbp-ice-the-secret-service-are-reportedly-locate-x-to-track-people-through-their-apps), said the tool was "used for internal research purposes only" and that its data "may not be used as the basis for any legal process in any country, including as the basis for a warrant or subpoena." Data that never appears in court is never tested in court.

The internal checks found the gaps and could not close them. The inspector general reported that CBP, ICE and the Secret Service "[did not adhere to Department privacy policies](https://www.oig.dhs.gov/sites/default/files/assets/2023-09/OIG-23-61-Sep23-Redacted.pdf#page=4)" before buying and using the data, and that one CBP employee used the data "inappropriately to track coworkers" ([OIG-23-61, PDF p. 18](https://www.oig.dhs.gov/sites/default/files/assets/2023-09/OIG-23-61-Sep23-Redacted.pdf#page=18)). The Secret Service "did not believe CTD-specific policies and procedures were needed" ([PDF p. 10](https://www.oig.dhs.gov/sites/default/files/assets/2023-09/OIG-23-61-Sep23-Redacted.pdf#page=10)). When the inspector general recommended that ICE stop using the data until its privacy impact assessments were approved, DHS replied: "Non-concur. CTD is an important mission contributor to the ICE investigative process" ([PDF p. 21](https://www.oig.dhs.gov/sites/default/files/assets/2023-09/OIG-23-61-Sep23-Redacted.pdf#page=21)).

Other watchdogs carved the purchases out of their own scope. The FTC's Gravy order bans selling sensitive location data but makes an exception for [limited national-security and law-enforcement uses](https://www.ftc.gov/news-events/news/press-releases/2024/12/ftc-takes-action-against-gravy-analytics-venntel-unlawfully-selling-location-data-tracking-consumers). The ODNI report defined commercially available information to exclude data "available exclusively to governments." At the Pentagon, the Government Accountability Office found in February 2024 that an intelligence-oversight review of "collateral telemetry data" was "[still in draft pending further site visits](https://www.gao.gov/products/gao-24-106190)."

Members of Congress have tried letters. In June 2020, lawmakers including Wyden and Sen. Elizabeth Warren, D-Mass., opened a [bicameral inquiry into Venntel](https://oversightdemocrats.house.gov/news/press-releases/members-launch-bicameral-investigation-into-company-tracking-collecting-and). In January 2024 Wyden released documents showing the National Security Agency [buys Americans' internet records](https://www.wyden.senate.gov/news/press-releases/wyden-releases-documents-confirming-the-nsa-buys-americans-internet-browsing-records-calls-on-intelligence-community-to-stop-buying-us-data-obtained-unlawfully-from-data-brokers-violating-recent-ftc-order) from brokers. Neither stopped the market.

{{MODULE:timeline}}

## Who else uses it, including America's adversaries?

The military and intelligence agencies buy too, and for longer. The GAO wrote that "collateral telemetry data" is "a consensus term developed by the Intelligence Community to standardize reference to commercially available datasets," including advertising and bidstream data ([GAO-24-106190](https://www.gao.gov/products/gao-24-106190)). Wired, drawing on reporter Byron Tau's book, described a contractor tool called Locomotive, later renamed VISR, that "would be shared widely inside the US intelligence community as a [tool to generate leads](https://www.wired.com/story/how-pentagon-learned-targeted-ads-to-find-targets-and-vladimir-putin/)."

The same story described the risk. In 2016, contractors testing the data saw phones move from Fort Bragg and MacDill Air Force Base through third countries to an abandoned cement factory in northern Syria, where U.S. special operators were then based at an unannounced site. The data that could find adversaries could find Americans.

By 2026 that warning had come true. In a May 28, 2026 letter, Wyden, Rep. Pat Harrigan, R-N.C., and 12 other lawmakers wrote that Central Command had told Congress it "[received multiple threat reports concerning adversary exploitation of commercial location data to target or surveil U.S. personnel in theater](https://www.wyden.senate.gov/imo/media/doc/wyden_led_letter_to_dod_cio_kirsten_adavies.pdf)." They added that CENTCOM "confirmed that the advertising ID is still not disabled on government-issued smartphones." The command's [written responses](https://www.wyden.senate.gov/imo/media/doc/unclassified_responses_to_sen_wyden_rfis_on_mobile_phone_use_in_centcom_aor.pdf) describe its restrictions on geolocation features. In July, TechCrunch, citing the Financial Times, reported that [Iran-linked actors](https://techcrunch.com/2026/07/14/iran-abused-mobile-networks-vulnerabilities-to-locate-u-s-military-in-the-middle-east-report-says/) had used advertising data and phone-network weaknesses to locate U.S. troops in the region.

Europe is exposed too. In November 2024, Wired and its reporting partners analyzed location data obtained from one U.S. broker and found "granular location data from up to [12,313 devices](https://www.wired.com/story/phone-data-us-soldiers-spies-nuclear-germany/) that appeared to spend time at or near at least 11 military and intelligence sites" in Germany.

NOTE: OctoProbe excluded intelligence-community operational details it could not source to public records, and does not publish methods for re-identifying individuals from location data.

## What happens next?

The trade is moving, not ending. Brokers have rebranded and changed owners since the first contracts surfaced; Venntel's parent, Gravy Analytics, is now part of Unacast, and the FTC's order restricts what Gravy and Venntel may sell. ICE has returned to the market through Penlink. The inspector general's recommendations for DHS-wide rules remain a test of whether the department's privacy office can say no. In the 2026 letter, lawmakers urged the Pentagon to disable the advertising ID on every government-issued phone. And the House-passed warrant requirement would have to start over in a new Congress.

The cheapest step is the one DHS controls. Agencies regularly release legal guidance that sets policy for their own staff; courts have treated such final, operative guidance as harder to withhold than a draft. Whether the 2020 opinion functioned that way is unknown, because DHS has not said how, or whether, components relied on it. Its general counsel has already written the analysis. Releasing it would tell the public what the department believes the Constitution allows it to buy.

For phone owners, the practical defenses are modest but real. On an iPhone, declining app tracking requests returns a blank advertising identifier. On Android, the advertising ID can be deleted in the privacy settings. Granting location only while an app is in use, and only to apps that need it, cuts off the kits that read GPS in the background. None of those settings reaches data already sold.

## Primary documents

The five DHS records below are posted exactly as received, byte for byte; the FBI file is a searchable copy of the bureau's public release. Page links open the PDF at the cited page. The explorer shows which pages were released and which were withheld.

{{MODULE:foia}}

{{MODULE:docs-table}}

NOTE: The five DHS files are posted unaltered as received; they are image PDFs with a text layer produced by DHS. The FBI file is a searchable copy of the bureau's 33-page [FBI Vault release](https://vault.fbi.gov/contract-with-venntel), re-imaged with an added text layer; page order and numbering match the Vault PDF, so page citations work in either. SHA-256 checksums for the hosted files are listed in the [SHA256SUMS file](/blog/dhs-phone-location-data-legal-opinion-foia/docs/SHA256SUMS.txt).

## What terms should FOIA requesters use?

Agencies describe the same data in different words. A request that names only one term can miss records filed under another.

{{MODULE:glossary}}

A thorough request lists the variants: "commercial telemetry data," "collateral telemetry data," "CTD," "commercially available information," "advertising identifier," "AdID," "MAID," "IDFA," "AAID," "GAID," "bidstream," "geofence" and "area search," plus vendor and product names such as Venntel, Locate X, Fog Reveal and Webloc.

{{FAQ}}

{{AUTHOR_NOTE}}

{{MODULE:related}}

## Disclaimer

This report relies on public records, FOIA releases, court opinions, government reports and published journalism. Interactive figures use generated data and fictional places. It does not accuse any named person of wrongdoing beyond what official findings state. OctoProbe is not a consumer reporting agency, and nothing here may be used for FCRA-covered eligibility decisions.
