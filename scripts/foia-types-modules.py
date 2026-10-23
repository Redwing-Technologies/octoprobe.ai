"""Figure/table modules for the FOIA Request Guide (scripts/build-foia-types-post.py).
Type 1 facts come from DoD OIG FOIA case DODOIG-2024-000442 (response dated July 10, 2024), obtained
under FOIA: four Office of General Counsel weekly activity reports (info memos) to the Inspector
General dated April 5, 12, 19, and 26, 2024. Numbers are transcribed from the released pages; PDF page
numbers refer to the hosted copy, in which OctoProbe blacked out only the requester's name, email,
and street address on page 1 (true redaction; underlying text removed). Everything else is as released.
Modules are inserted after smart-quote processing, so typographic quotes are written in place."""
from html import escape

SLUG = "useful-foia-request-types"
A = f"/blog/{SLUG}/assets/"
F = A + "figs/"
P = A + "dodoig-2024-000442.pdf"
CREDIT = "Record: DoD Office of Inspector General."
MODULES = {}
def w(name, s): MODULES[name] = s

def fig(fid, img, wd, ht, alt, docid, quote_html, caption_html, wide=True):
    """Document image + selectable transcription (with visible document ID) + caption."""
    cls = "doc-fig doc-pair" + (" doc-pair-wide" if wide else "")
    return (f'<figure class="{cls}" id="{fid}">'
            f'<div class="doc-img"><img loading="lazy" decoding="async" src="{F}{img}" width="{wd}" height="{ht}" alt="{escape(alt)}"></div>'
            f'<div class="doc-transcript"><p class="doc-id"><span class="doc-id-label">Transcription</span> {docid}</p>'
            f'<blockquote class="doc-quote">{quote_html}</blockquote>'
            f'<p class="doc-full"><a href="{F}{img}">Full-size image</a></p></div>'
            f'<figcaption>{caption_html}</figcaption></figure>\n')

def chart(img, wd, ht, alt, caption_html):
    return (f'<figure><img loading="lazy" decoding="async" src="{F}{img}" width="{wd}" height="{ht}" alt="{escape(alt)}">'
            f'<figcaption>{caption_html}</figcaption></figure>\n')

w("cover", f'<figure><img fetchpriority="high" decoding="async" src="{A}cover.png" width="2400" height="1260" '
  'alt="Dark street map of downtown Washington centered on the White House, with a red map pin on the White House grounds near Lafayette Square and the Eisenhower Executive Office Building. On the right, three official seals, each ringed in blue: the Department of War, the Office of the Director of National Intelligence, and the Executive Office of the President seal of the United States Trade Representative. Title: FOIA Request Guide. Records that show how federal agencies work."'
  '><figcaption>Map © OpenStreetMap contributors</figcaption></figure>\n')

w("takeaways", '''<div class="callout takeaways"><strong class="callout-label">Key Takeaways</strong><ul>
<li>Recurring internal reports, agency-held White House email, distribution lists, and intranet pages show how federal offices work, and each can be requested by date range, custodian, or name.</li>
<li>Four weekly reports from the Defense Department inspector general’s lawyers, released under FOIA, count 157 inspector general subpoenas over four weeks of April 2024.</li>
<li>In those four weeks, 79 of the 157 subpoenas, about half, were for basic subscriber information, according to the tables’ footnotes.</li>
<li>The office reported 559 subpoenas issued in the second quarter of fiscal 2024, 221 of them for the Army’s criminal investigators, and 969 for the first half of the fiscal year.</li>
<li>Crimes against persons accounted for 254 of the quarter’s subpoenas, or 45%.</li>
<li>The categories behind each week’s count, and most legal advice in the reports, were withheld under exemption (b)(5).</li>
<li>Copies of White House email held by agencies can be requested under FOIA; one released email sent talking points to Cabinet members with its addressees left unredacted.</li>
<li>A Small Business Administration release shows a White House invitation addressed to four distribution lists, one printed in full as DLOPSODepartment@WHO.eop.gov.</li>
<li>Justice Department intranet screenshots name internal systems and collections and end with an unredacted Justice Management Division sitemap.</li>
</ul></div>
''')

