# -*- coding: utf-8 -*-
# 일레온 사이트 생성기. 실행: python3 _build/build.py  (저장소 최상단에 html을 쓴다)
import os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = os.path.join(ROOT, "_설정")
TITLE = "FULL DIVE - ILEON"
DESC = "다이브포드에 누우면, 여명기 이후 800년의 벨라트 대륙이 열린다. 행적을 읽는 세계, 일레온."
E = html.escape

# ── 그림 (저장소 images/) ─────────────────────────
UP = ""
def bgd(code): return f"{UP}images/bg-draft/{BGD[code]}.webp"   # 배경 원안 (HUD 없음)
def cs(code, n): return f"{UP}images/CS/{code}_{n}.webp"        # 인물 상황 그림
def smp(code): return f"{UP}images/sample/{code}.webp"          # 인물 견본
def dims(src):
    if "/B/" in src or "/bg-draft/" in src: return 2048, 585
    if "/sample/" in src: return 1280, 883
    if re.search(r"_1\.webp$", src): return 1280, 828
    return 1280, 621

NAV = [("world.html", "대륙"), ("characters.html", "인물"), ("system.html", "체계"),
       ("reality.html", "현실"), ("start.html", "시작")]

ARROW = '<svg class="ic" width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 8h11M9 3.5 13.5 8 9 12.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="square"/></svg>'
BACK = '<svg class="ic" width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M14 8H3M7 3.5 2.5 8 7 12.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="square"/></svg>'


def gk(g): return GRADE_KEY.get(g, "g1")
def grade(g): return f'<span class="grade {gk(g)}">{g}</span>' if g else ""
def img(src, alt="", cls="", lazy=True):
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy" decoding="async"' if lazy else ' decoding="async" fetchpriority="high"'
    w, h = dims(src)
    return f'<img src="{src}" alt="{E(alt)}" width="{w}" height="{h}"{c}{l}>'
def lbl(t):
    return f'<p class="lbl">{t}</p>'
def rows(items):
    return '<dl class="data">' + "".join(f"<div><dt>{E(a)}</dt><dd>{b}</dd></div>" for a, b in items) + "</dl>"


def cta(cls="btn"):
    """크랙 링크가 있으면 플레이 버튼, 없으면 시작 모드로."""
    if CRACK:
        return f'<a class="{cls}" href="{CRACK}" target="_blank" rel="noopener" data-mag>크랙에서 플레이 {ARROW}</a>'
    return f'<a class="{cls}" href="{UP}start.html" data-mag>시작 모드 고르기 {ARROW}</a>'


def head(page, title, up="", desc=DESC):
    nav = "\n".join(
        f'      <li><a href="{up}{h}"{" aria-current=\"page\"" if h == page else ""}>{t}</a></li>' for h, t in NAV)
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
<meta name="theme-color" content="#0a0f1d">
<link rel="stylesheet" href="{up}assets/css/style.css">
<script>document.documentElement.className+=' js'</script>
</head>
<body>
<div class="progress" aria-hidden="true"></div>
<header class="top">
  <div class="wrap">
    <a class="brand" href="{up}home.html" aria-label="일레온 홈"><i></i><b>ILEON</b></a>
    <button class="menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><b class="sr">메뉴</b></button>
    <ul class="nav" id="nav">
{nav}
    </ul>
    <div class="clock" aria-label="현실 시각과 벨라트 시각">
      <span class="rt"><i>현실</i><b data-clock="real">--:--</b></span>
      <span class="bt"><i>벨라트</i><b data-clock="belat">--:--</b></span>
    </div>
  </div>
</header>
<main>
'''


def foot(up=""):
    links = "".join(f'<a href="{up}{h}">{t}</a>' for h, t in NAV)
    return f'''</main>
<footer class="foot">
  <div class="wrap">
    <a class="brand" href="{up}home.html"><i></i><b>ILEON</b></a>
    <nav aria-label="바닥글">{links}</nav>
  </div>
</footer>
<script src="{up}assets/js/main.js"></script>
</body>
</html>'''


def close_band(text="대륙은 지금도<br>돌아가고 있다.", sub="다이브포드 연결 대기", code="RH"):
    return f'''<section class="close">
  <div class="close-bg" data-par>{img(bgd(code), "", "bgimg")}</div>
  <div class="wrap">
    <span class="sysmsg" data-rv>{E(sub)}</span>
    <h2 data-rv style="--i:1">{text}</h2>
    <div class="btn-row" data-rv style="--i:2">{cta()}</div>
  </div>
</section>
'''


def phead(code, h1, p, toc=None, alt="", sysline=""):
    s = f'''<section class="phead">
  <div class="phead-bg" data-par>{img(bgd(code), alt, "bgimg", lazy=False)}</div>
  <div class="wrap">
    {f'<span class="sysmsg" data-rv>{sysline}</span>' if sysline else ""}
    <h1 data-rv style="--i:1">{h1}</h1>
    <p data-rv style="--i:2">{p}</p>
  </div>
</section>
'''
    if toc:
        s += '<nav class="toc" aria-label="이 페이지"><div class="wrap">' + "".join(f'<a href="#{k}">{v}</a>' for k, v in toc) + "</div></nav>\n"
    return s


def card(c, up="", i=0):
    player = c["side"] == "player"
    sub = c["real"] if player else c["role"].split(" · ")[0]
    meta = c["role"].split(" · ")[-1] if player else c["job"]
    return f'''<a class="card spot" href="{up}char/{c["slug"]}.html" data-side="{c["side"]}" data-rv style="--i:{i % 3}">
  <div class="ph">{img(smp(c["code"]), c["name"])}<span class="badge{"" if player else " npc"}">{"이방인" if player else "원주민"}</span></div>
  <div class="cap">
    <span class="nm"><b>{E(c["name"])}</b><small>{E(sub)}</small></span>
    <span class="meta">Lv{c["lv"]} · {E(meta)}</span>
    <p class="hook">{E(c["hook"])}</p>
    {f'<span class="job">{E(c["job"].split("(")[0])} {grade(c["grade"])}</span>' if c["grade"] else ""}
  </div>
