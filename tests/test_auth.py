# tests/test_auth.py
from src.pages.login_page import LoginPage
from src.config.config import Config
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

def test_login_success(driver):#tc_04_login
    print("\n[TC-04] 로그인 테스트")
    # 1. 페이지 객체 생성
    login_page = LoginPage(driver)
    
    # 2. 비즈니스 로직 수행
    login_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)

    WebDriverWait(driver, 10).until(lambda d: "9000" not in d.current_url)
    
    # 3. 검증 (Assertion)
    assert "9000" not in driver.current_url
    print("로그인 성공 url이 9000이 아닌 것을 확인했습니다.")

def test_signup_success(driver,fake): #tc_01_signup
    print("\n[TC-01] 회원가입 테스트")
    # 1. 페이지 객체
    login_page = LoginPage(driver)
    
    # 2. 데이터 준비 (Faker 쓰면 더 좋음)
    random_email = fake.email()
    random_username = fake.name()
    random_password = fake.password(length=10)

    print(f"생성된 회원정보 - 이메일: {random_email}, 이름: {random_username}, 비밀번호: {random_password}")

    # 3. 로직 수행
    login_page.signup(random_email, random_username, random_password)
    WebDriverWait(driver, 10).until(EC.url_contains("login"))
    
    # 4. 검증
    # 회원가입 후 로그인 페이지로 오는지, 아니면 바로 로그인되는지 확인
    assert "login" in driver.current_url