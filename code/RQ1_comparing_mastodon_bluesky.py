import pandas as pd
import matplotlib.pyplot as plt

# Define the unified time range
start_date = pd.Timestamp('2022-01-01')
end_date = pd.Timestamp('2024-09-30')
all_months = pd.date_range(start=start_date, end='2024-09-01', freq='MS')  # MS = Month Start

# ==== Mastodon ====
mastodon_df = pd.read_csv('mastodon_data_path')
mastodon_df['post_time'] = pd.to_datetime(mastodon_df['post_time'], errors='coerce')

# Get each user's first post
mastodon_first = mastodon_df.sort_values('post_time').groupby('user_id', as_index=False).first()
mastodon_first['month'] = mastodon_first['post_time'].dt.to_period('M').dt.to_timestamp()

# Filter posts within the analysis period
mastodon_first = mastodon_first[(mastodon_first['month'] >= start_date) & (mastodon_first['month'] <= end_date)]

# Count first posts per month, fill missing months with 0
mastodon_monthly = mastodon_first.groupby('month').size().reindex(all_months, fill_value=0).reset_index()
mastodon_monthly.columns = ['month', 'count']
mastodon_monthly['source'] = 'Mastodon'

# ==== Bluesky ====
bluesky_df = pd.read_csv('bluesky_data_path')
bluesky_df['post_time'] = pd.to_datetime(bluesky_df['created_at'], utc=True, errors='coerce')

# Get each user's first post
bluesky_first = bluesky_df.sort_values('post_time').groupby('username', as_index=False).first()
bluesky_first['month'] = bluesky_first['post_time'].dt.to_period('M').dt.to_timestamp()

# Filter posts within the analysis period
bluesky_first = bluesky_first[(bluesky_first['month'] >= start_date) & (bluesky_first['month'] <= end_date)]

# Count first posts per month, fill missing months with 0
bluesky_monthly = bluesky_first.groupby('month').size().reindex(all_months, fill_value=0).reset_index()
bluesky_monthly.columns = ['month', 'count']
bluesky_monthly['source'] = 'Bluesky'

# ==== Merge data and plot ====
all_data = pd.concat([mastodon_monthly, bluesky_monthly])
all_data = all_data.sort_values(['month', 'source'])

plt.figure(figsize=(12, 6))

# Plot first posts for each source
for label, group in all_data.groupby('source'):
    plt.plot(group['month'], group['count'], marker='o', linewidth=3, label=label)

plt.xlabel('Month', fontsize=16)
plt.ylabel("Developers' First Posts", fontsize=16)
plt.xticks(rotation=45, fontsize=14)
plt.yticks(fontsize=14)

# Highlight specific dates
plt.axvline(pd.Timestamp('2022-10-28'), color='#d62728', linestyle='--', linewidth=3, label='2022-10-28')
plt.axvline(pd.Timestamp('2023-07-23'), color='#009E73', linestyle='-.', linewidth=3, label='2023-07-23')

plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig('plot_path', dpi=500)
plt.show()
