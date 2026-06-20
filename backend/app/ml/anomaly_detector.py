
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')
MODEL_DIR = os.path.join(os.path.dirname(__file__), '../../models')

# Cache loaded data and results
_cached_audit_df = None
_cached_users_df = None
_cached_anomaly_results = None
_cached_audit_lookup = None

def _load_data():
    global _cached_audit_df, _cached_users_df, _cached_audit_lookup
    if _cached_audit_df is None:
        _cached_audit_df = pd.read_csv(os.path.join(DATA_DIR, 'audit_logs.csv'))
        # Precompute lookup
        _cached_audit_lookup = {}
        for user_id, group in _cached_audit_df.groupby('user_id'):
            _cached_audit_lookup[user_id] = group.copy()
    if _cached_users_df is None:
        _cached_users_df = pd.read_csv(os.path.join(DATA_DIR, 'users.csv'))
    return _cached_audit_lookup, _cached_users_df

def extract_features():
    audit_lookup, users_df = _load_data()
    user_ids = users_df['user_id'].values
    features = []
    for user_id in user_ids:
        user_logs = audit_lookup.get(user_id, pd.DataFrame())
        login_count = len(user_logs[user_logs['action'] == 'LOGIN'])
        platform_count = int(user_logs['platform'].nunique())
        resource_count = int(user_logs['resource'].nunique())
        country_count = int(user_logs['country'].nunique())
        hour_variance = 0.0
        
        try:
            if len(user_logs) > 0:
                user_logs.loc[:, 'hour'] = pd.to_datetime(user_logs['timestamp'], errors='coerce').dt.hour
                valid_hours = user_logs['hour'].dropna()
                if len(valid_hours) > 1:
                    hour_variance = float(valid_hours.var())
        except Exception:
            pass
        
        features.append([login_count, platform_count, resource_count, country_count, hour_variance])
    X = np.array(features, dtype=np.float64)
    X = np.nan_to_num(X, nan=0.0, posinf=1e10, neginf=-1e10)
    return X, user_ids, features

def train_all_models():
    os.makedirs(MODEL_DIR, exist_ok=True)
    X, user_ids, features = extract_features()
    
    # Train Isolation Forest
    if_model = IsolationForest(contamination=0.05, random_state=42)
    if_model.fit(X)
    joblib.dump(if_model, os.path.join(MODEL_DIR, 'isolation_forest_model.pkl'))
    
    # Train One-Class SVM
    ocsvm_model = OneClassSVM(nu=0.05, kernel='rbf', gamma='scale')
    ocsvm_model.fit(X)
    joblib.dump(ocsvm_model, os.path.join(MODEL_DIR, 'one_class_svm_model.pkl'))
    
    # Train Local Outlier Factor
    lof_model = LocalOutlierFactor(n_neighbors=20, contamination=0.05, novelty=True)
    lof_model.fit(X)
    joblib.dump(lof_model, os.path.join(MODEL_DIR, 'local_outlier_factor_model.pkl'))
    
    return if_model, ocsvm_model, lof_model

def load_model(model_type="isolation_forest"):
    if model_type == "isolation_forest":
        model_path = os.path.join(MODEL_DIR, 'isolation_forest_model.pkl')
    elif model_type == "one_class_svm":
        model_path = os.path.join(MODEL_DIR, 'one_class_svm_model.pkl')
    elif model_type == "local_outlier_factor":
        model_path = os.path.join(MODEL_DIR, 'local_outlier_factor_model.pkl')
    else:
        return None
    
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

def get_anomalies(model_type="isolation_forest"):
    if not os.path.exists(os.path.join(MODEL_DIR, 'isolation_forest_model.pkl')):
        train_all_models()
    
    model = load_model(model_type)
    if not model:
        return []
    
    X, user_ids, features = extract_features()
    
    predictions = model.predict(X)
    if model_type == "local_outlier_factor":
        # LOF uses decision_function on novelty mode
        anomaly_scores = model.decision_function(X)
    else:
        anomaly_scores = model.decision_function(X)
    
    results = []
    for i, user_id in enumerate(user_ids):
        results.append({
            "user_id": user_id,
            "is_anomaly": bool(predictions[i] == -1),
            "anomaly_score": float(anomaly_scores[i]),
            "model": model_type,
            "features": {
                "login_count": int(features[i][0]),
                "platform_count": int(features[i][1]),
                "resource_count": int(features[i][2]),
                "country_count": int(features[i][3]),
                "hour_variance": float(features[i][4])
            }
        })
    
    return results

