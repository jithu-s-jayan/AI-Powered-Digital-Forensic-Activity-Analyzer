import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os

def generate_synthetic_data(num_samples=5000):
    print("Generating synthetic smartphone sensor data...")
    np.random.seed(42)
    
    activities = ['Walking', 'Running', 'Sitting', 'Standing', 'Driving', 'Cycling', 'Stair Up', 'Stair Down']
    
    # Features: Acc_X, Acc_Y, Acc_Z, Gyro_X, Gyro_Y, Gyro_Z
    data = []
    labels = []
    
    for _ in range(num_samples):
        activity = np.random.choice(activities)
        
        if activity == 'Sitting':
            acc = np.random.normal(loc=[0.0, 9.8, 0.0], scale=[0.1, 0.1, 0.1])
            gyro = np.random.normal(loc=[0.0, 0.0, 0.0], scale=[0.01, 0.01, 0.01])
        elif activity == 'Standing':
            acc = np.random.normal(loc=[0.0, 9.8, 0.0], scale=[0.2, 0.2, 0.2])
            gyro = np.random.normal(loc=[0.0, 0.0, 0.0], scale=[0.05, 0.05, 0.05])
        elif activity == 'Walking':
            acc = np.random.normal(loc=[0.0, 9.8, 2.0], scale=[1.5, 2.0, 1.5])
            gyro = np.random.normal(loc=[0.5, 0.5, 0.5], scale=[1.0, 1.0, 1.0])
        elif activity == 'Running':
            acc = np.random.normal(loc=[0.0, 9.8, 5.0], scale=[4.0, 5.0, 4.0])
            gyro = np.random.normal(loc=[1.5, 1.5, 1.5], scale=[3.0, 3.0, 3.0])
        elif activity == 'Driving':
            acc = np.random.normal(loc=[0.5, 9.8, 0.5], scale=[0.5, 0.5, 0.5])
            gyro = np.random.normal(loc=[0.1, 0.1, 0.1], scale=[0.2, 0.2, 0.2])
        elif activity == 'Cycling':
            acc = np.random.normal(loc=[0.2, 9.8, 1.5], scale=[1.0, 1.0, 1.0])
            gyro = np.random.normal(loc=[0.3, 0.3, 0.3], scale=[0.8, 0.8, 0.8])
        elif activity == 'Stair Up':
            acc = np.random.normal(loc=[0.0, 9.8, 3.0], scale=[2.0, 3.0, 2.0])
            gyro = np.random.normal(loc=[1.0, 1.0, 1.0], scale=[1.5, 1.5, 1.5])
        elif activity == 'Stair Down':
            acc = np.random.normal(loc=[0.0, 9.8, -3.0], scale=[2.0, 3.0, 2.0])
            gyro = np.random.normal(loc=[1.0, 1.0, 1.0], scale=[1.5, 1.5, 1.5])
            
        row = list(acc) + list(gyro)
        data.append(row)
        labels.append(activity)
        
    df = pd.DataFrame(data, columns=['Acc_X', 'Acc_Y', 'Acc_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z'])
    df['Activity'] = labels
    
    # Save to dataset folder
    os.makedirs('datasets', exist_ok=True)
    df.to_csv('datasets/synthetic_sensor_data.csv', index=False)
    print("Dataset saved to datasets/synthetic_sensor_data.csv")
    return df

def train():
    df = generate_synthetic_data(10000)
    
    X = df.drop('Activity', axis=1)
    y = df['Activity']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training CatBoost model...")
    model = CatBoostClassifier(iterations=500, learning_rate=0.1, depth=6, loss_function='MultiClass', verbose=100)
    
    model.fit(X_train, y_train, eval_set=(X_test, y_test))
    
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"\nModel Accuracy: {acc * 100:.2f}%")
    
    print("\nClassification Report:")
    print(classification_report(y_test, preds))
    
    os.makedirs('models', exist_ok=True)
    model_path = 'models/activity_classifier.cbm'
    model.save_model(model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train()
