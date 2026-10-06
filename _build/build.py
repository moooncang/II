# -*- coding: utf-8 -*-
# 일레온 사이트 생성기. 실행: python3 _build/build.py  (저장소 최상단에 html을 쓴다)
# 콘셉트: 사이트 자체가 일레온 게임 클라이언트.
#   표지=로딩 화면, 홈=타이틀과 장면들, 인물=캐릭터 선택, 인물 상세=프로필 창,
#   대륙=지역 이동 화면, 체계=인쇄된 규칙서(종이), 현실=2047년 기기 화면, 시작=새 게임.
import os, re, sys, html, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = os.path.join(ROOT, "_설정")
TITLE = "FULL DIVE - ILEON"
DESC = "FULL DIVE - ILEON · 일레온 · 벨라트 대륙"
E = html.escape

UP = ""
def bgd(code): return f"{UP}images/bg-draft/{BGD[code]}.webp"
def cs(code, n): return f"{UP}images/CS/{code}_{n}.webp"
def smp(code): return f"{UP}images/sample/{code}.webp"
def dims(src):
    if "/B/" in src or "/bg-draft/" in src: return 2048, 585
    if "/sample/" in src: return 1280, 883
    if re.search(r"_1\.webp$", src): return 1280, 828
    return 1280, 621

NAV = [("world.html", "대륙", "WORLD"), ("characters.html", "인물", "CHARACTER"), ("system.html", "체계", "RULES"),
       ("reality.html", "현실", "REALITY"), ("start.html", "시작", "NEW GAME")]
NAV_BG = {"world.html": "ER", "characters.html": "T", "system.html": "TR", "reality.html": "CT", "start.html": "RI"}

ARROW = '<svg class="ic" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 8h11.5M9 3.5 13.5 8 9 12.5" stroke="currentColor" stroke-width="1.8"/></svg>'
BACK = '<svg class="ic" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M14 8H2.5M7 3.5 2.5 8 7 12.5" stroke="currentColor" stroke-width="1.8"/></svg>'
PLAY = '<svg class="ic" width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M2 1l9 5-9 5z" fill="currentColor"/></svg>'
WARN = '<svg class="ic" width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M9 1.5 17 16H1z" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M9 7v4M9 12.6v1.4" stroke="currentColor" stroke-width="1.6"/></svg>'


def gk(g): return GRADE_KEY.get(g, "g1")
def grade(g): return f'<span class="grade {gk(g)}">{g}</span>' if g else ""
def img(src, alt="", cls="", lazy=True):
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy" decoding="async"' if lazy else ' decoding="async" fetchpriority="high"'
    w, h = dims(src)
    return f'<img src="{src}" alt="{E(alt)}" width="{w}" height="{h}"{c}{l}>'
def key(k): return f'<kbd class="key">{E(k)}</kbd>'
def lbl(t, cls=""): return f'<p class="lbl {cls}" data-rv>{t}</p>'
def rows(items, cls="data"):
    return f'<dl class="{cls}">' + "".join(f"<div><dt>{E(a)}</dt><dd>{b}</dd></div>" for a, b in items) + "</dl>"
def pnl(label, inner, cls="", right=""):
    return f'<div class="pnl {cls}"><div class="pnl-h"><span>{label}</span><span>{right}</span></div><div class="pnl-b">{inner}</div></div>'


def cta(cls="btn"):
    if CRACK:
        return f'<a class="{cls}" href="{CRACK}" target="_blank" rel="noopener"><span>크랙에서 접속</span>{PLAY}</a>'
    return f'<a class="{cls}" href="{UP}start.html"><span>접속하기</span>{PLAY}</a>'


def head(page, title, up="", desc=DESC, body=""):
    tabs = "".join(
        f'<a href="{up}{h}"{" aria-current=\"page\"" if h == page else ""}>{key(str(k + 1))}<span>{t}</span></a>' for k, (h, t, en) in enumerate(NAV))
    menu = "".join(
        f'<li><a href="{up}{h}" data-bg="{up}{"images/bg-draft/" + BGD[NAV_BG[h]] + ".webp"}"{" aria-current=\"page\"" if h == page else ""}><i>0{k + 1}</i><b>{t}</b><small>{en}</small></a></li>' for k, (h, t, en) in enumerate(NAV))
    full = title if title == TITLE else f"{title} · {TITLE}"
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(full)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(full)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#07080a">
<link rel="stylesheet" href="{up}assets/css/style.css">
<script>document.documentElement.className+=' js'</script>
</head>
<body class="{body}">
<a class="skip" href="#main">본문으로</a>
<header class="hud">
  <a class="logo" href="{up}home.html" aria-label="일레온 타이틀 화면"><b>ILEON</b><span class="srv"><i></i>벨라트 서버</span></a>
  <nav class="tabs" aria-label="주 메뉴">{tabs}</nav>
  <div class="clk" aria-label="현실 시각과 벨라트 시각"><span><i>REAL</i><b data-clock="real">--:--</b></span><span class="b"><i>BELAT</i><b data-clock="belat">--:--</b></span></div>
  <button class="esc" type="button" aria-expanded="false" aria-controls="menu">{key("ESC")}<span>메뉴</span></button>
</header>
<div class="menu" id="menu" hidden>
  <div class="menu-bg" aria-hidden="true"></div>
  <div class="menu-in">
    <p class="lbl">MENU · 일시 정지</p>
    <ol>{menu}</ol>
    <div class="menu-foot"><a href="{up}home.html">타이틀 화면</a><a href="{up}index.html">로그아웃</a><button type="button" class="menu-x">{key("ESC")} 돌아가기</button></div>
  </div>
</div>
<main id="main">
'''


def foot(up=""):
    links = "".join(f'<a href="{up}{h}">{t}</a>' for h, t, en in NAV)
    return f'''</main>
<footer class="foot">
  <div class="foot-in">
    <a class="logo" href="{up}home.html"><b>ILEON</b><span class="srv"><i></i>FULL DIVE</span></a>
    <nav aria-label="바닥글">{links}</nav>
    <p><span>현실 <b data-clock="real">--:--</b> · 벨라트 <b data-clock="belat">--:--</b></span></p>
  </div>
