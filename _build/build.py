# -*- coding: utf-8 -*-
# 일레온 사이트 생성기. 실행: python3 _build/build.py  (저장소 최상단에 html을 쓴다)
# 디자인: 검정 + 형광 노랑 판, 찢긴 종이 가장자리, 거대한 한글 활자(Black Han Sans), HUD는 청록.
import os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SET = os.path.join(ROOT, "_설정")
TITLE = "FULL DIVE - ILEON"
DESC = "다이브포드에 누우면 벨라트 대륙이 열린다. 죽어도 돌아오는 이방인이 되어, 당신이 한 일이 직업이 되는 세계. 일레온."
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

ARROW = '<svg class="ic" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M1.5 8h12M9 3l5 5-5 5" stroke="currentColor" stroke-width="2" stroke-linecap="square"/></svg>'
BACK = '<svg class="ic" width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M14.5 8h-12M7 3 2 8l5 5" stroke="currentColor" stroke-width="2" stroke-linecap="square"/></svg>'
CROSS = '<svg class="x" viewBox="0 0 10 10" aria-hidden="true"><path d="M1 1l8 8M9 1 1 9" stroke="currentColor" stroke-width="2"/></svg>'


def gk(g): return GRADE_KEY.get(g, "g1")
def grade(g): return f'<span class="grade {gk(g)}">{g}</span>' if g else ""
def img(src, alt="", cls="", lazy=True):
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy" decoding="async"' if lazy else ' decoding="async" fetchpriority="high"'
    w, h = dims(src)
    return f'<img src="{src}" alt="{E(alt)}" width="{w}" height="{h}"{c}{l}>'
def rows(items, cls="data"):
    return f'<dl class="{cls}">' + "".join(f"<div><dt>{E(a)}</dt><dd>{b}</dd></div>" for a, b in items) + "</dl>"
def glitch(t, tag="span", cls=""):
    """글리치 제목: 같은 글자를 겹쳐 두 겹 더 그린다."""
    return f'<{tag} class="gl {cls}" data-t="{E(t)}">{E(t)}</{tag}>'


def kicker(no, en, ko=""):
    """섹션 머리표: 번호 / 영문 / 한글."""
    return f'<div class="kick" data-rv><span class="no">{no}</span><span class="en">{en}</span>{f"<span class=\"ko\">{ko}</span>" if ko else ""}<i></i></div>'


def cta(cls="btn"):
    """크랙 링크가 있으면 플레이 버튼, 없으면 시작 모드로."""
    if CRACK:
        return f'<a class="{cls}" href="{CRACK}" target="_blank" rel="noopener" data-mag><span>크랙에서 플레이</span>{ARROW}</a>'
    return f'<a class="{cls}" href="{UP}start.html" data-mag><span>시작 모드 고르기</span>{ARROW}</a>'


def marquee(items=MARQUEE, cls=""):
    one = "".join(f"<span>{E(t)}</span>{CROSS}" for t in items)
    return f'<div class="mq {cls}" aria-hidden="true"><div class="mq-t">{one}{one}</div></div>\n'


def head(page, title, up="", desc=DESC):
    nav = "\n".join(
        f'      <a href="{up}{h}"{" aria-current=\"page\"" if h == page else ""}><i>0{k + 1}</i>{t}</a>' for k, (h, t) in enumerate(NAV))
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
<meta name="theme-color" content="#0b0b0a">
<link rel="preload" href="{up}assets/fonts/frak/unifrakturcook-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{up}assets/css/style.css">
<script>document.documentElement.className+=' js'</script>
</head>
<body>
<a class="skip" href="#main">본문으로</a>
<div class="progress" aria-hidden="true"></div>
<header class="top">
  <a class="brand" href="{up}home.html" aria-label="일레온 홈"><b>Ileon</b><small>FULL<br>DIVE</small></a>
  <nav class="nav" id="nav" aria-label="주 메뉴">
{nav}
  </nav>
  <div class="clock" aria-label="현실 시각과 벨라트 시각">
    <span><i>REAL</i><b data-clock="real">--:--</b></span>
    <span class="bt"><i>BELAT</i><b data-clock="belat">--:--</b></span>
  </div>
  <button class="menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><b class="sr">메뉴</b></button>
</header>
<main id="main">
'''


def foot(up=""):
    links = "".join(f'<a href="{up}{h}"><i>0{k + 1}</i>{t}</a>' for k, (h, t) in enumerate(NAV))
    return f'''</main>
<footer class="foot">
  <div class="foot-big" aria-hidden="true">Ileon</div>
  <div class="wrap foot-row">
    <a class="brand" href="{up}home.html"><b>Ileon</b><small>FULL<br>DIVE</small></a>
    <nav aria-label="바닥글">{links}</nav>
    <span class="foot-sys">현실 <b data-clock="real">--:--</b> / 벨라트 <b data-clock="belat">--:--</b></span>
  </div>
</footer>
<script src="{up}assets/js/main.js"></script>
</body>
</html>'''


def close_band(l1="대륙은 지금도", l2="돌아가는 중.", sub="다이브포드 연결 대기", code="RH"):
    return f'''<section class="close">
  <div class="close-bg" data-par>{img(bgd(code), "", "bgimg")}</div>
  <div class="wrap">
    <span class="sysmsg" data-rv>{E(sub)}</span>
    <h2 class="mega" data-rv style="--i:1"><span>{E(l1)}</span><span class="acid">{E(l2)}</span></h2>
    <div class="btn-row" data-rv style="--i:2">{cta()}</div>
  </div>
</section>
'''


def phead(no, en, code, h1, p, toc=None, alt="", sysline=""):
    s = f'''<section class="phead">
  <div class="phead-bg" data-par>{img(bgd(code), alt, "bgimg", lazy=False)}</div>
  <span class="phead-no" aria-hidden="true">{no}</span>
  <div class="wrap">
    <div class="phead-k" data-rv><span>{no}</span><span>{en}</span>{f'<span class="sysmsg">{sysline}</span>' if sysline else ""}</div>
    <h1 class="mega" data-rv style="--i:1">{h1}</h1>
    <p data-rv style="--i:2">{p}</p>
  </div>
