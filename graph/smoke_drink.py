import matplotlib.pyplot as plt
import platform

if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='NanumGothic')

plt.rcParams['axes.unicode_minus'] = False


years = list(range(2010, 2025))

boy_data = {
    '아침식사 결식': [26.4, 27.1, 28.0, 29.2, 30.5, 32.1, 33.4, 34.9, 35.5, 37.1, 38.0, 39.1, 39.8, 40.0, 40.2],
    '신체활동 실천': [20.0, 19.5, 19.8, 20.1, 20.2, 21.0, 22.1, 23.0, 23.3, 23.9, 24.0, 24.7, 25.0, 25.0, 25.1],
    '음주율': [28.0, 27.2, 26.8, 25.9, 24.8, 23.5, 21.9, 20.1, 18.7, 17.3, 16.0, 14.5, 13.2, 12.1, 11.8],
    '흡연율': [14.3, 13.8, 13.2, 12.4, 11.3, 10.1, 9.2, 8.0, 7.1, 6.2, 5.7, 5.3, 4.9, 4.8, 4.8]
}

girl_data = {
    '아침식사 결식': [28.0, 28.3, 28.7, 29.5, 30.1, 31.2, 32.4, 34.0, 35.8, 37.2, 38.1, 39.3, 41.0, 43.1, 44.7],
    '신체활동 실천': [8.9, 8.2, 7.5, 6.9, 6.5, 6.2, 6.5, 6.8, 7.0, 7.2, 7.4, 7.7, 8.0, 8.4, 8.59],
    '음주율': [25.9, 25.2, 24.0, 22.8, 21.6, 20.3, 19.2, 18.0, 16.9, 16.0, 15.0, 14.2, 13.6, 13.0, 12.5],
    '흡연율': [8.9, 8.3, 7.5, 6.5, 5.9, 5.3, 4.6, 4.0, 3.5, 3.1, 2.9, 2.8, 2.6, 2.5, 2.4]
}

colors = {
    '아침식사 결식': 'navy',
    '신체활동 실천': 'deepskyblue',
    '음주율': 'forestgreen',
    '흡연율': 'orange'
}


fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharey=True)


for label, data in boy_data.items():
    axes[0].plot(years, data, label=label, color=colors[label], linewidth=2.5, marker='o')
axes[0].set_title('남학생 건강형태 변화', fontsize=14)
axes[0].set_xlabel('년도')
axes[0].set_ylabel('(%)')
axes[0].set_yticks(range(0, 51, 5))
axes[0].legend(loc='upper left')  
axes[0].grid(True)

for label, data in girl_data.items():
    axes[1].plot(years, data, label=label, color=colors[label], linewidth=2.5, marker='o')
axes[1].set_title('여학생 건강형태 변화', fontsize=14)
axes[1].set_xlabel('년도')
axes[1].set_yticks(range(0, 51, 5))
axes[1].legend(loc='upper left')  
axes[1].grid(True)

fig.suptitle('청소년 건강형태 변화', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('smoke_drink.png')
plt.show()
