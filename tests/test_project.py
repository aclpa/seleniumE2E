# tests/test_project.py
from src.pages.login_page import LoginPage
from src.pages.dashboard_page import DashboardPage
from src.pages.project_page import ProjectPage
from src.config.config import Config
from src.pages.team_page import TeamPage
from src.pages.sprint_page import SprintPage   
from src.pages.issue_page import issuePage
from src.pages.kanban_page import KanbanPage

def test_create_team(driver, fake): # tc_06
    print("\n[TC-06] 팀 생성 테스트")
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.main_login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
    
    # 2. 'Teams' 메뉴로 이동 (DashboardPage 담당)
    dashboard = DashboardPage(driver)
    dashboard.go_to_teams()
    

    # 3. 팀 생성 수행 (TeamPage 담당)
    team_page = TeamPage(driver)

    # Faker로 랜덤 팀 이름 생성 (중복 방지)
    random_team_name = fake.pystr(min_chars=4, max_chars=6)
    team_page.create_team(random_team_name)
    
    
    # 4. 검증
    assert team_page.is_text_visible(random_team_name)
    print(f"✅ 팀 생성 확인 완료: {random_team_name}")

def test_create_project(driver, fake): #tc_07
    print("\n[TC-07] 프로젝트 생성 테스트")
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.main_login(Config.TEST_EMAIL, Config.TEST_PASSWORD)

    # 2. 'Projects' 메뉴로 이동 (DashboardPage 담당)
    dashboard = DashboardPage(driver)
    dashboard.go_to_projects() 
    
    # 3. 프로젝트 생성 수행 (ProjectPage 담당)
    project_page = ProjectPage(driver)

    # Faker로 랜덤 프로젝트 이름/키 생성 (중복 방지)
    random_project_name = fake.pystr(min_chars=4, max_chars=6)
    random_project_key = random_project_name.upper()
    project_page.create_project(random_project_name, random_project_key)
    
    
    # 4. 검증
    assert project_page.is_text_visible(random_project_name)

    print(f"✅ 프로젝트 생성 확인 완료: {random_project_name} ({random_project_key})")


def test_create_sprint(driver, fake): # tc_08
    print("\n[TC-08] 스프린트 생성 테스트")
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.main_login(Config.TEST_EMAIL, Config.TEST_PASSWORD)

    # 2. 'Projects' 메뉴로 이동 (DashboardPage 담당)
    dashboard = DashboardPage(driver)
    dashboard.go_to_sprints() 

    # 3. 스프린트 생성 수행 (SprintPage 담당)
    sprint_page = SprintPage(driver)

    # Faker로 랜덤 스프린트 이름 생성 (중복 방지)
    random_sprint_name = fake.pystr(min_chars=4, max_chars=6)
    sprint_page.create_sprint(random_sprint_name)
    
    
    # 4. 검증
    assert sprint_page.is_text_visible(random_sprint_name)
    print(f"✅ 스프린트 생성 확인 완료: {random_sprint_name}")


def test_create_issue(driver, fake): # tc_09
    print("\n[TC-09] 이슈 생성 테스트")
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.main_login(Config.TEST_EMAIL, Config.TEST_PASSWORD)

    # 2. 'Issues' 메뉴로 이동 (DashboardPage 담당)
    dashboard = DashboardPage(driver)
    dashboard.go_to_issues() 
    
    # 3. 이슈 생성 수행 (ProjectPage 담당)
    issue_page = issuePage(driver)

    # Faker로 랜덤 이슈 제목 생성 (중복 방지)
    random_issue_title = fake.sentence(nb_words=4)
    issue_page.create_issue(random_issue_title)
    
    # 4. 검증
    assert issue_page.is_text_visible(random_issue_title)

    print(f"✅ 이슈 생성 확인 완료: {random_issue_title}")

def test_kanban(driver): # tc_10
    print("\n[TC-10] 칸반 보드 테스트")
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.main_login(Config.TEST_EMAIL, Config.TEST_PASSWORD)

    # 2. 'Projects' 메뉴로 이동 (DashboardPage 담당)
    dashboard = DashboardPage(driver)
    dashboard.go_to_kanban() 

    kanban_page = KanbanPage(driver)
    
    # 드래그 앤 드롭 수행
    kanban_page.move_card_to_done()
    
    # 검증: 카드가 진짜로 In Progress 컬럼 안에 있는지 확인
    assert kanban_page.is_text_visible_in_column("test", "In Progress")