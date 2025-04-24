import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import warnings

# ✅ 경고 숨기기
warnings.filterwarnings("ignore", category=UserWarning)

# ✅ 한글 폰트 설정
plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# ✅ 데이터 불러오기
smartphone_df = pd.read_json("smartphone_time.json")
depression_df = pd.read_json("depression.json")

# ✅ 시간대 → 중간값 매핑
time_midpoints = {
    "2시간 미만": 1,
    "2~4시간": 3,
    "4~6시간": 5,
    "6~8시간": 7,
    "8시간 이상": 9
}

# ✅ 14~19세, 전체 성별 필터
smartphone_filtered = smartphone_df[
    (smartphone_df['gender'] == '전체') &
    (smartphone_df['age'].between(14, 19))
].copy()
smartphone_filtered['time_mid'] = smartphone_filtered['time'].map(time_midpoints)

# ✅ 평균 스마트폰 사용시간 계산
grouped = smartphone_filtered.groupby(['year', 'age'])
expected_usage = (
    grouped['value'].apply(lambda v: (v * smartphone_filtered.loc[v.index, 'time_mid']).sum()) / 
    grouped['value'].sum()
).reset_index(name='expected_usage')

# ✅ 우울감 경험률 필터
depression_filtered = depression_df[
    (depression_df['gender'] == '전체') &
    (depression_df['age'].between(14, 19))
]

# ✅ 데이터 병합
merged_df = pd.merge(expected_usage, depression_filtered, on=['year', 'age'])

# # ✅ 사용자 지정 연한 파스텔톤 색상
# custom_palette = [
#     "#cdb4db",  # 연보라
#     "#ffc8dd",  # 연분홍
#     "#bde0fe",  # 연하늘
#     "#d3d3d3",  # 연회색
#     "#e2f0cb",  # 연연두
#     "#f1c0e8",  # 연보라핑크
#     "#a2d2ff",  # 맑은 하늘
# ]

# ✅ 시각화
plt.figure(figsize=(12, 7))  # 통일된 크기
sns.set(style="white")  # 그리드 없는 깔끔한 스타일

# 📌 산점도
sns.scatterplot(
    data=merged_df,
    x='expected_usage',
    y='depression_rate',
    hue='year',
    style='age',
    # palette=custom_palette,
    s=100
)

# 📌 회귀선 (전체 경향선)
sns.regplot(
    data=merged_df,
    x='expected_usage',
    y='depression_rate',
    scatter=False,
    color='black',
    line_kws={'linewidth': 2, 'linestyle': '--'}
)

# 📌 제목과 축 라벨
plt.title("Smartphone usage time vs Depression rate", fontsize=16, fontweight='bold')  # 통일된 제목 스타일
plt.xlabel("Smartphone usage time (hours)")
plt.ylabel("Depression rate (%)")
plt.legend(title='Year and Age', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
plt.ylim(20, 35)

# 📌 테두리: 아래/왼쪽만, 얇고 흐리게
ax = plt.gca()
for spine_name in ['top', 'right']:
    ax.spines[spine_name].set_visible(False)
for spine_name in ['left', 'bottom']:
    ax.spines[spine_name].set_linewidth(0.6)         # 얇게
    ax.spines[spine_name].set_color('#AAAAAA')       # 흐리게

plt.grid(False)
plt.tight_layout()
plt.savefig("scatter_smartphone.png", dpi=300)
plt.show()
