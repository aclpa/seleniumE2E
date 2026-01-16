from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

class issuePage(BasePage): 
    BTN_CREATE_ISSUE = (By.XPATH, "//span[contains(text(), 'New Issue')]") # 이슈 생성 버튼
    INPUT_ISSUE_NAME = (By.XPATH, "//input[@aria-label='Title *']") # 이슈 이름 입력 필드
    issue_project = (By.XPATH, "//div[contains(@class, 'q-field__control') and .//div[contains(., 'Project *')]]") # 이슈 프로젝트 선택 필드
    issue_project_select = (By.XPATH, "//div[@role='listbox']//span[contains(text(), 'test')]") # 이슈 프로젝트 선택 옵션
    issue_type = (By.XPATH, "//div[contains(@class, 'q-field__control') and .//div[contains(., 'Type *')]]") # 이슈 타입 선택 필드
    issue_type_select = (By.XPATH, "//div[@role='option']//span[contains(text(), 'Task')]") # 이슈 타입 선택 옵션
    BTN_CREATE_ISSUE_SUBMIT = (By.XPATH, "//span[contains(text(), 'Create')]") # 이슈 생성 확인 버튼
    


    def create_issue(self, issue_name):
        """이슈 생성 동작"""
        # 1. 생성 버튼 클릭
        print(f"이슈 생성 시도: {issue_name}")
        self.click(self.BTN_CREATE_ISSUE)

        # 2. 입력 필드 채우기
        self.send_keys(self.INPUT_ISSUE_NAME, issue_name)
        self.click(self.issue_project) # 프로젝트 선택 필드 클릭 대기
        self.wait.until(EC.visibility_of_element_located(self.issue_project_select))
        self.click(self.issue_project_select) # 프로젝트 선택
        self.click(self.issue_type) # 타입 선택 필드 클릭 대기
        self.wait.until(EC.visibility_of_element_located(self.issue_type_select))
        self.click(self.issue_type_select) # 타입 선택
        # 3. 저장/확인 버튼 클릭
        self.click(self.BTN_CREATE_ISSUE_SUBMIT)