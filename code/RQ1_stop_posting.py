import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress

# ========== Load data ==========
df = pd.read_csv('twitter_data_path')
print("Total number of tweets:", len(df))
print("Total number of users:", df['UserID'].nunique())

# Parse time field
df['time'] = pd.to_datetime(df['Tweet_Created At'], format='%a %b %d %H:%M:%S %z %Y')
df['time'] = df['time'].dt.tz_localize(None)  # remove timezone
df = df.dropna(subset=['Text'])

# ========== Set analysis period ==========
start_date = pd.Timestamp('2022-01-01')
end_date   = pd.Timestamp('2023-12-31') 

# ========== Identify users who stopped posting ==========
# Last post time for each user
last_post_full = df.groupby('UserID', as_index=False)['time'].max().rename(columns={'time':'last_time'})

# Define “stopped”: last post within [start_date, end_date]
stoppers = last_post_full[
    (last_post_full['last_time'] >= start_date) &
    (last_post_full['last_time'] <= end_date)
].copy()

num_left = stoppers['UserID'].nunique()
print(f"\nTotal number of users who stopped posting: {num_left}")

# ========== Monthly statistics ==========
stoppers['last_month'] = stoppers['last_time'].dt.to_period('M').dt.to_timestamp()
monthly_counts = stoppers.groupby('last_month')['UserID'].count().reset_index()
monthly_counts.columns = ['month', 'num_users_stopped']
monthly_counts = monthly_counts.sort_values('month')

# ========== Plot ==========
plt.figure(figsize=(10, 5))
plt.plot(monthly_counts['month'], monthly_counts['num_users_stopped'], marker='o', linewidth=3, markersize=8)
plt.xlabel('Month', fontsize=16)
plt.ylabel('Number of developers stop posting', fontsize=16)

# Key event timeline
plt.axvline(pd.Timestamp('2022-10-28'), color='#d62728', linestyle='--', linewidth=3, label='2022-10-28')
plt.axvline(pd.Timestamp('2023-07-23'), color='#009E73', linestyle='-.', linewidth=3, label='2023-07-23')
plt.legend(fontsize=14)

plt.xticks(rotation=45, fontsize=14)
plt.yticks(fontsize=14)
plt.tight_layout()
plt.savefig('plot_path)', dpi=500)
plt.show()

# ========== Users who stopped after 2022-10-28 ==========
cutoff_date = pd.Timestamp('2022-10-28')
num_after_oct2022 = stoppers[stoppers['last_time'] >= cutoff_date]['UserID'].nunique()
print(f"\nNumber of users who stopped on/after Oct 28, 2022: {num_after_oct2022}")

# ========== Activity analysis ==========
df_left = df[df['UserID'].isin(stoppers['UserID'])]
df_left = df_left.merge(stoppers[['UserID', 'last_time']], on='UserID')

# Define window (e.g., 30 days)
window_recent = pd.Timedelta(days=30)

# ====== Tweets within 30 days before leaving ======
df_recent = df_left[
    (df_left['time'] >= df_left['last_time'] - window_recent) &
    (df_left['time'] < df_left['last_time'])
]

recent_counts = df_recent.groupby('UserID')['Text'].count().reset_index()
recent_counts.columns = ['UserID', 'tweets_recent_30d']

# Add all leaving users (fill 0 if no tweets)
all_left_users = pd.DataFrame({'UserID': stoppers['UserID']})
recent_counts_full = all_left_users.merge(recent_counts, on='UserID', how='left').fillna(0)
recent_counts_full['tweets_recent_30d'] = recent_counts_full['tweets_recent_30d'].astype(int)
recent_counts_full['avg_daily_recent'] = recent_counts_full['tweets_recent_30d'] / window_recent.days

print("Tweet counts in last 30 days before leaving:")
print(recent_counts_full['tweets_recent_30d'].describe())
print("\nAverage daily tweet counts in last 30 days before leaving:")
print(recent_counts_full['avg_daily_recent'].describe())

# Number of users with 0 tweets in last 30 days
num_zero_tweets_30d = (recent_counts_full['tweets_recent_30d'] == 0).sum()
print(f"Number of users with 0 tweets in last 30 days: {num_zero_tweets_30d}")

# Number of users with >5 tweets in last 30 days
num_over5_tweets_30d = (recent_counts_full['tweets_recent_30d'] > 5).sum()
print(f"Number of users with more than 5 tweets in last 30 days: {num_over5_tweets_30d}")

# ========== Followers/Following analysis ==========
left_users = stoppers['UserID'].unique()
latest_info = df[df['UserID'].isin(left_users)].sort_values('time', ascending=False)
latest_info = latest_info.drop_duplicates(subset='UserID', keep='first')

influence_df = latest_info[['UserID', 'Followers_Count', 'Following_Count']]
top_follower_user = influence_df.loc[influence_df['Followers_Count'].idxmax()]
print("\nUser with most followers among leavers:")
print(top_follower_user)

num_over_1k = (influence_df['Followers_Count'] > 1000).sum()
print(f"\nNumber of users with more than 1000 followers among leavers: {num_over_1k}")


