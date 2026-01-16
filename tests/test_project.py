# tests/test_project.py
from src.pages.login_page import LoginPage
from src.pages.dashboard_page import DashboardPage
from src.pages.project_page import ProjectPage
from src.config.config import Config

def test_create_team_success(driver, fake): # tc_06
    print("\n[TC-06] 팀 생성 테스트")
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.main_login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    
    # 2. 'Teams' 메뉴로 이동 (DashboardPage 담당)
    dashboard = DashboardPage(driver)
    dashboard.go_to_teams() # 지난번에 만들어둔 함수 호출!
    

    # 3. 팀 생성 수행 (ProjectPage 담당)
    project_page = ProjectPage(driver)

    # Faker로 랜덤 팀 이름 생성 (중복 방지)
    random_team_name = f"{fake.color_name()} Team"
    project_page.create_team(random_team_name)
    
    
    # 4. 검증
    assert project_page.is_text_visible(random_team_name)

    print(f"✅ 팀 생성 확인 완료: {random_team_name}")