from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class TeamPage(BasePage):

    BTN_CREATE_TEAM = (By.XPATH, "//span[contains(text(), 'New Team')]")  # 팀 생성 버튼
    INPUT_TEAM_NAME = (
        By.XPATH,
        "//input[@aria-label='Team Name *']",
    )  # 팀 이름 입력필드
    SELECT_TEAM_MEMBERS = (
        By.XPATH,
        "//input[@aria-label='Select Initial Members']",
    )  # 팀 멤버 선택 필드
    BTN_SUBMIT = (
        By.XPATH,
        "//div[contains(@class, 'q-dialog')]//button[contains(., 'Create')]",
    )  # 생성 확인 버튼
    SELECT_TEAM_MEMBER_OPTION = (
        By.XPATH,
        "//div[@role='listbox']//div[contains(text(), 'test123')]",
    )  # 팀 멤버 선택 옵션

    def create_team(self, team_name):
        """팀을 생성하는 동작"""
        print(f"팀 생성 시도: {team_name}")

        # 1. 생성 버튼 클릭
        self.click(self.BTN_CREATE_TEAM)

        # 2. 팀 이름 입력 (BasePage의 기능 활용)
        self.send_keys(self.INPUT_TEAM_NAME, team_name)
        self.click(self.SELECT_TEAM_MEMBERS)  # 멤버 선택 필드 클릭 대기
        self.wait.until(
            EC.visibility_of_element_located(self.SELECT_TEAM_MEMBER_OPTION)
        )
        self.click(self.SELECT_TEAM_MEMBER_OPTION)  # 멤버 선택
        # 3. 저장/확인 버튼 클릭
        self.click(self.BTN_SUBMIT)
