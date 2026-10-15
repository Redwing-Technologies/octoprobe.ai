#!/usr/bin/env python3
"""OctoProbe standard blog cover template.

Renders a 2400x1260 (2x of 1200x630, OG aspect) PNG with Playwright:
  - real OpenStreetMap tiles (retina) as a dark-tinted map background
  - OctoProbe logo (repo /logo.svg) + wordmark, top-left
  - subject cutout (transparent PNG, e.g. rembg of an official photo), duotone,
    with a thin uniform bright-red outline (stroke) around the silhouette (--outline-px, default 8px at 2x)
  - red map pin at a chosen coordinate, title, insight lines, photo credit
No legal badges by default.

Usage:
  /tmp/v/bin/python tools/cover/make_cover.py \
    --photo cutout.png --title 'Wanying "Heather"' --title 'Zhang' \
    --insight 'Alleged surveillance trip, Sept 1, 2025' \
    --sub 'Irvine → SNA → Las Vegas → Seattle area · LAX arrest' \
    --credit 'Photo: FBI (via CBS News)' \
    --lat 33.68 --lon -117.83 --zoom 11 --out cover.png
"""
import argparse, base64, html, pathlib, tempfile
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
RED = "#E11D2E"
W, H = 1200, 630  # CSS px; rendered at deviceScaleFactor=2

def smart_quotes(t):
    """Pair straight quotes into typographic ones: "x" -> “x”, 'x' -> ‘x’ (apostrophes -> ’)."""
    import re
    t = re.sub(r'(^|[\s(\[{—-])"', "\\1“", t)
    t = t.replace('"', "”")
    t = re.sub(r"(^|[\s(\[{—-])'", "\\1‘", t)
    return t.replace("'", "’")

