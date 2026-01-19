# import time
# import sys
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from faker import Faker
# from selenium.webdriver.common.action_chains import ActionChains

# class DevFlowTestRunner:
#     def __init__(self):
#         """테스트 초기화: 브라우저 실행"""
#         print("🚀 [Setup] 테스트 환경을 초기화합니다...")
#         options = webdriver.ChromeOptions()
#         # options.add_argument("--headless")  # 화면 안 보고 싶으면 주석 해제
#         # options.add_argument("--start-maximized") # 전체화면
#         self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#         self.wait = WebDriverWait(self.driver, 10)
#         self.base_url = "http://localhost:8080"
#         self.auth_paths = {
#         "login_email": [
#         "ak-flow-executor",
#         "ak-stage-identification",
#         "input[name='uidField']"
#         ],
#         "login_submit": [
#         "ak-flow-executor",
#         "ak-stage-identification",
#         "button[type='submit']"
#         ],
#         "login_password": [
#         "ak-flow-executor",
#         "ak-stage-password",
#         "input[autocomplete='current-password']"
#         ],
#         "end_login_submit": [
#         "ak-flow-executor",
#         "ak-stage-password",
#         "button[type='submit']"
#         ],
#         "submit":[
#         "ak-flow-executor",
#         "ak-stage-identification",
#         "a[id='enroll']"
#         ],
#         "username": [
#         "ak-flow-executor",
#         "ak-stage-prompt",
#         "input[type='text']"
#         ],
#         "email": [
#         "ak-flow-executor",
#         "ak-stage-prompt",
#         "input[type='email']"
#         ],
#         "password": [
#         "ak-flow-executor",
#         "ak-stage-prompt",
#         "input[type='password']"
#         ],
#         "password_rep": [
#         "ak-flow-executor",
#         "ak-stage-prompt",
#         "input[name='password_repeat']"
#         ],
#         "submit_btn": [
#         "ak-flow-executor",
#         "ak-stage-prompt",
#         "button[type='submit']"
#         ],
#         "menu_projects": "//div[@role='listitem' and contains(., 'Projects')]",
#         "menu_teams": "//div[@role='listitem' and contains(., 'Teams')]",
#         "ahthentik_sso_btn": "//button[contains(., 'SSO')]",
#         "login_main_email": "//input[@type='text' or @type='email']",
#         "login_main_password":"//input[@type='password']",
#         "login_main_submit": "//span[contains(text(), '로그인')]",
#         }
#         self.authentik_url = "http://localhost:9000/if/flow/enrollment-flow/?next=%2Fapplication%2Fo%2Fauthorize%2F%3Fresponse_type%3Dcode%26client_id%3DqvN7JqQB4hk4LL1tlNbTBKcxuGqSQnA5pD8UBE1O%26redirect_uri%3Dhttp%253A%252F%252Flocalhost%253A8080%252Fauth%252Fcallback%26scope%3Dopenid%2Bemail%2Bprofile%26state%3Drandom_string_for_security"
#         self.shared_email = None
#         self.shared_password = None
#         self.shared_username = None
#         self.dashboard_url = "http://localhost:8080/#/dashboard"
#         self.fake = Faker('ko_KR')
#         self.scrpit ="document.querySelector(\"body > ak-flow-executor\").shadowRoot.querySelector(\"ak-locale-context > div.pf-c-page__drawer > div > div > div > div > div > div > div > ak-stage-password\").shadowRoot.querySelector(\"div > form > ak-flow-input-password > ak-form-element\").shadowRoot.querySelector(\"div > p\")"
#         self.existing_email = "test123a@test.com"
#         self.existing_password = "test123qaswera"
#     def teardown(self):
#         """테스트 종료: 브라우저 닫기"""
#         print("🛑 [Teardown] 브라우저를 닫습니다.")
#         time.sleep(0.5)
#         self.driver.quit()
#     # =================================================================
#     def get_shadow_element_v4(self, selectors):
#         """
#         [엔진] 섀도우 돔을 뚫고 들어가는 재귀 함수 (Retry 로직 포함)
#         """
#         try:

