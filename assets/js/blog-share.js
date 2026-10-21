/* OctoProbe blog: share bar. scripts/build-blog.py injects only the static container (icons,
   aria labels) under the byline of every post; styles live in blog.css (.share-bar).
   This script reads the article's own canonical URL (<link rel="canonical">) and headline
   (<h1>, falling back to og:title) at runtime, URL-encodes them, and builds every share link,
   the mailto, the copy-link value, the utm params and the GA4 `share` event from them, so
   each article is correct automatically. No third-party scripts. */
(function () {
  'use strict';
  var bar = document.querySelector('.share-bar');
  if (!bar) return;

  function meta(sel) { var el = document.querySelector(sel); return el ? (el.getAttribute('content') || el.getAttribute('href') || '').trim() : ''; }
  function clean(u) { return u.split('#')[0].split('?')[0]; }

  // Article identity, from the page itself
  var canonical = meta('link[rel="canonical"]') || meta('meta[property="og:url"]') || clean(location.href);
  var h1 = document.querySelector('h1');
  var title = ((h1 && h1.textContent) || meta('meta[property="og:title"]') || document.title).replace(/\s+/g, ' ').trim();

  // Shared URL per network: canonical + utm so GA attributes the visit (the page's canonical tag stays clean)
  function shareUrl(source) {
    return canonical + (canonical.indexOf('?') < 0 ? '?' : '&') +
      'utm_source=' + encodeURIComponent(source) + '&utm_medium=social';
  }
  var e = encodeURIComponent;
  var BUILD = {
    x:        function (u, t) { return 'https://x.com/intent/post?url=' + e(u) + '&text=' + e(t); },
    facebook: function (u)    { return 'https://facebook.com/sharer/sharer.php?u=' + e(u); },
    linkedin: function (u)    { return 'https://www.linkedin.com/sharing/share-offsite/?url=' + e(u); },
    reddit:   function (u, t) { return 'https://www.reddit.com/submit?url=' + e(u) + '&title=' + e(t); },
    whatsapp: function (u, t) { return 'https://api.whatsapp.com/send?text=' + e(t + ' ' + u); },
    telegram: function (u, t) { return 'https://t.me/share/url?url=' + e(u) + '&text=' + e(t); },
    bluesky:  function (u, t) { return 'https://bsky.app/intent/compose?text=' + e(t + ' ' + u); },
    email:    function (u, t) { return 'mailto:?subject=' + e(t) + '&body=' + e(t + '\n\n' + u); }
  };

  function track(method) {
    if (typeof window.gtag === 'function') {
      window.gtag('event', 'share', { method: method, content_type: 'article', item_id: canonical });
    }
  }

  // Network links
  Array.prototype.forEach.call(bar.querySelectorAll('a.share-link[data-share]'), function (a) {
    var key = a.getAttribute('data-share');
    if (!BUILD[key]) { a.parentNode.hidden = true; return; }
    a.href = BUILD[key](shareUrl(key), title);
    a.addEventListener('click', function () { track(key); });
  });

  // Copy link (clean canonical, no utm)
  var status = bar.querySelector('.share-status');
  var copyItem = bar.querySelector('.share-copy-item');
  var copyBtn = bar.querySelector('.share-copy');
  var timer;
  function say(msg) {
    if (status) status.textContent = msg;
    clearTimeout(timer);
    timer = setTimeout(function () {
      if (status) status.textContent = '';
      if (copyBtn) { copyBtn.classList.remove('is-copied'); copyBtn.setAttribute('aria-label', 'Copy link'); }
    }, 2000);
  }
  if (copyItem && copyBtn) {
    if (navigator.clipboard && window.isSecureContext) {
      copyBtn.addEventListener('click', function () {
        navigator.clipboard.writeText(canonical).then(function () {
          track('copy_link');
          copyBtn.classList.add('is-copied');
          copyBtn.setAttribute('aria-label', 'Link copied');
          say('Copied');
        }, function () { say('Copy failed'); });
      });
    } else {
      copyItem.hidden = true;
    }
  }

  // Mobile: one Share button (system share sheet); the icon row is the fallback.
  var native = bar.querySelector('.share-native');
  if (native && typeof navigator.share === 'function') {
    bar.classList.add('has-native');
    native.addEventListener('click', function () {
      var data = { title: title, text: title, url: shareUrl('web_share') };
      if (navigator.canShare && !navigator.canShare(data)) { bar.classList.add('show-all'); return; }
      navigator.share(data).then(function () { track('web_share'); }, function (err) {
        // AbortError = the reader closed the sheet; anything else: show the icon row instead.
        if (!err || err.name !== 'AbortError') bar.classList.add('show-all');
      });
    });
  }

  bar.hidden = false;
})();
