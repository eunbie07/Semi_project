import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


depression_path = "depression.json"
breakfast_path = "breakfast_skip.json"


with open(depression_path, "r", encoding="utf-8") as f:
    depression_data = json.load(f)

with open(breakfast_path, "r", encoding="utf-8") as f:
    breakfast_data = json.load(f)


df_depression = pd.DataFrame(depression_data)
df_breakfast = pd.DataFrame(breakfast_data)

df_depression = df_depression[df_depression["gender"] == "전체"]
df_breakfast = df_breakfast[df_breakfast["gender"] == "전체"]

df_depression["age"] = pd.to_numeric(df_depression["age"], errors="coerce")
df_breakfast["age"] = pd.to_numeric(df_breakfast["age"], errors="coerce")

merged_df = pd.merge(df_depression, df_breakfast, on=["year", "age"], how="inner")

merged_df.rename(columns={
    "depression_rate": "Depression Rate (%)",
    "breakfast_skip_rate": "Breakfast Skip Rate (%)"
}, inplace=True)

merged_df["Breakfast Skip Rate (%)"] = pd.to_numeric(merged_df["Breakfast Skip Rate (%)"], errors='coerce')

merged_df = merged_df[(merged_df["year"] >= 2020) & (merged_df["year"] <= 2024)]

plt.figure(figsize=(12, 7))  
sns.set(style="white")

sns.scatterplot(
    data=merged_df,
    x="Breakfast Skip Rate (%)",
    y="Depression Rate (%)",
    hue="year",
    style="age",
    palette="Set2",
    s=100
)

# 회귀선
sns.regplot(
    data=merged_df,
    x="Breakfast Skip Rate (%)",
    y="Depression Rate (%)",
    scatter=False,
    ci=95,
    color='black',
    line_kws={"linestyle": "dashed"}
)

plt.title("Breakfast skip rate vs Depression rate", fontsize=16, fontweight='bold')  # 통일된 제목 스타일
plt.legend(title="Year and Age", bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
plt.ylim(20, 35)

ax = plt.gca()
for spine_name in ['top', 'right']:
    ax.spines[spine_name].set_visible(False)
for spine_name in ['left', 'bottom']:
    ax.spines[spine_name].set_linewidth(0.6)
    ax.spines[spine_name].set_color('#AAAAAA')

plt.grid(False)
plt.tight_layout()
plt.savefig("scatter_breakfast.png", dpi=300)
plt.show()
