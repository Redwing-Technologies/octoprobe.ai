"""Figure/table modules for the Afghanistan withdrawal FOIA post (scripts/build-afghan-foia-post.py).
Facts and quotes come from the FOIA-released State OIG review AUD-MERO-23-15 (May 2023), its public
companion AUD-MERO-23-33 (September 2023), the FOIA-released classified annex ISP-S-23-05A and its
unclassified parent ISP-I-23-05 (November 2022), and two FOIA-released email chains from the records
of Adm. Michael Gilday, chief of naval operations (August 24 and August 27-28, 2021).
Every quote is verbatim from the released page cited. Only one word is changed from the release:
the surname of a private Afghan family in the White Scarfs chain is covered by a black bar in the
image and removed (true redaction) from the hosted PDF. Modules are inserted after smart-quote
processing, so typographic quotes are written in place."""
from html import escape

SLUG = "afghanistan-withdrawal-foia-kabul-evacuation-record"
A = f"/blog/{SLUG}/assets/"
F = A + "figs/"
D = f"/blog/{SLUG}/docs/"
G = D + "state-oig-aud-mero-23-15-kabul-evacuation-review-foia-release.pdf"
E = D + "state-oig-isp-s-23-05a-afghanistan-affairs-unit-annex-foia-release.pdf"
NA = D + "cno-gilday-naveur-allies-refuge-report-aug-24-2021-foia-version-a.pdf"
NB = D + "cno-gilday-naveur-allies-refuge-report-aug-24-2021-foia-version-b.pdf"
WS = D + "cno-gilday-malloy-white-scarfs-email-aug-27-28-2021-foia.pdf"
M33 = "https://www.oversight.gov/sites/default/files/documents/reports/2023-09/AUD-MERO-23-33.pdf"
I05 = "https://www.oversight.gov/sites/default/files/documents/reports/2022-11/ISP-I-23-05.pdf"
MODULES = {}
def w(name, s): MODULES[name] = s

def fig(fid, img, wd, ht, alt, docid, quote_html, caption_html, wide=False):
    """Document image + selectable transcription (with visible document ID) + caption."""
    cls = "doc-fig doc-pair" + (" doc-pair-wide" if wide else "")
    return (f'<figure class="{cls}" id="{fid}">'
            f'<div class="doc-img"><img loading="lazy" decoding="async" src="{F}{img}?v=1" width="{wd}" height="{ht}" alt="{escape(alt)}"></div>'
            f'<div class="doc-transcript"><p class="doc-id"><span class="doc-id-label">Transcription</span> {docid}</p>'
            f'<blockquote class="doc-quote">{quote_html}</blockquote>'
            f'<p class="doc-full"><a href="{F}{img}">Full-size image</a></p></div>'
            f'<figcaption>{caption_html}</figcaption></figure>\n')

w("cover", f'<figure><img fetchpriority="high" decoding="async" src="{A}cover.png?v=1" width="2400" height="1260" '
  'alt="Three document excerpts on a dark navy card: the Highlights page of State Department inspector general report AUD-MERO-23-15 with its What OIG Found box withheld under (b)(1); a Navy status report listing 662 evacuees at Naval Air Station Sigonella; and an August 27, 2021, email about 53 at-risk women stopped at a Taliban checkpoint outside Kabul airport. Title: The Kabul Evacuation, From the Record." '
  '><figcaption>Excerpts from State Department OIG report AUD-MERO-23-15 (May 2023) and two August 2021 Navy email chains, all released under the Freedom of Information Act. Redactions as released. Illustration: OctoProbe News.</figcaption></figure>\n')

w("takeaways", '''<div class="callout takeaways"><strong class="callout-label">Key Takeaways</strong><ul>
<li>The State Department inspector general found Embassy Kabul’s emergency plan met the rules but the embassy “was not adequately prepared for the full scope of challenges” in August 2021.</li>
<li>Embassy leadership feared that overt evacuation planning would “cause panic,” and key security and consular officers rotated out in the days and weeks before Kabul fell.</li>
<li>Staffing at the embassy rose from 3,938 to 4,091 between April and June 23, 2021, after an ordered departure.</li>
<li>The inspector general could not verify the government’s count of about 124,000 evacuees.</li>
<li>Emails from the Navy’s top admiral track 662 evacuees at Sigonella and 53 at-risk women turned back at a Taliban checkpoint.</li>
<li>Most of the review’s findings are still withheld under FOIA exemption (b)(1).</li>
</ul></div>
''')

