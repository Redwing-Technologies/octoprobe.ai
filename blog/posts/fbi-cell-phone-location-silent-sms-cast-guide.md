---
title: "Inside the FBI's CAST Guide: How Carriers and Agents Pin Down a Cell Phone"
og_title: "Silent Texts, No-Ring Calls and Tower Math: How the FBI Finds a Phone"
seo_title: "How Police Find a Phone: Silent SMS and the FBI Guide"
dek: "A 2019 FBI field guide, a public NDCAC briefing and an FCC order show how a phone can be made to reveal where it is, how precise the answer is, and where the law steps in."
description: "An FBI field guide shows how police make a phone reveal its location with silent texts, pings and tower timing, how precise it gets, and what the law requires."
date: 2026-10-20T17:55:59-04:00
date_modified: 2026-10-22T08:09:04-04:00
slug: fbi-cell-phone-location-silent-sms-cast-guide
canonical: https://www.octoprobe.ai/blog/fbi-cell-phone-location-silent-sms-cast-guide/
section: Investigations
tags: [Investigations, Surveillance, Cell Phones, FBI, Privacy Law]
keywords: [silent SMS, Type 0 SMS, stealth ping, cell phone ping, FBI CAST, Cellular Analysis Survey Team, cell site location information, CSLI, Carpenter v. United States, timing advance, PCMD, NELOS, tower dump, E911 Phase II, NDCAC, CALEA]
og_image: https://www.octoprobe.ai/blog/fbi-cell-phone-location-silent-sms-cast-guide/assets/og-cover.png?v=1
hero_alt: "Illustration: three cell towers on a stylized street grid, each casting a 120-degree sector and a range band that overlap around a red phone dot"
byline: Colin Aamot
author: Colin Aamot
primary_question: How do police and the FBI locate a cell phone, and what legal rules apply?
answer_first: A phone tells its carrier where it is every time the network reaches it, and investigators can trigger that on demand with an invisible "silent" message, a call that never rings or a carrier "ping." The answer can be as rough as a tower sector or as tight as a GPS fix. Historical records generally need a warrant under *Carpenter v. United States*; real-time pinging is a separate, unsettled category.
faq:
  - q: What is a silent SMS, or Type 0 SMS?
    a: It is a text message the phone is required to acknowledge but not show. The 3GPP standard for text messaging says that for a "short message type 0," the phone "shall acknowledge receipt of the short message to the SC but shall discard its contents," "shall not indicate the receipt of the type 0 short message to the user," and stores it nowhere. The acknowledgment travels over the network, which is why the message produces records of where the phone is connected.
  - q: Can police ping a phone without the owner knowing?
    a: Yes, with the carrier's help. A 2019 FBI field guide describes a Sprint location service in which "a silent message is sent to the phone requesting a location update," and says that on U.S. Cellular "you can force a call without a ring to the target device to determine tower/sector." In Germany, the federal government reported that the Federal Criminal Police Office registered 37,064 silent texts in the first half of 2022 alone.
  - q: How accurate is cell-tower location?
    a: It ranges from a few dozen meters to several kilometers. A single tower and sector covers a wedge of roughly 120 degrees. Round-trip timing adds a distance band, and readings from three or more towers can narrow it further. A GPS-based ping can be much tighter. The FBI guide warns that some carrier coordinates are "NOT GPS-based," and the FBI's cell team "does not testify to the accuracy" of AT&T's NELOS records.
  - q: Do police need a warrant to get cell-phone location data?
    a: For historical cell-site records, generally yes. A court order under 18 U.S.C. § 2703(d) needs only "specific and articulable facts" showing the records are "relevant and material" to an investigation, but in *Carpenter v. United States* (2018) the Supreme Court held that such an order "is not a permissible mechanism for accessing historical cell-site records" and told the government to "get a warrant," which requires probable cause. The Court left "real-time CSLI or 'tower dumps'" undecided, so rules for real-time pinging vary by court and state, and emergencies can justify going without a warrant.
  - q: What is the FBI's CAST team?
    a: CAST, the Cellular Analysis Survey Team, is the FBI unit that analyzes phone records and tower data for the bureau and for state, local and tribal agencies. Its 2019 guide lists 5 headquarters supervisors, 15 "National Assets" and more than 50 certified "Field Assets," and the FBI offers free CAST training in its CASTViz mapping software.
---

{{MODULE:cover}}

{{ANSWER}}

