## 🚀 ERP System E2E Automation Framework
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 복잡한 웹 컴포넌트(Shadow DOM) 구조를 가진 ERP 시스템의 핵심 기능을 검증하기 위해 구축한  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Python + Selenium 기반의 테스트 자동화 프레임워크입니다.

## 📌 Project Overview
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 본 프로젝트는 Page Object Model (POM) 디자인 패턴을 적용하여 페이지 동작(Page Class)과 테스트 시나리오(Test Script)를 분리했습니다.  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 이를 통해 Shadow DOM 요소 제어, 대기 로직 등 공통 기능을 모듈화하고 테스트 코드의 가독성을 높였습니다.


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

## 🏗️ Project Structure

&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 유지보수를 위해 소스 코드와 테스트 코드를 명확히 분리한 디렉토리 구조입니다.

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

## 💡 Key Implementations
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 주요 기술적 구현 사항입니다.

- Shadow DOM 제어 (Recursive Search)

&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 기본 Selenium 메서드로 접근이 불가능한 중첩된 Shadow DOM(Nested Shadow Roots) 요소를 찾기 위해,  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; base_page.py 내에 재귀 탐색 로직(get_shadow_element)을 구현하여 접근성을 확보했습니다.

- 명시적 대기 (Explicit Wait)

&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 네트워크 지연 및 렌더링 속도 차이로 인한 테스트 실패를 방지하기 위해 time.sleep 대신  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; WebDriverWait와 ExpectedConditions를 사용하여 요소의 상태(Clickable, Visible)를 정확히 감지하도록 처리했습니다.

- 동적 데이터 생성 (Dynamic Data)

&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Faker 라이브러리를 활용하여 매 테스트 실행 시 고유한 이메일, 이름, 전화번호를 생성함으로써  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 중복 데이터로 인한 에러를 방지하고 테스트 멱등성을 보장했습니다.

- 테스트 환경 격리 (Test Isolation)

&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Pytest Fixture를 사용하여 브라우저의 수명 주기(Setup/Teardown)를 관리하고,  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 테스트 종료 시 세션을 정리하여 각 테스트 케이스가 독립적인 환경에서 수행되도록 구성했습니다.
## 🛠 Tech Stack
- Language: Python 3.11+

- Test Framework: Pytest

- Automation Library: Selenium WebDriver
 
- Driver Management: Webdriver-manager
 
- Data Generation: Faker

## 📧 Contact
- Role: QA Automation Engineer

- Focus: Test Automation, CI/CD Integration, Quality Assurance

- Repository: https://github.com/DevFlow-ERP
