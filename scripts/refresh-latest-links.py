#!/usr/bin/env python3
"""Regenerate each post's "More from OctoProbe News" list.

Five newest posts, excluding the current one, in blog/index.html card order.
Hand-edited articles are patched in place between <!-- latest:start --> and
<!-- latest:end -->. The block sits after Related Reading (or after the author
note when a post has no Related Reading).

  python3 scripts/refresh-latest-links.py
  python3 scripts/refresh-latest-links.py --check
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import latest_posts  # noqa: E402


def main() -> int:
    check = "--check" in sys.argv
    stale = latest_posts.refresh_posts(check=check)
    if check:
        if stale:
            print(f"{len(stale)} post(s) have a stale More from list. "
                  "Run: python3 scripts/refresh-latest-links.py", file=sys.stderr)
            for path in stale:
                print(f"  {path}", file=sys.stderr)
            return 1
        print(f"more-from lists are up to date on {len(latest_posts.live_posts())} posts")
        return 0
    if stale:
        print(f"updated more-from lists on {len(stale)} posts")
    else:
        print("more-from lists already current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