TYPES = [
 ("type-1-inspector-general-weekly-activity-reports-and-info-memos", "Inspector general weekly activity reports and info memos", "Released record"),
 ("type-2-white-house-emails-requested-from-the-agency-side", "White House emails, requested from the agency side", "Released record"),
 ("type-3-distribution-lists-that-reach-core-staff", "Distribution lists that reach core staff", "Released record"),
 ("type-4-intranet-pages-and-screenshots", "Intranet pages and screenshots", "Released record"),
]
w("jumplist", '<div class="callout"><strong class="callout-label">Record Types in This Guide</strong><ul>\n'
  + "\n".join(f'<li><a href="#{a}">Type {i+1}: {escape(n[0].upper() + n[1:])}</a></li>' for i, (a, n, _) in enumerate(TYPES))
  + '\n</ul></div>\n')

# ── Types 2–4: hosted records and credits ────────────────────────────────────
# Per Colin (Oct. 23, 2026): no case numbers for Types 2-4; simple agency credits only.
P2 = A + "ustr-tai-email-release.pdf"
P3 = A + "sba-white-house-distribution-list-release.pdf"
P4 = A + "doj-jmd-intranet-release.pdf"
CREDIT2 = "Record: U.S. Trade Representative."
CREDIT3 = "Record: Small Business Administration."
CREDIT4 = "Record: Justice Department, Justice Management Division."

# ── Type 1 figures ───────────────────────────────────────────────────────────
w("fig-letter", fig("fig-letter", "dodoig-2024-000442-p01-response-letter-redacted.png", 1700, 1290,
  "Top of the DoD Office of Inspector General’s July 10, 2024, FOIA response letter, reference DODOIG-2024-000442, on Office of Inspector General letterhead. A solid black box covers the recipient block, and a second box follows the word Dear. Below, the letter describes the request for weekly activity reports for April 2024, the 5 U.S.C. 552(c) exclusion notice, and the release of 18 pages in part under exemptions (b)(5) and (b)(6).",
  "DODOIG-2024-000442, response letter, July 10, 2024 (PDF p. 1)",
  "<p>“This responds to your Freedom of Information Act (FOIA) request for ‘[a]ll Weekly Activity Reports (or Info Memos) or finalized weekly reporting to the DOD Inspector General from the Office of General Counsel,’ for the month of April 2024.”</p>"
  "<p>“Upon review, we determined that the enclosed 18 pages are appropriate for release in part pursuant to the following FOIA (5 U.S.C. § 552) exemptions: (b)(5) … and (b)(6) …”</p>",
  f'DoD Office of Inspector General, FOIA response letter, July 10, 2024, page 1. {CREDIT} <a href="{P}#page=1">Record, PDF p. 1</a>. <span class="redaction-note">OctoProbe blacked out the requester’s name, email address, and street address in this image and in the hosted PDF; the underlying text was removed.</span>'))

w("fig-memo", fig("fig-memo", "dodoig-2024-000442-p03-info-memo-april-5-2024.png", 1700, 2200,
  "First page of an Office of Inspector General info memo dated April 5, 2024, for the Inspector General, from Paul Hadjiyane, General Counsel, with a digital signature. The subject line reads Weekly Activity Report for April 1, 2024 to April 5, 2024. Under the heading Priorities, most bullet text is covered by black boxes marked (b)(5) and (b)(6); legible fragments include MOU with, We completed our revised comments on, and Support to OLAC and AI on. CUI markings at top and bottom are struck through.",
  "Weekly Activity Report for April 1, 2024 to April 5, 2024 (PDF p. 3)",
  "<p>“INFO MEMO … April 5, 2024 … FOR: INSPECTOR GENERAL … FROM: Paul Hadjiyane, General Counsel … SUBJECT: Weekly Activity Report for April 1, 2024 to April 5, 2024”</p>"
  "<p>“Priorities: MOU with [withheld, (b)(5)]: We completed our revised comments on [withheld, (b)(5)] … We plan to schedule an additional meeting to discuss.”</p>",
  f'First page of the Office of General Counsel’s weekly activity report dated April 5, 2024. {CREDIT} <a href="{P}#page=3">Record, PDF p. 3</a>.', wide=False))

