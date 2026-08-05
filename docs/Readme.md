# 🌞 Solar Flare Forecasting and Nowcasting using Aditya-L1 X-ray Data

> An AI-powered Space Weather Intelligence Platform for real-time solar flare detection, forecasting, and early warning generation using Aditya-L1 X-ray observations.

---

## 🚀 Overview

Solar flares are sudden bursts of electromagnetic radiation released from the Sun that can significantly impact satellites, GPS systems, radio communications, and terrestrial power infrastructure.

This project aims to develop an intelligent early warning system capable of:

- Detecting ongoing solar flares (**Nowcasting**)
- Predicting future solar flare events (**Forecasting**)
- Estimating flare severity levels
- Assessing risk to space assets
- Providing actionable alerts for space weather operations

The system leverages Artificial Intelligence and Machine Learning techniques on solar X-ray observations obtained from ISRO's Aditya-L1 mission.

---

## 🎯 Problem Statement

Develop an AI-driven framework capable of analyzing Aditya-L1 X-ray flux observations to:

- Predict imminent solar flare events.
- Classify flare intensity levels.
- Generate early warnings for high-impact space weather events.
- Assist in safeguarding satellite infrastructure and communication systems.

---

## ✨ Key Features

### 🌞 Solar Flare Nowcasting

Detect ongoing solar flare activity in real time.

### 🔮 Solar Flare Forecasting

Predict future flare occurrences for multiple forecasting horizons.

### ⚠️ Early Warning System

Generate intelligent alerts for potentially hazardous events.

### 📊 Interactive Dashboard

Visualize historical and real-time solar activity.

### 🛰️ Space Weather Risk Assessment

Estimate operational risk levels for space-based assets.

### 🧠 Explainable AI

Provide interpretable predictions using SHAP-based explanations.

---

## 🏗️ System Architecture

```text
Aditya-L1 X-ray Data
            │
            ▼
Data Acquisition Layer
            │
            ▼
Data Preprocessing Layer
            │
            ▼
Feature Engineering Layer
            │
            ▼
AI Prediction Engine
(LSTM / Transformer)
            │
            ▼
Flare Classification
            │
            ▼
Risk Assessment Engine
            │
            ▼
Alert Generation System
            │
            ▼
Interactive Dashboard
```

---

## 🛠️ Technology Stack

### Artificial Intelligence

- PyTorch
- Scikit-learn
- XGBoost
- SHAP

### Data Processing

- Pandas
- NumPy
- SciPy
- PyWavelets

### Backend

- FastAPI

### Frontend

- React.js
- Tailwind CSS

### Visualization

- Plotly
- Matplotlib

### Deployment

- Docker
- GitHub Actions

---

## 📂 Project Structure

```bash
.
├── backend/
├── frontend/
├── models/
├── notebooks/
├── datasets/
├── docs/
│
├── README.md
├── VISION.md
├── ROADMAP.md
├── TECHSTACK.md
├── DATASET.md
├── METHODOLOGY.md
├── ARCHITECTURE.md
├── MODEL_DOCUMENTATION.md
├── EVALUATION.md
└── LICENSE
```

---

## 📈 Machine Learning Pipeline

### Data Collection

- Aditya-L1 X-ray observations
- Historical solar flare catalogues

### Data Preprocessing

- Missing value handling
- Normalization
- Time-window generation

### Feature Engineering

- Statistical features
- Temporal features
- Frequency-domain features

### Model Development

Baseline Models:

- Random Forest
- XGBoost

Deep Learning Models:

- LSTM
- CNN + LSTM
- Transformer

---

## 📊 Evaluation Metrics

The models will be evaluated using:

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- True Skill Statistic (TSS)
- Heidke Skill Score (HSS)

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/your-username/solar-flare-forecasting.git
cd solar-flare-forecasting
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### Start Backend

```bash
cd backend
uvicorn app:app --reload
```

### Start Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 📌 Future Scope

- Real-time Aditya-L1 telemetry integration.
- Coronal Mass Ejection (CME) prediction.
- Solar Energetic Particle forecasting.
- Multi-modal space weather intelligence.
- Autonomous advisory system for satellite operations.

---

## 🌍 Expected Impact

- Enhance space weather preparedness.
- Improve satellite mission resilience.
- Support uninterrupted communication services.
- Contribute to AI-driven heliophysics research.

---

## 👥 Team

| Name | Role |
|-------|------|
| Team Member 1 | Machine Learning Engineer |
| Team Member 2 | Backend Developer |
| Team Member 3 | Frontend Developer |
| Team Member 4 | Data Engineer |

---

## 📜 License

This project is released under the MIT License.

---

## 🙏 Acknowledgements

- ISRO Aditya-L1 Mission
- Space Weather Research Community
- Open-source scientific computing ecosystem

---

**"Empowering Space Weather Intelligence through Artificial Intelligence."**