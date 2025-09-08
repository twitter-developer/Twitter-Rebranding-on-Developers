import pandas as pd
import re


df = pd.read_csv('data_path')

bluesky_regex = r'@([a-zA-Z0-9_]+\.bsky\.social)'

# Function to extract BlueSky accounts
def extract_bluesky_account(text):
    if not isinstance(text, str):
        return None
    match = re.search(bluesky_regex, text)
    if match:
        return match.group(0)  # Return full account, e.g., @johndoe.bsky.social
    return None

# Extract BlueSky accounts:
df['bluesky_account'] = df['Text'].apply(extract_bluesky_account)
df['bluesky_account'] = df['bluesky_account'].combine_first(df['Username'].apply(extract_bluesky_account))
df['bluesky_account'] = df['bluesky_account'].combine_first(df['User_Description'].apply(extract_bluesky_account))

# Filter rows containing BlueSky accounts
bluesky_account_df = df[df['bluesky_account'].notna()]


print("Unique BlueSky accounts:", bluesky_account_df['bluesky_account'].nunique())
print("Associated Twitter users:", bluesky_account_df['UserID'].nunique())
