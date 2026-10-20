#!/usr/bin/env python3
"""Generate the post's figure-style interactive modules (static, readable HTML;
assets/adtech.js enhances them). All data is illustrative except the FOIA page
maps, document facts and timeline events, which are sourced."""
import json, html, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULES = {}  # name -> HTML, read by scripts/build-adtech-post.py
SLUG = "dhs-phone-location-data-legal-opinion-foia"
D = f"/blog/{SLUG}/docs/"
A = f"/blog/{SLUG}/assets/"
e = html.escape
def ei(t):  # escape, then *Case* -> <em>Case</em> (case names)
    return re.sub(r"\*([^*\n]+)\*", r"<em>\1</em>", e(t))

def fig(mid, kicker, title, body, caption, fallback=True, extra_cls=""):
    fbp = ROOT / "blog" / SLUG / "assets" / f"fallback-{mid}.png"
    if fallback and fbp.exists():
        from PIL import Image
        fw, fh = Image.open(fbp).size
        fw, fh = fw // 2, fh // 2
    else:
        fw, fh = 1600, 900
    fb = (f'<img class="ix-fallback" src="{A}fallback-{mid}.png" alt="Static view of the interactive figure: {e(title)}" '
          f'width="{fw}" height="{fh}" loading="lazy" decoding="async">') if fallback else ""
    return (f'<figure class="ixm-fig" id="fig-{mid}">\n<div class="ixm {extra_cls}" data-ixm="{mid}">\n'
            f'<div class="ixm-head"><span class="ixm-kicker">{e(kicker)}</span><span class="ixm-title">{e(title)}</span></div>\n'
            f'{fb}<div class="ixm-live">\n{body}\n</div>\n</div>\n<figcaption>{caption}</figcaption>\n</figure>\n')

def w(name, s): MODULES[name] = s

# ---------- cover ----------
w("cover", f'<figure><img fetchpriority="high" decoding="async" src="{A}cover.png?v=2" width="2400" height="1260" '
  'alt="Illustration: bright street map of the Paso del Norte International Bridge over the Rio Grande between El Paso, Texas, and Ciudad Juárez, Mexico, with a red pin on the bridge, a U.S. flag, and a red line to a phone graphic showing an ad slot and a fictional advertising ID" '
  'title="87 of 93 pages withheld"><figcaption>The Paso del Norte port of entry on the U.S.–Mexico border at El Paso, Texas, linked to an example phone ad slot. '
  'The app, advertising ID and coordinates shown are fictional. Illustration: OctoProbe News; map © OpenStreetMap contributors; U.S. flag via Wikimedia Commons (public domain).</figcaption></figure>\n')

# ---------- takeaways ----------
w("takeaways", '''<aside aria-label="Key takeaways" class="key-takeaways">
<h2>Key Takeaways</h2>
<ul>
<li><a href="#what-did-dhs-lawyers-say-about-buying-phone-location-data">DHS released one page of its Sept. 25, 2020 legal opinion on advertising-ID location data. The other 23 pages, the legal analysis, were withheld under FOIA exemption (b)(5).</a></li>
<li><a href="#what-are-dhs-and-the-fbi-still-withholding">Across five DHS legal memos in the same release, 87 of 93 pages were withheld in full.</a></li>
<li><a href="#how-does-the-government-buy-it">The inspector general counted more than 55,000 CBP queries in fiscal 2019–2020 and more than 16,000 ICE queries in fiscal 2020, and found ICE used the data from September 2018 without an approved privacy assessment.</a></li>
<li><a href="#how-does-the-government-buy-it">The FBI bought one Venntel Portal seat, with “12,000 queries per year,” through a reseller in February 2020. Why it wanted the data is classified until 2045.</a></li>
<li><a href="#who-else-uses-it-including-america-s-adversaries">Central Command told Congress in April 2026 it had threat reports of adversaries exploiting commercial location data to target U.S. personnel.</a></li>
<li><a href="#primary-documents">Read all six primary documents, hosted in full.</a></li>
</ul>
</aside>
''')

# ---------- static FOIA figures ----------
def imgfig(name, src, wdt, hgt, alt, cap):
    w(name, f'<figure class="fig-pad doc-page"><img src="{A}{src}" width="{wdt}" height="{hgt}" alt="{e(alt)}" loading="lazy" decoding="async"><figcaption>{cap}</figcaption></figure>\n')
imgfig("fig-foia-p1", "foia1-p001.png", 1275, 1650,
  "First page of the DHS Office of the General Counsel memo dated September 25, 2020, subject Legal Implications of Advertising Identifier Geolocation Data Use by CBP and ICE, with the executive summary followed by a large (b)(5) withholding stamp",
  f'The only released page of DHS’s Sept. 25, 2020 opinion on advertising-ID location data. Pages 2–24 were withheld in full. Source: DHS FOIA 2024-HQFO-00696, Bates 000001 (<a href="{D}dhs-ogc-adid-legal-opinion-2020-09-25.pdf#page=1">PDF p. 1</a>).')
imgfig("fig-fbi-rfq", "fbi-p020.png", 1271, 760,
  "FBI request for quotes for one Venntel Portal user annual fee that includes 12,000 queries per year",
  f'The FBI’s request for quotes: one Venntel Portal seat, 12,000 queries a year. Source: FBI FOI/PA 1491075-000 (<a href="{D}fbi-foipa-1491075-000-venntel-portal-contract.pdf#page=20">PDF p. 20</a>).')
imgfig("fig-foia-st", "foia3-p002.png", 1275, 1650,
  "Second page of the DHS December 6, 2021 Privacy Act memo quoting subsection (e)(7) above a (b)(5) withholding stamp",
  f'One of only two text pages in the Dec. 6, 2021 Privacy Act memo to DHS’s Science and Technology Directorate. Source: DHS FOIA 2024-HQFO-00696, Bates 000037 (<a href="{D}dhs-ogc-privacy-act-e7-st-memo-2021-12-06.pdf#page=2">PDF p. 2</a>).')

