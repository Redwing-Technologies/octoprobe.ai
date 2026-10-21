"""Figure/table modules for the Obama Library FOIA guide (scripts/build-foia-obama-post.py).
Facts come from the Obama Library response letter and finding aid for case 24-09538-F (segment 1),
the library-hosted metadata spreadsheets and withdrawal sheets, and National Archives Catalog records."""
from html import escape

SLUG = "foia-how-to-obama-situation-room-photos-presidential-records"
A = f"/blog/{SLUG}/assets/"
CAT = "https://catalog.archives.gov/id/"
MODULES = {}
def w(name, s): MODULES[name] = s

w("cover", f'<figure><img fetchpriority="high" decoding="async" src="{A}cover.png?v=2" width="2400" height="1260" '
  'alt="Illustration: a withdrawal sheet from FOIA case 24-09538-F, reading Withheld In Full, reasons P5, b(1), P1, frame P011910PS-0580, '
  'framed in red over a dark street map of downtown Washington with a red pin at the White House, and the words How to FOIA the Situation Room." '
  '><figcaption>The withdrawal sheet the National Archives left in place of a withheld Situation Room photograph, frame P011910PS-0580, in FOIA case 24-09538-F. '
  'Illustration: OctoProbe News; map © OpenStreetMap contributors.</figcaption></figure>\n')

w("takeaways", '''<div class="callout takeaways"><strong class="callout-label">Key Takeaways</strong><ul>
<li>My FOIA request, Obama Library case 24-09538-F, freed 3,951 Situation Room photographs and 3,851 electronic files from January 2009 through July 2010.</li>
<li>The winning formula: name the record type, the people, the place and the time, and ask for the metadata. The metadata came back as spreadsheets with dates, photographers and original captions.</li>
<li>The library withheld 1,208 images, most as confidential presidential advice (P5) or classified information (P1/(b)(1)).</li>
<li>Free downloads are web-size. Publication-quality copies are ordered from the library by “P” number, at $14 to $17 per image.</li>
<li>Withheld isn’t final: each withdrawal sheet gives the frame number you need to request a declassification review, and P5 restrictions on Obama records end by January 2029.</li>
</ul></div>
''')

w("template", '''<div class="callout"><strong class="callout-label">A request you can adapt</strong>
<p>Under the Freedom of Information Act, 5 U.S.C. § 552, and the Presidential Records Act, 44 U.S.C. §§ 2201–2209, I request all photographs of [person or people] taken in [place] from [start date] through [end date], together with the associated date/time groups and all metadata for each photograph, including the caption, photographer and frame number. Please provide the records in electronic form. I am a [news media / educational / other] requester.</p>
<p>Keep the subject specific and searchable. Archivists search captions, places and dates; vague words such as “all communications about” invite delays and fee estimates.</p>
</div>
''')

w("letter", f'''<figure><img loading="lazy" decoding="async" src="{A}foia-24-09538-f-response-letter-p1-redacted.png?v=1" width="1100" height="1424" alt="First page of the Obama Presidential Library’s response letter in FOIA case 24-09538-F. It reports that about 5,159 images and 3,851 electronic files were processed, 1,208 images were withheld in whole and 3,951 images and 3,851 electronic files were released in whole, and it lists the withholding counts by code. The letter date, my email address and the request date are covered by black bars."><figcaption>Page one of the response letter in case 24-09538-F. My email address and two dates are redacted.</figcaption></figure>
''')

w("casenumber", f'''<figure><img loading="lazy" decoding="async" src="{A}foia-24-09538-f-response-letter-p3-case-number.png?v=1" width="1100" height="461" alt="Close of the response letter: the FOIA case log number is 24-09538-F (segment 1), followed by the signature of Jill Zawacki, Supervisory Archivist, Barack Obama Presidential Library."><figcaption>The letter’s last paragraph gives the case number, 24-09538-F (segment 1). It is signed by Jill Zawacki, supervisory archivist.</figcaption></figure>
''')

CONT = [("January 20, 2009–June 30, 2009", "748", "543", "205"),
        ("July 1, 2009–December 31, 2009", "1,398", "1,121", "277"),
        ("January 1, 2010–July 31, 2010", "3,013", "2,302", "711")]
