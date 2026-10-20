/* Interactive modules for the DHS advertising-ID location-data post.
   Progressive enhancement: every module's text is in the HTML; this script adds
   SVG, controls and state. All generated data is illustrative. No dependencies. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var RM = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var C = { blue: '#0288d1', blueD: '#0369a1', ind: '#6366f1', red: '#e11d48', teal: '#0d9488', amber: '#d97706', h: '#0f1b2d', t: '#33404f', s: '#5b6675', line: '#e2e8f0', p2: '#f1f8fe', green: '#16a34a' };
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function el(tag, a, p) { var n = document.createElementNS(NS, tag); for (var k in a) n.setAttribute(k, a[k]); if (p) p.appendChild(n); return n; }
  function txt(p, x, y, s, cls, a) { var t = el('text', Object.assign({ x: x, y: y, 'class': cls || 'sv-lbl' }, a || {}), p); t.textContent = s; return t; }
  function svg(host, w, h, label) {
    var s = el('svg', { viewBox: '0 0 ' + w + ' ' + h, role: 'img', 'aria-label': label || '' }); host.appendChild(s);
    var nx = host.nextElementSibling, wide = /(^| )(au-stage|dv-map|dv-dwell|gf-map|dr-vis|tl-axis)( |$)/.test(host.className);
    if (wide && !(nx && nx.classList.contains('ix-scroll-hint'))) { var hnt = document.createElement('p'); hnt.className = 'ix-scroll-hint'; hnt.textContent = '← Swipe to see the full diagram →'; host.parentNode.insertBefore(hnt, host.nextSibling); }
    return s;
  }
  // Seeded PRNG so the generated illustrative data is identical on every load
  function rng(seed) { return function () { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; }; }
  function press(btns, on) { btns.forEach(function (b) { b.setAttribute('aria-pressed', b === on ? 'true' : 'false'); }); }
  function fmt(n) { return Math.round(n).toLocaleString('en-US'); }
  function unhide(m) { $$('.ixm-controls[hidden], .dv-places[hidden]', m).forEach(function (c) { c.hidden = false; }); }
  // Fictional town: street grid + blocks, used by the device, geofence and directions modules
  function town(s, w, h, r) {
    el('rect', { x: 0, y: 0, width: w, height: h, fill: '#fbfdff' }, s);
    el('path', { d: 'M0 ' + (h - 40) + ' C ' + w * .3 + ' ' + (h - 70) + ', ' + w * .6 + ' ' + (h - 10) + ', ' + w + ' ' + (h - 50) + ' L ' + w + ' ' + h + ' L 0 ' + h + ' Z', 'class': 'sv-water' }, s);
    var xs = [], ys = [];
    for (var x = 30; x < w; x += 90 + Math.floor(r() * 30)) xs.push(x);
    for (var y = 24; y < h - 50; y += 70 + Math.floor(r() * 20)) ys.push(y);
    for (var i = 0; i < xs.length - 1; i++) for (var j = 0; j < ys.length - 1; j++) {
      var park = r() < .1;
      el('rect', { x: xs[i] + 8, y: ys[j] + 8, width: xs[i + 1] - xs[i] - 16, height: ys[j + 1] - ys[j] - 16, rx: 4, 'class': park ? 'sv-park' : 'sv-block' }, s);
    }
    xs.forEach(function (x) { el('line', { x1: x, y1: 0, x2: x, y2: h - 40, 'class': 'sv-street' }, s); });
    ys.forEach(function (y) { el('line', { x1: 0, y1: y, x2: w, y2: y, 'class': 'sv-street' }, s); });
    el('line', { x1: 0, y1: h * .15, x2: w, y2: h * .75, 'class': 'sv-street', 'stroke-width': 9 }, s);
    return { xs: xs, ys: ys };
  }
  function ll(x, y) { return (0.0100 + (420 - y) * 0.00002).toFixed(6) + ', ' + (0.0200 + x * 0.00002).toFixed(6); }

  var init = {};

  /* 1. Field explorer */
  init.fields = function (m) {
    unhide(m);
    var items = $$('.fx-list li', m), layers = $$('.fx-layers li', m), chips = $$('.chip', m), q = $('input', m), count = $('.fx-count', m);
    var st = { layer: null, src: 'all', q: '' };
    layers.forEach(function (L) {
      var k = L.dataset.layer; $('.ly-count', L).textContent = items.filter(function (i) { return i.dataset.layer === k; }).length;
      L.tabIndex = 0; L.setAttribute('role', 'button'); L.setAttribute('aria-pressed', 'false');
      function go() { st.layer = st.layer === k ? null : k; layers.forEach(function (x) { var on = x.dataset.layer === st.layer; x.classList.toggle('on', on); x.setAttribute('aria-pressed', on); }); apply(); }
      L.addEventListener('click', go); L.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
    });
    chips.forEach(function (c) { c.addEventListener('click', function () { st.src = c.dataset.src; press(chips, c); apply(); }); });
    q.addEventListener('input', function () { st.q = q.value.trim().toLowerCase(); apply(); });
    items.forEach(function (i) { i.tabIndex = 0; });
    function apply() {
      var n = 0;
      items.forEach(function (i) {
        var ok = (!st.layer || i.dataset.layer === st.layer) && (st.src === 'all' || i.dataset.src === st.src) && (!st.q || i.dataset.q.indexOf(st.q) >= 0);
        i.classList.toggle('hide', !ok); if (ok) n++;
      });
      count.textContent = n + ' of 56 fields shown';
    }
    apply();
  };

  /* 2. Ad-auction stepper */
  init.auction = function (m) {
    unhide(m);
    var W = 760, H = 270, s = svg($('.au-stage', m), W, H, 'Animated diagram of one bid request fanning out from an app to 12 bidders and a data broker');
    var N = {};
    function node(id, x, y, w, h, label, sub) {
      var g = el('g', { 'class': 'au-node' }, s); el('rect', { x: x, y: y, width: w, height: h, rx: 8, 'class': 'sv-box' }, g);
      txt(g, x + w / 2, y + h / 2 - (sub ? 4 : -4), label, 'sv-lbl-d', { 'text-anchor': 'middle' });
      if (sub) txt(g, x + w / 2, y + h / 2 + 12, sub, 'sv-lbl', { 'text-anchor': 'middle' });
      N[id] = { g: g, x: x, y: y, w: w, h: h, cx: x + w / 2, cy: y + h / 2 }; return g;
    }
    // phone with SDK layers
    var ph = el('g', { 'class': 'au-node' }, s); el('rect', { x: 14, y: 40, width: 140, height: 200, rx: 18, fill: '#fff', stroke: C.h, 'stroke-width': 2 }, ph);
    txt(ph, 84, 62, 'Phone', 'sv-lbl', { 'text-anchor': 'middle' });
    var bars = {}; [['sdk-app', 'App code', C.blue], ['sdk-med', 'Mediation SDK', C.ind], ['sdk-net', 'Ad network SDK', C.teal], ['sdk-loc', 'Location SDK', C.red]].forEach(function (b, i) {
      var r = el('rect', { x: 24, y: 76 + i * 38, width: 120, height: 30, rx: 5, fill: '#fff', stroke: b[2], 'stroke-width': 1.5 }, ph);
      txt(ph, 84, 95 + i * 38, b[1], 'sv-lbl', { 'text-anchor': 'middle', fill: C.h }); bars[b[0]] = r;
    });
    N.phone = { g: ph, cx: 154, cy: 140 };
    node('ex', 200, 112, 120, 56, 'Ad exchange', 'OpenRTB request');
    var bid = [];
    for (var i = 0; i < 12; i++) { var y = 14 + i * 20.5; var g = el('g', { 'class': 'au-node' }, s); var r = el('rect', { x: 430, y: y, width: 92, height: 16, rx: 4, 'class': 'sv-box' }, g); txt(g, 476, y + 12, 'Bidder ' + (i + 1), 'sv-lbl', { 'text-anchor': 'middle' }); bid.push({ g: g, r: r, cx: 430, cy: y + 8 }); }
    node('br', 600, 112, 140, 56, 'Data broker', 'joins by ad ID');
    var buy = node('buy', 600, 206, 140, 48, 'Customers', 'incl. agencies');
    var links = el('g', {}, s);
    function line(x1, y1, x2, y2, col) { return el('line', { x1: x1, y1: y1, x2: x2, y2: y2, stroke: col || C.line, 'stroke-width': 1.5 }, links); }
    var L1 = line(154, 140, 200, 140), fan = bid.map(function (b) { return line(320, 140, 430, b.cy); });
    var toBr = bid.map(function (b) { return line(522, b.cy, 600, 140); }), L3 = line(670, 168, 670, 206);
    var pk = el('g', {}, s), packets = [];
    for (var j = 0; j < 12; j++) packets.push(el('circle', { r: 5, cx: 0, cy: 0, fill: C.red, 'class': 'pk', opacity: 0 }, pk));
    function put(p, x, y, o) { p.style.transform = 'translate(' + x + 'px,' + y + 'px)'; p.setAttribute('opacity', o); }
    var steps = $$('.au-steps li', m), pos = $('.au-pos', m), cur = 0, timer = null, playB = $('.au-play', m);
    var winner = 4;
    function show(k) {
      cur = Math.max(0, Math.min(steps.length - 1, k));
      steps.forEach(function (li, i) { li.classList.toggle('on', i === cur); });
      pos.textContent = 'Step ' + (cur + 1) + ' of ' + steps.length;
      L1.setAttribute('stroke', cur >= 2 ? C.red : C.line);
      fan.forEach(function (l) { l.setAttribute('stroke', cur >= 3 ? 'rgba(225,29,72,.55)' : C.line); });
      toBr.forEach(function (l, i) { l.setAttribute('stroke', cur >= 5 && i % 3 !== 1 ? 'rgba(99,102,241,.6)' : C.line); });
      L3.setAttribute('stroke', cur >= 6 ? C.ind : C.line);
      bid.forEach(function (b, i) { b.r.setAttribute('stroke', cur >= 4 && i === winner ? C.green : (cur >= 3 ? C.red : 'rgba(15,23,42,.15)')); b.r.setAttribute('stroke-width', cur >= 4 && i === winner ? 2.5 : 1); });
      [N.ex.g, N.br.g, buy].forEach(function (g) { g.classList.remove('dim'); });
      if (cur < 2) N.ex.g.classList.add('dim'); if (cur < 5) N.br.g.classList.add('dim'); if (cur < 6) buy.classList.add('dim');
      packets.forEach(function (p, i) {
        if (cur === 0) put(p, 84, 140, 0);
        else if (cur === 1) put(p, 84, 140, i === 0 ? 1 : 0);
        else if (cur === 2) put(p, 260, 140, i === 0 ? 1 : 0);
        else if (cur === 3 || cur === 4) put(p, 440, bid[i].cy, 1);
        else if (cur === 5) put(p, i % 3 !== 1 ? 610 : 440, i % 3 !== 1 ? 140 : bid[i].cy, 1);
        else put(p, 670, 230, i < 4 ? 1 : 0);
      });
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } playB.textContent = 'Play'; playB.setAttribute('aria-pressed', 'false'); }
    $('.au-prev', m).addEventListener('click', function () { stop(); show(cur - 1); });
    $('.au-next', m).addEventListener('click', function () { stop(); show(cur + 1); });
    playB.addEventListener('click', function () {
      if (timer) return stop();
      if (cur >= steps.length - 1) show(0);
      playB.textContent = 'Pause'; playB.setAttribute('aria-pressed', 'true');
      timer = setInterval(function () { if (cur >= steps.length - 1) return stop(); show(cur + 1); }, RM ? 3200 : 2000);
    });
    steps.forEach(function (li, i) { li.addEventListener('click', function () { stop(); show(i); }); });
    $$('.au-sdk tr[data-hl]', m).forEach(function (tr) {
      function on(v) { tr.classList.toggle('hl', v); bars[tr.dataset.hl].setAttribute('fill', v ? '#fff7ed' : '#fff'); bars[tr.dataset.hl].setAttribute('stroke-width', v ? 3 : 1.5); }
      tr.tabIndex = 0;
      tr.addEventListener('mouseenter', function () { on(true); }); tr.addEventListener('mouseleave', function () { on(false); });
      tr.addEventListener('focus', function () { on(true); }); tr.addEventListener('blur', function () { on(false); });
    });
    show(0);
  };

  /* 3. Fan-out calculator */
  init.fanout = function (m) {
    var ins = $$('input[type=range]', m), st = {}, bar = $('.fo-bar', m);
    var W = 760, H = 110, s = svg(bar, W, H, 'Bar chart of location copies by hour of day'), g = el('g', {}, s);
    var curve = [1, .6, .4, .3, .3, .5, 1.2, 2, 2.2, 1.8, 1.6, 1.8, 2.2, 1.9, 1.7, 1.8, 2.1, 2.6, 3, 3.2, 3, 2.6, 2, 1.4];
    var tot = curve.reduce(function (a, b) { return a + b; }, 0);
    function upd() {
      ins.forEach(function (i) { st[i.dataset.k] = +i.value; var o = i.parentNode.querySelector('output'); o.textContent = i.dataset.k === 'geo' ? i.value + '%' : i.value; });
      var day = st.ads * st.bid * st.geo / 100;
      $('[data-o=day]', m).textContent = fmt(day); $('[data-o=month]', m).textContent = fmt(day * 30); $('[data-o=pts]', m).textContent = fmt(st.ads * st.geo / 100);
      while (g.firstChild) g.removeChild(g.firstChild);
      var mx = Math.max.apply(null, curve) / tot * day || 1;
      curve.forEach(function (c, h) {
        var v = c / tot * day, bh = mx ? v / mx * 80 : 0, x = 10 + h * 31;
        el('rect', { x: x, y: 88 - bh, width: 24, height: bh, rx: 3, fill: h < 6 ? C.ind : C.blue, opacity: .85 }, g);
        if (h % 3 === 0) txt(g, x + 12, 104, (h < 10 ? '0' : '') + h + 'h', 'sv-lbl', { 'text-anchor': 'middle' });
      });
      txt(g, 10, 10, 'Copies by hour (illustrative daily curve)', 'sv-lbl');
    }
    ins.forEach(function (i) { i.addEventListener('input', upd); }); upd();
  };

  /* 4. Precision ladder */
  init.ladder = function (m) {
    var items = $$('.ld-list li', m), vis = $('.ld-vis', m);
    var W = 320, H = 260, s = svg(vis, W, H, 'Circle showing the uncertainty radius for the selected precision level');
    var r0 = rng(7); town(s, W, H, r0);
    var radii = [10, 32, 95, 125, 150], circ = el('circle', { cx: 160, cy: 120, r: 10, fill: 'rgba(2,136,209,.16)', stroke: C.blue, 'stroke-width': 2 }, s);
    el('circle', { cx: 160, cy: 120, r: 4, fill: C.red }, s);
    var lab = txt(s, 160, 250, '', 'sv-lbl-d', { 'text-anchor': 'middle' });
    if (!RM) circ.style.transition = 'r .35s ease';
    function pick(i) {
      items.forEach(function (li, k) { li.classList.toggle('on', k === i); $('.ld-btn', li).setAttribute('aria-pressed', k === i); });
      circ.setAttribute('r', radii[i]); lab.textContent = items[i].querySelector('.ld-n').textContent + ' · ' + items[i].dataset.r;
    }
    items.forEach(function (li, i) { $('.ld-btn', li).addEventListener('click', function () { pick(i); }); });
    pick(0);
  };

  /* 5. Pattern of life */
  init.device = function (m) {
    unhide(m);
    var W = 760, H = 420, s = svg($('.dv-map', m), W, H, 'Map of 30 days of generated location points for one fictional advertising ID'), r = rng(20260320);
    town(s, W, H, r);
    var P = [
      { k: 'home', n: 'Home (inferred)', x: 150, y: 300, c: C.blue },
      { k: 'work', n: 'Workplace (inferred)', x: 560, y: 110, c: C.ind },
      { k: 'gym', n: 'Gym', x: 420, y: 260, c: C.teal },
      { k: 'cafe', n: 'Café', x: 640, y: 290, c: C.amber },
      { k: 'park', n: 'Park', x: 300, y: 120, c: C.green }
    ];
    function where(d, h) {
      var wd = d % 7 < 5;
      if (h < 7 || h >= 22) return 'home';
      if (wd && h >= 9 && h < 17) return 'work';
      if (wd && (d % 7 === 0 || d % 7 === 2 || d % 7 === 4) && h === 18) return 'gym';
      if (!wd && h >= 10 && h < 12) return 'cafe';
      if (!wd && h >= 14 && h < 16) return 'park';
      return h === 8 || h === 17 ? 'transit' : 'home';
    }
    var pts = [], byK = {};
    P.forEach(function (p) { byK[p.k] = p; });
    for (var d = 0; d < 30; d++) for (var h = 0; h < 24; h++) {
      var k = where(d, h); if (r() > (h < 6 ? .35 : .5)) continue;
      var x, y;
      if (k === 'transit') { var t = r(), a = byK.home, b = byK.work; x = a.x + (b.x - a.x) * t + (r() - .5) * 20; y = a.y + (b.y - a.y) * t + (r() - .5) * 20; }
      else { var p = byK[k]; x = p.x + (r() - .5) * 26; y = p.y + (r() - .5) * 26; }
      pts.push({ d: d, h: h, k: k, x: x, y: y, mi: Math.floor(r() * 60) });
    }
    var gPath = el('g', { opacity: 0 }, s), gPts = el('g', {}, s), gCl = el('g', {}, s);
    var day3 = pts.filter(function (p) { return p.d === 2; });
    el('polyline', { points: day3.map(function (p) { return p.x.toFixed(1) + ',' + p.y.toFixed(1); }).join(' '), fill: 'none', stroke: C.red, 'stroke-width': 2, 'stroke-dasharray': '5 4' }, gPath);
    txt(gPath, 12, 18, 'Path shown: day 3 (a weekday)', 'sv-lbl');
    var tip = $('.dv-tip', m);
    function col(k) { return k === 'transit' ? '#94a3b8' : byK[k].c; }
    function hh(h, mi) { return (h < 10 ? '0' : '') + h + ':' + (mi < 10 ? '0' : '') + mi; }
    pts.forEach(function (p) {
      p.el = el('circle', { cx: p.x.toFixed(1), cy: p.y.toFixed(1), r: 3.4, fill: col(p.k), opacity: .8, 'class': 'dv-pt' }, gPts);
      p.el.addEventListener('mouseenter', function () { tip.textContent = 'Day ' + (p.d + 1) + ' · ' + hh(p.h, p.mi) + ' · ' + (p.k === 'transit' ? 'in transit' : 'near ' + byK[p.k].n.replace(' (inferred)', '')) + ' · ' + ll(p.x, p.y) + ' (placeholder)'; });
    });
    var rings = {};
    P.forEach(function (p) {
      var n = pts.filter(function (q) { return q.k === p.k; }).length;
      var g = el('g', {}, gCl); rings[p.k] = el('circle', { cx: p.x, cy: p.y, r: 26, 'class': 'dv-cl', stroke: p.c }, g);
      if (p.k === 'home' || p.k === 'work') el('circle', { cx: p.x, cy: p.y, r: 40, fill: 'none', stroke: p.c, 'stroke-width': 1, opacity: .5 }, g);
      var lb = txt(g, p.x, p.y - 34, p.n + ' · ' + n, 'sv-lbl-d', { 'text-anchor': 'middle' }); lb.setAttribute('paint-order', 'stroke'); lb.setAttribute('stroke', '#fff'); lb.setAttribute('stroke-width', '4');
      p.count = n;
    });
    // Dwell profile: 30 rows (days) x 24 columns (hours)
    var DW = 760, DH = 30 * 5 + 36, ds = svg($('.dv-dwell', m), DW, DH, '30-day by 24-hour dwell grid'), cw = (DW - 60) / 24;
    txt(ds, 0, 10, 'Dwell profile: 30 days × 24 hours (color = inferred place)', 'sv-lbl');
    var cells = [];
    for (var dd = 0; dd < 30; dd++) for (var h2 = 0; h2 < 24; h2++) {
      var kk = where(dd, h2); cells.push({ k: kk, h: h2, d: dd, el: el('rect', { x: 50 + h2 * cw, y: 18 + dd * 5, width: cw - 1, height: 4, fill: col(kk), opacity: .75 }, ds) });
    }
    for (var h3 = 0; h3 < 24; h3 += 3) txt(ds, 50 + h3 * cw, DH - 4, (h3 < 10 ? '0' : '') + h3 + ':00', 'sv-lbl');
    txt(ds, 0, 24, 'Day 1', 'sv-lbl'); txt(ds, 0, 18 + 29 * 5 + 4, 'Day 30', 'sv-lbl');
    var st = { pts: true, path: false, clusters: true, tod: 'all', focus: null };
    function vis(p) {
      var wd = p.d % 7 < 5;
      var ok = st.tod === 'all' || (st.tod === 'night' && p.h < 5) || (st.tod === 'work' && wd && p.h >= 9 && p.h < 17);
      return ok && (!st.focus || p.k === st.focus);
    }
    function apply() {
      gPts.style.display = st.pts ? '' : 'none'; gPath.setAttribute('opacity', st.path ? 1 : 0); gCl.style.display = st.clusters ? '' : 'none';
      pts.forEach(function (p) { p.el.classList.toggle('off', !vis(p)); });
      cells.forEach(function (c) { c.el.setAttribute('opacity', vis(c) ? .8 : .1); });
      P.forEach(function (p) { rings[p.k].classList.toggle('on', st.focus === p.k); });
      var shown = pts.filter(vis), sum = {};
      shown.forEach(function (p) { sum[p.k] = (sum[p.k] || 0) + 1; });
      var top = Object.keys(sum).sort(function (a, b) { return sum[b] - sum[a]; })[0];
      tip.textContent = shown.length + ' points shown' + (top ? ' · most frequent: ' + (top === 'transit' ? 'in transit' : byK[top].n) + ' (' + Math.round(sum[top] / shown.length * 100) + '%)' : '');
    }
    $$('[data-layer]', m).forEach(function (b) { b.addEventListener('click', function () { st[b.dataset.layer] = !st[b.dataset.layer]; b.setAttribute('aria-pressed', st[b.dataset.layer]); apply(); }); });
    var tods = $$('[data-tod]', m); tods.forEach(function (b) { b.addEventListener('click', function () { st.tod = b.dataset.tod; press(tods, b); apply(); }); });
    var pb = $('.dv-place-btns', m), pbs = [];
    P.forEach(function (p) {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'chip'; b.setAttribute('aria-pressed', 'false'); b.textContent = p.n + ' (' + p.count + ' pts)';
      b.addEventListener('click', function () { st.focus = st.focus === p.k ? null : p.k; pbs.forEach(function (x) { x.setAttribute('aria-pressed', x === b && st.focus ? 'true' : 'false'); }); apply(); });
      pb.appendChild(b); pbs.push(b);
    });
    apply();
  };

  /* 6. Bid-request cross-section */
  init.bidrequest = function (m) {
    var lines = $$('.br-line', m), ex = $$('.br-expl li', m);
    var groups = [['id', 'Identifier', C.red], ['net', 'Network', C.amber], ['loc', 'Location', C.blue], ['hw', 'Hardware', C.teal], ['sw', 'Software and app', C.ind]];
    var W = 300, H = 300, s = svg($('.br-ring', m), W, H, 'Ring diagram grouping bid request fields'), cx = 150, cy = 150, R = 120, r0 = 70;
    var counts = groups.map(function (g) { return lines.filter(function (l) { return l.dataset.g === g[0]; }).length; }), tot = counts.reduce(function (a, b) { return a + b; }, 0), a0 = -Math.PI / 2, arcs = {};
    groups.forEach(function (g, i) {
      var a1 = a0 + counts[i] / tot * Math.PI * 2, la = a1 - a0 > Math.PI ? 1 : 0;
      function pt(a, rr) { return (cx + Math.cos(a) * rr).toFixed(1) + ' ' + (cy + Math.sin(a) * rr).toFixed(1); }
      arcs[g[0]] = el('path', { d: 'M' + pt(a0, R) + ' A' + R + ' ' + R + ' 0 ' + la + ' 1 ' + pt(a1, R) + ' L' + pt(a1, r0) + ' A' + r0 + ' ' + r0 + ' 0 ' + la + ' 0 ' + pt(a0, r0) + ' Z', fill: g[2], opacity: .35, stroke: '#fff', 'stroke-width': 2 }, s);
      var am = (a0 + a1) / 2; txt(s, cx + Math.cos(am) * (R + 18), cy + Math.sin(am) * (R + 18) + 4, g[1], 'sv-lbl', { 'text-anchor': Math.cos(am) > .2 ? 'start' : (Math.cos(am) < -.2 ? 'end' : 'middle') });
      a0 = a1;
    });
    txt(s, cx, cy - 4, 'One bid request', 'sv-lbl-d', { 'text-anchor': 'middle' }); var sub = txt(s, cx, cy + 14, tot + ' fields shown', 'sv-lbl', { 'text-anchor': 'middle' });
    function on(i, v) {
      var L = lines[i];
      if (v) { lines.forEach(function (x) { x.classList.remove('on'); }); ex.forEach(function (x) { x.classList.remove('on'); }); }
      L.classList.toggle('on', v); ex[i].classList.toggle('on', v);
      Object.keys(arcs).forEach(function (k) { arcs[k].setAttribute('opacity', v ? (k === L.dataset.g ? .95 : .15) : .35); });
      sub.textContent = v ? L.querySelector('.br-k').textContent : tot + ' fields shown';
    }
    lines.forEach(function (L, i) { ['mouseenter', 'focus'].forEach(function (e) { L.addEventListener(e, function () { on(i, true); }); }); ['mouseleave', 'blur'].forEach(function (e) { L.addEventListener(e, function () { on(i, false); }); }); });
    ex.forEach(function (li, i) { li.addEventListener('mouseenter', function () { on(i, true); }); li.addEventListener('mouseleave', function () { on(i, false); }); });
  };

  /* 7. Area search */
  init.geofence = function (m) {
    unhide(m);
    var W = 760, H = 360, s = svg($('.gf-map', m), W, H, 'Map of a fictional community center with a geofence polygon and generated device dots'), r = rng(424242);
    town(s, W, H, r);
    var poly = [[330, 120], [470, 105], [495, 210], [350, 235]];
    el('rect', { x: 360, y: 135, width: 100, height: 70, rx: 6, fill: '#fde7ec', stroke: C.red }, s);
    txt(s, 410, 175, 'Community center', 'sv-lbl-d', { 'text-anchor': 'middle' });
    el('polygon', { points: poly.map(function (p) { return p.join(','); }).join(' '), fill: 'rgba(225,29,72,.08)', stroke: C.red, 'stroke-width': 2.5, 'stroke-dasharray': '7 5' }, s);
    txt(s, 335, 112, 'Geofence', 'sv-lbl', { fill: C.red });
    function inside(x, y) { var c = false; for (var i = 0, j = poly.length - 1; i < poly.length; j = i++) { var xi = poly[i][0], yi = poly[i][1], xj = poly[j][0], yj = poly[j][1]; if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) c = !c; } return c; }
    var WINS = ['9–10 a.m.', '10–11 a.m.', '11 a.m.–noon', 'noon–1 p.m.', '1–2 p.m.', '2–3 p.m.', '3–4 p.m.', '4–5 p.m.'];
    var devs = [];
    for (var i = 0; i < 70; i++) {
      var id = Math.floor(r() * 0xffffffff).toString(16); while (id.length < 8) id = '0' + id;
      var vis = r() < .45, w0 = Math.floor(r() * 8), w1 = Math.min(7, w0 + Math.floor(r() * 3));
      var pos = [];
      for (var k = 0; k < 8; k++) {
        var x, y;
        if (vis && k >= w0 && k <= w1) { do { x = 340 + r() * 150; y = 112 + r() * 120; } while (!inside(x, y)); }
        else { do { x = 20 + r() * 720; y = 20 + r() * 290; } while (inside(x, y)); }
        pos.push([x, y]);
      }
      devs.push({ id: id + '-…', pos: pos, w0: vis ? w0 : -1, w1: vis ? w1 : -1, el: el('circle', { r: 4, cx: pos[0][0], cy: pos[0][1], 'class': 'gf-dev', fill: '#94a3b8' }, s) });
    }
    var k = 3, cum = $('.gf-cum input', m), win = $('.gf-win', m), cnt = $('.gf-count', m), list = $('.gf-list', m);
    function upd() {
      var lo = cum.checked ? 0 : k, hit = [];
      devs.forEach(function (d) {
        d.el.setAttribute('cx', d.pos[k][0].toFixed(1)); d.el.setAttribute('cy', d.pos[k][1].toFixed(1));
        var inNow = d.w0 >= 0 && k >= d.w0 && k <= d.w1, inWin = d.w0 >= 0 && d.w1 >= lo && d.w0 <= k;
        d.el.setAttribute('fill', inNow ? C.red : (inWin ? 'rgba(225,29,72,.45)' : '#94a3b8'));
        if (inWin) hit.push(d);
      });
      win.textContent = 'Window: Saturday ' + (cum.checked ? '9 a.m. to ' + WINS[k].split('–')[1] : WINS[k]);
      cnt.textContent = 'Devices inside the fence: ' + hit.length + (cum.checked ? ' (cumulative)' : ' (this hour)');
      list.innerHTML = '';
      hit.forEach(function (d) { var li = document.createElement('li'); li.textContent = 'adid ' + d.id; if (d.w0 === k) li.className = 'new'; list.appendChild(li); });
    }
    $('.gf-prev', m).addEventListener('click', function () { k = Math.max(0, k - 1); upd(); });
    $('.gf-next', m).addEventListener('click', function () { k = Math.min(7, k + 1); upd(); });
    cum.addEventListener('change', upd); upd();
  };

  /* 8. Two query directions */
  init.directions = function (m) {
    unhide(m);
    var W = 760, H = 230, s = svg($('.dr-vis', m), W, H, 'Diagram of forward and reverse queries'), g1 = el('g', {}, s), g2 = el('g', {}, s);
    // forward: one device -> places
    el('circle', { cx: 90, cy: 115, r: 26, fill: C.h }, g1); txt(g1, 90, 119, 'one ID', 'sv-lbl', { 'text-anchor': 'middle', fill: '#fff' });
    ['Home', 'Work', 'Gym', 'Café', 'Clinic'].forEach(function (n, i) { var y = 25 + i * 45; el('line', { x1: 116, y1: 115, x2: 300, y2: y, stroke: C.blue, 'stroke-width': 1.5 }, g1); el('rect', { x: 300, y: y - 14, width: 86, height: 28, rx: 6, fill: C.p2, stroke: C.blue }, g1); txt(g1, 343, y + 4, n, 'sv-lbl', { 'text-anchor': 'middle', fill: C.h }); });
    txt(g1, 20, 220, 'Device search → places', 'sv-lbl-d');
    // reverse: one place -> devices
    el('polygon', { points: '470,80 560,70 575,150 480,165', fill: 'rgba(225,29,72,.1)', stroke: C.red, 'stroke-width': 2, 'stroke-dasharray': '6 4' }, g2); txt(g2, 522, 122, 'one place', 'sv-lbl', { 'text-anchor': 'middle', fill: C.red });
    for (var i = 0; i < 8; i++) { var y = 18 + i * 26; el('line', { x1: 575, y1: 115, x2: 680, y2: y, stroke: C.red, 'stroke-width': 1.2, opacity: .7 }, g2); el('circle', { cx: 690, cy: y, r: 9, fill: C.h }, g2); txt(g2, 706, y + 4, 'ID ' + (i + 1), 'sv-lbl'); }
    txt(g2, 470, 220, 'Area search → devices', 'sv-lbl-d');
    var b = $$('[data-dir]', m).filter(function (x) { return x.tagName === 'BUTTON'; }), ps = $$('.dr-text p', m);
    function set(d) { g1.setAttribute('opacity', d === 'fwd' ? 1 : .15); g2.setAttribute('opacity', d === 'rev' ? 1 : .15); ps.forEach(function (p) { p.classList.toggle('on', p.dataset.dir === d); }); press(b, b.filter(function (x) { return x.dataset.dir === d; })[0]); }
    b.forEach(function (x) { x.addEventListener('click', function () { set(x.dataset.dir); }); });
    set('fwd');
  };

  /* 9. Acquisition path */
  init.flow = function (m) {
    var items = $$('.fl-list > li', m), panel = document.createElement('div');
    panel.className = 'fl-panel'; panel.setAttribute('aria-live', 'polite'); m.querySelector('.ixm-live').appendChild(panel);
    function open(i) {
      items.forEach(function (li, k) { $('.fl-btn', li).setAttribute('aria-expanded', k === i); });
      panel.innerHTML = '<p><strong>' + $('.fl-btn', items[i]).textContent.replace(/^\d+\s*/, '') + '.</strong> </p>' ;
      var det = $('.fl-det', items[i]).cloneNode(true); panel.firstChild.appendChild(document.createTextNode(det.querySelector('p').textContent));
      panel.appendChild(det.querySelector('ul'));
    }
    items.forEach(function (li, i) { $('.fl-btn', li).setAttribute('aria-controls', 'fl-panel'); $('.fl-btn', li).addEventListener('click', function () { open(i); }); });
    panel.id = 'fl-panel'; open(0);
  };

  /* 10. Timeline (built from the post's sourced event list) */
  init.timeline = function (m) {
    unhide(m);
    var items = $$('.tl-list li', m), chips = $$('.chip', m);
    var W = 760, H = 70, s = svg($('.tl-axis', m), W, H, 'Timeline axis from 2012 to 2026 with one dot per event');
    var y0 = 2012, y1 = 2026.99, X = function (d) { var p = d.split('-'); return 20 + ((+p[0] + (+p[1] - 1) / 12) - y0) / (y1 - y0) * (W - 40); };
    el('line', { x1: 20, y1: 40, x2: W - 20, y2: 40, stroke: '#cbd5e1', 'stroke-width': 2 }, s);
    for (var y = 2012; y <= 2026; y += 2) { el('line', { x1: X(y + '-01'), y1: 35, x2: X(y + '-01'), y2: 45, stroke: '#94a3b8' }, s); txt(s, X(y + '-01'), 62, String(y), 'sv-lbl', { 'text-anchor': 'middle' }); }
    var col = { dhs: C.blue, fbi: C.ind, military: C.red, law: C.teal, congress: C.amber, platform: '#64748b', press: '#db2777' }, stack = {};
    var dots = items.map(function (li) {
      var x = X(li.dataset.d), key = Math.round(x / 8); stack[key] = (stack[key] || 0) + 1;
      var d = el('circle', { cx: x, cy: 40 - (stack[key] - 1) * 11, r: 5, fill: col[li.dataset.cat], 'class': 'tl-dot', tabindex: 0, role: 'button', 'aria-label': li.querySelector('time').textContent + ': ' + li.querySelector('.tl-t').textContent }, s);
      function on() { items.forEach(function (x) { x.classList.remove('on'); }); dots.forEach(function (x) { x.classList.remove('on'); }); li.classList.add('on'); d.classList.add('on'); }
      d.addEventListener('click', on); d.addEventListener('focus', on); d.addEventListener('mouseenter', on);
      d.addEventListener('keydown', function (e) { if (e.key === 'Enter') li.querySelector('a').focus(); });
      return d;
    });
    chips.forEach(function (c) { c.addEventListener('click', function () { press(chips, c); var k = c.dataset.cat; items.forEach(function (li, i) { var ok = k === 'all' || li.dataset.cat === k; li.classList.toggle('hide', !ok); dots[i].setAttribute('opacity', ok ? 1 : .12); }); }); });
  };

  /* 11. FOIA document explorer (new; page-level links to the hosted PDFs) */
  init.foia = function (m) {
    unhide(m);
    var pages = $$('.pg', m).filter(function (p) { return p.closest('.fe-grid'); }), det = $('.fe-detail', m), chips = $$('.chip', m);
    pages.forEach(function (p) {
      var t = p.getAttribute('title') || p.getAttribute('aria-label'); if (p.tagName !== 'A') p.tabIndex = 0;
      ['mouseenter', 'focus'].forEach(function (e) { p.addEventListener(e, function () { det.textContent = t + (p.tagName === 'A' ? ' · select to open' : ''); }); });
    });
    chips.forEach(function (c) { c.addEventListener('click', function () { press(chips, c); var k = c.dataset.show; pages.forEach(function (p) { var cls = p.classList; var ok = k === 'all' || (k === 'rel' && cls.contains('rel')) || (k === 'wh' && (cls.contains('wh') || cls.contains('del'))); cls.toggle('fade', !ok); }); }); });
  };

  function boot() {
    $$('.ixm[data-ixm]').forEach(function (m) {
      var f = init[m.dataset.ixm]; if (!f) return;
      try { f(m); m.classList.add('ixm-ready'); } catch (err) { if (window.console) console.error('module ' + m.dataset.ixm, err); }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
