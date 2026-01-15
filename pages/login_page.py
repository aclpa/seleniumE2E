# pages/login_page.py
from pages.base_page import BasePage
from config.config import Config

class LoginPage(BasePage):
    SSO_BTN = "//button[contains(., 'SSO')]"
    LINK_LOGIN = ["ak-flow-executor", "ak-stage-identification", "a[id='enroll']"] 
    INPUT_EMAIL = ["ak-flow-executor", "ak-stage-identification", "input[name='uidField']"]
    BTN_NEXT = ["ak-flow-executor", "ak-stage-identification", "button[type='submit']"]
    INPUT_PW = ["ak-flow-executor", "ak-stage-password", "input[autocomplete='current-password']"]
    BTN_LOGIN = ["ak-flow-executor", "ak-stage-password", "button[type='submit']"]

    def login(self, email, password):
        self.driver.get(Config.BASE_URL)
        self.click(self.SSO_BTN)
    
        
        self.send_keys(self.INPUT_EMAIL, email)
        self.click(self.BTN_NEXT)
        
        # 여기서 WebDriverWait로 비밀번호 입력창 뜰 때까지 대기하는 로직 추가 권장
        import time; time.sleep(1) 
        
        self.send_keys(self.INPUT_PW, password)
        self.click(self.BTN_LOGIN)