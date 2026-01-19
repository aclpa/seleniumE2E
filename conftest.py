import pytest
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from faker import Faker
import time
# Config import 경로가 src.config.config 라고 가정합니다.
# 만약 경로 에러가 나면 sys.path.append를 사용해야 할 수도 있습니다.
try:
    from src.config.config import Config
except ImportError:
    # 혹시 모듈을 못 찾으면 현재 경로를 추가해 봅니다.
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
    from src.config.config import Config

from src.utils.api_client import APIClient

# ==========================================
# 🌐 Docker 환경 설정
# ==========================================
# selenium-chrome은 docker-compose.test.yml에 정의된 서비스 명입니다.
SELENIUM_GRID_URL = "http://selenium-chrome:4444/wd/hub"


@pytest.fixture(scope="session")
def fake():
    return Faker()


# ==========================================
# 🔌 API Client Fixtures (데이터 셋업용)
# ==========================================
@pytest.fixture(scope="session")
def api_client():
    """
    테스트 세션 동안 유지되는 API 클라이언트
    APIClient 내부에서 Config.API_URL을 참조하도록 구현되어 있어야 합니다.
    """
    client = APIClient()
    client.login()  # 세션 시작 시 1회 로그인
    return client


@pytest.fixture(scope="function")
def new_team(api_client, fake):
    t_name = f"Team_{fake.bothify(text='????')}"
    print(f"\n🏢 [Setup] 팀 생성 중: {t_name}")
    team = api_client.create_team(t_name)

    yield team
    
    try:
        api_client.delete_team(team["id"])
        print("   -> ✅ 팀 삭제 완료")
    except Exception as e:
        print(f"   -> ⚠️ 팀 삭제 실패: {e}")


@pytest.fixture(scope="function")
def new_project(api_client, fake, new_team):
    p_name = f"AutoProj_{fake.lexify(text='????')}"
    p_key = fake.lexify(text="???").upper()

    print(f"🏗️ [Setup] 프로젝트 생성 중: {p_name}")
    project = api_client.create_project(name=p_name, key=p_key, team_id=new_team["id"])

    yield project

    print(f"🗑️ [Teardown] 프로젝트 정리")
    try:
        api_client.delete_project(project["id"])
    except Exception as e:
        print(f"   -> ⚠️ 프로젝트 삭제 실패: {e}")


@pytest.fixture(scope="function")
def new_issue(api_client, new_project, fake):
    issue_title = f"AutoIssue_{fake.word()}_{fake.random_number(digits=3)}"
    print(f"\n📝 [Fixture] 이슈 생성: {issue_title}")

    issue = api_client.create_issue(project_id=new_project["id"], title=issue_title)

    yield issue

    try:
        api_client.delete_issue(issue["id"])
    except Exception as e:
        print(f"⚠️ 이슈 삭제 실패: {e}")


# ==========================================
# 🖥️ Selenium Driver Fixture (도커/로컬 통합)
# ==========================================
@pytest.fixture(scope="function")
def driver(request):
    """
    Docker Selenium Grid 연결 (재시도 로직 포함)
    """
    print(f"\n🚀 [Setup] Remote 브라우저 연결 시도: {SELENIUM_GRID_URL}")
    print(f"🔗 [Target] 테스트 대상 URL: {Config.BASE_URL}")

    options = Options()
    # options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")

    driver = None
    # 🔄 [핵심] 연결 재시도 로직 (최대 3회, 2초 간격)
    for i in range(3):
        try:
            driver = webdriver.Remote(
                command_executor=SELENIUM_GRID_URL,
                options=options
            )
            print(f"   -> ✅ 브라우저 연결 성공 (시도 {i+1}/3)")
            break
        except Exception as e:
            print(f"   -> ⚠️ 연결 실패 (시도 {i+1}/3): {e}")
            time.sleep(2)
    
    if driver is None:
        pytest.fail("❌ Selenium Grid 연결에 최종 실패했습니다. docker-compose 로그를 확인하세요.")

    # 프론트엔드 페이지 이동
    try:
        driver.get(Config.BASE_URL)
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
    except Exception as e:
        print(f"❌ URL 접속 실패: {Config.BASE_URL}")
        driver.quit()
        pytest.fail(f"페이지 로드 실패: {e}")

    yield driver

    # 📸 [디버깅] 테스트 실패 시 스크린샷 찍기
    if request.node.rep_call.failed:
        # 1. 저장할 폴더 이름 (상대 경로로 지정)
        save_dir = "screenshots"
        
        # 2. 폴더가 없다면 생성
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_name = f"error_{request.node.name}_{timestamp}.png"
        
        # 3. 경로 합치기 (os.path.join이 알아서 처리)
        full_path = os.path.join(save_dir, screenshot_name)
        
        driver.save_screenshot(full_path)
        print(f"\n📸 테스트 실패! 스크린샷 저장됨: {full_path}")

    print("\n🛑 [Teardown] 브라우저 종료")
    driver.quit()

# Pytest Hook: 실패 여부 감지용
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)