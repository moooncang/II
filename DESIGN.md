---
name: FULL DIVE - ILEON
description: 행적을 읽는 세계, 일레온 서버가 직접 말하는 소개 사이트
colors:
  hud: "#5ee6f2"
  hud-2: "#2bb8cc"
  hud-lift: "#8ff0f8"
  hud-ink: "#04121a"
  hud-a: "rgba(94,230,242,.12)"
  hud-b: "rgba(94,230,242,.28)"
  mag: "#cf86f5"
  signal: "#ff7350"
  bg: "#0a0f1d"
  bg-2: "#0e1527"
  bg-3: "#131c33"
  bg-4: "#1a2440"
  void: "#05080f"
  console: "#060a14"
  line: "rgba(150,180,230,.11)"
  line-2: "rgba(150,180,230,.2)"
  line-3: "rgba(150,180,230,.32)"
  text: "#e3e9f4"
  dim: "#a3aec4"
  dimmer: "#8792ac"
  grade-1-common: "#9aa6bd"
  grade-2-rare: "#62a6ff"
  grade-3-epic: "#b688ff"
  grade-4-unique: "#f2c46a"
  grade-5-legend: "#ff9d45"
  grade-6-myth: "#ff5874"
typography:
  display-cover:
    fontFamily: "Hahmlet Variable, Nanum Myeongjo, serif"
    fontSize: "clamp(68px, 13vw, 150px)"
    fontWeight: 800
    lineHeight: 0.95
    letterSpacing: "-0.04em"
  display:
    fontFamily: "Hahmlet Variable, Nanum Myeongjo, serif"
    fontSize: "clamp(50px, 8.4vw, 108px)"
    fontWeight: 800
    lineHeight: 1.02
    letterSpacing: "-0.045em"
  headline:
    fontFamily: "Hahmlet Variable, Nanum Myeongjo, serif"
    fontSize: "clamp(42px, 6.4vw, 78px)"
    fontWeight: 800
    lineHeight: 1.08
    letterSpacing: "-0.045em"
  band:
    fontFamily: "Hahmlet Variable, Nanum Myeongjo, serif"
    fontSize: "clamp(32px, 4.4vw, 52px)"
    fontWeight: 800
    lineHeight: 1.2
    letterSpacing: "-0.04em"
  section:
    fontFamily: "Pretendard Variable, Pretendard, Apple SD Gothic Neo, Malgun Gothic, sans-serif"
    fontSize: "clamp(25px, 3vw, 34px)"
    fontWeight: 800
    lineHeight: 1.35
    letterSpacing: "-0.03em"
  quote:
    fontFamily: "Hahmlet Variable, Nanum Myeongjo, serif"
    fontSize: "clamp(22px, 2.6vw, 32px)"
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: "-0.025em"
  title-world:
    fontFamily: "Hahmlet Variable, Nanum Myeongjo, serif"
    fontSize: "24px"
    fontWeight: 800
    lineHeight: 1.3
    letterSpacing: "-0.03em"
  title:
    fontFamily: "Pretendard Variable, Pretendard, Apple SD Gothic Neo, Malgun Gothic, sans-serif"
    fontSize: "19px"
    fontWeight: 700
    lineHeight: 1.45
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Pretendard Variable, Pretendard, Apple SD Gothic Neo, Malgun Gothic, sans-serif"
    fontSize: "15.5px"
    fontWeight: 400
    lineHeight: 1.8
    letterSpacing: "-0.01em"
    fontFeature: "tnum"
  system:
    fontFamily: "Nanum Gothic Coding, ui-monospace, monospace"
    fontSize: "12.5px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0.02em"
  button:
    fontFamily: "Nanum Gothic Coding, ui-monospace, monospace"
    fontSize: "13px"
    fontWeight: 700
    letterSpacing: "0.14em"
  label:
    fontFamily: "Nanum Gothic Coding, ui-monospace, monospace"
    fontSize: "11px"
    fontWeight: 700
    letterSpacing: "0.26em"
  data-key:
    fontFamily: "Nanum Gothic Coding, ui-monospace, monospace"
    fontSize: "11.5px"
    fontWeight: 400
    letterSpacing: "0.12em"
