# tests/test_user_flow.py
from src.pages.login_page import LoginPage
from src.pages.profile_page import ProfilePage
from src.pages.dashboard_page import DashboardPage
from src.config.config import Config
from src.pages.base_page import BasePage as base_page

def test_profile_update(driver, fake): # tc_05
    print("\n[TC-05] 프로필 수정 테스트")
    
    # 1. 로그인 (기존 계정 활용)
    login_page = LoginPage(driver)
    login_page.main_login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    
    # 2. 프로필 페이지 이동
    Dashboard_page = DashboardPage(driver)
    Dashboard_page.open_profile()
    
    # 3. 랜덤 데이터 생성
    new_name = fake.name()
    new_phone = fake.phone_number()
    print(f"변경할 정보 -> 이름: {new_name}, 폰: {new_phone}")

    # 4. 수정 수행
    profile_page = ProfilePage(driver)
    profile_page.update_profile(new_name, new_phone)
    
    # 5. 검증 (토스트 메시지)
    actual_msg = profile_page.get_toast_message()
    print(f"결과 메시지: {actual_msg}")

    assert "updated" in actual_msg or "성공" in actual_msg or "successfully" in actual_msg

def test_logout(driver): # tc_11
    print("\n[TC-11] 로그아웃 테스트")
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.main_login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    
    # 2. 로그아웃 수행
    dashboard_page = DashboardPage(driver)
    dashboard_page.logout()
    
    # 3. 검증 (토스트 메시지 + URL)
    actual_msg = base_page(driver).get_toast_message()
    print(f"결과 메시지: {actual_msg}")

    assert "로그아웃" in actual_msg or "안전하게" in actual_msg or "리소스" in actual_msg