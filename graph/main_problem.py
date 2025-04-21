import matplotlib.pyplot as plt
import numpy as np

# 한글 폰트 설정 (운영체제별로 자동 대응)
plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 카테고리 및 데이터
categories = [
    "외모", "신체적·정신적 건강", "가정 환경(부모의 불화 등)", "가계경제어려움", "용돈부족",
    "공부(성적, 적성 등)", "직업(직업선택, 보수 등)", "친구(우정)", "연애상대와의 관계(성문제 포함)",
    "학교(원) 폭력", "흡연, 음주, 약물남용", "인터넷 중독(누리소통망(SNS), 게임 등)", "기타", "고민없음"
]
years = ["2016", "2018", "2020", "2022", "2024"]
data = [
    [10.9, 10.7, 10.4, 9.7, 11.9],
    [4.9, 5.2, 8.1, 6.0, 7.1],
    [2.2, 2.4, 1.5, 1.8, 1.3],
    [4.8, 4.0, 3.8, 3.5, 3.1],
    [4.3, 4.5, 4.3, 4.7, 5.0],
    [32.7, 29.5, 29.0, 31.5, 33.0],
    [28.8, 30.2, 27.5, 28.0, 26.2],
    [2.6, 2.7, 2.5, 3.5, 3.7],
    [1.7, 1.8, 1.2, 1.0, 0.9],
    [1.5, 1.1, 0.8, 0.6, 0.5],
    [0.6, 0.5, 0.5, 0.4, 0.3],
    [1.0, 0.9, 0.8, 0.9, 0.9],
    [0.9, 1.1, 0.7, 0.7, 0.8],
    [5.1, 6.7, 8.9, 9.5, 8.4]
]

# 시각화
df = np.array(data)
bar_width = 0.15
x = np.arange(len(categories))
colors = ['#FF6B6B', '#6BCB77', '#FFD93D', '#4D96FF', '#C084FC']

plt.figure(figsize=(18, 8))
for i in range(len(years)):
    plt.bar(x + i * bar_width, df[:, i], width=bar_width, label=years[i], color=colors[i])

plt.xticks(x + bar_width * 2, categories, rotation=45, ha='right', fontsize=10)
plt.ylabel('비율 (%)')
plt.title('청소년 고민 (2016~2024)', fontsize=16, fontweight='bold')
plt.legend(title='연도', loc='upper right')
plt.grid(axis='y', linestyle='--', alpha=0.5)

# 수치 라벨 추가
for i in range(len(years)):
    for j in range(len(categories)):
        plt.text(x[j] + i * bar_width, df[j, i] + 0.3, f'{df[j, i]:.1f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('main_problem.png')
plt.show()
