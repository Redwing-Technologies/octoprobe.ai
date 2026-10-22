#!/usr/bin/env python3
"""Fail when a heading's last line is a single word at 1280px or 390px.

Measures post h1/h2/h3 (including the More-from heading), blog-index card
titles, and homepage latest-card titles in headless Chrome, after
text-wrap: balance. A one-line heading is not an orphan.

  python3 scripts/check-heading-orphans.py
"""
from __future__ import annotations

import base64
import json
import os
import shutil
import socket
import struct
import subprocess
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
WIDTHS = (1280, 390)
CHROME = os.environ.get("CHROME") or shutil.which("google-chrome") or shutil.which("google-chrome-stable")

MEASURE_JS = r"""
(() => {
  const path = location.pathname;
  const nodes = (path === "/index.html" || path === "/")
    ? [...document.querySelectorAll(".latest-title")]
    : (path === "/blog/index.html" || path === "/blog/")
      ? [...document.querySelectorAll(".blog-hero h1, .post-card h2, .blog-faq h2, .faq-list summary")]
      : [...document.querySelectorAll("main h1, main h2, main h3")];
  const range = document.createRange();
  const out = [];
  const font = nodes.length ? getComputedStyle(nodes[0]).fontFamily : "";
  for (const el of nodes) {
    if (el.closest(".mobile-menu, .nav, footer")) continue;
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden") continue;
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    const lines = [];
    let node;
    while ((node = walker.nextNode())) {
      const text = node.textContent;
      for (let i = 0; i < text.length; i++) {
        range.setStart(node, i);
        range.setEnd(node, i + 1);
        const rect = range.getClientRects()[0];
        if (!rect || rect.width < 0.2 || rect.height < 0.2) continue;
        const top = Math.round(rect.top);
        let line = lines.find(l => Math.abs(l.top - top) < 2);
        if (!line) {
          line = {top, text: ""};
          lines.push(line);
        }
        line.text += text[i];
      }
    }
    if (lines.length < 2) continue;
    lines.sort((a, b) => a.top - b.top);
    const lastText = lines[lines.length - 1].text.trim();
    // NBSP keeps two words on one line; it still separates them for the count.
    const lastWords = lastText.split(/[\s\u00a0]+/).filter(Boolean);
    if (lastWords.length === 1) {
      out.push({
        tag: el.tagName.toLowerCase(),
        id: el.id || "",
        text: (el.innerText || "").replace(/\s+/g, " ").trim(),
        last: lastWords[0],
        line: lastText,
        cls: el.className || ""
      });
    }
  }
  const hero = document.querySelector(".post-hero h1, .blog-hero h1, .latest-title");
  return {font, textWrap: hero ? (getComputedStyle(hero).textWrap || "") : "", checked: nodes.length, orphans: out};
})()
"""


class _Server(ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        # Chrome cancels font and image fetches; that is not a check failure.
        return


class _Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt: str, *args) -> None:
        return

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except BrokenPipeError:
            pass


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _ws_connect(url: str) -> socket.socket:
    assert url.startswith("ws://")
    hostport, path = url[5:].split("/", 1)
    host, port = hostport.split(":")
    key = base64.b64encode(os.urandom(16)).decode()
    sock = socket.create_connection((host, int(port)), timeout=20)
    sock.sendall(
        f"GET /{path} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\n"
        f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode()
    )
    buf = b""
    while b"\r\n\r\n" not in buf:
        chunk = sock.recv(4096)
        if not chunk:
            raise RuntimeError("websocket handshake failed")
        buf += chunk
    if b" 101 " not in buf.split(b"\r\n", 1)[0]:
        raise RuntimeError(buf[:200].decode("utf-8", "replace"))
    sock.settimeout(30)
    return sock


def _send(sock: socket.socket, payload: str) -> None:
    data = payload.encode()
    mask = os.urandom(4)
    n = len(data)
    header = bytearray([0x81])
    if n < 126:
        header.append(0x80 | n)
    elif n < 65536:
        header.append(0x80 | 126)
        header += struct.pack(">H", n)
    else:
        header.append(0x80 | 127)
        header += struct.pack(">Q", n)
    header += mask
    sock.sendall(bytes(header) + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))


def _recv(sock: socket.socket) -> str:
    while True:
        header = _read(sock, 2)
        opcode = header[0] & 0x0F
        ln = header[1] & 0x7F
        if ln == 126:
            ln = struct.unpack(">H", _read(sock, 2))[0]
        elif ln == 127:
            ln = struct.unpack(">Q", _read(sock, 8))[0]
        if header[1] & 0x80:
            mask = _read(sock, 4)
            data = bytes(b ^ mask[i % 4] for i, b in enumerate(_read(sock, ln)))
        else:
            data = _read(sock, ln)
        if opcode == 0x8:
            raise RuntimeError("websocket closed")
        if opcode == 0x9:
            # pong
            payload = data
            frame = bytearray([0x8A])
            frame.append(0x80 | len(payload))
            mask = os.urandom(4)
            frame += mask
            frame += bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
            sock.sendall(frame)
            continue
        if opcode == 0x1:
            return data.decode()


