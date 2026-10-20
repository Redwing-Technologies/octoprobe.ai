/* Interactive modules for the Secret Service FOIA x OSINT guide.
   Progressive enhancement: every module's content is in the HTML; this script adds the
   lightbox, the loop diagram, table search and filters, the request builder and the
   release explorer. No network calls except loading this post's own hostfinder-data.json. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function el(tag, a, p) { var n = document.createElementNS(NS, tag); for (var k in a) n.setAttribute(k, a[k]); if (p) p.appendChild(n); return n; }
  function press(btns, on) { btns.forEach(function (b) { b.setAttribute('aria-pressed', b === on ? 'true' : 'false'); }); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function copyText(t, done) {
    function fallback() { var ta = document.createElement('textarea'); ta.value = t; ta.style.position = 'fixed'; ta.style.opacity = '0'; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); done(true); } catch (e) { done(false); } document.body.removeChild(ta); }
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(t).then(function () { done(true); }, fallback); else fallback();
  }

  // ---------- Rowe page lightbox ----------
  function rowe(m) {
    var a = $('.rl-open', m); if (!a || !window.HTMLDialogElement) return;
    var d = document.createElement('dialog'); d.className = 'rl-dialog'; d.setAttribute('aria-label', 'Browser-history page, full size');
    d.innerHTML = '<div class="rl-bar"><span>Secret Service release, request 20240110 · <a href="' + a.getAttribute('href') + '">Open image</a></span><button type="button">Close</button></div><img alt="">';
    document.body.appendChild(d);
    var img = $('img', d), small = $('img', a);
    img.alt = small.alt;
    $('button', d).addEventListener('click', function () { d.close(); });
    d.addEventListener('click', function (ev) { if (ev.target === d) d.close(); });
    a.addEventListener('click', function (ev) {
      ev.preventDefault();
      if (!img.getAttribute('src')) img.src = a.getAttribute('data-full');
      d.showModal(); $('button', d).focus();
    });
  }

  // ---------- Loop ----------
  function loop(m) {
    var nodes = $$('.lp-node', m), host = $('.lp-stage', m), st = $('.lp-status', m), i = 0;
    var W = 560, H = 360, cx = 280, cy = 180, rx = 190, ry = 125;
    var s = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Loop diagram: Map, Name, Request, Mine, then back to Map' }, host);
    var defs = el('defs', {}, s), mk = el('marker', { id: 'lpa', viewBox: '0 0 10 10', refX: 8, refY: 5, markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse' }, defs);
    el('path', { d: 'M0 0 L10 5 L0 10 z', fill: '#0288d1' }, mk);
    el('ellipse', { cx: cx, cy: cy, rx: rx, ry: ry, 'class': 'lp-ring' }, s);
    var pos = [[cx, cy - ry], [cx + rx, cy], [cx, cy + ry], [cx - rx, cy]];
    var subs = ['DNS · tenant metadata', 'bios · FOIA logs', 'logs · documents · Teams', 'sites · hosts · offices'];
    for (var k = 0; k < 4; k++) {
      var a = pos[k], b = pos[(k + 1) % 4];
      var dx = b[0] - a[0], dy = b[1] - a[1];
      var sx = a[0] + dx * 0.28, sy = a[1] + dy * 0.28, ex = a[0] + dx * 0.72, ey = a[1] + dy * 0.72;
      var qx = (a[0] + b[0]) / 2 + (cx - (a[0] + b[0]) / 2) * -0.35, qy = (a[1] + b[1]) / 2 + (cy - (a[1] + b[1]) / 2) * -0.35;
      el('path', { d: 'M' + sx + ' ' + sy + ' Q ' + qx + ' ' + qy + ' ' + ex + ' ' + ey, 'class': 'lp-arrow', 'marker-end': 'url(#lpa)' }, s);
    }
    var t = el('text', { x: cx, y: cy - 4, 'class': 'lp-mid' }, s); t.textContent = 'OSINT → FOIA';
    var t2 = el('text', { x: cx, y: cy + 14, 'class': 'lp-mid' }, s); t2.textContent = '→ OSINT';
    var gs = nodes.map(function (n, k) {
      var g = el('g', { 'class': 'lp-g', tabindex: '-1' }, s);
      el('rect', { x: pos[k][0] - 78, y: pos[k][1] - 30, width: 156, height: 60, rx: 14, 'class': 'lp-c' }, g);
      var a1 = el('text', { x: pos[k][0], y: pos[k][1] - 3, 'class': 'lp-t' }, g); a1.textContent = (k + 1) + '. ' + $('strong', n).textContent.replace('.', '');
      var a2 = el('text', { x: pos[k][0], y: pos[k][1] + 15, 'class': 'lp-s' }, g); a2.textContent = subs[k];
      g.addEventListener('click', function () { set(k); });
      n.addEventListener('click', function () { set(k); });
      return g;
    });
    function set(k) {
      i = (k + 4) % 4;
      nodes.forEach(function (n, j) { n.classList.toggle('on', j === i); });
      gs.forEach(function (g, j) { g.classList.toggle('on', j === i); });
      st.textContent = 'Step ' + (i + 1) + ' of 4: ' + $('strong', nodes[i]).textContent.replace('.', '');
    }
    $('[data-lp="next"]', m).addEventListener('click', function () { set(i + 1); });
    $('[data-lp="prev"]', m).addEventListener('click', function () { set(i - 1); });
    m.addEventListener('keydown', function (ev) {
      if (ev.target.tagName === 'INPUT') return;
      if (ev.key === 'ArrowRight' || ev.key === 'ArrowDown') { set(i + 1); ev.preventDefault(); }
      if (ev.key === 'ArrowLeft' || ev.key === 'ArrowUp') { set(i - 1); ev.preventDefault(); }
    });
    m.setAttribute('tabindex', '0');
    set(0);
  }

  // ---------- Host finder ----------
  var BADGE = { ok: 'resolves', nx: 'no DNS record', na: 'not checked' };
  function hfRow(r) {
    var rown = r[0], title = r[1], tag = r[2], cols = r[3], notes = r[4], st = r[5], dept = tag || 'Independent / untagged';
    var cells = cols.map(function (c) {
      return '<span class="hf-col"><span class="hf-lab">' + esc(c[0]) + '</span> ' + c[1].map(function (h) {
        return '<span class="hf-h hf-' + h[2] + '"><code>' + esc(h[0]) + '</code> <span class="hf-b">' + BADGE[h[2]] + '</span></span>';
      }).join('') + (c[2] ? '<span class="hf-mm">Cell link points to <code>' + esc(c[2]) + '</code></span>' : '') + '</span>';
    }).join('');
    return '<tr data-dept="' + esc(dept) + '" data-dns="' + st + '" data-note="' + (notes.length ? 1 : 0) + '"><td class="hf-row">' + rown + '</td><td><strong>' + esc(title) + '</strong><span class="hf-dept">' + esc(dept) + '</span></td><td>' +
      (cells || '<span class="hf-none">No hosts listed</span>') + '</td><td class="hf-note">' + notes.map(function (n) { return '<p>' + n + '</p>'; }).join('') + '</td></tr>';
  }
  function hostfinder(m) {
    var wrap = $('.hf-scroll', m), tb = $('tbody', wrap), q = $('[data-hf="q"]', m), dept = $('[data-hf="dept"]', m), cnt = $('.hf-count', m);
    var chips = $$('[data-hf-f]', m), mode = 'all', total = tb.rows.length;
    var staticRows = {};
    $$('tr', tb).forEach(function (tr) { staticRows[tr.cells[0].textContent] = true; });
    function addCopy() {
      $$('.hf-h', tb).forEach(function (h) {
        if ($('.hf-copy', h)) return;
        var b = document.createElement('button'); b.type = 'button'; b.className = 'hf-copy'; b.textContent = 'Copy';
        var host = $('code', h).textContent.replace(/^https?:\/\//, '').split('/')[0].replace(/["']/g, '').toLowerCase();
        b.setAttribute('aria-label', 'Copy ' + host);
        b.addEventListener('click', function () { copyText(host, function (ok) { b.textContent = ok ? 'Copied' : 'Copy failed'; setTimeout(function () { b.textContent = 'Copy'; }, 1500); }); });
        h.appendChild(b);
      });
    }
    function apply() {
      var s = (q.value || '').trim().toLowerCase(), d = dept.value, n = 0;
      $$('tr', tb).forEach(function (tr) {
        var ok = (!s || tr.textContent.toLowerCase().indexOf(s) >= 0) && (!d || tr.getAttribute('data-dept') === d) &&
          (mode === 'all' || (mode === 'note' && tr.getAttribute('data-note') === '1') || (mode === 'none' && tr.getAttribute('data-dns') === 'none'));
        tr.hidden = !ok; if (ok) n++;
      });
      cnt.textContent = 'Showing ' + n + ' of ' + total + ' rows';
    }
    q.addEventListener('input', apply); dept.addEventListener('change', apply);
    chips.forEach(function (c) { c.addEventListener('click', function () { mode = c.getAttribute('data-hf-f'); press(chips, c); apply(); }); });
    addCopy(); apply();
    var src = wrap.getAttribute('data-src');
    if (src && window.fetch) fetch(src).then(function (r) { return r.json(); }).then(function (j) {
      tb.innerHTML = j.rows.map(function (r) {
        var h = hfRow(r);
        return staticRows[String(r[0])] ? h : h.replace('<tr ', '<tr class="hf-dyn" ');
      }).join('');
      total = j.rows.length; addCopy(); apply();
      var pn = document.createElement('p'); pn.className = 'hf-print-note';
      pn.textContent = 'Print view shows the Homeland Security rows and rows with notes. The full table is in the CSV.';
      wrap.parentNode.insertBefore(pn, wrap.nextSibling);
    }).catch(function () { cnt.textContent += ' (full table unavailable; use the CSV)'; });
  }

  // ---------- Request builder ----------
  function builder(m) {
    var form = $('.rb-form', m), out = $('.rb-out', m), ta = $('textarea', out), status = $('.rb-status', m);
    form.hidden = false; out.hidden = false;
    var tpls = {};
    $$('.rb-list li', m).forEach(function (li) { tpls[li.getAttribute('data-t')] = $('.rb-tpl', li).textContent.replace(/^“|”$/g, ''); });
    var xtra = {};
    $$('.rb-xlist li', m).forEach(function (li) { xtra[li.getAttribute('data-x')] = $('.rb-tpl', li).textContent.replace(/^“|”$/g, ''); });
    function val(k) { var v = $('[data-rb="' + k + '"]', m).value.trim(); return v; }
    function render() {
      var map = { AGENCY: val('agency') || '[Agency]', TENANT: val('tenant') || '[tenant]', CUSTODIAN: val('custodian') || '[Full name]', TITLE: val('title') || '[Title]', START: val('start') || '[Start date]', END: val('end') || '[End date]', KEYWORDS: val('keywords') || '[keywords]' };
      var items = $$('[data-rb-t]', m).filter(function (c) { return c.checked; }).map(function (c) { return tpls[c.getAttribute('data-rb-t')]; });
      var body = items.map(function (t, i) { return (i + 1) + '. ' + t.replace(/\[([A-Z]+)\]/g, function (x, k) { return map[k] || x; }); }).join('\n\n');
      var extras = $$('[data-rb-x]', m).filter(function (c) { return c.checked; }).map(function (c) { return xtra[c.getAttribute('data-rb-x')]; });
      ta.value = 'Under the Freedom of Information Act, 5 U.S.C. § 552, I request the following records:\n\n' + (body || '[Select at least one item.]') +
        '\n\nPlease provide the records in electronic form, as native files where available, under 5 U.S.C. § 552(a)(3)(B). Please describe the systems and locations searched.' +
        (extras.length ? '\n\n' + extras.join('\n\n') : '');
    }
    $$('input', form).forEach(function (i) { i.addEventListener('input', render); i.addEventListener('change', render); });
    $('[data-rb-copy]', m).addEventListener('click', function () { copyText(ta.value, function (ok) { status.textContent = ok ? 'Copied.' : 'Select the text and copy it manually.'; }); });
    render();
  }

  // ---------- Release explorer ----------
  function explorer(m) {
    var det = $('.fe-detail', m), chips = $$('[data-show]', m), docs = $$('.fe-doc', m);
    $$('a.pg', m).forEach(function (p) {
      function show() { det.textContent = p.getAttribute('aria-label'); }
      p.addEventListener('mouseenter', show); p.addEventListener('focus', show);
    });
    chips.forEach(function (c) { c.addEventListener('click', function () {
      var v = c.getAttribute('data-show'); press(chips, c);
      docs.forEach(function (d) { d.classList.toggle('dim', v !== 'all' && d.getAttribute('data-g') !== v); });
    }); });
  }

  var INIT = { rowe: rowe, loop: loop, hostfinder: hostfinder, builder: builder, explorer: explorer };
  function boot() {
    $$('.ixm[data-ixm]').forEach(function (m) {
      var f = INIT[m.getAttribute('data-ixm')];
      $$('.ixm-controls[hidden]', m).forEach(function (c) { c.hidden = false; });
      if (f) { try { f(m); } catch (e) { if (window.console) console.error('module ' + m.getAttribute('data-ixm'), e); } }
      m.classList.add('ixm-ready');
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
