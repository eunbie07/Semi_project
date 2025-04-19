import matplotlib.pyplot as plt
import numpy as np

# 한글 폰트 설정 (운영체제 자동 대응)
plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 데이터
categories = ["슬픔·절망감", "자살생각", "자살계획", "자살시도"]
daily = [21.0, 10.0, 7.0, 2.0]   # 매일 아침식사 및
skip = [45.0, 22.0, 17.0, 9.0]   # 아침 미섭취

bar_width = 0.35
x = np.arange(len(categories))

# 시각화
plt.figure(figsize=(10, 6))
plt.bar(x, daily, width=bar_width, label='매일 아침식사 및', color='#FFC107')
plt.bar(x + bar_width, skip, width=bar_width, label='아침 미섭취', color='#FF5722')

plt.xticks(x + bar_width / 2, categories)
plt.ylabel('유병률 (%)')
plt.title('아침식사 여부에 따른 청소년 정신건강 지표 (YRBS 2023)', fontsize=14, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.legend()

# 수치 라벨 추가
for i in range(len(categories)):
    plt.text(x[i], daily[i] + 1, f'{daily[i]:.1f}%', ha='center', fontsize=10)
    plt.text(x[i] + bar_width, skip[i] + 1, f'{skip[i]:.1f}%', ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('breakfast_US.png')
plt.show()