# ---------- 56-field explorer ----------
SRC = {"bid": "Bid request (OpenRTB)", "lookup": "Device-database lookup", "sdk": "App SDK or carrier side", "derived": "Broker enrichment"}
LAY = {"loc": "Location and time", "id": "Identifiers", "net": "Network", "hw": "Device hardware", "sw": "Software and context"}
F = [  # (label from list, cleaned label, layer, source, note)
 ("Lat / long","Latitude and longitude","loc","bid","OpenRTB device.geo.lat / lon; precision depends on geo.type"),
 ("Timestamp","Timestamp of the observation","loc","derived","Logged by the exchange or SDK when the record is created"),
 ("Places","Places visited","loc","derived","Inferred by matching coordinates to points of interest"),
 ("Languages","Device language","sw","bid","OpenRTB device.language"),
 ("Originating application","Originating app","sw","bid","OpenRTB app.bundle / app.name"),
 ("User agent","User agent string","sw","bid","OpenRTB device.ua"),
 ("IP address","IP address","net","bid","OpenRTB device.ip / ipv6"),
 ("Port","Source port","net","sdk","Network logs; not an OpenRTB field"),
 ("Hostname","Reverse-DNS hostname","net","derived","Looked up from the IP address"),
 ("Domain","Network domain","net","derived","Looked up from the IP address"),
 ("ISP","Internet provider or carrier","net","bid","OpenRTB device.carrier; or IP lookup"),
 ("Network types","Connection type","net","bid","OpenRTB device.connectiontype (Wi-Fi, 4G, 5G …)"),
 ("Network interfaces","Network interfaces","net","lookup","Device catalogue property"),
 ("MAC address","Wi-Fi MAC address","id","sdk","Not in OpenRTB; readable only by some SDKs"),
 ("Historical IDs","Prior advertising IDs","id","derived","Linked by brokers after a user resets the ID"),
 ("IMEI","IMEI hardware serial","id","sdk","Not in OpenRTB"),
 ("ICCID","SIM card number (ICCID)","id","sdk","Not in OpenRTB"),
 ("ESN","Electronic serial number","id","sdk","Legacy CDMA identifier; not in OpenRTB"),
 ("TACs","Type Allocation Code","hw","lookup","First 8 digits of an IMEI; identifies the model"),
 ("Type","Device type","hw","bid","OpenRTB device.devicetype"),
 ("Vendor","Device manufacturer","hw","bid","OpenRTB device.make"),
 ("Alt model","Alternate model name","hw","lookup","Device catalogue property"),
 ("Names","Names (a category some exchanges report)","hw","lookup","Not reported by every exchange"),
 ("Released","Year released","hw","lookup","Device catalogue property"),
 ("Primary screen","Screen size and density","hw","bid","OpenRTB device.w / h / ppi / pxratio"),
 ("Camera capabilities","Camera capabilities","hw","lookup","Device catalogue property"),
 ("Audio chips","Audio chipset","hw","lookup","Device catalogue property"),
 ("Baseband chips","Baseband (modem) chipset","hw","lookup","Device catalogue property"),
 ("Chip connectivity","Chipset connectivity","hw","lookup","Device catalogue property"),
 ("Chip manufacturer","Chipset vendor","hw","lookup","Device catalogue property"),
 ("CPU manufacturer","CPU vendor","hw","lookup","Device catalogue property"),
 ("CPU speed","CPU speed","hw","lookup","Device catalogue property"),
 ("CPU type","CPU type","hw","lookup","Device catalogue property"),
 ("Internal memory size","RAM","hw","lookup","Device catalogue property"),
 ("Internal storage size","Internal storage","hw","lookup","Device catalogue property"),
 ("Removable service","Expandable (removable) storage","hw","lookup","Device catalogue property; listed as “removable service” in the source"),
 ("SIM card","SIM slots","hw","lookup","Device catalogue property"),
 ("Telephony","Telephony capabilities","hw","lookup","Device catalogue property"),
 ("Frequencies","Radio frequency bands","hw","lookup","Device catalogue property"),
 ("Bluetooth types/models","Bluetooth version","hw","lookup","Device catalogue property"),
 ("Wifi versions","Wi-Fi standards","hw","lookup","Device catalogue property"),
 ("Wifi capabilities","Wi-Fi capabilities","hw","lookup","Device catalogue property"),
 ("Wifi security types","Wi-Fi security types","hw","lookup","Device catalogue property"),
 ("Cable usage","Cable usage (a category some exchanges report)","hw","lookup","Not reported by every exchange"),
 ("Electronic capabilities","Other hardware capabilities","hw","lookup","Device catalogue property (e.g., NFC)"),
 ("Input capabilities","Input methods","hw","lookup","Device catalogue property (touch, keys)"),
 ("Output capabilities","Output capabilities","hw","lookup","Device catalogue property"),
 ("Keyboard types","Keyboard types","hw","lookup","Device catalogue property"),
 ("OS","Operating system","sw","bid","OpenRTB device.os"),
 ("OS version","OS version","sw","bid","OpenRTB device.osv"),
 ("OS vendor","OS vendor","sw","lookup","Device catalogue property"),
 ("Web browser","Web browser","sw","derived","Parsed from the user agent"),
 ("Web browser vendor","Browser vendor","sw","derived","Parsed from the user agent"),
 ("Email services","Supported email services","sw","lookup","Device catalogue property"),
 ("Email security types","Supported email security","sw","lookup","Device catalogue property"),
 ("Classifiers","Audience segments","sw","derived","Broker-assigned interest or behavior labels"),
]
assert len(F) == 56, len(F)
lis = "\n".join(
  f'<li data-layer="{l}" data-src="{s}" data-q="{e((a+" "+b+" "+n).lower())}"><span class="fx-n">{i+1:02d}</span><span class="fx-name">{e(b)}</span>'
  f'<span class="fx-tags"><span class="fx-tag fx-l-{l}">{LAY[l]}</span><span class="fx-tag fx-s-{s}">{SRC[s]}</span></span><span class="fx-note">{e(n)}</span></li>'
  for i, (a, b, l, s, n) in enumerate(F))
