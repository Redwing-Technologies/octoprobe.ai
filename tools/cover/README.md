# OctoProbe blog cover template

`make_cover.py` renders every blog cover the same way: 2400×1260 PNG (2× of 1200×630, OG aspect),
dark-tinted OpenStreetMap retina tiles, the repo `/logo.svg` + "OctoProbe AI" wordmark top-left,
duotone subject cutout with a single bright-red (#E11D2E) thin uniform outline (stroke) around the silhouette (`--outline-px`, default 8px at 2x output; 0 = none), a red map pin, title,
insight line, sub-line, and photo + OSM credit. No legal badges.

Requires Playwright + Chromium (`/tmp/v/bin/python` on the box) and network access for tiles/fonts.
Cutout: transparent PNG, e.g. `rembg` of the official (FBI/DOJ) photo at its original resolution.

Zhang (live):
    python tools/cover/make_cover.py \
      --photo blog/heather-zhang-prc-agent-case-reddit-allegation/assets/cover-cutout.png \
      --title 'Wanying "Heather"' --title 'Zhang' \
      --insight 'Alleged surveillance trip, Sept 1, 2025' \
      --sub 'Irvine → SNA → Las Vegas → Seattle area · LAX arrest' \
      --credit 'Photo: FBI (via CBS News)' \
      --lat 33.6846 --lon -117.8265 --zoom 11 \
      --out blog/heather-zhang-prc-agent-case-reddit-allegation/assets/cover.png

Burns (preview only):
    python tools/cover/make_cover.py --photo <burns cutout.png> \
      --title 'Christopher' --title 'W. Burns' --insight 'Last seen Sept 24, 2020' \
      --sub 'Wayne, PA · Maps activity after last sighting' \
      --credit 'Photo: FBI wanted poster (public)' --lat 40.0440 --lon -75.3877 --zoom 13 --out preview-burns.png

Tuning flags: --pin-x/--pin-y (CSS px in 1200×630 space; map pans so lat/lon sits under the pin),
--title-size, --title-top, --subject-h, --subject-right.

## Optional logo overlay and connector

For covers that tie an organization's logo or seal to the subject image (e.g. a code card):

- `--logo-overlay PATH`: circular logo or seal (PNG/WebP), with the same red ring width as `--outline-px`
- `--logo-x/--logo-y`: center of the overlay in CSS px on the 1200×630 canvas. `--logo-size`: its diameter
- `--connector`: red graph-edge line with end dots from the overlay to the subject's top edge. Set the width with `--connector-px` (output px) and where it lands with `--connector-target` (0 = left, 1 = right)
- `--no-pin`: hide the map pin and its rings, so the cover keeps one red focal point

Example (Myrotvorets cover v2):

    python3 tools/cover/make_cover.py --photo cutout.png --title 'Your Taxes, Their Target List' \
      --title "Following NED Money Into Ukraine's Online Info-Ops Web" --insight '…' --sub '…' \
      --credit 'Code: … · Seal: Myrotvorets' --lat 50.45 --lon 30.52 --title-size 50 --subject-h 230 \
      --no-pin --logo-overlay seal.webp --logo-x 990 --logo-y 165 --logo-size 210 \
      --connector --connector-target 0.62 --out cover.png
