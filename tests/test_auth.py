# tests/test_auth.py
from src.pages.login_page import LoginPage
from src.config.config import Config
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


def test_signup_success(driver,fake): #tc_01
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
    WebDriverWait(driver, 3).until(EC.url_contains("login"))
    
    # 4. 검증
    # 회원가입 후 로그인 페이지로 오는지, 아니면 바로 로그인되는지 확인
    assert "9000" not in driver.current_url
    print("회원가입 후 로그인 페이지로 이동했음을 확인했습니다.")


def test_signup_existing_email(driver): #tc_02
    print("\n[TC-02] 기존 이메일로 회원가입 테스트")
    # 1. 페이지 객체 생성
    login_page = LoginPage(driver)
    
    # 2. 데이터 준비 (기존에 있는 이메일 사용)
    existing_email = Config.TEST_EMAIL
    fail_username = "Existing User"
    fail_password = "ExistingPass123!"

    # 3. 로직 수행
    login_page.signup(existing_email, fail_username, fail_password)
    
    # 4. 검증 (에러 메시지 확인)
    error_locator = login_page.signup_error_text()
    print("에러 메시지 :", error_locator)
    assert "거부" in error_locator or "이미 존재" in error_locator
    print("✅ 기존 이메일 가입 방지 기능 확인 완료")


def test_signup_password_mismatch(driver): #tc_03
    print("\n[TC-03] 비밀번호 불일치 로그인 테스트")
    # 1. 페이지 객체 생성
    login_page = LoginPage(driver)


    # 2. 데이터 준비 (비밀번호 불일치 상황 만들기)
    valid_email = Config.TEST_EMAIL      # 설정 파일에 있는 진짜 이메일
    wrong_password = "WrongPassword123!" # 아무거나 틀린 비밀번호

    print(f"생성된 회원정보 - 이메일: {valid_email}, 비밀번호: Password123!")

    # 3. 로직 수행
    login_page.login(valid_email, wrong_password)

    # 4. 검증 (에러 메시지 확인)
    error_msg = login_page.login_error_text()
    print("에러 메시지 :", error_msg)
    # 'Invalid'라는 단어가 포함되어 있는지 확인
    assert "Invalid" in error_msg or "password" in error_msg    
    print("✅ 기존 이메일 가입 방지 기능 확인 완료")



def test_login_success(driver):#tc_04
    print("\n[TC-04] 로그인 테스트")
    # 1. 페이지 객체 생성
    login_page = LoginPage(driver)
    
    # 2. 비즈니스 로직 수행
    login_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)

    WebDriverWait(driver, 3).until(lambda d: "9000" not in d.current_url)
    
    # 3. 검증 (Assertion)
    assert "9000" not in driver.current_url
    print("로그인 성공 url이 9000이 아닌 것을 확인했습니다.")



