import requests
from src.config.config import Config

class APIClient:
    BASE_URL = "http://localhost:8000/api/v1"

    def __init__(self):
        self.token = None
        self.headers = {}

    def login(self):
        """관리자 계정으로 API 로그인"""
        payload = {
            "email": Config.TEST_EMAIL,
            "password": Config.TEST_PASSWORD
        }
        # JSON Body로 로그인 요청
        response = requests.post(f"{self.BASE_URL}/auth/login", json=payload)
        
        if response.status_code != 200:
            raise Exception(f"API 로그인 실패: {response.text}")
            
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
        print(f"🔑 [API] 로그인 성공")

    def create_team(self, name):
        """[필수] 팀 생성 메서드"""
        if not self.token:
            self.login()
            
        payload = {
            "name": name,
            "description": "Selenium Test Team"
        }
        # 팀 생성 요청
        res = requests.post(f"{self.BASE_URL}/teams/", json=payload, headers=self.headers)
        
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
        res = requests.post(f"{self.BASE_URL}/projects/", json=payload, headers=self.headers)
        
        if res.status_code not in [200, 201]:
             raise Exception(f"프로젝트 생성 실패: {res.text}")
             
        data = res.json()
        print(f"🏗️ [API] 프로젝트 생성 완료: {data['name']} (ID: {data['id']})")
        return data