/* OctoProbe News: search filter bar for the blog index (/blog/).
 *
 * Ranks the existing post cards by how close each story is to the query:
 *   1. Lexical (instant): MiniSearch BM25 over title > description/tags > keywords > body,
 *      with prefix + typo-tolerant matching. Built from /assets/search/index.json.
 *   2. Contextual (lazy): a static sentence-embedding model (Model2Vec potion-base-8M, int8,
 *      ~7.9 MB, fetched once when the reader first uses the search box) embeds the query in
 *      plain JS; posts are scored by cosine similarity to their title/description vector and
 *      their best-matching body passage (/assets/search/vectors.json, built offline by
 *      scripts/build-search-index.py with the same tokenizer). Scores are fused with lexical.
 * Degrades: no JS -> the search bar stays hidden and every card shows, as before; no model
 * (slow/save-data connection, fetch error) -> lexical ranking only; no index -> card text.
 */
(function (root, factory) {
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.OctoSearch = api;
  if (typeof document !== 'undefined') api.mount(document);
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var MODEL_V = 'potion-base-8M-i8-1';
  var W_SEM = 0.65;            // weight of contextual score in the fused rank
  var SEM_FLOOR = 0.26;        // min cosine for a contextual-only match
  var LEX_REL = 0.2;           // min lexical score, relative to the best lexical hit
  var KEEP_REL = 0.45;         // drop results scoring below this share of the top result

  var STOP = {};
  ('a about an and are as at be by can did do does for from has have how i in into is it its ' +
   'me my of on or our s so than that the their them they this to was we were what when where ' +
   'which who why will with you your').split(' ').forEach(function (w) { STOP[w] = 1; });

  // Light English stemmer: enough to fold plurals and common verb endings.
  function stem(w) {
    if (w.length < 5 || /\d/.test(w)) return w;
    if (/ies$/.test(w)) return w.slice(0, -3) + 'y';
    if (/(sses|xes|ches|shes)$/.test(w)) return w.slice(0, -2);
    if (/ing$/.test(w) && w.length > 6) return undouble(w.slice(0, -3));
    if (/ed$/.test(w) && w.length > 5 && !/eed$/.test(w)) return undouble(w.slice(0, -2));
    if (/[^su]s$/.test(w)) return w.slice(0, -1);
    return w;
  }
  function undouble(w) {   // "spott" -> "spot", "planned" -> "plan"; keeps "miss", "call"
    return /([bdgkmnprt])\1$/.test(w) ? w.slice(0, -1) : w;
  }
  function fold(s) {
    return String(s).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[\u2018\u2019\u02bc]/g, "'");
  }
  function processTerm(t) {
    t = fold(t).replace(/^'+|'+$/g, '').replace(/'s$/, '');
    if (!t || STOP[t]) return null;
    return stem(t);
  }

  // ── WordPiece tokenizer (BERT uncased), mirrors scripts/build-search-index.py ──
  var PUNCT = /[\p{P}\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]/u;
  var MARK = /\p{Mn}/u;
  var CTRL = /[\p{Cc}\p{Cf}]/u;
  function isCJK(cp) {
    return (cp >= 0x4E00 && cp <= 0x9FFF) || (cp >= 0x3400 && cp <= 0x4DBF) ||
      (cp >= 0x20000 && cp <= 0x2A6DF) || (cp >= 0x2A700 && cp <= 0x2B73F) ||
      (cp >= 0x2B740 && cp <= 0x2B81F) || (cp >= 0x2B820 && cp <= 0x2CEAF) ||
      (cp >= 0xF900 && cp <= 0xFAFF) || (cp >= 0x2F800 && cp <= 0x2FA1F);
  }
  function words(text) {
    var out = [], cur = '';
    var s = String(text).toLowerCase().normalize('NFD');
    for (var ch of s) {
      var cp = ch.codePointAt(0);
      if (cp === 0 || cp === 0xFFFD || MARK.test(ch)) continue;
      if (/\s/.test(ch) || (CTRL.test(ch) && ch !== '\t' && ch !== '\n' && ch !== '\r')) {
        if (cur) { out.push(cur); cur = ''; }
      } else if (PUNCT.test(ch) || isCJK(cp)) {
        if (cur) { out.push(cur); cur = ''; }
        out.push(ch);
      } else cur += ch;
    }
    if (cur) out.push(cur);
    return out;
  }
  function makeTokenizer(vocab, unk) {
    var ids = new Map();
    vocab.forEach(function (t, i) { ids.set(t, i); });
    var unkId = ids.has(unk) ? ids.get(unk) : -1;
    return function encode(text) {
      var res = [];
      words(text).forEach(function (w) {
        var chars = Array.from(w);
        if (chars.length > 100) { if (unkId >= 0) res.push(unkId); return; }
        var start = 0, pieces = [], bad = false;
        while (start < chars.length) {
          var end = chars.length, hit = -1;
          while (start < end) {
            var sub = chars.slice(start, end).join('');
            if (start > 0) sub = '##' + sub;
            if (ids.has(sub)) { hit = ids.get(sub); break; }
            end--;
          }
          if (hit < 0) { bad = true; break; }
          pieces.push(hit); start = end;
        }
        if (bad) { if (unkId >= 0) res.push(unkId); } else res.push.apply(res, pieces);
      });
      return res;
    };
  }

  function b64ToInt8(s) {
    var bin = atob(s), out = new Int8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = (bin.charCodeAt(i) << 24) >> 24;
    return out;
  }

  // Static embedding model: mean of int8 token rows (x per-row scale), L2-normalised.
  function makeModel(meta, vocabText, scalesBuf, embBuf) {
    var vocab = vocabText.split('\n');
    if (vocab[vocab.length - 1] === '') vocab.pop();
    var dim = meta.dim, q = new Int8Array(embBuf), sc = new Float32Array(scalesBuf);
    if (q.length !== vocab.length * dim || sc.length !== vocab.length) throw new Error('model size mismatch');
    var skip = new Set(meta.skip_ids || []);
    var encode = makeTokenizer(vocab, meta.unk_token || '[UNK]');
    var whole = new Set(vocab);
    return {
      dim: dim,
      encode: encode,
      // Share of the query's content words the model knows as whole words. Gibberish and
      // unknown names split into sub-word pieces whose average vector is noise.
      coverage: function (text) {
        var ws = words(text).filter(function (w) { return /[\p{L}\p{N}]/u.test(w) && !STOP[w]; });
        if (!ws.length) return 0;
        return ws.filter(function (w) { return whole.has(w); }).length / ws.length;
      },
      embed: function (text) {
        var acc = new Float32Array(dim), n = 0;
        encode(text).forEach(function (id) {
          if (skip.has(id)) return;
          var s = sc[id], o = id * dim;
          for (var k = 0; k < dim; k++) acc[k] += q[o + k] * s;
          n++;
        });
        if (!n) return null;
        var norm = 0;
        for (var k = 0; k < dim; k++) norm += acc[k] * acc[k];
        norm = Math.sqrt(norm) || 1;
        for (k = 0; k < dim; k++) acc[k] /= norm;
        return acc;
      }
    };
  }

  function makeVectors(vec) {
    var dim = vec.dim, by = {};
    vec.posts.forEach(function (p) {
      by[p.slug] = { head: b64ToInt8(p.head), passages: p.passages.map(b64ToInt8) };
    });
    function dot(a, b) { var s = 0; for (var k = 0; k < dim; k++) s += a[k] * b[k]; return s / 127; }
    return {
      // 0.5 * title/description similarity + 0.5 * best body-passage similarity
      score: function (slug, qv) {
        var p = by[slug];
        if (!p || !qv) return 0;
        var best = -1;
        for (var i = 0; i < p.passages.length; i++) { var d = dot(p.passages[i], qv); if (d > best) best = d; }
        return 0.5 * dot(p.head, qv) + 0.5 * Math.max(best, 0);
      }
    };
  }

  function makeLexical(MiniSearch, posts) {
    var docs = posts.map(function (p) {
      return {
        id: p.slug, title: p.title, description: p.description || '', category: p.category || '',
        tags: (p.tags || []).join(' '), keywords: (p.keywords || []).join(' '), body: p.body || ''
      };
    });
    if (!MiniSearch) {
      // Tiny fallback if the vendored library failed to load: weighted term overlap.
      return function (query) {
        var terms = query.split(/[^\p{L}\p{N}']+/u).map(processTerm).filter(Boolean);
        var out = {};
        docs.forEach(function (d) {
          var s = 0;
          [['title', 4], ['description', 2], ['tags', 2], ['keywords', 1.5], ['body', 0.5]].forEach(function (f) {
            var txt = fold(d[f[0]]);
            terms.forEach(function (t) { if (txt.indexOf(t) >= 0) s += f[1]; });
          });
          if (s) out[d.id] = s;
        });
        return out;
      };
    }
    var ms = new MiniSearch({
      fields: ['title', 'description', 'category', 'tags', 'keywords', 'body'],
      processTerm: processTerm,
      searchOptions: {
        boost: { title: 4, description: 2, tags: 2, category: 1.5, keywords: 1.5, body: 1 },
        // search-as-you-type: only the last word may be a prefix; typo tolerance on long words
        prefix: function (t, i, all) { return i === all.length - 1 && t.length >= 3; },
        fuzzy: function (t) { return t.length >= 6 ? 0.2 : false; },
        combineWith: 'OR'
      }
    });
    ms.addAll(docs);
    return function (query) {
      var out = {};
      ms.search(query).forEach(function (r) { out[r.id] = r.score; });
      return out;
    };
  }

  /* Rank slugs for a query. lex: {slug: score}; sem: function(slug) -> cosine or null. */
  function rank(slugs, lex, sem) {
    var maxLex = 0, maxSem = 0, rows = [];
    slugs.forEach(function (s) { if ((lex[s] || 0) > maxLex) maxLex = lex[s]; });
    slugs.forEach(function (s) {
      var l = maxLex ? (lex[s] || 0) / maxLex : 0;
      var c = sem ? sem(s) : 0;
      if (c > maxSem) maxSem = c;
      rows.push({ slug: s, lex: l, sem: c });
    });
    var useSem = !!sem && maxSem >= SEM_FLOOR;
    rows.forEach(function (r) {
      r.ok = r.lex >= LEX_REL || (useSem && r.sem >= SEM_FLOOR);
      r.score = useSem ? W_SEM * (r.sem / maxSem) + (1 - W_SEM) * r.lex : r.lex;
    });
    rows = rows.filter(function (r) { return r.ok; }).sort(function (a, b) { return b.score - a.score; });
    if (rows.length) {
      var top = rows[0].score;
      rows = rows.filter(function (r) { return r.score >= KEEP_REL * top; });
    }
    return rows;
  }

  function engine(posts, MiniSearch) {
    var slugs = posts.map(function (p) { return p.slug; });
    var lexical = makeLexical(MiniSearch, posts);
    var model = null, vectors = null;
    return {
      setSemantic: function (m, v) { model = m; vectors = v; },
      semanticReady: function () { return !!(model && vectors); },
      search: function (query) {
        var lex = lexical(query);
        var qv = model && vectors && query.replace(/\s+/g, '').length >= 3 &&
          model.coverage(query) >= 0.5 ? model.embed(query) : null;
        return rank(slugs, lex, qv ? function (s) { return vectors.score(s, qv); } : null);
      }
    };
  }

  // ── DOM ────────────────────────────────────────────────────────────────────
  function mount(doc) {
    var box = doc.getElementById('blogSearch');
    var grid = doc.getElementById('postGrid');
    if (!box || !grid || !doc.addEventListener) return;
    var win = doc.defaultView;
    var input = doc.getElementById('blogSearchInput');
    var clear = box.querySelector('.blog-search-clear');
    var status = doc.getElementById('blogSearchStatus');
    var empty = doc.getElementById('blogSearchEmpty');
    var emptyQ = doc.getElementById('blogSearchEmptyQuery');
    var showAll = doc.getElementById('blogSearchShowAll');
    var base = box.getAttribute('data-search-base') || '/assets/search/';
    var ver = box.getAttribute('data-search-version') || '1';
    var cards = Array.prototype.slice.call(grid.querySelectorAll('.post-card'));
    var bySlug = {};
    cards.forEach(function (c) {
      var m = (c.getAttribute('href') || '').match(/\/blog\/([^/]+)\//);
      if (m) bySlug[m[1]] = c;
    });
    var eng = null, enginePromise = null, modelPromise = null, lastQ = null, urlTimer = 0;

    box.hidden = false;
    doc.documentElement.classList.add('has-blog-search');

    function getJSON(url) {
      return win.fetch(url, { credentials: 'same-origin' }).then(function (r) {
        if (!r.ok) throw new Error(url + ' ' + r.status); return r.json();
      });
    }
    function getBuf(url) {
      return win.fetch(url, { credentials: 'same-origin' }).then(function (r) {
        if (!r.ok) throw new Error(url + ' ' + r.status); return r.arrayBuffer();
      });
    }
    function getText(url) {
      return win.fetch(url, { credentials: 'same-origin' }).then(function (r) {
        if (!r.ok) throw new Error(url + ' ' + r.status); return r.text();
      });
    }
    function postsFromCards() {
      return cards.map(function (c) {
        var h = c.querySelector('h2'), e = c.querySelector('.excerpt');
        return {
          slug: (c.getAttribute('href').match(/\/blog\/([^/]+)\//) || [])[1],
          title: h ? h.textContent : '', description: e ? e.textContent : '',
          tags: Array.prototype.map.call(c.querySelectorAll('.tag'), function (t) { return t.textContent; })
        };
      });
    }
    function loadEngine() {
      if (enginePromise) return enginePromise;
      enginePromise = getJSON(base + 'index.json?v=' + ver)
        .then(function (ix) { return ix.posts.filter(function (p) { return bySlug[p.slug]; }); })
        .catch(function () { return postsFromCards(); })
        .then(function (posts) { eng = engine(posts, win.MiniSearch); return eng; });
      return enginePromise;
    }
    function semanticAllowed() {
      var c = win.navigator && win.navigator.connection;
      // ~7.9 MB model: skip it on Save-Data and on 2G/3G-class connections
      if (c && (c.saveData || /^(slow-2g|2g|3g)$/.test(c.effectiveType || ''))) return false;
      return typeof win.fetch === 'function' && typeof Int8Array !== 'undefined';
    }
    function loadModel() {
      if (modelPromise || !semanticAllowed()) return modelPromise;
      var mb = base + 'model/', mv = '?v=' + MODEL_V, t0 = Date.now();
      modelPromise = Promise.all([
        getJSON(mb + 'meta.json' + mv), getText(mb + 'vocab.txt' + mv),
        getBuf(mb + 'scales.f32' + mv), getBuf(mb + 'embeddings.i8' + mv),
        getJSON(base + 'vectors.json?v=' + ver), loadEngine()
      ]).then(function (r) {
        eng.setSemantic(makeModel(r[0], r[1], r[2], r[3]), makeVectors(r[4]));
        box.setAttribute('data-semantic', 'ready');
        box.setAttribute('data-semantic-ms', String(Date.now() - t0));
        if (lastQ) run(true);
      }).catch(function () {
        box.setAttribute('data-semantic', 'off');   // lexical ranking stays in place
        if (lastQ) run(true);
      });
      return modelPromise;
    }
    function warm() { loadEngine(); loadModel(); }

    function plural(n) { return n === 1 ? '1 story' : n + ' stories'; }
    function show(list) {
      // list: ordered slugs to show, or null for every card in its original order
      var frag = doc.createDocumentFragment(), keep = {};
      if (list) list.forEach(function (s) { keep[s] = 1; var c = bySlug[s]; c.hidden = false; c.classList.add('in'); frag.appendChild(c); });
      cards.forEach(function (c) {
        if (!list) { c.hidden = false; frag.appendChild(c); return; }
        var m = (c.getAttribute('href') || '').match(/\/blog\/([^/]+)\//);
        if (!m || !keep[m[1]]) { c.hidden = true; frag.appendChild(c); }
      });
      grid.appendChild(frag);
    }
    function setURL(q) {
      win.clearTimeout(urlTimer);
      urlTimer = win.setTimeout(function () {
        try {
          var u = new win.URL(win.location.href);
          if (q) u.searchParams.set('q', q); else u.searchParams.delete('q');
          win.history.replaceState(win.history.state, '', u.pathname + u.search + u.hash);
        } catch (e) { /* ignore */ }
      }, 350);
    }
    function run(force) {
      var raw = input.value, q = raw.trim();
      clear.hidden = !raw;
      box.classList.toggle('is-active', !!q);
      if (!force && q === lastQ) return;
      lastQ = q;
      setURL(q);
      if (q.length < 2) {
        box.classList.remove('is-empty');
        show(null);
        grid.hidden = false; empty.hidden = true;
        status.textContent = '';
        box.removeAttribute('data-results');
        grid.removeAttribute('aria-busy');
        return;
      }
      if (!eng) { grid.setAttribute('aria-busy', 'true'); loadEngine().then(function () { if (input.value.trim() === q) run(true); }); return; }
      grid.removeAttribute('aria-busy');
      var rows = eng.search(q);
      box.classList.toggle('is-empty', !rows.length);
      if (!rows.length) {
        show([]); grid.hidden = true; empty.hidden = false;
        emptyQ.textContent = q;
        status.textContent = 'No stories match \u201c' + q + '\u201d';
        box.setAttribute('data-results', '');
        return;
      }
      grid.hidden = false; empty.hidden = true;
      show(rows.map(function (r) { return r.slug; }));
      status.textContent = plural(rows.length) + ' \u00b7 closest match first' +
        (eng.semanticReady() ? '' : (modelPromise && box.getAttribute('data-semantic') !== 'off' ? ' \u00b7 refining\u2026' : ''));
      box.setAttribute('data-results', rows.map(function (r) { return r.slug; }).join(' '));
    }

    input.addEventListener('focus', warm, { once: true });
    input.addEventListener('input', function () { run(false); });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        if (input.value) { input.value = ''; run(false); e.preventDefault(); }
        else input.blur();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        run(true);
        var first = grid.querySelector('.post-card:not([hidden])');
        if (first && input.value.trim().length >= 2 && !grid.hidden) first.focus();
      }
    });
    clear.addEventListener('click', function () { input.value = ''; run(false); input.focus(); });
    showAll.addEventListener('click', function () { input.value = ''; run(false); input.focus(); });
    doc.addEventListener('keydown', function (e) {
      if (e.key !== '/' || e.ctrlKey || e.metaKey || e.altKey) return;
      var t = e.target, tag = t && t.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (t && t.isContentEditable)) return;
      e.preventDefault(); input.focus();
    });

    var q0 = '';
    try { q0 = new win.URL(win.location.href).searchParams.get('q') || ''; } catch (e) { /* ignore */ }
    if (q0) input.value = q0;
    if (input.value) { warm(); run(true); }   // deep link, or text typed/restored before mount
  }

  return { mount: mount, engine: engine, rank: rank, makeModel: makeModel, makeVectors: makeVectors,
           makeTokenizer: makeTokenizer, processTerm: processTerm };
}));