w("fig-weekly", fig("fig-weekly", "dodoig-2024-000442-p11-weekly-subpoena-support-april-8-12.png", 1250, 1060,
  "Weekly Subpoena Support table from the report dated April 12, 2024, with columns DoD Component and Number and Category. Component cells read CID 17, OSI 6, DFAS 3, USMC CID 2, DCIS 1, NCIS 1, and DES MPI 1; every Number and Category cell is covered by black boxes marked (b)(5).",
  "Weekly Subpoena Support, report dated April 12, 2024 (PDF p. 11)",
  "<p>“CID – 17 … OSI – 6 … DFAS – 3 … USMC CID – 2 … DCIS – 1 … NCIS – 1 … DES MPI – 1 … TOTAL – 31”</p>"
  "<p>“** 20 of the total issued subpoenas were for Basic Subscriber Information”</p>"
  "<p>Number and Category: [withheld, (b)(5)]</p>",
  f'“Weekly Subpoena Support” table in the Office of General Counsel’s weekly activity report dated April 12, 2024. The table’s total row, “TOTAL – 31,” and its footnote sit just below this crop on the same page. {CREDIT} <a href="{P}#page=11">Record, PDF p. 11</a>.'))

w("fig-weekly-55", fig("fig-weekly-55", "dodoig-2024-000442-p19-weekly-subpoena-support-april-22-26.png", 1250, 770,
  "Weekly Subpoena Support table from the report dated April 26, 2024: USACIDC 37, OSI 15, DCIS 2, and DFAS 1, with every Number and Category cell covered by black boxes marked (b)(5).",
  "Weekly Subpoena Support, report dated April 26, 2024 (PDF p. 19)",
  "<p>“USACIDC – 37 … OSI – 15 … DCIS –2 … DFAS – 1 … TOTAL – 55”</p>"
  "<p>“**25 of the total issued subpoenas were for Basic Subscriber Information”</p>",
  f'The month’s largest weekly count, in the report dated April 26, 2024. The total row and footnote sit just below this crop. {CREDIT} <a href="{P}#page=19">Record, PDF p. 19</a>.'))

w("fig-q2", fig("fig-q2", "dodoig-2024-000442-p06-fy2024-q2-subpoena-statistics.png", 1210, 970,
  "A bullet reading FY 2024 Q2 Subpoena Statistics (Q1 and Q2 total = 969 issued subpoenas), above a three-dimensional pie chart titled DOD IG SUBPOENAS ISSUED - 2nd QUARTER FY 2024, total 559, as of 4/4/2024. Slices: CID 221, 40%; OSI 117, 21%; NCIS 66, 12%; DCIS 53, 9%; DFAS 41, 7%; USAF SFI 25, 4%; USMC CID 20, 4%; DES MPI 9, 2%; PFPA 5, 1%; Other 2, 0%. Below, the first two lines of Q2 Subpoenas by Type of Investigation.",
  "FY 2024 Q2 Subpoena Statistics, report dated April 5, 2024 (PDF p. 6)",
  "<p>“FY 2024 Q2 Subpoena Statistics (Q1 and Q2 total = 969 issued subpoenas)”</p>"
  "<p>“DOD IG SUBPOENAS ISSUED - 2nd QUARTER FY 2024 … TOTAL = 559 … AS OF: 4/4/2024” — CID, 221, 40%; OSI, 117, 21%; NCIS, 66, 12%; DCIS, 53, 9%; DFAS, 41, 7%; USAF SFI, 25, 4%; USMC CID, 20, 4%; DES MPI, 9, 2%; PFPA, 5, 1%; OTHER, 2, 0%</p>"
  "<p>“Q2 Subpoenas by Type of Investigation: 254 – Crimes Against Persons (45%) … 76 – Procurement Fraud (14%) … 21 – Public Corruption and National Security (4%) … 127 – Theft of Private or Government Property/Funds (23%) … 81 – Other Crimes (e.g., pay fraud, computer crime) (14%)”</p>",
  f'Quarterly subpoena statistics in the weekly activity report dated April 5, 2024. The last three investigation types appear just below this crop. {CREDIT} <a href="{P}#page=6">Record, PDF p. 6</a>.'))

w("fig-times", fig("fig-times", "dodoig-2024-000442-p07-subpoena-processing-times-march-2024.png", 1080, 450,
  "Table titled Monthly Subpoena Processing Times – March 2024, with Min/Max Days and Average Days: Pending Action (in queue) 0.25/0.5, average 0.3; Subpoena Team Processing 0.25/2.5, average 0.6; Attorney Team Processing 0.25/0.5, average 0.3; Total Processing 0.75/3.0, average 1.2; Cradle to Grave 0.75/14.0, average 2.4.",
  "Monthly Subpoena Processing Times – March 2024, report dated April 5, 2024 (PDF p. 7)",
  "<p>“Pending Action (in queue) 0.25/0.5 · 0.3 — Subpoena Team Processing 0.25/2.5 · 0.6 — Attorney Team Processing 0.25/0.5 · 0.3 — Total Processing 0.75/3.0 · 1.2 — Cradle to Grave 0.75/14.0 · 2.4”</p>"
  "<p>“*Calculation excludes weekends and holidays.”</p>",
  f'Processing-time table in the weekly activity report dated April 5, 2024; the footnote on weekends and holidays sits just below this crop. {CREDIT} <a href="{P}#page=7">Record, PDF p. 7</a>.'))

