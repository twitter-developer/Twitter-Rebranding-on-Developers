import matplotlib.pyplot as plt
import pandas as pd

# Load data
df = pd.read_csv('twitter_data_path')

# Print total rows and number of unique users
print(len(df))
print(df['UserID'].nunique())

# Parse datetime field
df['time'] = pd.to_datetime(df['Tweet_Created At'], format='%a %b %d %H:%M:%S %z %Y')
df['time'] = df['time'].dt.tz_localize(None)  # Remove timezone

# Define analysis period and grace period
start_date = pd.Timestamp('2022-01-01')
end_date = pd.Timestamp('2023-12-31')
grace_period = pd.Timedelta(days=120)  # Grace period length: 120 days

# Filter data within the analysis period including grace period
df = df[(df['time'] >= start_date) & (df['time'] <= end_date + grace_period)]
df = df.dropna(subset=['Text'])

# Get last post time for each user
last_post = df.groupby('UserID')['time'].max().reset_index()
last_post.columns = ['UserID', 'last_time']

# Identify users who posted after the grace period
activity_cutoff = end_date + grace_period
has_later_posts = df[df['time'] > activity_cutoff]['UserID'].unique()

# Remove users who are still active after the grace period
last_post = last_post[~last_post['UserID'].isin(has_later_posts)]

# Keep last post times within the analysis period
last_post = last_post[(last_post['last_time'] >= start_date) & (last_post['last_time'] <= end_date)]

# Count total users who stopped posting
num_left = last_post['UserID'].nunique()
print(f"Total users who stopped posting: {num_left}")

# Count users by month
last_post['last_month'] = last_post['last_time'].dt.to_period('M').dt.to_timestamp()
monthly_counts = last_post.groupby('last_month')['UserID'].count().reset_index()
monthly_counts.columns = ['month', 'num_users_stopped']
monthly_counts = monthly_counts.sort_values('month')

# Plot monthly user drop-off
plt.figure(figsize=(10, 5))
plt.plot(monthly_counts['month'], monthly_counts['num_users_stopped'], marker='o', linewidth=3, markersize=8)
plt.xlabel('Month', fontsize=16)
plt.ylabel('Number of developers stopped posting', fontsize=16)
plt.axvline(pd.Timestamp('2022-10-28'), color='#d62728', linestyle='--', linewidth=3, label='2022-10-28')
plt.axvline(pd.Timestamp('2023-07-23'), color='#009E73', linestyle='-.', linewidth=3, label='2023-07-23')
plt.legend(fontsize=14)
plt.xticks(rotation=45, fontsize=14)
plt.yticks(fontsize=14)
plt.tight_layout()
plt.savefig('plot_path', dpi=500)
plt.show()

# Analyze users who stopped posting after a specific date
cutoff_date = pd.Timestamp('2022-10-01')
num_after_oct2022 = last_post[last_post['last_time'] >= cutoff_date]['UserID'].nunique()
print(f"\nNumber of users who stopped posting on or after 2022-10-01: {num_after_oct2022}")
