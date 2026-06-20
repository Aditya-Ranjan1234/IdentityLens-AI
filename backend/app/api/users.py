
from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()
DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')

_cached_users = None
_cached_ad_df = None
_cached_aws_df = None
_cached_okta_df = None
_cached_sf_df = None
_cached_users_df = None

def convert_nan(obj):
    if pd.isna(obj):
        return None
    return obj

def _load_data():
    global _cached_users_df, _cached_ad_df, _cached_aws_df, _cached_okta_df, _cached_sf_df
    if _cached_users_df is None:
        _cached_users_df = pd.read_csv(os.path.join(DATA_DIR, 'users.csv'))
    if _cached_ad_df is None:
        _cached_ad_df = pd.read_csv(os.path.join(DATA_DIR, 'ad_accounts.csv'))
    if _cached_aws_df is None:
        _cached_aws_df = pd.read_csv(os.path.join(DATA_DIR, 'aws_accounts.csv'))
    if _cached_okta_df is None:
        _cached_okta_df = pd.read_csv(os.path.join(DATA_DIR, 'okta_accounts.csv'))
    if _cached_sf_df is None:
        _cached_sf_df = pd.read_csv(os.path.join(DATA_DIR, 'salesforce_accounts.csv'))
    return _cached_users_df, _cached_ad_df, _cached_aws_df, _cached_okta_df, _cached_sf_df

@router.get("/")
def get_all_users():
    global _cached_users
    if _cached_users is not None:
        return _cached_users
    
    df, ad_df, aws_df, okta_df, sf_df = _load_data()
    
    # Precompute lookups
    ad_lookup = ad_df.set_index('user_id').to_dict('index')
    aws_lookup = aws_df.set_index('user_id').to_dict('index')
    okta_lookup = okta_df.set_index('user_id').to_dict('index')
    sf_lookup = sf_df.set_index('user_id').to_dict('index')
    
    users = []
    for _, row in df.iterrows():
        user = {
            "user_id": row['user_id'],
            "name": row['name'],
            "email": row['email'],
            "department": row['department'],
            "title": row['title'],
            "status": row['status'],
            "platforms": {}
        }
        
        user_id = row['user_id']
        if user_id in ad_lookup:
            ad_dict = {k: convert_nan(v) for k, v in ad_lookup[user_id].items()}
            user['platforms']['AD'] = ad_dict
        if user_id in aws_lookup:
            aws_dict = {k: convert_nan(v) for k, v in aws_lookup[user_id].items()}
            user['platforms']['AWS'] = aws_dict
        if user_id in okta_lookup:
            okta_dict = {k: convert_nan(v) for k, v in okta_lookup[user_id].items()}
            user['platforms']['Okta'] = okta_dict
        if user_id in sf_lookup:
            sf_dict = {k: convert_nan(v) for k, v in sf_lookup[user_id].items()}
            user['platforms']['Salesforce'] = sf_dict
        
        users.append(user)
    
    _cached_users = users
    return users

