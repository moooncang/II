# -*- coding: utf-8 -*-
# 일레온 사이트 생성기. 실행: python3 _build/build.py  (저장소 최상단에 html을 쓴다)
import os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = os.path.join(ROOT, "_설정")
TITLE = "FULL DIVE - ILEON"
DESC = "2047년 대한민국의 다이브포드에서, 여명기 이후 800년의 벨라트 대륙으로. 행적을 읽는 세계 「FULL DIVE - ILEON」(일레온). 문창놈의 크랙 채팅봇."
E = html.escape

NAV = [("world.html", "대륙"), ("characters.html", "인물"), ("system.html", "체계"),
       ("reality.html", "현실"), ("start.html", "시작")]

ARROW = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 8h11M9 3.5 13.5 8 9 12.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="square"/></svg>'
ARROW_S = '<svg width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 8h11M9 3.5 13.5 8 9 12.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="square"/></svg>'
MENU = '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 4h12M2 8h12M2 12h12" stroke="currentColor" stroke-width="1.6"/></svg>'


def gk(g): return GRADE_KEY.get(g, "g1")
def grade(g): return f'<span class="grade {gk(g)}">{g}</span>' if g else ""
def img(src, alt="", cls="", lazy=True, extra=""):
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy" decoding="async"' if lazy else ' decoding="async" fetchpriority="high"'
    return f'<img src="{src}" alt="{E(alt)}"{c}{l}{extra}>'


def crack_btn(label="크랙에서 접속", cls="btn"):
    if CRACK:
        return f'<a class="{cls}" href="{CRACK}" target="_blank" rel="noopener">{label} {ARROW}</a>'
    return f'<span class="{cls}" aria-disabled="true" title="크랙 작품 링크는 준비 중입니다">{label} · 준비 중</span>'


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
<meta name="theme-color" content="#eef1f3">
<link rel="preload" href="{up}assets/css/style.css" as="style">
<link rel="stylesheet" href="{up}assets/css/style.css">
<script>document.documentElement.className+=' js'</script>
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="{up}home.html"><b>ILEON</b><span>FULL DIVE</span></a>
    <button class="menu" aria-expanded="false" aria-controls="nav">{MENU} 메뉴</button>
    <ul class="nav" id="nav">
{nav}
    </ul>
    <div class="clock" aria-label="현실 시각과 벨라트 시각(4배속)">
      <span class="rt">현실 <b data-clock="real">--:--</b></span>
      <span class="bt">벨라트 <b data-clock="belat">--:--</b></span>
    </div>
  </div>
</header>
<main>
'''


def foot(up=""):
    links = " ".join(f'<a href="{up}{h}">{t}</a>' for h, t in NAV)
    return f'''</main>
<footer class="foot">
  <div class="wrap">
    <div><b>FULL DIVE - ILEON</b> · 일레온 · 문창놈의 크랙 채팅봇<br>수록 그림은 전부 생성물이며 무단 전재를 금합니다.</div>
    <nav aria-label="바닥글">{links}</nav>
  </div>
</footer>
<script src="{up}assets/js/main.js"></script>
</body>
</html>'''


def close_band(up="", text="대륙은 지금도 돌아가고 있습니다.", sub=None):
    sub = sub or ['다이브포드 연결 대기', '접속 위치 선택 — 리아텔 · 카뎃트 · 잿빛 회랑 · 라흐나']
    boot = "".join(f'<span class="sysmsg ln">{E(s)}</span><br>' for s in sub)
    return f'''<section class="close on-sys">
  <div class="wrap">
    <p class="boot typing">{boot}</p>
    <h2 class="h2">{text}</h2>
    <div class="btn-row">
      {crack_btn(cls="btn light")}
      <a class="more" href="{up}start.html">시작 모드 보기 {ARROW_S}</a>
    </div>
  </div>
</section>
'''


def pcard(c, up="", sub=None, side=True):
    sub = sub if sub is not None else c["job"]
    s = ""
    if side:
        s = '<span class="side p">이방인</span>' if c["side"] == "player" else '<span class="side">원주민</span>'
    return f'''<a class="pc" href="{up}char/{c["slug"]}.html">
  {s}<div class="ph">{img(cs(c["code"], 2), c["name"])}</div>
  <div class="cap"><span class="nm">{E(c["name"])}</span><span class="sub">{E(sub)}</span></div>
</a>'''


def write(name, s):
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
        lines = f.read().split("\n")
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
            url = m.group(1)
            if "/B/" in url:
                out.append(f'<figure class="wide">{img(url, "배경")}</figure>')
            else:
                out.append(f'<figure>{img(url, "인물")}</figure>')
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
def build_cover():
    boot = [("다이브포드 연결", "완료"), ("머리 받침 고정", "완료"), ("감각 해상도 확인", "완료"),
            ("서버", "벨라트 대륙"), ("시간비", "현실 6시간 = 게임 1일")]
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
<meta name="theme-color" content="#1b2259">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="prefetch" href="home.html">
<script>document.documentElement.className+=' js'</script>
</head>
<body>
<main class="cover">
  {img(bg("P"), "", "bgimg", lazy=False)}
  <div class="cover-in">
    <ol class="boot" aria-label="접속 로그">
      {li}
      <li class="final"><span>접속 위치</span><span class="s">리아텔 · 귀환석 광장</span></li>
    </ol>
    <div>
      <h1><span class="fd">FULL DIVE</span>ILEON<span class="kr">일레온 — 행적을 읽는 세계</span></h1>
      <div class="enter">
        <a class="btn light" href="home.html" data-enter>접속 {ARROW}</a>
        <p class="note">2047년 대한민국, 다이브포드에 누우면<br>여명기 이후 800년의 벨라트 대륙이 열립니다.</p>
      </div>
    </div>
    <p class="by">문창놈 · 크랙 채팅봇 · 수록 그림은 전부 생성물입니다</p>
  </div>
  <div class="flash"></div>
</main>
<script src="assets/js/main.js"></script>
</body>
</html>'''
    write("index.html", s)


