# tests/test_auth.py
from pages.login_page import LoginPage
from config.config import Config
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

def test_login_success(driver):
    # 1. 페이지 객체 생성
    login_page = LoginPage(driver)
    
    # 2. 비즈니스 로직 수행
    login_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)

    WebDriverWait(driver, 10).until(lambda d: "9000" not in d.current_url)
    
    # 3. 검증 (Assertion)
    assert "9000" not in driver.current_url
    print("로그인 성공 url이 9000이 아닌 것을 확인했습니다.")