# src/pages/dashboard_page.py
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class DashboardPage(BasePage):
    # --- 상단 메뉴 로케이터 ---
    AVATAR_ICON = (By.XPATH, "//button[.//div[contains(@class, 'q-avatar')]]")
    MENU_PROFILE = (By.XPATH, "//div[contains(text(), 'Profile')]")
    MENU_LOGOUT = (By.XPATH, "//div[contains(text(), 'Logout')]")
    
    # --- 사이드바 메뉴 로케이터 ---
    MENU_PROJECTS = (By.XPATH, "//div[@role='listitem' and contains(., 'Projects')]")
    MENU_TEAMS = (By.XPATH, "//div[@role='listitem' and contains(., 'Teams')]")
    MENU_SPRINTS = (By.XPATH, "//div[@role='listitem' and contains(., 'Sprints')]")
    MENU_ISSUES = (By.XPATH, "//div[@role='listitem' and contains(., 'Issues')]")
    MENU_KANBAN = (By.XPATH, "//div[@role='listitem' and contains(., 'Kanban Board')]")



    def open_profile(self):
        """프로필 페이지로 이동"""
        self.click(self.AVATAR_ICON)
        self.click(self.MENU_PROFILE)

    def logout(self):
        """로그아웃 수행"""
        print("로그아웃 시도 중...")
        self.click(self.AVATAR_ICON)
        self.click(self.MENU_LOGOUT)
        self.wait.until(lambda d: "auth/login" in self.get_current_url())
        
    def go_to_projects(self):
        self.click(self.MENU_PROJECTS)# 프로젝트 메뉴 클릭

    def go_to_teams(self):
        self.click(self.MENU_TEAMS)# 팀 메뉴 클릭
        
    def go_to_sprints(self):
        self.click(self.MENU_SPRINTS)# 스프린트 메뉴 클릭

    def go_to_issues(self):
        self.click(self.MENU_ISSUES)# 이슈 메뉴 클릭

    def go_to_kanban(self):
        self.click(self.MENU_KANBAN)# 칸반 메뉴 클릭