</section>
'''
    if toc:
        s += '<nav class="toc" aria-label="이 페이지"><div class="wrap">' + "".join(f'<a href="#{k}"><i>{n + 1:02d}</i>{v}</a>' for n, (k, v) in enumerate(toc)) + "</div></nav>\n"
    return s


def card(c, up="", i=0):
    player = c["side"] == "player"
    sub = c["real"] if player else c["role"].split(" · ")[0]
    return f'''<a class="card" href="{up}char/{c["slug"]}.html" data-side="{c["side"]}" data-rv style="--i:{i % 3}">
  <div class="ph duo">{img(smp(c["code"]), c["name"])}<span class="badge{"" if player else " npc"}">{"이방인" if player else "원주민"}</span><span class="lv">Lv<b>{c["lv"]}</b></span></div>
  <div class="cap">
    <span class="code">{c["code"]}</span>
    <b class="nm">{E(c["name"])}</b>
    <small>{E(sub)} · {E(c["job"].split("(")[0])} {grade(c["grade"])}</small>
    <p class="hook">{E(c["hook"])}</p>
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
def build_cover():
    boot = [("다이브포드 연결", "OK"), ("머리 받침 고정", "OK"), ("감각 해상도", "OK"), ("서버", "벨라트 대륙")]
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
<meta name="theme-color" content="#0b0b0a">
<link rel="preload" href="assets/fonts/frak/unifrakturcook-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
<link rel="prefetch" href="home.html">
<script>document.documentElement.className+=' js'</script>
</head>
<body class="is-cover">
<main class="cover">
  <div class="cover-bg">{img(bgd("P"), "", "bgimg", lazy=False)}</div>
  <div class="cover-top"><span>FULL DIVE</span><span>VRMMO · 2047</span><span class="blink">● REC</span></div>
  <div class="cover-in">
    <h1 class="cover-logo">{glitch("Ileon", "span")}</h1>
    <p class="cover-kr"><b>일레온</b><span>행적을 읽는 세계</span></p>
    <a class="btn big" href="home.html" data-enter data-mag><span>접속</span>{ARROW}</a>
  </div>
  <ol class="boot" aria-label="접속 로그">
    {li}
    <li class="final"><span>접속 위치</span><span class="s">리아텔 · 귀환석 광장</span></li>
  </ol>
  <div class="cover-bot"><span>현실 <b data-clock="real">--:--</b></span><span>벨라트 <b data-clock="belat">--:--</b></span></div>
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
    cast = "".join(f'''<a class="pc" href="char/{c["slug"]}.html" style="--i:{k}" data-rv>
      <div class="pc-ph duo">{img(smp(c["code"]), c["name"])}</div>
      <span class="pc-no">P/0{k + 1}</span>
      <span class="pc-tx"><small>{E(c["real"])} · Lv{c["lv"]} · {E(c["job"].split("(")[0])}</small><b>{E(c["name"])}</b><em>{E(c["hook"])}</em></span>
    </a>''' for k, c in enumerate(players))
    faces = "".join(f'<a href="char/{c["slug"]}.html"><span class="duo">{img(smp(c["code"]), c["name"])}</span><b>{E(c["name"])}</b></a>' for c in npcs)
    statement = "메인 스토리 없음. 결말도 없음. 당신이 한 짓이 직업이 되고, 대륙에서 터진 일이 그대로 역사가 된다."
    jobs = "".join(f'''<div class="log" data-rv style="--i:{k}">
        <span class="log-h"><i>SERVER LOG</i><i>#{k + 1:03d}</i></span>
        <span class="log-m">새 직업이 발현되었습니다.</span>
        <b data-scramble>{E(n)}</b>
        <span class="log-g">{grade(g)}{f'<a href="char/{CMAP["D" if w == "헤리몽" else "E"]["slug"]}.html">{E(w)} {ARROW}</a>' if w else ""}</span>
        <p>{E(t)}</p>
      </div>''' for k, (n, g, t, w) in enumerate(HIDDEN[:4]))
    s = head("home.html", TITLE)
    s += f'''<section class="hero">
  <div class="hero-bg" data-tilt>{img(bgd("RI"), "리아텔의 들판과 마을", "bgimg", lazy=False)}</div>
  <div class="hero-scan" aria-hidden="true"></div>
  <div class="hero-in">
    <div class="hero-sys">
      <span class="sysmsg" data-rv>벨라트 대륙에 오신 것을 환영합니다.</span>
      <span class="sysmsg dim" data-rv style="--i:1">리아텔 · 귀환석 광장 · Lv1 무직</span>
    </div>
    <h1 class="mega hero-t"><span class="ln" data-rv style="--i:2">{glitch("죽어도")}</span><span class="ln acid" data-rv style="--i:3">{glitch("돌아온다.")}</span></h1>
    <div class="hero-foot">
      <p class="hero-sub" data-rv style="--i:4">당신은 이방인. 죽으면 레벨이 깎이고, 귀환석에서 다시 눈을 뜬다.<br>원주민은? <b>한 번이면 끝.</b></p>
      <div class="btn-row" data-rv style="--i:5">
        {cta()}
        <a class="btn ghost" href="world.html" data-mag><span>대륙 둘러보기</span></a>
      </div>
    </div>
    <div class="stamp" data-rv style="--i:6"><small>신화 등급 보유자</small><b>0</b><small>서비스 이래</small></div>
  </div>
  <div class="rail" aria-label="월드 로그">
    <span class="lb"><i></i>LIVE</span><div class="feed">{feed}</div>
  </div>
</section>
{marquee()}
<section class="statement">
  <div class="wrap">
    {kicker("00", "PREMISE", "전제")}
    <p class="say-big">{words(statement)}</p>
  </div>
</section>

<section class="axes" aria-label="현실과 대륙">
  <a class="axis real" href="reality.html">
    {img(bgd("P"), "포드방")}
    <div class="tx">
      <span class="k">2047 · 대한민국</span>
      <h2 class="mega">몸은 여기.</h2>
      <p>월정액, 포드 할부, 정비비. 로그아웃하면 저린 다리랑 커뮤 여론이 기다린다.</p>
      <span class="clk"><b data-clock="real">--:--</b><small>REAL TIME</small></span>
    </div>
  </a>
  <a class="axis virt" href="world.html">
    {img(bgd("KD"), "카뎃트")}
    <div class="tx">
      <span class="k">벨라트 · 여명기 이후 800년</span>
      <h2 class="mega">나는 저기.</h2>
      <p>꺼 둔 사이에도 대륙은 굴러간다. 현실 여섯 시간이 여기선 하루.</p>
      <span class="clk"><b data-clock="belat">--:--</b><small>BELAT TIME ×4</small></span>
    </div>
  </a>
</section>

<section class="quote-band">
  <div class="qb-bg duo dark" data-par>{img(smp("F"), "베른하르트 콜")}</div>
  <div class="wrap">
    <blockquote data-rv>
      <p>“죽어도 돌아오는 자에게 검을 가르치는 건, 삽을 쥐여주는 것과 다르지 않다.”</p>
      <footer><a href="char/bernhardt.html">베른하르트 콜</a> · 카르시온 검술 교관 · Lv71</footer>
    </blockquote>
    <div class="vs" data-rv style="--i:1">
      <div><span>PLAYER</span><b>이방인</b><p>죽으면 레벨이 깎이고, 귀환석에서 돌아온다.</p></div>
      <i>VS</i>
      <div><span>NATIVE</span><b>원주민</b><p>죽으면 끝. 다음은 없다.</p></div>
    </div>
  </div>
</section>

<section class="slab hidden-sec">
  <img class="splat" src="assets/img/ink.png" alt="" aria-hidden="true" loading="lazy">
  <div class="wrap">
    {kicker("01", "HIDDEN CLASS", "히든직")}
    <div class="hs-top">
      <h2 class="mega" data-rv>한 짓이<br>직업이 된다.</h2>
      <p class="lead" data-rv style="--i:1">뭘 반복했는지, 어디 오래 머물렀는지, 누구랑 엮였는지. 시스템이 그걸 읽고 당신 하나만을 위한 직업을 만든다. 조건? <b>아무도 모른다.</b></p>
    </div>
    <div class="hs-grid">
      <div class="zero" data-rv>
        <b data-count="0">0</b>
        <p>신화 등급 보유자.<br>서비스 이래, 지금까지.</p>
        <div class="ladder">{"".join(f'<span class="{gk(g)}">{g}</span>' for g in GRADES)}</div>
      </div>
      <div class="logs">{jobs}</div>
    </div>
    <a class="more" href="system.html#hidden" data-rv>히든직 더 보기 {ARROW}</a>
  </div>
</section>

<section class="sec cast">
  <div class="wrap">
    {kicker("02", "CAST", "인물")}
    <h2 class="mega" data-rv>기다려 주지<br>않는 사람들.</h2>
    <p class="lead" data-rv style="--i:1">이방인 다섯, 원주민 열. 다들 사정이 있고, 다들 먼저 움직인다.</p>
    <div class="pcs">{cast}</div>
    <div class="npc-row" data-rv>{faces}<a class="more" href="characters.html">열다섯 명 전부 {ARROW}</a></div>
  </div>
</section>
{marquee(["사변 발생", "전조 · 발발 · 국면 · 결착 · 여파", "되돌릴 수 없음", "당신 편이 이긴다는 보장 없음"], "red")}
<section class="sec timeline-sec">
  <div class="wrap">
    {kicker("03", "WORLD EVENT", "사변")}
    <h2 class="mega" data-rv>일어난 일이<br><span class="red">곧 이야기.</span></h2>
    <p class="lead" data-rv style="--i:1">대륙 어딘가는 늘 끓는다. 터지면 사변. 무너진 마을은 폐허로 남고, 국경은 다시 그어지고, 죽은 원주민은 돌아오지 않는다.</p>
    <ol class="flow" data-draw>{"".join(f'<li style="--i:{k}"><span>0{k + 1}</span><b>{k_}</b><p>{E(t)}</p></li>' for k, (k_, t) in enumerate(INCIDENT_FLOW))}</ol>
  </div>
</section>

<section class="sec modes-sec">
  <div class="wrap">
    {kicker("04", "START", "시작")}
    <h2 class="mega" data-rv>어디서<br>눈을 뜰래?</h2>
    <div class="modes">
      <a class="mode m1" href="start.html#newbie" data-rv><div class="duo">{img(bgd("RI"), "리아텔")}</div><div class="tx"><span class="sysmsg">리아텔 · 귀환석 광장</span><b>뉴비</b><p>Lv1, 무직. 견습 기사 유안이 덜그럭거리며 달려온다.</p></div><span class="mode-no">01</span></a>
      <a class="mode m2" href="start.html#myth" data-rv style="--i:1"><div class="duo">{img(bgd("BS"), "균열 보스룸")}</div><div class="tx"><span class="sysmsg mag">신화 등급 직업이 발현되었습니다.</span><b>신화직업</b><p>균열의 보상에, 줄리엣보다 먼저 손이 닿았다.</p></div><span class="mode-no">02</span></a>
      <a class="mode m3" href="start.html#free" data-rv style="--i:2"><div class="duo">{img(bgd("H"), "현실의 방")}</div><div class="tx"><span class="sysmsg">접속 위치를 선택하십시오.</span><b>자유모드</b><p>원룸 절반을 차지한 포드. 어디로 들어갈진 아직.</p></div><span class="mode-no">03</span></a>
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
    s += phead("01", "THE CONTINENT", "ER", "벨라트 대륙", "고대 마법 문명이 무너진 지 800년. 새 마법은 없다. 다들 유적에서 파낸 옛것을 고쳐 쓰는 중.",
               [("regions", "지역"), ("faults", "대립선"), ("threats", "위협"), ("halak", "할라크족"), ("gods", "신앙"), ("beyond", "이계")], "에르카시아")
    tabs = "".join(f'<button type="button" role="tab" aria-selected="{"true" if k == 0 else "false"}" data-r="{r["key"]}"><i>{k + 1:02d}</i>{E(r["name"])}</button>' for k, r in enumerate(REGIONS))
    panes = ""
    for k, r in enumerate(REGIONS):
        items = []
        if r["fields"]: items.append(("사냥터", " · ".join(f'{E(n)} <em>{lv}</em>' for n, lv in r["fields"])))
        if r["dungeons"]: items.append(("던전", " · ".join(f'{E(n)} <em>{lv}</em>' for n, kk, lv in r["dungeons"])))
        if r["god"]: items.append(("신앙", E(r["god"])))
        people = "".join(f'<a class="chip" href="char/{CMAP[p]["slug"]}.html">{img(smp(p), "")}{E(CMAP[p]["name"])}</a>' for p in r["people"])
        panes += f'''<article class="rpane" id="{r["key"]}" data-r="{r["key"]}"{"" if k == 0 else " hidden"}>
  <div class="rp-img">{img(bgd(r["img"]), r["name"], lazy=k > 1)}<span class="rp-no">{k + 1:02d}</span></div>
  <div class="rp-tx">
    <span class="where">{E(r["where"])}</span>
    <h3 class="mega">{E(r["name"])}</h3>
    <p>{E(r["text"])}</p>
    {rows(items) if items else ""}
    {f'<div class="people">{people}</div>' if people else ""}
  </div>
