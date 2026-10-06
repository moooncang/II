/* FULL DIVE - ILEON · interactions */
(function () {
  var d = document, root = d.documentElement;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(pointer: fine)').matches;
  function $$(s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); }
  function pad(n) { return (n < 10 ? '0' : '') + n; }

  /* 현실 ↔ 벨라트 시계. 시간비 4:1 (현실 6시간 = 게임 1일) */
  function tick() {
    var now = new Date();
    var sec = now.getHours() * 3600 + now.getMinutes() * 60 + now.getSeconds();
    var b = (sec * 4) % 86400;
    var real = pad(now.getHours()) + ':' + pad(now.getMinutes());
    var belat = pad(Math.floor(b / 3600)) + ':' + pad(Math.floor(b % 3600 / 60));
    var date = '2047.' + pad(now.getMonth() + 1) + '.' + pad(now.getDate());
    $$('[data-clock="real"]').forEach(function (e) { e.textContent = real; });
    $$('[data-clock="belat"]').forEach(function (e) { e.textContent = belat; });
    $$('[data-clock="date"]').forEach(function (e) { e.textContent = date; });
  }
  tick(); setInterval(tick, 1000);

  /* 헤더: 맨 위에서는 투명, 내려가면 유리판 */
  var sentinel = d.createElement('div');
  sentinel.style.cssText = 'position:absolute;top:0;left:0;height:80px;width:1px;pointer-events:none';
  d.body.prepend(sentinel);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) { root.classList.toggle('scrolled', !es[0].isIntersecting); }).observe(sentinel);
  }

  /* 메뉴 */
  var mb = d.querySelector('.menu'), nav = d.querySelector('.nav');
  if (mb && nav) {
    mb.addEventListener('click', function () {
      var o = nav.classList.toggle('open'); mb.setAttribute('aria-expanded', o);
    });
    d.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { nav.classList.remove('open'); mb.setAttribute('aria-expanded', 'false'); mb.focus(); }
    });
  }

  /* 월드 로그 */
  $$('.rail .feed').forEach(function (f) {
    var ps = $$('p', f), i = 0;
    if (!ps.length) return;
    ps[0].classList.add('on');
    if (reduce || ps.length < 2) return;
    setInterval(function () {
      var cur = ps[i]; i = (i + 1) % ps.length; var nx = ps[i];
      cur.classList.remove('on'); cur.classList.add('off');
      nx.classList.remove('off'); nx.classList.add('on');
      setTimeout(function () { cur.classList.remove('off'); }, 900);
    }, 3800);
  });

  /* 글자 해독 효과: 히든직 이름이 서버 로그처럼 풀려 나온다 */
  var GLYPH = '▓▒░#%&@$アイウエオ01';
  function scramble(el) {
    var text = el.dataset.final || el.textContent;
    el.dataset.final = text;
    if (reduce) { el.textContent = text; return; }
    var frame = 0, total = 22;
    (function step() {
      var out = '';
      for (var k = 0; k < text.length; k++) {
        var reveal = (frame / total) * text.length > k;
        out += reveal || text[k] === ' ' ? text[k] : GLYPH[(Math.random() * GLYPH.length) | 0];
      }
      el.textContent = out;
      if (++frame <= total) requestAnimationFrame(function () { setTimeout(step, 28); });
      else el.textContent = text;
    })();
  }

  /* 등장 */
  var targets = $$('[data-rv], [data-draw], [data-scramble]');
  if ('IntersectionObserver' in window && !reduce) {
    /* 큰 제목은 clip-path로 가려져 있어 면적이 0이다. 대신 감싼 상자를 지켜본다. */
    var proxy = new Map();
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var watched = e.target; io.unobserve(watched);
        proxy.get(watched).forEach(function (el) {
          el.classList.add('in');
          if (el.hasAttribute('data-scramble')) setTimeout(function () { scramble(el); }, 250);
        });
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0 });
    targets.forEach(function (el) {
      var w = el.classList.contains('mega') ? el.parentElement : el;
      if (!proxy.has(w)) { proxy.set(w, []); io.observe(w); }
      proxy.get(w).push(el);
    });
  } else {
    targets.forEach(function (el) { el.classList.add('in'); });
  }

  /* 글리치: 처음 보일 때 한 번, 올렸을 때, 그리고 가끔 저절로 */
  var gls = $$('.gl');
  function glitch(el) {
    if (reduce || el.classList.contains('go')) return;
    el.classList.add('go');
    setTimeout(function () { el.classList.remove('go'); }, 520);
  }
  if (gls.length && !reduce) {
    gls.forEach(function (el, k) {
      setTimeout(function () { glitch(el); }, 700 + k * 160);
      var host = el.closest('a, h1, h2') || el;
      host.addEventListener('pointerenter', function () { glitch(el); });
    });
    setInterval(function () {
      var vis = gls.filter(function (el) { var r = el.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; });
      if (vis.length) glitch(vis[(Math.random() * vis.length) | 0]);
    }, 4200);
  }

  if (fine && !reduce) {
    /* 자석 버튼 */
    $$('[data-mag]').forEach(function (b) {
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        var x = (e.clientX - r.left - r.width / 2) * .18, y = (e.clientY - r.top - r.height / 2) * .28;
        b.style.transform = 'translate(' + x + 'px,' + y + 'px)';
      });
      b.addEventListener('pointerleave', function () { b.style.transform = ''; });
    });

    /* 첫 화면 그림이 포인터를 따라 살짝 기운다 */
    $$('[data-tilt]').forEach(function (el) {
      var host = el.parentElement, raf = 0, tx = 0, ty = 0;
      host.addEventListener('pointermove', function (e) {
        var r = host.getBoundingClientRect();
        tx = ((e.clientX - r.left) / r.width - .5) * -18;
        ty = ((e.clientY - r.top) / r.height - .5) * -12;
        if (!raf) raf = requestAnimationFrame(function () { el.style.transform = 'translate3d(' + tx + 'px,' + ty + 'px,0)'; raf = 0; });
      });
      host.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
  }

  /* 페이지 안 목차 */
  var toc = $$('.toc a');
  if (toc.length && 'IntersectionObserver' in window) {
    var map = {};
    toc.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var so = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting && map[e.target.id]) {
          toc.forEach(function (a) { a.classList.remove('on'); });
          map[e.target.id].classList.add('on');
          var bar = map[e.target.id].parentNode, a = map[e.target.id];
          bar.scrollTo({ left: a.offsetLeft - bar.clientWidth / 2 + a.clientWidth / 2, behavior: reduce ? 'auto' : 'smooth' });
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    Object.keys(map).forEach(function (id) { var t = d.getElementById(id); if (t) so.observe(t); });
  }

  /* 미끄러지는 선택 표시 (거르기·게임/현실) */
  function pill(group) {
    var p = group.querySelector('.pill'), on = group.querySelector('[aria-selected="true"]');
    if (!p || !on) return;
    p.style.setProperty('--pl', on.offsetLeft + 'px');
    p.style.setProperty('--pw', on.offsetWidth + 'px');
  }
  $$('.filters, .axis-sw').forEach(function (g) { pill(g); addEventListener('resize', function () { pill(g); }); });
  if (d.fonts) d.fonts.ready.then(function () { $$('.filters, .axis-sw').forEach(pill); });

  /* 인물 거르기 */
  $$('.filters button').forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.dataset.f, g = b.parentNode;
      $$('button', g).forEach(function (x) { x.setAttribute('aria-selected', x === b ? 'true' : 'false'); });
      pill(g);
      var n = 0;
      $$('.cards .card').forEach(function (c) {
        var show = f === 'all' || c.dataset.side === f;
        c.classList.toggle('out', !show);
        if (show) { c.classList.remove('in'); c.style.setProperty('--i', n++ % 6); requestAnimationFrame(function () { requestAnimationFrame(function () { c.classList.add('in'); }); }); }
      });
    });
  });

  /* 지역 탭 */
  var rt = $$('.rtabs button');
  if (rt.length) {
    var showRegion = function (key, push) {
      rt.forEach(function (x) { x.setAttribute('aria-selected', x.dataset.r === key ? 'true' : 'false'); });
      $$('.rpane').forEach(function (p) { p.hidden = p.dataset.r !== key; });
      var on = d.querySelector('.rtabs [data-r="' + key + '"]');
      if (on) on.scrollIntoView({ block: 'nearest', inline: 'center', behavior: reduce ? 'auto' : 'smooth' });
      if (push) history.replaceState(null, '', '#' + key);
    };
    rt.forEach(function (b) { b.addEventListener('click', function () { showRegion(b.dataset.r, true); }); });
    d.querySelector('.rtabs').addEventListener('keydown', function (e) {
      var i = rt.indexOf(d.activeElement); if (i < 0) return;
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        var n = rt[(i + (e.key === 'ArrowRight' ? 1 : rt.length - 1)) % rt.length]; n.focus(); n.click(); e.preventDefault();
      }
    });
    var h = location.hash.slice(1);
    if (h && d.querySelector('.rpane[data-r="' + h + '"]')) showRegion(h, false);
  }

  /* 인물 표정 · 게임/현실 */
  var fig = d.querySelector('.viewer .fig');
  if (fig) {
    var show = function (src, alt) {
      if (fig.getAttribute('src') === src) return;
      fig.classList.add('fade');
      var im = new Image();
      im.onload = im.onerror = function () { setTimeout(function () { fig.src = src; fig.alt = alt; fig.classList.remove('fade'); }, 120); };
      im.src = src;
    };
    $$('.thumbs button').forEach(function (b) {
      b.addEventListener('click', function () {
        $$('button', b.parentNode).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true');
        show(b.dataset.src, b.dataset.alt);
      });
    });
    $$('.axis-sw button').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.dataset.axis;
        $$('.axis-sw button').forEach(function (x) { x.setAttribute('aria-selected', x === b ? 'true' : 'false'); });
        pill(b.parentNode);
        $$('.thumbs').forEach(function (t) { t.hidden = t.dataset.axis !== k; });
        var on = d.querySelector('.thumbs[data-axis="' + k + '"] button[aria-pressed="true"]') || d.querySelector('.thumbs[data-axis="' + k + '"] button');
        if (on) on.click();
      });
    });
    d.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      if (/INPUT|TEXTAREA/.test(d.activeElement.tagName) || d.activeElement.closest('.rtabs')) return;
      var bs = $$('.thumbs:not([hidden]) button');
      var i = bs.findIndex(function (x) { return x.getAttribute('aria-pressed') === 'true'; });
      var n = bs[(i + (e.key === 'ArrowRight' ? 1 : bs.length - 1)) % bs.length];
      if (n) n.click();
    });
  }

  /* 표지: 부팅 로그 → 접속 */
  var cover = d.querySelector('.cover');
  if (cover) {
    $$('.boot li:not(.final)', cover).forEach(function (li, k) { setTimeout(function () { li.classList.add('on'); }, reduce ? 0 : 500 + k * 380); });
    var go = cover.querySelector('[data-enter]');
    if (go) go.addEventListener('click', function (e) {
      if (reduce) return;
      e.preventDefault();
      var last = cover.querySelector('.boot .final');
      if (last) last.classList.add('on');
      cover.classList.add('go');
      setTimeout(function () { location.href = go.getAttribute('href'); }, 1300);
    });
  }
})();
