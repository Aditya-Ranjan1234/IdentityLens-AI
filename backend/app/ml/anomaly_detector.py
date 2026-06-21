
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

# In-memory model cache (avoid re-loading from disk each request)
_models_cache = {}

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
        login_count = len(user_logs[user_logs['action'] == 'LOGIN']) if len(user_logs) > 0 else 0
        platform_count = int(user_logs['platform'].nunique()) if len(user_logs) > 0 else 0
        resource_count = int(user_logs['resource'].nunique()) if len(user_logs) > 0 else 0
        country_count = int(user_logs['country'].nunique()) if len(user_logs) > 0 else 0
        hour_variance = 0.0

        try:
            if len(user_logs) > 0:
                user_logs = user_logs.copy()
                # Use ISO8601 format explicitly — avoids slow dateutil fallback warning
                user_logs['hour'] = pd.to_datetime(
                    user_logs['timestamp'], format='ISO8601', errors='coerce'
                ).dt.hour
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
    """Train and save all models. Always overwrites existing files."""
    global _models_cache
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

    # Populate in-memory cache
    _models_cache = {
        'isolation_forest': if_model,
        'one_class_svm': ocsvm_model,
        'local_outlier_factor': lof_model,
    }

    return if_model, ocsvm_model, lof_model

def _model_key(model_type):
    paths = {
        'isolation_forest': 'isolation_forest_model.pkl',
        'one_class_svm': 'one_class_svm_model.pkl',
        'local_outlier_factor': 'local_outlier_factor_model.pkl',
    }
    return paths.get(model_type)

def load_model(model_type="isolation_forest"):
    """Load model from in-memory cache, disk, or retrain if missing/corrupt."""
    global _models_cache

    # 1. In-memory cache hit
    if model_type in _models_cache:
        return _models_cache[model_type]

    # 2. Try loading from disk
    filename = _model_key(model_type)
    if filename is None:
        return None

    model_path = os.path.join(MODEL_DIR, filename)
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            _models_cache[model_type] = model
            return model
        except Exception:
            # Stale / incompatible pickle — delete and retrain below
            os.remove(model_path)

    # 3. File missing or corrupt → retrain everything
    train_all_models()
    return _models_cache.get(model_type)

def _ensure_models():
    """Make sure all models are available (training if necessary)."""
    if_path = os.path.join(MODEL_DIR, 'isolation_forest_model.pkl')
    if not os.path.exists(if_path):
        train_all_models()
        return

    # Quick sanity-check: try loading the primary model
    try:
        joblib.load(if_path)
    except Exception:
        # Stale pickle from a different Python version → retrain
        train_all_models()

def get_anomalies(model_type="isolation_forest"):
    _ensure_models()

    model = load_model(model_type)
    if not model:
        return []

    X, user_ids, features = extract_features()

    predictions = model.predict(X)
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
