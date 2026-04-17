# Hotaru's Daily Attendance

[English](README.md) | **한국어** | [日本語](README.ja.md)

Windows 로그인 시 지정한 게임 출석 페이지를 **하루에 한 번** 자동으로 브라우저에서 열어주는 소형 유틸리티.

## 특징

- Windows 시작 프로그램에 등록되어 로그인 시 자동 실행
- **하루 1회만 실행** — 로그아웃·재로그인해도 중복으로 열지 않음
- 간단한 GUI로 게임 선택 및 커스텀 URL 추가

## 설치

1. [Releases](../../releases)에서 최신 `HTR_DA.exe` 다운로드
2. `HTR_DA.exe` 실행 → 원하는 게임 체크 → **Install / Update** 클릭
3. 다음 Windows 로그인부터 자동 실행됨

## 커스텀 게임 추가

GUI에서 **+ Add Custom Game** 버튼을 눌러 이름과 URL을 입력하세요.

추가한 커스텀 게임을 삭제하려면 해당 항목 옆의 **×** 버튼을 누릅니다.

## 제거

- GUI 실행 후 **Uninstall** 버튼 클릭, 또는
- 커맨드라인: `HTR_DA.exe --uninstall`

## 파일 위치

| 용도 | 경로 |
|------|------|
| 설정 | `%APPDATA%\HTR_AttendanceAuto\config\` |
| 하루 1회 실행 플래그 | `%APPDATA%\HTR_AttendanceAuto\flags\` |
| 설치된 실행 파일 | `%APPDATA%\HTR_AttendanceAuto\bin\HTR_DA.exe` |
| 시작 프로그램 등록 | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\HTR_daily_attendance.vbs` |

## 동작 방식

Windows에 로그인하면, 프로그램은 **오늘 이미 출석 페이지를 열었는지** 먼저 확인합니다.

- 아직 열지 않았다면 → 설정된 출석 페이지들을 기본 브라우저에서 엽니다.
- 이미 열었다면 → 중복 실행 없이 즉시 종료합니다.

별도의 백그라운드 서비스나 작업 스케줄러 없이, 단순한 파일 기반 방식으로 "하루 1회" 동작을 보장합니다.

## 정책 관련 안내

이 도구는 기본 브라우저에서 출석 페이지를 여는 동작만 수행하며, 사용자를 대신해 로그인하거나 버튼을 누르거나 데이터를 전송하지 **않습니다**.

다만 특정 페이지를 이 도구로 여는 것이 해당 사이트의 이용약관이나 운영 정책에 위배된다고 판단되시면 [Issue로 알려주세요](../../issues). 해당 게임을 기본 카탈로그에서 제거하겠습니다.

## 라이선스

MIT

## 기여하기

기여는 언제나 환영합니다. 아래 순서로 진행해 주세요.

1. 이 저장소를 Fork
2. 새 브랜치 생성
3. 변경 사항 커밋
4. Pull Request 생성

기능 추가나 구조 변경처럼 비교적 큰 변경의 경우, 먼저 Issue를 통해 논의해 주시면 더 원활하게 진행할 수 있습니다.