layers = "".join(f'<li data-layer="{k}"><span class="ly-name">{v}</span><span class="ly-count"></span></li>' for k, v in LAY.items())
w("fields", fig("fields", "Interactive · data-field explorer", "What ad exchanges may measure when serving an ad: 56 possible fields",
 f'''<div class="fx-wrap">
<div class="fx-stack"><p class="ixm-sub">Record layers</p><ol class="fx-layers">{layers}</ol></div>
<div class="fx-main">
<div class="ixm-controls fx-controls" hidden>
<label class="ixm-search"><span class="sr-only">Search fields</span><input type="search" placeholder="Search fields (e.g., IMEI, screen)" aria-controls="fx-list"></label>
<div class="ixm-chips" role="group" aria-label="Filter by source"><button type="button" class="chip" data-src="all" aria-pressed="true">All sources</button>{"".join(f'<button type="button" class="chip" data-src="{k}" aria-pressed="false">{v}</button>' for k,v in SRC.items())}</div>
</div>
<p class="fx-count" aria-live="polite">56 fields</p>
<ol class="fx-list" id="fx-list">
{lis}
</ol></div></div>''',
 'Possible categories ad exchanges may measure when serving an ad, compiled across multiple exchanges as a wide lens; not every exchange measures every field. Where each typically comes from is per the IAB Tech Lab’s '
 '<a href="https://github.com/InteractiveAdvertisingBureau/openrtb2.x/blob/main/2.6.md">OpenRTB 2.6</a> specification and public device-catalogue documentation '
 '(<a href="https://www.deviceatlas.com/resources/available-properties">DeviceAtlas</a>). Which fields a given exchange or broker handles varies. Click a layer or a source to filter.', fallback=False))

# ---------- auction stepper ----------
STEPS = [
 ("App loads an ad slot", "A fictional weather app with location permission opens. Its ad SDK asks an exchange to fill a banner."),
 ("SDK builds the request", "The SDK attaches the advertising ID, device details, IP address and, if permitted, a GPS fix."),
 ("Exchange sends a bid request", "The exchange packages an OpenRTB bid request and sends a copy to every connected bidder, here 12."),
 ("Bidders read every field", "Each bidder sees device.ifa and device.geo whether or not it bids. Losing bidders keep what they received."),
 ("One bidder wins", "The winner’s ad is shown, typically within a fraction of a second. The other 11 copies remain in other systems."),
 ("Copies reach a broker", "A bidder or SDK partner sells or shares the records with a data broker, which joins them by advertising ID."),
 ("Broker sells access", "The broker licenses a searchable portal or data feed to customers, including government buyers through resellers."),
]
st = "\n".join(f'<li data-step="{i}"><strong>{e(a)}.</strong> {e(b)}</li>' for i, (a, b) in enumerate(STEPS))
w("auction", fig("auction", "Interactive · ad-auction stepper", "How one ad slot becomes a location record",
 f'''<div class="au-stage ix-vis" aria-hidden="true"></div>
<div class="ixm-controls au-controls" hidden>
<button type="button" class="btn au-prev" aria-label="Previous step">← Back</button>
<button type="button" class="btn btn-primary au-play" aria-pressed="false">Play</button>
<button type="button" class="btn au-next" aria-label="Next step">Next →</button>
<span class="au-pos" aria-live="polite">Step 1 of {len(STEPS)}</span>
</div>
<ol class="au-steps">
{st}
</ol>
<div class="au-sdk">
<p class="ixm-sub">Inside the app: a typical SDK stack (hover a row)</p>
<div class="ixm-table"><table>
<thead><tr><th>Layer</th><th>What it does</th><th>Can read location?</th></tr></thead>
<tbody>
<tr data-hl="sdk-app"><td>App code</td><td>Weather forecasts (fictional app)</td><td>Yes, with permission</td></tr>
<tr data-hl="sdk-med"><td>Ad mediation SDK</td><td>Chooses which ad network fills the slot</td><td>Passes what the app shares</td></tr>
<tr data-hl="sdk-net"><td>Ad network SDK</td><td>Requests ads from an exchange</td><td>Sends geo in bid requests</td></tr>
<tr data-hl="sdk-loc"><td>Analytics or location SDK</td><td>Collects data for the kit’s maker</td><td>Yes, can report GPS directly</td></tr>
</tbody></table></div></div>''',
 'Illustrative flow; app, exchange, bidders and broker are generic. Field names from the IAB Tech Lab’s '
 '<a href="https://github.com/InteractiveAdvertisingBureau/openrtb2.x/blob/main/2.6.md">OpenRTB 2.6</a>. Use Play or the arrow buttons; motion is reduced if your system requests it.'))

# ---------- fan-out ----------
w("fanout", fig("fanout", "Interactive · fan-out calculator", "One phone, one day: how many copies of its location?",
 '''<div class="fo-vis ix-vis"><div class="fo-grid">
<div class="fo-in"><label for="fo-ads">Ad requests per day</label><output for="fo-ads">200</output><input id="fo-ads" type="range" min="20" max="600" step="10" value="200" data-k="ads"></div>
<div class="fo-in"><label for="fo-bid">Bidders per request</label><output for="fo-bid">12</output><input id="fo-bid" type="range" min="1" max="40" step="1" value="12" data-k="bid"></div>
<div class="fo-in"><label for="fo-geo">Share of requests with location</label><output for="fo-geo">40%</output><input id="fo-geo" type="range" min="0" max="100" step="5" value="40" data-k="geo"></div>
</div>
<div class="fo-out">
<p><span class="fo-big" data-o="day">960</span><span class="fo-lbl">location copies per day</span></p>
<p><span class="fo-big" data-o="month">28,800</span><span class="fo-lbl">per 30 days</span></p>
<p><span class="fo-big" data-o="pts">80</span><span class="fo-lbl">distinct positions per day (one per ad load with location)</span></p>
</div>
<div class="fo-bar" aria-hidden="true"></div></div>
<p class="fo-static">At the default assumptions (200 ad requests, 12 bidders, 40% with location), one phone generates about 960 copies of its position a day, or 28,800 over 30 days.</p>''',
 'Illustrative arithmetic, not a measurement: copies = ad requests × bidders × share carrying location. Real counts vary widely by app, platform and exchange. Drag the sliders to change the assumptions.'))