</article>
'''
    s += f'''<section class="sec" id="regions">
  <div class="wrap">
    {kicker("01", "REGIONS", "지역")}
    <h2 class="mega" data-rv>제국 하나, 왕국 셋,<br>그리고 여섯 곳.</h2>
    <p class="lead" data-rv style="--i:1">지역마다 레벨대가 이어져 있다. 사냥터를 옮겨 가는 게 곧 성장.</p>
    <div class="rtabs" role="tablist" aria-label="지역" data-rv style="--i:2">{tabs}</div>
    <div class="rstage" data-rv style="--i:2">{panes}</div>
  </div>
</section>

<section class="slab" id="faults">
  <div class="wrap">
    {kicker("02", "FAULT LINES", "대립선")}
    <h2 class="mega" data-rv>전쟁의 씨앗,<br>여덟 줄.</h2>
    <p class="lead" data-rv style="--i:1">끓다가 터지면 사변. 운영사는 사변을 직접 안 쓴다는데, 커뮤는 터질 때마다 "이거 운영 각본 아님?"으로 한바탕 싸운다.</p>
    <ol class="faults">{"".join(f'<li data-rv style="--i:{k % 4}"><span>{k + 1:02d}</span><b>{E(a)}</b><p>{E(b)}</p></li>' for k, (a, b) in enumerate(FAULTS))}</ol>
  </div>
