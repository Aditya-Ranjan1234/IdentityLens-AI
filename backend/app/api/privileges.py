from fastapi import APIRouter, HTTPException
from app.graph.builder import calculate_effective_privileges, build_identity_graph_object
import pandas as pd
import os

router = APIRouter()
DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')

# Pre-load identity graph once!
G = build_identity_graph_object()

# Pre-load data
users_df = pd.read_csv(os.path.join(DATA_DIR, 'users.csv'))
aws_df = pd.read_csv(os.path.join(DATA_DIR, 'aws_accounts.csv'))
okta_df = pd.read_csv(os.path.join(DATA_DIR, 'okta_accounts.csv'))
sf_df = pd.read_csv(os.path.join(DATA_DIR, 'salesforce_accounts.csv'))
ad_df = pd.read_csv(os.path.join(DATA_DIR, 'ad_accounts.csv'))

# Create dictionaries for quick lookups
aws_lookup = dict(zip(aws_df['user_id'], aws_df.to_dict('records')))
okta_lookup = dict(zip(okta_df['user_id'], okta_df.to_dict('records')))
sf_lookup = dict(zip(sf_df['user_id'], sf_df.to_dict('records')))
ad_lookup = dict(zip(ad_df['user_id'], ad_df.to_dict('records')))

def calculate_privilege_score(effective_perms, roles):
    score = 0
    is_admin = False
    for perm in effective_perms:
        if perm in ["AdministratorAccess", "PowerUserAccess", "Modify All Data", "Delete Records"]:
            score += 100
            is_admin = True
        elif perm in ["AmazonEC2FullAccess", "AmazonS3FullAccess"]:
            score +=70
        else:
            score +=20
    return min(score, 200), is_admin

@router.get("/")
def get_all_privileges():
    all_privileges = []
    for _, user in users_df.iterrows():
        ep = calculate_effective_privileges(G, user['user_id'])
        score, is_admin = calculate_privilege_score(ep['effective_permissions'], ep['roles'])
        all_privileges.append({
            "user_id": user['user_id'],
            "effective_privileges": ep['effective_permissions'],
            "roles": ep['roles'],
            "groups": ep['groups'],
            "privilege_score": score,
            "is_admin": is_admin
        })
    return all_privileges

@router.get("/{user_id}")
def get_user_privileges(user_id: str):
    try:
        ep = calculate_effective_privileges(G, user_id)
        score, is_admin = calculate_privilege_score(ep['effective_permissions'], ep['roles'])
        return {
            "user_id": user_id,
            "effective_privileges": ep['effective_permissions'],
            "roles": ep['roles'],
            "groups": ep['groups'],
            "privilege_score": score,
            "is_admin": is_admin
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
