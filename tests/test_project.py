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


def test_create_sprint(driver, fake, new_project): # <--- new_project 픽스처 주입됨
    print("\n[TC-08] 스프린트 생성 테스트 (Hybrid Mode)")
    
    # 1. 로그인 (UI 로그인은 여전히 필요, 세션 유지를 위해)
    login_page = LoginPage(driver)
    login_page.main_login(Config.TEST_EMAIL, Config.TEST_PASSWORD)

    # 2. [Hybrid] API가 만든 프로젝트 페이지로 '바로 이동'
    # 프론트엔드 라우트 규칙: /projects/{id} 라고 가정 (실제 실행 시 URL 확인 필요)
    project_id = new_project['id'] 
    target_url = f"http://localhost:8080/projects/{project_id}"
    
    print(f"🚀 생성된 프로젝트 페이지로 바로 이동: {target_url}")
    driver.get(target_url)

    # 3. 스프린트 메뉴 진입 (화면 로직에 따라 다를 수 있음)
    # 만약 프로젝트 상세 페이지 안에 'Sprints' 탭이나 버튼이 있다면 그걸 클릭
    # 예시: DashboardPage나 ProjectPage에 "go_to_sprints_tab()" 같은 메서드가 필요할 수 있음
    # 여기서는 기존 로직을 최대한 활용하여 'Sprints' 메뉴로 이동한다고 가정
    
    # (주의) 만약 왼쪽 사이드바에서 해당 프로젝트를 클릭해야 한다면 로직이 복잡해집니다.
    # URL 이동이 가장 깔끔합니다. URL 이동 후 페이지 로딩 대기
    dashboard = DashboardPage(driver)
    # dashboard.go_to_sprints() <--- 기존 전역 메뉴 이동 방식 (삭제 혹은 수정 필요)
    
    # 4. 스프린트 생성 수행 (SprintPage 담당)
    sprint_page = SprintPage(driver)
    
    # UI 상에서 스프린트 생성 버튼 클릭 및 폼 입력
    random_sprint_name = fake.pystr(min_chars=4, max_chars=6)
    sprint_page.create_sprint(random_sprint_name)
    
    # 5. 검증
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