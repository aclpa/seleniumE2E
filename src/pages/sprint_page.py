from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class SprintPage(BasePage):

    BTN_CREATE_SPRINT = (
        By.XPATH,
        "//span[contains(text(), 'New Sprint')]",
    )  # 스프린트 생성 버튼
    INPUT_SPRINT_NAME = (
        By.XPATH,
        "//input[@aria-label='Sprint Name *']",
    )  # 스프린트 이름 입력 필드
    sprint_project = (
        By.XPATH,
        "//div[contains(@class, 'q-dialog')]//label[.//div[contains(text(), 'Project')]]//div[contains(@class, 'q-field__control')]",
    )
    # 스프린트 프로젝트 선택 필드

    sprint_project_select = (
        By.XPATH,
        "//div[@role='option']",
    )  # 스프린트 프로젝트 선택 옵션
    sprint_status = (
        By.XPATH,
        "//div[contains(@class, 'q-dialog')]//input[@aria-label='Status']/ancestor::label",
    )  # 스프린트 상태 선택 필드
    sprint_status_select = (
        By.XPATH,
        f"//div[@role='option']//div[contains(text(), 'Active')]",
    )  # 스프린트 상태 선택 옵션
    BTN_CREATE_SPRINT_SUBMIT = (
        By.XPATH,
        "//span[contains(text(), 'Create')]",
    )  # 스프린트 생성 확인 버튼

    def create_sprint(self, sprint_name, project_name=None):
        """스프린트 생성 동작"""
        # 1. 스프린트 생성 버튼 클릭
        print(f"스프린트 생성 시도: {sprint_name}")
        self.click(self.BTN_CREATE_SPRINT)
        self.wait.until(EC.visibility_of_element_located(self.INPUT_SPRINT_NAME))
        try:
            self.click(self.sprint_project)  # 프로젝트 선택 필드 클릭
            self.wait.until(
                EC.visibility_of_element_located(self.sprint_project_select)
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
                    self.driver.find_elements(*self.sprint_project_select)[0].click()
            else:
                # 이름 지정 안 했으면 그냥 첫 번째꺼 클릭
                self.driver.find_elements(*self.sprint_project_select)[0].click()

        except Exception as e:
            print(f"ℹ️ 프로젝트 선택 패스 (사유: {e})")

        # 2. 스프린트 이름 입력
        # self.click_js(self.sprint_project) # 프로젝트 선택 필드 클릭 대기
        # self.wait.until(EC.visibility_of_element_located(self.sprint_project_select))
        # self.click_js(self.sprint_project_select) # 프로젝트 선택
        self.send_keys(self.INPUT_SPRINT_NAME, sprint_name)  # 스프린트 이름 입력
        self.click_js(self.sprint_status)  # 상태 선택 필드 클릭
        self.wait.until(EC.visibility_of_element_located(self.sprint_status_select))
        self.click_js(self.sprint_status_select)  # 상태 선택
        # 3. 저장/확인 버튼 클릭
        self.click_js(self.BTN_CREATE_SPRINT_SUBMIT)
