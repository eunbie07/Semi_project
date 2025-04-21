import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# ✅ 한글 폰트 설정
# 윈도우용: 'Malgun Gothic', macOS용: 'AppleGothic', 리눅스용: 'NanumGothic'
plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# 데이터
years = list(range(2015, 2025))
# stress = [35.4, 37.4, 37.4, 37.2, 40.4, 39.9, 34.2, 38.8, 41.3, 37.3]
# breakfast_skip = [27.9, 28.2, 31.5, 33.6, 35.7, 37.3, 38.0, 39.0, 41.1, 42.4]
depression = [23.6, 25.5, 25.1, 27.1, 28.2, 25.2, 26.8, 28.7, 26.0, 27.7]

# 그래프 그리기
plt.figure(figsize=(6, 6))
# plt.plot(years, stress, label='스트레스 인지율', color='red', marker='o', linewidth=2.5)
# plt.plot(years, breakfast_skip, label='아침식사 결식률', color='orange', marker='o', linewidth=2.5)
plt.plot(years, depression, label='우울감 경험률', color='deepskyblue', marker='o', linewidth=2.5)

# 수치 표시
# for x, y in zip(years, stress):
#     plt.text(x, y + 0.8, f'{y}', color='red', ha='center', fontsize=9)
# for x, y in zip(years, breakfast_skip):
#     plt.text(x, y - 2, f'{y}', color='darkorange', ha='center', fontsize=9)
for x, y in zip(years, depression):
    plt.text(x, y + 0.8, f'{y}', color='deepskyblue', ha='center', fontsize=9)

# 스타일 설정
plt.title('우울감 경험률 (단위: %)', fontsize=15, fontweight='bold')
plt.xlabel('년도')
plt.ylabel('비율 (%)')
plt.ylim(0, 50) 
plt.xticks(np.arange(2015, 2025, 1))
plt.grid(axis='y', linestyle='--', alpha=0.5)
# plt.legend()
plt.tight_layout()
plt.savefig('depression.png')
plt.show()