</a>'''


def write(name, s):
    assert "—" not in s and "–" not in s, f"em/en dash in {name}"
    p = os.path.join(ROOT, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


# ── 크랙 출력 견본: 프롤로그 md → html ─────────────────────
def inline(t):
    t = E(t)
    t = re.sub(r"`([^`]+)`", r'<span class="sysmsg">\1</span>', t)
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
            out.append(f'<pre class="info">{E(chr(10).join(buf))}</pre>')
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
            out.append(f'<div class="qbox"><p class="q">퀘스트 : {E(q)}</p>{body}<p class="opt">{E(buf[-1])}</p></div>')
            continue
        if re.match(r"^`[^`]+`$", ln):
            out.append(f'<span class="sysmsg">{E(ln.strip("`"))}</span>')
        elif ln.startswith("*") and ln.endswith("*") and not ln.startswith("**"):
            out.append(f'<p class="nar">{inline(ln[1:-1])}</p>')
        else:
            out.append(f'<p class="line">{inline(ln)}</p>')
        i += 1
    return "\n".join(out)


# ═════════════ 표지 ═════════════
RING = '''<svg viewBox="0 0 400 400" aria-hidden="true" fill="none">
  <g class="r3"><circle cx="200" cy="200" r="196" stroke="rgba(94,230,242,.14)" stroke-width="1"/>
    <circle cx="200" cy="200" r="196" stroke="rgba(94,230,242,.55)" stroke-width="1.5" stroke-dasharray="2 14"/></g>
  <g class="r1"><circle cx="200" cy="200" r="168" stroke="rgba(94,230,242,.35)" stroke-width="6" stroke-dasharray="3 5"/>
    <path d="M200 26 A174 174 0 0 1 374 200" stroke="rgba(207,134,245,.6)" stroke-width="2"/></g>
  <g class="r2"><circle cx="200" cy="200" r="140" stroke="rgba(94,230,242,.22)" stroke-width="1"/>
    <path d="M60 200 A140 140 0 0 1 200 60" stroke="rgba(94,230,242,.8)" stroke-width="2"/>
    <path d="M340 200 A140 140 0 0 1 200 340" stroke="rgba(94,230,242,.8)" stroke-width="2"/></g>
  <circle cx="200" cy="200" r="118" stroke="rgba(207,134,245,.25)" stroke-width="1"/>
</svg>'''


def build_cover():
    boot = [("다이브포드 연결", "완료"), ("머리 받침 고정", "완료"), ("감각 해상도 확인", "완료"), ("서버", "벨라트 대륙")]
    li = "".join(f'<li><span>{E(a)}</span><span class="s">{E(b)}</span></li>' for a, b in boot)
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
<meta name="theme-color" content="#05080f">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="prefetch" href="home.html">
<script>document.documentElement.className+=' js'</script>
</head>
<body>
<main class="cover">
  {img(bgd("P"), "", "bgimg", lazy=False)}
  <div class="ring">{RING}</div>
  <div class="cover-in">
    <span class="fd">FULL DIVE</span>
    <h1>ILEON</h1>
    <p class="kr">행적을 읽는 세계, 일레온</p>
    <a class="btn" href="home.html" data-enter data-mag>접속 {ARROW}</a>
  </div>
  <ol class="boot" aria-label="접속 로그">
    {li}
    <li class="final"><span>접속 위치</span><span class="s">리아텔 · 귀환석 광장</span></li>
  </ol>
  <div class="flash"></div>
</main>
<script src="assets/js/main.js"></script>
</body>
</html>'''
    write("index.html", s)


# ═════════════ 홈 ═════════════
def words(t):
    return " ".join(f'<span class="w">{E(w)}</span>' for w in t.split())


