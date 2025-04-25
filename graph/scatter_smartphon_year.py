import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

smartphone_df = pd.read_json("smartphone_time.json")
depression_df = pd.read_json("depression.json")

time_midpoints = {
    "2시간 미만": 1,
    "2~4시간": 3,
    "4~6시간": 5,
    "6~8시간": 7,
    "8시간 이상": 9,
    "Less than 2 hours": 1,
    "2~4 hours": 3,
    "4~6 hours": 5,
    "6~8 hours": 7,
    "More than 8 hours": 9
}

smartphone_filtered = smartphone_df[
    (smartphone_df['gender'] == '전체') & 
    (smartphone_df['age'].between(14, 19))
].copy()
smartphone_filtered['time_mid'] = smartphone_filtered['time'].map(time_midpoints)

grouped = smartphone_filtered.groupby(['year', 'age'])
expected_usage = (
    grouped['value'].apply(lambda v: (v * smartphone_filtered.loc[v.index, 'time_mid']).sum()) /
    grouped['value'].sum()
).reset_index(name='expected_usage')

depression_filtered = depression_df[
    (depression_df['gender'] == '전체') &
    (depression_df['age'].between(14, 19))
]

merged_df = pd.merge(expected_usage, depression_filtered, on=['year', 'age'])

sns.set(style="whitegrid")
g = sns.lmplot(
    data=merged_df,
    x='expected_usage',
    y='depression_rate',
    hue='year',
    col='year',
    height=4,
    aspect=1,
    scatter_kws={'s': 60, 'alpha': 0.7},
    line_kws={'linewidth': 2}
)

g.set_axis_labels("Smartphone usage time (hours)", "Depression rate (%)", fontsize=9)
g.set_titles("Year: {col_name}")
plt.suptitle("Relationship between Smartphone Usage Time and Depression Rate", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.subplots_adjust(top=0.88)
plt.savefig("scatter_5.png", dpi=300)
plt.show()