# ═════════════ 홈 ═════════════
def build_home():
    feed = "".join(f'<p><span class="ch ch-{c}">[{c}]</span><span>{E(t)}</span></p>' for c, t in WORLD_LOG)
    s = head("home.html", TITLE)
    s += f'''<section class="hero">
  {img(bg("RI"), "리아텔 귀환석 광장", "bgimg", lazy=False)}
  <div class="wrap hero-in">
    <div class="arrive typing">
      <span class="sysmsg ln">벨라트 대륙에 오신 것을 환영합니다.</span>
      <span class="sysmsg ln">시작 지점: 리아텔 · 귀환석 광장</span>
    </div>
    <h1 class="title">벨라트 대륙<small>여명기 이후 800년. 고대 마법 문명이 무너진 땅에, 죽어도 돌아오는 자들이 내려섰다.</small></h1>
    <div class="btn-row">
      <a class="btn light" href="start.html">시작 모드 고르기 {ARROW}</a>
      {crack_btn(cls="btn")}
    </div>
  </div>
  <div class="rail on-sys" aria-label="월드 로그">
    <div class="wrap"><span class="lbl"><i></i>월드 로그</span><div class="feed">{feed}</div></div>
  </div>
</section>

<section class="axes" aria-label="두 개의 축">
  <a class="axis real" href="reality.html">
    {img(bg("P"), "포드방")}
    <span class="when">현실 · <span data-clock="date">2047</span></span>
    <h2 class="big">몸은 여기,<br>포드 안에.</h2>
    <p>2047년 대한민국. 월정액과 할부, 전기세와 정비비를 내고 다이브포드에 눕는다. 로그아웃하면 저린 다리와 커뮤의 여론이 기다린다.</p>
    <p class="clockbig"><small>현실 시각</small><span data-clock="real">--:--</span></p>
  </a>
  <a class="axis virt" href="world.html">
    {img(bg("KD"), "카뎃트")}
    <span class="when">게임 · 벨라트 대륙</span>
    <h2 class="big">나는 저기,<br>대륙 위에.</h2>
    <p>제국 하나, 왕국 셋, 자유도시와 무법 지대와 엘프의 숲. 로그아웃해 있는 동안에도 대륙의 시간은 똑같이 흐른다.</p>
    <p class="clockbig"><small>벨라트 시각</small><span data-clock="belat">--:--</span></p>
  </a>
</section>
<p class="ratio">시간비 <b>4 : 1</b> — 현실 6시간이 게임 하루. 위의 두 시계는 그 비율로 함께 갑니다.</p>

<section class="sec">
  <div class="wrap vs">
    <figure class="rv">{img(cs("F", 1), "베른하르트 콜")}<figcaption>베른하르트 콜 · Lv71 · 원주민</figcaption></figure>
    <div class="rv">
      <p class="say">“죽어도 돌아오는 자에게 검을 가르치는 건 삽을 쥐여주는 것과 다르지 않다.”<span class="who">카르시온 검술 교관</span></p>
      <ul class="log facts">
        <li><span class="ch ch-월드">[이방인]</span><span class="t">플레이어. 죽으면 레벨이 깎이고 귀환석에서 돌아온다.</span></li>
        <li><span class="ch ch-정세">[원주민]</span><span class="t">대륙에 사는 사람들. 죽으면 끝이다. 등록된 인물도 예외가 없다.</span></li>
        <li><span class="ch ch-사변">[전쟁]</span><span class="t">원주민 군대는 이방인을 '돌아오는 병력'으로 쓴다. 같은 참호에서 한쪽만 돌아온다.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap hidden-grid">
    <div class="rv">
      <h2 class="h2">행적이<br>직업이 된다.</h2>
      <p class="lead">무엇을 반복했는지, 어디에 오래 머물렀는지, 누구와 얽혔는지. 시스템이 그 사람의 행적을 읽고 그 사람만을 위한 히든직을 만든다. 조건은 공개되지 않고, 같은 이름은 둘이 가질 수 없다.</p>
      <div class="ladder" aria-label="직업 등급">{"".join(f'<span class="{gk(g)}" style="--gc:var(--{gk(g)})">{g}</span>' for g in GRADES)}</div>
      <p class="zero" aria-label="신화 등급 보유자 0명">0</p>
      <p class="zero-cap">신화 등급 보유자 · 서비스 이래</p>
    </div>
    <ul class="jobs rv">
      {"".join(f"""<li><span class="log-line"><span class="ch ch-히든">[히든]</span> 서버에 새 직업이 발현되었습니다</span><span class="n">{E(n)} {grade(g)}</span><span class="who">{E(w)}</span><p>{E(t)}</p></li>""" for n, g, t, w in HIDDEN[:4])}
    </ul>
  </div>
  <div class="wrap" style="margin-top:28px"><a class="more" href="system.html#hidden">직업과 등급 {ARROW_S}</a></div>
</section>

<section class="sec tight" style="padding-left:0;padding-right:0">
  <div class="wrap head-row">
    <div><h2 class="h2">접속 중인 열다섯 사람</h2>
    <p class="lead">이방인 다섯, 원주민 열. 각자 자기 사정으로 움직이고, 당신보다 먼저 움직인다.</p></div>
    <a class="more" href="characters.html">전원 보기 {ARROW_S}</a>
  </div>
  <div class="who-strip">
    {"".join(pcard(c) for c in C)}
  </div>
</section>

<section class="sec sysband on-sys">
  <div class="wrap">
    <h2 class="h2">메인 스토리는 없다.<br>일어난 일이 스토리가 된다.</h2>
    <p class="lead">정세가 끓다가 터지면 사변이 된다. 전쟁, 침공, 재해, 정변. 함락된 마을은 폐허로 남고, 국경은 바뀌고, 죽은 원주민은 돌아오지 않는다. 공략 위키는 늘 반 박자 늦는다.</p>
    <ol class="flow">
      {"".join(f'<li><span class="k">{k}</span><p>{E(t)}</p></li>' for k, t in INCIDENT_FLOW)}
    </ol>
    <p style="margin-top:36px"><a class="more" href="system.html#incident">사변과 퀘스트 {ARROW_S}</a></p>
  </div>
</section>

<section class="sec">
  <div class="wrap head-row"><div><h2 class="h2">어디서 눈을 뜰까</h2>
  <p class="lead">시작 모드는 셋. 처음 내려서는 뉴비, 서버 최초의 신화 직업, 그리고 아무것도 정하지 않은 자유 모드.</p></div></div>
  <div class="wrap modes">
    <a class="mode" href="start.html#newbie">{img(bg("RI"), "리아텔")}<span class="sysmsg">시작 지점: 리아텔 · 귀환석 광장</span><span class="nm">뉴비</span><p>Lv1, 무직. 견습 기사 유안이 덜그럭거리며 다가온다.</p><span class="go">프롤로그 읽기 {ARROW_S}</span></a>
    <a class="mode" href="start.html#myth">{img(bg("BS"), "균열 보스룸")}<span class="sysmsg">신화 등급 직업이 발현되었습니다.</span><span class="nm">신화직업</span><p>잿빛 회랑의 균열 보스룸. 줄리엣보다 먼저 손이 닿았다.</p><span class="go">프롤로그 읽기 {ARROW_S}</span></a>
    <a class="mode" href="start.html#free">{img(bg("H"), "현실의 방")}<span class="sysmsg">접속 위치를 선택하십시오.</span><span class="nm">자유모드</span><p>밤 열한 시 사십 분, 원룸의 절반을 차지한 포드. 어디로 들어갈지는 아직.</p><span class="go">프롤로그 읽기 {ARROW_S}</span></a>
  </div>
</section>
'''
    s += close_band()
    s += foot()
    write("home.html", s)


