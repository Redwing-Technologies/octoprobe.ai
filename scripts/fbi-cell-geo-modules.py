import re
#!/usr/bin/env python3
"""Static modules for 'Inside the FBI's CAST Guide' (Investigations).
Read by scripts/build-fbi-cell-geo-post.py. Standard library only.
Page images in assets/figs/ were rendered from the three hosted PDFs at 150 dpi. Before cropping,
OctoProbe blacked out the FBI guide's UNCLASSIFIED//LES handling marking, email addresses and telephone
numbers (see the editor's note in the post). Captions link to the page in the hosted PDF."""
from html import escape as e
SLUG = "fbi-cell-phone-location-silent-sms-cast-guide"
A = f"/blog/{SLUG}/assets/"
F = A + "figs/"
D = f"/blog/{SLUG}/docs/"
CAST = D + "fbi-cast-cellular-analysis-geolocation-field-resource-guide-2019-redacted.pdf"
NDCAC = D + "ndcac-director-eab-briefing-april-2018.pdf"
FCC = D + "fcc-05-153-calea-broadband-first-report-and-order-2005.pdf"
DOCS = {"CAST": (CAST, "FBI CAST field guide"), "NDCAC": (NDCAC, "NDCAC program update"), "FCC": (FCC, "FCC 05-153")}
MODULES = {}
def w(name, s): MODULES[name] = s

def fig(mid, img, wd, ht, alt, caption, doc, page, mark_note=""):
    url, label = DOCS[doc]
    src = f'{url}#page={page}'
    return (f'<figure class="doc-fig" id="fig-{mid}"><img loading="lazy" decoding="async" src="{F}{img}" width="{wd}" height="{ht}" alt="{e(alt)}">'
            f'<figcaption>{re.sub(r"&(?![A-Za-z0-9#]+;)", "&amp;", caption)} <a href="{src}">{label}, p. {page}</a>.{(" " + mark_note) if mark_note else ""}</figcaption></figure>\n')

M = "Handling marking redacted by OctoProbe."
w("cover", f'<figure><img fetchpriority="high" decoding="async" src="{A}cover.png?v=1" width="2400" height="1260" '
  'alt="Illustration: a stylized street grid on a navy card with three cell towers, each casting a 120-degree sector and a dashed range band; the three overlap around a red phone dot labeled Overlap." '
  '><figcaption>How a phone is narrowed down: three sectors and three round-trip range bands overlap in one spot. '
  'Illustration: OctoProbe News. The street grid is fictional.</figcaption></figure>\n')

w("takeaways", '''<aside aria-label="Key takeaways" class="key-takeaways">
<h2>Key Takeaways</h2>
<ul>
<li>A phone checks in through a specific tower and sector whenever the network reaches it, and carriers log those events.</li>
<li>Investigators can trigger check-ins on demand. The FBI’s 2019 CAST guide describes a carrier “ping” that sends “a silent message” and, for one carrier, a call “without a ring.”</li>
<li>Location gets narrowed by exclusion: a 120-degree sector, a round-trip distance band and readings from three or more towers. A GPS-based ping can be tighter still.</li>
<li><em>Carpenter v. United States</em> (2018) generally requires a warrant for historical cell-site records. The Court left real-time tracking and tower dumps undecided.</li>
<li>A tower hit is not proof of presence. The guide itself warns that some coordinates are “NOT GPS-based” and that CAST does not testify to the accuracy of one carrier’s data.</li>
</ul>
</aside>
''')

def card(href, thumb, tw, th, title, meta, prov):
    return (f'<li class="doc-card"><a class="doc-thumb" href="{href}"><img loading="lazy" decoding="async" src="{F}{thumb}" width="{tw}" height="{th}" alt="First page of {title} (PDF)"></a>'
            f'<div class="doc-body"><p class="doc-title"><a href="{href}">{title}</a></p><p class="doc-meta">{meta}</p><p class="doc-prov">{prov}</p>'
            f'<p class="doc-actions"><a href="{href}">View PDF</a> · <a href="{href}" download>Download</a></p></div></li>')
