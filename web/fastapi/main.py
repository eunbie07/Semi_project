from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # 프론트엔드 주소에 맞게 수정 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JSON 파일 경로 설정
base_dir = os.path.dirname(__file__)
depression_path = os.path.join(base_dir, "json/depression_data.json")
breakfast_path = os.path.join(base_dir, "json/breakfast_skip.json")

# 데이터 로딩
try:
    with open(depression_path, "r", encoding="utf-8") as f:
        depression_data = json.load(f)
except Exception as e:
    print("우울감 데이터 로딩 실패:", e)
    depression_data = []

try:
    with open(breakfast_path, "r", encoding="utf-8") as f:
        breakfast_data = json.load(f)
except Exception as e:
    print("아침결식률 데이터 로딩 실패:", e)
    breakfast_data = []

# 기본 경로
@app.get("/")
def root():
    return {
        "message": "정신건강 우울감 API - /depression?age=17&gender=female&year=2023\n"
                   "아침결식률 API - /breakfast_skip_rate?age=17&gender=여자&year=2023"
    }

# 우울감 데이터 API
@app.get("/depression")
def get_depression(age: int, gender: str, year: int):
    print(f"[우울감 요청] age={age}, gender={gender}, year={year}")
    for item in depression_data:
        if item["age"] == age and item["gender"] == gender and item["year"] == year:
            print("[우울감 데이터 찾음]", item)
            return {"depression_rate": item["depression_rate"]}
    print("[우울감 데이터 없음]")
    return {"depression_rate": None}

# 아침 결식률 데이터 API
@app.get("/breakfast_skip_rate")
def get_breakfast_skip_rate(age: int, gender: str, year: int):
    print(f"[아침결식 요청] age={age}, gender={gender}, year={year}")
    for item in breakfast_data:
        try:
            if int(item["age"]) == age and item["gender"] == gender and int(item["year"]) == year:
                print("[아침결식 데이터 찾음]", item)
                return {"breakfast_skip_rate": item["breakfast_skip_rate"]}
        except ValueError:
            continue  # age, year가 문자열일 경우 무시
    print("[아침결식 데이터 없음]")
    return {"breakfast_skip_rate": None}