</footer>
<script src="{up}assets/js/main.js"></script>
</body>
</html>'''


def logout_scene(code="CT", *_):
    """페이지 끝: 문장 없이 타이틀과 접속 버튼만."""
    return f'''<section class="scene logout">
  <div class="bg">{img(bgd(code), "")}</div><div class="shade"></div>
  <div class="logout-in">
    <p class="wm-k" data-rv>FULL DIVE</p>
    <p class="wm" data-rv aria-hidden="true">ILEON</p>
    <div class="btns" data-rv>{cta()}</div>
  </div>
</section>
'''


def write(name, s):
    assert "—" not in s and "–" not in s, f"em/en dash in {name}"
    p = os.path.join(ROOT, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


# ── 크랙 출력 견본: 프롤로그 md → html ─────────────────────
def inline(t):
    t = E(t)
    t = re.sub(r"`([^`]+)`", r'<span class="sys">\1</span>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    return t


def render_prologue(fname):
    with open(os.path.join(SET, fname), encoding="utf-8") as f:
        lines = f.read().replace("—", "-").split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1; continue
        if ln.startswith("```"):
            buf = []; i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            body = re.sub(r"^(\[[^\]]+\])", r'<span class="k">\1</span>', E(chr(10).join(buf)), flags=re.M)
            out.append(f'<div class="status"><p class="status-h"><span>STATUS</span><span>상태창</span></p><pre class="info">{body}</pre></div>')
            continue
        m = re.match(r"!\[\]\((.+)\)", ln)
        if m:
            url = re.sub(r"https://cjivip\.uk/II/(B|CS)/([^.]+)\.png", lambda k: f"{UP}images/{k.group(1)}/{k.group(2)}.webp", m.group(1))
            out.append(f'<figure class="wide">{img(url, "")}</figure>' if "/B/" in url else f'<figure>{img(url, "")}</figure>')
            i += 1; continue
        if ln.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i][1:].strip()); i += 1
            q = buf[0].replace("퀘스트 :", "").strip()
            body = "".join(f"<p>{E(b[2:] if b.startswith('- ') else b)}</p>" for b in buf[1:-1])
            out.append(f'<div class="quest"><p class="q">퀘스트 : {E(q)}</p>{body}<p class="opt">{E(buf[-1])}</p></div>')
            continue
        if re.match(r"^`[^`]+`$", ln):
            out.append(f'<p><span class="sys">{E(ln.strip("`"))}</span></p>')
        elif ln.startswith("*") and ln.endswith("*") and not ln.startswith("**"):
            out.append(f'<p class="nar">{inline(ln[1:-1])}</p>')
        else:
            out.append(f'<p class="say">{inline(ln)}</p>')
        i += 1
    return "\n".join(out)


# ═════════════ 표지: 로딩 화면 ═════════════
RING = '''<svg viewBox="0 0 600 600" fill="none" aria-hidden="true">
  <g class="r1"><circle cx="300" cy="300" r="292" stroke="currentColor" stroke-opacity=".18"/>
    <circle cx="300" cy="300" r="292" stroke="currentColor" stroke-opacity=".7" stroke-width="2" stroke-dasharray="1 11"/>
    <path d="M300 8a292 292 0 0 1 206 85" stroke="#3a7bff" stroke-width="3"/>
    <path d="M300 592a292 292 0 0 1-206-85" stroke="#3a7bff" stroke-opacity=".6" stroke-width="2"/></g>
  <g class="r2"><circle cx="300" cy="300" r="250" stroke="currentColor" stroke-opacity=".4" stroke-width="10" stroke-dasharray="2 6"/>
    <path d="M50 300a250 250 0 0 1 250-250" stroke="currentColor" stroke-width="2.5"/>
    <path d="M550 300a250 250 0 0 1-250 250" stroke="currentColor" stroke-width="2.5"/></g>
  <g class="r3"><circle cx="300" cy="300" r="214" stroke="currentColor" stroke-opacity=".22"/>
    <path d="M300 86a214 214 0 0 1 151 63M149 451A214 214 0 0 1 86 300" stroke="currentColor" stroke-opacity=".85" stroke-width="5"/>
    <circle cx="300" cy="86" r="5" fill="currentColor"/><circle cx="300" cy="514" r="5" fill="#3a7bff"/></g>
  <g class="r4"><circle cx="300" cy="300" r="186" stroke="#3a7bff" stroke-opacity=".45" stroke-dasharray="40 8 4 8"/></g>
  <g class="r5"><circle cx="300" cy="27" r="4" fill="#bff6ff"/></g>
  <path class="tk" d="M300 0v26M300 574v26M0 300h26M574 300h26" stroke="currentColor" stroke-opacity=".6" stroke-width="2"/>
</svg>'''


def build_cover():
    logs = ["다이브포드 연결", "머리 받침 고정", "감각 해상도 확인", "벨라트 서버 응답", "접속 위치 · 리아텔 귀환석 광장"]
    s = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{E(DESC)}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{E(DESC)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#07080a">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="prefetch" href="home.html">
<script>document.documentElement.className+=' js'</script>
</head>
<body class="cover-body">
<main class="cover" data-cover>
  <div class="bg">{img(bgd("P"), "", lazy=False)}</div><div class="shade"></div>
  <div class="cv-top"><span>FULL DIVE · VRMMO</span><span>2047 · 대한민국</span></div>
  <div class="cv-ring"><span class="cv-sweep"></span><span class="cv-pulse"></span><span class="cv-pulse p2"></span>{RING}</div>
  <div class="cv-frame" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="cv-read" aria-hidden="true"><span>SYNC <b data-pct2>0</b>%</span><span>SENSE RES · HIGH</span><span>SERVER · BELAT</span></div>
  <div class="cv-mid">
    <h1 class="cv-logo"><span>FULL DIVE</span><b>ILEON</b></h1>
    <p class="cv-kr">일레온 · 행적을 읽는 세계</p>
  </div>
  <div class="cv-load">
    <ol class="cv-log" aria-hidden="true">{"".join(f"<li>{E(t)}</li>" for t in logs)}</ol>
    <div class="cv-bar"><i></i></div>
    <div class="cv-pct"><span>LOADING</span><b data-pct>0</b></div>
    <a class="cv-go" href="home.html" data-enter><span class="pc">아무 키나 누르거나 화면을 눌러 접속</span><span class="mo">화면을 눌러 접속</span></a>
  </div>
  <div class="cv-flash"></div>
</main>
<script src="assets/js/main.js"></script>
</body>
</html>'''
    write("index.html", s)


