# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def get_shadow_element(self, selectors):# Shadow DOM 요소 찾기
        try:
            element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selectors[0])))
            for selector in selectors[1:]:
                shadow_root = element.shadow_root
                element = shadow_root.find_element(By.CSS_SELECTOR, selector)
            return element
        except Exception as e:
            print(f"❌ 요소 찾기 실패: {e}")
            return None

    def click(self, locator):
        """
        locator 타입에 따라 자동으로 처리하는 클릭 함수
        - 튜플: (By.XPATH, "//...") -> 일반 Selenium 방식 (추천)
        - 리스트: ["root", "child"] -> Shadow DOM 방식
        - 문자열: "//button" -> 구버전 호환 (자동 감지)
        """
        if isinstance(locator, tuple):  # 1. 튜플이면 (By.XX, "selector")
            element = self.wait.until(EC.element_to_be_clickable(locator))
        
        elif isinstance(locator, list): # 2. 리스트면 Shadow DOM
            element = self.get_shadow_element(locator)
        
        else: # 3. 문자열이면 자동 감지 (기존 코드 호환)
            by = By.XPATH if "//" in locator else By.CSS_SELECTOR
            element = self.wait.until(EC.element_to_be_clickable((by, locator)))
        
        element.click()


    def send_keys(self, locator, text): # 자동으로 처리하는 입력 함수
        if isinstance(locator, tuple):# 1. 튜플이면 (By.XX, "selector")
            element = self.wait.until(EC.visibility_of_element_located(locator))# 요소 대기
        elif isinstance(locator, list):# 2. 리스트면 Shadow DOM
            element = self.get_shadow_element(locator)# 요소 대기
        else:
            by = By.XPATH if "//" in locator else By.CSS_SELECTOR# 3. 문자열이면 자동 감지 (기존 코드 호환)
            element = self.wait.until(EC.visibility_of_element_located((by, locator)))
        
        element.clear()# 기존 내용 지우기
        element.send_keys(text)# 입력
        element.send_keys(Keys.TAB)# 포커스 아웃
        self.wait.until(lambda d: element.get_attribute('value') == text)


    def get_toast_message(self):
        """
        화면에 뜬 'q-notification' 토스트 메시지의 텍스트를 반환합니다.
        """
        # 찾아내신 HTML 클래스(.q-notification)를 사용합니다.
        TOAST_LOCATOR = (By.CSS_SELECTOR, ".q-notification") 

        try:
            # 1. 토스트 메시지가 나타날 때까지 최대 5초 대기 (나타나면 즉시 진행)
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(TOAST_LOCATOR)
            )
            
            # 2. 텍스트 반환 (예: "로그아웃\n안전하게 로그아웃되었습니다.")
            return element.text
        except:
            print("⚠️ 토스트 메시지를 찾을 수 없거나 너무 빨리 사라졌습니다.")
            return ""
        
    def is_text_visible(self, text):
        """
        화면에 특정 텍스트(text)가 보이는지 확인하는 만능 함수
        - 성공 시: True 반환
        - 실패 시: False 반환 (10초 대기 후)
        """
        # XPath를 사용해 해당 텍스트를 포함하는 모든 태그를 찾음
        locator = (By.XPATH, f"//*[contains(text(), '{text}')]")
        
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            print(f"❌ 텍스트를 찾을 수 없음: {text}")
            return False
        

    def click_js(self, locator):
        """
        [강제 클릭] JavaScript를 사용하여 요소를 직접 클릭합니다.
        ElementClickInterceptedException(가려짐) 에러가 날 때 사용하세요.
        """
        # 1. 요소 찾기
        if isinstance(locator, tuple):
            element = self.wait.until(EC.presence_of_element_located(locator))
        else:
            # 기존 로직 (Shadow DOM 등) 유지하거나, tuple만 처리해도 됨
            # 여기서는 편의상 tuple 기준으로 작성
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, locator) if "//" in locator else (By.CSS_SELECTOR, locator)))

        # 2. 자바스크립트로 클릭 실행 (겹친 요소 무시)
        self.driver.execute_script("arguments[0].click();", element)