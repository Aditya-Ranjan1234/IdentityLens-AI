import pandas as pd
import os
from typing import Dict, List

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')

# Define a privilege hierarchy
PRIVILEGE_SCORES = {
    "AdministratorAccess": 100,
    "Domain Admin": 100,
    "SuperAdmin": 100,
    "System Administrator": 95,
    "PowerUserAccess": 80,
    "AmazonEC2FullAccess": 70,
    "AmazonS3FullAccess": 70,
    "ReadOnlyAccess": 30,
    "View All Data": 30,
    "Marketing User": 20,
    "Sales User": 20,
}

def calculate_effective_privilege(user_id: str) -> Dict:
    aws_df = pd.read_csv(os.path.join(DATA_DIR, 'aws_accounts.csv'))
    okta_df = pd.read_csv(os.path.join(DATA_DIR, 'okta_accounts.csv'))
    salesforce_df = pd.read_csv(os.path.join(DATA_DIR, 'salesforce_accounts.csv'))
    ad_df = pd.read_csv(os.path.join(DATA_DIR, 'ad_accounts.csv'))

    effective_privileges: List[str] = []
    privilege_score = 0
    is_admin = False

    # AWS
    aws_account = aws_df[aws_df['user_id'] == user_id]
    if not aws_account.empty:
        roles = aws_account.iloc[0]['roles'].split(',')
        for role in roles:
            effective_privileges.append(f"AWS:{role}")
            if role in PRIVILEGE_SCORES:
                privilege_score += PRIVILEGE_SCORES[role]
            if role in ["AdministratorAccess", "PowerUserAccess"]:
                is_admin = True

    # Okta
    okta_account = okta_df[okta_df['user_id'] == user_id]
    if not okta_account.empty:
        groups = okta_account.iloc[0]['groups'].split(',')
        for group in groups:
            effective_privileges.append(f"Okta:{group}")
            if group in ["Admins", "SuperAdmin"]:
                is_admin = True
                privilege_score += 100

    # Salesforce
    sf_account = salesforce_df[salesforce_df['user_id'] == user_id]
    if not sf_account.empty:
        profile = sf_account.iloc[0]['profile']
        effective_privileges.append(f"Salesforce:{profile}")
        if profile == "System Administrator":
            is_admin = True
            privilege_score += 95
        perms = sf_account.iloc[0]['permissions'].split(',') if pd.notna(sf_account.iloc[0]['permissions']) else []
        for perm in perms:
            effective_privileges.append(f"SalesforcePerm:{perm}")

    # AD
    ad_account = ad_df[ad_df['user_id'] == user_id]
    if not ad_account.empty:
        effective_privileges.append(f"AD:{ad_account.iloc[0]['ad_account']}")

    return {
        "user_id": user_id,
        "effective_privileges": effective_privileges,
        "privilege_score": min(privilege_score, 200),
        "is_admin": is_admin
    }
