import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
depression_rates = [23.6, 25.5, 25.1, 27.1, 28.2, 25.2, 26.8, 28.7, 26.0, 27.7]

line_color = '#A8E6CF'       
shadow_color = '#D0F2E1'     
bg_color = '#FFFFFF'         

plt.figure(figsize=(9, 6), facecolor=bg_color)
ax = plt.gca()
ax.set_facecolor(bg_color)

plt.plot(years, depression_rates, color=shadow_color, linewidth=6)

plt.plot(years, depression_rates, color=line_color, marker='o', linewidth=2, label='우울감 경험률',
         markerfacecolor='white', markeredgewidth=2, markeredgecolor=line_color)

plt.fill_between(years, depression_rates, color=line_color, alpha=0.3)

plt.title(' 우울감 경험률 변화 (단위: %)', fontsize=16, pad=20)
plt.xlabel('년도', fontsize=12)
plt.ylabel('비율 (%)', fontsize=12)

plt.ylim(0, 50)
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend(frameon=False, fontsize=11)

for x, y in zip(years, depression_rates):
    plt.text(x, y + 0.8, f'{y}', ha='center', fontsize=10, color=line_color)

plt.tight_layout()
plt.savefig('graph/depression_solid.png', dpi=300)
plt.show()
