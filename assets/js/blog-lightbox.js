/* OctoProbe blog: click/tap a tall screenshot (figure.shot-mobile > a.shot-open) to open it
   larger in an accessible modal. No dependencies.
   - Native <dialog>.showModal(): page behind is inert, Esc closes (cancel event).
   - X button (aria-label), backdrop or image click closes; focus moves to the X and returns to
     the thumbnail; Tab stays inside; page scroll is locked while open.
   - Without JS or <dialog> support the thumbnail is a plain link to the image file. */
(function () {
  'use strict';
  var links = document.querySelectorAll('.prose figure.shot-mobile > a.shot-open');
  if (!links.length || typeof HTMLDialogElement !== 'function') return;

  var root = document.documentElement;
  var d = document.createElement('dialog');
  d.className = 'shot-dialog';
  d.setAttribute('aria-label', 'Enlarged screenshot');
  d.innerHTML =
    '<button type="button" class="shot-close" aria-label="Close enlarged image">' +
    '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false">' +
    '<path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>' +
    '<figure class="shot-stage"><img alt="" decoding="async"><figcaption id="shot-cap"></figcaption></figure>';
  document.body.appendChild(d);
  var big = d.querySelector('img'), cap = d.querySelector('figcaption'), btn = d.querySelector('.shot-close');
  var opener = null;

  function open(a) {
    var small = a.querySelector('img');
    var fc = a.parentNode.querySelector('figcaption');
    opener = a;
    big.alt = small ? small.alt : '';
    if (small && small.getAttribute('width')) {
      big.setAttribute('width', small.getAttribute('width'));
      big.setAttribute('height', small.getAttribute('height'));
    }
    big.src = a.getAttribute('href');
    cap.textContent = fc ? fc.textContent : '';
    cap.hidden = !cap.textContent;
    if (cap.textContent) d.setAttribute('aria-describedby', 'shot-cap'); else d.removeAttribute('aria-describedby');
    root.classList.add('shot-lock');
    d.showModal();
    btn.focus();
  }
  function close() { if (d.open) d.close(); }

  d.addEventListener('close', function () {
    root.classList.remove('shot-lock');
    big.removeAttribute('src');
    if (opener) { opener.focus(); opener = null; }
  });
  btn.addEventListener('click', close);
  d.addEventListener('click', function (e) {
    if (e.target === d || e.target === big || (e.target.classList && e.target.classList.contains('shot-stage'))) close();
  });
  d.addEventListener('keydown', function (e) {
    if (e.key === 'Tab') { e.preventDefault(); btn.focus(); } // the X is the only control: keep focus in the modal
  });

  var hint = '<span class="shot-hint" aria-hidden="true"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
    '<path d="M14 4h6v6M10 20H4v-6M20 4l-7 7M4 20l7-7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>Enlarge</span>';
  Array.prototype.forEach.call(links, function (a) {
    a.insertAdjacentHTML('beforeend', hint);
    a.addEventListener('click', function (e) {
      if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return; // let new-tab clicks through
      e.preventDefault();
      open(a);
    });
  });
})();
