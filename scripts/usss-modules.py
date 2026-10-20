#!/usr/bin/env python3
"""Figure-style interactive modules for the Secret Service FOIA x OSINT guide.
Every module's content is readable static HTML; assets/usss.js adds search, filters,
the loop stepper and the lightbox. Data sources:
  - docs/federal-foia-sharepoint-hostnames.csv (practitioner sheet, unaltered)
  - docs/dns-check-2026-10-20.csv (passive DNS results, Oct. 20, 2026)
  - page structure of docs/usss-foia-release-two-redactions.pdf (page footers)
Read by scripts/build-usss-post.py. Standard library only (Pillow optional, not needed)."""
import csv, html, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
SLUG = "secret-service-foia-sharepoint-browser-history-osint-guide"
POST = ROOT / "blog" / SLUG
D = f"/blog/{SLUG}/docs/"
A = f"/blog/{SLUG}/assets/"
REL = f"{D}usss-foia-release-two-redactions.pdf"
LOG = "https://www.secretservice.gov/sites/default/files/reports/2025-02/FOIA-Log-FY-2024.pdf"
MODULES = {}
e = html.escape

def w(name, s): MODULES[name] = s

def fig(mid, kicker, title, body, caption, extra_cls=""):
    return (f'<figure class="ixm-fig" id="fig-{mid}">\n<div class="ixm {extra_cls}" data-ixm="{mid}">\n'
            f'<div class="ixm-head"><span class="ixm-kicker">{e(kicker)}</span><span class="ixm-title">{e(title)}</span></div>\n'
            f'<div class="ixm-live">\n{body}\n</div>\n</div>\n<figcaption>{caption}</figcaption>\n</figure>\n')

# ---------- cover ----------
w("cover", f'<figure><img fetchpriority="high" decoding="async" src="{A}cover.png?v=1" width="2400" height="1260" '
  'alt="Illustration: bright street map of downtown Washington with a red pin on U.S. Secret Service headquarters at 950 H Street NW, the Secret Service star on the right, and the words Map the tenant. Name the custodian." '
  '><figcaption>U.S. Secret Service headquarters at 950 H St. NW in Washington. Illustration: OctoProbe News; map © OpenStreetMap contributors; '
  'Secret Service star: U.S. Secret Service. Use of the star does not imply endorsement.</figcaption></figure>\n')

# ---------- takeaways ----------
w("takeaways", '''<aside aria-label="Key takeaways" class="key-takeaways">
<h2>Key Takeaways</h2>
<ul>
<li><a href="#step-1-identify-the-agency-s-microsoft-365-tenant-and-sharepoint-hosts">You can confirm an agency’s SharePoint address with public DNS and Microsoft’s own sign-in metadata. No login, no scanning.</a></li>
<li><a href="#step-2-identify-the-custodian-by-name-or-title">You don’t need an email address. A name and title are enough for the agency to search a custodian’s records.</a></li>
<li><a href="#step-3-choose-the-record-types">Microsoft documents where Teams chats, channel posts and shared files are kept. A request that names those places is harder to answer with “no records.”</a></li>
<li><a href="#step-5-anticipate-the-agency-s-answers">The D.C. Circuit held in 2021 that two other agencies’ browsing histories were not agency records. The Secret Service processed requests for five top officials’ browser histories and closed all five “Granted/Denied in Part,” according to its FY 2024 FOIA log.</a></li>
<li><a href="#step-7-use-what-comes-back">An April 2025 request returned a sitemap of roughly 660 internal Secret Service sites and 105 pages of blacked-out card statements. The PDF contains no records for the two document requests.</a></li>
</ul>
</aside>
''')

