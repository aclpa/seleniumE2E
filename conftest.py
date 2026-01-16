# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.config.config import Config
from faker import Faker

@pytest.fixture(scope="session")
def fake():
    return Faker()

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