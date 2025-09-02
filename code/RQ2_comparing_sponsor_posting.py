import pandas as pd
import matplotlib.pyplot as plt

# ========== Load data ==========
df_main = pd.read_csv('our_work_dataset')
df_all = pd.read_csv('previous_work_dataset')

# ========== Process datetime ==========
df_main['time'] = pd.to_datetime(df_main['Tweet_Created At'], format='%a %b %d %H:%M:%S %z %Y', errors='coerce')
df_main['year_month'] = df_main['time'].dt.to_period('M')

df_all['time'] = pd.to_datetime(df_all['Time'], errors='coerce')
df_all['year_month'] = df_all['time'].dt.to_period('M')

# ========== Count tweets per month ==========
main_counts = df_main['year_month'].value_counts().sort_index()
all_counts = df_all['year_month'].value_counts().sort_index()

# ========== Combine counts and remove rows with all zeros ==========
monthly_df = pd.DataFrame({
    'Our Dataset': main_counts,
    'Refer Previous Work': all_counts
}).dropna(how='all')  # Remove rows where both are NaN

monthly_df = monthly_df[(monthly_df['Our Dataset'] > 0) | (monthly_df['Refer Previous Work'] > 0)]
monthly_df.index = monthly_df.index.to_timestamp()
monthly_df = monthly_df[monthly_df.index >= pd.Timestamp('2019-06')]

# ========== Plot ==========
plt.figure(figsize=(12, 6))

# Plot lines with markers and thicker width
plt.plot(monthly_df.index, monthly_df['Our Dataset'], marker='o', linewidth=3, label='Our Dataset')
plt.plot(monthly_df.index, monthly_df['Refer Previous Work'], marker='x', linewidth=3, label='Refer Previous Work')

# Add vertical lines to highlight specific dates
plt.axvline(pd.Timestamp('2022-10-28'), color='#d62728', linestyle='--', linewidth=3, label='2022-10-28')
plt.axvline(pd.Timestamp('2023-07-23'), color='#009E73', linestyle='-.', linewidth=3, label='2023-07-23')

plt.xlabel('Month', fontsize=16)
plt.ylabel('Number of Tweets', fontsize=16)
plt.legend(fontsize=14)

# Set x-axis ticks and labels, rotate labels for readability
plt.xticks(
    ticks=monthly_df.index[::3],
    labels=[d.strftime('%Y-%m') for d in monthly_df.index[::3]],
    rotation=45,
    fontsize=14
)

# Set y-axis tick font size
plt.yticks(fontsize=14)

plt.tight_layout()
plt.savefig('plot_path', dpi=500)
plt.show()