# ═════════════ 홈: 타이틀 화면과 장면들 ═════════════
def build_home():
    TAB = {"월드": "world", "랭킹": "world", "히든": "hidden", "정세": "news", "거래": "trade", "파티": "party"}
    chat = "".join(f'<li data-ch="{TAB.get(c, "etc")}" class="c-{TAB.get(c, "etc")}{" w" if c == "귓속말" else ""}"><span class="ch">[{c}]</span> {f"<b>{E(who)}</b> " if who else ""}<span class="msg">{E(t)}</span></li>' for c, who, t in CHAT)
    players = [c for c in C if c["side"] == "player"]
    npcs = [c for c in C if c["side"] == "npc"]
    menu = [("start.html", "새 게임", "NEW GAME"), ("world.html", "대륙", "WORLD"), ("characters.html", "캐릭터", "CHARACTER"),
            ("system.html", "규칙서", "RULES"), ("reality.html", "현실", "REALITY")]
    tmenu = "".join(f'<li><a href="{h}"{" class=\"on\"" if k == 0 else ""}><i>{PLAY}</i><b>{t}</b><small>{en}</small></a></li>' for k, (h, t, en) in enumerate(menu))
    regions = "".join(f'''<a class="rg" href="world.html#{r["key"]}" style="--i:{k}">
      <span class="rg-img">{img(bgd(r["img"]), r["name"])}</span>
      <span class="rg-tx"><i>{k + 1:02d}</i><b>{E(r["name"])}</b><small>{E(r["where"])}</small></span>
    </a>''' for k, r in enumerate(REGIONS))
    jobs = "".join(f'''<div class="job" data-k="{k}"{"" if k == 0 else " hidden"}>
        <b class="job-n" data-scramble>{E(n)}</b>
        <div class="job-g">{grade(g)}{f'<a href="char/{CMAP["D" if w == "헤리몽" else "E"]["slug"]}.html">{E(w)} {ARROW}</a>' if w else ""}</div>
      </div>''' for k, (n, g, t, w) in enumerate(HIDDEN))
    slant = "".join(f'''<a class="sl" href="char/{c["slug"]}.html" style="--i:{k}">
      <span class="sl-img">{img(smp(c["code"]), c["name"])}</span>
      <span class="sl-tx"><i>P{k + 1}</i><b>{E(c["name"])}</b><small>Lv{c["lv"]} · {E(c["job"].split("(")[0])}</small></span>
    </a>''' for k, c in enumerate(players))
    faces = "".join(f'<a href="char/{c["slug"]}.html">{img(smp(c["code"]), c["name"])}<span>{E(c["name"])}</span></a>' for c in npcs)
    slots = [("newbie", "뉴비", "RI", "리아텔 · 귀환석 광장", "Lv1 · 무직"),
             ("myth", "신화직업", "BS", "잿빛 회랑 · 균열 보스룸", "Lv1 · 신화"),
             ("free", "자유모드", "H", "현실 · 원룸", "제한 없음")]
    slot_html = "".join(f'''<a class="slot{" myth" if k == "myth" else ""}" href="start.html#{k}" data-rv>
      <span class="slot-img">{img(bgd(b), "")}</span>
      <span class="slot-no">SLOT<b>0{n + 1}</b></span>
      <span class="slot-nm"><b>{E(nm)}</b><small>{E(where)}</small></span>
      <span class="slot-meta"><span>{E(lv)}</span></span>
      <span class="slot-go">{PLAY}<span>시작</span></span>
    </a>''' for n, (k, nm, b, where, lv) in enumerate(slots))

    s = head("home.html", TITLE, body="home")
    s += f'''<section class="scene title">
  <div class="bg drift">{img(bgd("RI"), "리아텔의 들판과 마을", lazy=False)}</div><div class="shade"></div>
  <div class="title-in">
    <h1 class="tlogo"><span>FULL DIVE</span><b>ILEON</b><small>일레온</small></h1>
    <nav aria-label="타이틀 메뉴"><ul class="tmenu">{tmenu}</ul></nav>
  </div>
  <aside class="unit pnl" aria-label="플레이어 상태">
    <div class="pnl-h"><span>PLAYER</span><span>이방인</span></div>
    <div class="pnl-b">
      <div class="unit-top"><b>당신</b><span>Lv<em>1</em></span></div>
      <div class="bar hp"><i></i><span>HP</span></div>
      <dl class="data mini"><div><dt>직업</dt><dd>무직</dd></div><div><dt>위치</dt><dd>리아텔 · 귀환석 광장</dd></div></dl>
    </div>
  </aside>
  <div class="chat" aria-label="월드 채팅">
    <div class="chat-h" role="tablist" aria-label="채널">{"".join(f'<button type="button" role="tab" aria-selected="{"true" if k == "all" else "false"}" data-ch="{k}">{n}</button>' for k, n in (("all", "전체"), ("world", "월드"), ("hidden", "히든"), ("news", "정세"), ("trade", "거래"), ("party", "파티")))}</div>
    <ul class="chat-b">{chat}</ul>
  </div>
  <a class="scroll-hint" href="#regions"><span>SCROLL</span><i></i></a>
</section>

<section class="scene regions" id="regions">
  <div class="rg-h"><p class="lbl">WORLD · 벨라트 대륙</p><a class="more" href="world.html">지역 이동 {ARROW}</a></div>
  <div class="rgs">{regions}</div>
</section>

<section class="scene clocks">
  <div class="half real">
    <div class="bg">{img(bgd("P"), "포드방")}</div><div class="shade"></div>
    <div class="half-in">
      <p class="lbl">REAL · 2047 대한민국</p>
      <b class="big-clk" data-clock="real-s">--:--:--</b>
    </div>
  </div>
  <div class="seam" aria-hidden="true"><b>×4</b></div>
  <div class="half belat">
    <div class="bg">{img(bgd("KD"), "카뎃트")}</div><div class="shade"></div>
    <div class="half-in">
      <p class="lbl">BELAT · 여명기 이후 800년</p>
      <b class="big-clk" data-clock="belat-s">--:--:--</b>
    </div>
  </div>
</section>

<section class="scene cast">
  <div class="cast-h"><p class="lbl">CHARACTER · 15</p><a class="more" href="characters.html">캐릭터 선택 {ARROW}</a></div>
  <div class="slant">{slant}</div>
  <div class="npcs">{faces}</div>
</section>

<section class="scene reward" data-jobs>
  <div class="bg">{img(bgd("BS"), "균열 보스룸")}</div><div class="shade"></div>
  <div class="hc-art">{img(smp("E"), "무명")}</div>
  <div class="reward-in">
    <p class="sm-m"><span>SYSTEM</span>새 직업이 발현되었습니다.</p>
    {jobs}
    <div class="sm-f"><span class="dots">{"".join(f"<i{' class=on' if k == 0 else ''}></i>" for k in range(len(HIDDEN)))}</span><button type="button" class="btn sm ghost" data-next><span>다음</span></button><span class="pager" data-pager>1 / {len(HIDDEN)}</span></div>
  </div>
  <div class="zero"><span>HIDDEN · 신화</span><b>0</b></div>
</section>

<section class="scene newgame">
  <div class="ng-h"><p class="lbl">NEW GAME</p></div>
  <div class="slots">{slot_html}</div>
</section>
'''
    s += logout_scene("CT")
    s += foot()
    write("home.html", s)