w("chart-weekly", chart("dod-ig-weekly-subpoena-support-april-2024.png", 2400, 1136,
  "Horizontal bar chart of weekly DoD IG subpoena support in April 2024: 35 subpoenas in the report of April 5, 14 of them for basic subscriber information; 31 in the report of April 12, 20 for basic subscriber information; 36 in the report of April 19, 20; and 55 in the report of April 26, 25. Total 157, of which 79, or 50%, were for basic subscriber information.",
  f'Weekly totals and basic-subscriber counts as printed in the four reports; the monthly sum and share are OctoProbe calculations. Sources: <a href="{P}#page=5">PDF pp. 5–6</a>, <a href="{P}#page=11">p. 11</a>, <a href="{P}#page=15">pp. 15–16</a>, <a href="{P}#page=19">p. 19</a>. Chart: OctoProbe.'))

w("chart-component", chart("dod-ig-subpoenas-fy2024-q2-by-component.png", 2400, 1732,
  "Horizontal bar chart of DoD IG subpoenas issued in the second quarter of fiscal 2024 by requesting component: Army CID 221, Air Force OSI 117, NCIS 66, DCIS 53, DFAS 41, USAF SFI 25, USMC CID 20, DES MPI 9, PFPA 5, and Other 2. Total 559.",
  f'Redrawn from the three-dimensional pie chart in the report dated April 5, 2024. Source: <a href="{P}#page=6">PDF p. 6</a>. Chart: OctoProbe.'))

w("chart-type", chart("dod-ig-subpoenas-fy2024-q2-by-investigation-type.png", 2400, 1244,
  "Horizontal bar chart of DoD IG subpoenas issued in the second quarter of fiscal 2024 by type of investigation: crimes against persons 254; theft of private or government property or funds 127; other crimes, such as pay fraud and computer crime, 81; procurement fraud 76; public corruption and national security 21. Total 559.",
  f'Categories and counts as printed in the report dated April 5, 2024. Source: <a href="{P}#page=6">PDF p. 6</a>. Chart: OctoProbe.'))

# ── Type 2–4 figures ─────────────────────────────────────────────────────────
w("fig-eop", fig("fig-eop", "ustr-eop-p18-talking-points-cabinet-email-jan-24-2024.png", 1500, 1980,
  "First page of an email titled Talking Points on the Conflict in the Middle East, from Evan M. Ryan of the White House Office, dated Wednesday, January 24, 2024, at 5:57 p.m. Eastern time. The To line lists Jared Bernstein of the Council of Economic Advisers, Shalanda D. Young of the Office of Management and Budget, Katherine C. Tai of the Office of the U.S. Trade Representative, Arati Prabhakar of the Office of Science and Technology Policy, and addresses at the departments of Homeland Security, Commerce, Defense, Energy, Interior, Labor, Transportation, Education, Health and Human Services, Housing and Urban Development, Treasury, Agriculture, State, and Veterans Affairs, the EPA, ODNI, SBA, and CIA. Sheila B. Grant and Sanam Rastegar of the White House Office are copied. The email opens Cabinet members and lists talking points under headings including New Phase of the Conflict, Lower Intensity IDF Ops, and Humanitarian Aid. The addresses are unredacted.",
  "Talking Points on the Conflict in the Middle East, January 24, 2024 (PDF p. 18)",
  "<p>“From: ‘Ryan, Evan M. EOP/WHO’ … Cc: ‘Grant, Sheila B. EOP/WHO’ … ‘Rastegar, Sanam EOP/WHO’ … Date: Wed, 24 Jan 2024 17:57:51 -0500”</p>"
  "<p>“Cabinet members, I know that many of you are getting questions on the conflict in the Middle East, so I wanted to make sure that you have the latest talking points at your disposal.”</p>",
  f'A White House Office email to Cabinet members, as kept in Trade Representative Katherine Tai’s email and released with the addressees unredacted. {CREDIT2} <a href="{P2}#page=18">Record, PDF p. 18</a>.', wide=False))