# ── State OIG: AUD-MERO-23-15 ────────────────────────────────────────────────
w("fig-highlights", fig("fig-highlights", "aud-mero-23-15-p02-highlights-what-oig-found-withheld.png", 1275, 1650,
  "Highlights page of State Department OIG report AUD-MERO-23-15, May 2023. The left column, What OIG Reviewed and What OIG Recommends, is legible; the right-hand What OIG Found box is empty except for the marking (b)(1). The SECRET//NOFORN banners at top and bottom are struck through.",
  f'AUD-MERO-23-15, Highlights (PDF p. 2)',
  '<p>“(U) On August 31, 2021, the Department of State (Department) officially suspended operations at U.S. Embassy Kabul, Afghanistan. … From there, the Department, along with the Department of Defense (DoD), oversaw a chaotic, noncombatant evacuation operation (NEO) in which 13 U.S. service members and many Afghan nationals lost their lives.”</p>'
  '<p>“(U) What OIG Found” — [box withheld, marked “(b)(1)”]</p>',
  f'State Department Office of Inspector General, <em>Review of Emergency Action Planning Guiding the Evacuation of U.S. Embassy Kabul, Afghanistan</em>, AUD-MERO-23-15, May 2023, Highlights page, as released under FOIA. <a href="{G}#page=2">Released copy, PDF p. 2</a>; public companion: <a href="{M33}#page=1">AUD-MERO-23-33, p. 1</a>.'))

w("fig-finding-b", fig("fig-finding-b", "aud-mero-23-15-p15-finding-b-preparatory-actions.png", 1275, 1650,
  "Page 12 of AUD-MERO-23-15: the heading Finding B, Embassy Kabul Was Not Fully Prepared for Challenges it Encountered in Evacuating Individuals, followed by a large box withheld under (b)(1), then a section on preparatory actions describing the April 27, 2021, alert urging U.S. citizens to leave, and a footnote on staffing of 3,938 and 4,091 personnel.",
  'AUD-MERO-23-15, p. 12 (PDF p. 15)',
  '<p>“(U) Finding B: Embassy Kabul Was Not Fully Prepared for Challenges it Encountered in Evacuating Individuals” — [box withheld, marked “(b)(1)”]</p>'
  '<p>“In the intervening months, Embassy Kabul took some actions to prepare for potential emergencies.”</p>'
  '<p>“prior to the ordered departure in April 2021, the embassy reported that it had a total of 3,938 personnel (including 301 American direct hires) at the embassy. By June 23, 2021, that number had increased to 4,091 personnel (including 433 U.S. direct hires).”</p>',
  f'AUD-MERO-23-15, May 2023, p. 12, as released under FOIA. <a href="{G}#page=15">Released copy, PDF p. 15</a>; public companion: <a href="{M33}#page=5">AUD-MERO-23-33, p. 5</a>.'))

w("fig-position", fig("fig-position", "aud-mero-23-15-p35-administration-stated-position.png", 1275, 1650,
  "Page 32 of AUD-MERO-23-15: a large box withheld under (b)(1) above the underlined heading Embassy Kabul Leadership Was Executing the Administration’s Stated Position that Diplomatic Operations Would Continue Following the Withdrawal of U.S. Military Forces and Had Concerns That Overt Evacuation Planning Would Cause Panic, followed by quotes from President Biden and Secretary Blinken.",
  'AUD-MERO-23-15, p. 32 (PDF p. 35)',
  '<p>“(U) According to multiple officials OIG interviewed during this review, another reason why the Ambassador did not prompt the additional drawdown of personnel or initiate NEO procedures when the EAP risk indicators were crossed and security conditions worsened was, at least in part, due to embassy leaderships’ execution of the Administration’s stated position that diplomatic operations would continue following the withdrawal of U.S. military forces.”</p>',
  f'AUD-MERO-23-15, May 2023, p. 32, as released under FOIA. <a href="{G}#page=35">Released copy, PDF p. 35</a>; public companion: <a href="{M33}#page=7">AUD-MERO-23-33, p. 7</a>.'))

