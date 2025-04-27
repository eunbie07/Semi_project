import json
import matplotlib.pyplot as plt
import platform

# 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

# JSON 파일 불러오기
with open('smoke_drink.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

years = data['years']
boy_data = data['boy_data']
girl_data = data['girl_data']

colors = {
    '아침식사 결식': 'navy',
    '신체활동 실천': 'deepskyblue',
    '음주율': 'forestgreen',
    '흡연율': 'orange'
}

# 그래프 그리기
fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharey=True)

for label, values in boy_data.items():
    axes[0].plot(years, values, label=label, color=colors[label], linewidth=2.5, marker='o')
axes[0].set_title('남학생 건강형태 변화', fontsize=14)
axes[0].set_xlabel('년도')
axes[0].set_ylabel('(%)')
axes[0].set_yticks(range(0, 51, 5))
axes[0].legend(loc='upper left')
axes[0].grid(True)

for label, values in girl_data.items():
    axes[1].plot(years, values, label=label, color=colors[label], linewidth=2.5, marker='o')
axes[1].set_title('여학생 건강형태 변화', fontsize=14)
axes[1].set_xlabel('년도')
axes[1].set_yticks(range(0, 51, 5))
axes[1].legend(loc='upper left')
axes[1].grid(True)

fig.suptitle('청소년 건강형태 변화', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('smoke_drink.png')
plt.show()