# ═════════════ 대륙 ═════════════
def build_world():
    s = head("world.html", "대륙")
    s += f'''<section class="phead">
  {img(bg("KD"), "카뎃트", lazy=False)}
  <div class="wrap">
    <span class="sysmsg">서버: 벨라트 대륙 · 여명기 이후 800년</span>
    <h1>벨라트 대륙</h1>
    <p>고대 마법 문명이 무너지고 800년. 마법은 새로 만들지 못하고, 유적에서 나온 고대의 것을 되살려 쓴다. 대륙 어딘가는 늘 끓고 있다.</p>
  </div>
</section>
<nav class="toc" aria-label="이 페이지"><div class="wrap">
  <a href="#regions">지역</a><a href="#faults">대립선</a><a href="#threats">위협원</a><a href="#halak">할라크족과 칼데스</a><a href="#gods">신앙</a><a href="#beyond">이계</a>
</div></nav>

<section class="sec" id="regions">
  <div class="wrap">
    <div class="head-row"><div><h2 class="h2">제국 하나, 왕국 셋, 그리고 여섯 곳</h2>
    <p class="lead">지역마다 레벨대가 이어져 있어서, 사냥터를 옮기는 것 자체가 진행이 된다. 종족은 인간, 드워프, 엘프, 유목민, 그리고 할라크족.</p></div></div>
'''
    for r in REGIONS:
        fields = "".join(f'<span>{E(n)} {lv}</span>' for n, lv in r["fields"])
        dung = "".join(f'<span>{E(n)} ({E(k)}) {lv}</span>' for n, k, lv in r["dungeons"])
        rows = ""
        if fields: rows += f"<dt>사냥터</dt><dd>{fields}</dd>"
        if dung: rows += f"<dt>던전</dt><dd>{dung}</dd>"
        if r["god"]: rows += f"<dt>신앙</dt><dd>{E(r['god'])}</dd>"
        people = "".join(
            f'<a class="chip" href="char/{CMAP[p]["slug"]}.html">{img(cs(p, 2), "")}{E(CMAP[p]["name"])}</a>' for p in r["people"])
        s += f'''    <article class="region rv" id="{r["key"]}">
      <div class="rimg">{img(bg(r["img"]), r["name"])}<span class="where">{E(r["where"])}</span></div>
      <div class="rbody">
        <h3>{E(r["name"])}</h3>
        <p>{E(r["text"])}</p>
        {f'<dl class="rdata">{rows}</dl>' if rows else ""}
        {f'<div class="rpeople">{people}</div>' if people else ""}
      </div>
    </article>
'''
    s += f'''  </div>
</section>

<section class="sec sysband on-sys" id="faults">
  <div class="wrap split">
    <div class="stick"><h2 class="h2">전쟁의 씨앗, 여덟 줄</h2>
    <p class="lead">대립선이 끓다가 터지면 사변이 된다. 운영사는 사변을 직접 쓰지 않는다고 홍보한다. 대륙이 알아서 만든다는 것. 그래서 사변이 터질 때마다 커뮤는 "이거 운영 각본이냐 아니냐"로 한 번씩 싸운다.</p></div>
    <ul class="rows">
      {"".join(f'<li><b>{E(a)}</b><p>{E(b)}</p></li>' for a, b in FAULTS)}
    </ul>
  </div>
</section>

<section class="sec" id="threats">
  <div class="wrap split">
    <div class="stick"><h2 class="h2">침공의 근원</h2>
    <p class="lead">전쟁이 사람 사이의 일이라면, 이쪽은 대륙 바깥과 아래에서 온다.</p></div>
    <ul class="rows">
      {"".join(f'<li><b>{E(a)}</b><p>{E(b)}</p></li>' for a, b in THREATS)}
    </ul>
  </div>
</section>

<section class="plate" id="halak">
  {img(cs("N", 1), "카시엘")}
  <div class="wrap">
    <h2 class="h2" style="color:#fff">할라크족과 칼데스</h2>
    <p class="lead" style="max-width:34em">고대 흑룡의 피를 이은 장수 종족. 검은 굽은 뿔과 용의 금안을 지니고 수백 년을 산다. 인간 왕국보다 먼저 대륙에 있었다는 자부가 강하고, 라흐나 침강지 가장자리 고지대에 산다. 칼데스는 카시엘이 이끄는 그들의 군세다. 목적은 하나, 이방인을 대륙에서 몰아내는 것.</p>
    <p class="lead" style="max-width:34em">이방인은 죽어도 돌아오니 같은 봉인지를 주마다 들쑤신다. 그럴수록 봉인이 얇아진다. 카시엘이 이방인을 재앙이라 부르는 건 증오가 아니라 이 계산 때문이고, 본인이 대놓고 하는 말이다. 레이드라는 게임 행위가 곧바로 대륙의 정세로 이어진다.</p>
    <p style="margin-top:24px"><a class="more" href="char/kasiel.html" style="color:var(--sys-hi)">카시엘 · Lv88 {ARROW_S}</a></p>
  </div>
</section>

<section class="sec" id="gods">
  <div class="wrap">
    <div class="head-row"><div><h2 class="h2">신들은 침묵하지 않는다</h2>
    <p class="lead">다만 땅에 내려오지도 않는다. 신탁과 축복은 반드시 신전의 신관을 거쳐서 온다. 한 신의 신관에게 신뢰를 얻으면 다른 신전에서 냉대받는 일도 있다.</p></div></div>
    <div class="gods">
      {"".join(f'<div class="rv"><b>{E(n)}</b><i>{E(k)}</i><p>{E(t)}</p></div>' for n, k, t in GODS)}
    </div>
  </div>
</section>

<section class="plate" id="beyond">
  {img(bg("OW"), "이계")}
  <div class="wrap">
    <h2 class="h2" style="color:#fff">균열 너머, 이계</h2>
    <p class="lead" style="max-width:32em">균열은 예고 없이 열리고 일정 시간 뒤 닫힌다. 깊은 균열 너머에는 다른 세계가 이어져 있다. 마계나 천계 같은 구분 없이 하나의 '이계'로 부른다. 벨라트 대륙 밖, 최고 난도의 무대.</p>
  </div>
</section>
'''
    s += close_band()
    s += foot()
    write("world.html", s)