#             element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selectors[0])))# 1. 최상위 요소 찾기

#             # 2. 내부 관문 돌파
#             for selector in selectors[1:]:# 나머지 셀렉터들에 대해 반복
#                 shadow_root = element.shadow_root# 섀도우 루트 접근
#                 found = False# 요소 찾기 시도
#                 # 타이밍 이슈 해결을 위한 재시도 로직
#                 for _ in range(5): # 최대 5회 재시도
#                     try:# 요소 찾기 시도
#                         time.sleep(0.5)# 잠시 대기
#                         element = shadow_root.find_element(By.CSS_SELECTOR, selector)# 내부 요소 찾기
#                         found = True# 성공하면 루프
#                         break# 탈출
#                     except:# 실패하면 재시도
#                         pass# 무시하고 재시도

#                 if not found:
#                     raise Exception(f"요소를 찾을 수 없음 (Shadow DOM): {selector}")# 찾지 못했으면 예외 발생

#             return element

#         except Exception as e:
#             print(f"❌ [Engine Error] {e}")
#             return None

#     def _get_element_smart(self, path_key_or_selector):
#         """
#         [판별기] 입력받은 키가 리스트(Shadow)인지 문자열(일반)인지 구분해서 요소를 찾아줌
#         """
#         # 1. 딕셔너리에서 꺼내기 (없으면 입력값 그대로 사용)
#         target = self.auth_paths.get(path_key_or_selector, path_key_or_selector)

#         # 2. 리스트면 -> Shadow DOM 탐색
#         if isinstance(target, list):
#             return self.get_shadow_element_v4(target)

#         # 3. 문자열이면 -> 일반 DOM 탐색
#         else:
#             # XPath vs CSS 구분
#             by_method = By.XPATH if ("//" in target) or target.startswith("(") else By.CSS_SELECTOR
#             return self.wait.until(EC.element_to_be_clickable((by_method, target)))

#     def _shadow_fill(self, path_key, value):
#         """[통합 입력 함수] Shadow DOM / 일반 DOM 자동 구분"""
#         print(f"⌨️  입력 시도: [{path_key}] -> {value}")
#         try:
#             element = self._get_element_smart(path_key)
#             if element:
#                 element.click()
#                 element.clear()
#                 element.send_keys(value)
#                 print("   ✅ 입력 성공")
#             else:
#                 print("   ❌ 요소를 찾을 수 없습니다.")
#         except Exception as e:
#             print(f"   ❌ 에러: {e}")

#     def _shadow_click(self, path_key):
#         """[통합 클릭 함수] Shadow DOM / 일반 DOM 자동 구분"""
#         print(f"🖱️  클릭 시도: [{path_key}]")
#         try:
#             element = self._get_element_smart(path_key)
#             if element:
#                 element.click()
#                 print("   ✅ 클릭 성공")
#             else:
#                 print("   ❌ 요소를 찾을 수 없습니다.")
#         except Exception as e:
#             print(f"   ❌ 에러: {e}")

#     def _click(self, xpath_or_css):
#         """[일반 클릭 전용] (하위 호환성 유지용)"""
#         print(f"🖱️  일반 클릭: {xpath_or_css}")
#         self._shadow_click(xpath_or_css)

# =================================================================
# =================================================================
# ======================== 테스트 케이스들 =========================

# def tc_01_signup(self):
#     print("\n[TC-01] 회원가입 성공 테스트")
#     print("가입 폼 작성 중...")
#     email = self.fake.free_email()
#     username = self.fake.user_name()
#     password = self.fake.password(length=6)
#     print(f"생성된 계정 정보 | ID: {username} / PW: {password} / Email: {email}")

#     self.driver.get(self.base_url)
#     time.sleep(10)
#     time.sleep(0.5)
#     print("로그인 버튼 클릭")
#     self._shadow_click('ahthentik_sso_btn')
#     self._shadow_click('submit')

