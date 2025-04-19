from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 또는 ["*"] (전체 허용)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JSON 데이터 로딩 (최상단에서 미리 로딩해서 전역 변수로 보존)
data_path = os.path.join(os.path.dirname(__file__), "depression_data.json")

try:
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print("데이터 로딩 실패:", e)
    data = []

# 테스트용 루트
@app.get("/")
def root():
    return {"message": "정신건강 우울감 API - /depression?age=17&gender=female&year=2023"}

@app.get("/depression")
def get_depression(age: int, gender: str, year: int):
    print(f"[요청] age={age}, gender={gender}, year={year}")

    for item in data:
        if item["age"] == age and item["gender"] == gender and item["year"] == year:
            print("[찾음 ✅]", item)
            return {"depression_rate": item["depression_rate"]}

    print("[실패 ❌] 조건에 맞는 데이터 없음")
    return {"depression_rate": None}
