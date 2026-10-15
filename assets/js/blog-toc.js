/* OctoProbe blog: table of contents.
   One list only: lives in a sticky left rail (>=1024px) or a collapsed
   <details> above the article (<1024px); moved on breakpoint change. */
(function () {
  'use strict';
  var prose = document.querySelector('.post-body .prose');
  if (!prose || document.querySelector('.toc-rail, .toc-mobile')) return;
  var heads = Array.prototype.slice.call(prose.querySelectorAll('h2, h3')).filter(function (h) { return !h.closest('.post-cta'); })
    .filter(function (h) { return h.textContent.trim(); });
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

  // The single list
  var list = document.createElement('ul');
  list.className = 'toc-list';
  list.setAttribute('role', 'list');
  heads.forEach(function (h) {
    var li = document.createElement('li');
    li.className = h.tagName === 'H3' ? 'toc-h3' : 'toc-h2';
    var a = document.createElement('a');
    a.href = '#' + h.id; a.textContent = h.textContent.trim(); a.setAttribute('data-toc-id', h.id);
    li.appendChild(a); list.appendChild(li);
  });
  var nav = document.createElement('nav');
  nav.className = 'toc'; nav.setAttribute('aria-label', 'Table of contents');
  nav.appendChild(list);

  // Containers (only one is ever populated/visible)
  var rail = document.createElement('aside');
  rail.className = 'toc-rail'; rail.hidden = true;
  var label = document.createElement('p'); label.className = 'toc-title'; label.textContent = 'On this page';
  label.setAttribute('aria-hidden', 'true');
  rail.appendChild(label);

  var det = document.createElement('details');
  det.className = 'toc-mobile'; det.hidden = true;
  var sum = document.createElement('summary'); sum.textContent = 'Contents';
  det.appendChild(sum);

  var wrap = prose.parentElement;
  wrap.classList.add('has-toc');
  wrap.insertBefore(rail, prose);
  wrap.insertBefore(det, prose);

  var mq = window.matchMedia('(min-width: 1024px)');
  function place() {
    if (mq.matches) { rail.appendChild(nav); rail.hidden = false; det.hidden = true; det.open = false; wrap.classList.add('toc-on'); }
    else { det.appendChild(nav); det.hidden = false; rail.hidden = true; wrap.classList.remove('toc-on'); }
  }
  place();
  if (mq.addEventListener) mq.addEventListener('change', place); else if (mq.addListener) mq.addListener(place);

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var OFFSET = 88;
  // Scroll to a heading; re-correct if lazy images above it shift the layout.
  function goTo(t, behavior, tries) {
    var y = Math.max(0, t.getBoundingClientRect().top + window.pageYOffset - OFFSET);
    window.scrollTo({ top: y, behavior: behavior });
    var done = false;
    function check() {
      if (done) return; done = true;
      removeEventListener('scrollend', check);
      var off = t.getBoundingClientRect().top - OFFSET;
      if (Math.abs(off) > 4 && tries < 4) goTo(t, 'auto', tries + 1);
    }
    if ('onscrollend' in window) addEventListener('scrollend', check, { once: true });
    setTimeout(check, behavior === 'smooth' ? 900 : 150);
  }
  nav.addEventListener('click', function (e) {
    var a = e.target.closest('a[data-toc-id]');
    if (!a) return;
    var t = document.getElementById(a.getAttribute('data-toc-id'));
    if (!t) return;
    e.preventDefault();
    det.open = false; // collapse first so the layout doesn't shift after scrolling
    requestAnimationFrame(function () {
      t.setAttribute('tabindex', '-1'); t.focus({ preventScroll: true });
      if (history.replaceState) history.replaceState(null, '', '#' + t.id);
      goTo(t, reduce ? 'auto' : 'smooth', 0);
    });
  });

  // Active section
  var links = Array.prototype.slice.call(list.querySelectorAll('a'));
  var current = null;
  function update() {
    var cur = heads[0].id;
    for (var i = 0; i < heads.length; i++) {
      if (heads[i].getBoundingClientRect().top - 120 <= 0) cur = heads[i].id; else break;
    }
    if (cur === current) return;
    current = cur;
    links.forEach(function (l) {
      var on = l.getAttribute('data-toc-id') === cur;
      l.classList.toggle('active', on);
      if (on) {
        l.setAttribute('aria-current', 'location');
        if (!rail.hidden) {
          var r = l.getBoundingClientRect(), n = nav.getBoundingClientRect();
          if (r.top < n.top || r.bottom > n.bottom) nav.scrollTop += r.top - n.top - n.height / 3;
        }
      } else l.removeAttribute('aria-current');
    });
  }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(update, { rootMargin: '-96px 0px -55% 0px' });
    heads.forEach(function (h) { io.observe(h); });
  }
  var tick = false;
  addEventListener('scroll', function () {
    if (tick) return; tick = true;
    requestAnimationFrame(function () { tick = false; update(); });
  }, { passive: true });
  update();
})();