def _read(sock: socket.socket, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise RuntimeError("websocket closed while reading")
        buf += chunk
    return buf


class Cdp:
    def __init__(self, sock: socket.socket) -> None:
        self.sock = sock
        self.n = 0

    def call(self, method: str, params: dict | None = None, wait: str | None = None, timeout: float = 25) -> dict:
        self.n += 1
        mid = self.n
        _send(self.sock, json.dumps({"id": mid, "method": method, "params": params or {}}))
        deadline = time.time() + timeout
        event = None
        while time.time() < deadline:
            msg = json.loads(_recv(self.sock))
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result") or {}
            if wait and msg.get("method") == wait:
                event = msg
        raise TimeoutError(method)


def pages() -> list[str]:
    paths = ["/index.html", "/blog/index.html"]
    for path in sorted((ROOT / "blog").glob("*/index.html")):
        if path.parent.name.startswith("_"):
            continue
        html = path.read_text(encoding="utf-8")
        if 'class="post-body"' not in html and 'class="post-hero"' not in html:
            continue
        paths.append("/" + path.relative_to(ROOT).as_posix())
    return paths


def main() -> int:
    if not CHROME:
        print("google-chrome is not installed; heading orphan check skipped", file=sys.stderr)
        return 2
    port = _free_port()
    httpd = _Server(("127.0.0.1", port), _Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    dbg = _free_port()
    profile = Path(f"/tmp/chrome-orphan-{dbg}")
    proc = subprocess.Popen(
        [
            CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
            "--disable-dev-shm-usage", f"--remote-debugging-port={dbg}",
            f"--user-data-dir={profile}", "about:blank",
        ],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        version = None
        for _ in range(50):
            try:
                version = json.load(urlopen(f"http://127.0.0.1:{dbg}/json/version", timeout=1))
                break
            except Exception:
                time.sleep(0.1)
        if not version:
            print("Chrome did not open a debugging port", file=sys.stderr)
            return 2
        targets = json.load(urlopen(f"http://127.0.0.1:{dbg}/json/list", timeout=5))
        page = next(t for t in targets if t.get("type") == "page")
        cdp = Cdp(_ws_connect(page["webSocketDebuggerUrl"]))
        cdp.call("Page.enable")
        cdp.call("Runtime.enable")
        failures: list[str] = []
        font_note = ""
        checked = 0
        for width in WIDTHS:
            cdp.call("Emulation.setDeviceMetricsOverride", {
                "width": width, "height": 900, "deviceScaleFactor": 1, "mobile": width < 600,
            })
            for path in pages():
                cdp.call("Page.navigate", {"url": f"http://127.0.0.1:{port}{path}"})
                # Wait until this URL is the document, then for webfonts. Images can lag.
                cdp.call("Runtime.evaluate", {
                    "expression": (
                        "new Promise(resolve => { const want = " + json.dumps(path) + ";"
                        "const tick = () => { if (location.pathname === want && document.readyState !== 'loading')"
                        " document.fonts.ready.then(() => resolve(location.pathname));"
                        " else setTimeout(tick, 40); }; tick(); })"
                    ),
                    "awaitPromise": True,
                }, timeout=40)
                result = cdp.call("Runtime.evaluate", {
                    "expression": MEASURE_JS,
                    "returnByValue": True,
                }, timeout=40)
                value = (result.get("result") or {}).get("value") or {}
                checked += int(value.get("checked") or 0)
                if not font_note and value.get("font"):
                    font_note = f"font={value.get('font')!r} textWrap={value.get('textWrap')!r}"
                for item in value.get("orphans") or []:
                    where = item["id"] or item["cls"] or item["tag"]
                    failures.append(
                        f"{width}px {path} <{item['tag']}> {where}: last line {item.get('line')!r} in {item['text']!r}"
                    )
        print(f"checked {checked} headings. {font_note}")
        if failures:
            print(f"{len(failures)} heading orphan(s):", file=sys.stderr)
            for line in failures:
                print(line, file=sys.stderr)
            return 1
        print(f"no single-word heading lines at {WIDTHS[0]}px or {WIDTHS[1]}px")
        return 0
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        httpd.shutdown()


if __name__ == "__main__":
    sys.exit(main())
