from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

class SprintPage(BasePage):
    
    BTN_CREATE_SPRINT = (By.XPATH, "//span[contains(text(), 'New Sprint')]") # 스프린트 생성 버튼
    INPUT_SPRINT_NAME = (By.XPATH, "//input[@aria-label='Sprint Name *']") # 스프린트 이름 입력 필드
    sprint_project = (By.XPATH, "//div[contains(@class, 'q-field__control') and .//div[contains(., 'Project *')]]") # 스프린트 프로젝트 선택 필드
    sprint_project_select = (By.XPATH, "//div[@role='option']//span[contains(text(), 'test')]") # 스프린트 프로젝트 선택 옵션
    sprint_status = (By.XPATH, "//i[contains(text(), 'event_note')]") # 스프린트 상태 선택 필드
    sprint_status_select = (By.XPATH, f"//div[@role='option']//div[contains(text(), 'Active')]" ) # 스프린트 상태 선택 옵션
    BTN_CREATE_SPRINT_SUBMIT = (By.XPATH, "//span[contains(text(), 'Create')]") # 스프린트 생성 확인 버튼


    def create_sprint(self, sprint_name):
        """스프린트 생성 동작"""
        # 1. 스프린트 생성 버튼 클릭
        print(f"스프린트 생성 시도: {sprint_name}")
        self.click(self.BTN_CREATE_SPRINT)

        # 2. 스프린트 이름 입력
        self.click(self.sprint_project) # 프로젝트 선택 필드 클릭 대기
        self.wait.until(EC.visibility_of_element_located(self.sprint_project_select))
        self.click(self.sprint_project_select) # 프로젝트 선택
        self.send_keys(self.INPUT_SPRINT_NAME, sprint_name) # 스프린트 이름 입력
        self.click(self.sprint_status) # 상태 선택 필드 클릭
        self.wait.until(EC.visibility_of_element_located(self.sprint_status_select))
        self.click(self.sprint_status_select) # 상태 선택
        # 3. 저장/확인 버튼 클릭
        self.click(self.BTN_CREATE_SPRINT_SUBMIT)