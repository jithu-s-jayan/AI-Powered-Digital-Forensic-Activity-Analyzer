import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os

def train_on_kaggle_data(csv_path="datasets/Human_activity_Dataset.csv"):
    print(f"Loading dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    print("Unique activities found:", df['Activity'].unique())
    
    # Drop irrelevant columns if they exist
    if 'subject/Participant' in df.columns:
        df = df.drop('subject/Participant', axis=1)
    if 'subject' in df.columns:
        df = df.drop('subject', axis=1)
        
    # Split X and y
    X = df.drop('Activity', axis=1)
    y = df['Activity']
    
    # Label Encoder (CRITICAL FIX)
    print("Encoding labels...")
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Save Label Encoder
    os.makedirs('models', exist_ok=True)
    joblib.dump(le, "models/label_encoder.pkl")
    
    # Save expected features to ensure predict.py gets exactly the right columns
    expected_features = list(X.columns)
    joblib.dump(expected_features, "models/expected_features.pkl")
    
    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    print("Training CatBoost Classifier...")
    model = CatBoostClassifier(
        iterations=100,
        learning_rate=0.1,
        depth=6,
        loss_function='MultiClass',
        verbose=10
    )
    
    model.fit(X_train, y_train, eval_set=(X_test, y_test))
    
    # Save Model
    model.save_model(os.path.join('models', 'activity_classifier.cbm'))
    print("Training complete! Model and Encoder saved.")

if __name__ == "__main__":
    train_on_kaggle_data()
