import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# ========== Load data ==========
df = pd.read_csv('sponsor_data')
print(len(df))

# Split data into before and after rebranding
before_df = df[df['posted_before_rebranding'] == True]
after_df = df[df['posted_before_rebranding'] == False]

print(len(before_df))
print(len(after_df))

# Function to analyze user types
def analyze_user_type(sub_df, label=''):
    counts = sub_df['type'].value_counts()
    ratio = counts / counts.sum()

    print(f"=== User Type Ratios ({label}) ===")
    print("Counts:\n", counts)
    print("Ratios:\n", ratio)
    print()

# Function to analyze primary programming languages
def analyze_languages(sub_df, label='', topn=7):
    langs = sub_df[['github_username', 'primary_language']].dropna().drop_duplicates(subset='github_username')

    # Count all languages by unique GitHub users
    all_langs = langs['primary_language'].tolist()
    counter_all = Counter(all_langs)

    # Get top N languages
    top_langs = [lang for lang, _ in counter_all.most_common(topn)]

    def get_language_counts(df):
        langs = df[['github_username', 'primary_language']].dropna().drop_duplicates(subset='github_username')
        all_langs = langs['primary_language'].tolist()
        counter = Counter(all_langs)
        total = sum(counter.values())
        return counter, total

    person_df = sub_df[sub_df['type'] == 'User']
    org_df = sub_df[sub_df['type'] == 'Organization']

    person_counter, person_total = get_language_counts(person_df)
    org_counter, org_total = get_language_counts(org_df)

    def summarize_counter(counter, top_langs):
        result = {}
        other_count = 0
        for lang, count in counter.items():
            if lang in top_langs and lang != 'Undetermined':
                result[lang] = count
            else:
                other_count += count
        result['Other'] = other_count
        return result

    summarized_person = summarize_counter(person_counter, top_langs)
    summarized_org = summarize_counter(org_counter, top_langs)

    def calc_ratio(count, total):
        return (count / total * 100) if total > 0 else 0

    # Force language order: top_langs + 'Other'
    lang_order = [lang for lang in top_langs if lang in summarized_person or lang in summarized_org]
    lang_order.append('Other')

    print(f"=== Primary Programming Language Counts and Ratios ({label}) ===")
    print(f"{'Language':<20} {'Person':<20} {'Organization':<20}")
    print("-" * 60)

    for lang in lang_order:
        person_count = summarized_person.get(lang, 0)
        person_ratio = calc_ratio(person_count, person_total)
        org_count = summarized_org.get(lang, 0)
        org_ratio = calc_ratio(org_count, org_total)
        print(f"{lang:<20} {person_count} ({person_ratio:.1f}%) {'':<5} {org_count} ({org_ratio:.1f}%)")

    print("-" * 60)
    print(f"{'Sum':<20} {person_total:<20} {org_total:<20}")
    print()

# Analyze data before rebranding
analyze_user_type(before_df, label='Before Rebranding')
analyze_languages(before_df, label='Before Rebranding')

# Analyze data after rebranding
analyze_user_type(after_df, label='After Rebranding')
analyze_languages(after_df, label='After Rebranding')

# GitHub user intersection between before and after
before_users = set(before_df['github_username'].dropna())
after_users = set(after_df['github_username'].dropna())
both_users = before_users & after_users

print(f"Number of GitHub users in both before and after: {len(both_users)}")

# ========== Monthly tweet count plot ==========
df['time'] = pd.to_datetime(df['Tweet_Created At'], format='%a %b %d %H:%M:%S %z %Y', errors='coerce')
df['year_month'] = df['time'].dt.to_period('M')

monthly_counts = df['year_month'].value_counts().sort_index()
monthly_counts.index = monthly_counts.index.astype(str)

# Select every 3 months for x-axis ticks
xticks = monthly_counts.index[::3]

plt.figure(figsize=(12, 6))
monthly_counts.plot(kind='line', marker='o')
plt.xlabel("Month")
plt.ylabel("Number of Tweets")

# Set x-axis labels and rotate
plt.xticks(ticks=range(len(monthly_counts)), labels=monthly_counts.index, rotation=45)

# Show only every 3rd tick label
for i, label in enumerate(plt.gca().get_xticklabels()):
    if monthly_counts.index[i] not in xticks:
        label.set_visible(False)

plt.tight_layout()
plt.savefig('plot_path', dpi=500)
plt.show()