# ---------- checklists ----------
w("can-request", '''<aside class="checklist-box" aria-label="What you can request">
<p class="cl-h">What you can request</p>
<ul class="cl-list">
<li><a href="#browser-history-and-web-proxy-logs">Browser history and web-proxy, gateway, DNS or endpoint logs</a></li>
<li><a href="#sharepoint-documents-created-and-edited">SharePoint and OneDrive documents a custodian created or edited</a></li>
<li><a href="#teams-messages-channel-files-and-chat-files">Teams chats (Exchange Online mailbox), channel posts (team mailbox), channel files (SharePoint) and chat files (OneDrive)</a></li>
<li><a href="#card-statements-and-sitemaps">Agency card statements</a></li>
<li><a href="#card-statements-and-sitemaps">A sitemap of the agency’s SharePoint</a></li>
</ul>
</aside>
''')
w("before-file", '''<aside class="checklist-box cl-end" aria-label="Before you file checklist">
<ul class="cl-list cl-check">
<li>You confirmed the tenant: DNS resolves, and the tenant ID matches the agency’s email domain.</li>
<li>You named both hosts: <code>[tenant].sharepoint.com</code> and <code>[tenant]-my.sharepoint.com</code>.</li>
<li>Every item names a custodian by full name and title, with the dates the person held the job.</li>
<li>Every item has a fixed start and end date.</li>
<li>Each record type is its own numbered item, tied to the system that holds it.</li>
<li>You asked for documents sorted by date, not a list or index of them.</li>
<li>Teams and email items carry keywords.</li>
<li>Browser-history items also ask for centrally retained proxy, gateway, DNS or endpoint logs.</li>
<li>You asked for electronic copies or native files and a description of the search.</li>
<li>You stated your fee category and, if it fits, asked for a fee waiver or expedited processing.</li>
<li>You are filing log requests soon after the period you care about.</li>
<li>You will record the receipt date and log number, then check the agency’s FOIA log.</li>
</ul>
</aside>
''')

# ---------- static figures ----------
def imgfig(name, src, wdt, hgt, alt, cap, cls="fig-pad doc-page"):
    w(name, f'<figure class="{cls}"><img src="{A}{src}" width="{wdt}" height="{hgt}" alt="{e(alt)}" loading="lazy" decoding="async"><figcaption>{cap}</figcaption></figure>\n')

imgfig("fig-log", "usss-foia-log-fy2024-browser-history-requests.png", 2200, 763,
  "Rows from the Secret Service FOIA log for requests 20240109 through 20240113, received Nov. 3, 2023, each seeking an official’s browser history from October 2023 and each marked Granted/Denied in Part. The requester column is covered by black boxes added by OctoProbe.",
  f'The Secret Service’s FY 2024 FOIA log lists five requests for top officials’ browser histories, received Nov. 3, 2023, each closed “Granted/Denied in Part.” Requester name redacted by OctoProbe; the requester is the author. Source: U.S. Secret Service, <a href="{LOG}#page=12">FOIA Log FY 2024</a>, pp. 12–13 (full log, as posted).',
  cls="fig-pad wide-doc")

imgfig("fig-sitemap", "usss-release-p106-sitemap.png", 1650, 1275,
  "First page of the released SharePoint sitemap, headed USSS - Standard Sensitive Info, with columns for site name, URL, hub and Active/Accessable; the entire URL column is covered by one box stamped (b)(7)(E)",
  f'First page of the sitemap the Secret Service released. Site names and hubs came out; every URL was withheld under exemption (b)(7)(E). Source: Secret Service FOIA release (<a href="{REL}#page=106">PDF p. 106</a>).',
  cls="fig-pad wide-doc")

imgfig("fig-statement", "usss-release-p003-statement.png", 850, 1100,
  "A released card-statement page that is blank except for the header Account: XXXX-XXXX-XXXX followed by a box stamped (b)(7)(E); (b)(6); (b)(7)(C), and the footer Page 4 of 4",
  f'A typical card-statement page: a masked account line, an exemption box and a page number. Source: Secret Service FOIA release (<a href="{REL}#page=3">PDF p. 3</a>).')