def build_home():
    feed = "".join(f'<p><span class="ch ch-{c}">[{c}]</span><span>{E(t)}</span></p>' for c, t in WORLD_LOG)
    players = [c for c in C if c["side"] == "player"]
    npcs = [c for c in C if c["side"] == "npc"]
    acc = "".join(f'''<a class="acc-i" href="char/{c["slug"]}.html" style="--i:{k}">
      {img(smp(c["code"]), c["name"])}
      <span class="acc-tx"><small>{E(c["real"])} · Lv{c["lv"]}</small><b>{E(c["name"])}</b><em><span>{E(c["hook"])}</span></em></span>
    </a>''' for k, c in enumerate(players))
    faces = "".join(f'<a href="char/{c["slug"]}.html" title="{E(c["name"])}">{img(smp(c["code"]), c["name"])}<span>{E(c["name"])}</span></a>' for c in npcs)
    statement = "다이브포드에 누우면 여명기 이후 800년의 대륙이 열린다. 그곳에서 당신은 죽어도 돌아오는 이방인이다. 정해진 이야기는 없다. 당신이 한 일이 직업이 되고, 대륙에서 벌어진 일이 곧 역사가 된다."
    s = head("home.html", TITLE)
    s += f'''<section class="hero">
  <div class="hero-bg" data-tilt>{img(bgd("RI"), "리아텔의 들판과 마을", "bgimg", lazy=False)}</div>
  <div class="wrap hero-in">
    <div class="arrive">
      <span class="sysmsg" data-rv>벨라트 대륙에 오신 것을 환영합니다.</span>
      <span class="sysmsg" data-rv style="--i:1">시작 지점: 리아텔 · 귀환석 광장</span>
    </div>
    <h1 class="title"><span class="ln" data-rv style="--i:2">벨라트 대륙</span></h1>
    <p class="sub" data-rv style="--i:3">죽어도 돌아오는 자들이 내려선 땅. 여기서 무엇을 하든, 대륙은 그걸 기억한다.</p>
    <div class="btn-row" data-rv style="--i:4">
      {cta()}
      <a class="btn ghost" href="world.html">대륙 둘러보기</a>
    </div>
  </div>
  <div class="rail" aria-label="월드 로그">
    <div class="wrap"><span class="lb"><i></i>LIVE</span><div class="feed">{feed}</div></div>
  </div>
</section>

<section class="sec statement">
  <div class="wrap">
    <p class="say-big">{words(statement)}</p>
  </div>
</section>

<section class="axes" aria-label="현실과 대륙">
  <a class="axis real" href="reality.html">
    {img(bgd("P"), "포드방")}
    <div class="tx">
      <span class="k">2047 · 대한민국</span>
      <h2>몸은 여기,<br>포드 안에</h2>
      <p>월정액과 정비비를 내고 포드에 눕는다. 로그아웃하면 저린 다리와 커뮤의 여론이 기다린다.</p>
      <span class="clk"><b data-clock="real">--:--</b><small>현실 시각</small></span>
    </div>
  </a>
  <a class="axis virt" href="world.html">
    {img(bgd("KD"), "카뎃트")}
    <div class="tx">
      <span class="k">벨라트 · 여명기 이후 800년</span>
      <h2>나는 저기,<br>대륙 위에</h2>
      <p>로그아웃해 있는 동안에도 대륙의 시간은 흐른다. 현실의 여섯 시간이 이곳의 하루다.</p>
      <span class="clk"><b data-clock="belat">--:--</b><small>벨라트 시각 · 4배속</small></span>
    </div>
  </a>
</section>

<section class="quote-band">
  <div class="qb-bg" data-par>{img(smp("F"), "베른하르트 콜")}</div>
  <div class="wrap">
    <blockquote data-rv>
      <p>“죽어도 돌아오는 자에게 검을 가르치는 건, 삽을 쥐여주는 것과 다르지 않다.”</p>
      <footer>베른하르트 콜 · 카르시온 검술 교관</footer>
    </blockquote>
    <div class="vs" data-rv style="--i:1">
      <div><b>이방인</b><p>플레이어. 죽으면 레벨이 깎인 채 귀환석에서 돌아온다.</p></div>
      <div><b>원주민</b><p>대륙에 사는 사람들. 한 번 죽으면 그걸로 끝이다.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    {lbl("HIDDEN CLASS")}
    <h2 class="h2" data-rv>당신이 한 일이 직업이 된다</h2>
    <p class="lead" data-rv style="--i:1">무엇을 반복했는지, 어디에 오래 머물렀는지, 누구와 얽혔는지. 시스템은 그걸 읽고 그 사람만을 위한 직업을 만든다. 조건은 아무도 모른다.</p>
    <div class="bento">
      <div class="b-zero spot" data-rv>
        <b data-count="0">0</b>
        <p>신화 등급 보유자<br>서비스 이래 지금까지</p>
        <div class="ladder">{"".join(f'<span class="{gk(g)}">{g}</span>' for g in GRADES)}</div>
      </div>
      {"".join(f'<div class="b-job spot" data-rv style="--i:{k + 1}"><span class="ln"><span class="ch ch-히든">[히든]</span> 새 직업이 발현되었습니다</span><b data-scramble>{E(n)}</b>{grade(g)}<p>{E(t)}</p>{f"<a class=\"who\" href=\"char/{CMAP['D' if w == '헤리몽' else 'E']['slug']}.html\">{E(w)} {ARROW}</a>" if w else ""}</div>' for k, (n, g, t, w) in enumerate(HIDDEN[:4]))}
      <div class="b-img" data-rv style="--i:2">{img(cs("E", 10), "무명")}</div>
    </div>
  </div>
</section>

<section class="sec cast">
  <div class="wrap">
    <h2 class="h2" data-rv>먼저 움직이는 사람들</h2>
    <p class="lead" data-rv style="--i:1">이방인 다섯과 원주민 열. 모두 저마다의 사정이 있고, 당신을 기다려 주지 않는다.</p>
    <div class="acc" data-rv style="--i:2">{acc}</div>
    <div class="npc-row" data-rv style="--i:3">{faces}<a class="more" href="characters.html">열다섯 명 모두 보기 {ARROW}</a></div>
  </div>
</section>

<section class="sec alt timeline-sec">
  <div class="wrap">
    {lbl("WORLD EVENT")}
    <h2 class="h2" data-rv>정해진 이야기는 없다.<br>일어난 일이 이야기가 된다.</h2>
    <p class="lead" data-rv style="--i:1">대륙 어딘가는 늘 끓고 있다. 그게 터지면 사변이다. 함락된 마을은 폐허로 남고, 국경은 다시 그어지고, 죽은 원주민은 돌아오지 않는다.</p>
    <ol class="flow" data-draw>{"".join(f'<li style="--i:{k}"><b>{k_}</b><p>{E(t)}</p></li>' for k, (k_, t) in enumerate(INCIDENT_FLOW))}</ol>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <h2 class="h2" data-rv>어디서 눈을 뜰까</h2>
    <div class="modes">
      <a class="mode m1 spot" href="start.html#newbie" data-rv>{img(bgd("RI"), "리아텔")}<div class="tx"><span class="sysmsg">리아텔 · 귀환석 광장</span><b>뉴비</b><p>Lv1, 무직. 견습 기사 유안이 덜그럭거리며 달려온다.</p></div></a>
      <a class="mode m2 spot" href="start.html#myth" data-rv style="--i:1">{img(bgd("BS"), "균열 보스룸")}<div class="tx"><span class="sysmsg">신화 등급 직업이 발현되었습니다.</span><b>신화직업</b><p>균열의 보상에, 줄리엣보다 먼저 손이 닿았다.</p></div></a>
      <a class="mode m3 spot" href="start.html#free" data-rv style="--i:2">{img(bgd("H"), "현실의 방")}<div class="tx"><span class="sysmsg">접속 위치를 선택하십시오.</span><b>자유모드</b><p>원룸의 절반을 차지한 포드. 어디로 들어갈지는 아직 정하지 않았다.</p></div></a>
    </div>
  </div>
</section>
'''
    s += close_band()
    s += foot()
    write("home.html", s)


