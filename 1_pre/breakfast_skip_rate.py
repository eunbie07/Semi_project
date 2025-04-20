
import pandas as pd
import matplotlib.pyplot as plt
import json

# ✅ 한글 폰트 설정
plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# JSON 데이터 불러오기
with open("breakfast_skip_rate.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# 데이터 변형 (long-form)
df_melted = df.melt(id_vars='성별', var_name='연도', value_name='결식률')

# 그래프 그리기
plt.figure(figsize=(10, 6))
for gender in df_melted['성별'].unique():
    subset = df_melted[df_melted['성별'] == gender]
    plt.plot(subset['연도'], subset['결식률'], marker='o', label=gender)
    
    # 텍스트 표시
    for x, y in zip(subset['연도'], subset['결식률']):
        plt.text(x, y + 0.5, f'{y:.1f}', ha='center', va='bottom', fontsize=9)

plt.title("연도별 청소년 아침식사 결식률 (성별 비교)", fontsize=14)
plt.xlabel("연도")
plt.ylabel("결식률 (%)")
plt.ylim(25, 50)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title="성별")
plt.tight_layout()
plt.savefig("breakfast_skip_rate_chart_with_labels.png")
plt.show()
