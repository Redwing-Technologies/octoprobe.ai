#!/usr/bin/env python3
"""Static modules for 'Subpoena, Order, Warrant' (Investigations).
Read by scripts/build-subpoena-ladder-post.py. Standard library only.
Page images in assets/figs/ were rendered from the two hosted FOIA PDFs at 200 dpi, cropped and converted to
grayscale. Redactions are exactly as released; OctoProbe added none and removed none. One figure (the Kik
warrant attachment) joins the top and bottom of a single page and drops the blank space between them, marked
by a dashed rule. Captions link to the page in the hosted PDF.
The three retention-chart figures (s3-*) are rendered in color at 1500 px wide from the FBI CAST field guide
already hosted with the CAST post (pp. 74, 127, 137), cropped at the bottom; the "UNCLASSIFIED//LES" handling
marking at the top of p. 74 is boxed out, as on the CAST post. Their captions link to that hosted copy."""
import re
from html import escape as e
SLUG = "subpoena-warrant-online-accounts-three-branches"
A = f"/blog/{SLUG}/assets/"
F = A + "figs/"
D = f"/blog/{SLUG}/docs/"
HOUSE = D + "house-judiciary-oversight-subpoenas-fbi-2023-foia-release.pdf"
NCIS = D + "ncis-dodig-subpoenas-november-2025-foia-2026-002860.pdf"
CAST = "/blog/fbi-cell-phone-location-silent-sms-cast-guide/docs/fbi-cast-cellular-analysis-geolocation-field-resource-guide-2019-redacted.pdf"
DOCS = {"HOUSE": (HOUSE, "House subpoena file"), "NCIS": (NCIS, "NCIS release"), "CAST": (CAST, "FBI CAST field guide")}
CAST_CREDIT = "FBI Cellular Analysis Survey Team (CAST), provider retention reference, as of March 2019."
MODULES = {}
def w(name, s): MODULES[name] = s

def fig(mid, img, wd, ht, alt, caption, doc, page):
    url, label = DOCS[doc]
    cap = re.sub(r"&(?![A-Za-z0-9#]+;)", "&amp;", caption)
    return (f'<figure class="doc-fig" id="fig-{mid}"><img loading="lazy" decoding="async" src="{F}{img}" width="{wd}" height="{ht}" alt="{e(alt)}">'
            f'<figcaption>{cap} <a href="{url}#page={page}">{label}, p. {page}</a>.</figcaption></figure>\n')

w("cover", f'<figure><img fetchpriority="high" decoding="async" src="{A}cover.png?v=1" width="2400" height="1260" '
  'alt="Three document excerpts on a navy card: a House of Representatives subpoena, a Defense Department inspector general subpoena duces tecum and a search warrant attachment, over a three-step ladder reading subpoena, 2703(d) order, warrant." '
  '><figcaption>Three branches, three kinds of compulsory process. Excerpts from the two FOIA releases discussed below. '
  'Graphic: OctoProbe News.</figcaption></figure>\n')

w("takeaways", '''<aside aria-label="Key takeaways" class="key-takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>Congress, executive agencies and the courts each compel records, under different authority and different limits. No judge signs a congressional or administrative subpoena before it goes out.</li>
<li>A House committee subpoena reaches anything “touching matters of inquiry committed to said committee.” The courts require a valid legislative purpose, and enforcement runs through contempt or a lawsuit.</li>
<li>An inspector general’s subpoena reaches only what its statute allows. Served on Apple, Google, Meta or Snap, it gets the basic subscriber records listed in 18 U.S.C. § 2703(c)(2): name, address, session logs, IP addresses, identifiers, payment.</li>
<li>A § 2703(d) order, signed by a judge, works like a pen register: it shows who talked to whom, when and for how long, not what was said. Message content takes a warrant based on probable cause, and the major platforms say they hand it over only on one.</li>
<li>Retention is often the tighter limit. In the FBI’s carrier retention chart, as of March 2019, call records lasted one to seven years and most carriers kept no text-message content at all; Verizon and U.S. Cellular kept it for days. Most federal crimes can be charged for five years.</li>
<li>One NCIS FOIA release shows all of it in a single month: eight inspector general subpoenas to tech and telecom companies, a military judge’s subpoena, a sealed federal court subpoena and a search warrant attachment for a Kik account.</li>
</ul>
</aside>
''')

def card(href, thumb, tw, th, title, meta, prov):
    return (f'<li class="doc-card"><a class="doc-thumb" href="{href}"><img loading="lazy" decoding="async" src="{F}{thumb}" width="{tw}" height="{th}" alt="First page excerpt of {title} (PDF)"></a>'
            f'<div class="doc-body"><p class="doc-title"><a href="{href}">{title}</a></p><p class="doc-meta">{meta}</p><p class="doc-prov">{prov}</p>'
            f'<p class="doc-actions"><a href="{href}">View PDF</a> · <a href="{href}" download>Download</a></p></div></li>')