# ═════════════ 대륙 ═════════════
def build_world():
    s = head("world.html", "대륙")
    s += phead("ER", "벨라트 대륙", "고대 마법 문명이 무너지고 800년. 새 마법은 만들어지지 않고, 사람들은 유적에서 찾아낸 옛것을 되살려 쓴다.",
               [("regions", "지역"), ("faults", "대립선"), ("threats", "위협"), ("halak", "할라크족"), ("gods", "신앙"), ("beyond", "이계")], "에르카시아")
    tabs = "".join(f'<button type="button" role="tab" aria-selected="{"true" if k == 0 else "false"}" data-r="{r["key"]}">{E(r["name"])}</button>' for k, r in enumerate(REGIONS))
    panes = ""
    for k, r in enumerate(REGIONS):
        items = []
        if r["fields"]: items.append(("사냥터", " · ".join(f'{E(n)} <em>{lv}</em>' for n, lv in r["fields"])))
        if r["dungeons"]: items.append(("던전", " · ".join(f'{E(n)} <em>{lv}</em>' for n, kk, lv in r["dungeons"])))
        if r["god"]: items.append(("신앙", E(r["god"])))
        people = "".join(f'<a class="chip" href="char/{CMAP[p]["slug"]}.html">{img(smp(p), "")}{E(CMAP[p]["name"])}</a>' for p in r["people"])
        panes += f'''<article class="rpane" id="{r["key"]}" data-r="{r["key"]}"{"" if k == 0 else " hidden"}>
  <div class="rp-img">{img(bgd(r["img"]), r["name"], lazy=k > 1)}</div>
  <div class="rp-tx">
    <span class="where">{E(r["where"])}</span>
    <h3>{E(r["name"])}</h3>
    <p>{E(r["text"])}</p>
    {rows(items) if items else ""}
    {f'<div class="people">{people}</div>' if people else ""}
  </div>
</article>
'''
    s += f'''<section class="sec" id="regions">
  <div class="wrap">
    <h2 class="h2" data-rv>제국 하나, 왕국 셋, 그리고 여섯 곳</h2>
    <p class="lead" data-rv style="--i:1">지역마다 레벨대가 이어져 있어서, 사냥터를 옮겨 가는 것 자체가 성장이 된다.</p>
    <div class="rtabs" role="tablist" aria-label="지역" data-rv style="--i:2">{tabs}</div>
    <div class="rstage" data-rv style="--i:2">{panes}</div>
  </div>
</section>

<section class="sec alt" id="faults">
  <div class="wrap">
    {lbl("FAULT LINES")}
    <h2 class="h2" data-rv>전쟁의 씨앗, 여덟 줄</h2>
    <p class="lead" data-rv style="--i:1">이 선들이 끓다가 터지면 사변이 된다. 운영사는 사변을 직접 쓰지 않는다고 말하고, 커뮤는 사변이 터질 때마다 "이거 운영 각본 아니냐"로 한 번씩 싸운다.</p>
    <div class="faults">{"".join(f'<div class="spot" data-rv style="--i:{k % 4}"><b>{E(a)}</b><p>{E(b)}</p></div>' for k, (a, b) in enumerate(FAULTS))}</div>
  </div>
</section>

<section class="sec" id="threats">
  <div class="wrap split">
    <div class="stick"><h2 class="h2" data-rv>사람 바깥에서 오는 것들</h2>
    <p class="lead" data-rv style="--i:1">전쟁이 사람 사이의 일이라면, 침공은 대륙의 바깥과 아래에서 온다.</p></div>
    <ol class="threats">{"".join(f'<li data-rv style="--i:{k}"><b>{E(a)}</b><p>{E(b)}</p></li>' for k, (a, b) in enumerate(THREATS))}</ol>
  </div>
</section>

<section class="feature-band" id="halak">
  <div class="fb-img" data-par>{img(smp("N"), "카시엘")}</div>
  <div class="wrap">
    <div class="fb-tx" data-rv>
      <h2 class="h2">이방인을 재앙이라 부르는 자들</h2>
      <p>할라크족은 고대 흑룡의 피를 이은 장수 종족이다. 검은 굽은 뿔과 금빛 눈으로 수백 년을 살고, 라흐나 침강지 가장자리 고지대에 터를 잡았다. 인간 왕국보다 먼저 이 대륙에 있었다는 자부가 강하다.</p>
      <p>그들의 군세 칼데스를 이끄는 카시엘은 이방인을 대륙에서 몰아내려 한다. 죽어도 돌아오는 이방인이 매주 봉인지를 들쑤시고, 그럴수록 봉인이 얇아진다고 보기 때문이다. 그는 이 말을 숨기지 않는다.</p>
      <a class="more" href="char/kasiel.html">카시엘 · Lv88 {ARROW}</a>
    </div>
  </div>
</section>

<section class="sec" id="gods">
  <div class="wrap">
    <h2 class="h2" data-rv>신들은 침묵하지 않는다</h2>
    <p class="lead" data-rv style="--i:1">다만 직접 내려오지도 않는다. 신탁과 축복은 반드시 신관을 거쳐 온다. 한 신전에서 신뢰를 얻으면, 다른 신전에서는 냉대를 받기도 한다.</p>
    <div class="gods">{"".join(f'<div class="spot" data-rv style="--i:{k % 3}"><b>{E(n)}</b><i>{E(k_)}</i><p>{E(t)}</p></div>' for k, (n, k_, t) in enumerate(GODS))}</div>
  </div>
</section>

<section class="band" id="beyond">
  <div class="band-bg" data-par>{img(bgd("OW"), "이계", "bgimg")}</div>
  <div class="wrap" data-rv>
    <h2>균열 너머, 이계</h2>
    <p>균열은 예고 없이 열렸다가 닫힌다. 깊은 균열 너머에는 대륙 밖의 다른 세계가 이어져 있다. 마계나 천계 같은 구분 없이, 그저 이계라고 부른다. 가장 어려운 무대다.</p>
  </div>
</section>
'''
    s += close_band()
    s += foot()
    write("world.html", s)


