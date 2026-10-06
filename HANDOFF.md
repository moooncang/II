# 일레온 사이트 인수인계

새 세션은 이 문서를 먼저 읽고 작가님 지시를 기다린다. 기준일 2026-10-06.

## 작가님과 일하는 방식

- 호칭은 '작가님', 존댓말. 답은 짧고 실무적으로, 변경점만.
- 작가님은 자주, 정확하게 정정한다. 처음 해석을 고집하지 말고 바로 반영.
- 고친 결과는 main에 커밋·푸시까지 하고, 무엇이 바뀌었는지 한두 줄로 보고한다.
- 화면 문구에 줄표(—, –) 금지. 생성기가 빌드 때 검사한다.

## 저장소와 배포

- 저장소: https://github.com/moooncang/II (main). `site-build` 브랜치도 main과 같이 맞춰 둔다.
- 배포: GitHub Pages(main, 루트). `.nojekyll` 있음. 주소: https://moooncang.github.io/II/
  - Pages 켜기는 작가님이 설정에서 직접 했다(이 환경의 GitHub API로는 Pages 설정 불가).
- 사이트는 생성기로 만든다: `python3 _build/build.py` → 저장소 최상단 html 22개를 다시 쓴다.
  - `_build/data.py`: 인물 15인·지역·대립선·신앙·히든직 등 모든 문구와 데이터, 배경 원안 대응표(BGD), 크랙 링크(`CRACK`, 아직 빈 값).
  - `_build/build.py`: 페이지 틀. 표지(index), 홈, 대륙, 인물(+char/15개), 체계, 현실, 시작.
  - `assets/css/style.css`, `assets/js/main.js`, 글꼴은 `assets/fonts`(Pretendard·Barlow Condensed·Hahmlet·Nanum Gothic Coding 자체 포함).
- html을 손으로 고치지 말고 data.py/build.py를 고친 뒤 빌드한다.

## 그림 (전부 저장소 images/, WebP 압축본)

- `images/bg-draft/` 배경 원안 43장(HUD 없음, 2048×585). 파일명이 시드 숫자라 `data.py`의 `BGD`로 코드에 대응(그림 비교로 1:1 확인).
- `images/B/` 지역 HUD가 든 배경 43장. 시작 페이지의 크랙 출력 견본(프롤로그)에서만 쓴다.
- `images/sample/` 인물 견본 20장(A~O, A2~E2, 1280×883). 카드·인물 상세 상단·현실 얼굴.
- `images/CS/` 인물 상황 그림 215장(게임 A~O_1~11, 현실 A2~E2_1~10). 표정 보기.
- 배경 코드 ER=카르시온 수도 에르카시아, SL=미르젠 항구 도시 셀라운(작가님 확인).

## 현재 디자인 (3차, 2026-10-06)

- 사이트 전체가 일레온 게임 클라이언트. 표지=로딩, 홈=타이틀+장면, 인물=캐릭터 선택, 상세=프로필 창, 대륙=지역 이동, 체계=인쇄된 규칙서(종이), 현실=2047 기기 화면(밝은 유리), 시작=새 게임 슬롯. 자세한 기준은 DESIGN.md.
- 먹색 + 신호 빨강 하나. 청록은 시스템·벨라트 시각, 보라는 히든직. 그림은 원색 그대로.
- 글꼴: Pretendard 900(제목), Barlow Condensed(숫자·라벨), Nanum Gothic Coding(시스템), Hahmlet(대사·신 이름).
- 조작: 1~5 탭 이동, ESC 메뉴, Enter 채팅, M 효과음, 지역 ↑↓, 표정 ← →, 인물 Q/E.
- 채팅: 모든 페이지 오른쪽 아래 채팅 버튼(`chat_widget`). 대화 원본은 `data.py`의 `CHAT`. 닫혀 있으면 새 대화 수가 빨간 배지로, 입력하면 '당신'으로 올라간다(저장 없음).
- 효과음: `assets/sfx/` 9개(enter·hover·click·menu·chat·select·travel·flip·reveal, mp3). ElevenLabs 커넥터(text to sound v2)로 만들고 ffmpeg로 자르고 맞춤. 작업 흐름 이름 'ILEON site SFX'. `main.js`의 `sfx`가 Web Audio로 재생, 첫 클릭·키 입력 뒤에만 울린다. 상단과 표지의 SFX 버튼이나 M 키로 끄고 켜며 localStorage(`ileon-sfx`)에 기억. 호버 틱은 마우스에서만, 채팅은 열 때와 보낼 때만(자동 메시지엔 소리 없음), 히든직은 처음 보일 때와 다음 버튼.
- 모바일: 터치에서는 등장 효과·장면 맞춤 스크롤·흐림·배경 움직임을 끈다(`.touch`, `(hover:none)`). 안쪽 이중 스크롤 금지.
- 폐기한 시안: 1차 밤 남색+청록, 2차 먹색+형광 노랑 진(작가님: "이전 디자인에서 타파 못 함, 완전히 갈아치워"). 같은 문법으로 돌아가지 말 것.
- 참고 사이트(morkborg.com/preview, cyberpunk.net)와 figma.com 파일 받기는 이 환경 네트워크에서 막혀 있다. 열려면 환경 설정의 허용 도메인에 추가해야 한다.

## 지켜야 할 것 (PRODUCT.md, _설정/)

- 설정 문서가 정답. 미결 사항은 단정하지 않는다: 할라크족이 봉인을 지켜온 쪽인지, '대륙 연대기' 명칭(사이트에서 쓰지 않음), 줄리엣이 제3환에 매달리는 이유, 무명 정체 공개 시점 등.
- 지어내지 않는 것: 로고, BGM, 지도, 크랙 링크, 실적·후기·이용자 수.
- 화면에서 지운 것: "문창놈 · 크랙 채팅봇", "수록 그림은 생성물" 같은 안내 문구(작가님 요청).
- 벨라트 시각의 기준점(현실 자정 = 벨라트 0시)은 임의로 둔 것.

## 도구

- 스킬: `.claude/skills/` 의 impeccable, emil-design-eng, design-taste-frontend.
- Playwright MCP는 크롬 경로 문제로 안 뜬다. 대신 `npm root -g`의 playwright를 node로 직접 쓰고 executablePath는 `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`. 로컬 확인은 `python3 -m http.server`로 띄워서(file://는 글꼴·마스크가 막힌다).
- MCP: `.mcp.json`에 Playwright(헤드리스)를 프로젝트 범위로 등록. Figma는 claude.ai 커넥터로 연결됨.
- 화면 점검: 로컬 파일을 Playwright로 열어 1440·390 폭으로 찍는다. 지연 로딩 그림은 eager로 바꾸고 스크롤한 뒤 찍어야 다 나온다.

## 남은 일

- 작가님이 실제 브라우저에서 보고 줄 피드백 반영(애니메이션 체감, 문구 말투).
- 크랙 작품 링크가 정해지면 `data.py`의 `CRACK`만 채우고 빌드.
- 필요하면 DESIGN.md를 최신 개편 기준으로 다시 쓰기.
