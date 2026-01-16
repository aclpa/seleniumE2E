# src/pages/profile_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.pages.dashboard_page import DashboardPage


class ProfilePage(DashboardPage):
    # 로케이터
    BTN_EDIT_PROFILE = (By.XPATH, "//span[contains(., 'Edit Profile')]")
    INPUT_PHONE = (By.XPATH, "//input[@aria-label='Phone *']")
    INPUT_NAME = (By.XPATH, "//input[@aria-label='Full Name *']")
    BTN_UPDATE = (By.XPATH, "//button[contains(., 'Update')]")


    def update_profile(self, new_name, new_phone):
        """이름과 전화번호를 수정하고 저장"""
        # 1. Edit Profile 탭 클릭
        self.click(self.BTN_EDIT_PROFILE)


        # 2. 전화번호 입력 (기존 값 지우고 입력)
        phone_elem = self.driver.find_element(*self.INPUT_PHONE)
        phone_elem.send_keys(Keys.CONTROL + "a")
        phone_elem.send_keys(Keys.DELETE)
        phone_elem.send_keys(new_phone)

        # 3. 이름 입력
        name_elem = self.driver.find_element(*self.INPUT_NAME)
        name_elem.send_keys(Keys.CONTROL + "a")
        name_elem.send_keys(Keys.DELETE)
        name_elem.send_keys(new_name)

        # 4. 저장 버튼 클릭
        self.click(self.BTN_UPDATE)

        