# ═════════════ 인물 목록 ═════════════
def build_characters():
    players = [c for c in C if c["side"] == "player"]
    s = head("characters.html", "인물")
    s += phead("T", "열다섯 사람", "이방인 다섯에게는 포드 밖의 삶이 있다. 원주민 열은 죽으면 돌아오지 않는다. 누구와든 함께 다닐 수 있지만, 원주민은 망설인다. \"넌 언젠가 안 돌아올 거잖아.\"", alt="주점")
    s += f'''<section class="sec">
  <div class="wrap">
    <div class="filters" role="tablist" aria-label="인물 거르기">
      <button type="button" role="tab" aria-selected="true" data-f="all">전체 <small>{len(C)}</small></button>
      <button type="button" role="tab" aria-selected="false" data-f="player">이방인 <small>{len(players)}</small></button>
      <button type="button" role="tab" aria-selected="false" data-f="npc">원주민 <small>{len(C) - len(players)}</small></button>
      <i class="pill" aria-hidden="true"></i>
    </div>
    <div class="cards">{"".join(card(c, i=k) for k, c in enumerate(C))}</div>
  </div>
</section>
'''
    s += close_band()
    s += foot()
    write("characters.html", s)


# ═════════════ 인물 상세 ═════════════
def build_char(i, c):
    global UP
    up = UP = "../"
    player = c["side"] == "player"
    prev_c, next_c = C[i - 1], C[(i + 1) % len(C)]
    tags = f'<span class="tag on">{"이방인" if player else "원주민"}</span><span class="tag">Lv{c["lv"]}</span>' + \
           (f'<span class="tag">{E(c["job"].split("(")[0])}</span>{grade(c["grade"])}' if c["grade"] else f'<span class="tag">{E(c["job"])}</span>')
    data = [("레벨", f"Lv{c['lv']}")]
    data.append(("직업", f'{E(c["job"])}{" · 히든" if c["hidden"] else ""}') if c["grade"] else ("역할", E(c["job"])))
    data.append(("소속", E(c["role"])))
    if player: data.append(("본명", E(c["real"])))
    data.append(("나이", f'{c["sex"]} · {c["age"]}'))
    looks = [("게임" if player else "외형", E(c["look_game"]))]
    if player: looks.append(("현실", E(c["look_real"])))
    looks.append(("말투", E(c["speech"])))
    body = "".join(f"<p>{E(p)}</p>" for p in c["body"])
    quote = f'<blockquote class="cq" data-rv>“{E(c["quote"])}”</blockquote>' if c["quote"] else ""

    def thumbs(code, labels, axis, hidden=False):
        bs = "".join(f'<button type="button" aria-pressed="{"true" if n == 1 else "false"}" data-src="{cs(code, n)}" data-alt="{E(c["name"])} {lab}">{img(cs(code, n), "")}<span>{lab}</span></button>' for n, lab in enumerate(labels, 1))
        return f'<div class="thumbs" data-axis="{axis}"{" hidden" if hidden else ""}>{bs}</div>'

    th = thumbs(c["code"], EXPR, "game")
    sw = ""
    if player:
        sw = '<div class="axis-sw" role="tablist" aria-label="게임과 현실"><button type="button" role="tab" data-axis="game" aria-selected="true">게임</button><button type="button" role="tab" data-axis="real" aria-selected="false">현실</button><i class="pill" aria-hidden="true"></i></div>'
        th += thumbs(c["code"] + "2", EXPR_REAL, "real", hidden=True)

    s = head("characters.html", c["name"], up=up, desc=f'{c["name"]}. {c["hook"]}')
    s += f'''<section class="chead">
  <div class="chead-bg" data-tilt>{img(smp(c["code"]), c["name"], "bgimg", lazy=False)}</div>
  <div class="wrap">
    <a class="back" href="../characters.html" data-rv>{BACK} 인물 목록</a>
    <h1 data-rv style="--i:1">{E(c["name"])}</h1>
    {f'<p class="real" data-rv style="--i:1">{E(c["real"])}</p>' if player else ""}
    <div class="tags" data-rv style="--i:2">{tags}</div>
    <p class="hook" data-rv style="--i:3">{E(c["hook"])}</p>
  </div>
</section>
<section class="sec">
  <div class="wrap cbody">
    <div>
      <div class="prose" data-rv>{body}</div>
      {quote}
    </div>
    <aside data-rv style="--i:1">
      {rows(data)}
      <div class="looks">{rows(looks)}</div>
    </aside>
  </div>
</section>
<section class="sec alt">
  <div class="wrap">
    <div class="viewer">
      <div class="stage">{img(cs(c["code"], 1), c["name"], "fig")}</div>
      <div class="side">
        <h2 class="h3">표정</h2>
        {sw}{th}
        <p class="hint">← → 키로도 넘길 수 있다.</p>
      </div>
    </div>
  </div>
</section>
<nav class="pn" aria-label="다른 인물">
  <a href="{prev_c["slug"]}.html">{img(smp(prev_c["code"]), "")}<span><small>이전</small><b>{E(prev_c["name"])}</b></span></a>
  <a href="{next_c["slug"]}.html">{img(smp(next_c["code"]), "")}<span><small>다음</small><b>{E(next_c["name"])}</b></span></a>
</nav>
'''
    s += foot(up)
    UP = ""
    write(f"char/{c['slug']}.html", s)


