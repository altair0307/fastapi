from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 1. n8n에서 보낼 데이터의 모양(구조)을 정의합니다.
class InputData(BaseModel):
    message: str
    # 필요하다면 아래처럼 항목을 계속 추가할 수 있습니다.
    # user_id: int 
    # email: str

# 2. @app.get 대신 @app.post를 사용합니다.
@app.post("/")
def process_data(data: InputData):
    # n8n에서 보낸 데이터를 꺼내서 변수에 담습니다.
    received_message = data.message
    
    # -----------------------------------------
    # 💡 여기에 원하는 파이썬 작업을 작성하세요! 
    # 예: 크롤링, AI 요약, 데이터 분석 등...
    # -----------------------------------------
    
    # 작업이 끝난 후 n8n으로 돌려보낼 결과값입니다. (JSON 형태)
    return {
        "status": "success",
        "original_message": received_message,
        "result": f"파이썬이 '{received_message}'를 잘 받아서 처리했습니다!"
    }