# ═════════════ 인물 목록 ═════════════
def roster_card(c):
    lvl = f'Lv{c["lv"]}'
    g = grade(c["grade"]) if c["grade"] else ""
    tag = '<span class="side p">이방인</span>' if c["side"] == "player" else '<span class="side">원주민</span>'
    sub = c["real"] if c.get("real") else c["role"].split(" · ")[0]
    return f'''<a class="pc rv" href="char/{c["slug"]}.html">
  {tag}<div class="ph">{img(cs(c["code"], 2), c["name"])}</div>
  <div class="cap"><span class="nm">{E(c["name"])}</span><span class="sub">{E(sub)} · {c["sex"]}{c["age"]}</span>
  <span class="lvl">{lvl} · {E(c["job"].split("(")[0])} {g}</span></div>
</a>'''


def build_characters():
    players = [c for c in C if c["side"] == "player"]
    npcs = [c for c in C if c["side"] == "npc"]
    s = head("characters.html", "인물")
    s += f'''<section class="phead">
  {img(bg("T"), "주점", lazy=False)}
  <div class="wrap">
    <span class="sysmsg">/접속자 — 등록 인물 15</span>
    <h1>열다섯 사람</h1>
    <p>이방인 다섯은 게임 밖에도 삶이 있다. 원주민 열은 죽으면 돌아오지 않는다. 누구나 동행할 수 있고, 원주민과는 신전에서 서약해 결혼할 수도 있다. 다만 원주민은 망설인다. "넌 언젠가 안 돌아올 거잖아."</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="group-h"><h2 class="h2">이방인</h2><p>플레이어 다섯. 닉네임 아래에 본명과 현실의 얼굴이 있다.</p></div>
    <div class="roster">{"".join(roster_card(c) for c in players)}</div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="group-h"><h2 class="h2">원주민</h2><p>NPC 열. 대륙의 강자들은 랭킹 1위보다 레벨이 높다. 이방인이 그들을 "넘는" 게 아니라, 대륙에는 원래 그런 사람들이 있다.</p></div>
    <div class="roster npc">{"".join(roster_card(c) for c in npcs)}</div>
  </div>
</section>
'''
    s += close_band()
    s += foot()
    write("characters.html", s)