def data_uri(p, mime):
    return f"data:{mime};base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def build_html(a):
    logo = data_uri(ROOT / "logo.svg", "image/svg+xml")
    photo = data_uri(a.photo, "image/png")
    titles = "".join(f"<div>{html.escape(smart_quotes(t))}</div>" for t in a.title)
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>
html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:#0a1226}}
#map{{position:absolute;inset:0;filter:grayscale(1) invert(1) brightness(.78) contrast(1.15) sepia(.35) hue-rotate(185deg) saturate(1.6)}}
.leaflet-control-container{{display:none}}
.shade{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,14,32,.94) 0%,rgba(8,14,32,.82) 38%,rgba(8,14,32,.35) 62%,rgba(8,14,32,.15) 100%),linear-gradient(0deg,rgba(8,14,32,.55),rgba(8,14,32,0) 30%)}}
.brand{{position:absolute;left:48px;top:40px;display:flex;align-items:center;gap:12px;color:#fff;font:700 26px/1 'Space Grotesk',sans-serif;letter-spacing:-.01em}}
.brand img{{width:46px;height:46px}}
.brand small{{display:block;font:500 10px/1.4 'JetBrains Mono',monospace;letter-spacing:.22em;color:#9fb0cc;margin-top:4px}}
.title{{position:absolute;left:48px;top:{a.title_top}px;width:780px;color:#fff;font:700 {a.title_size}px/1.02 'Space Grotesk',sans-serif;letter-spacing:-.02em}}
.rule{{width:300px;height:4px;background:{RED};margin:22px 0 18px}}
.insight{{font:500 26px/1.3 'Inter',sans-serif;color:#e6ecf7;letter-spacing:0}}
.sub{{font:400 18px/1.4 'Inter',sans-serif;color:#a9bad6;margin-top:8px;letter-spacing:0}}
.credit{{position:absolute;left:48px;bottom:26px;font:500 10px/1 'JetBrains Mono',monospace;color:#7f8fab;letter-spacing:.04em}}
.osm{{position:absolute;right:14px;bottom:10px;font:400 9px 'Inter',sans-serif;color:rgba(200,210,230,.55)}}
.subject{{position:absolute;right:{a.subject_right}px;bottom:0;height:{a.subject_h}px}}
.subject img{{height:100%;display:block;filter:url(#duo) contrast(1.05) url(#outline)}}
.pin{{position:absolute;left:{a.pin_x}px;top:{a.pin_y}px;transform:translate(-50%,-100%);filter:drop-shadow(0 6px 10px rgba(0,0,0,.45))}}
.ring{{position:absolute;left:{a.pin_x}px;top:{a.pin_y}px;border:2px solid {RED};border-radius:50%;transform:translate(-50%,-50%) scaleY(.38);opacity:.85}}
</style></head><body>
<svg width="0" height="0" style="position:absolute"><filter id="duo" color-interpolation-filters="sRGB">
<feColorMatrix type="matrix" values=".33 .33 .33 0 0  .33 .33 .33 0 0  .33 .33 .33 0 0  0 0 0 1 0"/>
<feComponentTransfer><feFuncR type="table" tableValues="0.03 0.93"/><feFuncG type="table" tableValues="0.07 0.95"/><feFuncB type="table" tableValues="0.18 0.99"/></feComponentTransfer>
</filter>
<filter id="outline" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">
<feMorphology in="SourceAlpha" operator="dilate" radius="{a.outline_px/2}" result="d"/>
<feFlood flood-color="{RED}"/><feComposite in2="d" operator="in" result="ring"/>
<feMerge><feMergeNode in="ring"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter></svg>
<div id="map"></div><div class="shade"></div>
<div class="ring" style="width:90px;height:90px"></div><div class="ring" style="width:150px;height:150px;opacity:.55"></div><div class="ring" style="width:210px;height:210px;opacity:.3"></div>
<svg class="pin" width="64" height="90" viewBox="0 0 28 40"><path d="M14 0C6 0 0 6 0 14c0 10 14 26 14 26s14-16 14-26C28 6 22 0 14 0z" fill="{RED}"/><circle cx="14" cy="14" r="5.2" fill="#7a0a12"/></svg>
<div class="subject"><img id="ph" src="{photo}"></div>
<div class="brand"><img src="{logo}" alt=""><div>OctoProbe AI<small>OSINT CASE STUDY</small></div></div>
<div class="title">{titles}<div class="rule"></div><div class="insight">{html.escape(smart_quotes(a.insight))}</div><div class="sub">{html.escape(smart_quotes(a.sub or ''))}</div></div>
<div class="credit">{html.escape(a.credit)} · Map © OpenStreetMap contributors</div>
<script>
const m=L.map('map',{{zoomControl:false,attributionControl:false,fadeAnimation:false,zoomAnimation:false}});
L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{detectRetina:true,maxZoom:19}}).addTo(m);
m.setView([{a.lat},{a.lon}],{a.zoom},{{animate:false}});
m.panBy([{W/2}-{a.pin_x},{H/2}-{a.pin_y}],{{animate:false}});
window.READY=false;let n=0;m.eachLayer(l=>{{if(l.on)l.on('load',()=>{{window.READY=true}})}});
</script></body></html>"""

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--photo", required=True, help="transparent cutout PNG")
    p.add_argument("--title", action="append", required=True, help="title line (repeatable)")
    p.add_argument("--insight", required=True)
    p.add_argument("--sub", default="")
    p.add_argument("--credit", required=True)
    p.add_argument("--lat", type=float, required=True); p.add_argument("--lon", type=float, required=True)
    p.add_argument("--zoom", type=int, default=11)
    p.add_argument("--pin-x", dest="pin_x", type=int, default=610); p.add_argument("--pin-y", dest="pin_y", type=int, default=540)
    p.add_argument("--title-top", dest="title_top", type=int, default=150)
    p.add_argument("--title-size", dest="title_size", type=int, default=68)
    p.add_argument("--subject-h", dest="subject_h", type=int, default=500)
    p.add_argument("--subject-right", dest="subject_right", type=int, default=40)
    p.add_argument("--outline-px", dest="outline_px", type=float, default=8, help="red silhouette stroke width in output px (2x); 0 = none")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(build_html(a)); tmp = f.name
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        pg.goto("file://" + tmp, wait_until="networkidle")
        pg.wait_for_function("window.READY===true", timeout=30000)
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(800)
        pg.screenshot(path=a.out, type="png")
        b.close()
    try:
        from PIL import Image
        im = Image.open(a.out).convert("RGB"); im.save(a.out, optimize=True)
    except Exception:
        pass
    print(a.out)

if __name__ == "__main__":
    main()