</section>

<section class="sec" id="threats">
  <div class="wrap split">
    <div class="stick">
      {kicker("03", "THREATS", "위협")}
      <h2 class="mega" data-rv>사람 바깥에서<br>오는 것들.</h2>
      <p class="lead" data-rv style="--i:1">전쟁은 사람끼리. 침공은 대륙 바깥과, 아래에서.</p>
    </div>
    <ol class="threats">{"".join(f'<li data-rv style="--i:{k}"><span>{k + 1:02d}</span><b>{E(a)}</b><p>{E(b)}</p></li>' for k, (a, b) in enumerate(THREATS))}</ol>
  </div>
</section>

<section class="feature-band" id="halak">
  <div class="fb-img" data-par>{img(smp("N"), "카시엘")}</div>
  <div class="wrap">
    <div class="fb-tx">
      {kicker("04", "HALAK", "할라크족")}
      <h2 class="mega" data-rv>이방인을<br><span class="red">재앙</span>이라<br>부르는 자들.</h2>
      <p data-rv style="--i:1">고대 흑룡의 피를 이은 장수 종족. 검은 굽은 뿔에 금빛 눈, 수백 년을 산다. 라흐나 침강지 가장자리 고지대가 터전이고, 인간 왕국보다 먼저 이 땅에 있었다는 자부심이 세다.</p>
      <p data-rv style="--i:2">군세 칼데스를 이끄는 카시엘의 목표는 하나. 이방인을 대륙에서 몰아내는 것. 죽어도 돌아오는 자들이 매주 봉인지를 들쑤시고, 그럴수록 봉인이 얇아진다는 계산이다. 숨기지도 않는다.</p>
      <a class="more" href="char/kasiel.html" data-rv style="--i:3">카시엘 · Lv88 {ARROW}</a>
    </div>
  </div>
</section>

<section class="sec" id="gods">
  <div class="wrap">
    {kicker("05", "FAITH", "신앙")}
    <h2 class="mega" data-rv>신은<br>침묵하지 않는다.</h2>
    <p class="lead" data-rv style="--i:1">직접 내려오지도 않지만. 신탁도 축복도 꼭 신관을 거친다. 한 신전에서 신뢰를 얻으면, 다른 신전에선 찬밥이 되기도 하고.</p>
    <div class="gods">{"".join(f'<div data-rv style="--i:{k % 3}"><span>{k + 1:02d}</span><b>{E(n)}</b><i>{E(k_)}</i><p>{E(t)}</p></div>' for k, (n, k_, t) in enumerate(GODS))}</div>
  </div>
</section>