# ---------- precision ladder ----------
LAD = [
 ("L1","GPS / location services","5–20 m","geo.type = 1","Can place a phone at a single building or room."),
 ("L2","Wi-Fi or cell-assisted","20–100 m","SDK-reported","Usually identifies a block or a large building."),
 ("L3","IP address lookup","1–25 km","geo.type = 2","Often only a neighborhood, city or carrier hub."),
 ("L4","User-provided","Varies","geo.type = 3","A typed ZIP code or city; coarse and sometimes wrong."),
 ("L5","Country or region only","Region","geo.country / region","Useful for ad targeting, not for tracking."),
]
lad = "\n".join(f'<li data-lv="{i}" data-r="{r}"><button type="button" class="ld-btn" aria-pressed="{"true" if i==0 else "false"}"><span class="ld-k">{k}</span> <span class="ld-n">{e(n)}</span> <span class="ld-r">{e(r)}</span></button>'
                f'<span class="ld-d"><code>{e(c)}</code> {e(d)}</span></li>' for i,(k,n,r,c,d) in enumerate(LAD))
w("ladder", fig("ladder", "Interactive · precision ladder", "How precise is a location record?",
 f'<div class="ld-wrap"><ol class="ld-list">\n{lad}\n</ol><div class="ld-vis ix-vis" aria-hidden="true"></div></div>',
 'Typical accuracy ranges are approximate and illustrative. Location type codes are from OpenRTB 2.6’s <code>geo.type</code> list (1 = GPS/location services, 2 = IP address, 3 = user-provided). Select a level to compare its radius.'))

# ---------- device / pattern of life ----------
REC = [("AdID","3f2b9c1e-7d4a-4e0b-9a61-00000000a1b2"),("Latitude","0.012345"),("Longitude","0.023456"),("Timestamp (UTC)","2026-03-14 02:47:00"),
       ("Local offset","+00:00"),("Location type","GPS (geo.type 1)"),("IP address","198.51.100.23"),("App","Example Weather (fictional)"),("Device","Generic phone model")]
rec = "".join(f'<tr><td>{i+1:02d}</td><td>{e(a)}</td><td><code>{e(b)}</code></td></tr>' for i,(a,b) in enumerate(REC))
w("device", fig("device", "Interactive · pattern of life", "Thirty days of one fictional advertising ID",
 f'''<div class="ixm-controls dv-controls" hidden>
<div class="ixm-chips" role="group" aria-label="Map layers">
<button type="button" class="chip" data-layer="pts" aria-pressed="true">Location points</button>
<button type="button" class="chip" data-layer="path" aria-pressed="false">Daily path</button>
<button type="button" class="chip" data-layer="clusters" aria-pressed="true">Inferred places</button>
</div>
<div class="ixm-chips" role="group" aria-label="Time of day">
<button type="button" class="chip" data-tod="all" aria-pressed="true">All hours</button>
<button type="button" class="chip" data-tod="night" aria-pressed="false">Midnight–5 a.m.</button>
<button type="button" class="chip" data-tod="work" aria-pressed="false">Weekdays 9–5</button>
</div></div>
<div class="dv-map ix-vis" aria-hidden="true"></div>
<div class="dv-tip" role="status" aria-live="polite"></div>
<div class="dv-dwell" aria-hidden="true"></div>
<div class="dv-places" hidden><p class="ixm-sub">Inferred places (focus or tap)</p><div class="dv-place-btns"></div></div>
<p class="ixm-sub">One delivered record (illustrative)</p>
<div class="ixm-table"><table class="dv-rec"><thead><tr><th>#</th><th>Column</th><th>Example value</th></tr></thead><tbody>{rec}</tbody></table></div>''',
 'Generated data around placeholder coordinates near 0°, 0°, in open ocean, so they match no real place; streets and places are invented. The hourly dwell profile shows where the device sits at each hour across 30 days. Hover, tap or use the buttons to explore.'))

# ---------- bid request cross-section ----------
BR = [
 ("device.ifa","\"3f2b9c1e-7d4a-4e0b-9a61-00000000a1b2\"","The advertising ID, sent “in the clear (i.e., not hashed).”","id"),
 ("device.lmt","0","Limit-ad-tracking flag; 0 means tracking is unrestricted.","id"),
 ("device.ip","\"198.51.100.23\"","IP address; also resolves to a provider and rough place.","net"),
 ("device.geo.lat","0.012345","Latitude.","loc"),
 ("device.geo.lon","0.023456","Longitude.","loc"),
 ("device.geo.type","1","Location source: 1 = GPS/location services.","loc"),
 ("device.geo.accuracy","12","Estimated accuracy in meters.","loc"),
 ("device.make","\"ExampleCo\"","Manufacturer.","hw"),
 ("device.model","\"Phone X\"","Model.","hw"),
 ("device.os","\"Android\"","Operating system.","sw"),
 ("device.osv","\"15\"","OS version.","sw"),
 ("device.connectiontype","2","Connection: 2 = Wi-Fi.","net"),
 ("device.language","\"en\"","Device language.","sw"),
 ("app.bundle","\"com.example.weather\"","The app the ad slot belongs to (fictional).","sw"),
]
lines = "\n".join(f'<span class="br-line" data-f="{i}" data-g="{g}" tabindex="0"><span class="br-k">{e(k)}</span>: <span class="br-v">{e(v)}</span></span>' for i,(k,v,d,g) in enumerate(BR))
expl = "\n".join(f'<li data-f="{i}"><code>{e(k)}</code> {e(d)}</li>' for i,(k,v,d,g) in enumerate(BR))
w("bidrequest", fig("bidrequest", "Interactive · bid-request cross-section", "What a bidder receives in one request",
 f'''<div class="br-wrap"><div class="br-ring ix-vis" aria-hidden="true"></div><pre class="br-pre"><code>{lines}</code></pre></div>
<ul class="br-expl">
{expl}
</ul>''',
 'Simplified OpenRTB 2.6 bid request with fictional values; real requests carry more fields. Field meanings from the '
 '<a href="https://github.com/InteractiveAdvertisingBureau/openrtb2.x/blob/main/2.6.md">specification</a>. Hover or focus a line to see what it means.'))

