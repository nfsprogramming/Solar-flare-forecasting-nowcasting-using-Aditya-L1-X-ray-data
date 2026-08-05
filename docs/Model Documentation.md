# Model Documentation

## Project Title

**Solar Flare Forecasting and Nowcasting using Aditya-L1 X-ray Data**

---

# Overview

This document describes the Machine Learning and Deep Learning models used in the proposed solar flare forecasting and nowcasting system.

The primary objective of these models is to analyze historical and real-time solar X-ray observations to predict the occurrence and severity of future solar flare events.

The modeling framework consists of:

1. Baseline Machine Learning Models
2. Deep Learning Models
3. Advanced Sequence Modeling Architectures

---

# Prediction Tasks

The system addresses the following prediction tasks.

| Task | Type |
|-------|------|
| Flare Occurrence Prediction | Binary Classification |
| Flare Severity Prediction | Multi-Class Classification |
| Future X-ray Flux Estimation | Regression |
| Risk Assessment | Classification |

---

# Problem Formulation

## Binary Classification

Predict whether a significant solar flare (M/X class) will occur within a future prediction window.

### Classes

| Label | Description |
|--------|-------------|
| 0 | No Significant Flare |
| 1 | Significant Flare (M/X) |

---

## Multi-Class Classification

Predict the severity class of the upcoming flare.

| Label | Flare Class |
|--------|-------------|
| 0 | No Flare |
| 1 | C-Class |
| 2 | M-Class |
| 3 | X-Class |

---

# Input Data

The models utilize time-series observations derived from:

- Aditya-L1 X-ray observations
- GOES X-ray flux data (for supplementary training)
- Historical solar flare catalogs

## Input Features

| Feature | Description |
|----------|-------------|
| Timestamp | Observation time |
| XRSA Flux | Short wavelength X-ray flux |
| XRSB Flux | Long wavelength X-ray flux |
| Moving Average | Smoothed flux trend |
| Flux Gradient | Rate of change |
| Variance | Flux variability |

---

# Baseline Models

Baseline models establish benchmark performance.

---

## Random Forest

### Purpose

Provide interpretable baseline classification performance.

### Advantages

- Handles nonlinear relationships.
- Robust against overfitting.
- Generates feature importance scores.

### Hyperparameters

```yaml
n_estimators: 200
max_depth: 20
min_samples_split: 5
criterion: gini
```

---

## XGBoost

### Purpose

Provide strong tabular data performance.

### Advantages

- High predictive accuracy.
- Handles class imbalance effectively.
- Fast inference.

### Hyperparameters

```yaml
n_estimators: 300
learning_rate: 0.05
max_depth: 8
subsample: 0.8
colsample_bytree: 0.8
```

---

# Primary Deep Learning Model

# Long Short-Term Memory (LSTM)

## Motivation

Solar X-ray measurements are sequential in nature. LSTMs are capable of learning temporal dependencies and identifying precursor patterns associated with solar flares.

---

## LSTM Architecture

```text
Input Sequence
        ↓
LSTM Layer (128 Units)
        ↓
Dropout (0.3)
        ↓
LSTM Layer (64 Units)
        ↓
Dropout (0.3)
        ↓
Dense Layer (32 Units)
        ↓
Output Layer
```

---

## Layer Configuration

| Layer | Configuration |
|--------|--------------|
| Input Layer | Sequence × Features |
| LSTM Layer 1 | 128 Units |
| Dropout | 0.3 |
| LSTM Layer 2 | 64 Units |
| Dropout | 0.3 |
| Dense Layer | 32 Units |
| Output Layer | Sigmoid / Softmax |

---

## Input Shape

Example:

```text
Batch Size × Sequence Length × Features

32 × 60 × 6
```

Where:

- Batch Size = 32
- Sequence Length = 60 minutes
- Features = 6

---

# Output Layer

## Binary Classification

```text
1 Neuron + Sigmoid Activation
```

Output:

```text
Probability of Significant Flare
```

---

## Multi-Class Classification

```text
4 Neurons + Softmax Activation
```

Output:

```text
No Flare
C-Class
M-Class
X-Class
```

---

# CNN + LSTM Hybrid Model

## Motivation

CNN layers extract local temporal patterns while LSTM layers capture long-term dependencies.

---

## Architecture

```text
Input Sequence
        ↓
1D Convolution Layer
        ↓
Max Pooling Layer
        ↓
LSTM Layer
        ↓
Dense Layer
        ↓
Output Layer
```

---

## Advantages

- Captures local signal characteristics.
- Reduces noise sensitivity.
- Improves predictive performance.

---

# Transformer Model (Advanced)

## Motivation

Transformers effectively model long-range dependencies and allow parallel computation.

---

## Architecture

```text
Input Sequence
        ↓
Positional Encoding
        ↓
Transformer Encoder
        ↓
Global Average Pooling
        ↓
Dense Layer
        ↓
Output Layer
```

---

# Training Configuration

## Optimizer

```yaml
optimizer: Adam
learning_rate: 0.001
```

---

## Loss Functions

### Binary Classification

```yaml
loss: Binary Cross Entropy
```

### Multi-Class Classification

```yaml
loss: Categorical Cross Entropy
```

### Imbalanced Data

```yaml
loss: Focal Loss
```

---

## Batch Size

```yaml
batch_size: 32
```

---

## Epochs

```yaml
epochs: 100
```

---

## Early Stopping

```yaml
patience: 10
monitor: validation_loss
```

---

# Hyperparameter Tuning

Techniques used:

- Grid Search
- Random Search
- Bayesian Optimization

Parameters tuned:

- Learning Rate
- Hidden Units
- Sequence Length
- Batch Size
- Dropout Rate

---

# Dataset Split Strategy

Time-aware splitting is used.

| Dataset | Percentage |
|----------|------------|
| Training | 70% |
| Validation | 15% |
| Testing | 15% |

This prevents temporal data leakage.

---

# Evaluation Metrics

## General Metrics

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC

## Space Weather Metrics

- True Skill Statistic (TSS)
- Heidke Skill Score (HSS)

---

# Explainable AI

## SHAP

SHAP is used to explain model predictions and identify important features.

Example important features:

```text
1. X-ray Flux Gradient
2. Peak Flux
3. Moving Average
4. Flux Variance
```

Benefits:

- Improves transparency.
- Supports scientific interpretation.
- Builds user trust.

---

# Model Selection Criteria

The final model is selected based on:

1. Highest validation performance.
2. Lowest false alarm rate.
3. Highest TSS and HSS scores.
4. Fast inference time.
5. Good generalization capability.

---

# Expected Performance Targets

| Metric | Target |
|---------|--------|
| Accuracy | >90% |
| Precision | >85% |
| Recall | >85% |
| F1-Score | >85% |
| ROC-AUC | >0.90 |
| TSS | >0.70 |

---

# Model Deployment

The trained model will be exported in:

```text
PyTorch (.pt)
ONNX (.onnx)
```

The inference service will be deployed through a FastAPI backend for real-time predictions.

---

# Final Prediction Pipeline

```text
Solar X-ray Data
        ↓
Preprocessing
        ↓
Feature Engineering
        ↓
Sequence Generation
        ↓
LSTM / Transformer
        ↓
Flare Prediction
        ↓
Risk Assessment
        ↓
Alert Generation
```

---

# Summary

The proposed modeling framework integrates classical machine learning and advanced deep learning architectures to provide accurate, interpretable, and operationally useful solar flare forecasting and nowcasting capabilities for space weather applications.