<section class="band" id="beyond">
  <div class="band-bg" data-par>{img(bgd("OW"), "이계", "bgimg")}</div>
  <div class="wrap">
    {kicker("06", "BEYOND", "이계")}
    <h2 class="mega" data-rv>균열 너머.</h2>
    <p data-rv style="--i:1">예고 없이 열렸다 닫히는 균열. 깊은 데로 들어가면 대륙 밖 다른 세계가 이어져 있다. 마계니 천계니 하는 구분은 없다. 그냥 이계. 가장 어려운 무대.</p>
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
    s += phead("02", "CAST", "T", "열다섯 사람", "이방인 다섯에겐 포드 밖의 삶이 있고, 원주민 열은 죽으면 그만이다. 누구랑든 다닐 수 있지만, 원주민은 망설인다. <q>넌 언젠가 안 돌아올 거잖아.</q>", alt="주점")
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
    data = [("레벨", f"Lv{c['lv']}")]
    data.append(("직업", f'{E(c["job"])}{" · 히든" if c["hidden"] else ""} {grade(c["grade"])}') if c["grade"] else ("역할", E(c["job"])))
    data.append(("소속", E(c["role"])))
    if player: data.append(("본명", E(c["real"])))
    data.append(("나이", f'{c["sex"]} · {c["age"]}'))
    looks = [("게임" if player else "외형", E(c["look_game"]))]
    if player: looks.append(("현실", E(c["look_real"])))
    looks.append(("말투", E(c["speech"])))
    body = "".join(f"<p>{E(p)}</p>" for p in c["body"])
    quote = f'<blockquote class="cq" data-rv><span aria-hidden="true">“</span>{E(c["quote"])}</blockquote>' if c["quote"] else ""

    def thumbs(code, labels, axis, hidden=False):
        bs = "".join(f'<button type="button" aria-pressed="{"true" if n == 1 else "false"}" data-src="{cs(code, n)}" data-alt="{E(c["name"])} {lab}">{img(cs(code, n), "")}<span><i>{n:02d}</i>{lab}</span></button>' for n, lab in enumerate(labels, 1))
        return f'<div class="thumbs" data-axis="{axis}"{" hidden" if hidden else ""}>{bs}</div>'

    th = thumbs(c["code"], EXPR, "game")
    sw = ""
    if player:
        sw = '<div class="axis-sw" role="tablist" aria-label="게임과 현실"><button type="button" role="tab" data-axis="game" aria-selected="true">게임</button><button type="button" role="tab" data-axis="real" aria-selected="false">현실</button><i class="pill" aria-hidden="true"></i></div>'
        th += thumbs(c["code"] + "2", EXPR_REAL, "real", hidden=True)

    s = head("characters.html", c["name"], up=up, desc=f'{c["name"]}. {c["hook"]}')
    s += f'''<section class="chead{" is-npc" if not player else ""}">
  <div class="chead-bg" data-tilt>{img(smp(c["code"]), c["name"], "bgimg", lazy=False)}</div>
  <span class="chead-code" aria-hidden="true">{c["code"]}</span>
  <div class="wrap">
    <a class="back" href="../characters.html" data-rv>{BACK} 인물 목록</a>
    <div class="chead-k" data-rv><span class="badge{"" if player else " npc"}">{"이방인" if player else "원주민"}</span><span>{E(c["role"])}</span></div>
    <h1 class="mega" data-rv style="--i:1">{glitch(c["name"])}</h1>
    {f'<p class="real" data-rv style="--i:1">현실 · {E(c["real"])}</p>' if player else ""}
    <p class="hook" data-rv style="--i:2">{E(c["hook"])}</p>
    <div class="chead-stat" data-rv style="--i:3"><span><i>LV</i><b>{c["lv"]}</b></span><span><i>{"CLASS" if c["grade"] else "ROLE"}</i><b class="sm">{E(c["job"].split("(")[0])}</b></span>{f'<span><i>GRADE</i>{grade(c["grade"])}</span>' if c["grade"] else ""}</div>
  </div>
</section>
<section class="sec">
  <div class="wrap cbody">
    <div>
      {kicker("01", "PROFILE", "사람")}
      <div class="prose" data-rv>{body}</div>
      {quote}
    </div>
    <aside data-rv style="--i:1">
      {rows(data)}
      <div class="looks">{rows(looks)}</div>
    </aside>
  </div>
</section>
<section class="sec viewer-sec">
  <div class="wrap">
    {kicker("02", "EXPRESSIONS", "표정")}
    <div class="viewer">
      <div class="stage">{img(cs(c["code"], 1), c["name"], "fig")}<span class="st-hud" aria-hidden="true"></span></div>
      <div class="side">
        {sw}{th}
        <p class="hint">← → 키로도 넘어간다.</p>
      </div>
    </div>
  </div>
</section>
<nav class="pn" aria-label="다른 인물">
  <a href="{prev_c["slug"]}.html"><span class="duo">{img(smp(prev_c["code"]), "")}</span><span class="pn-tx"><small>{BACK} 이전</small><b>{E(prev_c["name"])}</b></span></a>
  <a href="{next_c["slug"]}.html"><span class="duo">{img(smp(next_c["code"]), "")}</span><span class="pn-tx"><small>다음 {ARROW}</small><b>{E(next_c["name"])}</b></span></a>
</nav>
'''
    s += foot(up)
    UP = ""
    write(f"char/{c['slug']}.html", s)


