
from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()
DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')

@router.get("/")
def get_offboarding_gaps():
    offboarding = pd.read_csv(os.path.join(DATA_DIR, 'offboarding.csv'))
    users = pd.read_csv(os.path.join(DATA_DIR, 'users.csv'))
    ad = pd.read_csv(os.path.join(DATA_DIR, 'ad_accounts.csv'))
    aws = pd.read_csv(os.path.join(DATA_DIR, 'aws_accounts.csv'))
    okta = pd.read_csv(os.path.join(DATA_DIR, 'okta_accounts.csv'))

    gaps = []
    for _, row in offboarding.iterrows():
        user = users[users['user_id'] == row['user_id']].iloc[0]
        platforms = []
        if not row['ad_disabled']: platforms.append('AD')
        if not row['aws_disabled']: platforms.append('AWS')
        if not row['okta_disabled']: platforms.append('Okta')
        
        if len(platforms) > 0:
            gaps.append({
                'user_id': row['user_id'],
                'name': user['name'],
                'email': user['email'],
                'termination_date': row['termination_date'],
                'orphaned_platforms': platforms,
                'hr_status': 'TERMINATED',
                'last_activity': '2023-11-24 14:22'
            })
    return gaps