w("fig-panic", fig("fig-panic", "aud-mero-23-15-p36-onward-assignments-create-panic.png", 1060, 755,
  "Crop of page 33 of AUD-MERO-23-15: two paragraphs on routine onward assignments, the early-August 2021 departure of the senior regional security officer and two deputies and the August 5 departure of the consular chief, and embassy leadership’s apprehension that overt evacuation steps would cause panic.",
  'AUD-MERO-23-15, p. 33 (PDF p. 36)',
  '<p>“despite the reported worsening security conditions, the Senior Regional Security Officer and two deputies (who had been at post for the prior year) departed in early August 2021, leaving the responsibility for security to individuals who had just arrived in July and August 2021.”</p>'
  '<p>“In their after-action report, management officers wrote that ‘Embassy Leadership did not wish to create panic and . . . ensured that Management Notices and informational emails did not address the truly dire situation.’”</p>',
  f'AUD-MERO-23-15, May 2023, p. 33, as released under FOIA. <a href="{G}#page=36">Released copy, PDF p. 36</a>; public companion: <a href="{M33}#page=8">AUD-MERO-23-33, p. 8</a>.', wide=True))

w("fig-124000", fig("fig-124000", "aud-mero-23-15-p45-data-reliability-124000.png", 1060, 470,
  "Crop of page 42 of AUD-MERO-23-15, the Data Reliability section, stating that after multiple inquiries the Department could not document its statement that about 124,000 people were evacuated.",
  'AUD-MERO-23-15, p. 42 (PDF p. 45)',
  '<p>“after multiple inquiries, the Department could not provide documentation supporting its statement that the U.S. government and its partners evacuated approximately 124,000 individuals in the weeks before it suspended operations at Embassy Kabul.”</p>',
  f'AUD-MERO-23-15, May 2023, Appendix A, p. 42, as released under FOIA. <a href="{G}#page=45">Released copy, PDF p. 45</a>; public companion: <a href="{M33}#page=5">AUD-MERO-23-33, p. 5</a>.', wide=True))

w("fig-appendix-b", fig("fig-appendix-b", "aud-mero-23-15-p46-appendix-b-decision-points-withheld.png", 1275, 1650,
  "Page 43 of AUD-MERO-23-15, the first page of Appendix B, U.S. Embassy Kabul Decision Points Framework, July 2021. Under the heading Operating Assumptions, nearly the whole page is a box withheld under (b)(1); the embedded SECRET/NOFORN marking is struck through.",
  'AUD-MERO-23-15, Appendix B, p. 43 (PDF p. 46)',
  '<p>“(U) APPENDIX B: U.S. EMBASSY KABUL DECISION POINTS FRAMEWORK, JULY 2021”</p>'
  '<p>“OPERATING ASSUMPTIONS: Operating Assumptions provide a baseline of the unique conditions in which Post operates.” — [rest of page withheld, marked “(b)(1)”]</p>',
  f'AUD-MERO-23-15, May 2023, Appendix B, p. 43, as released under FOIA. <a href="{G}#page=46">Released copy, PDF p. 46</a>.'))

# ── State OIG: ISP-S-23-05A ──────────────────────────────────────────────────
w("fig-annex-cover", fig("fig-annex-cover", "isp-s-23-05a-p01-classified-annex-cover.png", 1275, 1650,
  "Cover of State Department OIG report ISP-S-23-05A, Classified Annex to the Inspection of the Afghanistan Affairs Unit, Office of Inspections, November 2022. The classification block reading Classified By: Sandra Lewis, AIG; Reason: DSCG 17-01, C, G; Declassify By: 20471130 is crossed out with a large X, and the SECRET//NOFORN banners are struck through.",
  'ISP-S-23-05A, cover (PDF p. 1)',
  '<p>“ISP-S-23-05A Office of Inspections November 2022 — Classified Annex to the Inspection of the Afghanistan Affairs Unit — BUREAU OF SOUTH AND CENTRAL ASIAN AFFAIRS”</p>'
  '<p>[Crossed out:] “Classified By: Sandra Lewis, AIG / Reason: DSCG 17-01, C, G / Declassify By: 20471130”</p>',
  f'State Department Office of Inspector General, <em>Classified Annex to the Inspection of the Afghanistan Affairs Unit</em>, ISP-S-23-05A, November 2022, cover, as released under FOIA. <a href="{E}#page=1">Released copy, PDF p. 1</a>; unclassified parent report: <a href="{I05}">ISP-I-23-05</a>.'))