# ═════════════ 인물 상세 ═════════════
def build_char(i, c):
    up = "../"
    player = c["side"] == "player"
    prev_c, next_c = C[i - 1], C[(i + 1) % len(C)]
    bgp = bg(c["place"]) if c.get("place") else ""
    stat = f'<dt>레벨</dt><dd>Lv{c["lv"]}</dd>'
    if c["grade"]:
        stat += f'<dt>직업</dt><dd>{E(c["job"])} {grade(c["grade"])}{" · 히든" if c["hidden"] else ""}</dd>'
    else:
        stat += f'<dt>역할</dt><dd>{E(c["job"])}</dd>'
    stat += f'<dt>소속</dt><dd>{E(c["role"])}</dd><dt>나이</dt><dd>{c["sex"]} {c["age"]}</dd>'
    body = "".join(f"<p>{E(p)}</p>" for p in c["body"])
    looks = f'<p><b>{"게임" if player else "외형"}</b>{E(c["look_game"])}</p>'
    if player:
        looks += f'<p><b>현실</b>{E(c["look_real"])}</p>'
    looks += f'<p><b>말투</b>{E(c["speech"])}</p>'
    quote = f'<p class="quote">{E(c["quote"])}</p>' if c["quote"] else ""

    def thumbs(code, labels, axis, hidden=False):
        bs = []
        for n, lab in enumerate(labels, 1):
            on = "true" if n == 1 else "false"
            bs.append(f'<button type="button" aria-pressed="{on}" data-src="{cs(code, n)}" data-alt="{E(c["name"])} {lab}">'
                      f'{img(cs(code, n), "")}<span>{lab}</span></button>')
        h = " hidden" if hidden else ""
        return f'<div class="thumbs" data-axis="{axis}"{h}>{"".join(bs)}</div>'

    sw = ""
    th = thumbs(c["code"], EXPR, "game")
    if player:
        sw = '<div class="axis-sw" role="group" aria-label="게임과 현실"><button type="button" data-axis="game" aria-pressed="true">게임</button><button type="button" data-axis="real" aria-pressed="false">현실</button></div>'
        th += thumbs(c["code"] + "2", EXPR_REAL, "real", hidden=True)

    real = f'<p class="realname">본명 {E(c["real"])}</p>' if player else ""
    tagtxt = "게임 · 벨라트 대륙" if player else "원주민 · 벨라트 대륙"
    sysline = (f'{E(c["name"])} 님이 접속 중입니다.' if player else f'{E(c["name"])} — 원주민. 사망 시 돌아오지 않습니다.')

    s = head("characters.html", c["name"], up=up, desc=f'{c["name"]} — {c["hook"]}')
    s += f'''<section class="cd">
  <div class="cd-art">
    {img(bgp, "", "bgplace") if bgp else ""}
    {img(cs(c["code"], 1), c["name"] + " 첫등장", "fig", lazy=False)}
    <span class="sysmsg axis-tag">{tagtxt}</span>
  </div>
  <div class="cd-body">
    <span class="sysmsg">{sysline}</span>
    <h1>{E(c["name"])}</h1>
    {real}
    <p class="hook">{E(c["hook"])}</p>
    <dl class="stat">{stat}</dl>
    <div class="prose">{body}</div>
    {quote}
    <div class="looks">{looks}</div>
  </div>
</section>
<section class="expr" aria-label="표정">
  <div class="wrap">
    <div class="expr-h"><h2>표정 · {len(EXPR)}종{" / 현실 10종" if player else ""}</h2>{sw}</div>
    {th}
  </div>
</section>
<nav class="pn" aria-label="다른 인물">
  <a href="{prev_c["slug"]}.html"><small>이전</small><b>{E(prev_c["name"])}</b></a>
  <a href="{next_c["slug"]}.html"><small>다음</small><b>{E(next_c["name"])}</b></a>
</nav>
'''
    s += foot(up)
    write(f"char/{c['slug']}.html", s)