# ---------- Fig. 1: Rowe page + lightbox ----------
w("rowe", fig("rowe", "Primary record · photographed page", "One page of a deputy director’s web log",
 f'''<div class="rl-wrap">
<a class="rl-open" href="{A}rowe-browser-history-zoom.jpg" data-full="{A}rowe-browser-history-zoom.jpg">
<img src="{A}rowe-browser-history-web.jpg" width="1200" height="1679" loading="lazy" decoding="async" alt="Photograph of one printed page of a web-activity log. Columns show a date and time, a username beginning ron.rowe, a column covered by a box stamped (b)(6); (b)(7)(C), and a host name. The top rows are dated 10/10/2023 14:16 and list Microsoft 365 hosts including unitedstatessecretservice.sharepoint.com; the rest are dated 10/4/2023 between 22:33 and 22:38 and list news-site and advertising hosts. Some rows are highlighted in yellow.">
<span class="rl-zoom" aria-hidden="true">Open full size</span></a>
<div class="rl-notes">
<p class="ixm-sub">What the page shows</p>
<ul class="rl-list">
<li><strong>Dates.</strong> 15 rows at <code>10/10/2023 14:16</code>; the rest between <code>10/4/2023 22:33</code> and <code>22:38</code>, newest first.</li>
<li><strong>User.</strong> A username column that begins <code>ron.rowe</code>. The next column is withheld under (b)(6) and (b)(7)(C).</li>
<li><strong>Agency systems.</strong> <code>unitedstatessecretservice.sharepoint.com</code>, <code>gcc.thor.aesir.office.com</code>, <code>graph.microsoft.com</code>, <code>login.microsoftonline.com</code>.</li>
<li><strong>Everything else.</strong> Daily Mail, New York Post and Decider hosts, plus ad-exchange and ad-verification hosts such as <code>fastlane.rubiconproject.com</code>, <code>match.adsrvr.org</code> and <code>cdn.doubleverify.com</code>.</li>
<li><strong>Format.</strong> Host names only, no page paths or titles.</li>
</ul>
</div>
</div>''',
 'One page of the web-activity records the Secret Service released for Ronald L. Rowe Jr., then its deputy director, in response to request 20240110. '
 'Rows are timestamped Oct. 4 and Oct. 10, 2023, within the request’s October 2023 window. Yellow highlighting appears on the page as photographed. '
 'By the author’s count, the agency mailed the records on paper, about 500 pages. Select the image to enlarge it.'))

# ---------- Fig. 2: loop ----------
LOOP = [
 ("map", "Map", "Find the agency’s Microsoft 365 tenant with public DNS and Microsoft’s sign-in metadata.", "unitedstatessecretservice-my.sharepoint.com"),
 ("name", "Name", "Identify the custodian by name and title from bios, press releases and FOIA logs.", "Deputy Director Ronald L. Rowe Jr."),
 ("request", "Request", "Ask for the custodian’s web logs, SharePoint and OneDrive documents, and Teams messages.", "“The last 100 documents edited by the custodian”"),
 ("mine", "Mine", "Read the release for new site names, hosts, offices and custodians, then map again.", "“SP 2016 Audit Logs,” p. 116"),
]
lp = "\n".join(f'<li class="lp-node" data-step="{k}"><span class="lp-n">{i+1}</span> <strong>{t}.</strong> {e(dsc)} <span class="lp-ex">Example: <code>{e(ex)}</code></span></li>' for i,(k,t,dsc,ex) in enumerate(LOOP))
w("loop", fig("loop", "Interactive · method", "The OSINT–FOIA loop",
 f'''<div class="lp-stage" aria-hidden="true"></div>
<div class="ixm-controls lp-controls" hidden><button type="button" class="btn" data-lp="prev">← Back</button><button type="button" class="btn btn-primary" data-lp="next">Next step →</button><span class="lp-status" aria-live="polite"></span></div>
<ol class="lp-list">
{lp}
</ol>''',
 'Each release becomes the starting point for the next round of research. Examples are from this guide’s Secret Service requests. Use the buttons or the arrow keys to step through the loop.'))

# ---------- CLI box ----------
w("cli", '''<aside class="cli-box" aria-label="For the command line">
<p class="cli-h">For the command line</p>
<p>Three public lookups. None of them touches the agency’s servers.</p>
<pre><code># 1. Does the SharePoint name exist? (DNS-over-HTTPS; NXDOMAIN means no)
curl -s "https://dns.google/resolve?name=unitedstatessecretservice.sharepoint.com&amp;type=A"

# 2. Which Microsoft tenant signs in this email domain, and in which cloud?
curl -s "https://login.microsoftonline.com/secretservice.gov/v2.0/.well-known/openid-configuration" \\
  | jq -r .issuer,.tenant_region_sub_scope

# 3. Does the tenant's original name map to the same tenant?
curl -s "https://login.microsoftonline.com/unitedstatessecretservice.onmicrosoft.com/v2.0/.well-known/openid-configuration" \\
  | jq -r .issuer</code></pre>
<p>If the issuer lines match, the domains share one tenant. A <code>GCC</code> sub-scope marks Microsoft’s government community cloud.</p>
</aside>
''')