#     print("정보 입력 중...")
#     self._shadow_fill('username', username)
#     self._shadow_fill('password', password)
#     self._shadow_fill('password_rep', password)
#     self._shadow_fill('email', email)
#     self._shadow_click('submit_btn')
#     time.sleep(2)
#     current = self.driver.current_url
#     if "9000" not in current and "8080" in current:
#         print("✅ Pass: 가입 성공 (리디렉션 완료)")
#     else:
#         print(f"❌ Fail: 가입 실패 (URL: {self.driver.current_url})")
#     time.sleep(0.5)
#     self.driver.delete_all_cookies()
#     self.driver.execute_script("window.localStorage.clear();")

# def tc_02_signup_duplicate(self):
#     print("\n[TC-02] 중복 가입 방지 테스트")
#     self.driver.get(self.base_url)
#     time.sleep(0.5)
#     print("SSO로그인 버튼 클릭")
#     self._shadow_click('ahthentik_sso_btn')
#     self._shadow_click('submit')

#     print("이미 가입된 이메일로 가입 시도")
#     existing_email = "test123@test.com"
#     existing_username = "test123"
#     existing_password = "test123"
#     print(f"가입 시도: {existing_username} / {existing_email}")
#     self._shadow_fill('username', existing_username)
#     self._shadow_fill('email', existing_email)
#     self._shadow_fill('password', existing_password)
#     self._shadow_fill('password_rep', existing_password)
#     self._shadow_click('submit_btn')
#     time.sleep(0.5)
#     print("결과 확인 중...")
#     current = self.driver.current_url
#     if "9000" in current:
#          print(f"✅ Pass: 중복 가입이 잘 막혔습니다. (현재 주소 유지됨)")
#     else:
#          print(f"❌ Fail: 중복인데 가입이 되어버렸습니다! (URL: {current})")

#     self.driver.delete_all_cookies()
#     self.driver.execute_script("window.localStorage.clear();")

# def tc_03_password_fail(self):
#     print("\n[TC-03] 로그인 비밀번호 실패 테스트")
#     self.driver.get(self.base_url)
#     time.sleep(0.5)
#     print("SSO로그인 버튼 클릭")
#     self._click("//button[contains(., 'SSO')]")

#     print("잘못된 비밀번호 입력 후 로그인 시도")
#     print(f"👉 로그인 시도: {self.existing_email},password:worng password")
#     self._shadow_fill('login_email', self.existing_email)
#     self._shadow_click('login_submit')
#     self._shadow_fill('login_password', "worng password")
#     self._shadow_click('end_login_submit')
#     print("결과 검증 중")
#     target_path = [
#         "ak-flow-executor",
#         "ak-stage-password",
#         "ak-flow-input-password > ak-form-element",
#         "p.pf-c-form__helper-text"  # 혹은 "div > p" (에러 메시지 태그)
#     ]
#     time.sleep(0.5)
#     error_element = self.get_shadow_element_v4(target_path)
#     if error_element:
#         error_text = error_element.text
#         print(f"  🔍 감지된 메시지: {error_text}")
#         expected_keywords = ["Invalid password"]
#         if any(keyword in error_text for keyword in expected_keywords):
#             print("✅ Pass: 로그인 실패 메시지가 정상적으로 출력되었습니다.")
#         else:
#             print(f"⚠️ Warning: 에러 요소는 찾았으나 메시지가 예상과 다릅니다. (내용: {error_text})")

#     self.driver.delete_all_cookies()
#     self.driver.execute_script("window.localStorage.clear();")

# def tc_04_login(self):
#     print("\n[TC-04] 로그인 테스트")
#     self.driver.get(self.base_url)
#     time.sleep(0.5)

#     print("SSO로그인 버튼 클릭")
#     self._click("//button[contains(., 'SSO')]")
#     print("이메일, 비밀번호 입력 후 로그인 시도")
#     time.sleep(0.5)
#     # 3. [핵심] 헬퍼 함수로 입력 (Shadow DOM 뚫고 입력함)
#     print(f"👉 로그인 시도: {self.existing_email}")
#     # 주소록에 적은 'login_email' 키를 사용
#     self._shadow_fill('login_email', self.existing_email)
#     self._shadow_click('login_submit')
#     time.sleep(0.5)
#     self._shadow_fill('login_password', self.existing_password)
#     self._shadow_click('end_login_submit')
#     # 5. 검증
#     time.sleep(0.5)
#     if "9000" not in self.driver.current_url:
#         print("✅ Pass: 로그인 성공")
#     else:
#         print(f"❌ Fail: 로그인 실패 (URL: {self.driver.current_url})")
#     time.sleep(0.5)

