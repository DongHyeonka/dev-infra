from locust import HttpUser, task, between
import json
import random
import string

class AccountServiceUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    def on_start(self):
        """테스트 시작 시 실행되는 메서드"""
        self.base_url = "/api/accounts"
        self.client.verify = False
    
    def generate_random_email(self):
        """랜덤 이메일 생성"""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        domain = random.choice(['gmail.com', 'naver.com', 'daum.net', 'yahoo.com'])
        return f"{username}@{domain}"
    
    def generate_random_username(self):
        """랜덤 사용자명 생성"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(5, 12)))
    
    def generate_random_password(self):
        """랜덤 비밀번호 생성 (최소 8자)"""
        length = random.randint(8, 16)
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choices(characters, k=length))
    
    @task(1)
    def signup_performance_test(self):
        """정상 회원가입 성능 테스트 - 기본 성능 측정용"""
        signup_data = {
            "email": self.generate_random_email(),
            "username": self.generate_random_username(),
            "password": self.generate_random_password()
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        with self.client.post(
            f"{self.base_url}/signup",
            json=signup_data,
            headers=headers,
            catch_response=True
        ) as response:
            if response.status_code == 201:
                response.success()
            elif response.status_code == 409:
                # 이미 존재하는 이메일/사용자명 - 성능에는 영향 없음
                response.success()
            else:
                response.failure(f"Unexpected status code: {response.status_code}, Response: {response.text}")
