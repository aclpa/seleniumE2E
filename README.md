# ERP System E2E Automation & Load Testing Framework

이 프로젝트는 Shadow DOM 구조를 가진 ERP 웹 애플리케이션을 검증하기 위한 **Selenium 기반 E2E 테스트** 및 **Locust 기반 부하 테스트** 자동화 프레임워크입니다.

## 📌 주요 기능 및 특징 (Key Features)

### 1. 테스트 자동화 (E2E Automation)
- **Hybrid Test Approach:** 테스트 데이터 셋업(Team, Project, Issue 생성)은 API를 사용하고, 실제 UI 검증은 Selenium을 사용하는 하이브리드 방식을 채택하여 테스트 속도와 안정성을 확보했습니다.
- **Advanced Shadow DOM Handling:** `base_page.py` 내 재귀 탐색 로직(`get_shadow_element`)을 구현하여 중첩된 Shadow Root 내부의 요소를 제어합니다.
- **Auto Wait & Retry:** `StaleElementReferenceException` 발생 시 자동으로 재시도하며, 모든 상호작용 전 `WebDriverWait`를 통해 요소의 가시성을 보장합니다.

### 2. 테스트 환경 및 데이터 관리
- **Clean State Architecture:** Pytest Fixture의 `yield` 패턴을 활용하여 테스트 실행 후 생성된 데이터를 즉시 삭제(Teardown)합니다.
- **Bulk Cleanup Script:** 테스트 중단 등의 이유로 잔존하는 더미 데이터(Locust_, Auto_, Team_ 접두사 포함)를 일괄 삭제하는 `cleanup_all.py` 유틸리티를 포함합니다.
- **Dynamic Data Generation:** `Faker` 라이브러리를 사용하여 테스트 실행 시마다 고유한 사용자 및 프로젝트 데이터를 생성합니다.

### 3. 부하 테스트 (Load Testing)
- **Locust Integration:** 기존 구현된 `APIClient` 로직을 재사용하여 Locust 부하 테스트 시나리오를 구축했습니다.
- **Scenarios:** 사용자별 고유 프로젝트 생성, 이슈 생성 및 삭제 반복, 대시보드 조회 트래픽을 시뮬레이션합니다.

## 🏗️ 디렉토리 구조 (Directory Structure)

```bash
seleniumE2E-cleanup/
├── src/
│   ├── config/             # 환경 변수 및 전역 설정
│   ├── pages/              # POM (Page Object Model) 클래스 모음
│   │   ├── base_page.py    # 공통 메서드 (Shadow DOM 탐색, Wait, Click, Drag&Drop)
│   │   ├── login_page.py   # SSO 로그인 및 회원가입 처리
│   │   └── ...             # 각 페이지별(Dashboard, Kanban 등) 로직
│   └── utils/
│       └── api_client.py   # REST API 호출 클라이언트 (Requests 기반)
├── tests/                  # Pytest 기반 테스트 케이스
│   ├── test_auth.py        # 인증 관련 테스트
│   ├── test_project.py     # 프로젝트 CRUD 테스트
│   └── test_user_flow.py   # 프로필 수정 및 사용자 흐름 테스트
├── cleanup_all.py          # 테스트 잔존 데이터 일괄 삭제 스크립트
├── conftest.py             # Pytest Fixtures (Driver 설정, API 기반 데이터 셋업/티어다운)
├── locustfile.py           # Locust 부하 테스트 스크립트
└── requirements.txt        # (Python 의존성 파일 - 필요 시 생성 권장)
```

## 🎥 Demo Preview
### TC_04 로그인 테스트 
![alt text](media/tc4로그인테스트.gif)
### TC_06 팀 생성 테스트
![alt text](media/tc6팀생성.gif)
### TC
![TC](/media/seleniumtc.png)


## 부하 테스트 결과 분석
### locust 차트
![alt text](<media/locust 차트.png>)

- 현상: 동시 접속자 수가 증가함에 따라 응답 시간(Response Time)이 선형적으로 증가하지 않고, 기하급수적으로 폭발함.

- 임계점(Breakpoint): 그래프 앞부분 약 50~100명 구간부터 응답 시간이 튀기 시작함. 

- 장애 상황: 접속자 500명 도달 시, 최대 응답 지연이 **270초(4.5분)**까지 발생하며 서비스 불능 상태(Unresponsive)에 빠짐.

- 결론: 현재 서버 스펙 및 설정으로는 동시 접속자 50명 수준이 안정적인 최대 허용 범위임.

## 🛠 기술 스택 (Tech Stack)
- Language,Python 3.11+,전체 프레임워크 구현
- Test Runner,Pytest,"테스트 실행, Fixture 관리, Assertion"
- Web Driver,Selenium WebDriver,브라우저 제어 (Chrome)
- postman API 사전 테스트
- Load Test,Locust,API 부하 테스트 및 모니터링
- HTTP Client,Requests,테스트 데이터 셋업용 API 호출
- Data Gen,Faker,더미 데이터 생성

## 🚀 실행 방법 (How to Run)
### 1. 사전 준비

- Python 3.11 이상 및 Chrome 브라우저가 설치되어 있어야 합니다.

### 1. 의존성 설치

- pip install pytest selenium webdriver-manager requests faker locust

### 2. E2E 테스트 실행

- Pytest를 사용하여 시나리오 테스트를 수행합니다.

### 전체 테스트 실행
- pytest tests/

### 특정 테스트 파일 실행
- pytest tests/test_user_flow.py

### 브라우저 헤드리스 모드 해제 및 상세 로그 확인 (옵션)
- pytest tests/ -s

### 3. 부하 테스트 실행 (Locust)

- Locust 웹 인터페이스를 통해 부하 테스트를 수행합니다.
- locust -f locustfile.py
- 실행 후 브라우저에서 http://localhost:8089 접속하여 유저 수(Users)와 생성 속도(Spawn rate)를 설정하고 테스트를 시작합니다.
### 4. 잔존 데이터 정리

- 테스트 실패나 강제 종료로 인해 서버에 남은 더미 데이터를 정리합니다.
- python cleanup_all.py
- Auto, Locust, Team_ 등이 포함된 이름을 가진 팀과 하위 프로젝트를 찾아 삭제합니다.

## ⚠️ 주의 사항
- SSO 로그인: 로그인 페이지가 Shadow DOM 및 iframe을 포함한 복잡한 구조로 되어 있어, login_page.py의 선택자 수정 시 주의가 필요합니다.

- 드라이버 버전: webdriver_manager를 사용하여 Chrome Driver 버전을 자동으로 맞추지만, 로컬 Chrome 브라우저 버전과 크게 차이가 날 경우 업데이트가 필요할 수 있습니다.
