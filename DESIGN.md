---
name: FULL DIVE - ILEON
description: 행적을 읽는 세계, 일레온 서버가 직접 말하는 소개 사이트
colors:
  sys: "oklch(33% 0.155 266)"
  sys-deep: "oklch(25% 0.12 268)"
  sys-line: "oklch(44% 0.13 266)"
  sys-hi: "oklch(86% 0.13 205)"
  sys-ink: "oklch(96% 0.02 250)"
  sys-ink-2: "oklch(82% 0.06 256)"
  signal: "oklch(57% 0.2 31)"
  signal-lift: "oklch(74% 0.16 35)"
  ground: "oklch(96.2% 0.009 228)"
  ground-2: "oklch(92.6% 0.014 232)"
  ground-3: "oklch(88.5% 0.018 236)"
  ink: "oklch(21% 0.04 262)"
  ink-2: "oklch(40% 0.035 258)"
  ink-3: "oklch(52% 0.03 255)"
  rule: "oklch(84% 0.02 240)"
  veil-ink: "oklch(90% 0.02 250)"
  grade-1-common: "oklch(50% 0.015 250)"
  grade-2-rare: "oklch(50% 0.15 248)"
  grade-3-epic: "oklch(48% 0.19 302)"
  grade-4-unique: "oklch(55% 0.12 78)"
  grade-5-legend: "oklch(58% 0.18 48)"
  grade-6-myth: "oklch(54% 0.21 18)"
typography:
  display-cover:
    fontFamily: "Hahmlet Variable, Nanum Myeongjo, serif"
    fontSize: "clamp(84px, 19vw, 170px)"
    fontWeight: 780
    lineHeight: 0.9
    letterSpacing: "-0.05em"
  display:
    fontFamily: "Hahmlet Variable, Nanum Myeongjo, serif"
    fontSize: "clamp(52px, 11vw, 96px)"
    fontWeight: 780
    lineHeight: 1.02
    letterSpacing: "-0.045em"
  headline:
    fontFamily: "Hahmlet Variable, Nanum Myeongjo, serif"
    fontSize: "clamp(46px, 8vw, 92px)"
    fontWeight: 780
    lineHeight: 1.04
    letterSpacing: "-0.045em"
  section:
    fontFamily: "Hahmlet Variable, Nanum Myeongjo, serif"
    fontSize: "clamp(30px, 4.4vw, 52px)"
    fontWeight: 800
    lineHeight: 1.18
    letterSpacing: "-0.03em"
  quote:
    fontFamily: "Hahmlet Variable, Nanum Myeongjo, serif"
    fontSize: "clamp(25px, 3.2vw, 40px)"
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: "-0.025em"
  title:
    fontFamily: "Hahmlet Variable, Nanum Myeongjo, serif"
    fontSize: "clamp(21px, 2.2vw, 26px)"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "-0.02em"
  lead:
    fontFamily: "Pretendard Variable, Pretendard, Apple SD Gothic Neo, Malgun Gothic, sans-serif"
    fontSize: "clamp(17px, 1.5vw, 19px)"
    fontWeight: 400
    lineHeight: 1.8
    letterSpacing: "-0.008em"
  body:
    fontFamily: "Pretendard Variable, Pretendard, Apple SD Gothic Neo, Malgun Gothic, sans-serif"
    fontSize: "16.5px"
    fontWeight: 400
    lineHeight: 1.78
    letterSpacing: "-0.008em"
    fontFeature: "tnum"
  system:
    fontFamily: "Nanum Gothic Coding, ui-monospace, D2Coding, monospace"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "0"
  label:
    fontFamily: "Nanum Gothic Coding, ui-monospace, D2Coding, monospace"
    fontSize: "12.5px"
    fontWeight: 700
    lineHeight: 1.6
    letterSpacing: "0"
rounded:
  none: "0px"
spacing:
  seam-tight: "3px"
  seam: "4px"
  gutter: "clamp(16px, 4vw, 48px)"
  container: "1240px"
  header: "56px"
  section: "clamp(72px, 10vw, 132px)"
  section-tight: "clamp(48px, 7vw, 88px)"
