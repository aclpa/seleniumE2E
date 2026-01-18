# src/pages/project_page.py
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

class ProjectPage(BasePage):

    BTN_CREATE_PROJECT = (By.XPATH, "//span[contains(text(), 'New Project')]") # 프로젝트 생성 버튼
    INPUT_PROJECT_KEY = (By.XPATH, "//input[@aria-label='프로젝트 키 *']") # 프로젝트 키(ID) 입력
    INPUT_PROJECT_NAME = (By.XPATH, "//input[@aria-label='프로젝트 이름 *']") # 프로젝트 이름 입력
    project_team = (By.XPATH, "//div[contains(@class, 'q-field__control') and .//div[contains(., 'Team *')]]") # 프로젝트 팀 선택 필드
    project_team_select = (By.XPATH, "//div[@role='option']") # 프로젝트 팀 선택 옵션
    BTN_CREATE_PROJECT_SUBMIT = (By.XPATH, "//span[contains(text(), 'Create')]") # 프로젝트 생성 확인 버튼
    
        
    def create_project(self, project_name, project_key, team_name=None):
        """프로젝트 생성 동작"""
        # 1. 생성 버튼 클릭
        print(f"프로젝트 생성 시도: {project_name} ({project_key})")
        self.click(self.BTN_CREATE_PROJECT)

        # 2. 프로젝트 키와 이름 입력
        self.send_keys(self.INPUT_PROJECT_NAME, project_name)
        self.send_keys(self.INPUT_PROJECT_KEY, project_key)

        try:
            self.click(self.project_team) # 프로젝트 팀 선택 필드 클릭
            self.wait.until(EC.visibility_of_element_located(self.project_team_select)) # 옵션창이 뜰 때까지 대기
            
            if project_name:
                print(f"🔎 팀 찾는 중: {team_name}")
                # 🌟 [핵심] 특정 텍스트를 포함하는 옵션을 찾는 동적 XPath
                specific_option_xpath = f"//div[@role='option'][contains(., '{team_name}')]"
                
                try:
                    # 해당 팀 클릭
                    self.driver.self.wait.until(By.XPATH, specific_option_xpath).click()
                    print(f"✅ 팀 선택 성공: {team_name}")
                except:
                    print(f"⚠️ '{team_name}' 옵션을 찾지 못했습니다. 첫 번째 옵션을 대신 선택합니다.")
                    self.driver.find_elements(*self.project_team_select)[0].click()
            else:
                # 이름 지정 안 했으면 그냥 첫 번째꺼 클릭
                self.driver.find_elements(*self.project_team_select)[0].click()     

        except Exception as e:
            print(f"ℹ️ 프로젝트 선택 패스 (사유: {e})")


        # self.click(self.project_team) # 팀 선택 필드 클릭 대기
        # self.wait.until(EC.visibility_of_element_located(self.project_team_select))
        # self.click(self.project_team_select) # 팀 선택
        # 3. 저장/확인 버튼 클릭
        self.click(self.BTN_CREATE_PROJECT_SUBMIT)

    