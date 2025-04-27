import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

years = list(range(2015, 2025))
boys = [26.9, 27.3, 30.1, 32.2, 34.6, 35.5, 37.0, 37.4, 39.7, 40.2]
girls = [28.9, 29.3, 33.0, 35.1, 36.9, 39.2, 39.1, 40.7, 42.6, 44.7]

plt.figure(figsize=(10, 6))
plt.plot(years, boys, marker='s', linestyle='-', color='dodgerblue', label='남학생')
plt.plot(years, girls, marker='o', linestyle='-', color='crimson', label='여학생')

for i in range(len(years)):
    plt.text(years[i], boys[i] + 0.3, str(boys[i]), ha='center', fontsize=9, color='blue')
    plt.text(years[i], girls[i] + 0.3, str(girls[i]), ha='center', fontsize=9, color='darkred')

plt.title('청소년 아침식사 결식률 (2015-2024)', fontsize=14)
plt.xlabel('연도')
plt.ylabel('비율 (%)')
plt.ylim(25, 50)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig('breakfast_gender.png')
plt.show()