# ---------- geofence ----------
w("geofence", fig("geofence", "Interactive · area search", "Draw a fence around a place, get a list of phones",
 '''<div class="gf-map ix-vis" aria-hidden="true"></div>
<div class="ixm-controls gf-controls" hidden>
<button type="button" class="btn gf-prev">← Earlier</button>
<span class="gf-win" aria-live="polite">Window: Saturday 9–10 a.m.</span>
<button type="button" class="btn gf-next">Later →</button>
<label class="gf-cum"><input type="checkbox" checked> Accumulate</label>
</div>
<div class="gf-res"><p class="ixm-sub">Query result</p><p class="gf-count" aria-live="polite">An area search returns every device seen inside the fence during the chosen window.</p><ul class="gf-list"></ul></div>''',
 'Fictional “community center” and generated devices on an invented street grid. An area search returns each advertising ID seen inside the polygon in the time window; a follow-up device search on any ID would show where it spends nights. Step through the windows to watch the list grow.'))

# ---------- two directions ----------
w("directions", fig("directions", "Interactive · two query directions", "Same data, two questions",
 '''<div class="ixm-controls dr-controls" hidden><div class="ixm-chips" role="group" aria-label="Query direction">
<button type="button" class="chip" data-dir="fwd" aria-pressed="true">Device → places</button>
<button type="button" class="chip" data-dir="rev" aria-pressed="false">Place → devices</button></div></div>
<div class="dr-vis ix-vis" aria-hidden="true"></div>
<div class="dr-text">
<p data-dir="fwd"><strong>Device → places (“device search”).</strong> Start with one advertising ID and a date range. The result is every place the phone was seen: home, work and everywhere between.</p>
<p data-dir="rev"><strong>Place → devices (“area search”).</strong> Start with a polygon and a time window. The result is every advertising ID seen inside, each of which can then be run as a device search.</p>
</div>''',
 'Illustrative, with generated data. Query names follow the EFF’s description of <a href="https://www.eff.org/deeplinks/2022/08/inside-fog-data-science-secretive-company-selling-mass-surveillance-local-police">Fog Reveal</a>. Toggle to switch direction.'))

# ---------- acquisition flow ----------
FLOW = [
 ("Phone app or ad slot","Apps and SDKs collect the ID with location; ad exchanges broadcast it in bid requests.",
  [("OpenRTB 2.6 (device.ifa, geo)","https://github.com/InteractiveAdvertisingBureau/openrtb2.x/blob/main/2.6.md"),("EFF: X-Mode paid apps about 3 cents per user per month","https://www.eff.org/deeplinks/2022/08/inside-fog-data-science-secretive-company-selling-mass-surveillance-local-police")]),
 ("Aggregator","Firms buy or ingest records from many apps and exchanges and join them by advertising ID.",
  [("FTC on Gravy Analytics: 17 billion signals a day","https://www.ftc.gov/news-events/news/press-releases/2024/12/ftc-takes-action-against-gravy-analytics-venntel-unlawfully-selling-location-data-tracking-consumers"),("Unacast incident fact sheet","https://cdn.prod.website-files.com/661d3eb71206816721de67f8/67c5dda5d34d66734fb2ab24_Unacast%20Incident%20Fact%20Sheet_03032025.pdf")]),
 ("Broker portal","A subsidiary packages the data as a web portal with area and device searches, priced per seat and query.",
  [("DHS S&T Venntel order: 5 users, 12,000 queries each","https://www.dhs.gov/sites/default/files/2021-12/Venntel%20Contract%20Document-ocr-_0.pdf#page=5"),("EFF: area and device searches","https://www.eff.org/deeplinks/2022/08/inside-fog-data-science-secretive-company-selling-mass-surveillance-local-police")]),
 ("Reseller and contract vehicle","An IT reseller sells the subscription under an existing governmentwide contract.",
  [("USAspending: FBI order to GovPlace, $22,346.37","https://www.usaspending.gov/award/CONT_AWD_15F06720F0000659_1549_NNG15SC77B_8000"),("FBI order, PDF p. 22",D+"fbi-foipa-1491075-000-venntel-portal-contract.pdf#page=22")]),
 ("Agency user","Analysts log in and run queries; the data is treated as purchased commercial information, without a warrant.",
  [("OIG-23-61: 55,000+ CBP queries","https://www.oig.dhs.gov/sites/default/files/assets/2023-09/OIG-23-61-Sep23-Redacted.pdf#page=13"),("DIA memo on *Carpenter*","https://www.wyden.senate.gov/imo/media/doc/011521%20CTD%20Discussion%20RFI%20Response.pdf")]),
]
fl = "\n".join(f'<li data-i="{i}"><button type="button" class="fl-btn" aria-expanded="{"true" if i==0 else "false"}"><span class="fl-n">{i+1}</span> {e(n)}</button>'
               f'<div class="fl-det"><p>{e(d)}</p><ul>{"".join(f"<li><a href=\"{e(u)}\">{ei(t)}</a></li>" for t,u in s)}</ul></div></li>' for i,(n,d,s) in enumerate(FLOW))
