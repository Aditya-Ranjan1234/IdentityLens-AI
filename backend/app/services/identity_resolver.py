import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')

def resolve_identities():
    users_df = pd.read_csv(os.path.join(DATA_DIR, 'users.csv'))
    ad_df = pd.read_csv(os.path.join(DATA_DIR, 'ad_accounts.csv'))
    aws_df = pd.read_csv(os.path.join(DATA_DIR, 'aws_accounts.csv'))
    okta_df = pd.read_csv(os.path.join(DATA_DIR, 'okta_accounts.csv'))
    salesforce_df = pd.read_csv(os.path.join(DATA_DIR, 'salesforce_accounts.csv'))

    master_identities = []

    for _, user in users_df.iterrows():
        master_id = user['user_id']

        ad_account = ad_df[ad_df['user_id'] == master_id]
        aws_account = aws_df[aws_df['user_id'] == master_id]
        okta_account = okta_df[okta_df['user_id'] == master_id]
        salesforce_account = salesforce_df[salesforce_df['user_id'] == master_id]

        platform_ids = {}

        if not ad_account.empty:
            platform_ids['ad'] = ad_account.iloc[0]['ad_account']
        if not aws_account.empty:
            platform_ids['aws'] = aws_account.iloc[0]['aws_user']
        if not okta_account.empty:
            platform_ids['okta'] = okta_account.iloc[0]['okta_id']
        if not salesforce_account.empty:
            platform_ids['salesforce'] = master_id

        master_identities.append({
            'master_id': master_id,
            'name': user['name'],
            'email': user['email'],
            'department': user['department'],
            'platform_ids': platform_ids,
            'status': user['status']
        })

    return master_identities