rounded:
  none: "0px"
  dot: "50%"
spacing:
  hairline: "1px"
  gutter: "clamp(18px, 4vw, 40px)"
  container: "1200px"
  header: "60px"
  panel-gap: "24px"
  section: "clamp(72px, 9vw, 120px)"
  section-tight: "clamp(48px, 6vw, 72px)"
components:
  button-primary:
    backgroundColor: "{colors.hud}"
    textColor: "{colors.hud-ink}"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: "15px 24px 14px"
  button-primary-hover:
    backgroundColor: "{colors.hud-lift}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.text}"
    typography: "{typography.button}"
    rounded: "{rounded.none}"
    padding: "15px 24px 14px"
  button-ghost-hover:
    textColor: "{colors.hud}"
  button-pending:
    backgroundColor: "transparent"
    textColor: "{colors.dim}"
    typography: "{typography.button}"
    padding: "15px 24px 14px"
  section-label:
    textColor: "{colors.dimmer}"
    typography: "{typography.label}"
  system-message:
    backgroundColor: "rgba(8,20,34,.72)"
    textColor: "{colors.hud}"
    typography: "{typography.system}"
    rounded: "{rounded.none}"
    padding: "5px 12px 4px 10px"
  grade-chip:
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "2px 8px 1px"
  tag:
    textColor: "{colors.dim}"
    rounded: "{rounded.none}"
    padding: "4px 11px"
  tag-on:
    backgroundColor: "{colors.hud-a}"
    textColor: "{colors.hud}"
  filter:
    backgroundColor: "{colors.bg-2}"
    textColor: "{colors.dim}"
    padding: "9px 16px"
  filter-on:
    backgroundColor: "{colors.text}"
    textColor: "{colors.bg}"
  card-character:
    backgroundColor: "{colors.bg-2}"
    rounded: "{rounded.none}"
    padding: "16px 18px 18px"
  card-character-hover:
    backgroundColor: "{colors.bg-3}"
  grid-cell:
    backgroundColor: "{colors.bg}"
    padding: "22px 22px 24px"
  badge-stranger:
    backgroundColor: "{colors.hud}"
    textColor: "{colors.hud-ink}"
    padding: "4px 8px 3px"
  badge-native:
    backgroundColor: "rgba(10,15,29,.8)"
    textColor: "{colors.dim}"
    padding: "4px 8px 3px"
  info-window:
    backgroundColor: "{colors.console}"
    textColor: "#b8c4da"
    typography: "{typography.system}"
    padding: "16px 18px"
  header:
    backgroundColor: "rgba(10,15,29,.78)"
    height: "{spacing.header}"
---

# Design System: FULL DIVE - ILEON

## Overview

**Creative North Star: "심야의 접속 단말"**

밤의 군청 바탕 위에 서버의 청록 HUD가 켜진 화면입니다. 방문자는 다이브포드에 누워 접속 단말을 보고 있고, 그 단말이 벨라트 대륙을 기록 문서처럼 펼쳐 보입니다. 뼈대는 작가님의 앞선 작품 사이트(테이머)의 문법을 따릅니다. 고정폭 섹션 레이블과 그 뒤로 뻗는 가는 선, 키와 값이 한 줄씩 쌓인 데이터 행, 1px 헤어라인으로 맞붙은 카드 격자, 필터 막대가 그것입니다. 그 위에 일레온만의 것이 얹힙니다. 대륙의 이름과 사람은 굵은 명조 Hahmlet으로, 서버의 말은 고정폭 시스템 메시지로 쓰고, 헤더의 4:1 이중 시계와 표지의 회전하는 HUD 링이 이 세계의 시간과 접속을 보여 줍니다.

