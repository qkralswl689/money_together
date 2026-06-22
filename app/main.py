from fastapi import FastAPI
from pydantic import BaseModel
from app.api.codef_client import CodeFClient

app = FastAPI()
codef_client = CodeFClient()

# 계정 등록용 요청 모델
class AccountRegisterRequest(BaseModel):
    organization: str
    login_id: str
    login_password: str

# 카드 내역 조회용 요청 모델
class CardTransactionRequest(BaseModel):
    connected_id: str
    organization: str
    start_date: str
    end_date: str

@app.get("/")
def read_root():
    return {"message": "가계부 API 서버 정상 작동 중입니다."}

# 1. 카드사 계정 등록 (Connected ID 발급)
@app.post("/register-account")
def register_account(request: AccountRegisterRequest):
    try:
        result = codef_client.register_account(
            organization=request.organization,
            login_id=request.login_id,
            login_password=request.login_password
        )
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 2. 카드 승인 내역 조회
@app.post("/get-card-transactions")
def get_card_transactions(request: CardTransactionRequest):
    try:
        result = codef_client.get_card_approvals(
            connected_id=request.connected_id,
            organization=request.organization,
            start_date=request.start_date,
            end_date=request.end_date
        )
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}