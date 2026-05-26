# AI-Powered Digital Forensic Activity Analyzer

A modern, futuristic, professional, research-level forensic investigation system that uses Artificial Intelligence and Machine Learning to analyze smartphone sensor traces and predict human physical activities.

## Features

- **CatBoost ML Engine:** High-accuracy predictions for physical activities.
- **Futuristic UI:** Built with Tailwind CSS, Bootstrap 5, Glassmorphism, and GSAP/AOS animations.
- **Firebase Authentication:** Secure login, signup, and session handling.
- **Interactive Dashboard:** Data visualization with Chart.js.
- **Forensic Reporting:** Generate and print AI confidence scores and activity timelines.

## Technologies Used

- **Frontend:** HTML5, CSS3, JavaScript, Tailwind CSS, Bootstrap 5, GSAP, Chart.js
- **Backend:** Python, Flask
- **Machine Learning:** CatBoost, Scikit-learn, Pandas, NumPy
- **Authentication:** Firebase Auth

## Installation and Setup

1. **Clone or Download the Project**
2. **Create a Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Firebase:**
   - Open `static/js/main.js`.
   - Replace the `firebaseConfig` placeholder with your actual Firebase configuration.
5. **Train the Initial Model:**
   - Run `python train_model.py`. This will generate synthetic sensor data and train the CatBoost classifier, saving it to `models/activity_classifier.cbm`.
6. **Start the Flask Server:**
   ```bash
   python app.py
   ```
7. **Access the App:**
   - Navigate to `http://localhost:5000` in your web browser.

## Project Structure

- `/templates`: HTML files for the frontend views.
- `/static`: CSS, JavaScript, and Image assets.
- `/models`: Saved trained machine learning models (`.cbm` format).
- `/datasets`: Location for synthetic training data and uploaded investigation files.
- `/routes`: Flask API endpoints.
- `/utils`: Helper functions for ML prediction.
- `app.py`: Main Flask application entry point.
- `train_model.py`: Script to generate synthetic training data and train the AI model.

## Usage

1. Create an investigator account or log in.
2. Navigate to "New Analysis" on the Dashboard.
3. Upload a CSV or SQLite file containing smartphone sensor data (`Acc_X`, `Acc_Y`, `Acc_Z`, `Gyro_X`, `Gyro_Y`, `Gyro_Z`).
4. Wait for the AI prediction engine to analyze the traces.
5. Review the visual timeline, prediction summary, and confidence scores.
6. Click "Generate PDF Report" to print or save a forensic summary of the findings.
