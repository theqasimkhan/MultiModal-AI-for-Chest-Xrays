# Multimodal AI for Chest X-ray Analysis - Project Documentation

## 1. Project Overview
This project is a comprehensive **Multimodal AI System** designed to assist medical professionals in analyzing chest X-ray images. It combines **Computer Vision (CV)** for pathology detection with **Natural Language Processing (NLP)** for generating professional medical reports and answering clinical questions.

The system features a modern, responsive web interface that allows users to upload X-rays, view detailed analysis, track patient history, and interact with the AI assistant.

## 2. Key Features

### 🔍 Advanced Pathology Detection
- **Focused Analysis**: The system is specialized to detect **5 critical conditions** with high precision:
    1.  **Pneumonia**
    2.  **Tuberculosis**
    3.  **Pleural Effusion**
    4.  **Pneumothorax**
    5.  **Congestive Heart Failure**
- **Ambiguity Reduction**: Implements smart thresholding logic to provide decisive "High" or "Low" confidence results, minimizing ambiguous outputs.

### 📝 Automated Report Generation
- Generates professional, structured radiological reports.
- Sections include: **Patient Information**, **Clinical Indication**, **Findings**, **Impression**, and **Recommendations**.
- Uses Generative AI to produce natural, context-aware descriptions rather than simple templates.

### 💬 Interactive Clinical Q&A
- Users can ask specific questions about the X-ray (e.g., "Is there any sign of fluid?").
- The AI answers based on the visual findings and its medical knowledge base.

### 📂 Patient History & Search
- **Database Integration**: All reports are automatically saved to a local SQLite database.
- **Searchable History**: Users can browse past reports and search by patient name or date via the "History" tab.
- **Instant Retrieval**: Click on any history item to instantly reload the full report and findings.

### 🎨 Modern User Interface
- **Premium Design**: Clean, medical-grade aesthetic with smooth animations and responsive layout.
- **Real-time Feedback**: Loading states, scanning animations, and dynamic result rendering.
- **Dual-View**: Split-screen layout showing the report and the X-ray side-by-side.

## 3. System Architecture

The project follows a modular architecture:


graph TD
    User[User / Web Browser] <-->|HTTP Requests| Flask[Flask Backend Server]
    subgraph "Backend Core"
        Flask <-->|Manage Data| DB[(SQLite Database)]
        Flask -->|Image| CV[CV Module (DenseNet121)]
        Flask -->|Context| NLP[NLP Module (Flan-T5)]
        CV -->|Predictions| NLP
        CV -->|Structured Findings| Flask
        NLP -->|Generated Report| Flask
        NLP -->|QA Answers| Flask
    end
    

## 4. Technical Methodology

### Computer Vision (CV) Module
- **Model**: **DenseNet-121**, pre-trained on ImageNet and adapted for chest X-ray analysis.
- **Logic**:
    - Input images are resized to 224x224 and normalized.
    - The model predicts probabilities for 14 common pathologies.
    - **Post-Processing**: A custom mapping layer filters these down to the 5 target diseases. For example, 'Infiltration' is used as a proxy for Tuberculosis indicators, and 'Cardiomegaly' for Heart Failure.
    - **Smart Filtering**: Probabilities are processed through a non-linear function to boost high-confidence detections (>60%) and suppress noise (<20%).

### Natural Language Processing (NLP) Module
- **Model**: **Google's Flan-T5 Base** (Encoder-Decoder Transformer).
- **Report Generation**:
    - Constructs a dynamic prompt containing the clinical indication and the CV detected findings.
    - The model generates a coherent, grammatically correct medical report.
- **Question Answering**:
    - Context-aware prompting allows the model to answer user queries by combining the visual findings with general medical knowledge.

### Backend & Database
- **Framework**: **Flask** (Python) serves as the API and web server.
- **Storage**: **SQLite** (`medical_reports.db`) stores patient metadata, analysis results, and file paths.
- **API Design**: RESTful endpoints for upload (`/upload_and_analyze`), history (`/history`), and Q&A (`/question`).

### Frontend
- **Tech Stack**: HTML5, CSS3 (Custom properties, Flexbox/Grid), JavaScript (Vanilla ES6+).
- **Design System**: Custom color palette (Medical Blue, Slate, Emerald) and typography (Inter, Merriweather).

## 5. Workflow

1.  **Upload**: User selects a Chest X-ray image (DICOM/PNG/JPG) and enters patient details.
2.  **Processing**:
    - Image is sent to the CV model for feature extraction and classification.
    - Detected pathologies are sent to the NLP model.
3.  **Generation**: NLP model drafts the full text report.
4.  **Storage**: Image path and all generated data are saved to the database.
5.  **Display**: Results are streamed back to the UI, displaying the probability bars and typing out the report.
6.  **Interaction**: User can ask follow-up questions or navigate to the History tab to view previous cases.

## 6. Setup & Usage

### Prerequisites
- Python 3.8+
- PyTorch, Transformers, Flask, OpenCV

### Installation
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
python multimodal_integration.py
```
Access the interface at `http://localhost:5001`.
