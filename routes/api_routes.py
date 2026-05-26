from flask import Blueprint, request, jsonify, current_app, render_template
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from utils.predict import process_and_predict

api_bp = Blueprint('api', __name__)

ALLOWED_EXTENSIONS = {'csv', 'sqlite'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.root_path, 'datasets')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Run prediction
        result = process_and_predict(filepath)
        
        return jsonify(result)
        
    return jsonify({'error': 'Invalid file type'})

@api_bp.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    return render_template('report.html', 
                           date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           filename=data.get('filename', 'Unknown_Trace.csv'),
                           summary=data.get('summary', {}),
                           timeline=data.get('timeline', []))