#     self.driver.delete_all_cookies()
#     self.driver.execute_script("window.localStorage.clear();")

# def tc_05_profile(self):
#     print("\n[TC-05] 프로필 수정 테스트")
#     self.driver.get(self.base_url)
#     time.sleep(0.5)

#     print(f"👉 로그인 시도: {self.existing_email}")
#     print("로그인")
#     time.sleep(0.5)
#     self._shadow_fill('login_main_email', self.existing_email)
#     self._shadow_fill('login_main_password', self.existing_password)
#     self._shadow_click('login_main_submit')
#     time.sleep(0.5)
#     print("대시보드 도달 확인")
#     time.sleep(0.5)
#     try:
#         # ==========================================================
#         print("👉 1. 상단 계정 아이콘 클릭")

#         avatar_selector = ".q-avatar"
#         avatar_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, avatar_selector)))
#         avatar_btn.click()
#         time.sleep(0.5) # 메뉴가 펼쳐질 때까지 잠시 대기

#         print("👉 2. 메뉴에서 Profile 클릭")

#         menu_text = "Profile"
#         profile_menu = self.driver.find_element(By.XPATH, f"//div[contains(text(), '{menu_text}')]")
#         profile_menu.click()
#         time.sleep(0.5) # 페이지 이동 대기

#         edit_profile = "Edit Profile"

#         edit_profile_block = self.driver.find_element(By.XPATH, f"//span[contains(., '{edit_profile}')]")
#         edit_profile_block.click()
#         time.sleep(0.5)
#         # ==========================================================
#         fake = Faker('ko_KR')# 한국어 전화번호 생성기
#         new_phone = fake.numerify(text='010-####-####')# 새로운 전화번호 생성
#         print(f"👉 3. 새 전화번호 입력: {new_phone}")
#         phone_input = self.driver.find_element(By.XPATH, "//input[@aria-label='Phone *']")# 전화번호 입력창 찾기
#         phone_input.send_keys(Keys.CONTROL + "a")# 기존 값 지우기
#         phone_input.send_keys(Keys.DELETE)
#         phone_input.send_keys(new_phone)
#         # ==========================================================
#         full_name = self.driver.find_element(By.XPATH, "//input[@aria-label='Full Name *']")# 이름 입력창 찾기
#         full_name.send_keys(Keys.CONTROL + "a")
#         full_name.send_keys(Keys.DELETE)
#         full_name.send_keys(self.fake.name())# 이름 재입력
#         time.sleep(0.5)
#         # 3단계: 저장(Update) 버튼 클릭
#         # ==========================================================
#         print("👉 4. Update 버튼 클릭")
#         button_text = "Update"
#         update_btn = self.driver.find_element(By.XPATH, f"//button[contains(., 'Update')]")
#         update_btn.click()
#         # ==========================================================
#         print("👉 5. 'updated successfully' 메시지 확인 중...")
#         time.sleep(0.5)
#         # 화면 전체에서 해당 텍스트가 떴는지 찾습니다. (토스트 메시지 감지)
#         body_text = self.driver.find_element(By.TAG_NAME, "body").text # <body> 전체 텍스트

#         time.sleep(0.5)
#         if "updated successfully" in body_text:
#             print("✅ Pass: 성공 메시지 확인됨")
#         else:
#             print(f"⚠️ Warning: 성공 메시지를 못 찾았습니다. (화면에 뜬 텍스트: {body_text[:50]}...)")
#     except Exception as e:
#             print(f"❌ 에러 발생: {e}")

#     self.driver.delete_all_cookies()
#     self.driver.execute_script("window.localStorage.clear();")


# def tc_06_teamfeild(self):
#     print("tc_06 팀필드 제작 테스트")
#     self.driver.get(self.base_url)
#     time.sleep(0.5)
#     team_name = f"{self.fake.color_name()} 프로젝트"
#     self._shadow_fill('login_main_email', self.existing_email)
#     self._shadow_fill('login_main_password', self.existing_password)
#     self._shadow_click('login_main_submit')