w("docs", '<section class="doc-cards" aria-label="Source documents">\n<ul>\n'
  + card(CAST, "s1-p001-cover.jpg", 1500, 1125, "FBI CAST, Cellular Analysis &amp; Geo-Location Field Resource Guide",
         "139 pages · “Current as of March 2019” · PDF, 13 MB",
         "Released under FOIA to Property of the People. Five pages carry OctoProbe redactions of personal information.") + "\n"
  + card(NDCAC, "s2-p01-cover.jpg", 1500, 1159, "NDCAC Program Update, April 11, 2018",
         "14 slides · PDF, 0.7 MB",
         'Public briefing posted by NDCAC at <a href="https://ndcac.fbi.gov/file-repository/ndcac-director-eab-briefing-april-2018.pdf">ndcac.fbi.gov</a>. Unaltered.') + "\n"
  + card(FCC, "s3-p01-caption.png", 1148, 594, "FCC 05-153, CALEA and Broadband Access and Services",
         "First Report and Order, Aug. 5, 2005 · 59 pages · PDF, 0.3 MB",
         "Published FCC order. Unaltered copy of the file NDCAC hosts.")
  + '\n</ul>\n</section>\n')

w("fig-cast-cover", fig("cast-cover", "s1-p001-cover.jpg", 1500, 1125,
  "Cover of the FBI Cellular Analysis and Geo-Location Field Resource Guide: a Philadelphia street map with a cell sector wedge, the CAST and FBI seals, and the line Current as of March 2019",
  "The cover of the FBI’s CAST field guide.", "CAST", 1, M))
w("fig-cast-mission", fig("cast-mission", "s1-p005-cast-mission.jpg", 1500, 1125,
  "CAST Mission and Structure slide listing the program’s mission, three priorities, headquarters supervisors, National Assets and Field Assets",
  "CAST’s mission, priorities and staffing.", "CAST", 5, M))
w("fig-rf-survey", fig("rf-survey", "s1-p017-rf-survey.jpg", 1500, 1125,
  "Map of hexagonal cells with a phone in cell 691 and a neighbor list ranking five nearby cells by signal strength",
  "A phone keeps measuring nearby sectors and camps on the strongest.", "CAST", 17, M))
w("fig-sectors", fig("sectors", "s1-p030-sectors.jpg", 1500, 1125,
  "A tower drawn over a map with three colored sectors of about 120 degrees each, labeled alpha, beta and gamma",
  "A three-sector tower splits its coverage into wedges of about 120 degrees.", "CAST", 30, M))
w("fig-cell-id", fig("cell-id", "s1-p016-cell-id.jpg", 1500, 1125,
  "Base Stations slide with a table of switch and tower identifiers for AT&T, T-Mobile, Sprint, Verizon and U.S. Cellular on 3G and 4G networks",
  "Each sector has a network-unique cell identifier; carriers format it differently.", "CAST", 16, M))
w("fig-silent-message", fig("silent-message", "s1-p100-detail-silent-message.jpg", 705, 326,
  "Slide text: A Ping is conducted with the assistance of the cellular provider. A silent message is sent to the phone requesting a location update.",
  "From the guide’s slide on Sprint’s GPS “Ping.”", "CAST", 100))
w("fig-no-ring", fig("no-ring", "s1-p057-detail-ping-and-no-ring-call.jpg", 1500, 495,
  "Table rows for Sprint, Verizon and U.S. Cellular; the U.S. Cellular cell reads: No. However, you can force a call without a ring to the target device to determine tower/sector.",
  "The guide’s provider table. Bottom right: a call “without a ring.”", "CAST", 57))
w("fig-initiate-signal", fig("initiate-signal", "s1-p109-detail-initiate-a-signal.jpg", 1500, 326,
  "Slide heading Phrase to use in court orders/search warrants for T-Mobile E-911/GPS/Geo Locator, followed by the quoted order language",
  "Suggested order language for T-Mobile’s locator.", "CAST", 109))
w("fig-pcmd", fig("pcmd", "s1-p097-pcmd.jpg", 1500, 1125,
  "Engineering Data PCMD slide: a map with a tower, a 0.79-mile range arc and a red search-area box, with a caution that coordinates are not GPS-based",
  "Round-trip delay turns a sector into a distance band.", "CAST", 97, M))
w("fig-triangulation", fig("triangulation", "s1-p058-e911-triangulation.jpg", 1500, 1125,
  "E-911 Mobile Locator Tool slide: three towers on a street map with dashed range rings meeting at a phone, labeled with a latitude, longitude and uncertainty of 443 meters",
  "Triangulation from three or more towers. The coordinates are the guide’s sample.", "CAST", 58, M))
w("fig-tower-dumps", fig("tower-dumps", "s1-p060-tower-dumps.jpg", 1500, 1125,
  "Tower Dump Uses slide describing tower dumps for a specific crime and for multiple crimes",
  "Tower dumps, and how the guide suggests narrowing them.", "CAST", 60, M))
w("fig-e911-responses", fig("e911-responses", "s1-p111-e911-responses.jpg", 1500, 1125,
  "Table of five T-Mobile E-911 locator responses, from a successful location with coordinates to absent subscriber, position method failure, internal error and system failure",
  "What the locator returns, including failures. The sample phone number was redacted by OctoProbe.", "CAST", 111, M))
