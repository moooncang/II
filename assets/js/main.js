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
    $$('[data-clock]').forEach(function (e) { var v = map[e.dataset.clock]; if (v && e.textContent !== v) e.textContent = v; });
  }
  tick(); setInterval(tick, 250);

  /* ── 상단 HUD ── */
  var sentinel = d.createElement('div');
  sentinel.style.cssText = 'position:absolute;top:0;left:0;height:90px;width:1px;pointer-events:none';
  d.body.prepend(sentinel);
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { root.classList.toggle('scrolled', !es[0].isIntersecting); }).observe(sentinel);

  /* ── ESC 메뉴, 숫자 키 이동 ── */
  var menu = $('.menu'), escBtn = $('.esc'), menuBg = $('.menu-bg');
  function openMenu(o) {
    if (!menu) return;
    menu.hidden = !o; menu.classList.toggle('open', o);
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
      if (e.key === 'Escape') { openMenu(menu.hidden); e.preventDefault(); return; }
      if (/^[1-5]$/.test(e.key) && navLinks[+e.key - 1]) location.href = navLinks[+e.key - 1].href;
    });
  }

  /* ── 등장 ── */
  var rv = $$('[data-rv]');
  if ('IntersectionObserver' in window && !reduce) {
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
  if (chat && !reduce) setInterval(function () {
    var li = chat.firstElementChild; if (!li) return;
    li.classList.remove('new'); chat.appendChild(li); void li.offsetWidth; li.classList.add('new');
  }, 2600);

  /* ── 홈: 사망 화면 ── */
  var death = $('[data-death]');
  if (death) {
    var cd = $('[data-cd]', death), dt = [];
    function clearD() { dt.forEach(clearTimeout); dt = []; }
    function runDeath() {
      clearD(); death.classList.remove('done'); cd.textContent = '3';
      requestAnimationFrame(function () { death.classList.add('on'); });
      if (reduce) { cd.textContent = '0'; death.classList.add('done'); return; }
      [2, 1, 0].forEach(function (n, k) { dt.push(setTimeout(function () { cd.textContent = n; if (!n) death.classList.add('done'); }, 1600 + k * 1000)); });
      dt.push(setTimeout(function () { death.classList.remove('on', 'done'); dt.push(setTimeout(runDeath, 1400)); }, 9000));
    }
    whileVisible(death, runDeath, function () { clearD(); death.classList.remove('on', 'done'); }, .35);
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
    $('[data-next]', jobsBox).addEventListener('click', function () { showJob(ji + 1); auto(); });
    whileVisible(jobsBox, function () { showJob(ji); auto(); }, function () { clearInterval(jt); });
  }

  /* ── 홈: 사변 진행 ── */
  var ev = $('[data-event]');
  if (ev) {
    var sb = $$('.stages button', ev), stx = $$('.stage-tx p', ev), si = 0, st = 0;
    function stage(n, run) {
      si = n; clearTimeout(st);
      sb.forEach(function (b, k) {
        b.toggleAttribute('aria-current', k === si);
        b.classList.toggle('done', k < si);
        var f = $('.fill', b); f.style.animation = 'none'; void f.offsetWidth; f.style.animation = '';
      });
      stx.forEach(function (p, k) { p.hidden = k !== si; });
      if (run && !reduce) st = setTimeout(function () { stage((si + 1) % sb.length, true); }, 4600);
    }
    $('.stages', ev).classList.toggle('paused', reduce);
    sb.forEach(function (b, k) { b.addEventListener('click', function () { stage(k, true); }); });
    whileVisible(ev, function () { stage(si, true); }, function () { clearTimeout(st); });
  }

  /* ── 표지: 로딩 → 접속 ── */
  var cover = $('[data-cover]');
  if (cover) {
    var bar = $('.cv-bar i', cover), pct = $('[data-pct]', cover), logs = $$('.cv-log li', cover), go = $('[data-enter]', cover);
    var t0 = performance.now(), dur = reduce ? 1 : 2400, ready = false;
    (function load(t) {
      var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 2.2);
      bar.style.setProperty('--p', e); pct.textContent = Math.round(e * 100);
      logs.forEach(function (li, k) { if (e > (k + .6) / logs.length) li.classList.add('on'); });
      if (p < 1) requestAnimationFrame(load); else { ready = true; cover.classList.add('ready'); }
    })(t0);
    function enter(e) {
      if (!ready || cover.classList.contains('go')) return;
      if (e) e.preventDefault();
      if (reduce) { location.href = go.href; return; }
      cover.classList.add('go');
      setTimeout(function () { location.href = go.href; }, 1150);
    }
    cover.addEventListener('click', enter);
    d.addEventListener('keydown', function (e) { if (!e.metaKey && !e.ctrlKey && !e.altKey && e.key !== 'Tab') enter(e); });
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
        setFig(b.dataset.src, b.dataset.alt);
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
      if (push) history.replaceState(null, '', '#' + key);
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
      if (push) history.replaceState(null, '', '#' + key);
    }
    slotBtns.forEach(function (b) { b.addEventListener('click', function () { mode(b.dataset.m, true); }); });
    var mh = location.hash.slice(1);
    if (mh && panes.some(function (p) { return p.dataset.m === mh; })) mode(mh, false);
  }
})();
