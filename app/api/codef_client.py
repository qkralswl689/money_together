import requests
import os
import time
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

class CodeFClient:
    def __init__(self):
        self.client_id = os.getenv("CODEF_CLIENT_ID")
        self.client_secret = os.getenv("CODEF_CLIENT_SECRET")
        self.base_url = "https://development.codef.io/v1"  # 샌드박스 URL
        self.token_url = "https://oauth.codef.io/oauth/token"
        self._access_token = None
        self._token_expires_at = 0

    def get_token(self):
        """Access Token 발급 및 캐싱 (만료 전 재사용)"""
        if self._access_token and time.time() < self._token_expires_at:
            return self._access_token

        data = {"grant_type": "client_credentials", "scope": "read"}
        
        response = requests.post(
            self.token_url, 
            data=data, 
            auth=(self.client_id, self.client_secret)
        )
        
        if response.status_code == 200:
            token_data = response.json()
            self._access_token = token_data.get("access_token")
            expires_in = token_data.get("expires_in", 3600)
            self._token_expires_at = time.time() + expires_in - 60 
            return self._access_token
        else:
            raise Exception(f"토큰 발급 실패: {response.text}")

    def register_account(self, organization, login_id, login_password):
        """카드사 계정 등록 API (Connected ID 발급용)"""
        url = f"{self.base_url}/account/create"
        
        headers = {
            "Authorization": f"Bearer {self.get_token()}",
            "Content-Type": "application/json"
        }
        
        # 계정 등록 페이로드
        payload = {
            "accountList": [
                {
                    "countryCode": "KR",
                    "businessType": "BK", 
                    "organization": organization,
                    "loginType": "0", 
                    "loginId": login_id,
                    "loginPassword": login_password
                }
            ]
        }
        
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def get_card_approvals(self, connected_id, organization, start_date, end_date):
        """카드 승인내역 조회 API"""
        url = f"{self.base_url}/kr/card/p/approval"
        
        headers = {
            "Authorization": f"Bearer {self.get_token()}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "connectedId": connected_id,
            "organization": organization,
            "startDate": start_date,
            "endDate": end_date
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}