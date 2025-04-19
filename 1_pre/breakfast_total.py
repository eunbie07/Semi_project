import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 연도 및 우울감 경험률 데이터만 사용
years = list(range(2015, 2025))
depression = [27.9, 28.2, 31.5, 33.6, 35.7, 37.3, 38.0, 38.8, 41.1, 42.4]

# 그래프 그리기
plt.figure(figsize=(12, 6))
plt.plot(years, depression, marker='o', color='deepskyblue', label='아침식사 결식률')

# 값 표시
for i in range(len(years)):
    plt.text(years[i], depression[i] + 0.3, f'{depression[i]}', color='deepskyblue', ha='center')

# 제목과 축 라벨
plt.title('아침식사 결식률 (2015-2024)', fontsize=14)
plt.xlabel('연도')
plt.ylabel('비율 (%)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('breakfast_total.png')
plt.show()

