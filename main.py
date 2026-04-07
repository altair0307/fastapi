from fastapi import FastAPI
from pydantic import BaseModel
from pytrends.request import TrendReq
import pandas as pd

app = FastAPI()

# 1. n8n에서 받을 데이터 형태 정의 (검색어)
class TrendInput(BaseModel):
    keyword: str

# 2. POST 요청 처리
@app.post("/")
def get_google_trends(data: TrendInput):
    keyword = data.keyword
    
    try:
        # Pytrends 설정 (한국어, 한국 표준시 tz=540)
        pytrend = TrendReq(hl='ko-KR', tz=540)
        
        # 검색어 리스트 구성 (한 번에 여러 개도 가능하지만 여기선 1개만)
        kw_list = [keyword]
        
        # 페이로드 빌드 (최근 7일, 한국 기준)
        # timeframe 옵션: 'now 7-d' (최근 7일), 'today 1-m' (최근 1개월), 'today 3-m' (최근 3개월) 등
        pytrend.build_payload(kw_list, cat=0, timeframe='now 7-d', geo='KR', gprop='')
        
        # 시간에 따른 관심도 데이터 가져오기
        df = pytrend.interest_over_time()
        
        # 데이터가 없는 경우 처리
        if df.empty:
            return {
                "status": "empty",
                "keyword": keyword,
                "message": "해당 검색어의 트렌드 데이터가 부족합니다."
            }
            
        # 불필요한 'isPartial' 컬럼 제거
        df = df.drop(columns=['isPartial'], errors='ignore')
        
        # 날짜(인덱스)를 문자열로 변환 (JSON으로 보내기 위해)
        df.index = df.index.astype(str)
        
        # 데이터프레임을 딕셔너리로 변환
        trend_data = df.to_dict()[keyword]
        
        return {
            "status": "success",
            "keyword": keyword,
            "trend_data": trend_data
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
