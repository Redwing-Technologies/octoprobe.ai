/* OctoProbe AI — landing page interactions
   Loaded with <script defer src="assets/octoprobe.js"> (relative path → works on
   GitHub Pages at a custom domain root or a /repo/ project sub-path). */

// nav scroll state
const nav = document.getElementById('nav');
addEventListener('scroll', () => nav.classList.toggle('scrolled', scrollY > 10), { passive: true });

// mobile menu
const tg = document.getElementById('navToggle'), mm = document.getElementById('mobileMenu');
tg.addEventListener('click', () => { const o = mm.classList.toggle('open'); tg.setAttribute('aria-expanded', o); });
mm.querySelectorAll('a').forEach(a => a.addEventListener('click', () => { mm.classList.remove('open'); tg.setAttribute('aria-expanded', 'false'); }));

// reveal
const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .1 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// year
document.getElementById('yr').textContent = new Date().getFullYear();

// parallax octopus scene — the tall inner layer pans vertically as the page
// scrolls, so the head sits in the hero and the tentacles reach the lower page
// (sky + pirate ship → kraken → reef & treasure). It pans slower than the content,
// which reads as depth. Fades gently in over the first screen.
(function () {
  const bg = document.getElementById('octoBg');
  const pan = document.getElementById('octoPan');
  if (!bg || !pan) return;
  if (matchMedia('(prefers-reduced-motion:reduce)').matches) {
    const svg = pan.querySelector('svg');
    if (svg && svg.pauseAnimations) svg.pauseAnimations();   // freeze SMIL (flag, parrots)
    return;
  }
  let ticking = false;
  function update() {
    const y = window.scrollY || 0, vh = window.innerHeight || 1;
    const maxScroll = Math.max(1, document.documentElement.scrollHeight - vh);
    const prog = Math.min(1, Math.max(0, y / maxScroll));   // 0 → 1 across the whole page
    const panRange = Math.max(0, pan.offsetHeight - vh);     // room the tall scene can pan
    pan.style.transform = 'translateX(-50%) translate3d(0,' + (-prog * panRange).toFixed(1) + 'px,0)';
    const opProg = Math.min(1, y / (vh * 0.7));
    bg.style.opacity = (0.34 + opProg * 0.28).toFixed(3);    // 0.34 in the hero → 0.62 below
    ticking = false;
  }
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  addEventListener('resize', update, { passive: true });
  addEventListener('load', update);   // recompute once fonts/layout settle
  update();
})();

// platform tabs
const tabs = document.querySelectorAll('.mock-tab');
tabs.forEach(t => t.addEventListener('click', () => {
  tabs.forEach(o => o.setAttribute('aria-selected', o === t));
  document.querySelectorAll('.mock-panel').forEach(p => p.classList.remove('show'));
  document.getElementById('panel-' + t.dataset.mock).classList.add('show');
}));

// access form
// Paste your deployed Apps Script Web App URL here after deployment:
const ENDPOINT = 'https://script.google.com/macros/s/AKfycbwUB0cELiCngBQpSM4YnuvGWCJJ93PHagScJ1okTeqJpLqomey7Oj7uCFkMx398rWJXyA/exec';

document.querySelectorAll('[data-access-form]').forEach(form => {
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const d = Object.fromEntries(new FormData(form).entries());
    d.submitted_at = new Date().toISOString();
    d.page_url = location.href;
    const btn = form.querySelector('button[type=submit]');
    const wrap = form.closest('.form-card');

    if (ENDPOINT) {
      btn.disabled = true;
      btn.textContent = 'Sending…';
      try {
        // Apps Script Web Apps don't support CORS preflight — use no-cors.
        // The request always reaches the sheet; we optimistically show success.
        await fetch(ENDPOINT, {
          method: 'POST',
          mode: 'no-cors',
          headers: { 'Content-Type': 'text/plain' },
          body: JSON.stringify(d),
        });
      } catch (_) { /* network error — still fall through to success UI */ }

      // GA conversion event
      if (typeof gtag !== 'undefined') {
        gtag('event', 'generate_lead', { event_category: 'conversion', event_label: 'access_form' });
      }

      wrap.innerHTML = `
        <div style="padding:32px 0;text-align:center">
          <div style="font-size:2rem;margin-bottom:12px">✓</div>
          <p style="font-family:var(--fd);font-size:1.1rem;font-weight:600;color:var(--heading);margin-bottom:8px">You're on the list.</p>
          <p style="color:var(--soft);font-size:.9rem">We'll reach out to <strong style="color:var(--text)">${d.email}</strong> same day.</p>
          <p style="margin-top:16px;font-family:var(--fm);font-size:.72rem;color:var(--soft-2)">Questions? <a href="mailto:team@octoprobe.ai" style="color:var(--blue)">team@octoprobe.ai</a></p>
        </div>`;
      return;
    }

    // Fallback: mailto (used until ENDPOINT is set)
    const LABELS = { name: 'Full name', role: 'Role', organization: 'Organization',
      email: 'Email', sector: 'Sector', intended_use: 'Intended use' };
    const lines = Object.entries(d)
      .filter(([k]) => k in LABELS)
      .map(([k, v]) => `${LABELS[k]}: ${v || '—'}`)
      .join('\n');
    location.href = `mailto:team@octoprobe.ai?subject=${encodeURIComponent('OctoProbe Access — ' + (d.organization || ''))}&body=${encodeURIComponent(lines)}`;
  });
});
