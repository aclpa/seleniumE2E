import os
import sys
import random
from locust import HttpUser, task, between, events

# 1. 프로젝트 루트 경로를 파이썬 경로에 추가 (src 폴더를 찾기 위해 필수)
sys.path.append(os.getcwd())

# 2. 만든 모듈 가져오기
from src.utils.api_client import APIClient
from src.config.config import Config


class KanbanLoadUser(HttpUser):
    # 유저 한 명이 API 요청을 보내고 다음 요청까지 기다리는 시간 (1초~3초 랜덤)
    wait_time = between(1, 3)

    def on_start(self):
        """
        [가상 유저 접속 시 1회 실행]
        1. APIClient를 생성하고,
        2. Locust의 통계 수집 기능(self.client)을 APIClient에 이식합니다.
        3. 로그인하고 테스트용 프로젝트를 하나 만듭니다.
        """
        # 기존 APIClient 객체 생성
        self.api = APIClient()


        self.api.session = self.client

        # Locust 실행 시 입력한 주소
        self.api.BASE_URL = self.host

        print(f"👤 User {self.environment.runner.user_count}: 로그인 시도...")

        # 1. 로그인 
        try:
            self.api.login()
        except Exception as e:
            print(f"❌ 로그인 실패: {e}")
            self.environment.runner.quit()  # 로그인 못하면 테스트 종료
            return

        # 2. 부하 테스트를 위한 임시 팀 & 프로젝트 생성
        try:
            rnd = random.randint(1000, 9999)

            # 팀 생성
            team_name = f"LoadTeam_{rnd}"
            team = self.api.create_team(team_name)
            self.team_id = team["id"]

            # 프로젝트 생성
            proj_name = f"LoadProj_{rnd}"
            proj_key = f"LP{rnd}"
            project = self.api.create_project(proj_name, proj_key, self.team_id)
            self.project_id = project["id"]

            print(f"✅ Setup 완료: Project ID {self.project_id}")

        except Exception as e:
            print(f"⚠️ Setup 실패: {e}")
            self.project_id = None  # 실패 시 플래그 처리

    @task(3)
    def create_and_delete_issue_scenario(self):
        """
        [반복 수행 작업]
        이슈 생성 -> (잠시 대기) -> 이슈 삭제
        """
        if not self.project_id:
            return

        # 랜덤 제목으로 이슈 생성
        issue_title = f"LoadTest_Issue_{random.randint(1, 100000)}"

        try:
            # 1. 이슈 생성 요청
            issue = self.api.create_issue(self.project_id, issue_title)
            issue_id = issue["id"]


            self.api.delete_issue(issue_id)

        except Exception as e:

            pass

    @task(1)
    def just_view_dashboard(self):
        """
        [가끔 수행 작업]
        단순 조회 (서버 부하 분산용)
        """
        # APIClient에 대시보드 조회 기능이 없다면 직접 호출

        self.client.get("/api/dashboard", name="/api/dashboard (View)")

    def on_stop(self):
        """
        [가상 유저 종료 시 1회 실행]
        뒷정리: 만들었던 팀과 프로젝트를 삭제합니다.
        """
        if hasattr(self, "team_id") and self.team_id:
            print(f"🧹 Cleanup: 팀 삭제 (ID: {self.team_id})")
            try:
                self.api.delete_team(self.team_id)
            except:
                pass
