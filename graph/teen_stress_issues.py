
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json


plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# JSON 파일 불러오기
with open("teen_stress_issues.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

df['시점'] = df['시점'].fillna(method='ffill')
bar_df = df.pivot_table(index='항목', columns='시점', values='고민비율(%)')

custom_order = [
    '외모', '신체적·정신적 건강', '가정 환경(부모의 불화등)', '가계경제어려움', '용돈부족',
    '공부(성적, 적성 등)', '직업(직업선택, 보수 등)', '친구(우정)', '연애 상대와의 관계(성문제 포함)',
    '학교(원) 폭력', '흡연, 음주, 약물남용', '인터넷 중독[누리소통망(SNS), 게임 등]', '기타', '고민없음'
]
ordered_bar_df = bar_df.reindex(custom_order)

plt.figure(figsize=(12, 6))
bar_width = 0.13
x = np.arange(len(ordered_bar_df.index))
colors = ['#f87171', '#4ade80', '#facc15', '#c084fc', '#60a5fa'] 

for i, (year, color) in enumerate(zip(ordered_bar_df.columns, colors)):
    bar_positions = x + bar_width * i
    values = ordered_bar_df[year]
    bars = plt.bar(bar_positions, values, width=bar_width, label=int(year), color=color)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f'{height:.1f}', ha='center', va='bottom', fontsize=7)

plt.xticks(x + bar_width * (len(ordered_bar_df.columns) - 1) / 2, ordered_bar_df.index, rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
plt.ylabel("비율 (%)", fontsize=12)
plt.ylim(0, 50)
plt.title("청소년 고민 (2016~2024)", fontsize=14, weight='bold')
plt.legend(title="연도", fontsize=10, title_fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.5)

for spine in plt.gca().spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1.0)

plt.tight_layout()
plt.savefig('teen_stress_issues.png')
plt.show()