w("fig-dl-invite", fig("fig-dl-invite", "sba-p4-farewell-invite-distribution-lists.png", 1410, 425,
  "Calendar details printed with a forwarded White House invitation: Organizer Chiu, Rachel I. EOP/WHO, with the address blacked out; Subject Farewell to Natalie Montelongo!; Location Cab Camp (EEOB 160); Start Time 2024-02-23T17:00:00-05:00; End Time 2024-02-23T18:30:00-05:00. The Attendees line begins DL OPSO Department : DLOPSODepartment@WHO.eop.gov, followed by IGADepartment, DL WHO OPEAllStaff, and DL WHO Schedvance, whose addresses are mostly blacked out.",
  "Invitation details, February 2024 (PDF p. 4)",
  "<p>“Subject: Farewell to Natalie Montelongo! … Location: Cab Camp (EEOB 160) … Start Time: 2024-02-23T17:00:00-05:00”</p>"
  "<p>“Attendees: DL OPSO Department : DLOPSODepartment@WHO.eop.gov, IGADepartment, [withheld], DL WHO OPEAllStaff : [withheld], DL WHO Schedvance : [withheld]”</p>",
  f'The invitation’s attendee list opens with four White House distribution lists; one list address is printed in full. {CREDIT3} <a href="{P3}#page=4">Record, PDF p. 4</a>.'))

w("fig-dl-header", fig("fig-dl-header", "sba-p1-email-header-distribution-lists.png", 1510, 255,
  "Email header: From Chiu, Rachel I. EOP/WHO, with the address blacked out; Sent 2/16/2024 11:24:37 PM; To line naming DL OPSO Department, IGADepartment, DL WHO OPEAllStaff, and DL WHO Schedvance, with their addresses blacked out, followed by Office of the Vice President staff addresses that were left visible.",
  "Email header, February 16, 2024 (PDF p. 1)",
  "<p>“From: Chiu, Rachel I. EOP/WHO … Sent: 2/16/2024 11:24:37 PM … To: Chiu, Rachel I. EOP/WHO; DL OPSO Department [withheld]; IGADepartment [withheld]; DL WHO OPEAllStaff [withheld]; DL WHO Schedvance [withheld]; …”</p>",
  f'The same message on the release’s first page, where the list addresses are blacked out. {CREDIT3} <a href="{P3}#page=1">Record, PDF p. 1</a>.'))

w("fig-jmd-home", fig("fig-jmd-home", "doj-jmd-p1-dojnet-jmd-home.png", 1095, 1185,
  "Screenshot of the Justice Management Division landing page on DOJNet, the U.S. Department of Justice intranet. A left menu lists JMD staffs and offices, from the Appropriations Liaison Office to the Strategic Planning and Performance Staff and the JMD Document Library. The center lists the Assistant Attorney General for Administration and four deputy assistant attorneys general with their portfolios. A right column links to an organizational chart, the JMD Document Library, a DEIA committee, quick links including the DOJ Employee Service Portal (DOJEMP), the payroll calendar, and the JMD Correspondence Style Guide, and banners for the JMD e-Suggestion Box, the Table of Organization, telework support, and Justice Parking and Remote Credentialing.",
  "DOJNet, Justice Management Division landing page (PDF p. 1)",
  "<p>“DOJNet · U.S. Department of Justice Intranet … HOME · PEOPLE PLACES &amp; OFFICES · YOUR CAREER · HEALTH &amp; WELFARE · RESOURCES · POLICY, DIRECTIVES &amp; GUIDANCE · INFORMATION TECHNOLOGY”</p>"
  "<p>“Quick Links: DOJ Employee Service Portal (DOJEMP) · DOJ Libraries Acquisitions Services · Payroll Calendar · Flexible work options · JMD Supervisors’ Corner · DOJ Libraries Research Guides · JMD Correspondence Style Guide”</p>",
  f'The Justice Management Division’s page on the department’s intranet, as captured for the release. {CREDIT4} <a href="{P4}#page=1">Record, PDF p. 1</a>.', wide=False))