w("container", '<div class="table-wrap"><table><thead><tr><th scope="col">Situation Room photos, by date range</th><th scope="col">Photographs</th><th scope="col">Released in full</th><th scope="col">Withheld in full</th></tr></thead><tbody>\n'
  + "\n".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in CONT)
  + '\n</tbody></table></div>\n<p class="table-note">Source: Obama Library finding aid for FOIA 24-09538-F, container list.</p>\n')

EX = [("P1 / (b)(1)", "745", "National security information that is properly classified."),
      ("P3 / (b)(3)", "15", "Release would violate a federal statute."),
      ("P5", "1,178", "Confidential advice between the president and advisers, or between advisers. Presidential Records Act only."),
      ("P6 / (b)(6)", "13", "A clearly unwarranted invasion of personal privacy."),
      ("PRM", "441", "Personal record misfile: a personal, not presidential, record that was filed with official records."),
      ("(b)(7)(F)", "3", "Release could reasonably be expected to endanger someone’s life or physical safety. FOIA only.")]
w("exemptions", '<div class="table-wrap"><table class="ex-table"><thead><tr><th scope="col">Code</th><th scope="col">Images</th><th scope="col">What it means</th></tr></thead><tbody>\n'
  + "\n".join(f"<tr><td><code>{escape(c)}</code></td><td>{n}</td><td>{m}</td></tr>" for c, n, m in EX)
  + '\n</tbody></table></div>\n<p class="table-note">Source: response letter and code key in case 24-09538-F. “P” codes are Presidential Records Act restrictions, 44 U.S.C. § 2204(a); “(b)” codes are FOIA exemptions, 5 U.S.C. § 552(b).</p>\n')

# Sample rows from the library-hosted "1-1-2010 - 7-31-2010 Photo Metadata.xlsx" (verbatim fields; captions shortened with an ellipsis).
MD = [
 ("P010510PS-0214.CR2", "2010-01-05T00:00:00-0500", "Pete Souza", "President Barack Obama meets with his national security team in the Situation Room of the White House Jan. 5, 2010, about the attempted Christmas Day terrorist act aboard an airliner. …", "RESTRICTED", "P"),
 ("P011210PS-0282.CR2", "2010-01-12T00:00:00-0500", "Pete Souza", "President Barack Obama participates in a terrorism threat briefing in the Situation Room, Jan. 12, 2010. …", "CONTEMPLATIVE", "P"),
 ("P011310PS-0814.CR2", "2010-01-13T00:00:00-0500", "Pete Souza", "President Barack Obama meets with Vice President Joe Biden and senior civilian and military personnel who are coordinating the U.S. earthquake relief …", "RESTRICTED", "P"),
 ("P021710PS-0267.CR2", "2010-02-17T00:00:00-0500", "Pete Souza", "President Barack Obama meets with his national security team on Afghanistan and Pakistan in the Situation Room of the White House, Feb. 17, 2010. …", "RESTRICTED", "P"),
 ("P022610PS-0018.CR2", "2010-02-26T00:00:00-0500", "Pete Souza", "President Barack Obama meets with Prime Minister Gordon Brown of the United Kingdom and Chancellor Angela Merkel of Germany via secure video teleconference …", "RESTRICTED", "P"),
 ("P031510PS-0015.CR2", "2010-03-15T00:00:00-0400", "Pete Souza", "President Barack Obama has a Secure Video Teleconference (SVTC) with President Hamid Karzai of Afghanistan, in the  Situation Room, March 15, 2010. …", "RESTRICTED", "P"),
 ("P032410CK-0001.CR2", "2010-03-24T00:00:00-0400", "Chuck Kennedy", "Vice President Joe Biden drops by National Security Advisor Gen. James Jones's meeting with former National Security Advisors in the Situation Room …", "RESTRICTED", "P"),
 ("P032410PS-0054.CR2", "2010-03-24T00:00:00-0400", "Pete Souza", "President Barack Obama meets Sen. John Kerry, D-Mass., and Sen. Richard Lugar, R-Ind., on START in the Situation Room …", "CONGRESS", "P"),
 ("P042910PS-0640.CR2", "2010-04-29T00:00:00-0400", "Pete Souza", "President Barack Obama has a NSC Iran briefing in the Situation Room of the White House, April 29, 2010. …", "RESTRICTED", "P"),
 ("P050610PS-0204.CR2", "2010-05-06T00:00:00-0400", "Pete Souza", "General David Petraeus, Commander, U.S. Central Command, left, gestures during a meeting on Afghanistan and Pakistan …", "FLICKR", "P"),
 ("MP050610AC-0001.jpg", "2010-05-06T11:55:56-0400", "Arun Chaudhary", "President Barack Obama meets with his national security team on Afghanistan and Pakistan … This image represents the motion picture contents of: 20100506_Sit_Room", "", "MP"),
 ("P051010PS-0425.CR2", "2010-05-10T00:00:00-0400", "Pete Souza", "President Barack Obama meets with several Cabinet members and senior administration officials in the Situation Room of the White House, to review BP e…", "RESTRICTED", "P"),
 ("P072910PS-0346.CR2", "2010-07-29T00:00:00-0400", "Pete Souza", "President Barack Obama and Vice President Joe Biden meet with with members of the national security team in the Situation Room of the White House, to discuss Afghanistan and Pakistan …", "RESTRICTED", "P"),
]
def _dt(d):
    a, b = escape(d).split("T", 1)
    return f'<span class="dt">{a}</span><span class="dt">T{b}</span>'
