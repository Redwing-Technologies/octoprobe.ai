#!/usr/bin/env python3
"""Regenerate the homepage "Latest from OctoProbe News" section.

Reads card order from blog/index.html and rewrites the block between
<!-- home-latest:start --> and <!-- home-latest:end --> in /index.html
(inserted before the FAQ on the first run). Eight newest posts: title,
date, and the card dek.

  python3 scripts/refresh-home-latest.py
  python3 scripts/refresh-home-latest.py --check
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import latest_posts  # noqa: E402


def main() -> int:
    check = "--check" in sys.argv
    stale = latest_posts.refresh_home(check=check)
    if check:
        if stale:
            print("homepage latest block is stale. Run: python3 scripts/refresh-home-latest.py",
                  file=sys.stderr)
            return 1
        print("homepage latest block is up to date")
        return 0
    print("homepage latest block updated" if stale else "homepage latest block already current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
