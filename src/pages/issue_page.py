from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class issuePage(BasePage):
    BTN_CREATE_ISSUE = (
        By.XPATH,
        "//span[contains(text(), 'New Issue')]",
    )  # 이슈 생성 버튼
    INPUT_ISSUE_NAME = (
        By.XPATH,
        "//input[@aria-label='Title *']",
    )  # 이슈 이름 입력 필드
    issue_project = (
        By.XPATH,
        "//div[contains(@class, 'q-field__control') and .//div[contains(., 'Project *')]]",
    )  # 이슈 프로젝트 선택 필드
    issue_project_select = (
        By.XPATH,
        "//div[@role='listbox']",
    )  # 이슈 프로젝트 선택 옵션
    issue_type = (
        By.XPATH,
        "//div[contains(@class, 'q-field__control') and .//div[contains(., 'Type *')]]",
    )  # 이슈 타입 선택 필드
    issue_type_select = (
        By.XPATH,
        "//div[@role='option']//span[contains(text(), 'Bug')]",
    )  # 이슈 타입 선택 옵션
    BTN_CREATE_ISSUE_SUBMIT = (
        By.XPATH,
        "//span[contains(text(), 'Create')]",
    )  # 이슈 생성 확인 버튼

    def create_issue(self, issue_name, project_name=None):
        """이슈 생성 동작"""
        # 1. 생성 버튼 클릭
        print(f"이슈 생성 시도: {issue_name}")
        self.click(self.BTN_CREATE_ISSUE)

        # 2. 입력 필드 채우기
        self.send_keys(self.INPUT_ISSUE_NAME, issue_name)  # 이슈 이름 입력

        try:
            self.click(self.issue_project)  # 프로젝트 선택 필드 클릭
            self.wait.until(
                EC.visibility_of_element_located(self.issue_project_select)
            )  # 옵션창이 뜰 때까지 대기

            if project_name:
                print(f"🔎 프로젝트 찾는 중: {project_name}")
                # 🌟 [핵심] 특정 텍스트를 포함하는 옵션을 찾는 동적 XPath
                specific_option_xpath = (
                    f"//div[@role='option'][contains(., '{project_name}')]"
                )

                try:
                    # 해당 프로젝트 클릭
                    self.driver.self.wait.until(By.XPATH, specific_option_xpath).click()
                    print(f"✅ 프로젝트 선택 성공: {project_name}")
                except:
                    print(
                        f"⚠️ '{project_name}' 옵션을 찾지 못했습니다. 첫 번째 옵션을 대신 선택합니다."
                    )
                    self.driver.find_elements(*self.issue_project_select)[0].click()
            else:
                # 이름 지정 안 했으면 그냥 첫 번째꺼 클릭
                self.driver.find_elements(*self.issue_project_select)[0].click()

        except Exception as e:
            print(f"ℹ️ 프로젝트 선택 패스 (사유: {e})")

        # self.click(self.issue_project) # 프로젝트 선택 필드 클릭 대기
        # self.wait.until(EC.visibility_of_element_located(self.issue_project_select))
        # self.click(self.issue_project_select) # 프로젝트 선택
        self.click(self.issue_type)  # 타입 선택 필드 클릭 대기
        self.wait.until(EC.visibility_of_element_located(self.issue_type_select))
        self.click(self.issue_type_select)  # 타입 선택
        # 3. 저장/확인 버튼 클릭
        self.click(self.BTN_CREATE_ISSUE_SUBMIT)
