import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 파일 경로
depression_path = "depression.json"
breakfast_path = "breakfast_skip.json"

# JSON 파일 불러오기
with open(depression_path, "r", encoding="utf-8") as f:
    depression_data = json.load(f)

with open(breakfast_path, "r", encoding="utf-8") as f:
    breakfast_data = json.load(f)

# DataFrame 변환
df_depression = pd.DataFrame(depression_data)
df_breakfast = pd.DataFrame(breakfast_data)

# '전체' 성별만 필터링
df_depression = df_depression[df_depression["gender"] == "전체"]
df_breakfast = df_breakfast[df_breakfast["gender"] == "전체"]

# age 타입 통일
df_depression["age"] = pd.to_numeric(df_depression["age"], errors="coerce")
df_breakfast["age"] = pd.to_numeric(df_breakfast["age"], errors="coerce")

# 병합
merged_df = pd.merge(df_depression, df_breakfast, on=["year", "age"], how="inner")

# 컬럼명 정리
merged_df.rename(columns={
    "depression_rate": "Depression Rate (%)",
    "breakfast_skip_rate": "Breakfast Skip Rate (%)"
}, inplace=True)

# 숫자형 변환
merged_df["Breakfast Skip Rate (%)"] = pd.to_numeric(merged_df["Breakfast Skip Rate (%)"], errors='coerce')

# 🎯 연도 필터링
merged_df = merged_df[(merged_df["year"] >= 2020) & (merged_df["year"] <= 2024)]

# 시각화
plt.figure(figsize=(12, 7))  # 통일된 크기
sns.set(style="white")

# 산점도
sns.scatterplot(
    data=merged_df,
    x="Breakfast Skip Rate (%)",
    y="Depression Rate (%)",
    hue="year",
    style="age",
    palette="Set2",
    s=100
)

# 회귀선
sns.regplot(
    data=merged_df,
    x="Breakfast Skip Rate (%)",
    y="Depression Rate (%)",
    scatter=False,
    ci=95,
    color='black',
    line_kws={"linestyle": "dashed"}
)

# 제목 및 범례
plt.title("Breakfast skip rate vs Depression rate", fontsize=16, fontweight='bold')  # 통일된 제목 스타일
plt.legend(title="Year and Age", bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
plt.ylim(20, 35)

# ✅ 테두리: 아래/왼쪽만, 얇고 흐리게
ax = plt.gca()
for spine_name in ['top', 'right']:
    ax.spines[spine_name].set_visible(False)
for spine_name in ['left', 'bottom']:
    ax.spines[spine_name].set_linewidth(0.6)
    ax.spines[spine_name].set_color('#AAAAAA')

plt.grid(False)
plt.tight_layout()
plt.savefig("scatter_breakfast.png", dpi=300)
plt.show()