# ═════════════ 체계 ═════════════
def build_system():
    s = head("system.html", "체계")
    tiers = [("1차", "Lv10", "전직 NPC가 부여한다. 등급 일반.", ""),
             ("2차", "Lv40 + 실적 심사", "등급 희귀. 2차 전직자는 길드가 영입하러 온다. 생산 계열은 레벨이 아니라 제작 실적으로 심사한다.", ""),
             ("3차", "Lv60 + 시련 통과", "등급 에픽. 정규 루트는 여기서 끝난다. 서버 전체에 5명.", ""),
             ("히든", "레벨 무관", "조건을 채운 사람만. 취득하면 서버 공개 로그에 직업명만 뜬다.", "h")]
    s += f'''<section class="phead">
  {img(bg("TR"), "훈련장", lazy=False)}
  <div class="wrap">
    <span class="sysmsg">랭킹 1위 · Lv64</span>
    <h1>레벨이 아주 안 오르는 게임</h1>
    <p>서버 1위가 Lv64. 대부분은 Lv15 안쪽에서 접는다. 이 전제가 나머지를 전부 정한다. 스탯은 힘·민첩·지구력·감각 넷이고, 포인트를 나눠 주는 게 아니라 반복한 행동으로 오른다.</p>
  </div>
</section>
<nav class="toc" aria-label="이 페이지"><div class="wrap">
  <a href="#level">레벨</a><a href="#class">전직</a><a href="#hidden">히든직</a><a href="#third">3차 전직자</a><a href="#dungeon">던전</a><a href="#incident">사변</a><a href="#quest">퀘스트</a>
</div></nav>

<section class="sec" id="level">
  <div class="wrap">
    <h2 class="h2">레벨 분포</h2>
    <p class="lead">이방인 기준이다. 원주민 강자는 이 상한과 무관하다. 기사단장, 공작가, 할라크족 장로 같은 이들은 Lv70~90대이고, 랭킹 1위도 그들 앞에서는 아래다.</p>
    <div class="lvbar rv">
      <div class="track" aria-hidden="true"><span>1–15</span><span class="gap"></span><span>20–35</span><span class="gap"></span><span>40–50</span><span>55+</span><span class="top">64</span></div>
      <div class="ticks" aria-hidden="true"><span>Lv1</span><span>Lv64</span></div>
      <ol>
        <li><b>Lv1–15</b><p>전체 유저의 절대다수. 여기서 접는다.</p></li>
        <li><b>Lv20–35</b><p>꾸준히 하는 층. 마을에서 알아본다.</p></li>
        <li><b>Lv40–50</b><p>상위권. 2차 전직자는 길드가 영입하러 온다.</p></li>
        <li><b>Lv55+</b><p>랭커권.</p></li>
        <li><b>Lv64</b><p>정점. 현재 1명.</p></li>
      </ol>
    </div>
  </div>
</section>

<section class="sec" id="class">
  <div class="wrap">
    <h2 class="h2">전직은 세 번, 그리고 히든</h2>
    <ul class="tiers">
      {"".join(f'<li class="{h}"><span class="k">{E(b)}</span><b>{E(a)}</b><p>{E(t)}</p></li>' for a, b, t, h in tiers)}
    </ul>
    <div class="split" style="margin-top:clamp(48px,6vw,80px)">
      <div><h3 class="h3">계열 아홉</h3>
      <p class="lead" style="margin-top:12px">정규직은 뼈대만 있다. 이름과 조건이 전부 공개돼 있어 공략만 보면 누구나 밟아 올라갈 수 있다.</p>
      <div class="classes">{"".join(f"<span>{E(x)}</span>" for x in CLASSES)}</div></div>
      <div><h3 class="h3">정규 계보 예시</h3>
      <div class="lines">{"".join("<div>" + f" {ARROW_S} ".join(f'<span>{E(x)}</span> {grade(GRADES[k])}' for k, x in enumerate(ln)) + "</div>" for ln in LINES)}</div>
      <p class="cap-note">전부는 아니다.</p></div>
    </div>
  </div>
</section>

<section class="sec sysband on-sys" id="hidden">
  <div class="wrap split">
    <div class="stick">
      <h2 class="h2">히든직</h2>
      <p class="lead">이 게임의 간판이고, 사람들이 붙어 있는 이유다. 시스템이 행적을 읽고 그 사람만을 위한 직업을 만든다. 같은 이름의 히든직을 둘이 가질 수 없다.</p>
      <p class="lead">취득하면 서버 로그에 직업명만 뜨고 조건은 뜨지 않는다. 그래서 히든직이 하나 나올 때마다 커뮤가 조건을 추측하고, 대부분 틀린다.</p>
    </div>
    <div>
      <ul class="rows">
        {"".join(f'<li><b>{E(n)}<small>{E(w) if w else "히든직 예시"}</small></b><p>{grade(g)} {E(t)}</p></li>' for n, g, t, w in HIDDEN)}
      </ul>
    </div>
  </div>
</section>

<section class="sec" id="grade">
  <div class="wrap split">
    <div class="stick"><h2 class="h2">등급은 잠재력이다</h2>
    <p class="lead">일반 &lt; 희귀 &lt; 에픽 &lt; 유니크 &lt; 전설 &lt; 신화. 성장 상한과 스킬 계보의 희소성이지, 지금 당장의 강함이 아니다. 전설 등급을 Lv20에 얻어도 Lv64 에픽을 이기지 못한다.</p></div>
    <ul class="rows">
      <li><b>{grade("일반")} {grade("희귀")} {grade("에픽")}</b><p>정규 루트의 1차·2차·3차. 유니크 위로는 정규 루트에 아예 없다.</p></li>
      <li><b>{grade("유니크")}</b><p>히든직부터. 히든직의 등급은 일반부터 신화까지 흩어져 있고, 조건이 까다로웠다고 등급이 높은 것도 아니다. 히든직을 얻었다고 좋아했다가 일반 등급인 걸 확인하고 하소연하는 게 흔한 풍경이다.</p></li>
      <li><b>{grade("전설")}</b><p>서버에 두세 명.</p></li>
      <li><b>{grade("신화")}</b><p>서비스 이래 한 번도 나온 적이 없다. 존재한다는 것 자체가 추측이다.</p></li>
    </ul>
  </div>
</section>

<section class="sec sysband on-sys" id="third">
  <div class="wrap">
    <h2 class="h2">3차 전직자, 서버 전체 5명</h2>
    <p class="lead">1위 줄리엣만 직접 등장한다. 나머지 넷은 서버 로그와 커뮤와 소문으로만 오르내린다. 대륙 최상단이 비어 있지 않다.</p>
    <ol class="third">
      {"".join(f'<li><span class="r">{"랭킹 1위 · " if k == 0 else "3차 · "}Lv{lv}</span><b>{E(n)}</b><span class="j">{E(j)} · {sx}{a}</span><p>{E(t)}</p></li>' for k, (n, a, sx, lv, j, t) in enumerate(THIRD))}
    </ol>
  </div>
</section>

<section class="sec" id="dungeon">
  <div class="wrap split">
    <div class="stick"><h2 class="h2">던전</h2>
    <p class="lead">필드보스는 주기적으로 나오고 시각이 대략 알려져 있어 길드들이 시간을 맞춰 모인다. 네임드는 낮은 확률로 일반 몬스터 자리에 대신 나온다. 순전히 운이다.</p></div>
    <ul class="rows">
      <li><b>소굴<small>3–5인 · 반복</small></b><p>1시간 안짝. 일상적인 수입원.</p></li>
      <li><b>유적<small>5–8인 · 주 1회</small></b><p>기믹이 있다. 고대 기록이 나오고, 그게 스킬의 공급원이 된다.</p></li>
      <li><b>봉인지<small>레이드 · 20인 이상</small></b><p>라흐나에만 있다. 제1환·제2환 58–64. 제3환은 미돌파.</p></li>
      <li><b>균열<small>무작위 · 시간 제한</small></b><p>예고 없이 열리고 일정 시간 뒤 닫힌다. 최초 돌파 보상이 붙어 소문이 돌면 사람이 몰린다.</p></li>
      <li><b>이계<small>균열 너머</small></b><p>벨라트 대륙 밖, 최고 난도.</p></li>
    </ul>
  </div>
</section>

<section class="sec sysband on-sys" id="incident">
  <div class="wrap">
    <h2 class="h2">사변</h2>
    <p class="lead">정세가 터진 것. 정해진 일정 없이 터진다. 결과는 영구이고, 큰 사변은 대륙 연대기에 기록되며 결정적인 기여를 한 이방인의 이름이 함께 남는다. 커뮤에서는 "연대기 등재"라고 부른다.</p>
    <ol class="flow">
      {"".join(f'<li><span class="k">{k}</span><p>{E(t)}</p></li>' for k, t in INCIDENT_FLOW)}
    </ol>
  </div>
</section>
<section class="sec tight">
  <div class="wrap">
    <h3 class="h3">규모</h3>
    <div class="scale">{"".join(f'<div><b>{k}</b><p>{E(t)}</p></div>' for k, t in INCIDENT_SCALE)}</div>
    <p class="lead">참여는 자유다. 진영과 용병 계약, 징집, 약탈·밀수·피난민 호송 같은 독자 행동, 혹은 불참. 이방인의 행동이 사변을 부르기도 한다. 봉인지를 무리하게 돌면 범람이 가까워지고, 숲에서 벌목하면 아엘린이 날을 세운다.</p>
  </div>
</section>

<section class="sec" id="quest">
  <div class="wrap split">
    <div class="stick">
      <h2 class="h2">고정된 퀘스트 목록은 없다</h2>
      <p class="lead">전부 정세와 사변, 사람의 사정에서 만들어진다. 의뢰자는 자기 이익이 먼저라 보상을 깎거나, 정보를 빼먹거나, 등을 돌릴 수 있다. 같은 퀘스트도 푸는 방식에 따라 결과가 갈리고, 그 결과가 다음 정세가 된다.</p>
      <div class="sample" style="margin-top:28px">
        <div class="qbox"><p class="q">퀘스트 : 견습 기사의 안내</p><p>유안을 따라 수비대 훈련장에서 기본 무기를 받고, 옛 수로의 큰쥐 5마리를 처치한다. 보상: 초심자 무기, 20골드</p><p class="opt">수락 | 거절</p></div>
      </div>
      <p class="cap-note">퀘스트창 견본 · 뉴비 프롤로그에서</p>
    </div>
    <ul class="rows">
      {"".join(f'<li><b>{E(a)}</b><p>{E(b)}</p></li>' for a, b in QUEST_KINDS)}
    </ul>
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
    faces = "".join(f'''<a href="char/{c["slug"]}.html"><div class="ph">{img(cs(c["code"] + "2", 2), c["real"])}{img(cs(c["code"], 2), "", "g")}</div>
      <div class="cap"><b>{E(c["real"])}</b><span>{E(c["name"])} · {E(REAL_LIFE[c["code"]])}</span></div></a>''' for c in players)
    s = head("reality.html", "현실")
    s += f'''<section class="phead real">
  {img(bg("CT"), "2047년의 도시", lazy=False)}
  <div class="wrap">
    <span class="sysmsg">현실 · <span data-clock="date">2047</span> · <span data-clock="real">--:--</span></span>
    <h1>2047, 대한민국</h1>
    <p>일레온의 정식 무대는 두 개다. 대륙만이 아니라, 포드에 누운 사람이 사는 이쪽도. 현실은 사건을 결판내는 곳이 아니라, 정산하고 준비하는 곳이다.</p>
  </div>