# ═════════════ 체계 ═════════════
def build_system():
    s = head("system.html", "체계")
    tiers = [("1차", "Lv10", "전직 NPC에게 받는다. 등급은 일반."),
             ("2차", "Lv40 + 실적 심사", "등급은 희귀. 이쯤 되면 길드가 영입하러 온다. 생산 계열은 레벨 대신 제작 실적으로 심사한다."),
             ("3차", "Lv60 + 시련", "등급은 에픽. 정규 루트는 여기까지다. 서버 전체에 다섯 명뿐이다."),
             ("히든", "레벨 무관", "조건을 채운 사람만. 얻는 순간 서버 로그에 직업명만 뜬다.")]
    s += phead("TR", "레벨이 아주 느리게 오르는 세계", "서버 1위가 Lv64다. 대부분은 Lv15를 넘기지 못하고 떠난다. 스탯은 힘, 민첩, 지구력, 감각 넷. 포인트를 찍는 게 아니라, 반복한 만큼 오른다.",
               [("level", "레벨"), ("class", "전직"), ("hidden", "히든직"), ("third", "3차 전직자"), ("dungeon", "던전"), ("incident", "사변"), ("quest", "퀘스트")], "훈련장")
    s += f'''<section class="sec" id="level">
  <div class="wrap">
    <h2 class="h2" data-rv>Lv1에서 Lv64까지</h2>
    <p class="lead" data-rv style="--i:1">이방인 기준이다. 대륙의 원주민 강자들은 이 상한과 상관없다. 기사단장이나 공작가, 할라크족 장로는 Lv70에서 90대이고, 랭킹 1위도 그들 앞에서는 아래다.</p>
    <div class="lvbar" data-draw>
      <div class="track" aria-hidden="true"><span style="--w:15">1-15</span><span style="--w:5" class="gap"></span><span style="--w:15">20-35</span><span style="--w:5" class="gap"></span><span style="--w:10">40-50</span><span style="--w:9">55+</span><span style="--w:5" class="top">64</span></div>
      <ol>
        <li><b>Lv1-15</b><p>절대다수가 여기서 그만둔다.</p></li>
        <li><b>Lv20-35</b><p>꾸준히 하는 사람들. 마을에서 얼굴을 알아본다.</p></li>
        <li><b>Lv40-50</b><p>상위권. 길드가 먼저 찾아온다.</p></li>
        <li><b>Lv55+</b><p>랭커.</p></li>
        <li><b>Lv64</b><p>정점. 지금은 한 명.</p></li>
      </ol>
    </div>
  </div>
</section>

<section class="sec alt" id="class">
  <div class="wrap">
    <h2 class="h2" data-rv>전직은 세 번, 그리고 히든</h2>
    <div class="steps">{"".join(f'<div class="spot{" hid" if a == "히든" else ""}" data-rv style="--i:{k}"><span class="k">{E(b)}</span><b>{E(a)}</b><p>{E(t)}</p></div>' for k, (a, b, t) in enumerate(tiers))}</div>
    <div class="split" style="margin-top:clamp(56px,7vw,88px)">
      <div data-rv><h3 class="h3">계열 아홉</h3>
      <p class="lead">정규직은 뼈대만 있다. 이름도 조건도 전부 공개돼 있어서, 공략만 보면 누구나 밟아 올라갈 수 있다.</p>
      <div class="classes">{"".join(f"<span>{E(x)}</span>" for x in CLASSES)}</div></div>
      <div data-rv style="--i:1"><h3 class="h3">정규 계보 몇 가지</h3>
      <div class="lines">{"".join("<div>" + "<i></i>".join(f'<span>{E(x)} {grade(GRADES[k])}</span>' for k, x in enumerate(ln)) + "</div>" for ln in LINES)}</div></div>
    </div>
  </div>
</section>

<section class="sec" id="hidden">
  <div class="wrap">
    {lbl("HIDDEN CLASS")}
    <h2 class="h2" data-rv>이 게임의 간판</h2>
    <p class="lead" data-rv style="--i:1">시스템이 행적을 읽고, 그 사람만을 위한 직업을 만든다. 같은 이름은 둘이 가질 수 없다. 서버 로그에는 직업명만 뜨기 때문에, 히든직이 하나 나올 때마다 커뮤는 조건을 추측하고 대개 틀린다.</p>
    <div class="hjobs">{"".join(f'<div class="spot" data-rv style="--i:{k % 3}"><b data-scramble>{E(n)}</b>{grade(g)}<p>{E(t)}</p>{f"<span class=\"who\">{E(w)}</span>" if w else ""}</div>' for k, (n, g, t, w) in enumerate(HIDDEN))}</div>
    <div class="grade-note" data-rv>
      <div class="ladder big">{"".join(f'<span class="{gk(g)}">{g}</span>' for g in GRADES)}</div>
      <p>등급은 지금의 강함이 아니라 잠재력이다. 정규 루트는 에픽에서 끝나고, 유니크부터는 히든직뿐이다. 히든직의 등급은 일반부터 신화까지 제각각이라, 조건이 까다로웠다고 등급이 높은 것도 아니다. 전설 등급은 서버에 두세 명, 신화는 아직 한 명도 없다.</p>
    </div>
  </div>
</section>

<section class="sec alt" id="third">
  <div class="wrap">
    <h2 class="h2" data-rv>서버 꼭대기의 다섯</h2>
    <p class="lead" data-rv style="--i:1">3차 전직자는 서버 전체에 다섯 명이다. 나머지 넷은 서버 로그와 커뮤의 소문으로만 오르내린다.</p>
    <ol class="third">{"".join(f'<li class="spot{" first" if k == 0 else ""}" data-rv style="--i:{k}"><span class="r">Lv{lv}</span><b>{E(n)}</b><span class="j">{E(j)} {grade("에픽")}</span><p>{E(t)}</p></li>' for k, (n, a, sx, lv, j, t) in enumerate(THIRD))}</ol>
  </div>
</section>

<section class="sec" id="dungeon">
  <div class="wrap split">
    <div class="stick"><h2 class="h2" data-rv>소굴에서 이계까지</h2>
    <p class="lead" data-rv style="--i:1">필드보스는 나오는 시각이 대강 알려져 있어서, 길드들이 시간에 맞춰 모여든다. 네임드는 일반 몬스터 자리에 아주 가끔 대신 나온다. 그건 순전히 운이다.</p></div>
    <div class="dungeons">
      <div data-rv><b>소굴</b><span>3-5인 · 반복 입장</span><p>한 시간 안쪽. 매일의 벌이.</p></div>
      <div data-rv style="--i:1"><b>유적</b><span>5-8인 · 주 1회</span><p>기믹이 있고, 스킬의 원천이 되는 고대 기록이 나온다.</p></div>
      <div data-rv style="--i:2"><b>봉인지</b><span>20인 이상 · 라흐나</span><p>제1환과 제2환은 Lv58-64. 제3환은 아직 아무도 넘지 못했다.</p></div>
      <div data-rv style="--i:3"><b>균열</b><span>무작위 · 시간 제한</span><p>예고 없이 열리고 닫힌다. 최초 돌파 보상이 걸려 있어서, 소문이 돌면 사람이 몰린다.</p></div>
      <div data-rv style="--i:4"><b>이계</b><span>균열 너머</span><p>대륙 밖. 가장 어려운 곳.</p></div>
    </div>
  </div>
</section>

<section class="sec alt timeline-sec" id="incident">
  <div class="wrap">
    {lbl("WORLD EVENT")}
    <h2 class="h2" data-rv>사변은 이렇게 흘러간다</h2>
    <p class="lead" data-rv style="--i:1">정해진 일정은 없다. 결과는 영구히 남고, 큰 사변에는 결정적인 역할을 한 이방인의 이름이 함께 기록된다.</p>
    <ol class="flow" data-draw>{"".join(f'<li style="--i:{k}"><b>{k_}</b><p>{E(t)}</p></li>' for k, (k_, t) in enumerate(INCIDENT_FLOW))}</ol>
    <div class="scale">{"".join(f'<div data-rv style="--i:{k}"><b>{k_}</b><p>{E(t)}</p></div>' for k, (k_, t) in enumerate(INCIDENT_SCALE))}</div>
    <p class="lead" data-rv>참여 방식은 자유다. 용병 계약도, 징집도, 약탈이나 밀수나 피난민 호송 같은 독자 행동도, 아예 빠지는 것도 된다. 그리고 당신의 행동이 사변을 부르기도 한다. 봉인지를 무리하게 돌면 범람이 가까워지고, 숲에서 나무를 베면 아엘린이 날을 세운다.</p>
  </div>
</section>

<section class="sec" id="quest">
  <div class="wrap split">
    <div class="stick">
      <h2 class="h2" data-rv>퀘스트는 미리 정해져 있지 않다</h2>
      <p class="lead" data-rv style="--i:1">모두 정세와 사변, 그리고 사람의 사정에서 생겨난다. 의뢰자는 자기 이익이 먼저라 보상을 깎거나 정보를 빼거나 등을 돌리기도 한다. 같은 퀘스트도 어떻게 푸느냐에 따라 결과가 갈리고, 그 결과가 다음 정세가 된다.</p>
      <div class="qbox" data-rv style="--i:2;margin-top:28px"><p class="q">퀘스트 : 견습 기사의 안내</p><p>유안을 따라 수비대 훈련장에서 기본 무기를 받고, 옛 수로의 큰쥐 5마리를 처치한다. 보상: 초심자 무기, 20골드</p><p class="opt">수락 | 거절</p></div>
    </div>
    <div class="qkinds">{"".join(f'<div data-rv style="--i:{k % 2}"><b>{E(a)}</b><p>{E(b)}</p></div>' for k, (a, b) in enumerate(QUEST_KINDS))}</div>
  </div>
</section>
'''
    s += close_band()
    s += foot()
    write("system.html", s)