w("flow", fig("flow", "Interactive · acquisition path", "From an app to an agency, with the documents for each step",
 f'<ol class="fl-list">\n{fl}\n</ol>',
 'Stages generalized from the public record; each links to a document showing that step for a real transaction. Select a stage to see its sources.', fallback=False))

# ---------- timeline ----------
TL = [
 ("2012-09","platform","Apple introduces the IDFA with iOS 6.", "https://developer.apple.com/documentation/adsupport/asidentifiermanager/advertisingidentifier","Apple"),
 ("2016-01","military","Contractors testing ad data see phones move from U.S. bases to a cement factory in Syria (reported 2024).","https://www.wired.com/story/how-pentagon-learned-targeted-ads-to-find-targets-and-vladimir-putin/","Wired"),
 ("2018-06","law","Supreme Court decides *Carpenter v. United States*.","https://www.supremecourt.gov/opinions/17pdf/16-402_h315.pdf","Supreme Court"),
 ("2018-09","dhs","ICE begins using CTD without an approved privacy assessment.","https://www.oig.dhs.gov/sites/default/files/assets/2023-09/OIG-23-61-Sep23-Redacted.pdf#page=14","DHS OIG"),
 ("2019-06","dhs","DHS Privacy Office asks whether OGC ran a *Carpenter* analysis.","https://assets.aclu.org/live/uploads/legal-documents/DHS_HQ_21_09_Records.pdf#page=100","ACLU release"),
 ("2020-02","press","WSJ reports CBP and ICE buy Venntel location data.","https://www.wsj.com/articles/federal-agencies-use-cellphone-location-data-for-immigration-enforcement-11581078600","WSJ"),
 ("2020-02","fbi","FBI orders one Venntel Portal seat (Feb. 13).",D+"fbi-foipa-1491075-000-venntel-portal-contract.pdf#page=22","FBI FOIA"),
 ("2020-06","congress","Bicameral inquiry into Venntel opens.","https://oversightdemocrats.house.gov/news/press-releases/members-launch-bicameral-investigation-into-company-tracking-collecting-and","House Oversight"),
 ("2020-09","dhs","DHS OGC signs the AdID legal opinion (Sept. 25).",D+"dhs-ogc-adid-legal-opinion-2020-09-25.pdf#page=1","DHS FOIA"),
 ("2021-01","military","DIA says *Carpenter* does not require a warrant for purchases.","https://www.wyden.senate.gov/imo/media/doc/011521%20CTD%20Discussion%20RFI%20Response.pdf","DIA"),
 ("2021-04","platform","iOS 14.5 requires apps to ask before tracking.","https://www.apple.com/newsroom/2021/04/ios-14-5-offers-unlock-iphone-with-apple-watch-diverse-siri-voices-and-more/","Apple"),
 ("2022-06","law","ODNI declassifies its report on commercially available information.","https://www.dni.gov/files/ODNI/documents/assessments/ODNI-Declassified-Report-on-CAI-January2022.pdf","ODNI"),
 ("2023-09","dhs","DHS inspector general report OIG-23-61.","https://www.oversight.gov/reports/audit/cbp-ice-and-secret-service-did-not-adhere-privacy-policies-or-develop-sufficient","Oversight.gov"),
 ("2024-01","press","ICE says it stopped using the data.","https://fedscoop.com/ice-says-its-stopped-using-phone-location-data/","FedScoop"),
 ("2024-01","law","FTC order against X-Mode.","https://www.ftc.gov/news-events/news/press-releases/2024/01/ftc-order-prohibits-data-broker-x-mode-social-outlogic-selling-sensitive-location-data","FTC"),
 ("2024-02","military","GAO: DoD review of collateral telemetry data still in draft.","https://www.gao.gov/products/gao-24-106190","GAO"),
 ("2024-04","congress","House passes the Fourth Amendment Is Not For Sale Act, 219–199.","https://clerk.house.gov/Votes/2024136","House Clerk"),
 ("2024-08","dhs","CBP publishes its commercial telemetry privacy assessment.","https://www.dhs.gov/sites/default/files/2024-08/24_0812_priv_pia-cbp-080-commercial-telemetry.pdf","DHS"),
 ("2024-12","law","FTC acts against Gravy Analytics and Venntel.","https://www.ftc.gov/news-events/news/press-releases/2024/12/ftc-takes-action-against-gravy-analytics-venntel-unlawfully-selling-location-data-tracking-consumers","FTC"),
 ("2025-01","press","Hackers post a sample of Gravy data.","https://cdn.prod.website-files.com/661d3eb71206816721de67f8/67c5dda5d34d66734fb2ab24_Unacast%20Incident%20Fact%20Sheet_03032025.pdf","Unacast"),
 ("2025-09","dhs","ICE buys access to a Penlink location tool.","https://www.404media.co/ice-to-buy-tool-that-tracks-locations-of-hundreds-of-millions-of-phones-every-day/","404 Media"),
 ("2026-01","dhs","ACLU publishes ICE’s two-page legal memo.","https://www.aclu.org/news/privacy-technology/dhs-is-circumventing-constitution-by-buying-data-it-would-normally-need-a-warrant-to-access","ACLU"),
 ("2026-04","military","CENTCOM reports adversary use of location data against U.S. personnel.","https://www.wyden.senate.gov/imo/media/doc/unclassified_responses_to_sen_wyden_rfis_on_mobile_phone_use_in_centcom_aor.pdf","CENTCOM via Wyden"),
 ("2026-05","congress","Wyden, Harrigan and 12 others write to the DoD CIO.","https://www.wyden.senate.gov/imo/media/doc/wyden_led_letter_to_dod_cio_kirsten_adavies.pdf","Wyden"),
]
CAT = {"dhs":"DHS","fbi":"FBI","military":"Military/IC","law":"Courts and regulators","congress":"Congress","platform":"Platforms","press":"Reporting"}
MON = ["Jan.","Feb.","March","April","May","June","July","Aug.","Sept.","Oct.","Nov.","Dec."]
def dd(s):
    y,m=s.split("-")
    return y if s in YEAR_ONLY else f"{MON[int(m)-1]} {y}"