components:
  button-system:
    backgroundColor: "{colors.sys}"
    textColor: "{colors.sys-ink}"
    typography: "{typography.system}"
    rounded: "{rounded.none}"
    padding: "15px 24px 14px"
  button-system-hover:
    backgroundColor: "{colors.sys-deep}"
  button-light:
    backgroundColor: "{colors.sys-ink}"
    textColor: "{colors.sys}"
    rounded: "{rounded.none}"
    padding: "15px 24px 14px"
  system-message:
    backgroundColor: "{colors.ground-2}"
    textColor: "{colors.ink}"
    typography: "{typography.system}"
    rounded: "{rounded.none}"
    padding: "3px 9px 2px"
  system-message-on-sys:
    backgroundColor: "{colors.sys-deep}"
    textColor: "{colors.sys-ink}"
  log-line:
    backgroundColor: "{colors.ground-2}"
    textColor: "{colors.ink}"
    typography: "{typography.system}"
    padding: "13px 16px"
  grade-chip:
    textColor: "#ffffff"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "1px 7px 0"
  block-row:
    backgroundColor: "{colors.ground-2}"
    rounded: "{rounded.none}"
    padding: "18px 22px"
  person-chip:
    backgroundColor: "{colors.ground-2}"
    rounded: "{rounded.none}"
    padding: "3px 12px 3px 3px"
  person-chip-hover:
    backgroundColor: "{colors.ground-3}"
  info-window:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.veil-ink}"
    typography: "{typography.system}"
    padding: "16px 18px"
---

# Design System: FULL DIVE - ILEON

## Overview

**Creative North Star: "서버가 말하는 세계"**

이 사이트는 일레온 서버 자체가 방문자에게 말을 거는 화면입니다. 시스템 메시지, 월드 브로드캐스트, 접속 로그가 페이지의 문법이고, 그 사이로 벨라트 대륙의 이름과 사람들이 굵은 명조로 떠오릅니다. 바탕은 포드 안 백색광에 가까운 차갑고 옅은 광물빛(크림도 어둠도 아님)이며, 서버가 직접 발언하는 구간만 깊은 군청 면이 띠 전체를 차지합니다.

밀도는 중간입니다. 정보는 카드가 아니라 4px 틈으로 맞붙은 색 블록으로 쌓이고, 선·모서리 굴림·그림자 없이 바탕 톤 세 단계(ground → ground-2 → ground-3)만으로 층을 나눕니다. 그림은 저장소 `images/`의 WebP입니다. 배경(2048×585)은 왼쪽에 지역 이름 HUD가 그려진 띠라서, 페이지 머리·그림 띠·지역 행에서는 자르지 않고 통째로 보여 주고 글은 그 아래 군청 면에 둡니다. 화면을 꽉 채워야 하는 곳(표지, 홈 히어로, 두 축 패널, 시작 모드)만 오른쪽 기준으로 잘라 HUD를 빼고 군청 베일을 덮습니다. 인물(첫등장 1280×828, 나머지 1280×621)은 가로 그림 그대로 씁니다.

움직임은 "한 줄씩 인쇄"입니다. 로그 줄이 순서대로 켜지고, 월드 로그 레일이 위로 밀려 바뀌고, 헤더의 이중 시계(현실 : 벨라트 = 1 : 4)가 매초 흐릅니다. 튀거나 튕기는 것은 없습니다.

**Key Characteristics:**
- 차가운 광물빛 바탕 + 띠 전체를 차지하는 군청 시스템 면
- 두 서체 = 두 축: 코딩 고정폭(시스템·현실), 굵은 명조 Hahmlet(벨라트 대륙)
- 모서리 0, 테두리 없음, 4px 틈으로 붙는 블록
- 주홍은 사변 전용, 등급색은 등급 표시 전용
- 줄 단위로 켜지는 로그, 감속 곡선 하나

## Colors

차갑고 옅은 광물빛 중립 위에 군청 하나가 지배하고, 주홍과 등급색은 의미가 있을 때만 나오는 팔레트입니다. 원본 값은 OKLCH입니다.

### Primary
- **서버 군청** (`sys`): 시스템 밴드, 레일, 마무리 구획, 기본 버튼, 현재 페이지 표시, 포커스 링, 선택 영역. 서버가 말하는 면 그 자체입니다.
- **깊은 군청** (`sys-deep`): 히어로·페이지 머리 그림이 뜨기 전 바탕, 푸터, 군청 면 위의 시스템 메시지와 로그 줄 바탕, 버튼 hover.
- **군청 선** (`sys-line`): 사변 흐름 단계 위 3px 상단 띠. 군청 면 위에서만 씁니다.
- **수신 청록** (`sys-hi`): 군청 면 위의 강조. 레일의 깜빡이는 점, 부팅 로그의 결과값, 모드 링크, 군청 위 포커스 링.
- **군청 위 글자** (`sys-ink`, `sys-ink-2`): 군청 면 위 본문과 보조 글자.

