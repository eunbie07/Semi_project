import pandas as pd
import matplotlib.pyplot as plt
import json

# ✅ 한글 폰트 설정
plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# ✅ JSON 데이터 로드
with open("depression_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# ✅ 성별 이름을 한글로 변환
gender_map = {
    "male": "남자",
    "female": "여자",  # ← 오타 수정!
    "전체": "전체"
}
df["성별"] = df["gender"].map(gender_map)

# ✅ year를 정수형으로 변환 (혹시 문자열이면)
df["year"] = df["year"].astype(int)

# ✅ 성별별 연도별 평균 우울감 경험률 계산
plt.figure(figsize=(12, 6))
for gender in ["남자", "여자", "전체"]:
    sub = df[df["성별"] == gender]
    avg_by_year = sub.groupby("year")["depression_rate"].mean().reset_index()

    plt.plot(avg_by_year["year"], avg_by_year["depression_rate"], marker="o", label=gender)
    
    # ▶ 숫자 표시
    for x, y in zip(avg_by_year["year"], avg_by_year["depression_rate"]):
        plt.text(x, y + 0.4, f"{y:.1f}", ha="center", fontsize=8)

# ✅ 연도 눈금 표시 (모든 연도 보이게 설정)
plt.xticks(df["year"].unique())

plt.title("연도별 청소년 우울감 경험률 평균 (성별)", fontsize=14)
plt.xlabel("연도")
plt.ylabel("우울감 경험률 (%)")
plt.ylim(15, 40)
plt.legend(title="성별")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("depression_data.png")
plt.show()
