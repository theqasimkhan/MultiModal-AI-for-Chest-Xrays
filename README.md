# 🏥 Multimodal AI for Chest X-ray Analysis

An intelligent medical imaging system that combines **Computer Vision** and **Natural Language Processing** to automate chest X-ray analysis and generate professional radiological reports.

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

- **🔍 AI-Powered Pathology Detection**: Detects 5 critical conditions (Pneumonia, Tuberculosis, Pleural Effusion, Pneumothorax, Congestive Heart Failure) with high precision
- **📝 Automated Report Generation**: Creates professional medical reports using advanced NLP
- **💬 Interactive Q&A**: Ask questions about X-ray findings and get instant AI-powered answers
- **📊 Patient History Management**: SQLite database for tracking and searching past reports
- **🎨 Modern Web Interface**: Beautiful, responsive UI with real-time animations
- **⚡ Fast & Accurate**: Optimized inference with DenseNet-121 and Flan-T5

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/multimodal-chest-xray-ai.git
cd multimodal-chest-xray-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python multimodal_integration.py
```

4. Open your browser and navigate to:
```
http://localhost:5001
```

## 💻 Usage

1. **Upload X-ray**: Click or drag-and-drop a chest X-ray image (PNG, JPG, DICOM)
2. **Fill Details**: Enter patient name, date, and clinical indication
3. **Generate Report**: Click "Generate Report" to start AI analysis
4. **Review Results**: View detected pathologies, confidence scores, and full medical report
5. **Ask Questions**: Use the Q&A interface to get specific insights
6. **Browse History**: Switch to the "History" tab to view past reports

## 🏗️ Architecture

```
┌─────────────────┐
│   Web Browser   │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│  Flask Server   │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│  CV   │ │  NLP  │
│DenseNet│ │Flan-T5│
└───────┘ └───────┘
```

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask (Python) |
| **Computer Vision** | PyTorch, DenseNet-121 |
| **NLP** | Hugging Face Transformers, Flan-T5 |
| **Database** | SQLite |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Image Processing** | OpenCV, PIL |

## 📁 Project Structure

```
multimodal-chest-xray-ai/
├── chest_xray_cv_model.py       # Computer Vision module
├── nlp_report_generator.py      # NLP report generation
├── multimodal_integration.py    # Flask server & API
├── database.py                  # Database operations
├── templates/
│   └── index.html              # Web interface
├── static/
│   ├── css/style.css           # Styling
│   └── js/main.js              # Frontend logic
├── requirements.txt            # Dependencies
└── PROJECT_DOCUMENTATION.md    # Detailed docs
```

## 🎯 Key Capabilities

### Detected Conditions
1. **Pneumonia** - Lung infection/inflammation
2. **Tuberculosis** - Bacterial lung infection
3. **Pleural Effusion** - Fluid buildup around lungs
4. **Pneumothorax** - Collapsed lung
5. **Congestive Heart Failure** - Heart pumping inefficiency

### Report Sections
- Patient Information
- Clinical Indication
- Findings & Observations
- Impression & Diagnosis
- Recommendations

## 🔬 Model Details

- **Vision Model**: DenseNet-121 pre-trained on ImageNet, fine-tuned for chest pathologies
- **NLP Model**: Google Flan-T5 Base (248M parameters)
- **Inference Time**: ~2-3 seconds per image
- **Accuracy**: High precision with ambiguity reduction logic

## 📸 Screenshots

<img width="1670" height="857" alt="image" src="https://github.com/user-attachments/assets/685dbb1d-bac5-440d-a224-b9cd9c37f5d4" />

<img width="1666" height="844" alt="image" src="https://github.com/user-attachments/assets/2ef6fed0-b6a0-4ddf-b22b-0a8c7e561cea" />


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This system is designed for **educational and research purposes only**. It should not be used as the sole basis for clinical decision-making. Always consult qualified healthcare professionals for medical diagnoses.

## 📧 Contact

For questions or feedback, do contact me on my qasimkhankbt@gmail.com.

---

**Made with ❤️ for advancing medical AI**