w("fig-threat", fig("fig-threat", "isp-s-23-05a-p06-threat-ratings-withheld.png", 1060, 420,
  "Crop of page 6 of ISP-S-23-05A, Appendix A: Threat Ratings. Column headings Terrorism, Political Violence, Crime, Human Intelligence, and Technical Intelligence are legible, but the ratings row for the Afghanistan Affairs Unit and a note below the source line are withheld under (b)(1).",
  'ISP-S-23-05A, Appendix A (PDF p. 6)',
  '<p>“(U) APPENDIX A: THREAT RATINGS” — Post: “AAU” — Terrorism, Political Violence, Crime, Human Intelligence, Technical Intelligence: [withheld, marked “(b)(1)”]</p>'
  '<p>“Source: Department’s Security Environment Threat List, dated December 23, 2021.”</p>',
  f'ISP-S-23-05A, November 2022, Appendix A, as released under FOIA. <a href="{E}#page=6">Released copy, PDF p. 6</a>.', wide=True))

# ── Navy: NAVEUR Operation ALLIES REFUGE status report, Aug 24, 2021 ─────────
w("fig-sigonella", fig("fig-sigonella", "naveur-allies-refuge-aug-24-2021-p2-sigonella-rota-status-version-a.png", 1390, 1660,
  "Page 2 of an August 24, 2021, email to the chief of naval operations titled NAVEUR Operation ALLIES REFUGE EOD 23Aug21. It praises Scotty Gray and the base commanding officer at Sigonella, whose name is withheld under (b)(6), and lists site status: NAS Sigonella active with 662 evacuees on hand against a capacity of 1,500, and NS Rota on standby with 0 of 650.",
  'NAVEUR Operation ALLIES REFUGE EOD 23Aug21, August 24, 2021, p. 2',
  '<p>“NAS SIGONELLA: Active Site<br>Evacuated personnel on Hand / Current Capacity: 662 / 1500<br>…<br>COVID Testing: all 662 evacuees tested, 2 positive, 8 close contacts (all 10 same family isolated)<br>State and Host Nation: Embassy Team on Station. Awaiting Consular service team.”</p>'
  '<p>“Narrative: NASSIG received a total of 662 consisting of 1x American Citizen (AMCIT), 1 Other Country National (OCN), and 654 Afghan personnel.”</p>'
  '<p>“NS ROTA: On Standby<br>Evacuated personnel on Hand / Current Capacity: 0 / 650<br>…<br>DHS Biometrics: None on station - awaiting prioritization from State and DHS”</p>',
  f'Email, “NAVEUR Operation ALLIES REFUGE EOD 23Aug21,” sent Tuesday, August 24, 2021, 5:26 AM, to Adm. Michael Gilday, chief of naval operations, from his email records as released under FOIA (version A). <a href="{NA}#page=2">Released copy, p. 2</a>.'))