#     print("\n[TC-07] 팀 생성 및 멤버 초대 테스트")
#     print("대시보드 도달 확인")
#     time.sleep(0.5)
#     print("사이드바에서 'Teams' 메뉴 클릭")
#     self._shadow_click("menu_teams")
#     time.sleep(0.5)
#     print("'new Team' 버튼 클릭")
#     new_team_span = self.driver.find_element(By.XPATH, "//span[contains(text(), 'New Team')]")
#     new_team_span.click()
#     time.sleep(0.5)
#     print("팀 이름 입력")
#     team_name_input = self.driver.find_element(By.XPATH, "//input[@aria-label='Team Name *']")
#     team_name_input.send_keys(team_name)
#     target_member = "test123"
#     print("팀 멤버 검색시도: {test123}")
#     self.driver.find_element(By.XPATH, "//input[@aria-label='Select Initial Members']")# 팀 멤버 검색창 찾기
#     self._shadow_fill("//input[@aria-label='Select Initial Members']", target_member)# 팀 멤버 검색어 입력
#     time.sleep(0.5)
#     try:
#         self._click(f"//div[@role='listbox']//div[contains(text(), '{target_member}')]")
#         print("맴버선택완료")
#     except:
#         print("맴버선택실패")
#         self._click("//span[contains(text(), 'Create')]")
#     time.sleep(0.5)
#     print("팀 생성 버튼 클릭")
#     self._click("//span[contains(text(), 'Create')]")

#     time.sleep(0.5)
#     if team_name in self.driver.page_source:
#         print(f"✅ Pass: {team_name}")
#     else:
#         print(f"❌ Fail: {team_name} 없음")

#     self.driver.delete_all_cookies()
#     self.driver.execute_script("window.localStorage.clear();")

# def tc_07_projectfeild(self):
#     print("tc_07 프로젝트 필드 입력 테스트")
#     self.driver.get(self.base_url)
#     time.sleep(0.5)
#     self._shadow_fill('login_main_email', self.existing_email)
#     self._shadow_fill('login_main_password', self.existing_password)
#     self._shadow_click('login_main_submit')
#     print("대시보드 도달 확인")
#     time.sleep(0.5)
#     print("사이드바에서 'Projects' 메뉴 클릭")
#     self._shadow_click("menu_projects")
#     time.sleep(0.5)
#     print("'New Project' 버튼 클릭")
#     new_project_span = self.driver.find_element(By.XPATH, "//span[contains(text(), 'New Project')]")
#     new_project_span.click()
#     time.sleep(0.5)
#     project_name = f"{self.fake.color_name()} 개발 프로젝트"
#     print("프로젝트 이름 입력")
#     project_name_input = self.driver.find_element(By.XPATH, "//input[@aria-label='프로젝트 이름 *']")
#     project_name_input.send_keys(project_name)
#     print("프로젝트 키 입력")
#     upper_project_key = self.fake.color_name().upper()
#     project_key_input = self.driver.find_element(By.XPATH, "//input[@aria-label='프로젝트 키 *']")# 프로젝트 키 입력창 찾기
#     project_key_input.send_keys(upper_project_key)
#     print("프로젝트 팀 선택")# 클릭해서 드롭다운 열기
#     project_team_select = "//div[contains(@class, 'q-field__control') and .//div[contains(., 'Team *')]]"# XPath 수정
#     self._click(project_team_select)# 클릭해서 드롭다운 열기
#     time.sleep(0.5)# 대기
#     option_xpath = "//div[@role='option']//span[contains(text(), 'test')]"
#     self._click(option_xpath)
#     time.sleep(0.5)
#     print("프로젝트 생성 버튼 클릭")
#     self._click("//span[contains(text(), 'Create')]")
#     time.sleep(0.5)
#     if project_name in self.driver.page_source:
#         print(f"✅ Pass: {project_name}")
#     else:
#         print(f"❌ Fail: {project_name} 없음")
#     self.driver.delete_all_cookies()
#     self.driver.execute_script("window.localStorage.clear();")