# ═════════════ 대륙: 지역 이동 화면 ═════════════
def build_world():
    s = head("world.html", "대륙", body="world")
    bgs = "".join(f'<div class="tv-bg{" on" if k == 0 else ""}" data-r="{r["key"]}">{img(bgd(r["img"]), r["name"], lazy=k > 0)}</div>' for k, r in enumerate(REGIONS))
    lst = "".join(f'<li><button type="button" data-r="{r["key"]}"{" aria-current=\"true\"" if k == 0 else ""}><i>{k + 1:02d}</i><b>{E(r["name"])}</b><small>{E(r["where"])}</small></button></li>' for k, r in enumerate(REGIONS))
    infos = ""
    for k, r in enumerate(REGIONS):
        items = []
        if r["fields"]: items.append(("사냥터", " · ".join(f'{E(n)} <em>Lv{lv}</em>' for n, lv in r["fields"])))
        if r["dungeons"]: items.append(("던전", " · ".join(f'{E(n)} <em>{"Lv" + lv if lv != "?" else "?"}</em>' for n, kk, lv in r["dungeons"])))
        if r["god"]: items.append(("신앙", E(r["god"])))
        people = "".join(f'<a class="chip" href="char/{CMAP[p]["slug"]}.html">{img(smp(p), "")}<span>{E(CMAP[p]["name"])}</span></a>' for p in r["people"])
        infos += f'''<article class="tv-info" data-r="{r["key"]}"{"" if k == 0 else " hidden"}>
      <p class="where">{E(r["where"])}</p>
      <h2>{E(r["name"])}</h2>
      <p class="tx">{E(r["text"])}</p>
      {rows(items) if items else ""}
      {f'<div class="people">{people}</div>' if people else ""}
    </article>'''
    faults = "".join(f'<li data-rv><span class="no">{k + 1:02d}</span><b>{E(a).replace("↔", "<i>⟷</i>")}</b><p>{E(b)}</p></li>' for k, (a, b) in enumerate(FAULTS))
    threats = "".join(f'<li data-rv>{WARN}<b>{E(a)}</b><p>{E(b)}</p></li>' for a, b in THREATS)
    gods = "".join(f'<li data-rv style="--i:{k}"><b>{E(n)}</b><i>{E(k_)}</i><p>{E(t)}</p></li>' for k, (n, k_, t) in enumerate(GODS))
    s += f'''<section class="travel" data-travel>
  {bgs}<div class="shade"></div>
  <div class="tv-head">
    <p class="lbl">WORLD MAP · 지역 이동</p>
    <h1 class="ttl">벨라트 대륙</h1>
  </div>
  <ol class="tv-list" aria-label="지역">{lst}</ol>
  <div class="tv-panel pnl">
    <div class="pnl-h"><span>지역 정보</span><span>{key("↑")}{key("↓")} 이동</span></div>
    <div class="pnl-b">{infos}</div>
  </div>
</section>

<section class="board">
  <div class="board-h">
    {lbl("FAULT LINES · 대륙 정세")}
    <h2 class="ttl" data-rv>대륙 정세</h2>
  </div>
  <ol class="faults">{faults}</ol>
  <div class="threats-wrap">
    <h3 class="sub-t" data-rv>침공</h3>
    <ul class="threats">{threats}</ul>
  </div>
</section>

<section class="scene halak">
  <div class="bg">{img(smp("N"), "카시엘")}</div><div class="shade"></div>
  <div class="halak-in">
    {lbl("HALAK · 할라크족")}
    <h2 class="ttl" data-rv>할라크족<br><span>칼데스</span></h2>
    <a class="more" href="char/kasiel.html" data-rv>카시엘 · Lv88 {ARROW}</a>
  </div>
</section>

<section class="faith">
  <div class="faith-h">
    {lbl("FAITH · 신앙")}
    <h2 class="ttl" data-rv>여섯 신</h2>
  </div>
  <ol class="banners">{gods}</ol>
</section>

<section class="scene beyond">
  <div class="bg">{img(bgd("OW"), "이계")}</div><div class="shade"></div>
  <div class="beyond-in">
    {lbl("BEYOND · 이계")}
    <h2 class="ttl" data-rv>이계</h2>
  </div>
</section>
'''
    s += logout_scene("RH", "대륙은 지금도", "돌아가는 중.")
    s += foot()
    write("world.html", s)


# ═════════════ 인물: 캐릭터 선택 ═════════════
def char_data(c, up=""):
    return {"slug": c["slug"], "name": c["name"], "real": c.get("real", ""), "lv": c["lv"], "job": c["job"].split("(")[0],
            "grade": c["grade"], "gk": gk(c["grade"]) if c["grade"] else "", "hook": c["hook"], "role": c["role"],
            "side": c["side"], "img": smp(c["code"]), "hidden": c["hidden"]}