밀도는 중상입니다. 정보는 둥근 카드가 아니라 헤어라인 격자와 데이터 행으로 정리되고, 층은 바탕 톤 네 단계(bg → bg-2 → bg-3 → bg-4)와 가는 선 세 단계로 나눕니다. 그림은 `images/bg-draft`의 깨끗한 배경과 `images/sample` 인물 키 이미지이며, 언제나 군청 베일 그라데이션을 덮고 그 위에 글자를 올립니다. HUD 배너(`images/B`)는 시작 페이지의 크랙 출력 견본 안에서만 씁니다.

움직임은 단말이 켜지는 결입니다. 시스템 메시지가 한 줄씩 켜지고, 월드 로그 레일이 아래에서 밀려 올라오며, 시계가 매초 흐르고, 표지의 링 세 겹이 서로 다른 속도로 돕니다. 곡선은 `cubic-bezier(.16,1,.3,1)` 하나입니다.

**Key Characteristics:**
- 밤 군청 바탕(#0a0f1d) + 청록 HUD 강조 하나
- 세 서체 = 세 목소리: Hahmlet(대륙), 나눔고딕코딩(서버·데이터), Pretendard(해설)
- 1px 헤어라인 격자와 데이터 행, 모서리 0
- 고정폭 섹션 레이블 + 선, 목차와 같은 이름
- 빛은 HUD에서만 난다: 청록·주홍 발광, 떠 있는 그림자 없음

## Colors

밤 군청 중립 위에 청록 하나가 지배하고, 자홍·주홍·등급색은 의미가 있을 때만 켜지는 팔레트입니다. 원본 값은 `style.css`의 `:root` 사용자 속성입니다.

### Primary
- **HUD 청록** (`hud`): 기본 버튼 바탕, 현재 페이지·현재 목차, 포커스 링(1.5px, 3px 띄움), 선택 영역, 시스템 메시지 글자와 점, 레이블 안의 한국어 이름, 데이터의 강조값, 벨라트 쪽 시계 숫자, HUD 모서리 프레임. 화면에서 "서버가 켜져 있다"는 표시입니다.
- **밝은 청록** (`hud-lift`): 기본 버튼 hover 바탕.
- **청록 위 잉크** (`hud-ink`): 청록 면 위 글자(기본 버튼, 이방인 배지, 선택된 축 전환 버튼).
- **청록 막** (`hud-a`, `hud-b`): 선택된 태그·퀘스트창 바탕(12%), 시스템 메시지·더 보기 밑줄·모드 카드 hover 테두리(28%).
- `hud-2`는 토큰으로만 정의되어 있고 지금 빌드에서 쓰는 곳은 없습니다.

### Secondary
- **히든 자홍** (`mag`): `[히든]` 채널 글자색, 표지 HUD 링의 가장 안쪽 원(25% 불투명). 히든직을 가리키는 자리 외에는 쓰지 않습니다.

### Tertiary
- **사변 주홍** (`signal`): `[사변]`·`[전쟁]` 채널 글자색, 사변 흐름의 '발발' 마디(채움 + 발광), 흐름 선의 청록→주홍 그라데이션, 사변 규모 단계의 상단 2px 막대(불투명도 .4→1).
- **직업 등급 6단계** (`grade-1-common` 회청, `grade-2-rare` 청, `grade-3-epic` 보라, `grade-4-unique` 황금, `grade-5-legend` 주황, `grade-6-myth` 진홍): 등급 칩(글자·1px 테두리·12% 바탕이 같은 색), 등급 사다리, 3차 전직자의 직업 줄(에픽 보라). 신화 진홍은 "신화 0명" 큰 숫자와 레벨 분포 띠의 최상단 구간에도 쓰며, 둘 다 신화를 가리키는 자리입니다.

### Neutral
- **밤 군청** (`bg`): 페이지 바탕, 헤어라인 격자 칸 바탕. 화면 위쪽 오른편에 푸른 방사형 빛(12%), 왼편에 청록 빛(5%)이 고정으로 깔립니다.
- **한 층 위** (`bg-2`): 교차 구획 바탕, 카드·패널·지역·필터 버튼 바탕, 격자 칸 hover.
- **두 층 위** (`bg-3`): 카드 hover, 이미지 대기 바탕, 표정 썸네일 바탕.
- **세 층 위** (`bg-4`): 스크롤바 손잡이, 레벨 분포 띠의 기본 구간.
- **허공** (`void`): 표지 바탕, 표정 뷰어 무대. 그림이 떠 있는 가장 깊은 자리입니다.
- **콘솔** (`console`): 크랙 정보창 견본의 `pre` 바탕.
- **선** (`line` 11%, `line-2` 20%, `line-3` 32%): 헤어라인 격자, 데이터 행 구분, 구획 경계(`line`) / 태그·칩·필터 외곽(`line-2`) / 고스트 버튼 윤곽, 패널 hover 테두리(`line-3`).
- **글자** (`text`), **보조** (`dim`), **흐린 보조** (`dimmer`): 본문 / 설명·메타 / 레이블·데이터 키·캡션·시계 숫자 외 글자.

### Named Rules
**The 청록 하나 Rule.** 강조색은 청록 하나입니다. 행동(버튼), 현재 위치, 서버의 목소리, 벨라트 쪽 숫자에만 켭니다. 화면 대부분은 군청과 회청 글자입니다.

**The 사변 독점 Rule.** 주홍은 사변(과 전쟁) 채널과 사변 흐름·규모 표시만의 색입니다. 경고, 오류, 버튼, 장식에 빌려 쓰지 않습니다.

**The 등급은 칩 안에 Rule.** 등급색 여섯은 직업 등급을 가리킬 때만 씁니다. 자홍도 히든직 전용입니다.

## Typography

**Display Font:** Hahmlet Variable (Nanum Myeongjo, serif)
**Body Font:** Pretendard Variable (Pretendard, -apple-system, Apple SD Gothic Neo, Malgun Gothic, sans-serif)
**Label/Mono Font:** Nanum Gothic Coding (ui-monospace, monospace)

**Character:** Hahmlet은 벨라트 대륙의 이름·사람·말, 나눔고딕코딩은 서버와 데이터, Pretendard는 그 사이를 설명하는 해설입니다. 세 서체 모두 `assets/fonts`에 직접 실었습니다. 한국어는 `keep-all` 줄바꿈, 숫자는 고정폭 숫자(tnum)입니다.

### Hierarchy
- **Display Cover** (800, clamp(68px, 13vw, 150px), 0.95): 표지의 "ILEON" 한 단어. 청록 발광 번짐(`0 0 60px` 25%)이 붙고, 위에 고정폭 "FULL DIVE"(12px, 0.6em 자간, 청록)가 섭니다.
- **Display** (800, clamp(50px, 8.4vw, 108px), 1.02): 홈 히어로 제목. 아래 Pretendard 500 부제(15.5~18px, 최대 30em)가 붙습니다.
- **Headline** (800, clamp(42px, 6.4vw, 78px), 1.08): 페이지 머리 h1. 인물 상세 이름은 clamp(48px, 7vw, 88px)까지 키웁니다.
- **Band** (800, clamp(32px, 4.4vw, 52px), 1.2): 그림 띠·마무리 구획의 Hahmlet 제목(마무리는 clamp(32px, 5vw, 60px)), 모드 머리(clamp(34px, 4vw, 48px)).
- **Section** (Pretendard 800, clamp(25px, 3vw, 34px), 1.35, balance 줄바꿈): 섹션 레이블 아래 구획 제목. 설명하는 제목이므로 해설 서체를 씁니다.
- **Quote** (700, clamp(22px, 2.6vw, 32px), 1.5): 인물의 말. 아래 고정폭 12px로 화자를 붙이고, 인물 상세에서는 청록 2px 왼쪽 선과 함께 씁니다.
- **Title World** (Hahmlet 700~800, 21~30px, 대표 24px): 지역·히든직·신·모드·사변 단계·3차 전직자 이름처럼 대륙의 고유명이 카드나 칸의 제목일 때.
- **Title** (Pretendard 700, 19px, 1.45): 일반 소제목. 카드 안 인물 이름·타일 제목은 16~17px 700.
- **Body** (400, 15.5px, 1.8): 본문. 도입문(`lead`)은 같은 크기에 `dim`, 최대 62ch. 개요 도입·인물 산문은 17px / 15.5px에 1.9~1.95 행간.
- **System** (400, 12.5px, 1.5, 0.02em): 시스템 메시지, 정보창, 퀘스트 선택지.
- **Button** (700, 13px, 0.14em): 버튼, "더 보기"·"돌아가기" 링크(12~11.5px).
- **Label** (700, 11px, 0.26em, 대문자): 섹션 레이블. 같은 크기 대역(11~11.5px, 0.12~0.22em)의 고정폭이 데이터 키, 카드 소제목, 헤더 브랜드, 캡션에 쓰입니다.

### Named Rules
**The 세 목소리 Rule.** 대륙의 고유명은 Hahmlet, 서버와 수치는 고정폭, 설명은 Pretendard입니다. 한 컴포넌트가 두 축을 다룰 때도 따릅니다(두 축 패널: 가상 쪽 제목은 Hahmlet, 현실 쪽은 Pretendard).

**The 고정폭은 벌린다 Rule.** 고정폭은 언제나 양의 자간(0.02~0.26em)으로 HUD처럼 벌려 씁니다. 크기가 작을수록 넓게 벌립니다(레이블 11px 0.26em, 버튼 13px 0.14em, 메시지 12.5px 0.02em). 본문의 음수 자간을 물려받지 않습니다.

## Layout

본문 폭은 최대 1200px, 좌우 여백은 clamp(18px, 4vw, 40px)입니다. 헤더는 60px 높이로 상단에 붙고(78% 반투명 + 14px 흐림), 하위 페이지의 목차 띠가 바로 아래에 붙습니다(90% 반투명 + 10px 흐림). 앵커 이동 시 헤더 + 60px를 비웁니다.

구획 위아래 여백은 clamp(72px, 9vw, 120px), 촘촘한 구획은 clamp(48px, 6vw, 72px)입니다. 교차 구획은 `bg-2` 바탕 + 위아래 `line`으로 구분합니다. 구획은 섹션 레이블 → 구획 제목 → 도입문 순으로 열고, 제목 줄 오른쪽 끝에 "더 보기" 링크를 둡니다.

구성은 세 가지 그리드로 짭니다.
- **비대칭 두 단** (7:5, 4:8, 6:6, 8:4): 글과 데이터 행, 끈적한 왼쪽 단(헤더 + 76~80px)과 긴 오른쪽 단.
- **헤어라인 격자** (2~6열, 1px 간격): 격자 전체를 `line` 바탕 + 1px 외곽으로 두고 칸을 `bg`/`bg-2`로 채워, 1px 틈이 곧 선이 됩니다. 인물 카드, 히든직, 타일, 신앙, 3차 전직자, 사변 규모, 레벨 단계, 필터 막대, 인물 가로 띠(스크롤 스냅).
- **떨어진 패널** (24px 간격, 시작 모드는 20px): 그림이 큰 두 축·지역·모드 패널만 테두리를 가진 독립 패널로 띄웁니다.

전폭 그림 머리는 홈 히어로(100svh − 헤더), 페이지 머리, 인물 머리(min(78svh, 700px)), 그림 띠, 마무리 구획이고, 모두 왼쪽·아래쪽에서 `bg`로 어두워지는 베일을 덮습니다.

반응형 기준은 1000px(카드 3→2열), 900px(헤더 메뉴 접힘, 두 단·흐름·모드 → 한 단), 860px(비대칭 두 단 → 한 단), 760px(두 축·표정 격자 한 단), 640px(행 한 단), 600/560/520px(격자 → 1열)입니다.

### Named Rules
**The 틈이 선이다 Rule.** 맞붙는 칸끼리는 1px `line` 틈으로 나눕니다. 칸마다 따로 테두리를 그리거나 간격을 벌리지 않습니다.

## Elevation & Depth

평면 시스템입니다. 깊이는 바탕 톤 네 단계와 선 세 단계, 반투명 + 흐림 막(헤더, 목차, 레일, 시스템 메시지), 그리고 그림 위 군청 베일로 만듭니다. 그림자는 떠 있음이 아니라 빛을 뜻하며, HUD 청록과 사변 주홍만 빛납니다.

### Shadow Vocabulary
- **버튼 발광** (`box-shadow: 0 0 30px rgba(94,230,242,.35)`): 기본 버튼 hover.
- **신호 점 발광** (`box-shadow: 0 0 8px var(--hud)` / `0 0 10px var(--hud)` / `0 0 12px var(--signal)`): 시스템 메시지 앞 5px 사각 점, 레일의 깜빡이는 6px 점, 사변 흐름의 '발발' 마디.
- **안쪽 윤곽** (`box-shadow: inset 0 0 0 1px var(--line-3)`): 고스트 버튼(hover 시 청록), 대기 버튼은 `line-2`.
- **제목 번짐** (`text-shadow: 0 4px 40px rgba(0,0,0,.45)`, 표지는 `0 0 60px rgba(94,230,242,.25)`, 신화 0은 `0 0 40px rgba(255,88,116,.35)`): 그림 위 제목의 가독, 그리고 빛나는 숫자.

### Named Rules
**The 빛은 HUD에서만 Rule.** 번짐은 청록·주홍(그리고 신화 진홍) 같은 발광체에만 씁니다. 카드나 패널은 떠오르지 않고, hover는 바탕 한 단계 또는 테두리 한 단계와 3~4px 들림으로 표시합니다.

## Shapes

모서리는 직각(0px)입니다. 버튼, 칩, 태그, 카드, 패널, 사진, 시스템 메시지 모두 굴리지 않습니다. 둥근 것은 HUD의 원뿐입니다. 브랜드 표시(실선 원 안의 점선 원), 현재 페이지 4px 점, 레일 점, 사변 흐름 마디, 표지 링이 원입니다. 기본 버튼은 왼쪽 아래·오른쪽 위를 10px 비스듬히 깎은 다각형(`clip-path`)이고, 고스트·대기 버튼은 깎지 않습니다. 강조 그림에는 왼쪽 위·오른쪽 아래에 16px 청록 꺾쇠(1.5px)를 붙여 HUD 조준 프레임을 만들고, 표지는 위쪽 두 모서리에 28px 꺾쇠를 둡니다. 선은 1px가 기본이고 1.5px(포커스, 목차 현재 밑줄, 꺾쇠)와 2px(인용 왼쪽 선, 퀘스트창 왼쪽 선, 사변 규모 막대)만 예외입니다.

## Components

### Buttons
서버가 내미는 명령 단추입니다. 고정폭 700 대문자 자간, 화살표 SVG와 12px 간격.
- **Shape:** 직각, 10px 모서리 깎기(기본만).
- **Primary:** 청록 바탕 + 청록 위 잉크, 15px 24px 14px. 표지에서는 13.5px, 17px 34px 16px.
- **Hover / Focus:** 밝은 청록 + 청록 발광(.25s/.3s), 누르면 1px 내려갑니다. 포커스는 1.5px 청록 윤곽, 3px 띄움.
- **Ghost:** 투명 + 본문 글자 + `line-3` 안쪽 윤곽, hover 시 윤곽과 글자가 청록.
- **Pending:** 아직 링크가 없는 행동(크랙 작품 링크)은 `aria-disabled` 투명 + `dim` 글자 + `line-2` 윤곽, 기본 커서. 비어 있음을 정직하게 보여 줍니다.
- **더 보기 링크:** 고정폭 12px 청록 + `hud-b` 1px 밑줄, hover 시 밑줄이 진해지고 화살표 간격이 8→12px로 벌어집니다.

### Chips
- **등급 칩:** 고정폭 700 11px, 등급색 글자 + 1px 등급색 테두리 + 12% 등급색 바탕, 직각. 등급 사다리에서는 4px 간격, 50% 테두리·10% 바탕으로 한 단계 낮춥니다.
- **태그:** 12px, `line-2` 테두리 + `dim` 글자. 켜진 태그는 `hud-b` 테두리 + `hud-a` 바탕 + 청록 글자.
- **채널 태그:** `[월드]` `[랭킹]`(청록), `[히든]`(자홍), `[사변]` `[전쟁]`(주홍), `[정세]`(`dim`). 고정폭 700, 바탕 없이 글자색만.
- **인물 칩:** 28px 정사각 얼굴 + 12.5px 이름, `line-2` 테두리, hover 시 청록.

### Cards / Containers
- **Corner Style:** 직각(0px).
- **Background:** 격자 칸은 `bg`, 카드·패널은 `bg-2`, hover는 한 단계 위.
- **Shadow Strategy:** 없음(Elevation & Depth 참고).
- **Border:** 격자는 1px `line` 틈, 떨어진 패널은 1px `line`(hover `line-3` 또는 `hud-b`).
- **Internal Padding:** 격자 칸 20~26px, 카드 캡션 16px 18px 18px, 패널 글 20~28px.

### Inputs / Fields
- **필터 막대:** 헤어라인 격자로 붙은 버튼 묶음(`bg-2`, 12.5px 600, 9px 16px). 켜진 버튼은 반전(`text` 바탕 + `bg` 글자), 개수는 고정폭 11px 70%로 붙입니다.
- **축 전환:** `line-2` 외곽의 두 칸 전환, 켜진 칸은 청록 바탕 + 청록 위 잉크.

### Navigation
- **헤더:** 60px. 왼쪽 브랜드(22px 청록 이중 원 + 고정폭 700 12.5px 0.24em "ILEON" + `dimmer` 부제), 오른쪽 Pretendard 600 13.5px 메뉴(`dim`, hover `text`, 현재 페이지는 청록 + 아래 4px 점), 끝에 세로 선으로 나뉜 이중 시계.
- **모바일(900px 이하):** 고정폭 "MENU" 상자 버튼(`line-2`). 펼치면 헤더 아래 전폭 목록(16px, 행마다 `line`), 시계는 남고 "현실/벨라트" 글자만 빠집니다.
- **목차 띠:** 헤더 아래 붙는 13px 600 가로 스크롤, 현재 구획은 청록 + 1.5px 밑줄.
- **이전/다음:** 인물 상세 아래 두 칸, 고정폭 11px 레이블 + 17px 700 이름, hover `bg-2`.

### 섹션 레이블 (Signature)
고정폭 700 11px 0.26em 대문자 영문 이름 + 청록 `em`의 한국어 이름, 그 뒤로 남은 폭 전체에 1px `line`이 뻗습니다. 레이블은 그 페이지 목차의 구획 이름과 같은 말입니다(REGIONS 지역 10, FAITH 신앙). 구획마다 하나, 구획 제목 바로 위에만 둡니다.

### 시스템 메시지 (Signature)
서버의 한 줄입니다. 청록 고정폭 12.5px, 72% 깊은 남색 바탕 + `hud-b` 1px 테두리 + 6px 흐림, 앞에 발광하는 5px 청록 사각 점. 내용은 서버가 실제로 할 법한 문장이나 게임 데이터("벨라트 대륙에 오신 것을 환영합니다.", "신화 등급 직업이 발현되었습니다.")입니다. 화면에 들어오면 160ms 뒤부터 240ms 간격으로 한 줄씩 켜집니다.

### 데이터 행 (Signature)
키(고정폭 11.5px 0.12em `dimmer`)와 값(14.5px `text`)이 기준선에 맞춘 두 칸 그리드로 한 줄씩 쌓이고, 위아래 `line`으로 나뉩니다. 지역 카드 안에서는 13px로 줄입니다. 같은 결의 넓은 행(11em : 7fr, 18px 행 간격)은 이름 + 설명 목록에 쓰고, 앞에 청록 고정폭 번호를 붙입니다.

### 이중 시계 (Signature)
헤더 오른쪽 고정폭 11.5px. 현실 시각과 벨라트 시각(4배속, 현실 6시간 = 게임 1일)을 나란히 두고 벨라트 숫자만 청록으로 칠합니다. 두 축 패널에서는 같은 시계를 30px 고정폭 700으로 크게 보여 주고, 아래 비율 줄이 4:1을 밝힙니다.

### 인물 카드
16:10 사진(얼굴 높이 22% 초점) + 캡션(17px 700 이름, 고정폭 11px 본명, 청록 12.5px 메타, `dim` 13.5px 한 줄 소개, `line` 위로 분리된 직업·등급 줄). 오른쪽 위에 이방인(청록 면) / 원주민(어두운 면 + `line-2`) 배지. hover 시 바탕 한 단계, 사진 1.045배(1s).

### 표지 HUD 링
표지 가운데 min(86vmin, 640px) SVG 링 세 겹이 60s / 38s(역방향) / 90s로 돕니다. 청록 원(14~55%, 점선 포함)과 가장 안쪽 자홍 원(25%)으로 짭니다. 입장하면 링이 2s로 빨라지고 배경이 1.25배로 다가온 뒤 옅은 청록 섬광(`#dff9ff`)으로 넘어갑니다. 왼쪽 아래에는 접속 로그가 420ms 간격으로 한 줄씩 찍힙니다.

### 월드 로그 레일
홈 히어로 아래 끝의 48px 띠(70% `bg` + 8px 흐림, 위 `line-2`). 왼쪽에 깜빡이는 청록 점(1.8s)과 고정폭 레이블, 오른쪽에 로그 한 줄이 3.6초마다 아래에서 올라와 위로 빠집니다(.7s).

### 정보창 / 퀘스트창 견본
크랙 출력 형식의 견본입니다. 정보창은 `console` 바탕 고정폭 `pre`, 퀘스트창은 청록 2px 왼쪽 선 + `hud-a` 그라데이션, 내레이션은 기울임, 시스템 줄은 시스템 메시지. HUD 배너 그림(`images/B`)은 이 견본 안에서만 씁니다.

## Do's and Don'ts

### Do:
- **Do** 서버가 하는 말은 고정폭 시스템 메시지로, 대륙의 고유명은 Hahmlet 700~800으로, 설명은 Pretendard로 쓰세요.
- **Do** 정보를 묶을 때는 1px 헤어라인 격자(`line` 바탕 + `bg` 칸)나 데이터 행으로 짜세요.
- **Do** 구획은 목차와 같은 이름의 섹션 레이블로 여세요.
- **Do** 청록은 행동, 현재 위치, 서버의 목소리, 벨라트 쪽 숫자에만 켜세요.
- **Do** 그림 위 글자에는 왼쪽·아래쪽에서 `bg`로 어두워지는 군청 베일을 덮으세요.
- **Do** 움직임은 한 줄씩 켜기, 16px 아래에서 떠오르기, 느린 사진 확대 정도로 두고 곡선은 `cubic-bezier(.16,1,.3,1)` 하나를 쓰세요. `prefers-reduced-motion`에서는 모두 즉시 보이게 하세요.
- **Do** 아직 없는 링크나 자산은 대기 버튼처럼 비어 있음을 정직하게 보여 주세요.

### Don't:
- **Don't** 사각 요소의 모서리를 굴리지 마세요. 원은 HUD 점·마디·링에만 씁니다.
- **Don't** 카드나 패널에 떠 있는 그림자를 더하지 마세요. 번짐은 발광체에만 씁니다.
- **Don't** 주홍을 사변·전쟁 밖에서, 등급색을 등급 밖에서, 자홍을 히든직 밖에서 쓰지 마세요.
- **Don't** 시스템 메시지나 섹션 레이블에 지어낸 문구를 담지 마세요. 메시지는 서버가 할 법한 말이나 게임 데이터, 레이블은 목차의 구획 이름뿐입니다.
- **Don't** HUD 배너(`images/B`)를 크랙 출력 견본 밖의 장식으로 쓰지 마세요.
- **Don't** 튕기거나 크기가 출렁이는 움직임을 쓰지 마세요.