# def tc_08_sprint(self):
#     print("\n[TC-08] 스프린트 생성 테스트")
#     self.driver.get(self.base_url)
#     time.sleep(0.5)
#     self._shadow_fill('login_main_email', self.existing_email)
#     self._shadow_fill('login_main_password', self.existing_password)
#     self._shadow_click('login_main_submit')
#     print("대시보드 도달 확인")
#     time.sleep(0.5)
#     print("사이드바에서 Sprints 메뉴 클릭")
#     self._shadow_click("//div[@role='listitem' and contains(., 'Sprints')]")
#     time.sleep(0.5)
#     print("'New Sprint' 버튼 클릭")
#     new_sprint_span = self.driver.find_element(By.XPATH, "//span[contains(text(), 'New Sprint')]")
#     new_sprint_span.click()
#     time.sleep(0.5)
#     print("프로젝트 선택")
#     project_select = "//div[contains(@class, 'q-field__control') and .//div[contains(., 'Project *')]]"
#     self._click(project_select)
#     time.sleep(0.5)
#     option_xpath = "//div[@role='option']//span[contains(text(), 'test')]"
#     self._click(option_xpath)
#     time.sleep(0.5)
#     print("스프린트 이름 입력")
#     sprint_name = f"{self.fake.color_name()} 스프린트"
#     sprint_name_input = self.driver.find_element(By.XPATH, "//input[@aria-label='Sprint Name *']")
#     sprint_name_input.send_keys(sprint_name)
#     time.sleep(0.5)
#     print("status 선택")
#     status_xpath = self._click("//i[contains(text(), 'event_note')]")
#     self._click(status_xpath)
#     time.sleep(0.5)
#     active_ele = self.driver.switch_to.active_element
#     active_ele.send_keys(Keys.ARROW_UP)
#     time.sleep(0.5)
#     active_ele.send_keys(Keys.ENTER)
#     time.sleep(0.5)

#     print("스프린트 생성 버튼 클릭")
#     self._click("//span[contains(text(), 'Create')]")
#     time.sleep(0.5)
#     if sprint_name in self.driver.page_source:
#         print(f"✅ Pass: {sprint_name}")
#     else:
#         print(f"❌ Fail: {sprint_name} 없음")

#     self.driver.delete_all_cookies()
#     self.driver.execute_script("window.localStorage.clear();")

# def tc_09_issue(self):
#     print("\n[TC-09] 이슈 생성 테스트")
#     self.driver.get(self.base_url)
#     time.sleep(0.5)
#     self._shadow_fill('login_main_email', self.existing_email)
#     self._shadow_fill('login_main_password', self.existing_password)
#     self._shadow_click('login_main_submit')
#     print("대시보드 도달 확인")
#     time.sleep(0.5)
#     print("사이드바에서 Issues 메뉴 클릭")
#     self._shadow_click("//div[@role='listitem' and contains(., 'Issues')]")
#     time.sleep(0.5)
#     print("'New Issue' 버튼 클릭")
#     new_issue_span = self.driver.find_element(By.XPATH, "//span[contains(text(), 'New Issue')]")
#     new_issue_span.click()
#     time.sleep(0.5)
#     print("이슈 제목 입력")
#     issue_title = f"{self.fake.color_name()} 버그 이슈"
#     issue_title_input = self.driver.find_element(By.XPATH, "//input[@aria-label='Title *']")
#     issue_title_input.send_keys(issue_title)
#     time.sleep(0.5)
#     print("프로젝트 선택")
#     project_select = "//div[contains(@class, 'q-field__control') and .//div[contains(., 'Project *')]]"
#     self._click(project_select)
#     time.sleep(0.5)
#     option_xpath = "//div[@role='option']//span[contains(text(), 'test')]" # 프로젝트 선택
#     self._click(option_xpath)
#     time.sleep(0.5)
#     print("이슈 타입 선택")
#     issue_type_select = "//div[contains(@class, 'q-field__control') and .//div[contains(., 'Type *')]]"
#     self._click(issue_type_select)
#     time.sleep(0.5)
#     issue_type_option = "//div[@role='option']//span[contains(text(), 'Bug')]"
#     self._click(issue_type_option)
#     time.sleep(0.5)
#     print("이슈 생성 버튼 클릭")
#     self._click("//span[contains(text(), 'Create')]")
#     time.sleep(0.5)
#     if issue_title in self.driver.page_source:
#         print(f"✅ Pass: {issue_title}")
#     else:
#         print(f"❌ Fail: {issue_title} 없음")
#     self.driver.delete_all_cookies()
#     self.driver.execute_script("window.localStorage.clear();")

