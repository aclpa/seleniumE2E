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
        """일반/Shadow DOM 자동 판별 클릭"""
        if isinstance(locator, list): # Shadow DOM
            element = self.get_shadow_element(locator)
        else: # 일반 DOM (XPath/CSS)
            by = By.XPATH if "//" in locator else By.CSS_SELECTOR
            element = self.wait.until(EC.element_to_be_clickable((by, locator)))
        
        element.click()

    def send_keys(self, locator, text):
        """일반/Shadow DOM 자동 판별 입력"""
        if isinstance(locator, list):
            element = self.get_shadow_element(locator)
        else:
            by = By.XPATH if "//" in locator else By.CSS_SELECTOR
            element = self.wait.until(EC.visibility_of_element_located((by, locator)))
        
        element.clear()
        element.send_keys(text)