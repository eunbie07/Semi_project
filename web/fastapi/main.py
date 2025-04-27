from fastapi import FastAPI
import json
import os
from fastapi import Query 

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_dir = os.path.dirname(__file__)
depression_path = os.path.join(base_dir, "json/depression.json")
breakfast_path = os.path.join(base_dir, "json/breakfast_skip.json")
edu_path = os.path.join(base_dir, "json/private_edu.json")
stress_path = os.path.join(base_dir, "json/stress_issues.json")  
stress_region_path = os.path.join(base_dir, "json/stress_region.json")
breakfast_region_path = os.path.join(base_dir, "json/breakfast_region.json")


try:
    with open(depression_path, "r", encoding="utf-8") as f:
        depression = json.load(f)
except Exception as e:
    print("우울감 데이터 로딩 실패:", e)
    depression = []

try:
    with open(breakfast_path, "r", encoding="utf-8") as f:
        breakfast_data = json.load(f)
except Exception as e:
    print("아침결식률 데이터 로딩 실패:", e)
    breakfast_data = []

try:
    with open(edu_path, "r", encoding="utf-8") as f:
        edu_data = json.load(f)
except Exception as e:
    print("사교육 데이터 로딩 실패:", e)
    edu_data = []

try:
    with open(stress_path, "r", encoding="utf-8") as f:
        stress_data = json.load(f)
except Exception as e:
    print("청소년 스트레스 고민 데이터 로딩 실패:", e)
    stress_data = []

try:
    with open(stress_region_path, "r", encoding="utf-8") as f:
        stress_region_data = json.load(f)
except Exception as e:
    print("지역별 스트레스 데이터 로딩 실패:", e)
    stress_region_data = []

try:
    with open(breakfast_region_path, "r", encoding="utf-8") as f:
        breakfast_region_data = json.load(f)
except Exception as e:
    print("지역별 아침식사 결식률 데이터 로딩 실패:", e)
    breakfast_region_data = []



@app.get("/")
def root():
    return {
        "message": "depression"
    }

@app.get("/depression")
def get_depression(age: int, gender: str, year: int):
    print(f"[우울감 요청] age={age}, gender={gender}, year={year}")
    for item in depression:
        if item["age"] == age and item["gender"] == gender and item["year"] == year:
            print("[우울감 데이터 찾음]", item)
            return {"result": True,"depression_rate": item["depression_rate"]}
    print("[우울감 데이터 없음]")
    return {"result": False,"depression_rate": None}

@app.get("/breakfast_skip_rate")
def get_breakfast_skip_rate(age: int, gender: str, year: int):
    print(f"[아침결식 요청] age={age}, gender={gender}, year={year}")
    for item in breakfast_data:
        try:
            if int(item["age"]) == age and item["gender"] == gender and int(item["year"]) == year:
                print("[아침결식 데이터 찾음]", item)
                return {"result": True,"breakfast_skip_rate": item["breakfast_skip_rate"]}
        except ValueError:
            continue
    print("[아침결식 데이터 없음]")
    return {"result": False,"breakfast_skip_rate": None}

# 나이 -> 학제 매핑 함수
def age_to_school_level(age: int) -> str:
    if 8 <= age <= 13:
        return "초등학교 (%)"
    elif 14 <= age <= 16:
        return "중학교 (%)"
    elif 17 <= age <= 19:
        return "고등학교 (%)"
    else:
        return None

@app.get("/private_edu")
def get_private_edu(age: int, year: int):
    print(f"[사교육 요청] age={age}, year={year}")
    level = age_to_school_level(age)
    if level is None:
        return {"result": False}

    for item in edu_data:
        if int(item["year"]) == year and item["school_level"] == level:
            print("[사교육 데이터 찾음]", item)
            return {
                "result": True,
                "school_level": level.replace(" (%)", ""),
                "private_edu_rate": item["private_edu_rate"]
            }

    print("[사교육 데이터 없음]")
    return {"result": False,"private_edu_rate": None}

@app.get("/stress_top_issue")
def get_stress_top_issue(year: int):
    year_data = [item for item in stress_data if int(item["year"]) == year]
    if not year_data:
        return {"result": False}

    top = max(year_data, key=lambda x: x["concern_rate(%)"])
    return {
        "result": True,
        "top_issue": top["issue"],
        "concern_rate(%)": top["concern_rate(%)"]
    }

@app.get("/stress_region")
def get_stress_rate_by_region(region: str, year: int):
    region = region.strip()
    print(f"[스트레스 지역 요청] region={region}, year={year}")

    for item in stress_region_data:
        if item["region"].strip() == region:
            for record in item["data"]:
                if record["year"] == year:
                    print("[데이터 찾음]", region, record)
                    return {
                        "result": True,
                        "region": region,
                        "year": year,
                        "stress_rate": record["stress_rate"]
                    }
    print("[데이터 없음]", region, year)
    return {
        "result": False,
        "message": "해당 지역 또는 연도의 데이터가 없습니다."
    }


@app.get("/stress_issues")
def get_stress_issues(year: float = Query(...)):
    filtered = [
        {"issue": d["issue"], "concern_rate": d["concern_rate(%)"]}
        for d in stress_data if d["year"] == year
    ]
    return filtered

@app.get("/breakfast_region")
def get_breakfast_rate(region: str = Query(...), year: int = Query(...)):
    region = region.strip()
    print(f"[아침식사 결식률 요청] region={region}, year={year}")

    year_key = f"{year}.0"  
    for item in breakfast_region_data:
        if item["지역"].strip() == region:
            if year_key in item:
                return {
                    "result": True,
                    "region": region,
                    "year": year,
                    "breakfast_rate": item[year_key]
                }

    return {
        "result": False,
        "message": "해당 지역 또는 연도의 데이터가 없습니다."
    }