def build_characters():
    players = [c for c in C if c["side"] == "player"]
    first = C[0]
    roster = ""
    for grp, title in (("player", "이방인"), ("npc", "원주민")):
        items = [c for c in C if c["side"] == grp]
        roster += f'<li class="ro-g" data-side="{grp}">{title} <small>{len(items)}</small></li>'
        for c in items:
            d = char_data(c)
            roster += f'''<li data-side="{grp}"><a class="ro{" on" if c is first else ""}" href="char/{c["slug"]}.html" data-c='{E(json.dumps(d, ensure_ascii=False))}'>
          <span class="ro-img">{img(smp(c["code"]), "")}</span><span class="ro-nm"><b>{E(c["name"])}</b><small>{E(c["real"] if c["side"] == "player" else c["role"].split(" · ")[0])}</small></span><span class="ro-lv">Lv<b>{c["lv"]}</b></span></a></li>'''
    s = head("characters.html", "인물", body="select-page")
    s += f'''<section class="select" data-select>
  <div class="sel-bg"><img src="{smp(first["code"])}" alt="" width="1280" height="883" decoding="async" fetchpriority="high" data-sel-img></div><div class="shade"></div>
  <div class="sel-roster pnl">
    <div class="pnl-h"><span>캐릭터 선택</span><span>{len(C)}</span></div>
    <div class="pnl-b">
      <div class="sel-f" role="tablist" aria-label="거르기">
        <button type="button" role="tab" aria-selected="true" data-f="all">전체</button>
        <button type="button" role="tab" aria-selected="false" data-f="player">이방인 {len(players)}</button>
        <button type="button" role="tab" aria-selected="false" data-f="npc">원주민 {len(C) - len(players)}</button>
      </div>
      <ol class="roster">{roster}</ol>
    </div>
  </div>
  <div class="sel-info" aria-live="polite">
    <p class="sel-side"><span class="badge" data-f-side>이방인</span><span data-f-role>{E(first["role"])}</span></p>
    <h1 class="ttl" data-f-name>{E(first["name"])}</h1>
    <p class="sel-real" data-f-real>현실 · {E(first["real"])}</p>
    <p class="sel-hook" data-f-hook>{E(first["hook"])}</p>
    <div class="sel-stat"><span><i>LV</i><b data-f-lv>{first["lv"]}</b></span><span><i>CLASS</i><b class="t" data-f-job>{E(first["job"])}</b></span><span data-f-gradebox><i>GRADE</i><span data-f-grade>{grade(first["grade"])}</span></span></div>
    <a class="btn" href="char/{first["slug"]}.html" data-f-link><span>프로필 열기</span>{PLAY}</a>
  </div>
</section>
'''
    s += foot()
    write("characters.html", s)


# ═════════════ 인물 상세: 프로필 창 ═════════════
def build_char(i, c):
    global UP
    up = UP = "../"
    player = c["side"] == "player"
    prev_c, next_c = C[i - 1], C[(i + 1) % len(C)]
    stats = [("LV", f'<b class="n">{c["lv"]}</b>')]
    stats.append(("CLASS" if c["grade"] else "ROLE", f'<b>{E(c["job"])}</b>'))
    if c["grade"]: stats.append(("GRADE", grade(c["grade"]) + (' <small>히든</small>' if c["hidden"] else "")))
    stats.append(("AGE", f'<b>{c["sex"]} · {c["age"]}</b>'))
    looks = [("게임" if player else "외형", E(c["look_game"]))]
    if player: looks.append(("현실", E(c["look_real"])))
    looks.append(("말투", E(c["speech"])))
    body = "".join(f"<p>{E(p)}</p>" for p in c["body"])
    quote = f'<blockquote class="cq"><p>“{E(c["quote"])}”</p></blockquote>' if c["quote"] else ""

    def thumbs(code, labels, axis, hidden=False):
        bs = "".join(f'<button type="button" aria-pressed="{"true" if n == 1 else "false"}" data-src="{cs(code, n)}" data-alt="{E(c["name"])} {lab}">{img(cs(code, n), "")}<span>{lab}</span></button>' for n, lab in enumerate(labels, 1))
        return f'<div class="thumbs" data-axis="{axis}"{" hidden" if hidden else ""}>{bs}</div>'

    th = thumbs(c["code"], EXPR, "game")
    sw = ""
    if player:
        sw = f'<div class="sw" role="tablist" aria-label="게임과 현실"><button type="button" role="tab" data-axis="game" aria-selected="true">게임</button><button type="button" role="tab" data-axis="real" aria-selected="false">현실</button></div>'
        th += thumbs(c["code"] + "2", EXPR_REAL, "real", hidden=True)

    s = head("characters.html", c["name"], up=up, desc=f'{c["name"]}. {c["hook"]}', body="prof-page")
    s += f'''<section class="prof">
  <div class="prof-stage">
    <div class="stage">{img(cs(c["code"], 1), c["name"], "fig", lazy=False)}</div>
    <div class="exp">
      <div class="exp-h"><span class="lbl">표정</span>{sw}<span class="exp-k">{key("←")}{key("→")}</span></div>
      {th}
    </div>
  </div>
  <div class="prof-info">
    <nav class="prof-nav" aria-label="다른 인물">
      <a href="../characters.html" class="back">{BACK} 캐릭터 선택</a>
      <span><a href="{prev_c["slug"]}.html" data-prev>{key("Q")} {E(prev_c["name"])}</a><a href="{next_c["slug"]}.html" data-next>{E(next_c["name"])} {key("E")}</a></span>
    </nav>
    <p class="sel-side"><span class="badge{"" if player else " npc"}">{"이방인" if player else "원주민"}</span><span>{E(c["role"])}</span></p>
    <h1 class="ttl">{E(c["name"])}</h1>
    {f'<p class="sel-real">현실 · {E(c["real"])}</p>' if player else ""}
    <p class="prof-hook">{E(c["hook"])}</p>
    <dl class="stats">{"".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in stats)}</dl>
    <div class="prose">{body}</div>
    {quote}
    {rows(looks, "data looks")}
  </div>
</section>
'''
    s += foot(up)
    UP = ""
    write(f"char/{c['slug']}.html", s)