### Secondary
- **사변 주홍** (`signal`): 사변 채널 태그, 대륙 규모 사변 블록. 사변 외에는 쓰지 않습니다.
- **밝은 주홍** (`signal-lift`): 어두운 면 위에서 쓰는 사변 주홍(군청 위 사변 태그, 사변 흐름의 '발발' 단계, 현실 피드의 [추측] 표시).

### Tertiary: 직업 등급 6단계
- **일반 회청** (`grade-1-common`), **희귀 청** (`grade-2-rare`), **에픽 보라** (`grade-3-epic`), **유니크 황토** (`grade-4-unique`), **전설 주황** (`grade-5-legend`), **신화 진홍** (`grade-6-myth`): 흰 글자 등급 칩, 등급 사다리, 등급 이름 글자색에만 씁니다. 신화 진홍은 "신화 0명"의 큰 숫자와 레벨 띠의 최상단 구간에도 쓰는데, 둘 다 신화 등급을 가리키는 자리입니다. 에픽 보라와 유니크 황토는 각각 [히든], [연대기] 채널 태그의 글자색도 겸합니다.

### Neutral
- **포드 백광** (`ground`): 페이지 바탕, 헤더(90% 반투명 + 흐림), 사진 위 캡션 띠.
- **옅은 광물** (`ground-2`): 블록 바탕(로그 줄, 표 같은 목록, 신앙, 단계), 시스템 메시지 바탕, 목차 띠, 스크롤바 트랙.
- **짙은 광물** (`ground-3`): 한 단계 더 들어간 면(인물 카드, 이미지 대기 바탕, hover 바탕, 블록 안의 시스템 메시지).
- **심야 잉크** (`ink`): 본문 글자. 반전 블록(정보창, 현실 피드, 강조 단계, 비율 띠)의 바탕도 겸합니다.
- **보조 잉크** (`ink-2`), **흐린 잉크** (`ink-3`): 설명문, 메타 정보, 데이터 라벨.
- **베일 위 글자** (`veil-ink`): 사진 베일 위·잉크 반전 블록 위 본문.
- `rule`은 토큰으로만 정의되어 있고 지금 빌드에서 쓰는 곳은 없습니다. 새 선을 긋는 근거로 삼지 마세요.

### Named Rules
**The 사변 독점 Rule.** 주홍(`signal`, `signal-lift`)은 사변만의 색입니다. 경고, 오류, 장식, CTA에 빌려 쓰지 않습니다.

**The 등급은 칩 안에 Rule.** 등급색 여섯은 직업 등급을 가리킬 때만 씁니다. 등급과 무관한 강조나 일러스트용 색으로 쓰지 않습니다.

**The 군청은 면이다 Rule.** 군청은 글자 강조색이 아니라 띠 전체를 차지하는 면입니다. 밝은 바탕 위에서 군청 글자는 현재 위치 표시, 링크, [월드]·[랭킹] 채널 태그 정도로만 씁니다.

## Typography

**Display Font:** Hahmlet Variable (Nanum Myeongjo, serif)
**Body Font:** Pretendard Variable (Apple SD Gothic Neo, Malgun Gothic, sans-serif)
**Label/Mono Font:** Nanum Gothic Coding (ui-monospace, D2Coding, monospace)

**Character:** 세 서체는 각각 한 목소리입니다. Hahmlet은 벨라트 대륙의 이름과 사람의 말, 나눔고딕코딩은 서버와 2047년 현실, Pretendard는 그 사이를 설명하는 해설입니다. 세 서체 모두 `assets/fonts`에 직접 실었습니다.

