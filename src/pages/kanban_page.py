# src/pages/kanban_page.py
from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class KanbanPage(BasePage):

    CARD_SOURCE = (By.XPATH, "//div[contains(text(), 'test')]") # test 카드

    COLUMN_IN_PROGRESS = (By.XPATH, "//div[contains(@class, 'q-card') and contains(., 'In Progress')]") # In Progress 컬럼

    
    def move_card_to_done(self):
        print("test 카드를 'In Progress' 컬럼으로 이동 시도")
        self.drag_and_drop(self.CARD_SOURCE, self.COLUMN_IN_PROGRESS)