# ═════════════ 체계: 인쇄된 규칙서 ═════════════
def build_system():
    chapters = [("level", "레벨"), ("class", "전직"), ("hidden", "히든직"), ("top", "상위 다섯"), ("dungeon", "던전"), ("incident", "사변"), ("quest", "퀘스트")]
    toc = "".join(f'<li><a href="#{k}"><span>{n}</span><i></i><b>{j + 1}</b></a></li>' for j, (k, n) in enumerate(chapters))
    tiers = [("1차", "Lv10", "일반", "전직 NPC에게서."),
             ("2차", "Lv40 + 실적 심사", "희귀", "이쯤이면 길드가 영입하러 온다. 생산 계열은 레벨 대신 제작 실적."),
             ("3차", "Lv60 + 시련", "에픽", "정규 루트의 끝. 서버 전체에 다섯 명."),
             ("히든", "레벨 무관", "일반~신화", "조건을 채운 사람만. 얻는 순간 서버 로그엔 직업명만 뜬다.")]
    s = head("system.html", "체계", body="paper")

    def ch(n, k, title, sub):
        return f'<header class="ch-h" id="{k}"><span class="ch-n" aria-hidden="true">{n}</span><div><p class="ch-k">제{n}장</p><h2>{title}</h2></div></header>'

    s += f'''<article class="book">
<section class="b-cover">
  <div class="b-cover-img">{img(bgd("TR"), "훈련장", lazy=False)}</div>
  <div class="b-cover-tx">
    <p class="b-k">이방인을 위한 규칙서 · 벨라트 서버</p>
    <h1>규칙서</h1>
  </div>
  <nav class="b-toc" aria-label="차례"><p>차례</p><ol>{toc}</ol></nav>
  <span class="stamp">Lv64<small>현재 정점</small></span>
</section>

<section class="b-ch">
  {ch(1, "level", "레벨", "이방인 기준 얘기. 원주민 강자들은 이 상한 밖에 있다. 기사단장, 공작가, 할라크족 장로는 Lv70에서 90대. 랭킹 1위도 그 앞에선 아래.")}
  <div class="ladder" data-rv>
    <div class="lad-bar"><span style="--w:15">1-15</span><span class="gap" style="--w:5"></span><span style="--w:15">20-35</span><span class="gap" style="--w:5"></span><span style="--w:10">40-50</span><span style="--w:9">55+</span><span class="peak" style="--w:5">64</span></div>
    <ol>
      <li><b>Lv1-15</b>절대다수가 여기서 접는다.</li>
      <li><b>Lv20-35</b>꾸준파. 마을에서 얼굴을 알아본다.</li>
      <li><b>Lv40-50</b>상위권. 길드가 먼저 찾아온다.</li>
      <li><b>Lv55+</b>랭커.</li>
      <li><b>Lv64</b>정점. 지금은 한 명.</li>
    </ol>
  </div>
</section>

<section class="b-ch">
  {ch(2, "class", "전직", "정규직은 뼈대만 있다. 이름도 조건도 다 공개돼서, 공략만 보면 누구나 밟아 올라간다.")}
  <table class="tbl" data-rv>
    <thead><tr><th>차수</th><th>조건</th><th>등급</th><th>메모</th></tr></thead>
    <tbody>{"".join(f'<tr{" class=hid" if a == "히든" else ""}><th>{E(a)}</th><td>{E(b)}</td><td>{E(g)}</td><td>{E(t)}</td></tr>' for a, b, g, t in tiers)}</tbody>
  </table>
  <div class="cols2">
    <div data-rv><h3>계열 아홉</h3><p class="classes">{" · ".join(E(x) for x in CLASSES)}</p></div>
    <div data-rv><h3>정규 계보 몇 가지</h3><ul class="lines">{"".join("<li>" + " <i>→</i> ".join(E(x) for x in ln) + "</li>" for ln in LINES)}</ul></div>
  </div>
</section>

<section class="b-ch inv">
  {ch(3, "hidden", "히든직", "시스템이 행적을 읽고 그 사람만의 직업을 만든다. 같은 이름은 둘이 못 가진다. 서버 로그엔 직업명만 뜨니까, 하나 나올 때마다 커뮤는 조건을 추측하고, 대개 틀린다.")}
  <dl class="entries">{"".join(f'<div data-rv><dt><b>{E(n)}</b><span>{E(g)}</span></dt><dd>{E(t)}{f" <em>보유 · {E(w)}</em>" if w else ""}</dd></div>' for n, g, t, w in HIDDEN)}</dl>
  <div class="grades" data-rv>
    <ol>{"".join(f"<li>{g}</li>" for g in GRADES)}</ol>
    <p>등급은 지금의 강함이 아니라 잠재력. 정규 루트는 에픽에서 끝나고, 유니크부터는 히든직뿐이다. 히든직 등급은 일반부터 신화까지 제각각이라, 조건이 까다롭다고 등급이 높은 것도 아니다. 전설은 서버에 두세 명.</p>
  </div>
  <span class="stamp red">신화<small>0명</small></span>
</section>

<section class="b-ch">
  {ch(4, "top", "3차 전직자", "3차 전직자, 서버 전체에 다섯. 나머지 넷은 서버 로그와 커뮤 소문으로만 오르내린다.")}
  <table class="tbl rank" data-rv>
    <thead><tr><th>#</th><th>이름</th><th>레벨</th><th>직업</th><th>메모</th></tr></thead>
    <tbody>{"".join(f'<tr><td class="r">{k + 1}</td><th>{E(n)}</th><td>Lv{lv}</td><td>{E(j)}</td><td>{E(t)}</td></tr>' for k, (n, a, sx, lv, j, t) in enumerate(THIRD))}</tbody>
  </table>
</section>

<section class="b-ch">
  {ch(5, "dungeon", "던전", "필드보스는 나오는 시각이 대충 알려져 있어서, 길드들이 시간 맞춰 몰려든다. 네임드는 일반 몬스터 자리에 아주 가끔. 그건 순전히 운.")}
  <table class="tbl" data-rv>
    <thead><tr><th>종류</th><th>인원 · 주기</th><th>메모</th></tr></thead>
    <tbody>
      <tr><th>소굴</th><td>3-5인 · 반복 입장</td><td>한 시간 안쪽. 매일의 벌이.</td></tr>
      <tr><th>유적</th><td>5-8인 · 주 1회</td><td>기믹이 있고, 스킬의 원천이 되는 고대 기록이 나온다.</td></tr>
      <tr><th>봉인지</th><td>20인 이상 · 라흐나</td><td>제1·2환은 Lv58-64. 제3환은 아직 아무도 못 넘었다.</td></tr>
      <tr><th>균열</th><td>무작위 · 시간 제한</td><td>예고 없이 열리고 닫힌다. 최초 돌파 보상이 걸려서, 소문 돌면 사람이 몰린다.</td></tr>
      <tr><th>이계</th><td>균열 너머</td><td>대륙 밖. 제일 어려운 곳.</td></tr>
    </tbody>
  </table>
</section>

<section class="b-ch">
  {ch(6, "incident", "사변", "일정은 없다. 결과는 영구히 남고, 큰 사변엔 결정적 역할을 한 이방인 이름이 같이 기록된다.")}
  <ol class="flow" data-rv>{"".join(f'<li><span>{k + 1}</span><b>{n}</b><p>{E(t)}</p></li>' for k, (n, t) in enumerate(INCIDENT_FLOW))}</ol>
  <div class="cols2 one">
    <div data-rv><h3>규모</h3><dl class="scale">{"".join(f"<div><dt>{n}</dt><dd>{E(t)}</dd></div>" for n, t in INCIDENT_SCALE)}</dl></div>
  </div>
</section>

<section class="b-ch">
  {ch(7, "quest", "퀘스트", "정세와 사변, 사람의 사정에서 생겨난다. 의뢰자는 자기 이익이 먼저라 보상을 깎고, 정보를 빼고, 등을 돌리기도 한다. 어떻게 푸느냐에 따라 결과가 갈리고, 그 결과가 다음 정세가 된다.")}
  <div class="cols2 q">
    <dl class="qk" data-rv>{"".join(f"<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>" for a, b in QUEST_KINDS)}</dl>
    <div class="qcard" data-rv><p class="qc-k">예시</p><p class="q">퀘스트 : 견습 기사의 안내</p><p>유안을 따라 수비대 훈련장에서 기본 무기를 받고, 옛 수로의 큰쥐 5마리를 처치한다.</p><p class="rw">보상 · 초심자 무기, 20골드</p><p class="opt">수락 | 거절</p></div>
  </div>
</section>
</article>
'''
    s += foot()
    write("system.html", s)