w("fig-ab", f'''<figure class="doc-fig doc-compare" id="fig-ab">
<div class="ab-grid">
<div class="ab-col"><p class="ab-label">Version A</p><div class="doc-img"><img loading="lazy" decoding="async" src="{F}naveur-allies-refuge-aug-24-2021-p1-header-version-a.png?v=1" width="1390" height="220" alt="Version A, page 1 header of Adm. Gilday’s August 24, 2021, 9:48 AM reply: the To line and parts of the Cc line are covered by black bars labeled (b) (6), with Grady, Christopher W ADM USN USFFC (USA) and Paparo, Samuel J Jr ADM USN COMPACFLT N0 (USA) visible."></div>
<div class="doc-img"><img loading="lazy" decoding="async" src="{F}naveur-allies-refuge-aug-24-2021-p2-base-co-line-version-a.png?v=1" width="1390" height="153" alt="Version A, page 2: Scotty Gray and a black bar labeled (b) (6), followed by (base CO at Sig) have done an absolutely superb job bringing this together."></div></div>
<div class="ab-col"><p class="ab-label">Version B</p><div class="doc-img"><img loading="lazy" decoding="async" src="{F}naveur-allies-refuge-aug-24-2021-p1-header-version-b.png?v=1" width="1390" height="220" alt="Version B, page 1 header of the same reply: the Cc line carries more and differently split black bars labeled (b) (6) than version A, with Grady and Paparo still visible."></div>
<div class="doc-img"><img loading="lazy" decoding="async" src="{F}naveur-allies-refuge-aug-24-2021-p2-base-co-line-version-b.png?v=1" width="1390" height="153" alt="Version B, page 2: the same sentence, with the base commanding officer’s name covered by an unlabeled black bar instead of one labeled (b) (6)."></div></div>
</div>
<div class="doc-transcript"><p class="doc-id"><span class="doc-id-label">Transcription</span> NAVEUR Operation ALLIES REFUGE EOD 23Aug21, August 24, 2021, pp. 1–2, versions A and B</p>
<blockquote class="doc-quote"><p>Both versions: “Bob, super job by everyone. Good news on the BM kits … that’s been a constraint to thruput elsewhere. Based on calls I’ve had, I believe tempo will increase … airlift from HKIA over past 28 hrs the most visible of a few indicators.”</p><p>Version A: “Scotty Gray and (b) (6) (base CO at Sig) have done an absolutely superb job bringing this together.” Version B: “Scotty Gray and [unlabeled bar] (base CO at Sig) have done an absolutely superb job bringing this together.”</p></blockquote></div>
<figcaption>The same August 24, 2021, email processed twice under FOIA, with different redactions: version A (left) and version B (right). The body text is identical; only the bars differ, and neither version discloses anything the other withholds. Released copies: <a href="{NA}#page=1">version A</a>, <a href="{NB}#page=1">version B</a>.</figcaption></figure>
''')

# ── Navy: White Scarfs chain, Aug 27-28, 2021 ────────────────────────────────
w("fig-checkpoint", fig("fig-checkpoint", "white-scarfs-aug-27-2021-p4-taliban-checkpoint.png", 1390, 1100,
  "Vice Adm. James Malloy’s Friday, August 27, 2021, 8:40 PM email to Adm. Michael Gilday, subject NED White Scarfs Update, reporting that a group of 53 at-risk women on two buses was told by Taliban soldiers at a checkpoint near the airport’s South Gate that they were not approved to move forward. Gilday’s address is withheld under (b)(6).",
  'NED “White Scarfs” Update, August 27, 2021, 8:40 PM (p. 4)',
  '<p>“BL: I just received the following update from our A/SIG cell here at CENTCOM regarding the ‘White Scarfs.’ We are tracking that this particular group of White Scarfs (53 X at-risk females) is still in Kabul after an unsuccessful attempt to get through a TB checkpoint to the gates at HKIA.”</p>'
  '<p>“Once they completed their phone calls, the TB got back on the buses and told the passenger they were not ‘approved’ to move forward and they should leave the line immediately.”</p>'
  '<p>“As we discussed, the transition through Taliban check points has become increasingly problematic and the ICC’s ability to assist Afghans (without visa’s) at check points has become very limited.”</p>',
  f'Email from Vice Adm. James J. Malloy, U.S. Central Command, to Adm. Michael Gilday, chief of naval operations, “NED ‘White Scarfs’ Update,” Friday, August 27, 2021, 8:40 PM, from Gilday’s email records as released under FOIA. The attached list is not in the release. <a href="{WS}#page=4">Released copy, p. 4</a>.'))

w("fig-southgate", fig("fig-southgate", "white-scarfs-aug-28-2021-p3-south-gate-family-redacted.png", 1390, 450,
  "Adm. Gilday’s Saturday, August 28, 2021, 10:30 AM reply to Vice Adm. Malloy, reporting that one small group, possibly a family, of the 53 was allowed through while the rest waited 100 meters from the South Gate. The family’s surname is covered by a plain black bar added by OctoProbe News; the addresses are withheld under (b)(6).",
  'NED “White Scarfs” Update, August 28, 2021, 10:30 AM (p. 3)',
  '<p>“Jim,<br>Rcvd word that one small group, possibly a family ([private family name blacked out]), of the 53 total, was allowed through, but the remainder of the group is 100m from South Gate.</p>'
  '<p>Can A/SIG check status again with ICC?</p>'
  '<p>Thanks very much Jim. VR Mike”</p>',
  f'Email from Adm. Michael Gilday to Vice Adm. James J. Malloy, Saturday, August 28, 2021, 10:30 AM, as released under FOIA. <a href="{WS}#page=3">Released copy, p. 3</a>. <span class="redaction-note">OctoProbe News blacked out one word here and in the linked PDF: the surname of a private Afghan family.</span>', wide=True))