w("docs", '<section class="doc-cards" aria-label="Source documents">\n<ul>\n'
  + card(HOUSE, "s1-p01-house-judiciary-subpoena-wray-feb-2023.jpg", 1500, 1476,
         "House Judiciary and Oversight Committee subpoenas to the FBI, 2023",
         "53 pages · seven subpoenas, cover letters, schedules, instructions · scanned PDF, 3.6 MB",
         "Released under FOIA. The file carries no agency cover letter. Hosted as received, without a text layer.") + "\n"
  + card(NCIS, "s2-p01-ncis-foia-release-letter.jpg", 1389, 1856,
         "NCIS FOIA release 2026-002860: ten subpoenas, November 2025",
         "35 pages · release letter dated Feb. 18, 2026 · PDF, 4.2 MB",
         "Released by the Naval Criminal Investigative Service under FOIA. Redactions under (b)(6), (b)(7)(C) and (b)(7)(D) are the agency’s.")
  + '\n</ul>\n</section>\n')

# --- House (Article I) figures ---
w("fig-house-cover", fig("house-cover", "s1-p01-house-judiciary-subpoena-wray-feb-2023.jpg", 1500, 1476,
  "House subpoena form headed By Authority of the House of Representatives of the Congress of the United States of America, addressed to FBI Director Christopher A. Wray, commanding production before the Committee on the Judiciary on March 1, 2023, signed by the chairman and attested by the clerk",
  "The House Judiciary Committee’s February 2023 subpoena to the FBI director. The production box is checked; the deposition and hearing boxes are not.", "HOUSE", 1))
w("fig-house-schedule", fig("house-schedule", "s1-p03-schedule-a-school-board-threats.jpg", 1401, 1085,
  "Schedule A listing five categories of FBI documents about the Attorney General's October 4, 2021 memorandum on threats to school officials and the EDUOFFICIALS threat tag, from January 26, 2021 to present, in unredacted form",
  "Schedule A to the February 2023 subpoena: school-board threat records, “in unredacted form.”", "HOUSE", 3))
w("fig-house-letter", fig("house-letter", "s1-p11-judiciary-letter-april-10-2023.jpg", 1381, 755,
  "April 10, 2023 letter from the House Judiciary Committee to Director Wray about the FBI Richmond Field Office document on Catholic Americans",
  "The cover letter for the April 2023 subpoena.", "HOUSE", 11))
w("fig-house-mazars", fig("house-mazars", "s1-p13-letter-oversight-power-mazars.jpg", 1370, 666,
  "Letter paragraph quoting the Supreme Court on Congress's broad and indispensable power to conduct oversight and listing possible legislative reforms",
  "The legislative-purpose paragraph, citing <em>Trump v. Mazars</em> in its footnote.", "HOUSE", 13))
w("fig-house-richmond", fig("house-richmond", "s1-p16-schedule-a-richmond-catholic-document.jpg", 1346, 1698,
  "Schedule A with seven numbered demands for FBI records about the January 23, 2023 Richmond Field Office Domain Perspective on Radical-Traditionalist Catholic ideology",
  "Schedule A to the April 2023 subpoena.", "HOUSE", 16))
w("fig-house-privileges", fig("house-privileges", "s1-p19-instruction-17-privileges-not-recognized.jpg", 1146, 475,
  "Instruction 17(b) and (c): the Committee does not recognize common-law non-disclosure privileges, FOIA protections or contractual privileges such as non-disclosure agreements",
  "Instruction 17(b) and (c), repeated in each document subpoena’s instructions.", "HOUSE", 19))
w("fig-house-communication", fig("house-communication", "s1-p08-definition-communication-signal-whatsapp.jpg", 1304, 359,
  "Definition of communication covering email, text, instant messages and encrypted apps including Signal, WhatsApp and Telegram, plus Discord, Google Hangouts, Microsoft Teams, Slack, Skype and Viber",
  "The subpoenas’ definition of “communication” names Signal, WhatsApp and Telegram.", "HOUSE", 8))
w("fig-house-comer", fig("house-comer", "s1-p25-oversight-committee-letter-rule-xi.jpg", 1380, 245,
  "Oversight Committee letter stating the subpoena is issued under House Rule XI clause 2(m)(1)(B) and Committee Rule 12(g)",
  "The Oversight Committee chairman cites the House rule that lets him sign subpoenas.", "HOUSE", 25))
w("fig-house-fd1023", fig("house-fd1023", "s1-p28-schedule-fd-1023-forms.jpg", 1384, 398,
  "Schedule to Subpoena demanding all FD-1023 forms created or modified in June 2020 containing the term Biden",
  "The one-item schedule to the Oversight Committee’s May 2023 subpoena.", "HOUSE", 28))