# ═════════════ 현실: 2047년 기기 화면 ═════════════
REAL_LIFE = {"A": "길드 법인 정직원", "B": "울산 공단 하청", "C": "공방 운영", "D": "공략 방송인", "E": "집 밖에 나가지 않는다"}


def build_reality():
    players = [c for c in C if c["side"] == "player"]
    contacts = "".join(f'''<a class="ct" href="char/{c["slug"]}.html" data-rv>
      <span class="ct-ph">{img(smp(c["code"] + "2"), c["real"])}{img(smp(c["code"]), "", "g")}</span>
      <span class="ct-tx"><b>{E(c["real"])}</b><small>{E(REAL_LIFE[c["code"]])}</small><span class="ct-g">게임 · {E(c["name"])}</span></span>
    </a>''' for c in players)
    s = head("reality.html", "현실", body="os")
    s += f'''<div class="os-bg" aria-hidden="true">{img(bgd("CT"), "", lazy=False)}</div>
<section class="lock">
  <p class="lock-date" data-clock="date-long">2047년</p>
  <b class="lock-time" data-clock="real">--:--</b>
  <h1 class="lock-t">2047, 대한민국</h1>
  <ul class="notis">
    <li data-rv><span class="app pod">P</span><div><b>다이브포드</b><p>정비 기한을 넘기면 감각이 한 박자씩 늦게 따라옵니다.</p></div><time>지금</time></li>
    <li data-rv><span class="app pay">₩</span><div><b>자동 결제</b><p>월정액, 포드 할부, 전기세, 정비비가 이번 달에도 빠져나갑니다.</p></div><time>오늘</time></li>
    <li data-rv><span class="app com">C</span><div><b>커뮤</b><p>새 히든직이 서버 로그에 떴습니다. 조건 추측 글이 올라오는 중.</p></div><time>방금</time></li>
  </ul>
</section>

<section class="apps">
  <div class="apps-h">
    <p class="lbl">DIVE POD</p>
    <h2>다이브포드</h2>
  </div>
  <div class="cards">
    <article class="card wide" data-rv>
      <p class="c-k">포드 등급</p>
      <div class="tiers"><span>보급형</span><i></i><span>프로용</span></div>
      <div class="tier-ex"><span><b>울산강펀치</b> 보급형 최저가</span><span><b>무명</b> PK로 번 돈으로 산 프로용</span></div>
    </article>
    <article class="card" data-rv><p class="c-k">포드방</p><b class="c-b">공용</b></article>
    <article class="card warn" data-rv><p class="c-k">정비</p><b class="c-b">기한 확인 필요</b></article>
    <article class="card" data-rv>
      <p class="c-k">로그아웃 직후</p>
      <ul class="cond"><li>목이 마르다</li><li>다리가 저리다</li><li>시간 감각이 어긋난다</li></ul>
      
    </article>
    <article class="card wallet" data-rv>
      <p class="c-k">지갑</p>
      <ul class="bills"><li>월정액<span>자동 결제</span></li><li>포드 할부<span>자동 결제</span></li><li>전기세<span>자동 결제</span></li><li>정비비<span>자동 결제</span></li></ul>
      <div class="xchg"><span>골드</span><i>→</i><span>원</span><small>수수료 있음 · 출금 느림</small></div>
    </article>
    <article class="card acct" data-rv>
      <p class="c-k">계정</p>
      <div class="slot1"><b>캐릭터 슬롯</b><span>1 / 1</span></div>
      <ul class="cond"><li>부계정 없음</li><li>핵·매크로 없음</li></ul>
      <button type="button" class="danger" disabled>캐릭터 삭제</button>
    </article>
    <article class="card info-c" data-rv>
      <p class="c-k">현실 장면 정보창</p>
      <pre class="info">[현실] 3월 14일 (목) 23:40
[잔고] 미정 | 다음 결제 미정
[포드] 미정
[컨디션] 양호
[관계] └─</pre>
    </article>
  </div>
</section>

<section class="feed">
  <div class="apps-h">
    <p class="lbl">COMMUNITY</p>
    <h2>커뮤</h2>
  </div>
  <ol class="posts">
    <li data-rv><span class="tag">감지</span><p>누가 뭔가를 봤다. 목격담 한 줄.</p></li>
    <li data-rv><span class="tag">확산</span><p>커뮤와 방송을 타고 번진다.</p></li>
    <li data-rv><span class="tag">변질</span><p>안 한 일이, 그 사람이 한 일이 된다.</p></li>
    <li data-rv><span class="tag">잔향</span><p>잠잠해져도 뭔가는 남는다.</p></li>
  </ol>
</section>

<section class="contacts">
  <div class="apps-h">
    <p class="lbl">CONTACTS</p>
    <h2>연락처</h2>
  </div>
  <div class="cts">{contacts}</div>
</section>
'''
    s += foot()
    write("reality.html", s)