# ═════════════ 현실 ═════════════
REAL_LIFE = {"A": "길드 법인 정직원", "B": "울산 공단 하청", "C": "공방 운영", "D": "공략 방송인", "E": "집 밖에 나가지 않는다"}


def build_reality():
    players = [c for c in C if c["side"] == "player"]
    faces = "".join(f'''<a class="face spot" href="char/{c["slug"]}.html" data-rv style="--i:{k}"><div class="ph">{img(smp(c["code"] + "2"), c["real"])}{img(smp(c["code"]), "", "g")}</div>
      <div class="cap"><b>{E(c["real"])}</b><span>{E(REAL_LIFE[c["code"]])}</span><small>게임에서는 {E(c["name"])}</small></div></a>''' for k, c in enumerate(players))
    s = head("reality.html", "현실")
    s += phead("CT", "2047, 대한민국", "일레온의 무대는 대륙만이 아니다. 포드에 누운 사람이 사는 이쪽도 이야기의 일부다. 일이 결판나는 곳은 아니지만, 정산하고 다음을 준비하는 곳.",
               [("pod", "다이브포드"), ("money", "돈"), ("account", "계정"), ("opinion", "여론"), ("faces", "포드 밖의 얼굴")], "2047년의 도시",
               '현실 · <span data-clock="date">2047</span> · <span data-clock="real">--:--</span>')
    s += f'''<section class="sec" id="pod">
  <div class="wrap pod">
    <div>
      <h2 class="h2" data-rv>누우면 열린다</h2>
      <p class="lead" data-rv style="--i:1">풀수면 VR, 다이브포드. 머리 받침이 천천히 내려오고, 시야가 어두워지고, 귓가에 익숙한 안내음이 깔린다.</p>
    </div>
    <div class="podgrid">
      <div class="spot" data-rv><b>등급</b><p>보급형부터 프로용까지. 등급이 갈리는 건 감각 해상도와 반응 속도, 접속 한계다. 울산강펀치는 보급형 최저가를 쓰고, 무명은 PK로 번 돈으로 프로용을 샀다.</p></div>
      <div class="spot" data-rv style="--i:1"><b>포드방</b><p>집에 포드가 없어도 괜찮다. 공용 포드방이 있다.</p></div>
      <div class="spot" data-rv style="--i:2"><b>정비</b><p>정비 기한을 넘기면 감각이 한 박자씩 늦게 따라온다.</p></div>
      <div class="spot" data-rv style="--i:3"><b>로그아웃</b><p>목이 마르고, 다리가 저리고, 시간 감각이 어긋난다. 오래 접속할수록 컨디션이 떨어지고, 자고 먹어야 돌아온다.</p></div>
    </div>
  </div>
</section>

<section class="band" id="money">
  <div class="band-bg" data-par>{img(bgd("P"), "포드방", "bgimg")}</div>
  <div class="wrap" data-rv>
    <h2>게임의 돈, 현실의 돈</h2>
    <p>월정액과 할부, 전기세와 정비비는 진짜로 빠져나간다. 골드는 환전할 수 있지만 수수료가 붙고 출금은 느리다. 그래도 이걸로 먹고사는 사람들이 있다.</p>
  </div>
</section>

<section class="sec" id="account">
  <div class="wrap split">
    <div class="stick"><h2 class="h2" data-rv>캐릭터는 하나뿐</h2>
    <p class="lead" data-rv style="--i:1">부계정은 없다. 새로 시작하려면 지금의 캐릭터를 지워야 한다. 그래서 히든직과 레벨을 쌓은 캐릭터를 버리는 일은 드물고, 커뮤에서 "캐삭"은 큰 사건이 된다. 핵이나 매크로는 존재하지 않는다.</p></div>
    <div data-rv style="--i:1">
      <pre class="info">[현실] 3월 14일 (목) 23:40
[잔고] 미정 | 다음 결제 미정
[포드] 미정
[컨디션] 양호
[관계] └─</pre>
      <p class="hint">현실 장면에서는 정보창도 이렇게 바뀐다.</p>
    </div>
  </div>
</section>

<section class="sec alt timeline-sec" id="opinion">
  <div class="wrap">
    <h2 class="h2" data-rv>커뮤는 늘 반 박자 늦고,<br>절반은 틀린다</h2>
    <p class="lead" data-rv style="--i:1">커뮤와 공략 위키, 스트림챗, 기사. 여론은 세계 안에서 쉬지 않고 돌아가고, 반드시 무언가를 바꾼다. 사냥 효율이 떨어지거나, 시세가 오르거나, 파티를 구하기 어려워진다.</p>
    <ol class="flow four" data-draw>
      <li style="--i:0"><b>감지</b><p>누군가 무언가를 봤다. 목격담 한 줄.</p></li>
      <li style="--i:1"><b>확산</b><p>커뮤와 방송을 타고 번진다.</p></li>
      <li style="--i:2"><b>변질</b><p>하지 않은 일이, 그 사람이 한 일이 된다.</p></li>
      <li style="--i:3"><b>잔향</b><p>잠잠해진 뒤에도 무언가는 남는다.</p></li>
    </ol>
  </div>
</section>

<section class="sec" id="faces">
  <div class="wrap">
    <h2 class="h2" data-rv>닉네임 아래의 사람들</h2>
    <p class="lead" data-rv style="--i:1">이방인 다섯의 현실. 그림에 마우스를 올리면 게임 속 모습이 보인다.</p>
    <div class="faces">{faces}</div>
  </div>
</section>
'''
    s += close_band(text="로그아웃해도<br>대륙은 멈추지 않는다.", sub="포드 정비 기한 확인", code="CT")
    s += foot()
    write("reality.html", s)


