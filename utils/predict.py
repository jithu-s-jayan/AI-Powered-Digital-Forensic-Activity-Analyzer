import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
import joblib
import os
import datetime

def process_and_predict(filepath):
    # Load model
    model_path = os.path.join('models', 'activity_classifier.cbm')
    encoder_path = os.path.join('models', 'label_encoder.pkl')
    features_path = os.path.join('models', 'expected_features.pkl')
    
    if not os.path.exists(model_path):
        return {"error": "Model not found. Please train the model first."}
        
    model = CatBoostClassifier()
    model.load_model(model_path)
    
    # Load Label Encoder if it exists
    le = None
    if os.path.exists(encoder_path):
        le = joblib.load(encoder_path)
        
    # Load expected features if they exist
    expected_features = None
    if os.path.exists(features_path):
        expected_features = joblib.load(features_path)
    
    try:
        # Load data
        df = pd.read_csv(filepath)
        
        # If we have expected features from Kaggle dataset, extract them
        if expected_features is not None:
            # Check if all expected features are present
            missing = [f for f in expected_features if f not in df.columns]
            if len(missing) > 0:
                return {"error": f"Uploaded CSV is missing {len(missing)} required features for the Kaggle model (e.g. {missing[0]})."}
            features = df[expected_features].copy()
        else:
            # Fallback to the old 6-column synthetic logic
            required_cols = ['Acc_X', 'Acc_Y', 'Acc_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z']
            col_mapping = {}
            df_cols_lower = {c.lower(): c for c in df.columns}
            for req in required_cols:
                if req in df.columns:
                    col_mapping[req] = req
                elif req.lower() in df_cols_lower:
                    col_mapping[req] = df_cols_lower[req.lower()]
                    
            if len(col_mapping) < 6:
                if len(df.columns) >= 6:
                    features = df.iloc[:, :6].copy()
                    features.columns = required_cols
                else:
                    return {"error": f"CSV must contain at least 6 columns. Found {len(df.columns)} columns."}
            else:
                features = df[[col_mapping[c] for c in required_cols]].copy()
                features.columns = required_cols
                
        # Ensure data is numeric
        features = features.apply(pd.to_numeric, errors='coerce').fillna(0)
        
        # Predict classes and probabilities
        preds = model.predict(features)
        probs = model.predict_proba(features)
        
        # DECODE PREDICTIONS IF ENCODER EXISTS
        if le is not None:
            # preds might be shape (N, 1)
            if len(preds.shape) > 1:
                preds = preds.flatten()
            decoded_preds = le.inverse_transform(preds.astype(int))
            df['Predicted_Activity'] = decoded_preds
        else:
            decoded_preds = preds.flatten()
            df['Predicted_Activity'] = decoded_preds
            
        # Extract max probability for confidence
        confidence = np.max(probs, axis=1) * 100
        
        # Aggregate results
        activity_counts = df['Predicted_Activity'].value_counts().to_dict()
        
        pie_data = {
            "labels": list(activity_counts.keys()),
            "data": list(activity_counts.values())
        }
        
        # Generate Timeline (simulating sequential data)
        base_time = datetime.datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        timeline = []
        
        # Sample every N rows for timeline to avoid too many points
        sample_rate = max(1, len(df) // 20) 
        
        for i in range(0, len(df), sample_rate):
            current_time = base_time + datetime.timedelta(seconds=i)
            activity = df.iloc[i]['Predicted_Activity']
            conf_score = confidence[i]
            
            timeline.append({
                "time": current_time.strftime("%H:%M:%S"),
                "activity": activity,
                "confidence": round(float(conf_score), 1)
            })
            
        return {
            "pie_data": pie_data,
            "summary": {
                "total_records": len(df),
                "dominant_activity": max(activity_counts, key=activity_counts.get) if activity_counts else "Unknown"
            },
            "timeline": timeline
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