# ═════════════ 시작: 새 게임 ═════════════
def build_start():
    modes = [
        ("newbie", "뉴비", "일레온 프롤로그(뉴비).md", "RI", "리아텔 · 귀환석 광장", "Lv1 · 무직",
         "처음 대륙에 내려선 이방인. 견습 기사 유안의 안내를 받고, 옛 수로 큰쥐부터. 대륙을 처음부터 천천히 밟고 싶다면."),
        ("myth", "신화직업", "일레온 프롤로그(신화직업).md", "BS", "잿빛 회랑 · 균열 보스룸", "Lv1 · 신화",
         "줄리엣과 둘이서 균열의 파수꾼을 쓰러뜨렸고, 보상에 먼저 손이 닿았다. 서비스 이래 첫 신화 등급 직업. 대가로 레벨은 1. 무슨 직업인지는, 시작하면서 당신이 밝힌다."),
        ("free", "자유모드", "일레온 프롤로그(자유모드).md", "H", "현실 · 원룸", "제한 없음",
         "밤 열한 시 사십 분, 포드 앞. 어디로 들어갈지, 누구로 살지 아무것도 안 정해졌다. 원하는 대로."),
    ]
    slots = "".join(f'''<button type="button" class="slot{" myth" if key_ == "myth" else ""}" role="tab" aria-selected="{"true" if k == 0 else "false"}" data-m="{key_}">
      <span class="slot-img">{img(bgd(b), "", lazy=False)}</span>
      <span class="slot-no">SLOT<b>0{k + 1}</b></span>
      <span class="slot-nm"><b>{E(name)}</b><small>{E(where)}</small></span>
      <span class="slot-meta"><span>{E(lv)}</span></span>
    </button>''' for k, (key_, name, fn, b, where, lv, desc) in enumerate(modes))
    panes = "".join(f'''<article class="replay{" myth" if key_ == "myth" else ""}" id="{key_}" data-m="{key_}" role="tabpanel"{"" if k == 0 else " hidden"}>
      <div class="rp-meta">
        <p class="lbl">SLOT 0{k + 1}</p>
        <h2 class="ttl">{E(name)}</h2>
        {rows([("시작 지점", E(where)), ("시작 상태", E(lv))])}
        {cta()}
      </div>
      <div class="rp-log pnl"><div class="pnl-h"><span>크랙 출력 견본 · 첫 장면</span><span>{E(name)}</span></div><div class="pnl-b log">{render_prologue(fn)}</div></div>
    </article>''' for k, (key_, name, fn, b, where, lv, desc) in enumerate(modes))
    keys = [("`문장`", "시스템", "월드 메시지, 레벨업, 전직 같은 시스템 메시지."),
            ("&gt;문장", "채팅", "귓속말, 길드챗, 파티챗. 풀다이브라 평소엔 목소리로 말하고, 채팅은 거들 뿐."),
            ("!인터넷 - 내용", "검색", "궁금한 건 찾아본다. 커뮤, 위키, 방송, 기사가 원문 그대로."),
            ("판정", "행동", "모든 행동은 시도. 성공, 대가를 치른 성공, 실패. 레벨 10 이상 차이면 거의 일방적. 죽으면 레벨이 깎이고 현실로 튕겨 나온다.")]
    s = head("start.html", "시작", body="start-page")
    s += f'''<section class="ng">
  <div class="bg">{img(bgd("CP"), "", lazy=False)}</div><div class="shade"></div>
  <div class="ng-top">
    <p class="lbl">NEW GAME · 시작 모드 선택</p>
    <h1 class="ttl">새 게임</h1>
  </div>
  <div class="slots" role="tablist" aria-label="시작 모드">{slots}</div>
</section>
<section class="replays">{panes}</section>

<section class="controls">
  <div class="ctl-h">
    <p class="lbl">KEY GUIDE · 조작</p>
    <h2 class="ttl">조작</h2>
  </div>
  <div class="ctl-grid">
    {"".join(f'<div class="ctl" data-rv><kbd class="cap">{a}</kbd><b>{b}</b><p>{c}</p></div>' for a, b, c in keys)}
  </div>
  <div class="binds pnl"><div class="pnl-h"><span>단축어</span><span>{len(SHORTCUTS)}</span></div><div class="pnl-b">{rows([(a, E(b)) for a, b in SHORTCUTS])}</div></div>
</section>
'''
    s += logout_scene("RI", "대륙은 지금도", "돌아가는 중.")
    s += foot()
    write("start.html", s)


if __name__ == "__main__":
    build_cover(); build_home(); build_world(); build_characters()
    for i, c in enumerate(C):
        build_char(i, c)
    build_system(); build_reality(); build_start()
    print("ok:", 7 + len(C), "pages")
