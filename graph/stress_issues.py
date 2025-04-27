import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# matplotlib 한글 폰트 설정
plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# JSON 데이터 (복사해온 것을 문자열로 변환)
with open('stress_issues.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# DataFrame로 변환
df = pd.DataFrame(data)


# 카테고리 한글 변환 매핑
en_to_ko = {
    "Appearance": "외모",
    "Physical and Mental Health": "신체적·정신적 건강",
    "Family": "가정 환경(부모의 불화 등)",
    "Finance": "가계경제어려움",
    "Allowance": "용돈부족",
    "Study": "공부(성적, 적성 등)",
    "Career": "직업(직업선택, 보수 등)",
    "Friends": "친구(우정)",
    "Romantic Relationships": "연애상대와의 관계(성문제 포함)",
    "School Violence": "학교(원) 폭력",
    "Smoking_Drinking_Substance Abuse": "흡연, 음주, 약물남용",
    "SNS_Games": "인터넷 중독(누리소통망(SNS), 게임 등)",
    "Others": "기타",
    "No Concerns": "고민없음"
}

# 연도별, 카테고리별 데이터 정리
years = sorted(list(set(item['year'] for item in data)))
categories = [en_to_ko[key] for key in en_to_ko]

# (카테고리, 연도)별 concern_rate를 채워넣기
data_matrix = []
for category_en, category_ko in en_to_ko.items():
    row = []
    for year in years:
        match = next((item for item in data if item['year'] == year and item['issue'] == category_en), None)
        if match:
            row.append(match['concern_rate(%)'])
        else:
            row.append(0)
    data_matrix.append(row)

data_matrix = np.array(data_matrix)

# 시각화
bar_width = 0.15
x = np.arange(len(categories))
colors = ['#FF6B6B', '#6BCB77', '#FFD93D', '#4D96FF', '#C084FC']

plt.figure(figsize=(18, 8))
for i in range(len(years)):
    plt.bar(x + i * bar_width, data_matrix[:, i], width=bar_width, label=str(years[i]), color=colors[i % len(colors)])

plt.xticks(x + bar_width * 2, categories, rotation=45, ha='right', fontsize=10)
plt.ylabel('비율 (%)')
plt.title('청소년 고민 (2016~2024)', fontsize=16, fontweight='bold')
plt.legend(title='연도', loc='upper right')
plt.grid(axis='y', linestyle='--', alpha=0.5)

# 수치 라벨 추가
for i in range(len(years)):
    for j in range(len(categories)):
        plt.text(x[j] + i * bar_width, data_matrix[j, i] + 0.3, f'{data_matrix[j, i]:.1f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('stress_issues.png')
plt.show()
