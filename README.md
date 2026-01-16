## 🚀 ERP System E2E Automation Framework

복잡한 웹 컴포넌트(Shadow DOM) 구조를 가진 ERP 시스템의 핵심 기능을 검증하기 위해 구축한 **Python + Selenium 기반의 테스트 자동화 프레임워크**입니다.

## 📌 Project Overview

본 프로젝트는 유지보수성이 낮은 절차적 스크립트 방식의 한계를 극복하기 위해 **Page Object Model (POM)** 디자인 패턴을 적용했습니다. 이를 통해 화면 요소(Page)와 비즈니스 로직, 그리고 테스트 시나리오(Test)를 명확히 분리하여 코드 재사용성을 극대화했습니다.

특히, 일반적인 Selenium 메서드로는 접근이 어려운 **Shadow DOM** 내부 요소 제어를 위해 재귀 탐색 로직을 유틸리티화하였으며, **Pytest** 프레임워크를 도입하여 테스트 수명 주기(Setup/Teardown)를 체계적으로 관리합니다.


## 🎥 Demo Preview
### TC_04 로그인 테스트 
![alt text](media/tc4로그인테스트.gif)
### TC_06 팀 생성 테스트
![alt text](media/tc6팀생성.gif)
### TC
![TC](/media/seleniumtc.png)

## 🏗️ Project Structure

유지보수를 위해 소스 코드와 테스트 코드를 명확히 분리한 디렉토리 구조입니다.

```bash
seleniumE2E-12/
├── src/
│   ├── config/             # (코드 내 import로 확인됨, 전역 설정)
│   └── pages/              # Page Object Model (화면별 요소 및 동작 정의)
│       ├── base_page.py    # 공통 메서드 (Shadow DOM 탐색, Wait 로직 등)
│       ├── dashboard_page.py # 대시보드 및 상단/사이드 메뉴 로직
│       ├── issue_page.py   # 이슈 관리 페이지 로직
│       ├── kanban_page.py  # 칸반 보드 페이지 로직
│       ├── login_page.py   # 로그인, 회원가입, 에러 메시지 처리
│       ├── profile_page.py # 프로필 정보 수정 로직
│       ├── project_page.py # 프로젝트 생성 및 관리 로직
│       ├── sprint_page.py  # 스프린트 관리 로직
│       └── team_page.py    # 팀 관리 페이지 로직
├── tests/                  # 실제 테스트 시나리오 (Pytest 기반)
│   ├── test_auth.py        # 로그인, 회원가입, 예외 케이스 TC
│   ├── test_project.py     # 프로젝트 관련 TC
│   └── test_user_flow.py   # 프로필 수정, 로그아웃 등 사용자 흐름 TC
├── legacy/                 # (Legacy) 기존 Selenium 테스트 스크립트
│   └── selenium_test.py
├── media/                  # 테스트 결과 스크린샷 및 이미지 리소스
├── node_modules/           # Node.js 라이브러리 (JavaScript 의존성)
├── conftest.py             # Pytest Fixture (브라우저 실행/종료, Faker 설정)
├── package.json            # Node.js 프로젝트 설정
├── package-lock.json       # Node.js 의존성 잠금 파일
├── .gitignore              # Git 제외 파일 설정
└── README.md               # 프로젝트 문서
```

## 💡 Key Features & Challenges Solved

### 이 프로젝트에서 중점적으로 다룬 기술적 챌린지와 해결 전략입니다.

- Advanced Shadow DOM Handling
Challenge: Authentik SSO 로그인 페이지 등 최신 웹 컴포넌트가 Shadow Root로 캡슐화되어 있어, 기본 find_element로는 접근이 불가능함.

Solution: base_page.py 내에 재귀 함수(get_shadow_element)를 구현. 중첩된 Shadow DOM(Nested Shadow Roots) 구조를 순차적으로 진입하여 요소를 찾아내도록 추상화.

- 해결: 재귀 함수(get_shadow_element_v4)를 구현하여, 중첩된 Shadow DOM(Nested Shadow Roots)을 뚫고 들어가 요소를 찾아내도록 로직을 설계했습니다.

Solution: 페이지의 Locator와 행위(Method)를 src/pages 클래스로 분리. UI 변경 시 해당 Page Class만 수정하면 되도록 개선.

 - Synchronization & Stability (동기화 전략)
Challenge: 네트워크 지연이나 렌더링 속도 차이로 인한 Flaky Test(간헐적 실패) 발생.

Solution: time.sleep() 사용을 지양하고, WebDriverWait와 ExpectedConditions를 활용한 명시적 대기(Explicit Wait)를 적용하여 안정성 확보.

- Dynamic Data Generation
Challenge: 반복 실행 시 데이터 중복(Duplicate Entry) 에러 발생.

Solution: Faker 라이브러리를 활용하여 매 테스트마다 고유한 이메일, 이름, 전화번호를 동적으로 생성하여 테스트 멱등성 보장.

- Complex Interactions (Drag & Drop)
Challenge: 칸반 보드 내 이슈 카드 이동과 같은 복잡한 사용자 인터랙션 검증 필요.


**4. Test Isolation & State Management (테스트 격리 및 상태 관리)**

- 문제: E2E 테스트 특성상 이전 테스트의 로그인 세션이나 데이터가 남아있으면 다음 테스트가 실패(Flaky Test)할 가능성이 높았습니다.

- 해결: 각 테스트 케이스(tc_xx) 실행 종료 시 Teardown 루틴(Cookie 및 LocalStorage 초기화)을 강제하여 테스트 환경을 항상 'Clean State'로 리셋하도록 설계했습니다.

- 효과: 테스트 간의 상호 의존성(Dependency)을 제거하여, 특정    테스트가 실패하더라도 나머지 테스트는 정상 수행됩니다.

- 필요에 따라 tc_01, tc_09 등 특정 케이스만 개별적으로 실행해도 문제없이 동작하도록 독립성을 확보했습니다.

## 🛠 Tech Stack & Tools

- Language	Python 3.11+	전체 자동화 로직 구현
- Framework	Pytest	테스트 실행, Fixture 및 Assertions 관리
- Automation	Selenium WebDriver	브라우저 제어 및 사용자 인터랙션 시뮬레이션
- Driver Mgmt	Webdriver-manager	브라우저 드라이버 버전 자동 관리
- Data Gen	Faker	테스트용 더미 데이터 생성

## 📧 Contact

Role: QA Automation Engineer

Focus: Test Automation, CI/CD Integration, Quality Assurance

test program = 팀플제작 ERP https://github.com/DevFlow-ERP