w("fig-jmd-sitemap", fig("fig-jmd-sitemap", "doj-jmd-p39-jmd-sitemap.png", 1120, 1490,
  "A page titled JMD Sitemap: a nested list beginning with Justice Management Division (JMD), then DAAG Chief Information Officer with the Office of the Chief Information Officer and its Cybersecurity Services, Policy and Planning, and Service Delivery staffs; DAAG Controller with the Appropriations Liaison Office, Asset Forfeiture Management Staff, Budget Staff, Debt Collection Management Staff, Finance Staff and its groups, Strategic Planning and Performance Staff, and Table of Organization; DAAG Human Resources and Administration with offices including Human Resources, the Library Staff, and the Security and Emergency Planning Staff, marked SharePoint site; and DAAG Policy, Management, and Procurement with offices including the Electronic Litigation Program, the Office of General Counsel, and the Office of Records Management Policy, FOIA, and Ediscovery.",
  "JMD Sitemap (PDF p. 39)",
  "<p>“JMD Sitemap · Justice Management Division (JMD) · DAAG Chief Information Officer · Office of the Chief Information Officer (OCIO) · Cybersecurity Services Staff (CSS) · Policy &amp; Planning Staff (PPS) · Service Delivery Staff (SDS) · DAAG Controller …”</p>"
  "<p>“Security &amp; Emergency Planning Staff (SEPS) (SharePoint site) … Office of Records Management Policy, FOIA, and Ediscovery (ORMP) … Procurement Services Staff (PSS)”</p>",
  f'The division’s internal sitemap, the release’s last page. {CREDIT4} <a href="{P4}#page=39">Record, PDF p. 39</a>.', wide=False))

JMD = [
 ("DOJ Employee Service Portal (DOJEMP)", "Employee service requests and issue reports, per its overview", "1, 34"),
 ("Table of Organization (T.O.)", "Position management system for approved positions, managed by HR and the Budget Staff", "1, 35, 39"),
 ("Justice Parking and Remote Credentialing (JPARC)", "Electronic parking passes", "1, 37"),
 ("JSMART, Justice Security Management &amp; Resource Tool", "Security and Emergency Planning Staff SharePoint site, with menu items for an SPM Portal and a Ticketing System", "19"),
 ("webTA; Employment Fact Book; G-Invoicing", "Entries in the Finance Staff menu under Financial Systems and Payroll", "30, 10"),
 ("JMD Ediscovery; Enterprise SharePoint; Justice Enterprise File Sharing (JEFS) System; JSTARS", "Entries under Applications &amp; Platform Services in the Chief Information Officer’s menu", "34"),
 ("OCIO Portal on SharePoint; Microsoft Teams; Office 365", "Telework resources page", "36"),
 ("JMD Document Library; JMD Fact Sheets", "Internal document collections", "1, 21"),
 ("RIM Lexicon; RIM Directive; OneDrive File Plan Instructions", "Records management office menu", "15"),
 ("Audit Liaison Handbook", "Internal Review and Evaluation Office menu", "12"),
 ("Purchase Card Program; Procurement Information Bulletins (PIBs)", "Procurement Services Staff menu", "18"),
 ("JMD Correspondence Style Guide", "Cover page", "38"),
 ("JMD Sitemap", "Four deputy portfolios and the staffs under each", "39"),
]
w("jmd-table", '<div class="table-wrap"><table class="sum-table"><thead><tr><th scope="col">Name in the screenshots</th><th scope="col">Where or what, as shown</th><th scope="col">PDF pages</th></tr></thead><tbody>\n'
  + "\n".join(f'<tr><td>{a}</td><td>{b}</td><td><a href="{P4}#page={c.split(",")[0].strip()}">{c}</a></td></tr>' for a, b, c in JMD)
  + '\n</tbody></table></div>\n<p class="table-note">Names as printed in the screenshots, with spelling normalized where the image is legible. The list is not exhaustive. Internal addresses shown in the images are not reproduced as links.</p>\n')




