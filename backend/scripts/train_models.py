
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.ml.anomaly_detector import train_all_models

if __name__ == "__main__":
    train_all_models()
    print("All models trained and saved successfully!")

