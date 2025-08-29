from locust import HttpUser, task, between
import json
import random

class LoginTest(HttpUser):
    wait_time = between(1, 2)
    
    def on_start(self):
        """테스트 시작 시 실행되는 메서드"""
        # 테스트용 사용자 계정 (실제 DB에 존재하는 계정으로 변경 필요)
        self.test_user = {"username": "testuser", "password": "password123"}
    
    @task
    def test_login(self):
        """로그인 기능 테스트"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # 로그인 요청
        with self.client.post(
            "/api/accounts/login",
            json=self.test_user,
            headers=headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
                print(f"로그인 성공: {response.status_code}")
                # 응답에서 토큰 확인
                try:
                    token_data = response.json()
                    if "accessToken" in token_data:
                        print(f"액세스 토큰 받음: {token_data['accessToken'][:20]}...")
                except Exception as e:
                    print(f"응답 파싱 오류: {e}")
            else:
                response.failure(f"로그인 실패 - 상태코드: {response.status_code}, 응답: {response.text}")
                print(f"로그인 실패: {response.status_code} - {response.text}")
    