### Hierarchy
- **Display Cover** (780, clamp(84px, 19vw, 170px), 0.9): 표지의 "ILEON" 한 단어. 위에 고정폭 "FULL DIVE"(0.32em 자간), 아래 Hahmlet 500의 한국어 부제가 붙습니다.
- **Display** (780, clamp(52px, 11vw, 96px), 1.02): 홈 히어로 "벨라트 대륙". 사진 위 가독을 위한 흐린 그림자를 씁니다.
- **Headline** (780, clamp(46px, 8vw, 92px), 1.04): 페이지 머리 h1, 인물 상세 이름(clamp(46px, 6.6vw, 84px)).
- **Section** (800, clamp(30px, 4.4vw, 52px), 1.18, balance 줄바꿈): 구획 제목. 마무리 구획에서는 clamp(34px, 5.6vw, 72px)까지 키웁니다.
- **Quote** (700, clamp(25px, 3.2vw, 40px), 1.4): 인물의 말. 아래 고정폭 700으로 화자를 붙입니다.
- **Title** (700, clamp(21px, 2.2vw, 26px), 1.3): 소제목, 히든직 이름, 블록 안 제목. 블록 제목은 17~38px 사이에서 Hahmlet 700~800으로 같은 결을 유지합니다.
- **Lead** (400, clamp(17px, 1.5vw, 19px), 1.8, 최대 40em): 제목 밑 도입문, `ink-2`.
- **Body** (400, 16.5px, 1.78, 최대 38em): 본문. 한국어 줄바꿈은 `keep-all`, 숫자는 고정폭 숫자(tnum).
- **System** (400/700, 14px, 1.6, 자간 0): 시스템 메시지, 로그, 데이터 표, 버튼.
- **Label** (400/700, 11.5~13px, 자간 0): 등급 칩, 캡션, 메타 정보, 시계.

### Named Rules
**The 두 목소리 두 축 Rule.** 벨라트 대륙의 것은 Hahmlet, 서버와 현실의 것은 고정폭입니다. 같은 컴포넌트가 두 축을 다룰 때도 이 규칙을 따릅니다. 현실 쪽 축 패널의 큰 글자와 현실 페이지 h1은 고정폭 700으로 바뀝니다.

**The 고정폭은 자간 0 Rule.** 나눔고딕코딩은 언제나 `letter-spacing: 0`으로 씁니다. 본문의 음수 자간을 물려받지 않습니다. 예외는 표지 "FULL DIVE"의 0.32em 하나뿐입니다.

## Layout

본문 폭은 최대 1240px이고 좌우 여백은 clamp(16px, 4vw, 48px)입니다. 헤더는 56px 높이로 상단에 붙고, 페이지 안 목차가 그 바로 아래에 붙습니다. 앵커 이동 시 헤더와 목차 높이만큼 비워 둡니다.

구획 위아래 여백은 clamp(72px, 10vw, 132px)이고, 촘촘한 구획은 clamp(48px, 7vw, 88px)입니다. 밝은 구획끼리 이어질 때는 뒤 구획의 위 여백을 없애 한 흐름으로 읽히게 합니다. 군청 밴드는 앞뒤 구획과 여백을 따로 가집니다.

꽉 채우는 그림은 히어로·두 축 패널·시작 모드·표지뿐이고(오른쪽 기준 자르기), 페이지 머리·큰 그림 띠·지역 행은 배경 띠를 원래 비율(2048:585) 그대로 깝니다. 인물 카드는 1280:621, 인물 상세의 무대와 할라크족 카드는 1280:828 비율입니다. 그 밖의 구성은 비대칭 두 단(5:7, 4:8, 7:5) 그리드와 4px 틈으로 붙는 블록 그리드(3~5열)입니다. 지역 소개는 띠 아래 본문 두 단입니다.

반응형 기준은 880px(헤더 메뉴 접힘), 860/900px(두 단 → 한 단), 760px(두 축·인용 한 단), 600/520px(블록 그리드 2열 → 1열)입니다. 모바일에서 그림 패널은 svh 단위 높이를 씁니다.

### Named Rules
**The 4px 틈 Rule.** 블록끼리는 4px(로그 줄은 3px) 틈으로 붙고, 틈 사이로 바탕이 비칩니다. 블록 사이에 여백 대신 선을 긋지 않습니다.

## Elevation & Depth

평면 시스템입니다. 깊이는 바탕 톤 세 단계와 군청 면, 그리고 사진 위 군청 베일(위아래 또는 왼쪽에서 어두워지는 선형 그라데이션)로 만듭니다. 그림자는 기능이 있을 때만 씁니다.

### Shadow Vocabulary
- **헤더 바닥** (`box-shadow: 0 1px 0 var(--ground-2)`): 반투명 헤더와 본문을 가르는 1px 톤. 선이 아니라 그림자 자리에 둔 바탕색입니다.
- **모바일 메뉴** (`box-shadow: 0 12px 24px -12px oklch(20% 0.04 262 / .25)`): 펼친 메뉴가 본문 위에 떠 있음을 알리는 유일한 떠 있는 그림자.
- **사진 위 제목** (`text-shadow: 0 2px 30px oklch(15% 0.08 266 / .5)`): 히어로 제목의 가독용 흐린 번짐.
- **안쪽 윤곽** (`box-shadow: inset 0 0 0 1.5px currentColor` / `inset 0 0 0 2px var(--sys)`): 대기 중 버튼, 비어 있는 신화 칸, 선택된 표정 썸네일. 바깥으로 튀어나오지 않는 상태 표시입니다.

