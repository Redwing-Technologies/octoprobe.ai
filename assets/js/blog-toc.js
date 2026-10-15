/* OctoProbe blog: auto table of contents (desktop sticky rail + mobile <details>). */
(function () {
  'use strict';
  var prose = document.querySelector('.post-body .prose');
  if (!prose) return;
  var heads = Array.prototype.slice.call(prose.querySelectorAll('h2, h3'));
  if (heads.filter(function (h) { return h.tagName === 'H2'; }).length < 2) return;

  var used = {};
  Array.prototype.forEach.call(document.querySelectorAll('[id]'), function (el) { used[el.id] = true; });
  function slugify(t) {
    return (t || '').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 64) || 'section';
  }
  heads.forEach(function (h) {
    if (h.id) return;
    var base = slugify(h.textContent), id = base, n = 2;
    while (used[id]) id = base + '-' + n++;
    used[id] = true; h.id = id;
  });

  function buildList() {
    var ol = document.createElement('ol');
    ol.className = 'toc-list';
    heads.forEach(function (h) {
      var li = document.createElement('li');
      li.className = h.tagName === 'H3' ? 'toc-h3' : 'toc-h2';
      var a = document.createElement('a');
      a.href = '#' + h.id; a.textContent = h.textContent; a.setAttribute('data-toc-id', h.id);
      li.appendChild(a); ol.appendChild(li);
    });
    return ol;
  }

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function onClick(e) {
    var a = e.target.closest('a[data-toc-id]');
    if (!a) return;
    var t = document.getElementById(a.getAttribute('data-toc-id'));
    if (!t) return;
    e.preventDefault();
    t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    if (history.replaceState) history.replaceState(null, '', '#' + t.id);
    t.setAttribute('tabindex', '-1'); t.focus({ preventScroll: true });
    var d = a.closest('details'); if (d) d.open = false;
  }

  // Desktop rail
  var rail = document.createElement('aside');
  rail.className = 'toc-rail';
  var nav = document.createElement('nav');
  nav.className = 'toc'; nav.setAttribute('aria-label', 'Table of contents');
  var title = document.createElement('p'); title.className = 'toc-title'; title.textContent = 'On this page';
  nav.appendChild(title); nav.appendChild(buildList()); rail.appendChild(nav);

  // Mobile details
  var det = document.createElement('details');
  det.className = 'toc-mobile';
  var sum = document.createElement('summary'); sum.textContent = 'Contents';
  var mnav = document.createElement('nav'); mnav.setAttribute('aria-label', 'Table of contents');
  mnav.appendChild(buildList()); det.appendChild(sum); det.appendChild(mnav);

  var wrap = prose.parentElement;
  wrap.classList.add('has-toc');
  wrap.insertBefore(rail, prose);
  wrap.insertBefore(det, prose);
  rail.addEventListener('click', onClick); det.addEventListener('click', onClick);

  // Active section highlight
  if (!('IntersectionObserver' in window)) return;
  var links = Array.prototype.slice.call(rail.querySelectorAll('a[data-toc-id]'));
  var visible = {};
  function setActive(id) {
    links.forEach(function (l) {
      var on = l.getAttribute('data-toc-id') === id;
      l.classList.toggle('active', on);
      if (on) l.setAttribute('aria-current', 'location'); else l.removeAttribute('aria-current');
    });
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { visible[en.target.id] = en.isIntersecting; });
    var cur = null;
    for (var i = 0; i < heads.length; i++) {
      var r = heads[i].getBoundingClientRect();
      if (r.top - 120 <= 0) cur = heads[i].id; else break;
    }
    if (!cur) cur = heads[0].id;
    setActive(cur);
  }, { rootMargin: '-96px 0px -60% 0px', threshold: [0, 1] });
  heads.forEach(function (h) { io.observe(h); });
  addEventListener('scroll', function () {
    var cur = heads[0].id;
    for (var i = 0; i < heads.length; i++) { if (heads[i].getBoundingClientRect().top - 120 <= 0) cur = heads[i].id; else break; }
    setActive(cur);
  }, { passive: true });
  setActive(heads[0].id);
})();