# ═════════════ 체계 ═════════════
def build_system():
    s = head("system.html", "체계")
    tiers = [("1차", "Lv10", "전직 NPC에게서. 등급은 일반."),
             ("2차", "Lv40 + 실적 심사", "희귀 등급. 이쯤이면 길드가 영입하러 온다. 생산 계열은 레벨 대신 제작 실적."),
             ("3차", "Lv60 + 시련", "에픽. 정규 루트의 끝. 서버 전체에 다섯 명."),
             ("히든", "레벨 무관", "조건을 채운 사람만. 얻는 순간, 서버 로그엔 직업명만 뜬다.")]
    s += phead("03", "SYSTEM", "TR", "느리게<br>오른다.", "서버 1위가 Lv64. 대부분은 Lv15 언저리에서 접는다. 스탯은 힘, 민첩, 지구력, 감각. 포인트 찍는 거 없다. 반복한 만큼 오른다.",
               [("level", "레벨"), ("class", "전직"), ("hidden", "히든직"), ("third", "3차 전직자"), ("dungeon", "던전"), ("incident", "사변"), ("quest", "퀘스트")], "훈련장")
    s += f'''<section class="sec" id="level">
  <div class="wrap">
    {kicker("01", "LEVEL", "레벨")}
    <h2 class="mega" data-rv>Lv1에서<br>Lv64까지.</h2>
    <p class="lead" data-rv style="--i:1">이방인 기준 얘기. 원주민 강자들은 이 상한 밖에 있다. 기사단장, 공작가, 할라크족 장로는 Lv70에서 90대. 랭킹 1위도 그 앞에선 아래.</p>
    <div class="lvbar" data-draw>
      <div class="track" aria-hidden="true"><span style="--w:15">1-15</span><span style="--w:5" class="gap"></span><span style="--w:15">20-35</span><span style="--w:5" class="gap"></span><span style="--w:10">40-50</span><span style="--w:9">55+</span><span style="--w:5" class="peak">64</span></div>
      <ol>
        <li><b>Lv1-15</b><p>절대다수가 여기서 접는다.</p></li>
        <li><b>Lv20-35</b><p>꾸준파. 마을에서 얼굴을 알아본다.</p></li>
        <li><b>Lv40-50</b><p>상위권. 길드가 먼저 찾아온다.</p></li>
        <li><b>Lv55+</b><p>랭커.</p></li>
        <li><b>Lv64</b><p>정점. 지금은 한 명.</p></li>
      </ol>
    </div>
  </div>
</section>

<section class="sec" id="class">
  <div class="wrap">
    {kicker("02", "CLASS", "전직")}
    <h2 class="mega" data-rv>전직은 세 번,<br>그리고 히든.</h2>
    <div class="steps">{"".join(f'<div class="{"hid" if a == "히든" else ""}" data-rv style="--i:{k}"><span class="k">{E(b)}</span><b>{E(a)}</b><p>{E(t)}</p></div>' for k, (a, b, t) in enumerate(tiers))}</div>
    <div class="split" style="margin-top:clamp(56px,7vw,96px)">
      <div data-rv><h3 class="h3">계열 아홉</h3>
      <p class="lead">정규직은 뼈대만 있다. 이름도 조건도 다 공개돼서, 공략만 보면 누구나 밟아 올라간다.</p>
      <div class="classes">{"".join(f"<span>{E(x)}</span>" for x in CLASSES)}</div></div>
      <div data-rv style="--i:1"><h3 class="h3">정규 계보 몇 가지</h3>
      <div class="lines">{"".join("<div>" + "<i></i>".join(f'<span>{E(x)} {grade(GRADES[k])}</span>' for k, x in enumerate(ln)) + "</div>" for ln in LINES)}</div></div>
    </div>
  </div>
</section>

<section class="slab" id="hidden">
  <img class="splat" src="assets/img/ink.png" alt="" aria-hidden="true" loading="lazy">
  <div class="wrap">
    {kicker("03", "HIDDEN CLASS", "히든직")}
    <h2 class="mega" data-rv>이 게임의<br>간판.</h2>
    <p class="lead" data-rv style="--i:1">시스템이 행적을 읽고 그 사람만의 직업을 만든다. 같은 이름은 둘이 못 가진다. 서버 로그엔 직업명만 뜨니까, 하나 나올 때마다 커뮤는 조건을 추측하고, 대개 틀린다.</p>
    <div class="logs five">{"".join(f'<div class="log" data-rv style="--i:{k % 3}"><span class="log-h"><i>SERVER LOG</i><i>#{k + 1:03d}</i></span><b data-scramble>{E(n)}</b><span class="log-g">{grade(g)}{f"<em>{E(w)}</em>" if w else ""}</span><p>{E(t)}</p></div>' for k, (n, g, t, w) in enumerate(HIDDEN))}</div>
    <div class="grade-note" data-rv>
      <div class="ladder big">{"".join(f'<span class="{gk(g)}">{g}</span>' for g in GRADES)}</div>
      <p>등급은 지금의 강함이 아니라 잠재력. 정규 루트는 에픽에서 끝나고, 유니크부터는 히든직뿐이다. 히든직 등급은 일반부터 신화까지 제각각이라, 조건이 까다롭다고 등급이 높은 것도 아니다. 전설은 서버에 두세 명. <b>신화는 아직 0명.</b></p>
    </div>
  </div>
</section>

<section class="sec" id="third">
  <div class="wrap">
    {kicker("04", "TOP 5", "3차 전직자")}
    <h2 class="mega" data-rv>서버 꼭대기의<br>다섯.</h2>
    <p class="lead" data-rv style="--i:1">3차 전직자, 서버 전체에 다섯. 나머지 넷은 서버 로그와 커뮤 소문으로만 오르내린다.</p>
    <ol class="third">{"".join(f'<li class="{"first" if k == 0 else ""}" data-rv style="--i:{k}"><span class="rk">#{k + 1}</span><span class="r">Lv{lv}</span><b>{E(n)}</b><span class="j">{E(j)} {grade("에픽")}</span><p>{E(t)}</p></li>' for k, (n, a, sx, lv, j, t) in enumerate(THIRD))}</ol>
  </div>
</section>

<section class="sec" id="dungeon">
  <div class="wrap split">
    <div class="stick">
      {kicker("05", "DUNGEON", "던전")}
      <h2 class="mega" data-rv>소굴에서<br>이계까지.</h2>
      <p class="lead" data-rv style="--i:1">필드보스는 나오는 시각이 대충 알려져 있어서, 길드들이 시간 맞춰 몰려든다. 네임드는 일반 몬스터 자리에 아주 가끔. 그건 순전히 운.</p>
    </div>
    <div class="dungeons">
      <div data-rv><b>소굴</b><span>3-5인 · 반복 입장</span><p>한 시간 안쪽. 매일의 벌이.</p></div>
      <div data-rv style="--i:1"><b>유적</b><span>5-8인 · 주 1회</span><p>기믹이 있고, 스킬의 원천이 되는 고대 기록이 나온다.</p></div>
      <div data-rv style="--i:2"><b>봉인지</b><span>20인 이상 · 라흐나</span><p>제1·2환은 Lv58-64. 제3환은 아직 아무도 못 넘었다.</p></div>
      <div data-rv style="--i:3"><b>균열</b><span>무작위 · 시간 제한</span><p>예고 없이 열리고 닫힌다. 최초 돌파 보상이 걸려서, 소문 돌면 사람이 몰린다.</p></div>
      <div data-rv style="--i:4" class="deep"><b>이계</b><span>균열 너머</span><p>대륙 밖. 제일 어려운 곳.</p></div>
    </div>
  </div>
</section>
{marquee(["사변 발생", "전조 · 발발 · 국면 · 결착 · 여파", "되돌릴 수 없음", "당신 편이 이긴다는 보장 없음"], "red")}
<section class="sec timeline-sec" id="incident">
  <div class="wrap">
    {kicker("06", "WORLD EVENT", "사변")}
    <h2 class="mega" data-rv>사변은<br><span class="red">이렇게</span> 흘러간다.</h2>
    <p class="lead" data-rv style="--i:1">일정은 없다. 결과는 영구히 남고, 큰 사변엔 결정적 역할을 한 이방인 이름이 같이 기록된다.</p>
    <ol class="flow" data-draw>{"".join(f'<li style="--i:{k}"><span>0{k + 1}</span><b>{k_}</b><p>{E(t)}</p></li>' for k, (k_, t) in enumerate(INCIDENT_FLOW))}</ol>
    <div class="scale">{"".join(f'<div data-rv style="--i:{k}"><span>{"I" * (k + 1) if k < 3 else "IV"}</span><b>{k_}</b><p>{E(t)}</p></div>' for k, (k_, t) in enumerate(INCIDENT_SCALE))}</div>
    <p class="lead wide" data-rv>참여는 자유. 용병 계약, 징집, 약탈, 밀수, 피난민 호송, 아예 빠지기까지. 그리고 당신이 사변을 부르기도 한다. 봉인지를 무리하게 돌면 범람이 가까워지고, 숲에서 나무를 베면 아엘린이 날을 세운다.</p>
  </div>
</section>

<section class="sec" id="quest">
  <div class="wrap split">
    <div class="stick">
      {kicker("07", "QUEST", "퀘스트")}
      <h2 class="mega" data-rv>미리 정해진<br>퀘스트는 없다.</h2>
      <p class="lead" data-rv style="--i:1">정세와 사변, 사람의 사정에서 생겨난다. 의뢰자는 자기 이익이 먼저라 보상을 깎고, 정보를 빼고, 등을 돌리기도 한다. 어떻게 푸느냐에 따라 결과가 갈리고, 그 결과가 다음 정세가 된다.</p>
      <div class="qbox" data-rv style="--i:2;margin-top:28px"><p class="q">퀘스트 : 견습 기사의 안내</p><p>유안을 따라 수비대 훈련장에서 기본 무기를 받고, 옛 수로의 큰쥐 5마리를 처치한다. 보상: 초심자 무기, 20골드</p><p class="opt">수락 | 거절</p></div>
    </div>
    <div class="qkinds">{"".join(f'<div data-rv style="--i:{k % 2}"><span>{k + 1:02d}</span><b>{E(a)}</b><p>{E(b)}</p></div>' for k, (a, b) in enumerate(QUEST_KINDS))}</div>
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
    faces = "".join(f'''<a class="face" href="char/{c["slug"]}.html" data-rv style="--i:{k}"><div class="ph">{img(smp(c["code"] + "2"), c["real"])}{img(smp(c["code"]), "", "g")}<span class="face-sw" aria-hidden="true">GAME ⇄ REAL</span></div>
      <div class="cap"><b>{E(c["real"])}</b><span>{E(REAL_LIFE[c["code"]])}</span><small>게임에선 {E(c["name"])}</small></div></a>''' for k, c in enumerate(players))
    s = head("reality.html", "현실")
    s += phead("04", "REALITY · 2047", "CT", "2047,<br>대한민국", "무대는 대륙만이 아니다. 포드에 누운 사람이 사는 이쪽도 이야기의 일부. 결판이 나는 곳은 아니지만, 정산하고 다음을 준비하는 곳.",
               [("pod", "다이브포드"), ("money", "돈"), ("account", "계정"), ("opinion", "여론"), ("faces", "포드 밖의 얼굴")], "2047년의 도시",
               '현실 · <span data-clock="date">2047</span> · <span data-clock="real">--:--</span>')
    s += f'''<section class="sec" id="pod">
  <div class="wrap pod">
    <div>
      {kicker("01", "DIVE POD", "다이브포드")}
      <h2 class="mega" data-rv>누우면<br>열린다.</h2>
      <p class="lead" data-rv style="--i:1">풀수면 VR, 다이브포드. 머리 받침이 천천히 내려오고, 시야가 어두워지고, 귓가에 익숙한 안내음.</p>
    </div>
    <div class="podgrid">
      <div data-rv><span>01</span><b>등급</b><p>보급형부터 프로용까지. 감각 해상도, 반응 속도, 접속 한계가 갈린다. 울산강펀치는 보급형 최저가, 무명은 PK로 번 돈으로 프로용.</p></div>
      <div data-rv style="--i:1"><span>02</span><b>포드방</b><p>집에 포드가 없어도 된다. 공용 포드방이 있으니까.</p></div>
      <div data-rv style="--i:2"><span>03</span><b>정비</b><p>정비 기한을 넘기면 감각이 한 박자씩 늦게 따라온다.</p></div>
      <div data-rv style="--i:3"><span>04</span><b>로그아웃</b><p>목 마르고, 다리 저리고, 시간 감각이 어긋난다. 오래 있을수록 컨디션은 떨어지고, 자고 먹어야 돌아온다.</p></div>
    </div>
  </div>