w("fig-100", fig("fig-100", "white-scarfs-aug-28-2021-p1-100-made-it-into-hkia.png", 1390, 510,
  "Adm. Gilday’s Saturday, August 28, 2021, 8:48:59 PM email to Vice Adm. Malloy saying about 100 of the White Scarfs made it into HKIA. Both men’s email addresses are withheld under (b)(6).",
  'NED “White Scarfs” Update, August 28, 2021, 8:48:59 PM (p. 1)',
  '<p>“Jim, I received a call that about 100 of the White Scarfs made it into HKIA. Thank you Jim … and the teams here and forward who are doing God’s work under the most difficult of circumstances.<br>VR Mike”</p>',
  f'Email from Adm. Michael Gilday to Vice Adm. James J. Malloy, Saturday, August 28, 2021, 8:48:59 PM, as released under FOIA. <a href="{WS}#page=1">Released copy, p. 1</a>.', wide=True))

# ── Timeline table ───────────────────────────────────────────────────────────
def gp(rp, pdfp): return f'<a href="{G}#page={pdfp}">AUD-MERO-23-15, p. {rp}</a>'
TL = [
 ("Feb. 29, 2020", "U.S. and Taliban sign the Doha Agreement; U.S. commits to withdraw all forces by May 1, 2021.", gp(1, 4)),
 ("Feb. 2021", "Embassy Kabul’s F-77 Report of Potential Evacuees, February version.", gp(15, 18)),
 ("Apr. 14, 2021", "President Biden announces the final withdrawal: “our diplomatic and humanitarian work will continue.”", gp(32, 35)),
 ("Apr. 27, 2021", "Ordered departure of non-emergency staff; embassy alert urges U.S. citizens to leave “as soon as possible.”", gp(12, 15)),
 ("Apr. 2021", "Embassy signs evacuation-support agreements with Canada, Germany, France, South Korea, and Sweden.", gp(13, 16)),
 ("May 21, 2021", "Joint Task Force Crisis Response, CENTCOM’s NEO task force, is activated.", gp(13, 16)),
 ("June 2021", "F-77 update reduces the estimate of potential evacuees.", f'<a href="{M33}#page=5">AUD-MERO-23-33, p. 5</a>'),
 ("June 23, 2021", "Embassy headcount reaches 4,091, up from 3,938 before the April ordered departure.", gp(33, 36)),
 ("July 2021", "Embassy Decision Points Framework (Appendix B), mostly withheld.", gp(43, 46)),
 ("July 8, 2021", "Biden: “I intend to maintain our diplomatic presence in Afghanistan.”", gp(32, 35)),
 ("July 22, 2021", "Embassy orders more personnel out; deputy chief of mission calls the cut temporary.", gp(33, 36)),
 ("Early Aug. 2021", "Senior regional security officer and two deputies depart post.", gp(33, 36)),
 ("Aug. 5, 2021", "Consular chief departs.", gp(33, 36)),
 ("Aug. 6, 2021", "Taliban capture their first provincial capital; interagency tabletop exercise in Washington.", f'{gp(2, 5)}; <a href="{M33}#page=5">AUD-MERO-23-33, p. 5</a>'),
 ("Aug. 15, 2021", "Taliban enter Kabul; embassy evacuates to Hamid Karzai International Airport.", gp(34, 37)),
 ("Aug. 24, 2021, 5:26 AM", "Navy report to the CNO: 662 evacuees at Sigonella; Rota on standby at 0 of 650.", f'<a href="{NA}#page=2">NAVEUR email, p. 2</a>'),
 ("Aug. 24, 2021, 9:48 AM", "Gilday: “I believe tempo will increase.”", f'<a href="{NA}#page=1">NAVEUR email, p. 1</a>'),
 ("Aug. 26, 2021", "Suicide bombing outside Abbey Gate kills 13 U.S. service members and many Afghans.", f'<a href="{M33}#page=1">AUD-MERO-23-33, p. 1</a>'),
 ("Aug. 27, 2021, 8:40 PM", "Malloy to Gilday: 53 at-risk women turned back at a Taliban checkpoint.", f'<a href="{WS}#page=4">White Scarfs email, p. 4</a>'),
 ("Aug. 28, 2021, 10:30 AM", "Gilday: one small group of the 53 let through; the rest 100 meters from South Gate.", f'<a href="{WS}#page=3">White Scarfs email, p. 3</a>'),
 ("Aug. 28, 2021, 8:48:59 PM", "Gilday: “about 100 of the White Scarfs made it into HKIA.”", f'<a href="{WS}#page=1">White Scarfs email, p. 1</a>'),
 ("Aug. 31, 2021", "State Department suspends operations at Embassy Kabul; last U.S. forces depart.", gp(13, 16)),
 ("Mar. 31, 2023", "State Department responds to the inspector general’s draft report.", gp(61, 64)),
 ("May 2023", "AUD-MERO-23-15 issued; listed as classified and not public.", f'<a href="{G}#page=1">AUD-MERO-23-15, cover</a>'),
 ("Sept. 2023", "Unclassified information brief AUD-MERO-23-33 published.", f'<a href="{M33}#page=1">AUD-MERO-23-33, p. 1</a>'),
]
w("timeline", '<div class="table-wrap"><table class="tl-table"><caption class="sr-only">Timeline of the Afghanistan withdrawal and Kabul evacuation reconstructed from FOIA records</caption><thead><tr><th scope="col">Date</th><th scope="col">Event</th><th scope="col">Document and page</th></tr></thead><tbody>\n'
  + "\n".join(f"<tr><td>{d}</td><td>{e}</td><td>{s}</td></tr>" for d, e, s in TL)
  + '\n</tbody></table></div>\n<p class="table-note">Report page numbers are the printed numbers; links open the released PDF at the matching page. Email times are as printed in the headers.</p>\n')

