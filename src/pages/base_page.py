# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains


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
        [Pure Selenium] StaleElement 발생 시, Wait을 통해 스마트하게 재시도
        """
        attempts = 0
        while attempts < 3:
            try:
                # 1. 요소가 클릭 가능할 때까지 기다림 (여기서 자동으로 대기함)
                if isinstance(locator, tuple):
                    element = self.wait.until(EC.element_to_be_clickable(locator))
                elif isinstance(locator, list):
                    element = self.get_shadow_element(locator)
                else:
                    by = By.XPATH if "//" in locator else By.CSS_SELECTOR
                    element = self.wait.until(EC.element_to_be_clickable((by, locator)))
                
                # 2. 클릭 시도
                element.click()
                return # 성공하면 함수 종료

            except StaleElementReferenceException:

                attempts += 1
                print(f"⚠️ 요소 변경 감지(Stale). 재시도 {attempts}/3")
                
        # 3번 다 실패하면 에러 발생
        raise Exception(f"요소를 클릭할 수 없습니다 (Stale): {locator}")


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

            element = self.wait.until(EC.presence_of_element_located((By.XPATH, locator) if "//" in locator else (By.CSS_SELECTOR, locator)))

        # 2. 자바스크립트로 클릭 실행 (겹친 요소 무시)
        self.driver.execute_script("arguments[0].click();", element)

    def drag_and_drop(self, source_locator, target_locator):
        """
        source 요소를 잡아서 target 요소 위로 드래그 앤 드롭합니다.
        """
        # 1. 요소 찾기
        if isinstance(source_locator, tuple):
            source = self.wait.until(EC.visibility_of_element_located(source_locator))
        else:
            source = source_locator

        if isinstance(target_locator, tuple):
            target = self.wait.until(EC.visibility_of_element_located(target_locator))
        else:
            target = target_locator

        # 2. 액션 수행 (잡고 -> 이동 -> 놓기)
        actions = ActionChains(self.driver)
        

        actions.click_and_hold(source)\
               .pause(0.5)\
               .move_to_element(target)\
               .pause(0.5)\
               .release()\
               .perform()
        


    def drag_and_drop_js(self, source_locator, target_locator):
        """
        [JS 우회] ActionChains로 해결되지 않는 HTML5 드래그 앤 드롭을 처리합니다.
        Vue/React의 DOM Re-render로 인한 Stale 에러를 100% 방지합니다.
        """
        # 1. 요소 찾기
        if isinstance(source_locator, tuple):
            source = self.wait.until(EC.presence_of_element_located(source_locator))
        else:
            source = source_locator

        if isinstance(target_locator, tuple):
            target = self.wait.until(EC.presence_of_element_located(target_locator))
        else:
            target = target_locator


        js_script = """
            var src = arguments[0];
            var tgt = arguments[1];
            
            var dataTransfer = {
                dropEffect: '',
                effectAllowed: 'all',
                files: [],
                items: {},
                types: [],
                setData: function (format, data) {
                    this.items[format] = data;
                    this.types.push(format);
                },
                getData: function (format) {
                    return this.items[format];
                },
                clearData: function (format) { }
            };

            var emit = function (event, target) {
                var evt = document.createEvent("Event");
                evt.initEvent(event, true, false);
                evt.dataTransfer = dataTransfer;
                target.dispatchEvent(evt);
            };

            emit("dragstart", src);
            emit("dragenter", tgt);
            emit("dragover", tgt);
            emit("drop", tgt);
            emit("dragend", src);
        """
        self.driver.execute_script(js_script, source, target)
        print("   ⚡ JS로 강제 드래그 앤 드롭 실행 완료")