{{MODULE:takeaways}}

Your phone is not hiding from the cell network. To deliver a call or a text, the network has to find it, and every time it does, the phone checks in through a particular antenna on a particular tower. Carriers record those check-ins. Investigators can read them later or, with the right paperwork, cause new ones on demand.

How that works, in the government's own words, is laid out in three public documents. The first is a 139-page FBI field guide from 2019. The second is a 2018 briefing from the Justice Department's National Domestic Communications Assistance Center (NDCAC). The third is the 2005 Federal Communications Commission order that extended federal wiretap-assistance rules to broadband. All three are posted below, with page images of the key passages.

## The documents

The FBI guide is the "Cellular Analysis & Geo-Location Field Resource Guide," produced by the bureau's Cellular Analysis Survey Team and marked "Current as of March 2019." The nonprofit Property of the People obtained it under the Freedom of Information Act, and [Motherboard reported on it](https://www.vice.com/en/article/how-fbi-gets-phone-data-att-tmobile-verizon/) in October 2021. It is a training deck: how towers work, what each carrier keeps and for how long, what legal process to use, and how to plot records on a map.


The [CAST mission](/blog/fbi-cell-phone-location-silent-sms-cast-guide/docs/fbi-cast-cellular-analysis-geolocation-field-resource-guide-2019-redacted.pdf#page=5), per the guide, "is to support FBI, along with state, local, and tribal investigations through the analysis of cellular call detail records (CDRs) and their associated tower information." Its listed priorities are, in order, "An immediate threat to life," FBI priorities "to include National Security, Criminal, and Cyber," and "Assistance to state, local, and other federal agencies." The program had 5 headquarters supervisors, 15 "National Assets" embedded in field offices, and "over 50 CAST certified 'Field Assets'" who work cases in their own offices. The FBI still advertises [free CAST training](https://forms.fbi.gov/cast-basic-cell-site-analysis) for police, where students install "the FBI provided mapping software CASTViz."

{{MODULE:fig-cast-mission}}

The NDCAC briefing is a 14-slide "Program Update" presented by then-Director Marybeth Paglino to the center's Executive Advisory Board on April 11, 2018, at a meeting [announced in the Federal Register](https://www.federalregister.gov/documents/2018/03/23/2018-05968/meeting-of-the-ndcac-executive-advisory-board) as open to the public. NDCAC posts it on its own public site, at [ndcac.fbi.gov](https://ndcac.fbi.gov/file-repository/ndcac-director-eab-briefing-april-2018.pdf).

The FCC order is [FCC 05-153](https://www.federalregister.gov/documents/2005/10/13/05-20606/communications-assistance-for-law-enforcement-act-and-broadband-access-and-services), adopted Aug. 5, 2005, which applied the Communications Assistance for Law Enforcement Act (CALEA) to broadband and internet phone providers.

{{MODULE:docs}}

NOTE: The FBI guide's pages carry the handling marking "UNCLASSIFIED//LES." OctoProbe removed it from the page images in this article; it remains in the hosted PDF as released. In the hosted PDF, OctoProbe redacted a special agent's name on page 14 and telephone numbers, an MSISDN and IMSI/IMEI columns in sample carrier records on pages 95, 111, 112 and 128. Those five pages are replaced with redacted images; every other page is as released. The NDCAC briefing is byte-identical to the copy on ndcac.fbi.gov. The FCC order is byte-identical to the copy NDCAC hosts at ndcac.fbi.gov/file-repository/34.pdf. Checksums are in the [SHA256SUMS file](/blog/fbi-cell-phone-location-silent-sms-cast-guide/docs/SHA256SUMS.txt).

## How a phone gives away where it is

A switched-on phone is always listening. The FBI guide puts it plainly: "A cellular phone is regularly surveying the Radio Frequency (RF) environment of the cellular provider to identify the cell tower and sector with the BEST RF Signal." The phone keeps a running list of neighboring sectors and their signal strengths, and it camps on the strongest one.

{{MODULE:fig-rf-survey}}

Each tower is usually split into sectors, and each sector has its own identifier. According to the guide, a typical "3-sector tower" transmits "through 3 separate sectors each covering approximately 120 degrees," and each base station's Global Cell ID "is unique on the network and not duplicated (like a fingerprint)." When the phone does something on the network, the carrier writes it down: "When a cell phone connects to a tower to conduct an outgoing call or receive an incoming call, the phone company (provider) maintains a record of that EVENT in the Call Detail Records."

{{MODULE:fig-sectors}}

{{MODULE:fig-cell-id}}

So the basic unit of cell-site location information (CSLI) is a time stamp, a tower and a sector: a pie wedge, not a point. Everything else in the guide is about making that wedge smaller or making the phone produce more of them.

## Making a phone talk: silent texts and calls that never ring

A phone that sits idle produces few records. One that's told to answer produces them on command.

The best-known trigger is the "silent SMS." The 3GPP standard for text messaging, [TS 23.040](https://www.3gpp.org/DynaReport/23040.htm), defines a "Short Message Type 0" in its protocol-identifier field. The standard's conformance requirement, as quoted in a [3GPP test specification change](https://www.3gpp.org/ftp/tsg_t/TSG_T/TSGT_16/Docs/PDFs/TP-020164.pdf), reads: "When a mobile terminated message is type 0, the UE shall acknowledge receipt of the short message to the SC but shall discard its contents." The phone "shall not indicate the receipt of the type 0 short message to the user," and "the short message shall neither be stored in the (U)SIM nor ME."

In other words, the phone must answer but must not tell its owner. To deliver the message, the network first has to find the handset; the 3GPP test sequence for a Type 0 message begins with the phone's "PAGING RESPONSE." That round trip happens over a specific cell, and it leaves the same kind of network record a real text would.

NOTE: 3GPP specifications are revised by release; the Type 0 language quoted here is from the conformance test text, which cites "3GPP TS 23.040, 9.2.3.9" as its reference. Logging of Type 0 deliveries by any particular carrier was not tested.

The FBI guide doesn't use the term "Type 0," but it describes the same idea in carrier products. On Sprint's GPS "Ping," the guide says: "A Ping is conducted with the assistance of the cellular provider. A silent message is sent to the phone requesting a location update. The phone uses its own GPS receiver and reports its location."

{{MODULE:fig-silent-message}}

For a carrier without that service, the guide offers a cruder trigger. Its provider table says of U.S. Cellular: "No. However, you can force a call without a ring to the target device to determine tower/sector." The retention chart repeats it under real-time ("Prospective") tools: "No, but force 'no ring' call."

{{MODULE:fig-no-ring}}

And for T-Mobile, the guide supplies the wording to put in a court order or warrant: "Such service provider shall initiate a signal to determine the location of the subject's mobile device on the service provider's network or with such other reference points as may be reasonably available and at such intervals and times as directed by the law enforcement agent serving this order."

{{MODULE:fig-initiate-signal}}

Anything that makes the network reach the phone (a call, a text of any kind, a data session) can produce a location record. The guide's retention chart lists separate "Cell Site (Voice)," "Cell Site (SMS)" and "Cell Site (Data)" records for each carrier. A silent text or no-ring call just does it without the owner seeing anything.

App push notifications are a different category. Sen. Ron Wyden [wrote in December 2023](https://www.wyden.senate.gov/imo/media/doc/wyden_smartphone_push_notification_surveillance_letter.pdf) that governments had sought push records from Apple and Google, which hold metadata "detailing which app received a notification and when, as well as the phone and associated Apple or Google account to which that notification was intended to be delivered." That is account data at a tech company, not tower data at a carrier.

Germany is one of the few places that counts silent texts publicly. In a [March 2023 answer to lawmakers](https://dserver.bundestag.de/btd/20/062/2006233.pdf), the federal government reported that the Federal Criminal Police Office (BKA) registered 37,064 "Stille SMS" in the first half of 2022 and 14,886 in the second. The Federal Police sent 12,475 and 7,228, plus 457 and 903 through outside firms. Figures for the domestic intelligence service and customs were classified "VS – Geheim." The government cited a Federal Court of Justice ruling placing the practice under section 100i of the criminal procedure code.

## From a wedge to a dot: timing, triangulation and exclusion

A sector wedge can cover miles. Three techniques shrink it.

**Distance from the tower.** Carriers measure how long a signal takes to make the round trip. The guide's explanation of Sprint's Per Call Measurement Data (PCMD): "By using the data transfer rate between the cellular device and the tower, the cellular provider can approximate the signal distance between the tower and the cellular device using a Round Trip Delay measurement from the tower." Verizon's version, the Real Time Tool, provides "sector/tower and distance from tower with confidence rating." T-Mobile's is called True Call. The output is an arc: a band at a certain distance inside the wedge.

{{MODULE:fig-pcmd}}

**Multiple towers.** Measuring the same signal at several towers gives intersecting arcs. The guide's slide on T-Mobile's E-911 Locator and AT&T's Mobile Locator says: "TOA positioning method is based on measuring the Time of Arrival (TOA) or (Timing Advance) of a known signal sent from the cell phone and received at three or more measurement units (towers)." Its provider table describes T-Mobile's version as "3 to 6 tower triangulation." The sample response on the slide gives a latitude, a longitude and "Uncertainty 443 m."

{{MODULE:fig-triangulation}}

**The phone's own GPS.** The Sprint ping asks the handset for a satellite fix, which the guide says depends "upon the phone interacting with a minimum of 4 satellites (3 without altitude)." For 911 calls, federal rules set the bar: handset-based systems must deliver "[50 meters for 67 percent of calls, and 150 meters for 80 percent of calls](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-9/subpart-C/section-9.10)," on a per-county or per-PSAP basis.

The narrowing works by exclusion. The phone is in this sector, not the other two. It is about 0.8 miles out, not 0.2 or 2. Three towers' arcs overlap here and nowhere else. Investigators apply the same logic across many phones with "tower dumps," lists of every device that used a site during a window. The guide suggests narrowing a [tower dump](/blog/fbi-cell-phone-location-silent-sms-cast-guide/docs/fbi-cast-cellular-analysis-geolocation-field-resource-guide-2019-redacted.pdf#page=60) "based on knowledge (outgoing call only, 3 minute conversation, not in area after crime, etc.)"

{{MODULE:fig-tower-dumps}}

Even a failed ping says something. The guide's list of T-Mobile locator responses includes "[Absent_Subscriber] – phone is not on the network" and "[Position_Method_ Failure] – phone is powered off or has moved into an area where switch is not provisioned," with the note: "If you see this – it may come back on."

{{MODULE:fig-e911-responses}}

AT&T's historical tool, NELOS, grades each location record on a 14-step scale, from "Location accuracy likely better than 25 meters" for GPS-derived events to "better than 25000 meters" for tower-and-sector-only records. Its timing records cover cases where "low propagation delay indicates very near presence to a particular cell tower (within 200M)."

{{MODULE:fig-nelos}}

## Real-time pinging and historical records are different things

The guide separates two kinds of data, and the law increasingly does too.

**Historical records** already exist in the carrier's files: call detail records with cell sites, tower dumps, and engineering data such as PCMD, RTT, True Call and NELOS. The March 2019 retention chart shows AT&T keeping call records, cell sites and tower dumps for "7 years," T-Mobile for "2 years," Sprint for "18 months," and Verizon for "1 year." Engineering data is short-lived: Verizon RTT "8 days," Sprint PCMD "~90 days SMS & voice; 2 weeks data," AT&T NELOS "90 days."

**Real-time ("prospective") location** is generated on request: AT&T's "Mobile Locate (Triangulation / AGPS)," T-Mobile's "E911 (Triangulation)," Sprint's "GPS 'Ping' (device dependent)," and, for U.S. Cellular, the no-ring call. Verizon RTT, the guide says, is "provided to law enforcement during exigent circumstances or if requested in a legal document."

{{MODULE:fig-retention}}

{{MODULE:fig-rtt}}

Retention figures are as of March 2019. Sprint has since merged into T-Mobile, and carriers' practices may have changed.

## What the law requires

Two kinds of court paper come up again and again in the FBI guide: a court order under 18 U.S.C. § 2703(d) and a search warrant. They are not interchangeable, and the difference decides which phone records police can get.

### A 2703(d) order vs. a search warrant

The Stored Communications Act lets the government require a carrier to hand over customer records "(not including the contents of communications)" when it "obtains a warrant issued using the procedures described in the Federal Rules of Criminal Procedure" or "obtains a court order for such disclosure under subsection (d) of this section," [according to § 2703(c)](https://www.law.cornell.edu/uscode/text/18/2703).

The two routes have different bars. A [§ 2703(d) order](https://www.law.cornell.edu/uscode/text/18/2703) "shall issue only if the governmental entity offers specific and articulable facts showing that there are reasonable grounds to believe that the contents of a wire or electronic communication, or the records or other information sought, are relevant and material to an ongoing criminal investigation." A federal warrant under [Rule 41(d)(1)](https://www.uscourts.gov/sites/default/files/2025-02/federal-rules-of-criminal-procedure-dec-1-2024_0.pdf#page=75) is different: a judge "must issue the warrant if there is probable cause to search for and seize a person or property or to install and use a tracking device."

| | § 2703(d) court order | Rule 41 search warrant |
|---|---|---|
| Standard | "Specific and articulable facts" showing "reasonable grounds to believe" the records are "relevant and material" to an investigation | "Probable cause" |
| What it authorizes | Disclosure of stored provider records | A search or seizure, including installing and using a tracking device |
| Content or non-content | Mainly non-content records: subscriber details, call logs, cell sites | Content and non-content |
| Typical cell-phone use, per the 2019 FBI guide | Historical call detail records, offered as "2703(d) or search warrant" | Text-message content, which one carrier page marks "Requires a Search Warrant" |

NOTE: The last row reflects the FBI guide's carrier-specific request language ([pp. 10, 14](/blog/fbi-cell-phone-location-silent-sms-cast-guide/docs/fbi-cast-cellular-analysis-geolocation-field-resource-guide-2019-redacted.pdf#page=10)). Section 2703(d) orders can also reach some stored content under § 2703(b) with notice to the customer. The guide's general table lists "Text Messaging /Text Content" under "Court Order or Search Warrant," while its carrier pages flag message content as warrant-only.

### What *Carpenter* changed

Before 2018, a § 2703(d) order was the usual way to get historical cell-site records. That is how prosecutors got 12,898 location points on Timothy Carpenter, "an average of 101 data points per day." In [*Carpenter v. United States*](https://www.supremecourt.gov/opinions/17pdf/16-402_h315.pdf), decided in June 2018, the Supreme Court called cell-phone location data "detailed, encyclopedic, and effortlessly compiled," and held "that accessing seven days of CSLI constitutes a Fourth Amendment search."

The Court said the § 2703(d) standard falls short. Under it, "law enforcement need only show that the cell-site evidence might be pertinent to an ongoing investigation—a 'gigantic' departure from the probable cause rule." Its conclusion: "Consequently, an order issued under Section 2703(d) of the Act is not a permissible mechanism for accessing historical cell-site records. Before compelling a wireless carrier to turn over a subscriber's CSLI, the Government's obligation is a familiar one—get a warrant."

### The gaps: tower dumps and real-time location

The Court also said what it was not deciding: "Our decision today is a narrow one. We do not express a view on matters not before us: real-time CSLI or 'tower dumps' (a download of information on all the devices that connected to a particular cell site during a particular interval)." It noted that emergencies, such as the need to "pursue a fleeing suspect," can still justify a warrantless search.

Silent texts, no-ring calls and carrier pings fall in that gap. They don't pull records the carrier already holds; they make the phone produce new location data on the government's request. No Supreme Court ruling settles whether that requires a warrant, and courts and legislatures have answered differently. Massachusetts' highest court took up the question in [*Commonwealth v. Almonor*](https://www.eff.org/files/2019/04/24/mass_supreme_court_opinion-almonor.pdf) (2019), describing the practice this way: "On request, a cellular service provider (service provider) can cause a cell phone to transmit its global positioning system (GPS) coordinates to the provider, in a process known as 'pinging.'" It held under the state constitution that "by causing the defendant's cell phone to reveal its real-time location, the Commonwealth intruded on the defendant's reasonable expectation of privacy in the real-time location of his cell phone." The court still upheld that ping, which police ran without a warrant, because of the emergency.

Tower dumps sit in the same gap. The FBI guide's section on them gives the "Legal Threshold" as "Need a court order or search warrant" ([p. 60](/blog/fbi-cell-phone-location-silent-sms-cast-guide/docs/fbi-cast-cellular-analysis-geolocation-field-resource-guide-2019-redacted.pdf#page=60)).

### What the 2019 FBI guide tells agents

The FBI guide, "Current as of March 2019," about nine months after *Carpenter*, still lists both options for historical records: "Court order 2703(d) or search warrant for historical call detail and cell site. Refer to the AUSA for the most current court requirement." It adds: "Court order 2703(d) & 3123 hybrid order for pen register to also get historical records may require a search warrant," and advises agents to "discuss with your local AUSA and determine what method (2703(d) or search warrant) should be pursued." Its general table, headed "Varies by Judicial District," puts "Ping data (Sprint)," "E-911 (T-Mobile & AT&T)" and "Location Based Services" under "Court Order or Search Warrant."

{{MODULE:fig-legal}}

There is also an emergency route. Under 18 U.S.C. § 2702(c)(4), a carrier "may divulge a record or other information" to the government if it "in good faith, believes that an emergency involving danger of death or serious physical injury to any person requires disclosure without delay." The guide notes that "Providers have the discretion to refuse or except [sic] these requests" and that FBI personnel need assistant special agent in charge approval.

{{MODULE:fig-exigent}}

One more limit is written into CALEA itself. For information acquired "solely pursuant to the authority for pen registers and trap and trace devices," call-identifying information "shall not include any information that may disclose the physical location of the subscriber (except to the extent that the location may be determined from the telephone number)," [under 47 U.S.C. § 1002](https://www.law.cornell.edu/uscode/text/47/1002). A pen-register order alone is not supposed to deliver location.

## Why a tower hit isn't proof

A phone that connected to a tower near a crime scene was somewhere in that tower's coverage, which in a city can include thousands of people and in the country can stretch for miles. Towers are everywhere; a connection to one is not evidence of anything by itself.

The guide is candid about this. Its first content page warns: "Cell analysis is a great investigative tool. However, testifying in court regarding cell phone records is difficult and requires significant training. Prior to testifying, CAST agents receive over 500 hours of training." CAST uses "drive test equipment to determine the true geographical coverage breadth of a cell site sector," because a sector's real reach depends on terrain and buildings.

{{MODULE:fig-disclaimer}}

{{MODULE:fig-cast-origin}}

Several data sources come with explicit cautions. On PCMD: "Lat/Long coordinates are NOT GPS-based. The distance from tower information is generally more accurate." On NELOS: "Use cautiously. AT&T does not validate results," and "CAST currently does not testify to the accuracy to NELOS." On a T-Mobile switch list that maps record codes to cities: "NOT TO BE INTERPRETED AS THE LOCATION OF THE DEVICE."

{{MODULE:fig-switch-pooling}}

## The plumbing: NDCAC and CALEA

Most police departments don't have a CAST agent. That is part of why NDCAC exists. The Justice Department center helps state and local agencies with the technical side of electronic evidence and surveillance. Its April 2018 update said its Technical Resource Group served "more that [sic] 14,600" law-enforcement clients and handled 3,497 requests in six months. Among the "Types of calls handled": "Interpretation of provider call detail records / cell tower information" and "Assistance with legal demand (templates)." The center's 2018 budget was $10,987,055.

{{MODULE:fig-ndcac-trg}}

The FBI guide points readers to NDCAC's restricted portal for a "Database of current and archived tower lists for all major" carriers, the reference data needed to turn a cell ID into a map location.

The legal foundation is CALEA. "Congress enacted CALEA on October 25, 1994," the FCC's 2005 order explains, "in response to concerns that emerging technologies such as digital and wireless communications were making it increasingly difficult for law enforcement agencies to execute authorized surveillance." The law requires carriers to build their networks so they can deliver intercepts and call-identifying information under court order.

{{MODULE:fig-fcc-para4}}

The 2005 order extended that duty: "In this Order, we conclude that the Communications Assistance for Law Enforcement Act (CALEA) applies to facilities-based broadband Internet access providers and providers of interconnected voice over Internet Protocol (VoIP) service." It responded to a 2004 petition from the Justice Department, the FBI and the Drug Enforcement Administration, and gave newly covered providers 18 months to comply.

{{MODULE:fig-fcc-para1}}

NOTE: Download the documents: the [FBI CAST field guide (redacted as described above)](/blog/fbi-cell-phone-location-silent-sms-cast-guide/docs/fbi-cast-cellular-analysis-geolocation-field-resource-guide-2019-redacted.pdf), the [NDCAC April 2018 program update](/blog/fbi-cell-phone-location-silent-sms-cast-guide/docs/ndcac-director-eab-briefing-april-2018.pdf) and [FCC 05-153](/blog/fbi-cell-phone-location-silent-sms-cast-guide/docs/fcc-05-153-calea-broadband-first-report-and-order-2005.pdf). Figures in the guide reflect carrier practices as of 2018 and 2019.

{{FAQ}}

## Disclaimer

This article describes government documents and published law for public understanding. It is not legal advice.

{{AUTHOR_NOTE}}

{{MODULE:related}}
