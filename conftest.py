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
    return api_client.create_team(t_name)

@pytest.fixture(scope="function")
def new_project(api_client, fake, new_team):
    p_name = f"AutoProj_{fake.lexify(text='????')}"
    p_key = fake.lexify(text='???').upper()
    
    # new_team['id']를 인자로 넘겨줍니다.
    return api_client.create_project(name=p_name, key=p_key, team_id=new_team['id'])



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