</section>
<nav class="toc" aria-label="이 페이지"><div class="wrap">
  <a href="#pod">다이브포드</a><a href="#money">돈</a><a href="#account">계정</a><a href="#opinion">여론</a><a href="#faces">포드 밖의 얼굴</a>
</div></nav>

<section class="sec" id="pod">
  <div class="wrap split">
    <div class="stick"><h2 class="h2">다이브포드</h2>
    <p class="lead">풀수면 VR. 누우면 머리 받침이 내려오고, 시야가 어두워지고, 귓가에 익숙한 안내음이 깔린다.</p></div>
    <ul class="rows">
      <li><b>등급<small>보급형 ~ 프로용</small></b><p>등급 차이는 감각 해상도, 반응 지연, 접속 한계로 드러난다. 울산강펀치는 보급형 최저가를 쓰고, 무명은 PK로 번 돈으로 프로용을 샀다.</p></li>
      <li><b>포드방<small>공용 시설</small></b><p>포드방은 공용 시설이다. 집에 포드가 없어도 일레온에 들어갈 수 있다.</p></li>
      <li><b>정비<small>기한</small></b><p>정비 기한을 넘기면 감각이 늦게 따라온다.</p></li>
      <li><b>이탈<small>로그아웃</small></b><p>탈수, 저린 다리, 시간 감각의 오차. 연속 접속이 쌓이면 컨디션이 떨어지고, 자고 먹어야 돌아온다.</p></li>
    </ul>
  </div>
</section>

<section class="plate" id="money">
  {img(bg("P"), "포드방")}
  <div class="wrap">
    <h2 class="h2" style="color:#fff">게임 돈과 현실 돈</h2>
    <p class="lead" style="max-width:32em">월정액, 할부, 전기세, 정비비는 실제로 나간다. 골드는 환전할 수 있지만 수수료가 붙고 출금은 늦다. 이걸로 먹고사는 층이 있다. 현실의 돈과 게임 속 선택은 같은 대가 구조로 묶여 있다.</p>
  </div>
</section>

<section class="sec" id="account">
  <div class="wrap split">
    <div class="stick"><h2 class="h2">1인 1계정</h2>
    <p class="lead">부계정은 만들 수 없다. 새로 시작하려면 지금 캐릭터를 지워야 한다. 핵과 매크로는 존재하지 않는다.</p></div>
    <div class="prose" style="font-size:17px;color:var(--ink-2)">
      <p>그래서 히든직과 레벨을 쌓은 캐릭터를 버리는 일은 드물다. 커뮤에서 "캐삭"은 큰 사건이다.</p>
      <p>운영사가 하는 일은 점검, 밸런스 패치, 시즌 이벤트뿐이다. 사변은 대륙이 만든다.</p>
      <div class="sample" style="margin-top:28px">
        <pre class="info">[현실] 3월 14일 (목) 23:40
[잔고] 미정 | 다음 결제 미정
[포드] 미정
[컨디션] 양호
[관계] └─</pre>
      </div>
      <p class="cap-note">현실 정보창 견본 · 자유모드 프롤로그에서</p>
    </div>
  </div>
