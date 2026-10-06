---
name: FULL DIVE - ILEON
description: 사이트 자체가 일레온 게임 클라이언트. 표지는 로딩 화면, 인물은 캐릭터 선택, 대륙은 지역 이동, 체계는 인쇄된 규칙서, 현실은 2047년 기기 화면.
colors:
  void: "#07080a"
  void-2: "#0d0f13"
  void-3: "#151820"
  void-4: "#1e222c"
  fg: "#f3f1ec"
  fg-2: "#b9bcc4"
  fg-3: "#8a8f9a"
  edge: "rgba(255,255,255,.13)"
  edge-2: "rgba(255,255,255,.26)"
  signal: "#ff2e43"
  hud: "#5ce5ff"
  hidden: "#d68cff"
  paper: "#e9e3d3"
  paper-ink: "#16130f"
  paper-red: "#c8202d"
  os-bg: "#dde1e8"
  os-ink: "#101216"
  os-ink-2: "#555b66"
  grade-1-common: "#a9adb6"
  grade-2-rare: "#5fa8ff"
  grade-3-epic: "#b98bff"
  grade-4-unique: "#ffd166"
  grade-5-legend: "#ff9440"
  grade-6-myth: "#ff2e43"
typography:
  title-xl:
    fontFamily: "Pretendard Variable, Pretendard, Apple SD Gothic Neo, Malgun Gothic, sans-serif"
    fontSize: "clamp(76px, 13.5vw, 228px)"
    fontWeight: 900
    lineHeight: 0.88
    letterSpacing: "-0.065em"
  title:
    fontFamily: "Pretendard Variable, Pretendard, Apple SD Gothic Neo, Malgun Gothic, sans-serif"
    fontSize: "clamp(44px, 6.2vw, 104px)"
    fontWeight: 900
    lineHeight: 0.98
    letterSpacing: "-0.055em"
  hud-number:
    fontFamily: "Barlow Condensed, Pretendard Variable, sans-serif"
    fontSize: "clamp(64px, 9vw, 156px)"
    fontWeight: 800
    lineHeight: 0.88
  label:
    fontFamily: "Barlow Condensed, Pretendard Variable, sans-serif"
    fontSize: "13px"
    fontWeight: 700
    letterSpacing: "0.2em"
  lore:
    fontFamily: "Hahmlet Variable, Nanum Myeongjo, serif"
    fontSize: "clamp(24px, 2.3vw, 34px)"
    fontWeight: 800
    lineHeight: 1.4
    letterSpacing: "-0.035em"
  body:
    fontFamily: "Pretendard Variable, Pretendard, Apple SD Gothic Neo, Malgun Gothic, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.75
    letterSpacing: "-0.01em"
  system:
    fontFamily: "Nanum Gothic Coding, ui-monospace, monospace"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.5
rounded:
  none: "0px"
  os-card: "26px"
  os-pill: "999px"
spacing:
  gutter: "clamp(18px, 4vw, 56px)"
  header: "64px"
  scene: "100svh"
---

# 일레온 디자인 기준 (3차, 게임 클라이언트)

## 콘셉트

사이트를 소개 페이지가 아니라 **일레온 게임 클라이언트**로 만든다. 섹션 머리표 + 제목 + 카드 격자 같은 웹사이트 문법을 쓰지 않는다. 각 페이지는 게임 안의 화면 하나다.

| 페이지 | 화면 | 핵심 장치 |
|---|---|---|
| 표지 index | 로딩 화면 | 진행 막대, 접속 로그, 아무 키나 눌러 접속, 흰 섬광 |
| 홈 home | 타이틀 화면 + 장면 | ILEON 로고와 타이틀 메뉴, 플레이어 상태창, 월드 채팅, 지역 띠, 두 시계(×4), 기울어진 인물 패널, 히든직 발현 화면, 저장 슬롯 |
| 인물 characters | 캐릭터 선택 | 왼쪽 명단에 올리면 배경 그림과 이름·능력치가 바뀐다 |
| 인물 상세 char/ | 프로필 창 | 왼쪽 고정 무대(표정 그림) + 표정 줄, ← →, Q/E |
| 대륙 world | 지역 이동 | 지역 목록, 배경 교체, 지역 정보 패널, ↑↓ / 정세판 / 신앙 깃발 |
| 체계 system | 인쇄된 규칙서 | 종이, 장 번호, 굵은 괘선 표, 도장, 검은 페이지 한 장 |
| 현실 reality | 2047년 기기 | 잠금 화면 시계, 알림, 유리 카드 앱 |
| 시작 start | 새 게임 | 슬롯 3개 → 크랙 출력 견본, 조작 안내 |

참고: Mörk Borg(규칙서의 인쇄물 감각, 거친 크기 대비), Cyberpunk 2077 사이트(HUD, 잘린 모서리, 압축 대문자).

## 색

- 게임 화면: 먹색 `void` 바탕에 미색 글자. 강조는 **신호 빨강 `signal` 하나**. 버튼, 현재 위치, 사망, 사변.
- 청록 `hud`는 게임 시스템 메시지와 벨라트 시각에만. 히든직은 보라 `hidden`. 등급색은 등급 칩에만.
- 그림은 **원래 색 그대로** 크게. 노랑 덧칠이나 이중톤 금지. 어둡게 깔 때만 그라데이션과 밝기 조정.
- 규칙서는 종이색 `paper` + 잉크 + 인쇄 빨강. 현실은 밝은 유리(`os-*`).

## 글꼴

- 한글 제목: Pretendard 900, 자간 -0.055em 이하로 바짝.
- 숫자·영문 라벨·HUD: Barlow Condensed(기울임 900은 레벨, 슬롯 번호, 시계).
- 시스템 문구: Nanum Gothic Coding. 대사·인용·신 이름: Hahmlet.

## 공용 부품

- 상단 HUD: 로고, 서버 표시, 탭(숫자 키 1~5), 현실/벨라트 시계, ESC 메뉴.
- `.pnl`: 반투명 패널, 모서리 두 곳에 꺾쇠, 머리줄(영문 라벨 + 오른쪽 보조).
- `.btn`: 빨강, 오른쪽 아래 모서리 잘림. 올리면 미색으로 뒤집힌다.
- `.key`: 키캡. 조작 힌트는 언제나 키캡으로.

## 움직임

- 장면 단위 등장(위로 22px + 투명도). 큰 제목에 clip-path 숨김을 쓰지 않는다(화면 감지가 깨진다).
- 자동 순환(채팅, 히든직 알림, 사변 단계, 사망 카운트)은 화면에 보일 때만 돈다.
- 움직임 줄이기 설정이면 모두 멈추고 최종 상태를 보여 준다.

## 문구

**설명 문장을 쓰지 않는다**(작가님: "~다. 설명 빼, 매력을 보여 줘"). 타이틀은 ILEON 그 자체. 장면은 그림과 이름, 숫자, 게임 UI 문구로만 말한다. 세계 규칙(원주민은 죽으면 끝 등)을 표어로 내걸지 않는다. 설명문을 나열하지 않는다. 짧게 끊고 문장 끝을 섞는다(명사 끝, ~지, ~고, 물음). 게임 UI 문구(시스템 알림, 버튼)는 게임 말투 그대로.
