import pandas as pd
import numpy as np
import os

def create_specific_trace(filename, dominant_activities, num_samples=2000):
    print(f"Generating {filename}...")
    np.random.seed() # Randomize seed
    
    data = []
    labels = []
    
    for _ in range(num_samples):
        # 80% chance of being one of the dominant activities, 20% random
        if np.random.rand() < 0.80:
            activity = np.random.choice(dominant_activities)
        else:
            all_activities = ['Walking', 'Running', 'Sitting', 'Standing', 'Driving', 'Cycling', 'Stair Up', 'Stair Down']
            activity = np.random.choice(all_activities)
            
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
    
    # Save to dataset folder
    os.makedirs('datasets', exist_ok=True)
    filepath = os.path.join('datasets', filename)
    df.to_csv(filepath, index=False)
    print(f"Saved: {filepath}")

if __name__ == "__main__":
    create_specific_trace('suspect_1_running_trace.csv', ['Running', 'Walking'])
    create_specific_trace('suspect_2_driving_trace.csv', ['Driving', 'Sitting'])
    create_specific_trace('suspect_3_mixed_trace.csv', ['Cycling', 'Stair Up', 'Stair Down'])
    print("Done generating test files!")
