# pages/login_page.py
from src.pages.base_page import BasePage
from src.config.config import Config
import time

class LoginPage(BasePage):
    SSO_BTN = "//button[contains(., 'SSO')]"

    LINK_SIGNUP = ["ak-flow-executor","ak-stage-identification","a[id='enroll']"] # 회원가입 링크

    INPUT_NAME = ["ak-flow-executor","ak-stage-prompt","input[type='text']"] # 회원가입 이름 입력필드

    INPUT_EMAIL = ["ak-flow-executor","ak-stage-prompt","input[type='email']"] # 회원가입 이메일 입력필드

    INPUT_PW = ["ak-flow-executor","ak-stage-prompt","input[type='password']"] # 회원가입 비밀번호 입력필드

    INPUT_PW_CONFIRM = ["ak-flow-executor","ak-stage-prompt","input[name='password_repeat']"] # 회원가입 비밀번호 확인 입력필드

    BTN_SIGNUP = ["ak-flow-executor", "ak-stage-prompt","button[type='submit']"] # 회원가입 확인 버튼

    LOGIN_EMAIL = ["ak-flow-executor","ak-stage-identification","input[name='uidField']"] # 로그인 이메일 입력필드

    BTN_NEXT = ["ak-flow-executor","ak-stage-identification","button[type='submit']"] # 로그인 이메일 다음 버튼

    LOGIN_PW = ["ak-flow-executor","ak-stage-password","input[type='password']"] # 로그인 비밀번호 입력필드

    BTN_LOGIN = ["ak-flow-executor", "ak-stage-password", "button[type='submit']"] # 로그인 비밀번호 로그인 버튼

   

    signup_error = ["ak-flow-executor", "ak-stage-access-denied", "ak-empty-state[header='요청이 거부되었습니다.']"] # 회원가입 에러 메시지

    login_error = ["ak-flow-executor", "ak-stage-password", "ak-flow-input-password > ak-form-element", "p.pf-c-form__helper-text"]# 로그인 에러 메시지



    def login(self, email, password):
        self.driver.get(Config.BASE_URL)
        self.click(self.SSO_BTN)
    
        
        self.send_keys(self.LOGIN_EMAIL, email)
        self.click(self.BTN_NEXT)
        

        self.send_keys(self.LOGIN_PW, password)
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
        self.click(self.BTN_SIGNUP)


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
        
    def login_error_text(self):
        time.sleep(0.5)
        try:
            # BasePage의 get_shadow_element 기능 활용
            element = self.get_shadow_element(self.login_error)
            
            if element and element.is_displayed():
                return element.text
            return "" # 안 보이면 빈 문자열 반환
        except:
            return ""
        

    