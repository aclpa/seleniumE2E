🚀 ERP E2E Automation Suite
"복잡한 Shadow DOM 구조와 동적 인터랙션을 100% 자동화한 Selenium 테스트 프레임워크"

📌 Project Overview

이 프로젝트는 웹 애플리케이션 ERP의 핵심 기능을 검증하기 위해 설계된 Python 기반 E2E(End-to-End) 자동화 테스트 솔루션입니다. 단순한 녹화/재생 방식이 아닌, Page Object Model(POM) 설계 패턴을 고려한 구조와 재귀적 탐색 알고리즘을 통해 유지보수성이 높고 견고한 테스트 코드를 구현했습니다.

특히, 자동화가 까다로운 Shadow DOM 내부 요소 제어와 Drag & Drop 인터랙션을 완벽하게 구현하여 수동 테스트 시간을 획기적으로 단축하는 것을 목표로 했습니다.

🛠 Tech Stack & Tools

Category	Technology	Usage
Language		전체 테스트 스크립트 로직 구현
Automation		브라우저 제어 및 사용자 동작 시뮬레이션
Data Gen		테스트 실행 시마다 랜덤 데이터(이메일, 이름 등) 자동 생성
Driver		webdriver-manager를 통한 드라이버 버전 자동 관리


💡 Key Features & Challenges Solved

이 프로젝트에서 해결한 주요 기술적 챌린지와 핵심 기능입니다.

1. Advanced Shadow DOM Handling (Shadow DOM 제어)

문제: Authentik SSO 로그인 페이지와 같은 최신 웹 컴포넌트들이 Shadow Root로 캡슐화되어 있어 일반적인 Selenium find_element로는 접근이 불가능했습니다.

해결: 재귀 함수(get_shadow_element_v4)를 직접 구현하여, 중첩된 Shadow DOM(Nested Shadow Roots)을 뚫고 들어가 요소를 찾아내도록 로직을 설계했습니다.

코드 하이라이트:

Python

# 다중 Shadow Root를 뚫고 들어가는 재귀 탐색 로직
def get_shadow_element_v4(self, selectors):
    element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selectors[0])))
    for selector in selectors[1:]:
        shadow_root = element.shadow_root
        # ... (Retry Logic) ...
        element = shadow_root.find_element(By.CSS_SELECTOR, selector)
    return element
2. Complex User Interactions (Drag & Drop)

기능: 칸반 보드(Kanban Board)에서 이슈 카드를 이동시키는 시나리오 구현.

기술: Selenium의 ActionChains 클래스를 활용하여 마우스 클릭(Hold) → 이동(Move) → 놓기(Release) 동작을 정교하게 제어했습니다.

3. Dynamic Data Generation (동적 데이터 생성)

기능: 테스트를 반복 실행할 때마다 "이미 존재하는 이메일입니다" 에러를 방지하기 위해 Faker 라이브러리를 도입했습니다.

효과: 매번 새로운 사용자 이름, 이메일, 프로젝트 키를 생성하여 독립적인 테스트 환경을 보장합니다.

4. Robust Sync Strategy (동기화 전략)

기술: time.sleep을 최소화하고 WebDriverWait와 ExpectedConditions(EC)를 적극 사용하여, 네트워크 속도나 렌더링 지연에 상관없이 테스트가 안정적으로 수행되도록 구현했습니다.

5. Test Isolation & State Management (테스트 격리 및 상태 관리)

문제: E2E 테스트 특성상 이전 테스트의 로그인 세션이나 데이터가 남아있으면 다음 테스트가 실패(Flaky Test)할 가능성이 높았습니다.

해결: 각 테스트 케이스(tc_xx) 실행 종료 시 Teardown 루틴(Cookie 및 LocalStorage 초기화)을 강제하여 테스트 환경을 항상 'Clean State'로 리셋하도록 설계했습니다.

효과:

테스트 간의 상호 의존성(Dependency)을 제거하여, 특정 테스트가 실패하더라도 나머지 테스트는 정상 수행됩니다.

필요에 따라 tc_01, tc_09 등 특정 케이스만 개별적으로 실행해도 문제없이 동작하도록 독립성을 확보했습니다.

🧪 Test Scenarios (Coverage)

총 11개의 핵심 비즈니스 로직에 대한 테스트 케이스(TC)를 커버합니다.

TC ID	Scenario	Description	Outcome
TC-01	회원가입	랜덤 생성된 유저 정보로 신규 가입 프로세스 검증	✅ Pass
TC-02	중복 가입 방지	기가입된 이메일 입력 시 가입 차단 여부 검증	✅ Pass
TC-03	로그인 실패	잘못된 비밀번호 입력 시 에러 메시지 노출 검증	✅ Pass
TC-04	정상 로그인	유효한 계정으로 로그인 후 대시보드 진입 확인	✅ Pass
TC-05	프로필 수정	사용자 이름 및 전화번호 변경 후 성공 메시지 검증	✅ Pass
TC-06	팀 생성	새로운 팀 생성 및 멤버 초대 로직 검증	✅ Pass
TC-07	프로젝트 생성	프로젝트 키(Key)와 이름, 팀 할당 기능 검증	✅ Pass
TC-08	스프린트 생성	프로젝트 내 신규 스프린트 생성 및 상태 설정	✅ Pass
TC-09	이슈 생성	버그(Bug) 타입의 이슈 티켓 생성 검증	✅ Pass
TC-10	칸반 보드 이동	Drag & Drop으로 이슈 상태 변경(To Do → In Progress)	✅ Pass
TC-11	로그아웃	세션 종료 및 로그인 페이지 리다이렉트 확인	✅ Pass


Sheets로 내보내기

💻 How to Run

로컬 환경에서 이 테스트 스위트를 실행하는 방법입니다.

1. 환경 설정 (Prerequisites)

Bash

# 필수 라이브러리 설치
pip install selenium webdriver-manager faker
2. 테스트 실행

Bash

# 스크립트 실행
python selenium_test.py
3. 결과 확인

콘솔 로그를 통해 각 TC별 Pass/Fail 여부가 실시간으로 출력됩니다.

에러 발생 시 error_screen.png 스크린샷이 자동으로 저장되어 디버깅을 돕습니다.

📧 Contact

Role: QA Automation Engineer

Focus: Test Automation, CI/CD Integration, Quality Assurance