### Named Rules
**The 면으로 층을 Rule.** 층은 그림자가 아니라 바탕 톤으로 나눕니다. 블록은 언제나 평평합니다.

## Shapes

모든 모서리는 직각(0px)입니다. 버튼, 칩, 블록, 사진, 시스템 메시지 모두 굴리지 않습니다. 테두리도 거의 없습니다. 쓰는 곳은 기능이 분명한 몇 곳뿐입니다. 현재 위치 밑줄 2px(내비·목차), "더 보기" 링크 밑줄 1.5px, 사변 흐름 단계의 상단 띠 3px입니다. 사진은 3:4, 2:3, 3:2, 16:9 비율로 잘라 쓰고 인물은 얼굴 높이(위 12~18%)에 초점을 맞춥니다.

## Components

### Buttons
고정폭 700 글자의 단단한 직사각형입니다. 서버가 내미는 명령처럼 보입니다.
- **Shape:** 직각(0px), 고정폭 700 15.5px, 화살표 SVG와 12px 간격.
- **Primary:** 군청 바탕 + 군청 위 글자, 안쪽 여백 15px 24px 14px. 표지에서는 17px, 18px 30px 17px로 키웁니다.
- **Hover / Focus:** hover 시 깊은 군청으로 바뀌고(.25s), 누르면 1px 내려갑니다. 포커스는 2px 군청 윤곽, 3px 띄움(군청 면 위에서는 수신 청록).
- **Light:** 어두운 사진·군청 면 위에서 쓰는 반전형(옅은 글자색 바탕 + 군청 글자, hover 시 흰색).
- **Pending:** 아직 링크가 없는 행동("크랙에서 접속")은 투명 바탕 + 1.5px 안쪽 윤곽 + 75% 불투명도로, 누를 수 없음을 정직하게 보여 줍니다.

### Chips
- **등급 칩:** 등급색 바탕, 흰 고정폭 700 12.5px, 직각. 등급 사다리에서는 3px 틈으로 이어 붙이고, 비어 있는 신화 칸은 안쪽 윤곽만 그립니다.
- **채널 태그:** `[월드]` `[히든]` `[사변]` `[연대기]` `[정세]` `[랭킹]` 대괄호 글자. 바탕 없이 채널별 글자색(군청·에픽 보라·사변 주홍·유니크 황토·보조 잉크)만 씁니다. 군청 면 위에서는 밝은 짝으로 바뀝니다.
- **인물 칩:** 옅은 광물 바탕에 30px 정사각 얼굴 + 600 14px 이름. hover 시 한 단계 짙어집니다.

### Cards / Containers
- **Corner Style:** 직각(0px).
- **Background:** 옅은 광물 블록, 강조는 잉크 반전 또는 군청.
- **Shadow Strategy:** 없음(Elevation & Depth 참고).
- **Border:** 없음.
- **Internal Padding:** 18~26px(블록), 13px 16px(로그 줄).

### Navigation
- **헤더:** 56px, 90% 반투명 백광 + 14px 흐림. 왼쪽에 Hahmlet 800 "ILEON" + 고정폭 부제, 가운데 Pretendard 600 14.5px 메뉴(`ink-2`, hover 시 `ink`, 현재 페이지는 군청 글자 + 2px 밑줄), 오른쪽 끝에 이중 시계.
- **모바일(880px 이하):** 고정폭 "메뉴" 버튼(옅은 광물 바탕), 펼치면 헤더 아래 전폭 목록(17px 항목, 밑줄 대신 군청 글자).
- **페이지 목차:** 헤더 아래 붙는 옅은 광물 띠, 고정폭 13.5px, 가로 스크롤, 현재 구획은 군청 글자 + 2px 밑줄.

### 시스템 메시지 (Signature)
서버의 한 줄입니다. 고정폭 14px, 옅은 광물 바탕의 인라인 블록, 안쪽 여백 3px 9px 2px. 군청 면 위에서는 깊은 군청 바탕, 사진 위에서는 78~80% 불투명 깊은 군청 + 6px 흐림을 씁니다. 내용은 언제나 서버가 실제로 할 법한 문장이나 게임 데이터("벨라트 대륙에 오신 것을 환영합니다.", "랭킹 1위 · Lv64")입니다. 화면에 들어오면 160ms 뒤부터 240ms 간격으로 한 줄씩 켜집니다.