w("fig-nelos", fig("nelos", "s1-p082-nelos.jpg", 1500, 1125,
  "AT&T NELOS slide listing network event types and a location accuracy key from 0 to 13, with the banner CAST currently does not testify to the accuracy to NELOS",
  "AT&T’s NELOS accuracy key runs from 25 meters to 25 kilometers.", "CAST", 82, M))
w("fig-retention", fig("retention", "s1-p074-retention-prospective.jpg", 1500, 1125,
  "Provider Retention Periods grid, as of March 2019, listing how long AT&T, Cricket, T-Mobile, MetroPCS, Sprint, Verizon and U.S. Cellular keep each record type, including prospective location tools",
  "Retention periods and real-time (“prospective”) tools by carrier, as of March 2019.", "CAST", 74, M))
w("fig-rtt", fig("rtt", "s1-p130-verizon-rtt.jpg", 1500, 1125,
  "Verizon RTT slide comparing a call detail record with Real Time Tool columns that add an access distance in miles",
  "Verizon’s Real Time Tool adds distance from the tower.", "CAST", 130, M))
w("fig-legal", fig("legal", "s1-p010-codes-and-orders.jpg", 1500, 1125,
  "US Codes and Orders slide listing statutes and advising a 2703(d) court order or search warrant for historical call detail and cell site records",
  "The guide’s statute list and its advice to consult a federal prosecutor.", "CAST", 10, M)
  + fig("legal-table", "s1-p011-legal-process.jpg", 1500, 1125,
  "Two-column table: records available by subpoena versus by court order or search warrant, including ping data and E-911",
  "What the guide puts under subpoena and under court order or warrant. It notes requirements vary by judicial district.", "CAST", 11, M))
w("fig-exigent", fig("exigent", "s1-p066-exigent-requests.jpg", 1500, 1125,
  "Exigent Requests slide explaining voluntary disclosure under 18 U.S.C. 2702(c)(4) and compelled emergency disclosure under 18 U.S.C. 3125",
  "Emergency disclosure, voluntary and compelled.", "CAST", 66, M))
w("fig-disclaimer", fig("disclaimer", "s1-p002-disclaimer.jpg", 1500, 1125,
  "Disclaimer slide: studying the manual does not certify anyone to testify; CAST agents receive over 500 hours of training before testifying",
  "The guide’s first content page.", "CAST", 2, M))
w("fig-cast-origin", fig("cast-origin", "s1-p004-cast-origin.jpg", 1500, 1125,
  "CAST’s Origin slide describing drive testing of cell site coverage and a Project Pin Point mapping program",
  "CAST says it drive-tests sectors to find their true coverage. An email address was redacted by OctoProbe.", "CAST", 4, M))
w("fig-switch-pooling", fig("switch-pooling", "s1-p120-switch-pooling-not-location.jpg", 1500, 1125,
  "Switch list mapping two-letter codes to cities, under the heading MSC Location, not to be interpreted as the location of the device",
  "A switch code names a city, not a phone’s location.", "CAST", 120, M))
w("fig-ndcac-trg", fig("ndcac-trg", "s2-p03-trg.jpg", 1500, 1159,
  "NDCAC Technical Resource Group slide listing client numbers, types of calls handled including interpretation of call detail records, and 3,497 requests in six months",
  "NDCAC’s help desk for police, April 2018.", "NDCAC", 3))
w("fig-fcc-para4", fig("fcc-para4", "s3-p02-para4-background.png", 1148, 264,
  "Paragraph 4 of FCC order 05-153, explaining that Congress enacted CALEA on October 25, 1994",
  "Why Congress passed CALEA, in the FCC’s words.", "FCC", 2))
w("fig-fcc-para1", fig("fcc-para1", "s3-p01-para1.png", 1148, 247,
  "Paragraph 1 of FCC order 05-153: CALEA applies to facilities-based broadband Internet access providers and interconnected VoIP providers",
  "The 2005 order’s holding.", "FCC", 1))

w("related", '''<aside aria-label="Related reading" class="related-reading">
<h2>Related Reading</h2>
<ul>
<li><a href="/blog/dhs-phone-location-data-legal-opinion-foia/">DHS Lawyers Wrote 24 Pages on Buying Your Phone’s Location Data. They Withheld Every Page of the Analysis.</a></li>
<li><a href="/blog/secret-service-foia-sharepoint-browser-history-osint-guide/">How to FOIA an Official’s Browser History, SharePoint Files and Teams Messages</a></li>
</ul>
</aside>
''')
