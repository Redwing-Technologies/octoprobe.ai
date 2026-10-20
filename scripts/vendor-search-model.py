#!/usr/bin/env python3
"""Vendor the static embedding model used by the blog search into assets/search/model/.

One-off / re-vendor tool (the normal build only needs scripts/build-search-index.py).
Downloads minishlab/potion-base-8M (Model2Vec, MIT) at a pinned revision from Hugging Face,
verifies the SHA-256 of model.safetensors, and converts the float32 token-embedding table to
int8 with one float32 scale per row, so the browser fetches ~7.6 MB instead of ~30 MB:

  assets/search/model/embeddings.i8   int8, row-major, vocab_size x dim
  assets/search/model/scales.f32      float32 little-endian, one per row (row = int8 * scale)
  assets/search/model/vocab.txt       WordPiece vocab, one token per line, id = line number
  assets/search/model/meta.json       name, revision, dim, vocab size, special ids
  assets/search/model/LICENSE         upstream MIT licence

Usage (repo root):
  python3 scripts/vendor-search-model.py
  python3 scripts/vendor-search-model.py --from DIR   # use an already-downloaded snapshot
No third-party packages. Then run scripts/build-search-index.py to refresh the vectors.
"""
from __future__ import annotations

import hashlib
import json
import struct
import sys
import urllib.request
from array import array
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "search" / "model"
REPO = "minishlab/potion-base-8M"
REVISION = "bf8b056651a2c21b8d2565580b8569da283cab23"
SAFETENSORS_SHA256 = "f65d0f325faadc1e121c319e2faa41170d3fa07d8c89abd48ca5358d9a223de2"
LICENSE = """MIT License

Copyright (c) 2024 Thomas van Dongen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Model: https://huggingface.co/minishlab/potion-base-8M (Model2Vec, MinishLab),
distilled from BAAI/bge-base-en-v1.5 (MIT). Converted to int8 by
scripts/vendor-search-model.py; no other changes.
"""


def fetch(name: str, src: Path | None) -> bytes:
    if src:
        return (src / name).read_bytes()
    url = f"https://huggingface.co/{REPO}/resolve/{REVISION}/{name}"
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read()


def main() -> int:
    src = Path(sys.argv[sys.argv.index("--from") + 1]) if "--from" in sys.argv else None
    st = fetch("model.safetensors", src)
    if hashlib.sha256(st).hexdigest() != SAFETENSORS_SHA256:
        raise SystemExit("ERROR: model.safetensors SHA-256 mismatch")
    tok = json.loads(fetch("tokenizer.json", src))

    hlen = struct.unpack("<Q", st[:8])[0]
    header = json.loads(st[8:8 + hlen])
    t = header["embeddings"]
    assert t["dtype"] == "F32", t
    rows, dim = t["shape"]
    a, b = t["data_offsets"]
    emb = array("f")
    emb.frombytes(st[8 + hlen + a:8 + hlen + b])
    if sys.byteorder != "little":
        emb.byteswap()

    vocab = sorted(tok["model"]["vocab"].items(), key=lambda kv: kv[1])
    assert [i for _, i in vocab] == list(range(rows)), "vocab ids must be 0..n-1"
    assert not any("\n" in w for w, _ in vocab)
    assert tok["model"]["type"] == "WordPiece" and tok["normalizer"]["lowercase"]

    q = bytearray(rows * dim)
    scales = array("f", [0.0] * rows)
    for r in range(rows):
        row = emb[r * dim:(r + 1) * dim]
        m = max(abs(x) for x in row)
        s = (m / 127.0) or 1.0
        scales[r] = s
        s = scales[r]  # use the float32-rounded scale
        for k, x in enumerate(row):
            q[r * dim + k] = max(-127, min(127, round(x / s))) & 0xFF
    if sys.byteorder != "little":
        scales.byteswap()

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "embeddings.i8").write_bytes(bytes(q))
    (OUT / "scales.f32").write_bytes(scales.tobytes())
    (OUT / "vocab.txt").write_text("\n".join(w for w, _ in vocab) + "\n", encoding="utf-8")
    (OUT / "LICENSE").write_text(LICENSE, encoding="utf-8")
    meta = {
        "name": REPO,
        "revision": REVISION,
        "source": f"https://huggingface.co/{REPO}",
        "license": "MIT",
        "dim": dim,
        "vocab_size": rows,
        "unk_token": tok["model"].get("unk_token", "[UNK]"),
        "skip_ids": [x["id"] for x in tok.get("added_tokens", []) if x.get("special")],
        "format": "embeddings.i8: int8 row-major vocab_size x dim; scales.f32: float32 LE per-row scale; row = int8 * scale",
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=1) + "\n", encoding="utf-8")
    for f in sorted(OUT.iterdir()):
        print(f"wrote {f.relative_to(ROOT)} ({f.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
