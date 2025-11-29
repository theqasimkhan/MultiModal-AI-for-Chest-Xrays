import json
from chest_xray_cv_model import ChestXRayClassifier
from nlp_report_generator import MedicalReportGenerator

class MultimodalChestXRayAnalyzer:
    """
    Integration layer that combines Computer Vision and NLP modules
    for comprehensive chest X-ray analysis
    """
    
    def __init__(self, cv_model_path=None, nlp_model_name="google/flan-t5-base"):
        """
        Initialize the multimodal analyzer
        
        Args:
            cv_model_path (str): Path to pre-trained CV model weights
            nlp_model_name (str): Name of the pre-trained NLP model
        """
        # Initialize CV module
        self.cv_model = ChestXRayClassifier(model_path=cv_model_path)
        
        # Initialize NLP module
        self.nlp_model = MedicalReportGenerator(model_name=nlp_model_name)
        
    def analyze(self, image_path, clinical_indication="Routine examination", date="Today"):
        """
        Perform complete analysis of a chest X-ray image
        
        Args:
            image_path (str): Path to the chest X-ray image
            clinical_indication (str): Reason for the examination
            date (str): Date of examination
            
        Returns:
            dict: Complete analysis results including predictions and report
        """
        # Step 1: Computer Vision analysis
        print("Performing Computer Vision analysis...")
        cv_predictions = self.cv_model.predict(image_path)
        
        # Step 2: Generate heatmap (optional visualization)
        # heatmap = self.cv_model.generate_heatmap(image_path, 0)  # For first pathology
        
        # Step 3: NLP report generation
        print("Generating medical report...")
        report = self.nlp_model.generate_report(
            predictions=cv_predictions,
            clinical_indication=clinical_indication,
            date=date
        )
        
        # Step 4: Format results
        results = {
            "image_path": image_path,
            "analysis_date": date,
            "clinical_indication": clinical_indication,
            "cv_findings": cv_predictions,
            "medical_report": report,
            "status": "success"
        }
        
        return results
    
    def answer_question(self, question, image_path):
        """
        Answer a clinical question about a chest X-ray image
        
        Args:
            question (str): Clinical question
            image_path (str): Path to the chest X-ray image
            
        Returns:
            str: Answer to the question
        """
        # First get CV predictions
        cv_predictions = self.cv_model.predict(image_path)
        
        # Then use NLP model to answer question
        answer = self.nlp_model.answer_question(question, cv_predictions)
        
        return answer
    
    def get_structured_findings(self, image_path):
        """
        Get structured findings from CV analysis
        
        Args:
            image_path (str): Path to the chest X-ray image
            
        Returns:
            dict: Structured findings
        """
        return self.cv_model.predict(image_path)

# Example usage and API endpoints
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os

import database

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

analyzer = MultimodalChestXRayAnalyzer()

@app.route('/', methods=['GET'])
def index():
    """
    Web interface for uploading and analyzing X-rays
    """
    return render_template('index.html')

@app.route('/upload_and_analyze', methods=['POST'])
def upload_and_analyze():
    """
    API endpoint for uploading and analyzing chest X-rays via web interface
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get form data
        clinical_indication = request.form.get('clinical_indication', 'Routine examination')
        date = request.form.get('date', 'Today')
        patient_name = request.form.get('patient_name', 'Anonymous')
        
        # Perform analysis
        results = analyzer.analyze(filepath, clinical_indication, date)
        
        # Save to database
        database.save_report(
            patient_name=patient_name,
            exam_date=date,
            image_path=filepath,
            clinical_indication=clinical_indication,
            findings=json.dumps(results['cv_findings']),
            report_text=results['medical_report'],
            structured_data=results
        )
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    """
    API endpoint to get past reports
    """
    query = request.args.get('q')
    reports = database.get_reports(query)
    return jsonify({"reports": reports}), 200

@app.route('/api', methods=['GET'])
def api_info():
    """
    API documentation endpoint
    """
    return jsonify({
        "message": "Welcome to the Multimodal Chest X-Ray Analyzer API",
        "status": "online",
        "endpoints": {
            "web_interface": "GET /",
            "upload_and_analyze": "POST /upload_and_analyze",
            "history": "GET /history",
            "analyze": "POST /analyze",
            "question": "POST /question",
            "findings": "POST /findings"
        }
    }), 200

@app.route('/analyze', methods=['POST'])
def analyze_xray():
    """
    API endpoint for chest X-ray analysis
    Expected JSON: {"image_path": "path/to/image.jpg", "clinical_indication": "reason", "date": "YYYY-MM-DD"}
    """
    try:
        # Get request data
        data = request.get_json()
        image_path = data.get('image_path')
        clinical_indication = data.get('clinical_indication', 'Routine examination')
        date = data.get('date', 'Today')
        
        # Validate image path
        if not image_path or not os.path.exists(image_path):
            return jsonify({"error": "Invalid image path"}), 400
        
        # Perform analysis
        results = analyzer.analyze(image_path, clinical_indication, date)
        
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/question', methods=['POST'])
def answer_question():
    """
    API endpoint for answering clinical questions
    Expected JSON: {"question": "What does...", "image_path": "path/to/image.jpg"}
    """
    try:
        # Get request data
        data = request.get_json()
        question = data.get('question')
        image_path = data.get('image_path')
        
        # Validate inputs
        if not question or not image_path:
            return jsonify({"error": "Missing question or image_path"}), 400
            
        if not os.path.exists(image_path):
            return jsonify({"error": "Invalid image path"}), 400
        
        # Answer question
        answer = analyzer.answer_question(question, image_path)
        
        return jsonify({"question": question, "answer": answer}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/findings', methods=['POST'])
def get_findings():
    """
    API endpoint for getting structured findings
    Expected JSON: {"image_path": "path/to/image.jpg"}
    """
    try:
        # Get request data
        data = request.get_json()
        image_path = data.get('image_path')
        
        # Validate image path
        if not image_path or not os.path.exists(image_path):
            return jsonify({"error": "Invalid image path"}), 400
        
        # Get findings
        findings = analyzer.get_structured_findings(image_path)
        
        return jsonify({"image_path": image_path, "findings": findings}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Example direct usage
    print("Multimodal Chest X-Ray Analyzer")
    print("=" * 40)
    
    # Note: You would need to provide actual image paths for real usage
    # example_image_path = "path/to/chest_xray.jpg"
    # results = analyzer.analyze(example_image_path, "Fever and cough", "2023-06-15")
    # print(json.dumps(results, indent=2))
    
    # Run Flask API
    print("Starting API server...")
    app.run(host='0.0.0.0', port=5001, debug=True)