YEAR_ONLY={"2016-01"}
tl = "\n".join(f'<li data-cat="{c}" data-d="{d}"><time datetime="{d if d not in YEAR_ONLY else d[:4]}">{dd(d)}</time> <span class="tl-cat tl-c-{c}">{CAT[c]}</span> <span class="tl-t">{ei(t)}</span> <a href="{e(u)}">{e(s)}</a></li>' for d,c,t,u,s in TL)
w("timeline", fig("timeline", "Interactive · timeline", "The advertising-ID location trade, 2012–2026",
 f'''<div class="ixm-controls tl-controls" hidden><div class="ixm-chips" role="group" aria-label="Filter events"><button type="button" class="chip" data-cat="all" aria-pressed="true">All</button>{"".join(f'<button type="button" class="chip" data-cat="{k}" aria-pressed="false">{v}</button>' for k,v in CAT.items())}</div></div>
<div class="tl-axis" aria-hidden="true"></div>
<ol class="tl-list">
{tl}
</ol>''',
 'Dates are month of the event or document; each entry links to its source. Filter by category or select a dot on the axis.', fallback=False))

# ---------- FOIA explorer ----------
DOCS = [
 ("dhs-ogc-adid-legal-opinion-2020-09-25.pdf","AdID legal opinion","Sept. 25, 2020",1,24,[1]),
 ("dhs-ogc-social-media-domestic-threats-memo-2018-11-16.pdf","Social media, domestic threats","Nov. 16, 2018",25,11,[1]),
 ("dhs-ogc-privacy-act-e7-st-memo-2021-12-06.pdf","Privacy Act (e)(7), S&amp;T","Dec. 6, 2021",36,23,[1,2]),
 ("dhs-ogc-osint-restrictions-memo-2022-04-07.pdf","OSINT restrictions","April 7, 2022",59,15,[1]),
 ("dhs-ogc-social-media-legal-authorities-2019-03-01.pdf","Social media authorities","March 1, 2019",74,20,[1]),
]
def tile(href, cls, label, num):
    return f'<li><a class="pg {cls}" href="{href}" aria-label="{e(label)}" title="{e(label)}">{num}</a></li>'
blocks = []
for f,t,dt,b0,n,rel in DOCS:
    tiles = "".join(tile(f"{D}{f}#page={p}", "rel" if p in rel else "wh",
        f"{html.unescape(t)}, page {p}, Bates {b0+p-1:06d}: " + ("released with text" if p in rel else "withheld in full, (b)(5)"), p) for p in range(1,n+1))
    blocks.append(f'<div class="fe-doc" data-agency="dhs"><p class="fe-h"><a href="{D}{f}">{t}</a> <span>{dt} · {n} pages · {n-len(rel)} withheld · Bates {b0:06d}–{b0+n-1:06d}</span></p><ol class="fe-grid">{tiles}</ol></div>')
# FBI: PDF p1 = deleted-page sheet; pp2-33 released with redactions
fbi_notes = {1:"FBI deleted-page sheet listing 13 pages withheld",6:"SOW cover, SECRET//NOFORN",7:"SOW: contract for portal access",8:"Unclassified product; place of performance",11:"Market research report",20:"Request for quotes: 1 seat, 12,000 queries",22:"Order 15F06720F0000659",24:"Period of performance",30:"DOJ data-broker PII clause",32:"Classified acquisition? No"}
ft = "".join(tile(f"{D}fbi-foipa-1491075-000-venntel-portal-contract.pdf#page={p}", "sheet" if p==1 else ("rel key" if p in fbi_notes else "rel"),
     f"FBI release, PDF page {p}: " + (fbi_notes.get(p) or "released, with redactions"), p) for p in range(1,34))
ft += "".join(f'<li><span class="pg del" title="Deleted page {i+1} of 13 (not in PDF)">×</span></li>' for i in range(13))
blocks.append(f'<div class="fe-doc" data-agency="fbi"><p class="fe-h"><a href="{D}fbi-foipa-1491075-000-venntel-portal-contract.pdf">FBI Venntel Portal contract</a> <span>FOI/PA 1491075-000 · 33 PDF pages · 13 more deleted in full</span></p><ol class="fe-grid">{ft}</ol></div>')
w("foia", fig("foia", "Interactive · FOIA document explorer", "Every page of the six releases: what came out and what didn’t",
 f'''<div class="fe-sum"><p><span class="fe-big">93</span> DHS pages</p><p><span class="fe-big fe-red">87</span> withheld in full</p><p><span class="fe-big fe-blue">6</span> with any text</p><p><span class="fe-big">13</span> FBI pages deleted</p></div>
<div class="ixm-controls fe-controls" hidden><div class="ixm-chips" role="group" aria-label="Show pages">
<button type="button" class="chip" data-show="all" aria-pressed="true">All pages</button>
<button type="button" class="chip" data-show="rel" aria-pressed="false">Released text</button>
<button type="button" class="chip" data-show="wh" aria-pressed="false">Withheld</button></div></div>
<p class="fe-legend"><span class="pg rel">n</span> released text <span class="pg wh">n</span> withheld, (b)(5) <span class="pg sheet">1</span> FBI deletion sheet <span class="pg del">×</span> deleted, not in PDF</p>
{"".join(blocks)}
<p class="fe-detail" aria-live="polite">Hover or focus a page for details; select it to open the PDF at that page.</p>''',
 'Page status from the released PDFs: DHS FOIA 2024-HQFO-00696 (Bates 000001–000093) and FBI FOI/PA 1491075-000. FBI PDF page 1 is the bureau’s deleted-page sheet; the 32 pages after it were released with redactions, and 13 more were withheld in full. Each square links to that page.', fallback=False))

