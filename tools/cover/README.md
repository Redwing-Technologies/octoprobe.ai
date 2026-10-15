# OctoProbe blog cover template

`make_cover.py` renders every blog cover the same way: 2400×1260 PNG (2× of 1200×630, OG aspect),
dark-tinted OpenStreetMap retina tiles, the repo `/logo.svg` + "OctoProbe AI" wordmark top-left,
duotone subject cutout with a single bright-red (#E11D2E) silhouette offset, a red map pin, title,
insight line, sub-line, and photo + OSM credit. No legal badges.

Requires Playwright + Chromium (`/tmp/v/bin/python` on the box) and network access for tiles/fonts.
Cutout: transparent PNG, e.g. `rembg` of the official (FBI/DOJ) photo at its original resolution.

Zhang (live):
    python tools/cover/make_cover.py \
      --photo blog/2026-10-15-wanying-zhang-reddit-passport-allegation-osint/assets/cover-cutout.png \
      --title 'Wanying "Heather"' --title 'Zhang' \
      --insight 'Alleged surveillance trip, Sept 1, 2025' \
      --sub 'Irvine → SNA → Las Vegas → Seattle area · LAX arrest' \
      --credit 'Photo: FBI (via CBS News)' \
      --lat 33.6846 --lon -117.8265 --zoom 11 \
      --out blog/2026-10-15-wanying-zhang-reddit-passport-allegation-osint/assets/cover.png

Burns (preview only):
    python tools/cover/make_cover.py --photo <burns cutout.png> \
      --title 'Christopher' --title 'W. Burns' --insight 'Last seen Sept 24, 2020' \
      --sub 'Wayne, PA · Maps activity after last sighting' \
      --credit 'Photo: FBI wanted poster (public)' --lat 40.0440 --lon -75.3877 --zoom 13 --out preview-burns.png

Tuning flags: --pin-x/--pin-y (CSS px in 1200×630 space; map pans so lat/lon sits under the pin),
--title-size, --title-top, --subject-h, --subject-right.
