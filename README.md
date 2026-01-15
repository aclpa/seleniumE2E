## 🚀 ERP System E2E Automation Framework

복잡한 웹 컴포넌트(Shadow DOM) 구조를 가진 ERP 시스템의 핵심 기능을 검증하기 위해 구축한 **Python + Selenium 기반의 테스트 자동화 프레임워크**입니다.

## 📌 Project Overview

본 프로젝트는 유지보수성이 낮은 절차적 스크립트 방식의 한계를 극복하기 위해 **Page Object Model (POM)** 디자인 패턴을 적용했습니다. 이를 통해 화면 요소(Page)와 비즈니스 로직, 그리고 테스트 시나리오(Test)를 명확히 분리하여 코드 재사용성을 극대화했습니다.

특히, 일반적인 Selenium 메서드로는 접근이 어려운 **Shadow DOM** 내부 요소 제어를 위해 재귀 탐색 로직을 유틸리티화하였으며, **Pytest** 프레임워크를 도입하여 테스트 수명 주기(Setup/Teardown)를 체계적으로 관리합니다.


## 🏗️ Project Structure

유지보수를 위해 소스 코드와 테스트 코드를 명확히 분리한 디렉토리 구조입니다.

```bash
seleniumE2E-6/
├── src/
│   ├── config/             # URL, Timeout 등 전역 설정 관리
│   └── pages/              # Page Object Model (화면별 요소 및 동작 정의)
│       ├── base_page.py    # 공통 메서드 (Shadow DOM 탐색, Wait 로직 등)
│       ├── login_page.py   # 로그인/회원가입 페이지 로직
│       ├── dashboard_page.py # 대시보드 및 칸반보드 로직
│       └── profile_page.py # 프로필 수정 로직
├── tests/                  # 실제 테스트 시나리오 (Pytest 기반)
│   ├── test_auth.py        # 로그인, 회원가입, 중복 가입 방지 TC
│   └── test_user_flow.py   # 프로필 수정, 로그아웃 등 사용자 시나리오 TC
├── conftest.py             # Pytest Fixture (브라우저 실행/종료, Faker 설정)
├── requirements.txt        # 의존성 패키지 목록
└── README.md
```
## 🎥 Demo Preview

### **TC 이미지를 클릭하면 시연 영상을 볼 수 있습니다.**
[![테스트 결과 화면](/media/seleniumtc.png)](https://youtu.be/uwcIr0_jezI?si=90FvkfzObSI7YHkc)


## 💡 Key Features & Challenges Solved

### 이 프로젝트에서 중점적으로 다룬 기술적 챌린지와 해결 전략입니다.

- Advanced Shadow DOM Handling
Challenge: Authentik SSO 로그인 페이지 등 최신 웹 컴포넌트가 Shadow Root로 캡슐화되어 있어, 기본 find_element로는 접근이 불가능함.

Solution: base_page.py 내에 재귀 함수(get_shadow_element)를 구현. 중첩된 Shadow DOM(Nested Shadow Roots) 구조를 순차적으로 진입하여 요소를 찾아내도록 추상화.

- Page Object Model (POM) Implementation
Challenge: UI 변경 시 테스트 코드 전체를 수정해야 하는 유지보수 비용 발생.

Solution: 페이지의 Locator와 행위(Method)를 src/pages 클래스로 분리. UI 변경 시 해당 Page Class만 수정하면 되도록 개선.

 - Synchronization & Stability (동기화 전략)
Challenge: 네트워크 지연이나 렌더링 속도 차이로 인한 Flaky Test(간헐적 실패) 발생.

Solution: time.sleep() 사용을 지양하고, WebDriverWait와 ExpectedConditions를 활용한 명시적 대기(Explicit Wait)를 적용하여 안정성 확보.

- Dynamic Data Generation
Challenge: 반복 실행 시 데이터 중복(Duplicate Entry) 에러 발생.

Solution: Faker 라이브러리를 활용하여 매 테스트마다 고유한 이메일, 이름, 전화번호를 동적으로 생성하여 테스트 멱등성 보장.

- Complex Interactions (Drag & Drop)
Challenge: 칸반 보드 내 이슈 카드 이동과 같은 복잡한 사용자 인터랙션 검증 필요.

Solution: Selenium ActionChains 클래스를 활용하여 ClickAndHold → Move → Release 동작을 정교하게 제어.

## 🛠 Tech Stack & Tools

- Language	Python 3.11+	전체 자동화 로직 구현
- Framework	Pytest	테스트 실행, Fixture 및 Assertions 관리
- Automation	Selenium WebDriver	브라우저 제어 및 사용자 인터랙션 시뮬레이션
- Driver Mgmt	Webdriver-manager	브라우저 드라이버 버전 자동 관리
- Data Gen	Faker	테스트용 더미 데이터 생성

## 📧 Contact

Role: QA Automation Engineer

Focus: Test Automation, CI/CD Integration, Quality Assurance
