import requests
from src.config.config import Config

class APIClient:

    def __init__(self):
        self.token = None
        self.headers = {}
        self.API_URL = Config.API_URL
        self.session = requests.Session()

    def login(self):
        """관리자 계정으로 API 로그인"""
        payload = {
            "email": Config.TEST_EMAIL,
            "password": Config.TEST_PASSWORD
        }
        # JSON Body로 로그인 요청
        response = requests.post(f"{self.API_URL}/auth/login", json=payload)
        
        if response.status_code != 200:
            raise Exception(f"API 로그인 실패: {response.text}")
            
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
        print(f"🔑 [API] 로그인 성공")

        response = self.session.post(f"{self.API_URL}/auth/login", json=payload)
        
        if response.status_code != 200:
            raise Exception(f"로그인 실패: {response.text}")

        # 2. 토큰 추출 
        token = response.json().get('access_token') 
        
        # 3. 세션 헤더에 토큰 설정
        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })
        
        print(f"🔑 [API] 로그인 성공 (토큰 획득)")

    def create_team(self, name):
        """[필수] 팀 생성 메서드"""
        if not self.token:
            self.login()
            
        payload = {
            "name": name,
            "description": "Selenium Test Team"
        }
        # 팀 생성 요청
        res = requests.post(f"{self.API_URL}/teams/", json=payload, headers=self.headers)
        
        if res.status_code != 201:
            raise Exception(f"팀 생성 실패: {res.text}")
            
        data = res.json()
        print(f"🏢 [API] 팀 생성 완료: {data['name']} (ID: {data['id']})")
        return data

    def create_project(self, name, key, team_id):
        """프로젝트 생성 (team_id 필수)"""
        if not self.token:
            self.login()

        payload = {
            "name": name,
            "key": key,
            "description": "Selenium Test Project",
            "team_id": team_id  # 팀 ID 포함
        }
        
        # 프로젝트 생성 요청
        res = requests.post(f"{self.API_URL}/projects/", json=payload, headers=self.headers)
        
        if res.status_code not in [200, 201]:
             raise Exception(f"프로젝트 생성 실패: {res.text}")
             
        data = res.json()
        print(f"🏗️ [API] 프로젝트 생성 완료: {data['name']} (ID: {data['id']})")
        return data

    def create_issue(self, project_id, title):  
        """
        API로 이슈를 생성합니다.
        :param project_id: 이슈가 속할 프로젝트 ID (필수)
        :param title: 이슈 제목
        :param sprint_id: (선택) 스프린트 ID
        """
        if not self.token:
            self.login()
        
        payload = {
            "project_id": project_id,
            "title": title,
            "type": "task",
            "priority": "medium",
            "status": "todo"
        }

        response = requests.post(f"{self.API_URL}/issues", json=payload, headers=self.headers)

        if response.status_code != 201:
            raise Exception(f"이슈 생성 실패: {response.text}")
            
        return response.json()


    def delete_issue(self, issue_id):
        # 이제 self.session을 사용할 수 있습니다.
        url = f"{self.API_URL}/issues/{issue_id}"
        response = self.session.delete(url) # ✅ 에러 해결
        return response

    def delete_project(self, project_id):
        """프로젝트 삭제"""
        url = f"{self.API_URL}/projects/{project_id}"
        response = self.session.delete(url)
        
        if response.status_code not in [200, 204]:
            raise Exception(f"프로젝트 삭제 실패: {response.text}")
        return response

    def delete_team(self, team_id):
        """팀 삭제"""
        url = f"{self.API_URL}/teams/{team_id}"
        response = self.session.delete(url)
        
        if response.status_code not in [200, 204]:
            raise Exception(f"팀 삭제 실패: {response.text}")
        return response