w("metadata", '<figure class="meta-fig"><div class="table-wrap meta-wrap"><table class="meta-table"><thead><tr><th scope="col">Frame</th><th scope="col">DateTaken</th><th scope="col">Photographer</th><th scope="col">Caption (shortened)</th><th scope="col">Keyword</th></tr></thead><tbody>\n'
  + "\n".join(f"<tr><td><code>{escape(f)}</code></td><td><code>{_dt(d)}</code></td><td>{escape(p)}</td><td>{escape(c)}</td><td>{escape(k) or '—'}</td></tr>" for f, d, p, c, k, fc in MD)
  + '\n</tbody></table></div><figcaption>Thirteen of the 2,301 rows in the released photo metadata for case 24-09538-F, January–July 2010, with fields as released and captions shortened. Every photo row carries Film Code “P” except the motion-picture still, which carries “MP,” and the Handling Restriction field reads “PRA.” Source: Obama Library finding aid, “1-1-2010 – 7-31-2010 Photo Metadata.xlsx.”</figcaption></figure>\n')

PHOTOS = [
 ("situation-room-2009-06-12-north-korea-P061209PS-0461.jpg", "P061209PS-0461", 628707590,
  "President Obama, seated in the foreground with his hand at his chin, faces Secretary of State Hillary Clinton and military and civilian officials around the Situation Room table, under clocks showing local, presidential and Zulu time.",
  "President Barack Obama attends a meeting regarding North Korea in the Situation Room, June 12, 2009. Participants include Secretary of State Hillary Clinton, Gen. James Jones, Adm. Michael Mullen, Deputy Secretary of State Jim Steinberg and CIA Director Leon Panetta."),
 ("situation-room-2009-10-09-afghanistan-pakistan-P100909PS-0428.jpg", "P100909PS-0428", 628708640,
  "President Obama speaks from the head of the Situation Room table beneath the presidential seal, with Secretary of State Hillary Clinton at right, during a meeting on Afghanistan and Pakistan.",
  "President Barack Obama meets with his national security team on Afghanistan and Pakistan in the Situation Room, October 9, 2009."),
 ("situation-room-2009-11-30-karzai-svtc-P113009PS-0909.jpg", "P113009PS-0909", 628709508,
  "President Obama and three aides sit at the end of a long, mostly empty Situation Room table, facing a large wall screen that shows a room of people on the other end of the video link.",
  "President Barack Obama participates in a secure video teleconference with President Hamid Karzai of Afghanistan in the Situation Room, November 30, 2009. Participants include Gen. James Jones, NSC director for Afghanistan Temim H. Nusraty and Lt. Gen. Doug Lute."),
 ("situation-room-2010-01-05-christmas-day-plot-P010510PS-0275.jpg", "P010510PS-0275", 628710123,
  "President Obama sits beneath the presidential seal with his chin on his hand, listening, as an official in the foreground turns toward him.",
  "President Barack Obama meets with his national security team in the Situation Room about the attempted Christmas Day terrorist attack aboard an airliner, January 5, 2010."),
 ("situation-room-2010-02-26-brown-merkel-svtc-P022610PS-0033.jpg", "P022610PS-0033", 628711199,
  "President Obama, in the foreground, and aides read papers at the Situation Room table while a wall screen at the far end shows participants on the video link, beneath a sign reading Mic On.",
  "President Barack Obama meets with Prime Minister Gordon Brown of the United Kingdom and Chancellor Angela Merkel of Germany via secure video teleconference in the Situation Room, February 26, 2010."),
 ("situation-room-2010-05-06-petraeus-afghanistan-P050610PS-0194.jpg", "P050610PS-0194", 628713011,
  "Gen. David Petraeus, in uniform, gestures over an open binder, with Gen. James Cartwright beside him, during a Situation Room meeting.",
  "Gen. David Petraeus, commander of U.S. Central Command, left, gestures during a meeting on Afghanistan and Pakistan with President Barack Obama and the national security team in the Situation Room, May 6, 2010. At right is Gen. James E. Cartwright, vice chairman of the Joint Chiefs of Staff."),
]
w("photos", "\n".join(
  f'<figure><img loading="lazy" decoding="async" src="{A}{fn}?v=2" width="1024" height="682" alt="{escape(alt)}">'
  f'<figcaption>{escape(cap)} Frame <a href="{CAT}{naid}">{p}</a>. Official White House photo by Pete Souza.</figcaption></figure>'
  for fn, p, naid, alt, cap in PHOTOS) + "\n")

