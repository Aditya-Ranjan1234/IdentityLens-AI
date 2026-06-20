
import pandas as pd
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')

# Cache loaded data
_cached_users_df = None
_cached_ad_df = None
_cached_aws_df = None
_cached_okta_df = None
_cached_offboard_df = None
_cached_risk_scores = None

def _load_data():
    global _cached_users_df, _cached_ad_df, _cached_aws_df, _cached_okta_df, _cached_offboard_df
    if _cached_users_df is None:
        _cached_users_df = pd.read_csv(os.path.join(DATA_DIR, 'users.csv'))
    if _cached_ad_df is None:
        _cached_ad_df = pd.read_csv(os.path.join(DATA_DIR, 'ad_accounts.csv'))
    if _cached_aws_df is None:
        _cached_aws_df = pd.read_csv(os.path.join(DATA_DIR, 'aws_accounts.csv'))
    if _cached_okta_df is None:
        _cached_okta_df = pd.read_csv(os.path.join(DATA_DIR, 'okta_accounts.csv'))
    if _cached_offboard_df is None and os.path.exists(os.path.join(DATA_DIR, 'offboarding.csv')):
        _cached_offboard_df = pd.read_csv(os.path.join(DATA_DIR, 'offboarding.csv'))
    return _cached_users_df, _cached_ad_df, _cached_aws_df, _cached_okta_df, _cached_offboard_df

def calculate_risk_scores():
    global _cached_risk_scores
    if _cached_risk_scores is not None:
        return _cached_risk_scores
    
    users_df, ad_df, aws_df, okta_df, offboard_df = _load_data()
    
    risk_results = []
    today = datetime.now()
    
    # Precompute lookups
    aws_lookup = aws_df.set_index('user_id').to_dict('index')
    okta_lookup = okta_df.set_index('user_id').to_dict('index')
    ad_lookup = ad_df.set_index('user_id').to_dict('index')
    offboard_lookup = None
    if offboard_df is not None:
        offboard_lookup = offboard_df.set_index('user_id').to_dict('index')
    
    for _, row in users_df.iterrows():
        risk_score = 0
        risk_reasons = []
        severity = "LOW"
        
        user_id = row['user_id']
        
        # Check offboarding gaps
        if offboard_lookup is not None and user_id in offboard_lookup:
            off = offboard_lookup[user_id]
            if off['ad_disabled'] == 'FALSE' or off['aws_disabled'] == 'FALSE' or off['okta_disabled'] == 'FALSE':
                risk_score += 40
                risk_reasons.append("Offboarding gap: account active in some platforms after termination")
        
        # Check for cross-platform admin
        is_admin = False
        admin_count = 0
        if user_id in aws_lookup and 'AdministratorAccess' in aws_lookup[user_id]['roles']:
            admin_count +=1
        
        if user_id in okta_lookup and 'Admins' in okta_lookup[user_id]['groups']:
            admin_count +=1
        
        if admin_count >=2:
            risk_score +=35
            risk_reasons.append("Cross-platform admin privileges detected")
            is_admin = True
        
        # Check dormancy
        last_login_ad = None
        last_login_aws = None
        
        if user_id in ad_lookup and pd.notna(ad_lookup[user_id]['last_login']):
            try:
                last_login_ad = datetime.strptime(ad_lookup[user_id]['last_login'], '%Y-%m-%d')
                delta = (today - last_login_ad).days
                if delta > 90 and is_admin:
                    risk_score += 20
                    risk_reasons.append(f"Dormant admin (last login {delta} days ago)")
            except:
                pass
        
        if user_id in aws_lookup and pd.notna(aws_lookup[user_id]['last_login']):
            try:
                last_login_aws = datetime.strptime(aws_lookup[user_id]['last_login'], '%Y-%m-%d')
                delta = (today - last_login_aws).days
                if delta > 90 and is_admin:
                    risk_score +=20
                    risk_reasons.append(f"Dormant AWS admin (last login {delta} days ago)")
            except:
                pass
        
        if risk_score >= 70:
            severity = "CRITICAL"
        elif risk_score >=40:
            severity = "HIGH"
        elif risk_score >=20:
            severity = "MEDIUM"
        
        risk_results.append({
            "user_id": user_id,
            "name": row['name'],
            "department": row['department'],
            "risk_score": risk_score,
            "severity": severity,
            "reasons": risk_reasons
        })
    
    _cached_risk_scores = sorted(risk_results, key=lambda x: x['risk_score'], reverse=True)
    return _cached_risk_scores