### 로그 목록 (Signature)
채널 태그 + 제목 줄 + Pretendard 설명 줄로 된 2단 그리드 블록입니다. 옅은 광물 바탕, 3px 틈으로 쌓입니다. 히든직 목록과 같은 결의 블록 목록은 4px 틈과 맨 위 고정폭 로그 문장을 씁니다.

### 월드 로그 레일 (Signature)
히어로 아래 끝에 붙는 52px 군청 띠입니다. 왼쪽에 깜빡이는 7px 청록 점과 고정폭 라벨, 오른쪽에 로그 한 줄이 아래에서 올라와 위로 빠집니다(.7s, 감속 곡선).

### 이중 시계 (Signature)
헤더 오른쪽 고정폭 12.5px. 현실 시각과 벨라트 시각(4배속)을 나란히 두고, 벨라트 쪽 숫자만 군청으로 칠합니다. 두 축 패널에서는 같은 시계를 clamp(28px, 3.6vw, 44px) 고정폭 700으로 크게 보여 줍니다.

### 인물 카드
2:3 세로 사진 + 백광 캡션(Hahmlet 700 18px 이름, 고정폭 12px 부제). 왼쪽 위 모서리에 이방인/원주민 표시를 붙이고, 이방인은 군청으로 칠합니다. hover 시 사진이 1.04배로 천천히(.9s) 커집니다.

### 정보창 / 퀘스트창 견본
크랙 출력 형식의 견본입니다. 정보창은 심야 잉크 바탕의 고정폭 `pre` 블록이고, 내레이션은 기울임, 시스템 줄은 짙은 광물 바탕 시스템 메시지로 씁니다. 이 견본 형식은 출력 예시 안에서만 씁니다.

## Do's and Don'ts

### Do:
- **Do** 서버가 하는 말은 고정폭 시스템 메시지나 로그 줄로 쓰고, 서버가 길게 발언하는 구간은 군청 밴드(`sys`) 전체로 칠하세요.
- **Do** 벨라트 대륙의 이름·사람·말은 Hahmlet 700~800, 서버와 2047년 현실은 나눔고딕코딩으로 쓰세요.
- **Do** 블록은 직각, 테두리 없이 옅은 광물(`ground-2`) 바탕으로 만들고 4px 틈으로 붙이세요.
- **Do** 사진은 화면 끝까지 채우고 깊은 군청 베일 그라데이션을 덮어 글자를 올리세요.
- **Do** 등장 움직임은 한 줄씩 켜거나 18px 아래에서 떠오르는 정도로 두고, 곡선은 `cubic-bezier(.16, 1, .3, 1)` 하나를 쓰세요. `prefers-reduced-motion`에서는 모두 즉시 보이게 하세요.
- **Do** 아직 없는 링크나 자산은 대기 버튼(안쪽 윤곽, 75% 불투명)처럼 비어 있음을 정직하게 보여 주세요.

### Don't:
- **Don't** 모서리를 굴리거나, 블록에 테두리·떠 있는 그림자를 더하지 마세요.
- **Don't** 주홍을 사변 외의 목적(경고, 버튼, 장식)에 쓰지 마세요.
- **Don't** 등급색을 등급 표시 밖에서 장식색으로 쓰지 마세요.
- **Don't** 시스템 메시지를 구획 이름표처럼 쓰지 마세요. 서버가 실제로 할 법한 문장이나 게임 데이터만 담습니다.
- **Don't** 금테 키아트 MMO 런처나 어두운 위키처럼 만들지 마세요. 바탕은 언제나 차갑고 옅은 광물빛입니다.
- **Don't** 튕기거나 크기가 출렁이는 움직임을 쓰지 마세요.


## 그림 규칙

- **The 띠는 자르지 않는다 Rule.** 배경 띠의 지역 이름 HUD는 서버가 띄우는 장소 표시입니다. 띠를 원래 비율로 보여 줄 수 있는 자리에서는 자르지 않습니다. 꽉 채워야 할 때만 `object-position: 100% 50%`로 HUD 쪽을 잘라 냅니다.
- 인물 그림은 가로 그대로 씁니다. 세로 칸에 억지로 맞추지 않습니다. 첫등장(_1) 그림에 든 정보 패널은 그대로 보이게 둡니다.
- 모든 `<img>`에 width/height를 넣어 자리 이동을 막습니다(생성기 `dims()`).