WD = [
 ("Tue Mar 26 15:29:53 EDT 2024", "P5,b(1),P1", "2.0.0.419bb5fa-96bb-4016-b353-2fb48376260b", "P011910PS-0580"),
 ("Thu Mar 21 11:35:40 EDT 2024", "P1,b(1),P5", "2.0.0.426e52ce-cb06-4501-a8b9-e570d819498e", "P010810PS-0291"),
 ("Tue Mar 12 12:38:41 EDT 2024", "P5,b(1),P1", "2.0.0.443bcc83-439d-4b0f-adea-24d1b6037795", "P100709PS-0493"),
]
def _sheet(d, r, g, p):
    return ("THIS RECORD IS A WITHDRAWAL SHEET\n"
            f"Date created: {d}\n\nReleasability: Withheld In Full\n\n"
            f"Reasons for Withholding:\n------------------------\n{r}\n\n"
            f"Notes:\n-------\n{g}\n<mark>{p}</mark>\n\nCase ID: 24-09538-F")
w("withdrawals", '<figure class="wd-fig"><div class="wd-grid">\n'
  + "\n".join(f'<pre class="wd-sheet" aria-label="Withdrawal sheet for {p}">{_sheet(escape(d), escape(r), escape(g), p)}</pre>' for d, r, g, p in WD)
  + '\n</div><figcaption>Three of the withdrawal sheets for case 24-09538-F, as released, each for an image withheld in full as classified (P1, b(1)) and as confidential advice (P5). The “P” number is highlighted; the empty “Additional Information” fields at the bottom of each sheet are omitted. Source: Obama Library finding aid, “Withdrawal Sheets.zip.”</figcaption></figure>\n')

w("related", '''<aside aria-label="Related reading" class="related-reading">
<h2 id="related-reading">Related Reading</h2>
<ul>
<li><a href="/blog/secret-service-foia-sharepoint-browser-history-osint-guide/">How to FOIA an Official’s Browser History, SharePoint Files and Teams Messages</a></li>
<li><a href="/blog/dhs-phone-location-data-legal-opinion-foia/">DHS Lawyers Wrote 24 Pages on Buying Your Phone’s Location Data. They Withheld Every Page of the Analysis.</a></li>
<li><a href="/blog/subpoena-warrant-online-accounts-three-branches/">Subpoena, Order, Warrant: How the Government Gets Your Data</a></li>
</ul>
</aside>
''')
