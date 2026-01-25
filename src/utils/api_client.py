import requests
from src.config.config import Config


class APIClient:

    def __init__(self):
        self.token = None
        # Locust가 주입해줄 host 주소를 받기 위해 변수로 관리
        self.API_URL = Config.API_URL
        
        self.session = requests.Session()

    def login(self):
        """관리자 계정으로 로그인하고 세션에 토큰 저장"""
        payload = {"email": Config.TEST_EMAIL, "password": Config.TEST_PASSWORD}

  
        response = self.session.post(f"{self.API_URL}/auth/login", json=payload)

        if response.status_code != 200:
            raise Exception(f"로그인 실패: {response.text}")

        # 토큰 추출
        data = response.json()
        self.token = data.get("access_token")

        # 
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        print(f"🔑 [API] 로그인 성공")

    def create_team(self, name):
        """팀 생성"""
        if not self.token:
            self.login()

        payload = {"name": name, "description": "Auto Test Team"}
        res = self.session.post(f"{self.API_URL}/teams/", json=payload)

        if res.status_code != 201:
            raise Exception(f"팀 생성 실패: {res.text}")

        return res.json()

    def create_project(self, name, key, team_id):
        """프로젝트 생성"""
        if not self.token:
            self.login()

        payload = {
            "name": name,
            "key": key,
            "description": "Auto Test Project",
            "team_id": team_id,
        }


        res = self.session.post(f"{self.API_URL}/projects/", json=payload)

        if res.status_code not in [200, 201]:
            raise Exception(f"프로젝트 생성 실패: {res.text}")

        return res.json()

    def create_issue(self, project_id, title):
        """이슈 생성"""
        if not self.token:
            self.login()

        payload = {
            "project_id": project_id,
            "title": title,
            "type": "task",
            "priority": "medium",
            "status": "todo",
        }


        response = self.session.post(f"{self.API_URL}/issues", json=payload)

        if response.status_code != 201:
            raise Exception(f"이슈 생성 실패: {response.text}")

        return response.json()

    def delete_issue(self, issue_id):
        url = f"{self.API_URL}/issues/{issue_id}"
        return self.session.delete(url)

    def delete_project(self, project_id):
        url = f"{self.API_URL}/projects/{project_id}"
        return self.session.delete(url)

    def delete_team(self, team_id):
        url = f"{self.API_URL}/teams/{team_id}"
        return self.session.delete(url)



    def get_all_teams(self):
        """모든 팀 목록을 가져옵니다"""
        if not self.token:
            self.login()

        # 팀 목록 조회 API 호출 (GET)
        res = self.session.get(f"{self.API_URL}/teams/")

        if res.status_code != 200:
            print(f"⚠️ 팀 목록 조회 실패: {res.text}")
            return []

        return res.json()