# ── What is still withheld ───────────────────────────────────────────────────
w("withheld", '''<ul>
<li><strong>The core findings.</strong> The “What OIG Found” box on the Highlights page of AUD-MERO-23-15 is withheld in full under (b)(1).</li>
<li><strong>The warning signs.</strong> The inspector general’s evaluation of how the embassy acted on its risk indicators as security worsened is withheld.</li>
<li><strong>Four recommendations.</strong> The wording of Recommendations 7 through 10 is withheld in the report’s list of recommendations.</li>
<li><strong>The decision points.</strong> Most of the embassy’s July 2021 Decision Points Framework, Appendix B, is withheld.</li>
<li><strong>The annex.</strong> Almost all of ISP-S-23-05A is withheld, including the threat ratings for the Afghanistan Affairs Unit.</li>
<li><strong>Personal details.</strong> In the Navy emails, (b)(6) covers email addresses, phone numbers, and some names, including the Sigonella base commander’s.</li>
</ul>
''')

# ── HowTo ────────────────────────────────────────────────────────────────────
HOWTO = [
 ("Find the record’s ID", "Search the inspector general’s report list, Oversight.gov, and the agency’s FOIA reading room. A classified report usually still has a public landing page with its number and date.", "step-1-find-the-record-id"),
 ("Request it by that ID", "File a FOIA request with the office that holds the record, cite the report number, and ask for every reasonably segregable portion. Classified pages come back with (b)(1) boxes, not blank refusals.", "step-2-request-it-by-that-id"),
 ("Pair it with the public version", "Read the redacted release next to any unclassified summary or parent report. The public version fills in context; the release shows how much of the full text exists.", "step-3-pair-it-with-the-public-version"),
 ("Pin every fact to a date and a page", "Log each event with its date, the document ID, and the printed and PDF page numbers, then sort the log into a timeline table.", "step-4-pin-every-fact-to-a-date-and-a-page"),
 ("Read email headers as data", "Record each message’s sender, recipients, timestamp, and subject. Re-sends, replies, and attachments missing from the release show how information moved.", "step-5-read-email-headers-as-data"),
 ("Compare duplicate releases", "When the same record turns up twice, set the copies side by side. Different redactions show processing choices, not new facts.", "step-6-compare-duplicate-releases"),
 ("State only what the record shows", "Quote verbatim, cite the page, and leave redactions alone. A blacked-out box tells you something exists, not what it says.", "step-7-state-only-what-the-record-shows"),
]
w("howto", '<ol class="howto-steps">\n' + "\n".join(
  f'<li id="{a}"><strong>{escape(n)}.</strong> {escape(t)}</li>' for n, t, a in HOWTO) + "\n</ol>\n")

