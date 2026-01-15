# pages/login_page.py
from src.pages.base_page import BasePage
from src.config.config import Config
import time

class LoginPage(BasePage):
    SSO_BTN = "//button[contains(., 'SSO')]"
    LINK_LOGIN = ["ak-flow-executor", "ak-stage-identification", "a[id='enroll']"] 
    INPUT_EMAIL = ["ak-flow-executor","ak-stage-prompt","input[type='email']"]
    BTN_NEXT = ["ak-flow-executor","ak-stage-prompt","button[type='submit']"]
    INPUT_PW = ["ak-flow-executor","ak-stage-prompt","input[type='password']"]
    BTN_LOGIN = ["ak-flow-executor", "ak-stage-password", "button[type='submit']"]
    LINK_SIGNUP = ["ak-flow-executor","ak-stage-identification","a[id='enroll']"]
    INPUT_NAME = ["ak-flow-executor","ak-stage-prompt","input[type='text']"]
    INPUT_PW_CONFIRM = ["ak-flow-executor","ak-stage-prompt","input[name='password_repeat']"]
    signup_error = ["ak-flow-executor", "ak-stage-access-denied", "ak-empty-state[header='요청이 거부되었습니다.']"]

    def login(self, email, password):
        self.driver.get(Config.BASE_URL)
        self.click(self.SSO_BTN)
    
        
        self.send_keys(self.INPUT_EMAIL, email)
        self.click(self.BTN_NEXT)
        

        self.send_keys(self.INPUT_PW, password)
        self.click(self.BTN_LOGIN)


    def signup(self, email, name, password):
        self.driver.get(Config.BASE_URL)
        self.click(self.SSO_BTN)
        
        # 회원가입 페이지로 이동
        self.click(self.LINK_SIGNUP) 
        
        # 정보 입력 (Shadow DOM 처리된 send_keys 사용)
        self.send_keys(self.INPUT_EMAIL, email)
        self.send_keys(self.INPUT_NAME, name)
        self.send_keys(self.INPUT_PW, password)
        self.send_keys(self.INPUT_PW_CONFIRM, password)
        
        # 확인 버튼 클릭
        self.click(self.BTN_NEXT)

    def signup_error_text(self):
        time.sleep(0.5)
        try:
            # BasePage의 get_shadow_element 기능 활용
            element = self.get_shadow_element(self.signup_error)
            
            if element and element.is_displayed():
                return element.text
            return "" # 안 보이면 빈 문자열 반환
        except:
            return ""

    