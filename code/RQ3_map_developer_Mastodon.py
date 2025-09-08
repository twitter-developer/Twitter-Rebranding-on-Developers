import pandas as pd
import re


df = pd.read_csv('data_path')

# List of Mastodon instances
mastodon_servers = [
    r'\bmstdn\.social\b', r'\bmastodon\.world\b', r'\bmas\.to\b',
    r'\bc\.im\b', r'\bmasto\.ai\b', r'\bfosstodon\.org\b',
    r'\binfosec\.exchange\b', r'\bsfba\.social\b', r'\bmindly\.social\b',
    r'\btoot\.community\b', r'\bmastodon\.online\b', r'\bmastodon\.social\b',
    r'\bnoc\.social\b', r'\bawscommunity\.social\b', r'\bfree-radical\.social\b',
    r'\bhispagatos\.social\b', r'\bdefcon\.social\b', r'\bmastodon\.radio\b',
    r'\bmastodon\.energy\b', r'\btreehouse\.social\b', r'\bnzoss\.social\b',
    r'\bassemblag\.es\b', r'\bstarnix\.social\b', r'\btechtoots\.social\b',
    r'\bazureheads\.social\b', r'\bgladtech\.social\b', r'\btty\.social\b',
    r'\btechie\.community\b', r'\baccessibility\.social\b', r'\bcoales\.co\b',
    r'\bhardlimit\.com\b', r'\btechnodon\.social\b', r'\bfsinfstodon\.social\b',
    r'\bh4x0rarmy\.social\b', r'\btechnews\.social\b', r'\bmastodon\.shantih19\.xyz\b',
    r'\beuccommunity\.social\b', r'\bgrinstodon\.social\b', r'\bbytesize\.social\b',
    r'\bidealhealth\.social\b', r'\bstranger\.social\b', r'\bgathering\.space\b',
    r'\bmadscientists\.social\b', r'\btroll\.social\b', r'\bmastodon\.borsos\.at\b',
    r'\bykzts\.technology\b', r'\bhaminoa\.social\b', r'\bwikiwack\.social\b',
    r'\bthegamers\.tavern\b', r'\bretro\.gaiden\b', r'\bliberal\.city\b',
    r'\bbeige\.party\b', r'\bmastodom\.social\b', r'\btechdon\.dev\b',
    r'\bgreengamedevelopment\.social\b', r'\bmstdn\.sirmaple\.ca\b',
    r'\bdislemoi\.social\b', r'\bsocial\.vouaix\.com\b', r'\brpigroup\.social\b',
    r'\bmastodon\.sdf\b', r'\beggplant\.social\b', r'\bloli\.exposed\b',
    r'\bcryptodon\.lol\b', r'\bcosmicnation\.social\b', r'\bgeobla\.social\b',
    r'\btherainbownetwork\.social\b', r'\bburmasocial\.social\b',
    r'\bmastodon\.gayfr\.social\b', r'\bkatsudon\.social\b', r'\bbaraag\.net\b',
    r'\bfurry\.engineer\b', r'\bsustainability\.social\b', r'\bckstechnews\.social\b',
    r'\bzenzone\.social\b', r'\bclickbait\.social\b', r'\bmastodontunisie\.social\b',
    r'\bakiba\.social\b', r'\bleaningleft\.social\b', r'\bwadoryu\.social\b',
    r'\bvtuber\.house\b', r'\bcircleoflight\.social\b', r'\bbetterboston\.social\b',
    r'\bmountainash\.social\b', r'\bmountains\.social\b', r'\bcardanodevelopment\.com\b',
    r'\bvenera\.social\b', r'\blibranet\.de\b', r'\bdeacon\.social\b'
]

# Map developers
def find_mastodon_account(text):
    if not isinstance(text, str):
        return None
    for server in mastodon_servers:
        match = re.search(rf'@\w+@{server}', text, re.IGNORECASE)
        if match:
            return match.group()
    return None

# Extract Mastodon usernames from each field
df['mastodon_username_name'] = df['Username'].apply(find_mastodon_account)
df['mastodon_username_profile'] = df['User_Description'].apply(find_mastodon_account)
df['mastodon_username_text'] = df['Text'].apply(find_mastodon_account)


def get_first_mastodon_match(row):
    for col in ['Username', 'User_Description', 'Text']:
        result = find_mastodon_account(row[col])
        if result:
            return result
    return None

df['mastodon_account'] = df.apply(get_first_mastodon_match, axis=1)

# Filter users with Mastodon accounts
mastodon_account_df = df[df['mastodon_account'].notna()]