# def tc_10_kanbanboard(self):
#     print("\n[TC-10] 칸반보드 테스트")
#     self.driver.get(self.base_url)
#     time.sleep(0.5)
#     self._shadow_fill('login_main_email', self.existing_email)
#     self._shadow_fill('login_main_password', self.existing_password)
#     self._shadow_click('login_main_submit')
#     print("대시보드 도달 확인")
#     time.sleep(0.5)
#     print("사이드바에서 Kanban Board 메뉴 클릭")
#     self._shadow_click("//div[@role='listitem' and contains(., 'Kanban Board')]")
#     time.sleep(0.5)
#     source = self.driver.find_element(By.XPATH, "//div[contains(text(), 'test')]")
#     target = self.driver.find_element(By.XPATH, "//div[contains(text(), 'In Progress')]/ancestor::div[contains(@class, 'column')]")
#     actions = ActionChains(self.driver)
#     actions.drag_and_drop(source, target).perform()
#     time.sleep(0.5)
#     assert "test" in self.driver.find_element(By.XPATH, "//div[contains(@class, 'q-card') and contains(., 'In Progress')]").text
#     print("✅ 검증 완료 : 이슈가 'In Progress' 칼럼으로 이동됨")
#     self.driver.delete_all_cookies()
#     self.driver.execute_script("window.localStorage.clear();")

# def tc_11_logout(self):
#     print("\n[TC-11] 로그아웃 테스트")
#     self.driver.get(self.base_url)
#     time.sleep(0.5)
#     self._shadow_fill('login_main_email', self.existing_email)
#     self._shadow_fill('login_main_password', self.existing_password)
#     self._shadow_click('login_main_submit')
#     print("대시보드 도달 확인")
#     time.sleep(0.5)
#     print("상단 계정 아이콘 클릭")
#     avatar_selector = ".q-avatar"
#     avatar_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, avatar_selector)))
#     avatar_btn.click()
#     time.sleep(0.5) # 메뉴가 펼쳐질 때까지 잠시 대기

#     print("메뉴에서 Logout 클릭")
#     menu_text = "Logout"
#     logout_menu = self.driver.find_element(By.XPATH, f"//div[contains(text(), '{menu_text}')]")
#     logout_menu.click()
#     time.sleep(0.5) # 페이지 이동 대기

#     print("로그아웃 후 로그인 페이지 도달 확인")
#     time.sleep(0.5)
#     if "login" in self.driver.current_url:
#         print("✅ Pass: 로그아웃 성공")


# =================================================================
# if __name__ == "__main__":
#     runner = DevFlowTestRunner()

#     target_tcs = [
#         "tc_01_signup",
#         "tc_02_signup_duplicate",
#         "tc_03_password_fail",
#         "tc_04_login",
#         "tc_05_profile",
#         "tc_06_teamfeild",
#         "tc_07_projectfeild",
#         "tc_08_sprint",
#         "tc_09_issue",
#         "tc_10_kanbanboard",
#         "tc_11_logout",


#     ]

#     try:
#         for tc_name in target_tcs:
#             if hasattr(runner, tc_name):
#                 print(f"\n▶️  {tc_name} 실행 중...")
#                 getattr(runner, tc_name)() # 함수 실행
#                 print(f"✅ {tc_name} 완료\n")
#             else:
#                 print(f"⚠️  경고: {tc_name} 함수가 없습니다.")
#     except Exception as e:
#         print(f"\n❌ 에러 발생: {e}")
#     finally:
#         runner.teardown()
