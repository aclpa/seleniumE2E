# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.config.config import Config
from faker import Faker
from src.utils.api_client import APIClient


@pytest.fixture(scope="session")
def fake():
    return Faker()

# --- 추가된 부분 시작 ---
@pytest.fixture(scope="session")
def api_client():
    """테스트 세션 동안 유지되는 API 클라이언트"""
    client = APIClient()
    client.login() # 세션 시작 시 1회 로그인
    return client

@pytest.fixture(scope="function")
def new_team(api_client, fake):
    t_name = f"Team_{fake.bothify(text='????')}"
    print(f"\n🏢 [Setup] 팀 생성 중: {t_name}") # 로그 추가
    team = api_client.create_team(t_name)
    
    yield team # 여기서 테스트로 데이터를 넘겨줌
    
    # yield 뒷부분은 테스트가 끝난 후 실행됩니다 (Teardown)
    print(f"🗑️ [Teardown] 팀 삭제 등 뒷정리 가능 (ID: {team['id']})")


@pytest.fixture(scope="function")
def new_project(api_client, fake, new_team):
    p_name = f"AutoProj_{fake.lexify(text='????')}"
    p_key = fake.lexify(text='???').upper()
    
    print(f"🏗️ [Setup] 프로젝트 생성 중: {p_name}") # 로그 추가
    project = api_client.create_project(name=p_name, key=p_key, team_id=new_team['id'])
    
    yield project
    
    print(f"🗑️ [Teardown] 프로젝트 정리 가능")



@pytest.fixture(scope="function")
def driver():
    print("\n🚀 [Setup] 브라우저 실행")
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") 
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.maximize_window()
    
    yield driver  # 테스트가 여기서 실행됩니다.
    
    print("\n🛑 [Teardown] 브라우저 종료")
    driver.quit()
