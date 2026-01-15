# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

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


    def send_keys(self, locator, text):
        if isinstance(locator, tuple):
            element = self.wait.until(EC.visibility_of_element_located(locator))
        elif isinstance(locator, list):
            element = self.get_shadow_element(locator)
        else:
            by = By.XPATH if "//" in locator else By.CSS_SELECTOR
            element = self.wait.until(EC.visibility_of_element_located((by, locator)))
            
        element.clear()
        element.send_keys(text)


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