</section>

<section class="band" id="money">
  <div class="band-bg" data-par>{img(bgd("P"), "포드방", "bgimg")}</div>
  <div class="wrap">
    {kicker("02", "MONEY", "돈")}
    <h2 class="mega" data-rv>게임의 돈,<br><span class="acid">현실의 돈.</span></h2>
    <p data-rv style="--i:1">월정액, 할부, 전기세, 정비비는 진짜로 빠져나간다. 골드는 환전되지만 수수료 붙고 출금은 느리다. 그래도 이걸로 먹고사는 사람이 있다.</p>
  </div>
</section>

<section class="sec" id="account">
  <div class="wrap split">
    <div class="stick">
      {kicker("03", "ACCOUNT", "계정")}
      <h2 class="mega" data-rv>캐릭터는<br>하나뿐.</h2>
      <p class="lead" data-rv style="--i:1">부계정 없음. 새로 하려면 지금 캐릭터를 지워야 한다. 그래서 히든직이랑 레벨 쌓은 캐릭터를 버리는 일은 드물고, 커뮤에서 "캐삭"은 사건이 된다. 핵이나 매크로? 존재하지 않는다.</p>
    </div>
    <div data-rv style="--i:1">
      <pre class="info">[현실] 3월 14일 (목) 23:40