# ---------- docs table ----------
ROWS = [
 ("Legal Implications of Advertising Identifier Geolocation Data Use by CBP and ICE","DHS OGC","Sept. 25, 2020","24 (23 withheld)","2024-HQFO-00696","dhs-ogc-adid-legal-opinion-2020-09-25.pdf"),
 ("Overview of DHS Legal Authority to Monitor and Collect Publicly Available Social Media for Domestic Threats Related to Ideologically Motivated Violence","DHS OGC","Nov. 16, 2018","11 (10 withheld)","2024-HQFO-00696","dhs-ogc-social-media-domestic-threats-memo-2018-11-16.pdf"),
 ("Overview of Department of Homeland Security Legal Authorities to Use Social Media","DHS OGC","March 1, 2019","20 (19 withheld)","2024-HQFO-00696","dhs-ogc-social-media-legal-authorities-2019-03-01.pdf"),
 ("Analyzing the Privacy Act of 1974’s Limitations on the Ability of the Science and Technology Directorate to Maintain Records Containing First Amendment Information","DHS OGC","Dec. 6, 2021","23 (21 withheld)","2024-HQFO-00696","dhs-ogc-privacy-act-e7-st-memo-2021-12-06.pdf"),
 ("Constitutional and Statutory Restrictions on Open Source Intelligence Activities","DHS OGC","April 7, 2022","15 (14 withheld)","2024-HQFO-00696","dhs-ogc-osint-restrictions-memo-2022-04-07.pdf"),
 ("Venntel Portal Access contract file (requisition, statement of work, market research, request for quotes, order)","FBI","Jan.–Feb. 2020","33 (13 more deleted)","FOI/PA 1491075-000 (source: <a href=\"https://vault.fbi.gov/contract-with-venntel\">FBI Vault</a>)","fbi-foipa-1491075-000-venntel-portal-contract.pdf"),
]
import os
sizes = {}
for r in ROWS:
    p = ROOT / "blog" / SLUG / "docs" / r[5]
    sizes[r[5]] = f"{p.stat().st_size/1e6:.1f} MB" if p.stat().st_size>1e6 else f"{round(p.stat().st_size/1e3)} KB"
tr = "\n".join(f'<tr><td><a href="{D}{f}">{e(t)}</a></td><td>{a}</td><td>{dt}</td><td>{pg}</td><td>{rq}</td><td>PDF, {sizes[f]}{", searchable" if f.startswith("fbi") else ""}</td></tr>' for t,a,dt,pg,rq,f in ROWS)
w("docs-table", f'<div class="table-wrap"><table><thead><tr><th>Document</th><th>Agency</th><th>Date</th><th>Pages</th><th>Request</th><th>File</th></tr></thead><tbody>\n{tr}\n</tbody></table></div>\n')

# ---------- glossary ----------
GL = [
 ("Mobile advertising ID (MAID), AdID","Generic terms for the resettable advertising identifier","DHS opinion; <a href=\"https://www.ftc.gov/news-events/news/press-releases/2024/01/ftc-order-prohibits-data-broker-x-mode-social-outlogic-selling-sensitive-location-data\">FTC</a>"),
 ("IDFA (Identifier for Advertisers)","Apple’s identifier on iOS; “AAID” in intelligence-community shorthand","<a href=\"https://developer.apple.com/documentation/adsupport/asidentifiermanager/advertisingidentifier\">Apple</a>"),
 ("Advertising ID (GAID; CBP writes “AAID”)","Google’s identifier on Android","<a href=\"https://support.google.com/googleplay/android-developer/answer/6048248\">Google</a>; <a href=\"https://www.dhs.gov/sites/default/files/2024-08/24_0812_priv_pia-cbp-080-commercial-telemetry.pdf#page=5\">CBP PIA</a>"),
 ("Commercial telemetry data (CTD)","DHS term for purchased location and device data","<a href=\"https://www.oig.dhs.gov/sites/default/files/assets/2023-09/OIG-23-61-Sep23-Redacted.pdf\">DHS OIG</a>"),
 ("Collateral telemetry data (CTD)","DoD and intelligence-community “consensus term”","<a href=\"https://www.gao.gov/products/gao-24-106190\">GAO-24-106190</a>"),
 ("Commercially available information (CAI)","Intelligence-community policy term","<a href=\"https://www.dni.gov/files/ODNI/documents/CAI/Commercially-Available-Information-Framework-May2024.pdf\">ODNI framework</a>"),
 ("Real-time bidding (RTB), bidstream","The ad-auction data flow","<a href=\"https://github.com/InteractiveAdvertisingBureau/openrtb2.x/blob/main/2.6.md\">OpenRTB 2.6</a>"),
 ("Area search (geofence); device search","Place-to-devices and device-to-places queries","<a href=\"https://www.eff.org/deeplinks/2022/08/inside-fog-data-science-secretive-company-selling-mass-surveillance-local-police\">EFF</a>"),
]
gt = "\n".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{c}</td></tr>" for a,b,c in GL)
w("glossary", f'<div class="table-wrap"><table><thead><tr><th>Term</th><th>Meaning and usage</th><th>Source</th></tr></thead><tbody>\n{gt}\n</tbody></table></div>\n')

# ---------- related ----------
w("related", '''<aside aria-label="Related reading" class="related-reading">
<h2>Related Reading</h2>
<ul>
<li><a href="/blog/centcom-war-orders-anvil-chart-foia/">The Only Public Map of CENTCOM’s War Orders Is Dated 2022</a></li>
<li><a href="/blog/identifier-graph-osint-methodology/">From Public Lead to Identifier Graph</a></li>
</ul>
</aside>
''')