w("doctypes", '''<ul>
<li><strong>Inspector general reports and their public companions</strong>, such as AUD-MERO-23-15 and AUD-MERO-23-33, for findings, footnoted dates, and staffing numbers.</li>
<li><strong>Classified annexes</strong>, such as ISP-S-23-05A, to map what is still withheld.</li>
<li><strong>Senior officials’ email records</strong>, for timestamps and the language used at the time.</li>
<li><strong>Daily situation reports</strong>, such as the Navy’s end-of-day status report, for headcounts and capacity.</li>
<li><strong>After-action reports and management responses</strong>, often quoted inside inspector general reports.</li>
</ul>
''')

# ── Summary table ────────────────────────────────────────────────────────────
SUM = [
 ("AUD-MERO-23-15", "State Department OIG, Office of Audits", "May 2023", "73", "Embassy Kabul’s plan met guidance, but the embassy was not fully prepared; leadership feared panic; evacuee data unreliable.", f'<a href="{G}">FOIA release</a>'),
 ("AUD-MERO-23-33", "State Department OIG", "Sept. 2023", "13", "Public summary of AUD-MERO-23-15; says the classified details are left out.", f'<a href="{M33}">Oversight.gov</a>'),
 ("ISP-S-23-05A", "State Department OIG, Office of Inspections", "Nov. 2022", "7", "Classified annex on the Afghanistan Affairs Unit; nearly all withheld.", f'<a href="{E}">FOIA release</a>'),
 ("ISP-I-23-05", "State Department OIG, Office of Inspections", "Nov. 2022", "28", "Unclassified inspection of the Doha-based Afghanistan Affairs Unit.", f'<a href="{I05}">Oversight.gov</a>'),
 ("NAVEUR ALLIES REFUGE EOD 23Aug21", "Email to the chief of naval operations", "Aug. 24, 2021", "3", "662 evacuees at Sigonella; Rota on standby; security forces the limiting factor.", f'<a href="{NA}">FOIA release (A)</a>, <a href="{NB}">(B)</a>'),
 ("NED “White Scarfs” Update", "Emails between Malloy and Gilday", "Aug. 27–28, 2021", "4", "53 at-risk women stopped at a Taliban checkpoint; about 100 White Scarfs later reach HKIA.", f'<a href="{WS}">FOIA release</a>'),
]
w("summary", '<div class="table-wrap"><table class="sum-table"><thead><tr><th scope="col">Document</th><th scope="col">Issuer</th><th scope="col">Date</th><th scope="col">Pages</th><th scope="col">What it shows</th><th scope="col">Source</th></tr></thead><tbody>\n'
  + "\n".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td><td>{f}</td></tr>" for a, b, c, d, e, f in SUM)
  + '\n</tbody></table></div>\n')

w("related", '''<aside aria-label="Related reading" class="related-reading">
<h2 id="related-reading">Related Reading</h2>
<ul>
<li><a href="/blog/foia-how-to-obama-situation-room-photos-presidential-records/">How to FOIA the Situation Room: One Request Pried Loose Thousands of Obama-Era Photos</a></li>
<li><a href="/blog/secret-service-foia-sharepoint-browser-history-osint-guide/">How to FOIA an Official’s Browser History, SharePoint Files and Teams Messages</a></li>
<li><a href="/blog/subpoena-warrant-online-accounts-three-branches/">Subpoena, Order, Warrant: How the Government Gets Your Data</a></li>
<li><a href="/blog/dhs-phone-location-data-legal-opinion-foia/">DHS Lawyers Wrote 24 Pages on Buying Your Phone’s Location Data. They Withheld Every Page of the Analysis.</a></li>
</ul>
</aside>
''')