[잔고] 미정 | 다음 결제 미정
[포드] 미정
[컨디션] 양호
[관계] └─</pre>
      <p class="hint">현실 장면에선 정보창도 이렇게 바뀐다.</p>
    </div>
  </div>
</section>

<section class="slab" id="opinion">
  <div class="wrap">
    {kicker("04", "COMMUNITY", "여론")}
    <h2 class="mega" data-rv>커뮤는 늘 반 박자 늦고,<br>절반은 틀린다.</h2>
    <p class="lead" data-rv style="--i:1">커뮤, 공략 위키, 스트림챗, 기사. 여론은 쉬지 않고 돌고, 반드시 뭔가를 바꾼다. 사냥 효율이 떨어지거나, 시세가 뛰거나, 파티 구하기가 어려워지거나.</p>
    <ol class="flow four" data-draw>
      <li style="--i:0"><span>01</span><b>감지</b><p>누가 뭔가를 봤다. 목격담 한 줄.</p></li>
      <li style="--i:1"><span>02</span><b>확산</b><p>커뮤와 방송을 타고 번진다.</p></li>
      <li style="--i:2"><span>03</span><b>변질</b><p>안 한 일이, 그 사람이 한 일이 된다.</p></li>
      <li style="--i:3"><span>04</span><b>잔향</b><p>잠잠해져도 뭔가는 남는다.</p></li>
    </ol>
  </div>
</section>

<section class="sec" id="faces">
  <div class="wrap">
    {kicker("05", "FACES", "포드 밖의 얼굴")}
    <h2 class="mega" data-rv>닉네임 아래의<br>사람들.</h2>
    <p class="lead" data-rv style="--i:1">이방인 다섯의 현실. 그림에 마우스를 올리면 게임 속 모습.</p>
    <div class="faces">{faces}</div>
  </div>
</section>
'''
    s += close_band(l1="로그아웃해도", l2="대륙은 안 멈춘다.", sub="포드 정비 기한 확인", code="CT")
    s += foot()
    write("reality.html", s)


# ═════════════ 시작 ═════════════
def build_start():
    modes = [
        ("newbie", "뉴비", "일레온 프롤로그(뉴비).md", "리아텔 · 귀환석 광장", "Lv1 · 무직",
         "처음 대륙에 내려선 이방인. 견습 기사 유안의 안내를 받고, 옛 수로 큰쥐부터. 대륙을 처음부터 천천히 밟고 싶다면."),
        ("myth", "신화직업", "일레온 프롤로그(신화직업).md", "잿빛 회랑 · 균열 보스룸", "Lv1 · 신화",
         "줄리엣과 둘이서 균열의 파수꾼을 쓰러뜨렸고, 보상에 먼저 손이 닿았다. 서비스 이래 첫 신화 등급 직업. 대가로 레벨은 1. 무슨 직업인지는, 시작하면서 당신이 밝힌다."),
        ("free", "자유모드", "일레온 프롤로그(자유모드).md", "현실 · 원룸", "제한 없음",
         "밤 열한 시 사십 분, 포드 앞. 어디로 들어갈지, 누구로 살지 아무것도 안 정해졌다. 원하는 대로."),
    ]
    s = head("start.html", "시작")
    s += phead("05", "START", "RI", "어디서<br>눈을 뜰래?", "시작 모드는 셋. 아래는 각 모드의 실제 첫 장면이다. 응답마다 배경 한 장과 함께, 이런 식으로 이어진다.",
               [("newbie", "뉴비"), ("myth", "신화직업"), ("free", "자유모드"), ("how", "플레이 방법")], "리아텔", "접속 위치를 선택하십시오.")
    for k, (key, name, fn, where, lv, desc) in enumerate(modes):
        s += f'''<section class="sec mode-sec{" myth" if key == "myth" else ""}" id="{key}">
  <div class="wrap modehead">
    <div class="stick">
      <span class="num" data-rv>0{k + 1}</span>
      <h2 class="mega" data-rv>{E(name)}</h2>
      <p class="lead" data-rv style="--i:1">{E(desc)}</p>
      <div data-rv style="--i:2">{rows([("시작 지점", E(where)), ("시작 상태", E(lv))])}</div>
    </div>
    <div class="sample" data-rv><div class="sample-bar"><span>크랙 출력 견본</span><i></i><i></i><i></i></div>{render_prologue(fn)}</div>
  </div>
</section>
'''
    s += f'''<section class="slab" id="how">
  <div class="wrap">
    {kicker("04", "HOW TO PLAY", "플레이 방법")}
    <h2 class="mega" data-rv>이렇게<br>논다.</h2>
    <div class="how">
      <div class="howgrid">
        <div data-rv><code>`문장`</code><p>월드 메시지, 레벨업, 전직 같은 시스템 메시지.</p></div>
        <div data-rv style="--i:1"><code>&gt;문장</code><p>귓속말, 길드챗, 파티챗. 풀다이브라 평소엔 목소리로 말하고, 채팅은 거들 뿐.</p></div>
        <div data-rv style="--i:2"><code>!인터넷 - 내용</code><p>궁금한 건 찾아본다. 커뮤, 위키, 방송, 기사가 원문 그대로.</p></div>
        <div data-rv style="--i:3"><code>판정</code><p>모든 행동은 시도. 성공, 대가를 치른 성공, 실패. 레벨 10 이상 차이면 거의 일방적. 죽으면 레벨이 깎이고 현실로 튕겨 나온다.</p></div>
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
