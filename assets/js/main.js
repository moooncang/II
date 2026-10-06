/* FULL DIVE - ILEON */
(function () {
  var d = document, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
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

  /* 메뉴 */
  var mb = d.querySelector('.menu'), nav = d.querySelector('.nav');
  if (mb && nav) mb.addEventListener('click', function () {
    var o = nav.classList.toggle('open'); mb.setAttribute('aria-expanded', o);
  });

  /* 월드 로그 레일 */
  $$('.rail .feed').forEach(function (f) {
    var ps = $$('p', f), i = 0;
    if (!ps.length) return;
    ps[0].classList.add('on');
    if (reduce || ps.length < 2) return;
    setInterval(function () {
      var cur = ps[i]; i = (i + 1) % ps.length; var nx = ps[i];
      cur.classList.remove('on'); cur.classList.add('off');
      nx.classList.remove('off'); nx.classList.add('on');
      setTimeout(function () { cur.classList.remove('off'); }, 800);
    }, 3600);
  });

  /* 등장: 기본은 보이는 상태, 관찰자가 있을 때만 숨겼다가 한 줄씩 */
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target; io.unobserve(el);
        if (el.classList.contains('typing')) {
          $$('.ln', el).forEach(function (ln, k) { setTimeout(function () { ln.classList.add('on'); }, 160 + k * 240); });
        } else el.classList.add('in');
      });
    }, { rootMargin: '0px 0px -12% 0px' });
    $$('.rv, .typing').forEach(function (el) { io.observe(el); });
  } else {
    $$('.rv').forEach(function (el) { el.classList.add('in'); });
    $$('.typing .ln').forEach(function (el) { el.classList.add('on'); });
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
          map[e.target.id].scrollIntoView({ block: 'nearest', inline: 'center' });
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    Object.keys(map).forEach(function (id) { var t = d.getElementById(id); if (t) so.observe(t); });
  }

  /* 인물 표정 · 게임/현실 */
  var fig = d.querySelector('.viewer .fig');
  if (fig) {
    function show(src, alt) {
      if (fig.getAttribute('src') === src) return;
      fig.classList.add('fade');
      var im = new Image();
      im.onload = im.onerror = function () { fig.src = src; fig.alt = alt; fig.classList.remove('fade'); };
      im.src = src;
    }
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
        $$('.axis-sw button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        $$('.thumbs').forEach(function (t) { t.hidden = t.dataset.axis !== k; });
        var on = d.querySelector('.thumbs[data-axis="' + k + '"] button[aria-pressed="true"]') ||
                 d.querySelector('.thumbs[data-axis="' + k + '"] button');
        if (on) on.click();
      });
    });
  }


  /* 인물 거르기 */
  $$('.filters button').forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.dataset.f;
      $$('.filters button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      $$('.cards .card').forEach(function (c) { c.hidden = f !== 'all' && c.dataset.side !== f; if (!c.hidden) c.classList.add('in'); });
    });
  });

  /* 표지: 부팅 로그 → 접속 */
  var cover = d.querySelector('.cover');
  if (cover) {
    var lines = $$('.boot li:not(.final)', cover);
    lines.forEach(function (li, k) { setTimeout(function () { li.classList.add('on'); }, reduce ? 0 : 300 + k * 420); });
    var go = cover.querySelector('[data-enter]');
    if (go) go.addEventListener('click', function (e) {
      if (reduce) return;
      e.preventDefault();
      var dest = go.getAttribute('href');
      var last = cover.querySelector('.boot .final');
      if (last) last.classList.add('on');
      cover.classList.add('go');
      setTimeout(function () { location.href = dest; }, 1250);
    });
  }
})();
