from fastapi import FastAPI
import json
import os

app = FastAPI()

# JSON 파일 경로 설정
base_dir = os.path.dirname(__file__)
depression_path = os.path.join(base_dir, "json/depression.json")
breakfast_path = os.path.join(base_dir, "json/breakfast_skip.json")
edu_path = os.path.join(base_dir, "json/private_edu.json")
stress_path = os.path.join(base_dir, "json/teen_stress_issues.json")  # 추가됨

# 데이터 로딩
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

# 기본 경로
@app.get("/")
def root():
    return {
        "message": (
            "✅ 정신건강 우울감 API - /depression?age=17&gender=female&year=2023\n"
            "✅ 아침결식률 API - /breakfast_skip_rate?age=17&gender=female&year=2023\n"
            "✅ 사교육 참여율 API - /private_edu?age=15&year=2022\n"
            "✅ 스트레스 고민 항목 API - /stress_issues?year=2024\n"
            "✅ 고민 항목별 추이 API - /stress_trend?issue=Study"
        )
    }

# 우울감 데이터 API
@app.get("/depression")
def get_depression(age: int, gender: str, year: int):
    print(f"[우울감 요청] age={age}, gender={gender}, year={year}")
    for item in depression:
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
            continue
    print("[아침결식 데이터 없음]")
    return {"breakfast_skip_rate": None}

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

# 사교육 참여율 데이터 API
@app.get("/private_edu")
def get_private_edu(age: int, year: int):
    print(f"[사교육 요청] age={age}, year={year}")
    level = age_to_school_level(age)
    if level is None:
        return {"error": "지원하지 않는 나이입니다. (8~19세만 조회 가능)"}

    for item in edu_data:
        if int(item["year"]) == year and item["school_level"] == level:
            print("[사교육 데이터 찾음]", item)
            return {
                "school_level": level.replace(" (%)", ""),
                "private_edu_rate": item["participation_rate"]
            }

    print("[사교육 데이터 없음]")
    return {"private_edu_rate": None}

# 스트레스 고민 항목 - 연도별 전체 보기
@app.get("/stress_issues")
def get_stress_issues(year: int):
    result = [item for item in stress_data if int(item["year"]) == year]
    if not result:
        return {"message": f"No data available for year {year}"}
    return {"year": year, "issues": result}

# 스트레스 고민 항목 - 특정 항목 추이 보기
@app.get("/stress_trend")
def get_stress_trend(issue: str):
    trend = [
        {"year": int(item["year"]), "rate": item["concern_rate(%)"]}
        for item in stress_data if item["issue"].lower() == issue.lower()
    ]
    if not trend:
        return {"message": f"No trend data found for issue: '{issue}'"}
    return {
        "issue": issue,
        "trend": sorted(trend, key=lambda x: x["year"])
    }
