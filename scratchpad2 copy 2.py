import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
# Load data
final_site_list = pd.read_csv('CPCB_Issues/AirPy_v2/final_site_list_new.csv')
count_summary = pd.read_csv('CPCB_Issues/AirPy_v2/new_data/summary/summary_count.csv')

# Filter sites based on site_id presence in final_site_list
sites = count_summary[count_summary['site_id'].isin(final_site_list['site_id'])]

df = count_summary

# df['outliers_detected']


sns.set_palette("Set2")

# print(df.columns, df.index, df)
print(df.groupby('year').agg('count'))
df = df.groupby(['year', 'prevalent_error']).agg('count').reset_index()
ax = sns.barplot(x='year', y='timestamp', hue='prevalent_error', data=df)

for i in ax.containers:
    ax.bar_label(i,)


# # Show the plot
plt.show()
