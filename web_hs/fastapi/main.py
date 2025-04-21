from fastapi import FastAPI
import json
import os

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "hello"
    }

# JSON 파일 경로 설정
base_dir = os.path.dirname(__file__)
smartphone_badeffect_path = os.path.join(base_dir, "json/smartphone_badeffect.json")
personality_dailyexperience_path = os.path.join(base_dir, "json/personality_dailyexperience.json")

# 데이터 로딩
try:
    with open(smartphone_badeffect_path, "r", encoding="utf-8") as f:
        smartphone_badeffect = json.load(f)
except Exception as e:
    print("과의존 척도 데이터 로딩 실패:", e)
    smartphone_badeffect = []

try:
    with open(personality_dailyexperience_path, "r", encoding="utf-8") as f:
        personality_dailyexperience = json.load(f)
except Exception as e:
    print("성격_일상경험 데이터 로딩 실패:", e)
    personality_dailyexperience = []


# 나이 → 학령군 변환
def age_to_school_level(age: int) -> str:
    if 8 <= age <= 13:
        return "초등학생"
    elif 14 <= age <= 16:
        return "중학생"
    elif 17 <= age <= 19:
        return "고등학생"
    else:
        return None

@app.get("/smartphone_badeffect")
def get_smartphone_badeffect(age: int, year: int):
    print(f"[인터넷 과의존 척도] age={age}, year={year}")
    group = age_to_school_level(age)
    if not group:
        return {"resultCode": False, "message": "지원하지 않는 나이입니다"}

    for item in smartphone_badeffect:
        if item["year"] == year and item["group"] == group:
            responses = item["responses"]

            # 문항 키워드
            q_fail = "스마트폰 이용시간을 줄이려 할 때마다 실패한다"
            q_family = "스마트폰 이용 때문에 가족과 심하게 다툰 적이 있다"
            q_friends = "스마트폰 이용 때문에 친구 혹은 동료 사회적 관계에서 심한 갈등을 경험한 적이 있다"

            # 긍정 응답 비율 계산 함수
            def calc_positive(question):
                if question in responses:
                    v = responses[question]
                    return round(v.get("그렇다 (%)", 0) + v.get("매우 그렇다 (%)", 0), 2)
                return None

            return {
                "resultCode": True,
                "year": year,
                "group": group,
                "fail_rate": calc_positive(q_fail),
                "family_rate": calc_positive(q_family),
                "friends_rate": calc_positive(q_friends)
            }

    return {"resultCode": False, "message": "해당 연도 또는 그룹의 데이터가 없습니다"}


@app.get("/personality_dailyexperience")
def get_personality_dailyexperience(age: int, year: int):
    print(f"[성격_일상경험] age={age}, year={year}")
    group = age_to_school_level(age)
    if not group:
        return {"resultCode": False, "message": "지원하지 않는 나이입니다"}

    for item in personality_dailyexperience:
        if item["year"] == year and item["group"] == group:
            responses = item["responses"]

            # 문항 키워드
            q_cheat = "평소 필요하다면 다른 사람을 속이는 것도 가능하다고 생각한다"
            q_satisfaction = "나는 전반적으로 현재의 생활에 만족한다"
            q_stress = "나는 일(직업 혹은 학업 일상적인 일 등) 스트레스를 많이 받는 편이다"

            # 긍정 응답 비율 계산 함수
            def calc_positive(question):
                if question in responses:
                    v = responses[question]
                    return round(v.get("그렇다 (%)", 0) + v.get("매우 그렇다 (%)", 0), 2)
                return None

            return {
                "resultCode": True,
                "year": year,
                "group": group,
                "cheat_rate": calc_positive(q_cheat),
                "satisfaction_rate": calc_positive(q_satisfaction),
                "stress_rate": calc_positive(q_stress)
            }

    return {"resultCode": False, "message": "해당 연도 또는 그룹의 데이터가 없습니다"}
