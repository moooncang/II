/* FULL DIVE - ILEON · 게임 클라이언트 동작
   전체 구조: 한 번만 뜨는 것(효과음, 배경음악, 키, 페이지 전환)과 페이지마다 새로 붙는 것(page())으로 나뉜다.
   사이트 안 링크는 새로고침 없이 본문만 바꿔 끼워서 음악이 끊기지 않는다. */
(function () {
  var d = document, root = d.documentElement;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var touch = matchMedia('(hover: none), (max-width: 900px)').matches;
  if (touch) root.classList.add('touch');
  function $(s, r) { return (r || d).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function typing() { var a = d.activeElement; return a && /INPUT|TEXTAREA|SELECT/.test(a.tagName); }
  var SCRIPT = (d.currentScript && d.currentScript.src) || '';
  var SITE = SCRIPT.replace(/assets\/js\/main\.js.*$/, '');

  /* ── 페이지 수명: 페이지를 떠날 때 이 페이지가 붙인 것을 모두 걷어낸다 ── */
  var P = null;
  function scope() {
    if (P) { P.dead = true; P.ac.abort(); P.t.forEach(clearInterval); P.o.forEach(clearTimeout); P.io.forEach(function (o) { o.disconnect(); }); P.fin.forEach(function (f) { f(); }); }
    P = { dead: false, ac: new AbortController(), t: [], o: [], io: [], fin: [] };
  }
  function on(t, type, fn, o) { o = o || {}; o.signal = P.ac.signal; t.addEventListener(type, fn, o); }
  function every(fn, ms) { P.t.push(setInterval(fn, ms)); }
  function later(fn, ms) { var id = setTimeout(fn, ms); P.o.push(id); return id; }
  /* 화면에 들어와 있는 동안만 콜백을 켠다 */
  function whileVisible(el, inF, outF, th) {
    if (!el) return;
    if (!('IntersectionObserver' in window)) { inF(); return; }
    var io = new IntersectionObserver(function (es) { es[0].isIntersecting ? inF() : outF && outF(); }, { threshold: th == null ? .4 : th });
    io.observe(el); P.io.push(io);
  }
  function replaceHash(h) { history.replaceState(history.state, '', '#' + h); }

  /* ── 효과음: ElevenLabs로 만든 짧은 UI 소리. 첫 조작 뒤에만 울리고, 끄면 기억한다 ── */
  var sfx = (function () {
    var base = SITE + 'assets/sfx/';
    var VOL = { loading: .5, enter: .7, hover: .14, click: .4, menu: .45, select: .24, travel: .4, flip: .32, reveal: .45 };
    var AC = window.AudioContext || window.webkitAudioContext, ctx, out, raw = {}, buf = {}, last = {}, live = {};
    var on_ = true; try { on_ = localStorage.getItem('ileon-sfx') !== 'off'; } catch (e) {}
    var fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
    function load(n) {
      if (!raw[n]) raw[n] = fetch(base + n + '.mp3').then(function (r) { return r.ok ? r.arrayBuffer() : Promise.reject(); });
      return raw[n];
    }
    function decode(n) {
      if (!buf[n]) buf[n] = load(n).then(function (a) { return new Promise(function (ok, no) { ctx.decodeAudioData(a.slice(0), ok, no); }); });
      return buf[n];
    }
    function wake() {
      if (!AC) return;
      if (!ctx) { ctx = new AC(); out = ctx.createGain(); out.gain.value = .8; out.connect(ctx.destination); Object.keys(VOL).forEach(decode); }
      if (ctx.state === 'suspended') ctx.resume();
    }
    ['pointerdown', 'keydown'].forEach(function (t) { addEventListener(t, wake, { capture: true, passive: true }); });
    function play(n, gap, from) {
      if (!on_ || !ctx || d.hidden) return;
      /* 막 누른 순간이면 깨어나는 중인 소리판을 기다린다. 그 밖에 잠든 상태면 울리지 않는다 */
      var ua = navigator.userActivation, waking = ctx.state === 'suspended' && (!ua || ua.isActive);
      if (ctx.state !== 'running' && !waking) return;
      var now = performance.now(); if (last[n] && now - last[n] < (gap == null ? 60 : gap)) return; last[n] = now;
      (waking ? ctx.resume() : Promise.resolve()).then(function () { return decode(n); }).then(function (b) {
        if (!last[n]) return;
        var s = ctx.createBufferSource(), g = ctx.createGain();
        g.gain.value = VOL[n]; s.buffer = b; s.connect(g); g.connect(out);
        var off = from ? (performance.now() - from) / 1000 : 0;
        if (off >= b.duration) return;
        s.start(0, off); live[n] = { s: s, g: g };
      }).catch(function () {});
    }
    /* 재생 중인 소리를 짧게 줄이며 멈춘다 */
    function stop(n) {
      last[n] = 0; var l = live[n]; if (!l || !ctx) return; live[n] = null;
      try { l.g.gain.setTargetAtTime(0, ctx.currentTime, .04); l.s.stop(ctx.currentTime + .2); } catch (e) {}
    }
    function paint() { $$('.snd').forEach(function (b) { b.setAttribute('aria-pressed', on_); $('b', b).textContent = on_ ? 'ON' : 'OFF'; }); }
    function set(v) {
      on_ = v; try { localStorage.setItem('ileon-sfx', v ? 'on' : 'off'); } catch (e) {}
      paint(); if (v) { wake(); play('click'); }
    }
    d.addEventListener('click', function (e) {
      var s = e.target.closest && e.target.closest('.snd');
      if (s) { e.stopPropagation(); e.preventDefault(); set(!on_); return; }
      /* 버튼과 링크는 누를 때 확인음. 따로 소리를 정한 곳은 건너뛴다 */
      var t = e.target.closest && e.target.closest('a[href], button');
      if (!t || t.closest('[data-mu-id], .mu-ctl, .mu-mini, .hbgm, .esc, .menu-x, [data-cover], .tv-list, .ng .slot, .thumbs, [data-jobs] [data-next]')) return;
      play('click');
    }, true);
    /* 마우스로 훑을 때만 짧은 틱. 손가락 조작에는 붙이지 않는다 */
    if (fine) d.addEventListener('mouseover', function (e) {
      var t = e.target.closest && e.target.closest('.tabs a, .menu ol a, .tmenu a, .rg, .sl, .ng .slot, .tv-list button, .btn, .esc, .snd, .hbgm-b');
      if (t && !t.contains(e.relatedTarget)) play('hover', 70);
    });
    return { play: play, stop: stop, load: load, paint: paint, toggle: function () { set(!on_); } };
  })();

  /* ── 배경음악 엔진: 페이지를 옮겨도 같은 소리가 계속 난다. 처음 들어오면 메인 테마 ── */
  var bgm = (function () {
    var data = $('#bgm-data'), list = data ? JSON.parse(data.textContent) : [];
    var a = new Audio(), subs = [], idx = 0, st = {}, api, ac = null, an = null;
    try { st = JSON.parse(localStorage.getItem('ileon-bgm')) || {}; } catch (e) {}
    var want = st.on !== false;
    a.preload = 'auto';
    function save() {
      if (!list.length) return;
      st.id = list[idx].id; st.on = want; st.vol = api.vol; st.rep = api.rep;
      if (a.currentTime) st.t = a.currentTime;
      try { localStorage.setItem('ileon-bgm', JSON.stringify(st)); } catch (e) {}
    }
    function hud() {
      var x = list[idx]; if (!x) return;
      root.classList.toggle('bgm-on', !a.paused);
      $$('[data-bgm]').forEach(function (h) {
        h.classList.toggle('wait', want && a.paused);
        var n = $('[data-bgm-name]', h); if (n.textContent !== x.n) n.textContent = x.n;
        var b = $('[data-bgm-toggle]', h); b.setAttribute('aria-pressed', want); b.setAttribute('aria-label', (want ? '배경음악 끄기' : '배경음악 켜기') + ' (B)');
      });
    }
    function emit() { subs.forEach(function (f) { f(); }); hud(); }
    function load(i, t) {
      idx = (i + list.length) % list.length; api.idx = idx; api.t0 = t || 0;
      a.src = SITE + 'assets/bgm/' + list[idx].id + '.mp3';
      if (t) a.addEventListener('loadedmetadata', function () { try { a.currentTime = Math.min(t, (a.duration || t + 1) - 1); } catch (e) {} }, { once: true });
      a.loop = api.rep;
      if ('mediaSession' in navigator && window.MediaMetadata) navigator.mediaSession.metadata = new MediaMetadata({ title: list[idx].n + ' · ' + list[idx].t, artist: 'FULL DIVE - ILEON', album: 'ILEON Soundtrack', artwork: [{ src: SITE + 'images/bgm/s/' + list[idx].id + '.webp', sizes: '640x360', type: 'image/webp' }] });
    }
    /* 소리 모양(음악 페이지)을 위한 오디오 그래프. 누른 순간에만 만든다(그 밖에 만들면 소리가 멎는다) */
    function analyser() {
      if (an || reduce) return an;
      var ua = navigator.userActivation; if (ua && !ua.isActive) return null;
      var AC = window.AudioContext || window.webkitAudioContext; if (!AC) return null;
      try { ac = new AC(); var src = ac.createMediaElementSource(a); an = ac.createAnalyser(); an.fftSize = 128; an.smoothingTimeConstant = .8; src.connect(an); an.connect(ac.destination); } catch (e) { an = null; }
      return an;
    }
    function play() {
      if (!list.length) return;
      want = true;
      if (ac && ac.state !== 'running') ac.resume();
      var p = a.play(); if (p && p.catch) p.catch(function () { hud(); });
      save(); hud();
    }
    function pause() { want = false; a.pause(); save(); emit(); }
    api = {
      list: list, audio: a, idx: 0, t0: 0, rep: !!st.rep,
      vol: st.vol != null ? st.vol / (st.vol > 1 ? 100 : 1) : .6,
      playing: function () { return !a.paused; },
      onChange: function (f) { subs.push(f); return function () { subs = subs.filter(function (x) { return x !== f; }); }; },
      analyser: analyser, hud: hud, play: play, pause: pause,
      toggle: function () { want && !a.paused ? pause() : play(); },
      go: function (i, autoplay) { var was = !a.paused || autoplay; load(i, 0); if (was) play(); save(); emit(); },
      seek: function (r) { if (a.duration) a.currentTime = r * a.duration; else if (r === 0) a.currentTime = 0; save(); },
      setVol: function (v) { api.vol = v; a.volume = v; save(); },
      setRep: function (v) { api.rep = v; a.loop = v; save(); emit(); },
      /* 표지에서 시작: 메인 테마. 이미 메인 테마가 나오고 있으면 그대로 둔다 */
      fresh: function () { if (!want && st.on === false) return; if (idx !== 0) load(0, 0); if (a.paused) play(); }
    };
    a.volume = api.vol;
    ['play', 'pause'].forEach(function (t) { a.addEventListener(t, emit); });
    a.addEventListener('ended', function () { api.go(idx + 1, true); });
    if (list.length) {
      /* 표지는 늘 메인 테마로 시작. 다른 페이지로 바로 들어오면 듣던 곡을 이어서 */
      var cover = !!$('[data-cover]'), si = list.findIndex(function (x) { return x.id === st.id; });
      if (cover) load(0, 0); else load(Math.max(0, si), si >= 0 ? st.t : 0);
      /* 들어오자마자 튼다. 브라우저가 막으면 첫 클릭이나 키에서 튼다 */
      if (want) play();
    }
    ['pointerdown', 'keydown'].forEach(function (t) {
      addEventListener(t, function (e) {
        if (!want || !a.paused || !list.length) return;
        if (e.target.closest && e.target.closest('[data-bgm-toggle], [data-mu-pp], [data-mu-id], .snd')) return;
        if ($('[data-cover]')) { if (idx !== 0) load(0, 0); }
        play();
      }, { capture: true, passive: true });
    });
    d.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('[data-bgm-toggle]')) api.toggle(); });
    if ('mediaSession' in navigator) {
      try {
        navigator.mediaSession.setActionHandler('play', play);
        navigator.mediaSession.setActionHandler('pause', pause);
        navigator.mediaSession.setActionHandler('previoustrack', function () { api.go(idx - 1); });
        navigator.mediaSession.setActionHandler('nexttrack', function () { api.go(idx + 1); });
      } catch (e) {}
    }
    addEventListener('pagehide', save);
    d.addEventListener('visibilitychange', function () { if (d.hidden) save(); });
    setInterval(function () { if (!a.paused) save(); }, 2000);
    return api;
  })();

  /* ── 전역 키: ESC 메뉴, 숫자 탭, M 효과음, B 배경음악 ── */
  d.addEventListener('keydown', function (e) {
    if (typing() || e.metaKey || e.ctrlKey || e.altKey || $('[data-cover]')) return;
    var menu = $('.menu');
    if (e.key === 'Escape' && menu) { openMenu(menu.hidden); e.preventDefault(); return; }
    var tabs = $$('.tabs a');
    if (/^[1-6]$/.test(e.key) && tabs[+e.key - 1]) { sfx.play('click'); go(tabs[+e.key - 1].href); return; }
    if (e.key === 'm' || e.key === 'M') sfx.toggle();
    if (e.key === 'b' || e.key === 'B') bgm.toggle();
  });
  function openMenu(o) {
    var menu = $('.menu'), escBtn = $('.esc'); if (!menu) return;
    if (menu.hidden === !o) return;
    menu.hidden = !o; menu.classList.toggle('open', o);
    sfx.play(o ? 'menu' : 'click');
    if (escBtn) escBtn.setAttribute('aria-expanded', o);
    d.body.style.overflow = o ? 'hidden' : '';
    if (o) { var c = $('ol a[aria-current]', menu) || $('ol a', menu); if (c) { c.focus(); setBg(c); } }
    else if (escBtn) escBtn.focus({ preventScroll: true });
  }
  function setBg(a) { var bg = $('.menu-bg'); if (bg && a.dataset.bg) bg.style.backgroundImage = 'url("' + a.dataset.bg + '")'; }

  /* ── 페이지 전환: 사이트 안 링크는 본문만 바꿔 끼운다 ── */
  var busy = 0, here = location.pathname;
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  history.replaceState({ y: scrollY }, '', location.href);
  function inside(u) {
    return u.origin === location.origin && (/\.html$/.test(u.pathname) || /\/$/.test(u.pathname)) && u.pathname.indexOf(SITE.replace(location.origin, '')) === 0;
  }
  function go(href, pop) {
    var u = new URL(href, location.href);
    if (!inside(u) || !window.fetch || !window.DOMParser) { location.href = u.href; return; }
    if (!pop && u.pathname === location.pathname && u.search === location.search) {
      if (u.hash) { var t = d.getElementById(decodeURIComponent(u.hash.slice(1))); if (t) { replaceHash(u.hash.slice(1)); t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' }); return; } }
      if (!u.hash) { scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); return; }
    }
    var n = ++busy;
    root.classList.add('leaving');
    if (!pop) history.replaceState({ y: scrollY }, '', location.href);
    fetch(u.href, { credentials: 'same-origin' }).then(function (r) {
      if (!r.ok) throw 0;
      return r.text();
    }).then(function (html) {
      if (n !== busy) return;
      var doc = new DOMParser().parseFromString(html, 'text/html');
      if (!doc.body || !doc.querySelector('script[src*="main.js"]')) throw 0;
      if (!pop) history.pushState({ y: 0 }, '', u.href);
      var swap = function () {
        d.title = doc.title;
        var desc = doc.querySelector('meta[name="description"]'), md = $('meta[name="description"]');
        if (desc && md) md.setAttribute('content', desc.getAttribute('content'));
        $$('script', doc.body).forEach(function (s) { if (s.src || s.id === 'bgm-data') s.remove(); });
        d.body.className = doc.body.className; d.body.removeAttribute('style');
        d.body.replaceChildren.apply(d.body, Array.prototype.slice.call(doc.body.childNodes).map(function (x) { return d.adoptNode(x); }));
        root.classList.remove('scrolled', 'leaving');
        here = location.pathname;
        page();
        var y = pop && history.state && history.state.y;
        if (y) scrollTo(0, y);
        else if (u.hash && d.getElementById(decodeURIComponent(u.hash.slice(1)))) d.getElementById(decodeURIComponent(u.hash.slice(1))).scrollIntoView();
        else scrollTo(0, 0);
        var f = $('main') || d.body; if (f && !pop) { f.setAttribute('tabindex', '-1'); f.focus({ preventScroll: true }); }
      };
      if (d.startViewTransition && !reduce) d.startViewTransition(swap); else swap();
    }).catch(function () { location.href = u.href; });
  }
  d.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || a.target || a.hasAttribute('download') || a.getAttribute('href').charAt(0) === '#') return;
    var u = new URL(a.href, location.href);
    if (!inside(u)) return;
    e.preventDefault();
    go(u.href);
  });
  addEventListener('popstate', function () {
    if (location.pathname === here) return;
    go(location.href, true);
  });
  /* 떠나기 전 스크롤 위치 */
  var sy = 0;
  addEventListener('scroll', function () { clearTimeout(sy); sy = setTimeout(function () { history.replaceState(Object.assign({}, history.state, { y: scrollY }), ''); }, 200); }, { passive: true });

  /* ── 시계: 현실과 벨라트(4배속) ── */
  var DAYS = ['일', '월', '화', '수', '목', '금', '토'], clocks = [], scrolling = 0;
  addEventListener('scroll', function () { clearTimeout(scrolling); scrolling = setTimeout(function () { scrolling = 0; }, 160); }, { passive: true });
  function tick() {
    var now = new Date();
    var sec = now.getHours() * 3600 + now.getMinutes() * 60 + now.getSeconds() + now.getMilliseconds() / 1000;
    var b = (sec * 4) % 86400;
    var rh = pad(now.getHours()), rm = pad(now.getMinutes()), rs = pad(now.getSeconds());
    var bh = pad(Math.floor(b / 3600)), bm = pad(Math.floor(b % 3600 / 60)), bs = pad(Math.floor(b % 60));
    var map = {
      'real': rh + ':' + rm, 'belat': bh + ':' + bm,
      'real-s': rh + ':' + rm + ':' + rs, 'belat-s': bh + ':' + bm + ':' + bs,
      'date': '2047.' + pad(now.getMonth() + 1) + '.' + pad(now.getDate()),
      'date-long': '2047년 ' + (now.getMonth() + 1) + '월 ' + now.getDate() + '일 ' + DAYS[now.getDay()] + '요일'
    };
    clocks.forEach(function (e) { var v = map[e.dataset.clock]; if (v && e.textContent !== v) e.textContent = v; });
  }
  var clockT = 0;
  function startClock() {
    clocks = $$('[data-clock]'); tick();
    clearInterval(clockT); clockT = setInterval(function () { if (!scrolling && !d.hidden) tick(); }, $('[data-clock="belat-s"]') ? 250 : 1000);
  }

  /* ── 글자 해독 ── */
  var GLYPH = '▓▒░#%&@$01アイウ';
  function scramble(el) {
    var text = el.dataset.final || el.textContent; el.dataset.final = text;
    if (reduce) { el.textContent = text; return; }
    var f = 0, total = 18, mine = P;
    (function step() {
      if (mine.dead) return;
      var out = '';
      for (var k = 0; k < text.length; k++) out += (f / total) * text.length > k || text[k] === ' ' ? text[k] : GLYPH[(Math.random() * GLYPH.length) | 0];
      el.textContent = out;
      if (++f <= total) later(step, 32); else el.textContent = text;
    })();
  }

  /* ═════════ 페이지마다 ═════════ */
  function page() {
    scope();
    var mine = P;
    startClock();
    sfx.paint(); bgm.hud();

    /* 상단 HUD: 조금 내리면 판을 깐다 */
    var sentinel = d.createElement('div');
    sentinel.style.cssText = 'position:absolute;top:0;left:0;height:90px;width:1px;pointer-events:none';
    d.body.prepend(sentinel);
    if ('IntersectionObserver' in window) { var hio = new IntersectionObserver(function (es) { root.classList.toggle('scrolled', !es[0].isIntersecting); }); hio.observe(sentinel); P.io.push(hio); }

    /* ESC 메뉴 */
    var menu = $('.menu'), escBtn = $('.esc');
    if (menu) {
      if (escBtn) escBtn.addEventListener('click', function () { openMenu(menu.hidden); });
      $('.menu-x', menu).addEventListener('click', function () { openMenu(false); });
      $$('ol a', menu).forEach(function (a) { a.addEventListener('mouseenter', function () { setBg(a); }); a.addEventListener('focus', function () { setBg(a); }); a.addEventListener('click', function () { if (!menu.hidden) { menu.hidden = true; menu.classList.remove('open'); d.body.style.overflow = ''; } }); });
    }
    function menuOpen() { return menu && !menu.hidden; }

    /* 등장 */
    var rv = $$('[data-rv]');
    if ('IntersectionObserver' in window && !reduce && !touch) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
      }, { rootMargin: '0px 0px -6% 0px', threshold: 0 });
      rv.forEach(function (el) { io.observe(el); }); P.io.push(io);
    } else rv.forEach(function (el) { el.classList.add('in'); });

    /* 홈: 월드 채팅 판 */
    var chat = $('.chat-b');
    if (chat) {
      var lines = $$('li', chat);
      var rotate = function () {
        if (d.hidden || scrolling) return;
        for (var n = 0; n < lines.length; n++) {
          var li = chat.firstElementChild; li.classList.remove('new'); chat.appendChild(li);
          if (!li.hidden) { void li.offsetWidth; li.classList.add('new'); return; }
        }
      };
      $$('.chat-h button').forEach(function (b) {
        b.addEventListener('click', function () {
          $$('.chat-h button').forEach(function (x) { x.setAttribute('aria-selected', x === b); });
          var f = b.dataset.ch;
          lines.forEach(function (li) { li.hidden = f !== 'all' && li.dataset.ch !== f; li.classList.remove('new'); });
        });
      });
      if (!reduce) { var chatOn = false; whileVisible(chat, function () { chatOn = true; }, function () { chatOn = false; }, 0); every(function () { if (chatOn) rotate(); }, 2200); }
    }

    /* 홈: 히든직 알림 */
    var jobsBox = $('[data-jobs]');
    if (jobsBox) {
      var jobs = $$('.job', jobsBox), dots = $$('.dots i', jobsBox), pager = $('[data-pager]', jobsBox), ji = 0, jt = 0;
      var showJob = function (n) {
        ji = (n + jobs.length) % jobs.length;
        jobs.forEach(function (j, k) { j.hidden = k !== ji; });
        dots.forEach(function (x, k) { x.classList.toggle('on', k === ji); });
        pager.textContent = (ji + 1) + ' / ' + jobs.length;
        scramble($('.job-n', jobs[ji]));
      };
      var auto = function () { clearInterval(jt); if (!reduce) jt = setInterval(function () { showJob(ji + 1); }, 4800); };
      P.fin.push(function () { clearInterval(jt); });
      $('[data-next]', jobsBox).addEventListener('click', function () { showJob(ji + 1); auto(); sfx.play('reveal'); });
      var revealed = false;
      whileVisible(jobsBox, function () { showJob(ji); auto(); if (!revealed) { revealed = true; sfx.play('reveal'); } }, function () { clearInterval(jt); }, .3);
    }

    /* 표지: 눌러서 시작 → 로딩(소리) → 접속. 로딩 중에 누르면 건너뛴다 */
    var cover = $('[data-cover]');
    if (cover) {
      sfx.load('loading'); sfx.load('enter');
      var bar = $('.cv-bar i', cover), pct = $('[data-pct]', cover), p2 = $('[data-pct2]', cover), logs = $$('.cv-log li', cover), link = $('[data-enter]', cover);
      var t0 = 0, dur = reduce ? 1 : 2400, state = 'idle';
      cover.classList.add('idle');
      var setP = function (e) {
        bar.style.setProperty('--p', e); pct.textContent = Math.round(e * 100); if (p2) p2.textContent = Math.round(e * 100);
        logs.forEach(function (li, k) { if (e > (k + .6) / logs.length) li.classList.add('on'); });
      };
      var load = function (t) {
        if (state !== 'loading' || mine.dead) return;
        var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 2.2);
        setP(e);
        if (p < 1) requestAnimationFrame(load); else { state = 'ready'; cover.classList.add('ready'); later(enter, reduce ? 0 : 420); }
      };
      var enter = function () {
        if (state === 'go') return;
        state = 'go'; sfx.stop('loading'); setP(1); cover.classList.add('ready');
        if (reduce) { go(link.href); return; }
        cover.classList.add('go'); sfx.play('enter');
        later(function () { go(link.href); }, 1150);
      };
      var press = function (e) {
        if (e) e.preventDefault();
        if (state === 'idle') {
          state = 'loading'; cover.classList.remove('idle');
          t0 = performance.now(); sfx.play('loading', 0); bgm.fresh(); requestAnimationFrame(load);
        } else if (state === 'loading') enter();
      };
      cover.addEventListener('click', press);
      on(d, 'keydown', function (e) { if (!e.metaKey && !e.ctrlKey && !e.altKey && e.key !== 'Tab') press(e); });
    }

    /* 인물: 캐릭터 선택 */
    var sel = $('[data-select]');
    if (sel) {
      var sImg = $('[data-sel-img]', sel), info = $('.sel-info', sel), cur = $('.ro.on', sel);
      var F = {}; $$('[data-f-name],[data-f-real],[data-f-hook],[data-f-lv],[data-f-job],[data-f-grade],[data-f-gradebox],[data-f-link],[data-f-side],[data-f-role]', sel)
        .forEach(function (el) { Object.keys(el.dataset).forEach(function (k) { if (k.indexOf('f') === 0) F[k] = el; }); });
      var pick = function (a) {
        if (!a || a === cur) return;
        var c = JSON.parse(a.dataset.c);
        if (cur) cur.classList.remove('on'); a.classList.add('on'); cur = a;
        sfx.play('select', 90);
        F.fName.textContent = c.name; F.fHook.textContent = c.hook; F.fLv.textContent = c.lv; F.fJob.textContent = c.job;
        F.fRole.textContent = c.role; F.fLink.href = a.getAttribute('href');
        F.fSide.textContent = c.side === 'player' ? '이방인' : '원주민'; F.fSide.classList.toggle('npc', c.side !== 'player');
        F.fReal.hidden = !c.real; F.fReal.textContent = '현실 · ' + c.real;
        F.fGradebox.hidden = !c.grade; F.fGrade.innerHTML = c.grade ? '<span class="grade ' + c.gk + '">' + c.grade + '</span>' : '';
        info.classList.remove('swap'); void info.offsetWidth; info.classList.add('swap');
        sImg.classList.add('out');
        var im = new Image();
        im.onload = im.onerror = function () { if (cur !== a) return; sImg.src = c.img; sImg.classList.remove('out'); };
        im.src = c.img;
      };
      $$('.ro', sel).forEach(function (a) {
        a.addEventListener('mouseenter', function () { pick(a); });
        a.addEventListener('focus', function () { pick(a); });
      });
      $$('.sel-f button', sel).forEach(function (b) {
        b.addEventListener('click', function () {
          $$('.sel-f button', sel).forEach(function (x) { x.setAttribute('aria-selected', x === b); });
          var f = b.dataset.f;
          $$('.roster > li', sel).forEach(function (li) { li.hidden = f !== 'all' && li.dataset.side !== f; });
          var first = $('.roster > li:not([hidden]) .ro', sel); if (first) pick(first);
        });
      });
      sel.addEventListener('keydown', function (e) {
        if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
        var list = $$('.roster > li:not([hidden]) .ro', sel), i = list.indexOf(d.activeElement);
        if (i < 0) i = list.indexOf(cur);
        var n = list[(i + (e.key === 'ArrowDown' ? 1 : list.length - 1)) % list.length];
        if (n) { n.focus(); e.preventDefault(); }
      });
    }

    /* 인물 상세: 표정 */
    var fig = $('.stage .fig');
    if (fig) {
      var stg = fig.parentElement;
      var setFig = function (src, alt) {
        stg.style.setProperty('--bgsrc', 'url("' + new URL(src, location.href).href + '")');
        if (fig.getAttribute('src') === src) return;
        fig.classList.add('fade');
        var im = new Image();
        im.onload = im.onerror = function () { later(function () { fig.src = src; fig.alt = alt; fig.classList.remove('fade'); }, 80); };
        im.src = src;
      };
      stg.style.setProperty('--bgsrc', 'url("' + fig.src + '")');
      $$('.thumbs button').forEach(function (b) {
        b.addEventListener('click', function () {
          $$('button', b.parentNode).forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
          setFig(b.dataset.src, b.dataset.alt); sfx.play('flip');
          b.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: reduce ? 'auto' : 'smooth' });
        });
      });
      $$('.sw button').forEach(function (b) {
        b.addEventListener('click', function () {
          $$('.sw button').forEach(function (x) { x.setAttribute('aria-selected', x === b); });
          $$('.thumbs').forEach(function (t) { t.hidden = t.dataset.axis !== b.dataset.axis; });
          var p = $('.thumbs[data-axis="' + b.dataset.axis + '"] button[aria-pressed="true"]'); if (p) p.click();
        });
      });
      on(d, 'keydown', function (e) {
        if (typing() || e.metaKey || e.ctrlKey || e.altKey || menuOpen()) return;
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
          var bs = $$('.thumbs:not([hidden]) button'), i = bs.findIndex(function (x) { return x.getAttribute('aria-pressed') === 'true'; });
          var n = bs[(i + (e.key === 'ArrowRight' ? 1 : bs.length - 1)) % bs.length]; if (n) { n.click(); e.preventDefault(); }
        }
        if (e.key === 'q' || e.key === 'Q') { var p = $('[data-prev]'); if (p) go(p.href); }
        if (e.key === 'e' || e.key === 'E') { var x = $('.prof-nav [data-next]'); if (x) go(x.href); }
      });
    }

    /* 대륙: 지역 이동 */
    var tv = $('[data-travel]');
    if (tv) {
      var tb = $$('.tv-list button', tv), tbg = $$('.tv-bg', tv), tinf = $$('.tv-info', tv);
      var go2 = function (key, push) {
        tb.forEach(function (b) { if (b.dataset.r === key) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current'); });
        tbg.forEach(function (b) {
          var cur_ = b.dataset.r === key; b.classList.toggle('on', cur_);
          if (cur_) { var im = $('img', b); if (im.loading === 'lazy') im.loading = 'eager'; }
        });
        tinf.forEach(function (x) { x.hidden = x.dataset.r !== key; });
        var cb = tb.filter(function (b) { return b.dataset.r === key; })[0];
        var sc = cb && cb.closest('.tv-list');
        if (sc && sc.scrollWidth > sc.clientWidth) sc.scrollTo({ left: cb.parentNode.offsetLeft - (sc.clientWidth - cb.parentNode.offsetWidth) / 2, behavior: reduce ? 'auto' : 'smooth' });
        if (push) { replaceHash(key); sfx.play('travel', 120); }
      };
      tb.forEach(function (b) { b.addEventListener('click', function () { go2(b.dataset.r, true); }); });
      var inView = false;
      whileVisible(tv, function () { inView = true; }, function () { inView = false; }, .5);
      on(d, 'keydown', function (e) {
        if (!inView || typing() || menuOpen() || (e.key !== 'ArrowDown' && e.key !== 'ArrowUp')) return;
        var i = tb.findIndex(function (b) { return b.hasAttribute('aria-current'); });
        var n = tb[(i + (e.key === 'ArrowDown' ? 1 : tb.length - 1)) % tb.length]; go2(n.dataset.r, true); e.preventDefault();
      });
      var h = location.hash.slice(1);
      if (h && tb.some(function (b) { return b.dataset.r === h; })) go2(h, false);
    }

    /* 시작: 슬롯 */
    var slotBtns = $$('.ng .slot');
    if (slotBtns.length) {
      var panes = $$('.replay');
      var mode = function (key, push) {
        slotBtns.forEach(function (b) { b.setAttribute('aria-selected', b.dataset.m === key); });
        panes.forEach(function (p) { p.hidden = p.dataset.m !== key; });
        if (push) { replaceHash(key); sfx.play('select'); }
      };
      slotBtns.forEach(function (b) { b.addEventListener('click', function () {
        mode(b.dataset.m, true);
        /* 좁은 화면에서는 슬롯 아래로 열린 첫 장면까지 내려 준다 */
        if (innerWidth <= 900) { var pane = $('.replay[data-m="' + b.dataset.m + '"]'); if (pane) pane.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' }); }
      }); });
      var mh = location.hash.slice(1);
      if (mh && panes.some(function (p) { return p.dataset.m === mh; })) mode(mh, false);
    }

    /* 음악 페이지: 엔진(bgm)에 붙는 큰 플레이어 */
    var mu = $('[data-music]');
    if (mu) {
      var T = bgm.list, a = bgm.audio, buf = null, raf = 0, seeking = false;
      var art = $('[data-mu-art]'), bgI = $('[data-mu-bg]'), seek = $('[data-mu-seek]'), vol = $('[data-mu-vol]'), rep = $('[data-mu-rep]');
      var cv = $('.mu-vis'), cx = cv.getContext('2d'), mini = $('[data-mu-mini]'), mbar = $('[data-mu-mbar]'), btns = $$('[data-mu-id]'), inViewStage = true;
      var el = { no: $('[data-mu-no]'), g: $('[data-mu-g]'), name: $('[data-mu-name]'), en: $('[data-mu-en]'), mname: $('[data-mu-mname]'), men: $('[data-mu-men]'), mimg: $('[data-mu-mimg]'), cur: $('[data-mu-cur]'), dur: $('[data-mu-dur]') };
      var fmt = function (n) { n = Math.max(0, Math.floor(n || 0)); return Math.floor(n / 60) + ':' + pad(n % 60); };
      var fill = function (r) { r.style.setProperty('--p', ((r.value - r.min) / (r.max - r.min) * 100) + '%'); };
      var setSrc = function (img, src) { if (img.getAttribute('src') !== src) img.src = src; };
      var tick2 = function () {
        if (seeking || mine.dead) return;
        var dd = a.duration || T[bgm.idx].d, r = Math.min(1, (a.currentTime || bgm.t0 || 0) / dd);
        seek.value = Math.round(r * 1000); fill(seek);
        el.cur.textContent = fmt(a.currentTime || bgm.t0); el.dur.textContent = fmt(dd);
        mbar.style.transform = 'scaleX(' + r + ')';
      };
      var draw = function () {
        raf = 0;
        var an = bgm.analyser();
        if (mine.dead || !an || !bgm.playing() || d.hidden) { cx.clearRect(0, 0, cv.width, cv.height); return; }
        var w = cv.clientWidth, hh = cv.clientHeight, dpr = Math.min(2, devicePixelRatio || 1);
        if (cv.width !== Math.round(w * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(hh * dpr); }
        if (!buf) buf = new Uint8Array(an.frequencyBinCount);
        an.getByteFrequencyData(buf);
        var n = 48, gap = 3 * dpr, bw = (cv.width - gap * (n - 1)) / n;
        cx.clearRect(0, 0, cv.width, cv.height);
        var g = cx.createLinearGradient(0, cv.height, 0, 0); g.addColorStop(0, 'rgba(92,229,255,.75)'); g.addColorStop(1, 'rgba(58,123,255,0)');
        cx.fillStyle = g;
        for (var k = 0; k < n; k++) { var v = buf[Math.floor(k / n * buf.length * .8)] / 255, bh = Math.max(2 * dpr, v * v * cv.height); cx.fillRect(k * (bw + gap), cv.height - bh, bw, bh); }
        raf = requestAnimationFrame(draw);
      };
      var kick = function () { if (!raf && bgm.playing()) raf = requestAnimationFrame(draw); };
      var render = function () {
        if (mine.dead) return;
        var x = T[bgm.idx], base = SITE + 'images/bgm/', playing = bgm.playing();
        mu.classList.toggle('mu-on', playing);
        if (!inViewStage) mini.hidden = false;
        btns.forEach(function (b) { if (b.dataset.muId === x.id) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current'); });
        el.no.textContent = pad(bgm.idx + 1); el.g.textContent = x.g; el.name.textContent = x.n; el.en.textContent = x.t;
        el.mname.textContent = x.n; el.men.textContent = x.t; setSrc(el.mimg, base + 's/' + x.id + '.webp'); setSrc(bgI, base + 's/' + x.id + '.webp');
        if (art.getAttribute('src') !== base + x.id + '.webp' && art.dataset.want !== x.id) {
          art.dataset.want = x.id; art.classList.add('out');
          var im = new Image(); im.onload = im.onerror = function () { if (mine.dead || T[bgm.idx].id !== x.id) return; art.src = im.src; art.alt = x.n; art.classList.remove('out'); };
          im.src = base + x.id + '.webp';
        }
        rep.setAttribute('aria-pressed', bgm.rep);
        if (location.hash.slice(1) !== x.id) replaceHash(x.id);
        tick2(); kick();
      };
      P.fin.push(bgm.onChange(render));
      P.fin.push(function () { cancelAnimationFrame(raf); raf = 0; });
      a.addEventListener('timeupdate', tick2); P.fin.push(function () { a.removeEventListener('timeupdate', tick2); });
      /* 소리 막대: 누른 순간 오디오 그래프를 만든다 */
      on(window, 'pointerdown', function () { later(kick, 0); }, { capture: true, passive: true });
      on(window, 'keydown', function () { later(kick, 0); }, { capture: true, passive: true });
      seek.addEventListener('input', function () { seeking = true; fill(seek); el.cur.textContent = fmt(seek.value / 1000 * (a.duration || T[bgm.idx].d)); });
      seek.addEventListener('change', function () { seeking = false; bgm.seek(seek.value / 1000); });
      vol.value = Math.round(bgm.vol * 100); fill(vol);
      vol.addEventListener('input', function () { fill(vol); bgm.setVol(vol.value / 100); });
      rep.addEventListener('click', function () { bgm.setRep(!bgm.rep); });
      $$('[data-mu-pp]').forEach(function (b) { b.addEventListener('click', function () { bgm.toggle(); }); });
      $$('[data-mu-next]').forEach(function (b) { b.addEventListener('click', function () { bgm.go(bgm.idx + 1); }); });
      $('[data-mu-prev]').addEventListener('click', function () { if (a.currentTime > 3) bgm.seek(0); else bgm.go(bgm.idx - 1); });
      btns.forEach(function (b) { b.addEventListener('click', function (e) {
        if (e.detail) b.blur();
        var i = T.findIndex(function (x) { return x.id === b.dataset.muId; });
        if (i === bgm.idx) bgm.toggle(); else bgm.go(i, true);
      }); });
      on(d, 'keydown', function (e) {
        if (typing() || e.metaKey || e.ctrlKey || e.altKey || menuOpen()) return;
        if (e.key === ' ' && !/BUTTON|A|INPUT/.test(d.activeElement.tagName)) { bgm.toggle(); e.preventDefault(); }
        if (e.key === 'ArrowRight' && d.activeElement.type !== 'range') { bgm.go(bgm.idx + 1); e.preventDefault(); }
        if (e.key === 'ArrowLeft' && d.activeElement.type !== 'range') { bgm.go(bgm.idx - 1); e.preventDefault(); }
      });
      whileVisible($('.mu-ctl'), function () { inViewStage = true; mini.hidden = true; }, function () { inViewStage = false; mini.hidden = false; }, .01);
      /* 주소에 곡이 있으면 그 곡으로 */
      var hi = T.findIndex(function (x) { return x.id === location.hash.slice(1); });
      if (hi >= 0 && hi !== bgm.idx) bgm.go(hi, bgm.playing());
      render();
    }
  }

  page();
})();