# ---------- Fig. 3: SharePoint host finder ----------
dns = {}
with open(POST / "docs" / "dns-check-2026-10-20.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f): dns[r["hostname"].lower()] = r["dns_result"].startswith("resolves")
with open(POST / "docs" / "federal-foia-sharepoint-hostnames.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.reader(f))
hdr, data = rows[0], rows[1:]
COLS = ["Base", "Personal (-my)", "Sub-agency", "Office", "Admin"]
MISMATCH = {  # (sheet row, column letter): hyperlink target stored in the XLSX cell
 (334,"C"):"usps365-my.sharepoint.com",(335,"C"):"usps365-my.sharepoint.com",(336,"C"):"usps365-my.sharepoint.com",
 (338,"C"):"dcgovict-my.sharepoint.com",(343,"C"):"uscc-my.sharepoint.com",(372,"C"):"fmcsgov-my.sharepoint.com",
 (362,"D"):"usepa.sharepoint.com",(381,"D"):"imls365.sharepoint.com",(398,"D"):"oge.sharepoint.com",(405,"D"):"osc.sharepoint.com"}
NOTES = {
 107: 'Sheet lists <code>usss.sharepoint.com</code>, which has no DNS record. The live Secret Service tenant is <code>unitedstatessecretservice.sharepoint.com</code> (and <code>-my</code>), the hosts named in the author’s request and in the Rowe log. <code>usdhs</code> is DHS headquarters’ tenant.',
 108: 'Agency name is wrong in the sheet: it is the Cybersecurity and <em>Infrastructure</em> Security Agency. The listed <code>cisa</code> hosts have no DNS record.',
 115: 'Not a component: this row is a FOIA.gov menu option captured with the list.',
 200: 'The Office host <code>doamspp</code> is a typo for <code>doimspp</code> and carries a stray quotation mark; <code>doamspp</code> has no DNS record.',
 338: 'D.C. government. It answers requests under the D.C. FOIA, not the federal FOIA.',
 343: 'The U.S. Chamber of Commerce is a private business group, not a federal agency. FOIA does not apply to it.',
}
def hosts_of(cell):
    out = []
    for tok in re.split(r"[,\s]+", cell.strip()):
        if not tok: continue
        h = re.sub(r"^https?://", "", tok).split("/")[0].strip('"\'').lower()
        if h: out.append((tok, h))
    return out
import json
depts, recs = {}, []
n_rows_dns = {"all":0,"some":0,"none":0,"nohost":0}
for i, r in enumerate(data):
    rown = i + 2
    title, tag = r[0], r[1]
    dept = tag or "Independent / untagged"
    depts[dept] = depts.get(dept, 0) + 1
    cols, okc, tot = [], 0, 0
    for ci, (lab, val) in enumerate(zip(COLS, r[2:7])):
        if not val.strip(): continue
        hs = []
        for raw, h in hosts_of(val):
            st = "ok" if dns.get(h) else ("nx" if h in dns else "na")
            tot += 1; okc += st == "ok"
            hs.append([raw, h, st])
        cols.append([lab, hs, MISMATCH.get((rown, "CDEFG"[ci]), "")])
    st = "nohost" if tot == 0 else ("all" if okc == tot else ("none" if okc == 0 else "some"))
    n_rows_dns[st] += 1
    notes = [NOTES[rown]] if rown in NOTES else []
    if any(k[0] == rown for k in MISMATCH): notes.append("The cell’s hyperlink and its displayed text name different hosts.")
    if st == "none": notes.append("No listed host resolves.")
    recs.append([rown, title, tag, cols, notes, st])
BADGE = {"ok": "resolves", "nx": "no DNS record", "na": "not checked"}
def hf_row(rec):
    rown, title, tag, cols, notes, st = rec
    dept = tag or "Independent / untagged"
    cells = "".join(f'<span class="hf-col"><span class="hf-lab">{lab}</span> ' + "".join(
        f'<span class="hf-h hf-{hst}"><code>{e(raw)}</code> <span class="hf-b">{BADGE[hst]}</span></span>' for raw, h, hst in hs)
        + (f'<span class="hf-mm">Cell link points to <code>{e(mm)}</code></span>' if mm else "") + "</span>" for lab, hs, mm in cols)
    return (f'<tr data-dept="{e(dept)}" data-dns="{st}" data-note="{1 if notes else 0}"><td class="hf-row">{rown}</td>'
            f'<td><strong>{e(title)}</strong><span class="hf-dept">{e(dept)}</span></td>'
            f'<td>{cells or "<span class=hf-none>No hosts listed</span>"}</td><td class="hf-note">{"".join(f"<p>{n}</p>" for n in notes)}</td></tr>')
# Static HTML carries the DHS rows and every row with a note; usss.js loads the full table from JSON.
static = [r for r in recs if r[2] == "Department of Homeland Security" or r[4]]
trs = [hf_row(r) for r in static]
(POST / "assets" / "hostfinder-data.json").write_text(json.dumps({"checked": "2026-10-20", "rows": recs}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
HF_STATIC = len(static)
n_hosts = len(dns); n_ok = sum(dns.values())
opts = "".join(f'<option value="{e(k)}">{e(k)} ({v})</option>' for k, v in sorted(depts.items(), key=lambda kv: (kv[0].startswith("Independent"), kv[0])))
w("hostfinder", fig("hostfinder", "Interactive · searchable table", "Federal FOIA components and their SharePoint hostnames",
 f'''<div class="hf-sum"><p><span class="fe-big">{len(data)}</span> rows</p><p><span class="fe-big">{n_hosts}</span> unique hosts</p><p><span class="fe-big fe-blue">{n_ok}</span> resolve</p><p><span class="fe-big fe-red">{n_hosts-n_ok}</span> no DNS record</p></div>
<div class="ixm-controls hf-controls" hidden>
<label class="ixm-search"><span class="sr-only">Search components or hostnames</span><input type="search" placeholder="Search agency or hostname" data-hf="q"></label>
<label><span class="sr-only">Department</span><select data-hf="dept"><option value="">All departments</option>{opts}</select></label>
<div class="ixm-chips" role="group" aria-label="Filter rows"><button type="button" class="chip" data-hf-f="all" aria-pressed="true">All</button><button type="button" class="chip" data-hf-f="note" aria-pressed="false">Rows with notes</button><button type="button" class="chip" data-hf-f="none" aria-pressed="false">No resolving host</button></div>
<span class="hf-count" aria-live="polite"></span>
</div>
<p class="hf-static-note">Showing the {HF_STATIC} Homeland Security rows and rows with notes. The full table of {len(data)} rows is in the <a href="{D}federal-foia-sharepoint-hostnames.csv">CSV</a>.</p>
<section class="ixm-table hf-scroll" tabindex="0" aria-label="SharePoint hostname table" data-src="{A}hostfinder-data.json">
<table class="hf-table"><thead><tr><th scope="col">Row</th><th scope="col">Component</th><th scope="col">Hostnames in the sheet, with DNS check</th><th scope="col">Notes</th></tr></thead><tbody>
{"".join(trs)}
</tbody></table></section>
<p class="hf-dl">Compiled by Redwing Technologies. Download the data unaltered: <a href="{D}federal-foia-sharepoint-hostnames.xlsx">XLSX</a> · <a href="{D}federal-foia-sharepoint-hostnames.csv">CSV</a> · DNS results: <a href="{D}dns-check-2026-10-20.csv">CSV</a></p>''',
 'Component names, departments and hostnames are shown as they appear in the sheet; row numbers match the XLSX. DNS badges record a passive lookup on Oct. 20, 2026: '
 '“resolves” means the name exists in Microsoft’s DNS, not that the agency owns it. “No DNS record” means the name did not exist that day. Hostnames are shown as text, not links.'))
HF_STATS = dict(rows=len(data), hosts=n_hosts, ok=n_ok, nx=n_hosts-n_ok, rowdns=n_rows_dns)

# ---------- Fig. 4: where Microsoft 365 keeps it ----------
TEAMS = "https://learn.microsoft.com/en-us/purview/edisc-search-teams"
META = "https://learn.microsoft.com/en-us/purview/edisc-ref-document-metadata-fields"
AUD = "https://learn.microsoft.com/en-us/purview/audit-log-activities"
M3 = [
 ("1:1 chats", "“Messages in 1:1 chats are stored in the Exchange Online mailbox of all chat participants.”", "The custodian’s Exchange Online mailbox", TEAMS),
 ("Group chats", "“Messages in group chats are stored in the Exchange Online mailbox of all chat participants.”", "The custodian’s Exchange Online mailbox", TEAMS),
 ("Files shared in chats", "“Files shared in a 1:1 chat are stored in the OneDrive account of the person who shared the file.”", "The custodian’s OneDrive (<code>[tenant]-my.sharepoint.com</code>)", TEAMS),
 ("Standard channel posts", "“All channel messages and posts are stored in the Exchange Online mailbox associated with the team.”", "The team’s mailbox, by team name", TEAMS),
 ("Channel files", "“Files shared in a channel are stored in the SharePoint site associated with the team.”", "The team’s SharePoint site", TEAMS),
 ("Who created or edited a document", "eDiscovery metadata includes “Created by” (“Created by value from SharePoint”) and “Last modified by” (“The user who last modified the document”).", "SharePoint and OneDrive, sorted by last-modified date", META),
 ("File activity", "The audit log records “Accessed file” (<code>FileAccessed</code>), “Modified file” (<code>FileModified</code>) and “Uploaded file” (<code>FileUploaded</code>) events.", "Audit records for the custodian’s account, if retained", AUD),
]
m3 = "\n".join(f'<tr><th scope="row">{a}</th><td data-label="What Microsoft says">{b}</td><td data-label="Name it in the request as">{c}</td><td data-label="Source"><a href="{u}">Microsoft Learn</a></td></tr>' for a,b,c,u in M3)
w("m365", fig("m365", "Reference · Microsoft documentation", "Where Microsoft 365 keeps it",
 f'''<div class="ixm-table"><table class="m3-table"><thead><tr><th scope="col">Record</th><th scope="col">What Microsoft says</th><th scope="col">Name it in the request as</th><th scope="col">Source</th></tr></thead><tbody>
{m3}
</tbody></table></div>''',
 'Quotes are from Microsoft’s eDiscovery and audit documentation. Microsoft says Teams data itself lives in Azure Cosmos DB and Exchange keeps the compliance copies eDiscovery searches. How long audit records are kept depends on the agency’s license and settings.'))

# ---------- Fig. 6: release explorer ----------
# Page structure from the PDF footers: 44 statement fragments on pp. 1-105, sitemap on pp. 106-117.
STMT = []  # (first_page, [(pdf_page, "x of n"), ...])
_three = [1,6,9,12,15,18,21,26,31,34,37,40,43,46,50,54,57,60,63,66,71,75,78,81,85,88,91,94,97,103]
_one = [4,5,24,25,29,30,49,53,69,70,74,84,100]
for p in _three: STMT.append((p, [(p,"2 of 4"),(p+1,"3 of 4"),(p+2,"4 of 4")]))
for p in _one: STMT.append((p, [(p,"2 of 2")]))
STMT.append((101, [(101,"2 of 4"),(102,"4 of 4")]))
STMT.sort()
assert len(STMT) == 44 and sum(len(s[1]) for s in STMT) == 105, (len(STMT), sum(len(s[1]) for s in STMT))
SITE_NOTES = {106:"Header “USSS - Standard Sensitive Info”; URL column withheld, (b)(7)(E)",
              107:"Protective divisions named for former presidents",
              110:"Contains one OctoProbe redaction (an employee’s first name)",
              113:"“Freedom of Information Act” and “Enterprise Records and Knowledge Management Division” sites",
              114:"Contains one OctoProbe redaction (an employee’s first name)",
              116:"“SP 2016 Audit Logs” and “Travel Card Portal” sites",
              117:"Last page, about a dozen rows"}
def tile(p, cls, label):
    return f'<li><a class="pg {cls}" href="{REL}#page={p}" aria-label="{e(label)}" title="{e(label)}">{p}</a></li>'
st_tiles = []
for first, pages in STMT:
    for p, xn in pages:
        acct = xn == "4 of 4"
        st_tiles.append(tile(p, "st" + (" acct" if acct else "") + (" gap" if p == 102 else ""),
            f"PDF page {p}: card statement page {xn}" + (", masked account line" if acct else "") + (". Page 3 of this statement is not in the release" if p == 102 else "") + ". Content blacked out."))
sm_tiles = [tile(p, "sm" + (" key" if p in SITE_NOTES else ""), f"PDF page {p}: SharePoint sitemap" + (f". {SITE_NOTES[p]}" if p in SITE_NOTES else "")) for p in range(106,118)]
w("explorer", fig("explorer", "Interactive · release explorer", "All 117 pages of the April 2025 release",
 f'''<div class="fe-sum"><p><span class="fe-big">105</span> statement pages</p><p><span class="fe-big fe-red">0</span> transactions visible</p><p><span class="fe-big fe-blue">12</span> sitemap pages</p><p><span class="fe-big">~660</span> site names, 0 URLs</p></div>
<div class="ixm-controls rx-controls" hidden><div class="ixm-chips" role="group" aria-label="Show pages">
<button type="button" class="chip" data-show="all" aria-pressed="true">All pages</button>
<button type="button" class="chip" data-show="st" aria-pressed="false">Card statements</button>
<button type="button" class="chip" data-show="sm" aria-pressed="false">Sitemap</button></div></div>
<p class="fe-legend"><span class="pg st">n</span> statement page <span class="pg st acct">n</span> last page, masked account line <span class="pg sm">n</span> sitemap page <span class="pg sm key">n</span> noted below</p>
<div class="fe-doc" data-g="st"><p class="fe-h">Item 3: card statements <span>pp. 1–105 · 44 statements · page 1 of each absent</span></p><ol class="fe-grid">{"".join(st_tiles)}</ol></div>
<div class="fe-doc" data-g="sm"><p class="fe-h">Item 4: SharePoint sitemap <span>pp. 106–117 · URL column withheld on every page</span></p><ol class="fe-grid">{"".join(sm_tiles)}</ol></div>
<p class="fe-detail" aria-live="polite">Hover or focus a page for details; select it to open the PDF at that page.</p>''',
 'Page structure is read from each page’s footer (“Page 2 of 4”). Items 1 and 2, the last 100 documents the custodian edited and created, have no pages in the release. Each square opens the hosted PDF at that page.'))

# ---------- docs table ----------
def size(fn):
    s = (POST / "docs" / fn).stat().st_size
    return f"{s/1e6:.1f} MB" if s > 1e6 else f"{round(s/1e3)} KB"
DOCROWS = [
 ("Secret Service FOIA release, April 2025 request (117 pp.)", "U.S. Secret Service", "Request received April 21, 2025", "usss-foia-release-two-redactions.pdf", "PDF, image only", "Two OctoProbe redactions, pp. 110 and 114; otherwise as released"),
 ("Final response letter, opening paragraphs", "U.S. Secret Service", "2025", "usss-final-response-excerpt.png", "PNG", "Excerpt only; file metadata removed"),
 ("Browser-history page, request 20240110 (photo)", "U.S. Secret Service", "Rows dated Oct. 4 and 10, 2023", "../assets/rowe-browser-history-zoom.jpg", "JPEG", "Photograph of one printed page"),
 ("Federal FOIA components and SharePoint hostnames", "Redwing Technologies", "Checked Oct. 20, 2026", "federal-foia-sharepoint-hostnames.xlsx", "XLSX", "Unaltered"),
 ("Same table as CSV", "Redwing Technologies", "", "federal-foia-sharepoint-hostnames.csv", "CSV", "Columns A–G, values as in the XLSX"),
 ("DNS check results for every hostname in the table", "OctoProbe News", "Oct. 20, 2026", "dns-check-2026-10-20.csv", "CSV", "Passive lookups"),
]
def fsize(fn):
    p = (POST / "docs" / fn).resolve()
    s = p.stat().st_size
    return f"{s/1e6:.1f} MB" if s > 1e6 else f"{round(s/1e3)} KB"
def href(f): return A + f[len("../assets/"):] if f.startswith("../assets/") else D + f
tr = "\n".join(f'<tr><td data-label="Document"><a href="{href(f)}">{e(t)}</a></td><td data-label="Source">{a}</td><td data-label="Date">{dt or "—"}</td><td data-label="File">{fmt}, {fsize(f)}</td><td data-label="Notes">{n}</td></tr>' for t,a,dt,f,fmt,n in DOCROWS)
tr += f'\n<tr><td data-label="Document"><a href="{LOG}">Secret Service FOIA Log, FY 2024</a> (see pp. 12–13)</td><td data-label="Source">U.S. Secret Service</td><td data-label="Date">Fiscal 2024</td><td data-label="File">PDF, on secretservice.gov</td><td data-label="Notes">Linked, not hosted</td></tr>'
w("docs-table", f'<div class="table-wrap docs-tw"><table class="docs-table"><thead><tr><th scope="col">Document</th><th scope="col">Source</th><th scope="col">Date</th><th scope="col">File</th><th scope="col">Notes</th></tr></thead><tbody>\n{tr}\n</tbody></table></div>\n')

# ---------- glossary ----------
GL = [
 ("Tenant", "An organization’s Microsoft 365 instance. Its original name forms the SharePoint address.", '<a href="https://learn.microsoft.com/en-us/sharepoint/change-your-sharepoint-domain-name">Microsoft Learn</a>'),
 ("Custodian", "The person whose records are searched. Agencies search by custodian, so a name and title usually suffice.", "FOIA practice"),
 ("OneDrive “-my” host", "The personal-storage address, <code>[tenant]-my.sharepoint.com</code>. Files shared in Teams chats land here.", f'<a href="{TEAMS}">Microsoft Learn</a>'),
 ("GCC", "Government Community Cloud, Microsoft’s U.S. government environment. Shown in the tenant’s public sign-in metadata.", '<a href="https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc">Microsoft Learn</a>'),
 ("Compliance copy", "The copy of a Teams message that Exchange Online keeps for eDiscovery.", f'<a href="{TEAMS}">Microsoft Learn</a>'),
 ("Audit log", "Microsoft’s record of user actions such as <code>FileAccessed</code> and <code>FileModified</code>.", f'<a href="{AUD}">Microsoft Learn</a>'),
 ("Hub site", "A SharePoint site that groups related sites. The released sitemap lists a hub for each site.", "Sitemap, pp. 106–117"),
 ("(b)(6)", "Exemption for files whose release would be “a clearly unwarranted invasion of personal privacy.”", '<a href="https://www.law.cornell.edu/uscode/text/5/552">5 U.S.C. § 552(b)(6)</a>'),
 ("(b)(7)(C)", "Law-enforcement records whose release “could reasonably be expected to constitute an unwarranted invasion of personal privacy.”", '<a href="https://www.law.cornell.edu/uscode/text/5/552">§ 552(b)(7)(C)</a>'),
 ("(b)(7)(E)", "Law-enforcement records that “would disclose techniques and procedures for law enforcement investigations or prosecutions.”", '<a href="https://www.law.cornell.edu/uscode/text/5/552">§ 552(b)(7)(E)</a>'),
]
gt = "\n".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a,b,c in GL)
w("glossary", f'<div class="table-wrap"><table><thead><tr><th>Term</th><th>Meaning</th><th>Source</th></tr></thead><tbody>\n{gt}\n</tbody></table></div>\n')

# ---------- related ----------
w("related", '''<aside aria-label="Related reading" class="related-reading">
<h2>Related Reading</h2>
<ul>
<li><a href="/blog/centcom-war-orders-anvil-chart-foia/">The Only Public Map of CENTCOM’s War Orders Is Dated 2022</a></li>
<li><a href="/blog/cefc-china-energy-pla-base-311-public-record/">CEFC, PLA Base 311, and the Long Gap from FBI Surveillance to Designation</a></li>
</ul>
</aside>
''')
