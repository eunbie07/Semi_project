import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

with open("breakfast_skip.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

print(df["age"].unique())
print(df["gender"].unique())

df_gender_plot = df[df["age"].isna() | (df["age"] == "전체")].copy()


df_gender_plot["gender"] = df_gender_plot["gender"].astype(str)
df_gender_plot["year"] = df_gender_plot["year"].astype(int)
df_gender_plot["breakfast_skip_rate"] = df_gender_plot["breakfast_skip_rate"].astype(float)

palette = {"남자": "#1f77b4", "여자": "#ff7f0e", "전체": "#2ca02c"}
plt.figure(figsize=(12, 6))
for gender in ["남자", "여자", "전체"]:
    subset = df_gender_plot[df_gender_plot["gender"] == gender]
    if subset.empty:
        print(f"[경고] '{gender}' 데이터 없음!")
        continue
    plt.plot(subset["year"], subset["breakfast_skip_rate"], marker='o', label=gender, color=palette[gender])
    for x, y in zip(subset["year"], subset["breakfast_skip_rate"]):
        plt.text(x, y + 0.3, f"{y:.1f}", ha='center', va='bottom', fontsize=9)

plt.title("연도별 청소년 아침식사 결식률 평균 (성별)", fontsize=14)
plt.xlabel("연도", fontsize=12)
plt.ylabel("아침식사 결식률 (%)", fontsize=12)
plt.xticks(df_gender_plot["year"].unique())
plt.ylim(25, 46)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title="성별", fontsize=10)
plt.tight_layout()
plt.savefig("breakfast_skip.png")
plt.show()
