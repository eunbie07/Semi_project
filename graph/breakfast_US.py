import matplotlib.pyplot as plt
import numpy as np
import json

# 한글 폰트 설정
plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# JSON 파일 불러오기
with open('breakfast_US.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

categories = data['categories']
daily = data['daily']
skip = data['skip']

bar_width = 0.35
x = np.arange(len(categories))

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