# ── Type 1 tables ────────────────────────────────────────────────────────────
WK = [
 ("Apr. 1–5", "Apr. 5", "Paul Hadjiyane, general counsel", "Army CID (USACIDC) 13, OSI 6, DFAS 5, DCIS 3, NCIS 3, DES MPI 3, PFPA 2", "35", "14", f'<a href="{P}#page=5">pp. 5–6</a>'),
 ("Apr. 8–12", "Apr. 12", "Paul Hadjiyane, general counsel", "CID 17, OSI 6, DFAS 3, USMC CID 2, DCIS 1, NCIS 1, DES MPI 1", "31", "20", f'<a href="{P}#page=11">p. 11</a>'),
 ("Apr. 15–19", "Apr. 19", "Paul Hadjiyane, general counsel", "OSI 16, Army CID (USACIDC) 10, NCIS 5, DES MPI 3, DFAS 2", "36", "20", f'<a href="{P}#page=15">pp. 15–16</a>'),
 ("Apr. 22–26", "Apr. 26", "David A. Core, principal deputy general counsel", "Army CID (USACIDC) 37, OSI 15, DCIS 2, DFAS 1", "55", "25", f'<a href="{P}#page=19">p. 19</a>'),
]
w("weekly-table", '<div class="table-wrap"><table class="sum-table"><thead><tr><th scope="col">Week</th><th scope="col">Report dated</th><th scope="col">From</th><th scope="col">Subpoenas by component, as printed</th><th scope="col">Total</th><th scope="col">Basic subscriber information</th><th scope="col">Record</th></tr></thead><tbody>\n'
  + "\n".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td><td>{f}</td><td>{g}</td></tr>" for a, b, c, d, e, f, g in WK)
  + '\n<tr><td>April 1–26</td><td>Four reports</td><td></td><td>Army CID 77, OSI 43, DFAS 11, NCIS 9, DES MPI 7, DCIS 6, PFPA 2, USMC CID 2</td><td>157</td><td>79</td><td>OctoProbe sum</td></tr>'
  + '\n</tbody></table></div>\n<p class="table-note">Component labels vary between reports (CID, USACIDC); both refer to the Army’s criminal investigators. The April 12 report’s subject line reads “April 8, 2024 to March 12, 2024,” as printed. The “Number and Category” column is withheld under (b)(5) in every week.</p>\n')

ACR = [
 ("CID, USACIDC", "U.S. Army Criminal Investigation Division (formerly Command)", '<a href="https://www.cid.army.mil/">Army</a>'),
 ("OSI", "Air Force Office of Special Investigations", '<a href="https://www.osi.af.mil/">AFOSI</a>'),
 ("NCIS", "Naval Criminal Investigative Service", '<a href="https://www.ncis.navy.mil/">NCIS</a>'),
 ("DCIS", "Defense Criminal Investigative Service, the inspector general’s own criminal investigators", '<a href="https://www.dodig.mil/Components/Investigations/">OIG</a>'),
 ("DFAS", "Defense Finance and Accounting Service", '<a href="https://www.dfas.mil/">DFAS</a>'),
 ("USMC CID", "U.S. Marine Corps Criminal Investigation Division", '<a href="https://www.lawenforcement.marines.mil/CID/">Marines</a>'),
 ("USAF SFI", "Not expanded in the record; Air Force Security Forces investigators work installation cases", '<a href="https://www.nellis.af.mil/News/Article/2431759/investigators-silent-partner-of-security-forces/">Nellis</a>'),
 ("DES MPI", "Not expanded in the record; on Army installations, military police investigators work under a Directorate of Emergency Services", '<a href="https://home.army.mil/huachuca/about/Garrison/DES/LE-division">Huachuca</a>'),
 ("PFPA", "Pentagon Force Protection Agency", '<a href="https://www.pfpa.mil/">PFPA</a>'),
]
w("acronyms", '<div class="table-wrap"><table class="sum-table"><thead><tr><th scope="col">Label in the record</th><th scope="col">Organization</th><th scope="col">Source</th></tr></thead><tbody>\n'
  + "\n".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in ACR) + '\n</tbody></table></div>\n')


w("related", '''<aside aria-label="Related reading" class="related-reading">
<h2 id="related-reading">Related Reading</h2>
<ul>
<li><a href="/blog/afghanistan-withdrawal-foia-kabul-evacuation-record/">‘Did Not Wish to Create Panic’: FOIA Records Rebuild the Official Story of the Kabul Evacuation</a></li>
<li><a href="/blog/secret-service-foia-sharepoint-browser-history-osint-guide/">How to FOIA an Official’s Browser History, SharePoint Files and Teams Messages</a></li>
<li><a href="/blog/dhs-phone-location-data-legal-opinion-foia/">DHS Lawyers Wrote 24 Pages on Buying Your Phone’s Location Data. They Withheld Every Page of the Analysis.</a></li>
</ul>
</aside>
''')