# ═════════════ 시작 ═════════════
def build_start():
    modes = [
        ("newbie", "뉴비", "일레온 프롤로그(뉴비).md", "리아텔 · 귀환석 광장", "Lv1 · 무직",
         "처음 대륙에 내려서는 이방인. 견습 기사 유안의 안내를 받고, 옛 수로의 큰쥐부터 잡는다. 대륙을 처음부터 천천히 밟아 가고 싶다면."),
        ("myth", "신화직업", "일레온 프롤로그(신화직업).md", "잿빛 회랑 · 균열 보스룸", "Lv1 · 신화",
         "줄리엣과 둘이서 균열의 파수꾼을 쓰러뜨렸고, 보상에 먼저 손이 닿았다. 서비스 이래 처음 나온 신화 등급 직업. 대가로 레벨은 1이 된다. 그게 어떤 직업인지는, 시작하면서 당신이 밝힌다."),
        ("free", "자유모드", "일레온 프롤로그(자유모드).md", "현실 · 원룸", "제한 없음",
         "밤 열한 시 사십 분, 포드 앞. 어디로 들어갈지, 누구로 살아갈지 정해진 게 없다. 원하는 대로 시작하면 된다."),
    ]
    s = head("start.html", "시작")
    s += phead("RI", "어디서 눈을 뜰까", "시작 모드는 세 가지다. 아래는 각 모드의 실제 첫 장면이다. 매 응답마다 배경 한 장과 함께 이런 식으로 이야기가 이어진다.",
               [("newbie", "뉴비"), ("myth", "신화직업"), ("free", "자유모드"), ("how", "플레이 방법")], "리아텔", "접속 위치를 선택하십시오.")
    for k, (key, name, fn, where, lv, desc) in enumerate(modes):
        s += f'''<section class="sec{" alt" if k % 2 else ""}" id="{key}">
  <div class="wrap modehead">
    <div class="stick">
      <span class="num" data-rv>0{k + 1}</span>
      <h2 data-rv>{E(name)}</h2>
      <p class="lead" data-rv style="--i:1">{E(desc)}</p>
      <div data-rv style="--i:2">{rows([("시작 지점", E(where)), ("시작 상태", E(lv))])}</div>
    </div>
    <div class="sample" data-rv>{render_prologue(fn)}</div>
  </div>
</section>
'''
    s += f'''<section class="sec" id="how">
  <div class="wrap">
    <h2 class="h2" data-rv>이렇게 플레이한다</h2>
    <div class="how">
      <div class="howgrid">
        <div class="spot" data-rv><code>`문장`</code><p>월드 메시지, 레벨업, 전직 같은 시스템 메시지.</p></div>
        <div class="spot" data-rv style="--i:1"><code>&gt;문장</code><p>귓속말과 길드챗, 파티챗. 풀다이브라 평소엔 목소리로 대화하고, 채팅은 거든다.</p></div>
        <div class="spot" data-rv style="--i:2"><code>!인터넷 - 내용</code><p>궁금한 걸 찾아본다. 커뮤, 위키, 방송, 기사가 원문 그대로 나온다.</p></div>
        <div class="spot" data-rv style="--i:3"><code>판정</code><p>모든 행동은 시도다. 성공, 대가를 치른 성공, 실패. 레벨이 10 이상 차이 나면 거의 일방적이다. 죽으면 레벨이 깎이고 현실로 튕겨 나온다.</p></div>
      </div>
      <div data-rv style="--i:1">
        <h3 class="h3">단축어</h3>
        {rows([(a, E(b)) for a, b in SHORTCUTS])}
      </div>
    </div>
  </div>
</section>
'''
    s += close_band()
    s += foot()
    write("start.html", s)


if __name__ == "__main__":
    build_cover(); build_home(); build_world(); build_characters()
    for i, c in enumerate(C):
        build_char(i, c)
    build_system(); build_reality(); build_start()
    print("ok:", 7 + len(C), "pages")
