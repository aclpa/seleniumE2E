import sys
import os

sys.path.append(os.getcwd())
from src.utils.api_client import APIClient


def clean_all_test_data():
    api = APIClient()
    print("🧹 데이터 대청소를 시작합니다...")

    try:
        api.login()

        # 1. 모든 팀 가져오기
        response_data = api.get_all_teams()

        # 🌟 [수정] 응답이 딕셔너리라면 진짜 리스트(알맹이)를 꺼냄
        teams = []
        if isinstance(response_data, list):
            teams = response_data
        elif isinstance(response_data, dict):
            # 보통 'items', 'teams', 'data' 같은 키 안에 리스트가 들어있음
            for key in ["items", "teams", "data", "results"]:
                if key in response_data and isinstance(response_data[key], list):
                    teams = response_data[key]
                    break

            # 못 찾았으면 그냥 값들 중에 리스트인 거 찾기
            if not teams:
                for val in response_data.values():
                    if isinstance(val, list):
                        teams = val
                        break

        print(f"📋 현재 총 {len(teams)}개의 팀이 발견되었습니다.")

        count = 0
        for team in teams:
            # 안전장치: 딕셔너리가 아닌 이상한 데이터는 건너뜀
            if not isinstance(team, dict):
                continue

            team_name = team.get("name", "")
            team_id = team.get("id")

            # 2. 삭제할 대상인지 확인 (Locust, Auto, Team_ 등이 포함된 경우)
            if any(
                keyword in team_name for keyword in ["Locust", "Auto", "Load", "Team_"]
            ):
                print(f"🗑️ [삭제 중] {team_name} (ID: {team_id})")

                try:
                    api.delete_team(team_id)
                    count += 1
                except Exception as e:
                    print(f"   -> ⚠️ 삭제 실패: {e}")
            else:
                print(f"🛡️ [보존] {team_name} (실제 데이터로 추정)")

        print(f"\n✨ 청소 끝! 총 {count}개의 테스트 팀을 삭제했습니다.")

    except Exception as e:
        print(f"❌ 에러 발생: {e}")


if __name__ == "__main__":
    clean_all_test_data()
