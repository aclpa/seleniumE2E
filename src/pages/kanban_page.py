# src/pages/kanban_page.py
from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class KanbanPage(BasePage):

    CARD_SOURCE = (By.XPATH, "//div[contains(text(), 'test')]") # test 카드

    COLUMN_IN_PROGRESS = (By.XPATH, "//div[contains(@class, 'q-card') and contains(., 'In Progress')]") # In Progress 컬럼

    
    def move_card_to_in_progress(self, card_title):
        """
        특정 제목을 가진 카드를 'In Progress' 컬럼으로 이동
        """
        # 🌟 핵심 변경: API가 만든 랜덤 제목을 찾기 위해 XPath를 동적으로 생성합니다.
        # 기존: CARD_SOURCE = (By.XPATH, "//div[contains(text(), 'test')]")
        dynamic_card_locator = (By.XPATH, f"//div[contains(text(), '{card_title}')]")

        print(f"🖱️ '{card_title}' 카드를 'In Progress' 컬럼으로 이동 시도")
        
        # BasePage에 있는 drag_and_drop 메서드 호출
        self.drag_and_drop(dynamic_card_locator, self.COLUMN_IN_PROGRESS)

    def is_text_visible_in_column(self, card_text, column_name):
        """
        검증 함수: 해당 컬럼 안에 텍스트가 존재하는지 확인
        """
        print(f"🔎 검증: '{column_name}' 컬럼에 '{card_text}'가 도착했나요?")
        try:
            # 검증용 XPath: 컬럼(q-card) 안에 해당 텍스트가 있는지 확인
            # (Quasar 프레임워크 구조에 맞춰 div 계층을 조금 유연하게 수정했습니다)
            xpath = f"//div[contains(@class, 'q-card') and .//div[contains(text(), '{column_name}')]]//div[contains(text(), '{card_text}')]"
            
            # 카드가 이동해서 렌더링될 때까지 잠시 대기
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            
            print("   -> ✅ 확인됨!")
            return True
        except:
            print("   -> ❌ 확인 불가 (Timeout)")
            return False