/* FULL DIVE - ILEON · 게임 클라이언트 동작 */
(function () {
  var d = document, root = d.documentElement;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s, r) { return (r || d).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function typing() { var a = d.activeElement; return a && /INPUT|TEXTAREA|SELECT/.test(a.tagName); }

  /* 화면에 들어와 있는 동안만 콜백을 켠다 */
  function whileVisible(el, on, off, th) {
    if (!el) return;
    if (!('IntersectionObserver' in window)) { on(); return; }
    new IntersectionObserver(function (es) { es[0].isIntersecting ? on() : off && off(); }, { threshold: th || .4 }).observe(el);
  }

  /* ── 효과음: ElevenLabs로 만든 짧은 UI 소리. 첫 조작 뒤에만 울리고, 끄면 기억한다 ── */
  var sfx = (function () {
    var base = (d.currentScript && d.currentScript.src || '').replace(/js\/main\.js.*$/, 'sfx/');
    var VOL = { loading: .5, enter: .7, hover: .14, click: .4, menu: .45, chat: .35, select: .24, travel: .4, flip: .32, reveal: .45 };
    var AC = window.AudioContext || window.webkitAudioContext, ctx, out, raw = {}, buf = {}, last = {}, live = {};
    var on = true; try { on = localStorage.getItem('ileon-sfx') !== 'off'; } catch (e) {}
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
      if (ctx.state === 'suspended') return ctx.resume();
    }
    ['pointerdown', 'keydown', 'touchstart'].forEach(function (t) { addEventListener(t, wake, { capture: true, passive: true }); });
    function play(n, gap, from) {
      if (!on || !ctx || d.hidden) return;
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
      l.g.gain.setTargetAtTime(0, ctx.currentTime, .04); l.s.stop(ctx.currentTime + .2);
    }
    function set(v) {
      on = v; try { localStorage.setItem('ileon-sfx', v ? 'on' : 'off'); } catch (e) {}
      $$('.snd').forEach(function (b) { b.setAttribute('aria-pressed', v); $('b', b).textContent = v ? 'ON' : 'OFF'; });
      if (v) { wake(); play('click'); }
    }
    $$('.snd').forEach(function (b) {
      b.setAttribute('aria-pressed', on); $('b', b).textContent = on ? 'ON' : 'OFF';
      b.addEventListener('click', function (e) { e.stopPropagation(); e.preventDefault(); set(!on); });
    });
    /* 표지에서는 첫 소리를 바로 낼 수 있게 미리 받아 둔다 */
    if ($('[data-cover]')) { load('loading'); load('enter'); }
    /* 마우스로 훑을 때만 짧은 틱. 손가락 조작에는 붙이지 않는다 */
    if (fine) d.addEventListener('mouseover', function (e) {
      var t = e.target.closest && e.target.closest('.tabs a, .menu ol a, .tmenu a, .rg, .sl, .ng .slot, .tv-list button, .btn, .cw-btn, .esc, .snd');
      if (t && !t.contains(e.relatedTarget)) play('hover', 70);
    });
    /* 버튼과 링크는 누를 때 확인음. 따로 소리를 정한 곳은 건너뛴다 */
    d.addEventListener('click', function (e) {
      var t = e.target.closest && e.target.closest('a[href], button');
      if (!t || t.closest('.snd, .cw-btn, .esc, .menu-x, [data-cover], .tv-list, .ng .slot, .thumbs, [data-jobs] [data-next], .cw-f')) return;
      play('click');
    });
    return { play: play, stop: stop, toggle: function () { set(!on); } };
  })();

  /* ── 시계: 현실과 벨라트(4배속) ── */
  var DAYS = ['일', '월', '화', '수', '목', '금', '토'];
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
  var clocks = $$('[data-clock]'), scrolling = 0;
  addEventListener('scroll', function () { clearTimeout(scrolling); scrolling = setTimeout(function () { scrolling = 0; }, 160); }, { passive: true });
  tick(); setInterval(function () { if (!scrolling) tick(); }, $('[data-clock="belat-s"]') ? 250 : 1000);


  /* ── 채팅창: 오른쪽 아래 버튼으로 열고 닫는다 ── */
  var cw = $('#cw'), cwBtn = $('.cw-btn');
  function openChat(o) {
    if (!cw) return;
    cw.hidden = !o; cwBtn.setAttribute('aria-expanded', o); cwBtn.classList.toggle('on', o);
    root.classList.toggle('cw-open', o);
    sfx.play(o ? 'chat' : 'click');
    if (o) { unread = 0; badge(); cwList.scrollTop = cwList.scrollHeight; if (!touchDev) $('#cw-in').focus(); }
    else cwBtn.focus({ preventScroll: true });
  }
  if (cw) {
    var cwList = $('.cw-b', cw), src = $$('li', $('#cw-src').content), si = 0, unread = 0, filter = 'all';
    var touchDev = matchMedia('(hover: none)').matches;
    var nBadge = $('.cw-n', cwBtn);
    function badge() { nBadge.hidden = !unread; nBadge.textContent = unread > 9 ? '9+' : unread; }
    function push(li, quiet) {
      li = li.cloneNode(true);
      li.hidden = filter !== 'all' && li.dataset.ch !== filter;
      var stick = cwList.scrollHeight - cwList.scrollTop - cwList.clientHeight < 40;
      cwList.appendChild(li);
      if (!quiet) li.classList.add('new');
      while (cwList.children.length > 80) cwList.removeChild(cwList.firstElementChild);
      if (stick) cwList.scrollTop = cwList.scrollHeight;
    }
    function next(quiet) { push(src[si % src.length], quiet); si++; }
    for (var k = 0; k < 8; k++) next(true);
    setInterval(function () {
      if (d.hidden) return;
      next(false);
      if (cw.hidden) { unread++; badge(); }
    }, 3400);
    cwBtn.addEventListener('click', function () { openChat(cw.hidden); });
    $('.cw-x', cw).addEventListener('click', function () { openChat(false); });
    $$('.cw-tabs button', cw).forEach(function (b) {
      b.addEventListener('click', function () {
        $$('.cw-tabs button', cw).forEach(function (x) { x.setAttribute('aria-selected', x === b); });
        filter = b.dataset.ch;
        $$('li', cwList).forEach(function (li) { li.hidden = filter !== 'all' && li.dataset.ch !== filter; });
        cwList.scrollTop = cwList.scrollHeight;
      });
    });
    $('.cw-f', cw).addEventListener('submit', function (e) {
      e.preventDefault();
      var inp = $('#cw-in'), t = inp.value.trim(); if (!t) return;
      var li = d.createElement('li'); li.className = 'c-me'; li.dataset.ch = 'etc';
      var ch = d.createElement('span'); ch.className = 'ch'; ch.textContent = '[일반]';
      var who = d.createElement('b'); who.textContent = '당신';
      var msg = d.createElement('span'); msg.className = 'msg'; msg.textContent = t;
      li.append(ch, ' ', who, ' ', msg);
      cwList.scrollTop = cwList.scrollHeight; push(li, false); cwList.scrollTop = cwList.scrollHeight;
      inp.value = ''; sfx.play('chat');
    });
    cw.addEventListener('keydown', function (e) { if (e.key === 'Escape') { openChat(false); e.stopPropagation(); } });
  }

  /* ── 상단 HUD ── */
  var sentinel = d.createElement('div');
  sentinel.style.cssText = 'position:absolute;top:0;left:0;height:90px;width:1px;pointer-events:none';
  d.body.prepend(sentinel);
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { root.classList.toggle('scrolled', !es[0].isIntersecting); }).observe(sentinel);

  /* ── ESC 메뉴, 숫자 키 이동 ── */
  var menu = $('.menu'), escBtn = $('.esc'), menuBg = $('.menu-bg');
  function openMenu(o) {
    if (!menu) return;
    if (menu.hidden === !o) return;
    menu.hidden = !o; menu.classList.toggle('open', o);
    sfx.play(o ? 'menu' : 'click');
    if (escBtn) escBtn.setAttribute('aria-expanded', o);
    d.body.style.overflow = o ? 'hidden' : '';
    if (o) { var c = $('ol a[aria-current]', menu) || $('ol a', menu); if (c) { c.focus(); setBg(c); } }
    else if (escBtn) escBtn.focus();
  }
  function setBg(a) { if (menuBg && a.dataset.bg) menuBg.style.backgroundImage = 'url("' + a.dataset.bg + '")'; }
  if (menu) {
    escBtn && escBtn.addEventListener('click', function () { openMenu(menu.hidden); });
    $('.menu-x', menu).addEventListener('click', function () { openMenu(false); });
    $$('ol a', menu).forEach(function (a) { a.addEventListener('mouseenter', function () { setBg(a); }); a.addEventListener('focus', function () { setBg(a); }); });
    var navLinks = $$('.tabs a');
    d.addEventListener('keydown', function (e) {
      if (typing() || e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === 'Escape' && cw && !cw.hidden) { openChat(false); e.preventDefault(); return; }
      if (e.key === 'Escape') { openMenu(menu.hidden); e.preventDefault(); return; }
      if (e.key === 'Enter' && cw && cw.hidden && menu.hidden && !/A|BUTTON/.test(d.activeElement.tagName) && !$('[data-cover]')) { openChat(true); e.preventDefault(); return; }
      if (/^[1-5]$/.test(e.key) && navLinks[+e.key - 1]) { sfx.play('click'); location.href = navLinks[+e.key - 1].href; }
      if (e.key === 'm' || e.key === 'M') sfx.toggle();
    });
  }

  /* ── 등장 ── */
  var rv = $$('[data-rv]');
  var touch = matchMedia('(hover: none), (max-width: 900px)').matches;
  if (touch) root.classList.add('touch');
  if ('IntersectionObserver' in window && !reduce && !touch) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0 });
    rv.forEach(function (el) { io.observe(el); });
  } else rv.forEach(function (el) { el.classList.add('in'); });

  /* ── 글자 해독 ── */
  var GLYPH = '▓▒░#%&@$01アイウ';
  function scramble(el) {
    var text = el.dataset.final || el.textContent; el.dataset.final = text;
    if (reduce) { el.textContent = text; return; }
    var f = 0, total = 18;
    (function step() {
      var out = '';
      for (var k = 0; k < text.length; k++) out += (f / total) * text.length > k || text[k] === ' ' ? text[k] : GLYPH[(Math.random() * GLYPH.length) | 0];
      el.textContent = out;
      if (++f <= total) setTimeout(step, 32); else el.textContent = text;
    })();
  }

  /* ── 홈: 월드 채팅 ── */
  var chat = $('.chat-b');
  if (chat) {
    var lines = $$('li', chat);
    function rotate() {
      for (var n = 0; n < lines.length; n++) {
        var li = chat.firstElementChild; li.classList.remove('new'); chat.appendChild(li);
        if (!li.hidden) { void li.offsetWidth; li.classList.add('new'); return; }
      }
    }
    $$('.chat-h button').forEach(function (b) {
      b.addEventListener('click', function () {
        $$('.chat-h button').forEach(function (x) { x.setAttribute('aria-selected', x === b); });
        var f = b.dataset.ch;
        lines.forEach(function (li) { li.hidden = f !== 'all' && li.dataset.ch !== f; li.classList.remove('new'); });
      });
    });
    if (!reduce) setInterval(rotate, 2200);
  }

  /* ── 홈: 히든직 알림 ── */
  var jobsBox = $('[data-jobs]');
  if (jobsBox) {
    var jobs = $$('.job', jobsBox), dots = $$('.dots i', jobsBox), pager = $('[data-pager]', jobsBox), ji = 0, jt = 0;
    function showJob(n) {
      ji = (n + jobs.length) % jobs.length;
      jobs.forEach(function (j, k) { j.hidden = k !== ji; });
      dots.forEach(function (x, k) { x.classList.toggle('on', k === ji); });
      pager.textContent = (ji + 1) + ' / ' + jobs.length;
      scramble($('.job-n', jobs[ji]));
    }
    function auto() { clearInterval(jt); if (!reduce) jt = setInterval(function () { showJob(ji + 1); }, 4800); }
    $('[data-next]', jobsBox).addEventListener('click', function () { showJob(ji + 1); auto(); sfx.play('reveal'); });
    var revealed = false;
    whileVisible(jobsBox, function () { showJob(ji); auto(); if (!revealed) { revealed = true; sfx.play('reveal'); } }, function () { clearInterval(jt); }, .3);
  }

  /* ── 표지: 눌러서 시작 → 로딩(소리) → 접속. 로딩 중에 누르면 건너뛴다 ── */
  var cover = $('[data-cover]');
  if (cover) {
    var bar = $('.cv-bar i', cover), pct = $('[data-pct]', cover), p2 = $('[data-pct2]', cover), logs = $$('.cv-log li', cover), go = $('[data-enter]', cover);
    var t0 = 0, dur = reduce ? 1 : 2400, state = 'idle';
    cover.classList.add('idle');
    function setP(e) {
      bar.style.setProperty('--p', e); pct.textContent = Math.round(e * 100); if (p2) p2.textContent = Math.round(e * 100);
      logs.forEach(function (li, k) { if (e > (k + .6) / logs.length) li.classList.add('on'); });
    }
    function load(t) {
      if (state !== 'loading') return;
      var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 2.2);
      setP(e);
      if (p < 1) requestAnimationFrame(load); else { state = 'ready'; cover.classList.add('ready'); setTimeout(enter, reduce ? 0 : 420); }
    }
    function enter() {
      if (state === 'go') return;
      state = 'go'; sfx.stop('loading'); setP(1); cover.classList.add('ready');
      if (reduce) { location.href = go.href; return; }
      cover.classList.add('go'); sfx.play('enter');
      setTimeout(function () { location.href = go.href; }, 1150);
    }
    function press(e) {
      if (e) e.preventDefault();
      if (state === 'idle') {
        state = 'loading'; cover.classList.remove('idle');
        t0 = performance.now(); sfx.play('loading', 0); requestAnimationFrame(load);
      } else if (state === 'loading') enter();
    }
    cover.addEventListener('click', press);
    d.addEventListener('keydown', function (e) { if (!e.metaKey && !e.ctrlKey && !e.altKey && e.key !== 'Tab') press(e); });
  }

  /* ── 인물: 캐릭터 선택 ── */
  var sel = $('[data-select]');
  if (sel) {
    var sImg = $('[data-sel-img]', sel), info = $('.sel-info', sel), cur = $('.ro.on', sel);
    var F = {}; $$('[data-f-name],[data-f-real],[data-f-hook],[data-f-lv],[data-f-job],[data-f-grade],[data-f-gradebox],[data-f-link],[data-f-side],[data-f-role]', sel)
      .forEach(function (el) { Object.keys(el.dataset).forEach(function (k) { if (k.indexOf('f') === 0) F[k] = el; }); });
    function pick(a) {
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
    }
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

  /* ── 인물 상세: 표정 ── */
  var fig = $('.stage .fig');
  if (fig) {
    var stg = fig.parentElement;
    function setFig(src, alt) {
      stg.style.setProperty('--bgsrc', 'url("' + src + '")');
      if (fig.getAttribute('src') === src) return;
      fig.classList.add('fade');
      var im = new Image();
      im.onload = im.onerror = function () { setTimeout(function () { fig.src = src; fig.alt = alt; fig.classList.remove('fade'); }, 80); };
      im.src = src;
    }
    stg.style.setProperty('--bgsrc', 'url("' + fig.getAttribute('src') + '")');
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
        var on = $('.thumbs[data-axis="' + b.dataset.axis + '"] button[aria-pressed="true"]'); if (on) on.click();
      });
    });
    d.addEventListener('keydown', function (e) {
      if (typing() || e.metaKey || e.ctrlKey || e.altKey || (menu && !menu.hidden)) return;
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        var bs = $$('.thumbs:not([hidden]) button'), i = bs.findIndex(function (x) { return x.getAttribute('aria-pressed') === 'true'; });
        var n = bs[(i + (e.key === 'ArrowRight' ? 1 : bs.length - 1)) % bs.length]; if (n) { n.click(); e.preventDefault(); }
      }
      if (e.key === 'q' || e.key === 'Q') { var p = $('[data-prev]'); if (p) location.href = p.href; }
      if (e.key === 'e' || e.key === 'E') { var x = $('.prof-nav [data-next]'); if (x) location.href = x.href; }
    });
  }

  /* ── 대륙: 지역 이동 ── */
  var tv = $('[data-travel]');
  if (tv) {
    var tb = $$('.tv-list button', tv), tbg = $$('.tv-bg', tv), tinf = $$('.tv-info', tv);
    function go2(key, push) {
      tb.forEach(function (b) { b.toggleAttribute('aria-current', b.dataset.r === key); if (b.dataset.r === key) b.setAttribute('aria-current', 'true'); });
      tbg.forEach(function (b) {
        var on = b.dataset.r === key; b.classList.toggle('on', on);
        if (on) { var im = $('img', b); if (im.loading === 'lazy') im.loading = 'eager'; }
      });
      tinf.forEach(function (x) { x.hidden = x.dataset.r !== key; });
      var cb = tb.filter(function (b) { return b.dataset.r === key; })[0];
      if (cb && cb.parentNode.parentNode.scrollWidth > cb.parentNode.parentNode.clientWidth) cb.scrollIntoView({ block: 'nearest', inline: 'center', behavior: reduce ? 'auto' : 'smooth' });
      if (push) { history.replaceState(null, '', '#' + key); sfx.play('travel', 120); }
    }
    tb.forEach(function (b) { b.addEventListener('click', function () { go2(b.dataset.r, true); }); });
    var inView = false;
    whileVisible(tv, function () { inView = true; }, function () { inView = false; }, .5);
    d.addEventListener('keydown', function (e) {
      if (!inView || typing() || (menu && !menu.hidden) || (e.key !== 'ArrowDown' && e.key !== 'ArrowUp')) return;
      var i = tb.findIndex(function (b) { return b.hasAttribute('aria-current'); });
      var n = tb[(i + (e.key === 'ArrowDown' ? 1 : tb.length - 1)) % tb.length]; go2(n.dataset.r, true); e.preventDefault();
    });
    var h = location.hash.slice(1);
    if (h && tb.some(function (b) { return b.dataset.r === h; })) go2(h, false);
  }

  /* ── 시작: 슬롯 ── */
  var slotBtns = $$('.ng .slot');
  if (slotBtns.length) {
    var panes = $$('.replay');
    function mode(key, push) {
      slotBtns.forEach(function (b) { b.setAttribute('aria-selected', b.dataset.m === key); });
      panes.forEach(function (p) { p.hidden = p.dataset.m !== key; });
      if (push) { history.replaceState(null, '', '#' + key); sfx.play('select'); }
    }
    slotBtns.forEach(function (b) { b.addEventListener('click', function () {
      mode(b.dataset.m, true);
      /* 좁은 화면에서는 슬롯 아래로 열린 첫 장면까지 내려 준다 */
      if (innerWidth <= 900) { var pane = d.querySelector('.replay[data-m="' + b.dataset.m + '"]'); if (pane) pane.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' }); }
    }); });
    var mh = location.hash.slice(1);
    if (mh && panes.some(function (p) { return p.dataset.m === mh; })) mode(mh, false);
  }
})();
