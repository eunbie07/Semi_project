import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  

years = list(range(2015, 2025))

depression = [23.6, 25.5, 25.1, 27.1, 28.2, 25.2, 26.8, 28.7, 26.0, 27.7]

plt.figure(figsize=(6, 6))

plt.plot(years, depression, label='우울감 경험률', color='deepskyblue', marker='o', linewidth=2.5)



for x, y in zip(years, depression):
    plt.text(x, y + 0.8, f'{y}', color='deepskyblue', ha='center', fontsize=9)

plt.title('우울감 경험률 (단위: %)', fontsize=15, fontweight='bold')
plt.xlabel('년도')
plt.ylabel('비율 (%)')
plt.ylim(0, 50) 
plt.xticks(np.arange(2015, 2025, 1))
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('depression.png')
plt.show()