</section>

<section class="sec sysband on-sys" id="opinion">
  <div class="wrap split">
    <div class="stick">
      <h2 class="h2">커뮤는 늘 반 박자 늦고, 절반은 틀린다</h2>
      <p class="lead">커뮤, 공략 위키, 스트림챗, 기사. 여론은 세계 안에서 늘 돌아가고, 반드시 무언가를 바꾼다. 사냥 효율이 떨어지고, 시세가 오르고, 최초 보상을 놓치고, 파티 모집이 어려워진다.</p>
    </div>
    <div>
      <ul class="rows">
        <li><b>감지</b><p>누가 무언가를 봤다. 목격담 한 줄.</p></li>
        <li><b>확산</b><p>커뮤와 방송을 타고 퍼진다.</p></li>
        <li><b>변질</b><p>하지 않은 일이 그 사람의 일이 된다.</p></li>
        <li><b>잔향</b><p>잠잠해진 뒤에도 남는다.</p></li>
      </ul>
      <p class="cap-note" style="color:var(--sys-ink-2)">게임 안에서 <span class="m">!인터넷 - 궁금한 내용</span>을 입력하면, 그 내용을 찾아보는 장면으로 커뮤·위키·방송·기사 원문이 나옵니다.</p>
    </div>
  </div>
</section>

<section class="sec" id="faces">
  <div class="wrap">
    <div class="group-h"><h2 class="h2">포드 밖의 얼굴</h2><p>이방인 다섯의 현실. 그림에 올리면 게임 속 모습으로 바뀝니다.</p></div>
    <div class="faces">{faces}</div>
  </div>
</section>
'''
    s += close_band(text="로그아웃해도 대륙은 멈추지 않습니다.", sub=["포드 정비 기한 확인", "다음 결제일 확인", "다이브포드 연결 대기"])
    s += foot()
    write("reality.html", s)


# ═════════════ 시작 ═════════════
def build_start():
    modes = [
        ("newbie", "뉴비", "일레온 프롤로그(뉴비).md", "리아텔 · 귀환석 광장", "Lv1 · 무직",
         "처음 내려서는 이방인. 견습 기사 유안의 안내로 시작해, 옛 수로의 큰쥐부터 잡는다. 대륙을 처음부터 밟아 가고 싶다면."),
        ("myth", "신화직업", "일레온 프롤로그(신화직업).md", "잿빛 회랑 · 균열 보스룸", "Lv1 · 신화",
         "줄리엣과 둘이 균열의 파수꾼을 쓰러뜨렸고, 보상에 먼저 손이 닿았다. 서비스 이래 처음 나온 신화 등급 직업. 대가로 레벨은 1로 돌아간다. 무슨 직업인지는 시작하며 직접 밝힌다."),
        ("free", "자유모드", "일레온 프롤로그(자유모드).md", "현실 · 원룸", "제한 없음",
         "현실의 방, 포드 접속 대기. 어디로 들어갈지, 누구로 들어갈지 정해진 게 없다. 설정 제한 없이 원하는 대로."),
    ]
    s = head("start.html", "시작")
    s += f'''<section class="phead">
  {img(bg("RI"), "리아텔", lazy=False)}
  <div class="wrap">
    <span class="sysmsg">벨라트 대륙 — 접속 위치를 선택하십시오.</span>
    <h1>어디서 눈을 뜰까</h1>
    <p>시작 모드는 셋. 아래는 각 모드의 실제 첫 화면입니다. 크랙에서는 이 형식으로, 매 응답 맨 위의 배경 한 장과 함께 이야기가 이어집니다.</p>
    <div class="btn-row" style="margin-top:26px">{crack_btn(cls="btn light")}</div>
  </div>
</section>
<nav class="toc" aria-label="이 페이지"><div class="wrap">
  <a href="#newbie">뉴비</a><a href="#myth">신화직업</a><a href="#free">자유모드</a><a href="#how">플레이 방법</a>
</div></nav>
'''
    for key, name, fn, where, lv, desc in modes:
        s += f'''<section class="sec" id="{key}">
  <div class="wrap modehead">
    <div class="h2">{E(name)}<div class="kv"><span>시작 지점 · {E(where)}</span><span>시작 상태 · {E(lv)}</span></div>
    <p class="lead">{E(desc)}</p></div>
    <div class="sample">{render_prologue(fn)}</div>
  </div>
</section>
'''
    s += f'''<section class="sec sysband on-sys" id="how">
  <div class="wrap">
    <h2 class="h2">플레이 방법</h2>
    <div class="how" style="margin-top:clamp(28px,4vw,48px)">
      <div>
        <h3 class="h3">대화와 시스템</h3>
        <ul class="rows" style="margin-top:16px">
          <li><b><span class="m">`문장`</span></b><p>월드 메시지, 레벨업, 전직, 알림 같은 시스템 메시지.</p></li>
          <li><b><span class="m">&gt;문장</span></b><p>귓속말, 길드챗, 파티챗. 풀다이브라 플레이어끼리는 기본이 음성 대화이고, 채팅은 보조다.</p></li>
          <li><b><span class="m">!인터넷 - 내용</span></b><p>그 내용을 찾아보는 행동. 커뮤·위키·방송·기사 원문이 나온다.</p></li>
          <li><b>판정</b><p>모든 행동은 시도다. 성공, 대가를 치른 부분 성공, 실패. 레벨 차이가 10 이상이면 거의 일방적이다. 죽으면 레벨이 깎이고 강제 로그아웃되어 현실로 돌아온다.</p></li>
        </ul>
      </div>
      <div>
        <h3 class="h3">단축어</h3>
        <ul class="rows" style="margin-top:16px">
          {"".join(f'<li><b><span class="m">{E(a)}</span></b><p>{E(b)}</p></li>' for a, b in SHORTCUTS)}
        </ul>
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