w("fig-house-content", fig("house-content", "s1-p34-schedule-a-content-moderation.jpg", 1328, 984,
  "Schedule A demanding FBI documents and communications about content moderation and misinformation, disinformation or malinformation, from January 1, 2020 to present",
  "Schedule A to the August 2023 subpoena on content moderation.", "HOUSE", 34))
w("fig-house-deposition", fig("house-deposition", "s1-p52-deposition-subpoena-sobocinski.jpg", 1500, 1420,
  "House subpoena to FBI Baltimore Special Agent in Charge Thomas J. Sobocinski with the deposition box checked for September 7, 2023, at 2237 Rayburn House Office Building",
  "A testimony subpoena: the deposition box is checked.", "HOUSE", 52))

# --- NCIS / DoD IG (Article II) figures ---
w("fig-ncis-letter", fig("ncis-letter", "s2-p01-ncis-foia-release-letter.jpg", 1389, 1856,
  "NCIS headquarters letter dated February 18, 2026, tracking number 2026-002860, stating that a search located ten subpoenas responsive to requests for all subpoenas issued in November 2025",
  "The NCIS release letter: “ten subpoenas responsive to your request.”", "NCIS", 1))
w("fig-apple", fig("apple", "s2-p06-dodig-subpoena-apple.jpg", 1500, 2121,
  "Department of Defense Office of Inspector General subpoena duces tecum to Apple's custodian of records, commanding production before an NCIS special agent in Naples, Italy, for Apple accounts tied to a redacted email address in an extortion scheme against a service member's dependent child",
  "The Apple subpoena. Signed for the inspector general by an associate general counsel.", "NCIS", 6))
w("fig-apple-appx", fig("apple-appx", "s2-p07-appendix-a-apple.jpg", 1392, 1478,
  "Appendix A to the Apple subpoena listing seven required records: registration information, customer service records, iCloud subscriber information and connection logs with IP addresses, device identifiers, iOS activation data and sign-on logs",
  "Apple’s Appendix A: seven categories, all account and device metadata.", "NCIS", 7))
w("fig-google-appx", fig("google-appx", "s2-p09-appendix-a-google.jpg", 1397, 1832,
  "Appendix A to the Google subpoena listing eight categories that track the statutory list: names, addresses, connection records, session times and IP addresses, length and types of service, instrument numbers, other subscriber identities and means of payment",
  "Google’s Appendix A follows the statute’s six categories almost word for word.", "NCIS", 9))
w("fig-meta", fig("meta", "s2-p13-dodig-subpoena-meta.jpg", 1436, 2087,
  "DoD inspector general subpoena to Meta Platforms for Facebook accounts tied to a redacted username and user ID, believed associated with the illegal sale of stolen Department of Defense property, March 1, 2024 through September 1, 2025",
  "The Meta subpoena: a stolen-property case, served through NCIS’s Washington field office.", "NCIS", 13))
w("fig-meta-appx", fig("meta-appx", "s2-p14-appendix-a-meta.jpg", 1353, 1120,
  "Appendix A to the Meta subpoena listing five required records: name, length of service, credit card information, email addresses and phone numbers, and login and logout IP addresses with timestamps",
  "Meta’s Appendix A: five items, close to the list Meta publishes for police.", "NCIS", 14))
w("fig-snap-appx", fig("snap-appx", "s2-p27-appendix-a-snap.jpg", 1392, 1363,
  "Appendix A to a Snap subpoena listing current and previous usernames, email addresses, phone numbers and display names, account creation date and IP address, IP addresses for account actions, and information about use of Snapchat services and account settings",
  "Snap’s Appendix A, copied from Snap’s law enforcement guide.", "NCIS", 27))
w("fig-snap-phone", fig("snap-phone", "s2-p21-dodig-subpoena-snap-phone.jpg", 1499, 1028,
  "DoD inspector general subpoena to Snap for records tied to a redacted phone number and Snapchat username, July 1 through September 30, 2025, returnable to NCIS Resident Agency Miramar",
  "A Snap subpoena keyed to a phone number and a username.", "NCIS", 21))
w("fig-mediatti", fig("mediatti", "s2-p34-dodig-subpoena-mediatti-ip-address.jpg", 1484, 965,
  "DoD inspector general subpoena to Mediatti Broadband Communications for the subscriber behind a redacted IP address between 21:30:16 UTC on May 24, 2025 and 11:18:01 UTC on May 27, 2025",
  "The broadband subpoena: one IP address, a window of about 62 hours.", "NCIS", 34))
w("fig-privacy-act", fig("privacy-act", "s2-p15-privacy-act-notice-noncompliance.jpg", 1398, 920,
  "Privacy Act notice served with the subpoenas, stating that disclosure is mandatory and that failure to comply may lead the Inspector General to request a court order, with contempt sanctions if the order is defied",
  "The Privacy Act notice served with each subpoena: enforcement goes through a court.", "NCIS", 15))
