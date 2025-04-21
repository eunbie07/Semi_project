import pandas as pd
import matplotlib.pyplot as plt
import json

# 한글 폰트 설정
plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# JSON 파일 불러오기
with open("private_edu.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# school_level에서 "(%)" 제거
df["school_level"] = df["school_level"].str.replace(" (%)", "", regex=False)

# 피벗: 연도별 학교급별 참여율
pivot_df = df.pivot(index="year", columns="school_level", values="participation_rate")

# 시각화
plt.figure(figsize=(10, 6))
for col in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[col], marker='o', label=col)
    for x, y in zip(pivot_df.index, pivot_df[col]):
        plt.text(x, y + 0.5, f"{y:.1f}", ha='center', fontsize=8)

plt.title("연도별 학교급별 사교육 참여율 변화", fontsize=14)
plt.xlabel("연도")
plt.ylabel("사교육 참여율 (%)")
plt.xticks(pivot_df.index)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title="학교급")
plt.tight_layout()
plt.savefig("private_edu.png")
plt.show()
