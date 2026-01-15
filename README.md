DevFlow Selenium E2E Automation Test
이 프로젝트는 DevFlow 웹 애플리케이션의 주요 기능을 검증하기 위한 Selenium Python 기반의 자동화 테스트 스크립트입니다. 회원가입부터 로그인, 프로젝트/팀 생성, 칸반 보드 조작까지 사용자의 핵심 시나리오를 자동으로 수행하고 검증합니다.

📋 주요 기능
Shadow DOM 처리: get_shadow_element_v4 메서드를 통해 복잡한 Shadow DOM 내부의 요소(특히 Authentik SSO 로그인 화면)를 자동으로 탐색하고 제어합니다.

데이터 자동 생성: Faker 라이브러리를 사용하여 테스트 실행 시마다 랜덤한 사용자 정보, 프로젝트명 등을 생성해 중복을 방지합니다.

시나리오 기반 테스트: 회원가입, 로그인, 프로필 수정, 프로젝트 관리 등 11가지의 핵심 테스트 케이스를 포함합니다.

🛠️ 사전 요구 사항 (Prerequisites)
이 스크립트를 실행하기 위해서는 다음 환경이 필요합니다.

Python 3.x

Chrome Browser (최신 버전 권장)

테스트 대상 애플리케이션이 로컬 환경에서 실행 중이어야 합니다.

메인 앱: http://localhost:8080

인증 서버(Authentik): http://localhost:9000

📦 설치 (Installation)
이 리포지토리를 클론하거나 다운로드합니다.

필요한 Python 라이브러리를 설치합니다.

Bash

pip install selenium webdriver-manager faker
참고: package.json 파일은 테스트 대상이 되는 프론트엔드 프로젝트의 의존성(예: vuedraggable, sortablejs)을 나타내며, 이 Python 테스트 스크립트 실행을 위해 npm install을 할 필요는 없습니다.

🚀 실행 방법 (Usage)
터미널에서 아래 명령어를 실행하여 테스트를 시작합니다.

Bash

python selenium_test.py
스크립트가 실행되면 Chrome 브라우저가 자동으로 열리고 테스트 케이스들이 순차적으로 수행됩니다. 테스트 종료 후 브라우저는 자동으로 닫힙니다.

🧪 테스트 시나리오 (Test Cases)
스크립트(selenium_test.py)에는 총 11개의 테스트 케이스가 정의되어 있습니다.

TC ID	테스트 명	설명
TC-01	Signup	Faker를 이용해 랜덤 생성된 정보로 회원가입을 시도하고 성공 여부를 검증합니다.
TC-02	Signup Duplicate	이미 가입된 이메일로 중복 가입을 시도하여 차단되는지 확인합니다.
TC-03	Password Fail	잘못된 비밀번호 입력 시 에러 메시지("Invalid password")가 출력되는지 확인합니다.
TC-04	Login	정상적인 이메일과 비밀번호로 로그인을 시도하고 대시보드로 이동하는지 확인합니다.
TC-05	Profile Update	프로필 페이지에서 전화번호와 이름을 수정하고 "updated successfully" 메시지를 검증합니다.
TC-06	Team Create	새로운 팀을 생성하고 멤버를 초대한 뒤 팀 목록에 표시되는지 확인합니다.
TC-07	Project Create	새로운 프로젝트를 생성(키, 팀 지정)하고 생성을 검증합니다.
TC-08	Sprint Create	프로젝트 내에서 새로운 스프린트를 생성합니다.
TC-09	Issue Create	버그(Bug) 타입의 새로운 이슈를 생성합니다.
TC-10	Kanban Board	칸반 보드에서 이슈 카드를 Drag & Drop 하여 상태(예: In Progress)를 변경합니다.
TC-11	Logout	로그아웃 버튼을 클릭하여 로그인 페이지로 리다이렉트 되는지 확인합니다.


⚙️ 설정 (Configuration)
스크립트 내 DevFlowTestRunner 클래스의 __init__ 메서드에서 주요 설정을 변경할 수 있습니다.

Headless 모드: 브라우저 화면 없이 실행하려면 options.add_argument("--headless") 주석을 해제하세요.

테스트 계정: self.existing_email, self.existing_password 변수에서 로그인 테스트에 사용할 기본 계정 정보를 수정할 수 있습니다.

URL: self.base_url 및 self.authentik_url 변수에서 테스트 환경의 주소를 변경할 수 있습니다.

⚠️ 문제 해결 (Troubleshooting)
요소를 찾을 수 없음 (NoSuchElementException): 네트워크 속도나 로딩 지연으로 인해 발생할 수 있습니다. time.sleep() 시간을 늘리거나 WebDriverWait 설정을 조정해보세요.

에러 스크린샷: 테스트 실패 시 예외가 발생하면 지정된 경로(C:/Users/.../error_screen.png)에 스크린샷이 저장됩니다. 경로를 본인의 환경에 맞게 수정해주세요.