w("fig-custodian", fig("custodian", "s2-p25-custodian-letter-privacy-request.jpg", 1388, 933,
  "NCIS Far East Field Office custodian letter: this investigation is private and we request such privacy be maintained, and the recipient may consult an attorney",
  "A request, not a gag order: “we request such privacy be maintained.”", "NCIS", 25))

# --- Military judge / courts (Article III) figures ---
w("fig-dd453", fig("dd453", "s2-p19-dd-form-453-military-judge-subpoena.jpg", 1500, 1377,
  "DD Form 453 military justice subpoena commanding Hilton San Diego Bayfront, under 10 U.S.C. sections 846 and 847, to produce items listed in Attachment A, issued October 17, 2025 by a military judge",
  "A military judge’s subpoena to a hotel, on DD Form 453.", "NCIS", 19))
w("fig-hilton", fig("hilton", "s2-p20-attachment-a-hilton-records.jpg", 1240, 751,
  "Attachment A to the hotel subpoena requesting reservation details, room charges and video surveillance for February 9 to 12, 2025",
  "Its Attachment A: guest records, room charges and surveillance video.", "NCIS", 20))
w("fig-kik", fig("kik", "s2-p12-kik-warrant-attachment-a.jpg", 1500, 764,
  "Attachment A, Property to be Searched: this warrant applies to records stored by Kik care of MediaLab.ai in Santa Monica related to a redacted user name; footer reads Attachment A AS ISSUED for Kik Warrant, digitally signed 2025.10.15",
  "A search warrant’s Attachment A for a Kik account, included in the release. Top and bottom of one page; the dashed rule marks blank space removed.", "NCIS", 12))
w("fig-sealed", fig("sealed", "s2-p23-sealed-subpoena-withheld.jpg", 1500, 132,
  "Withholding notice: pages 18 through 20 redacted under exemption (b)(7)(D), sealed subpoena originated with the U.S. District Court for the Southern District of California",
  "The one subpoena withheld in full: a sealed federal court subpoena.", "NCIS", 23))

# --- Retention (FBI CAST provider retention reference, as of March 2019) ---
w("fig-cast-retention-matrix", fig("cast-retention-matrix", "s3-p074-cast-provider-retention-periods-all-carriers.jpg", 1500, 1078,
  "Provider Retention Periods chart, as of March 2019, listing how long AT&T, Cricket, T-Mobile, MetroPCS, Sprint, Verizon and U.S. Cellular kept each type of record, from subscriber data and call detail records to text message content, store video, voicemail and web browsing",
  "How long each carrier kept each kind of record, as of March 2019. Text-message content (“SMS content”) is the shortest-lived row. Carrier practices change over time; the figures show the pattern, not current policy. "
  + CAST_CREDIT + " Handling marking redacted by OctoProbe.", "CAST", 74))
w("fig-cast-verizon", fig("cast-verizon", "s3-p127-cast-verizon-data-retention-periods.jpg", 1500, 915,
  "Verizon Data Retention Periods table with Record, Timeframe Available and Cost columns; text message content is listed at 3-5 days, never more than 10 days, at $50 per 5 day increment, and call details at 365 rolling calendar days",
  "Verizon’s page: call and text records for “365 Rolling Calendar Days,” text-message content for “3-5 Days (never more than 10 days),” the only row with a price. Figures as of March 2019; practices change. "
  + CAST_CREDIT, "CAST", 127))
w("fig-cast-us-cellular", fig("cast-us-cellular", "s3-p137-cast-us-cellular-records-retention-time.jpg", 1500, 1030,
  "U.S. Cellular table of record types, descriptions and retention periods: call detail records, text message records and cell tower information for one rolling calendar year, content of text messages for 3-5 days",
  "U.S. Cellular’s page: call, text and cell-tower records for “1 rolling calendar year,” text content for “3-5 days.” Figures as of March 2019; practices change. "
  + CAST_CREDIT, "CAST", 137))

w("related", '''<aside aria-label="Related reading" class="related-reading">
<h2>Related Reading</h2>
<ul>
<li><a href="/blog/dhs-phone-location-data-legal-opinion-foia/">DHS Lawyers Wrote 24 Pages on Buying Your Phone’s Location Data. They Withheld Every Page of the Analysis.</a></li>
<li><a href="/blog/secret-service-foia-sharepoint-browser-history-osint-guide/">How to FOIA an Official’s Browser History, SharePoint Files and Teams Messages</a></li>
<li><a href="/blog/centcom-war-orders-anvil-chart-foia/">The Only Public Map of CENTCOM’s War Orders Is Dated 2022</a></li>
</ul>
</aside>
''')
