# Evaluation

## Project Title

**Solar Flare Forecasting and Nowcasting using Aditya-L1 X-ray Data**

---

# Overview

This document describes the evaluation methodology, performance metrics, validation strategies, and benchmarking procedures used to assess the effectiveness of the proposed solar flare forecasting and nowcasting system.

The primary objective of evaluation is to ensure that the developed models can accurately detect and predict solar flare events while minimizing false alarms and missed high-impact events.

---

# Evaluation Objectives

The evaluation framework aims to:

- Assess prediction accuracy.
- Measure forecasting reliability.
- Quantify false alarm rates.
- Evaluate model generalization capability.
- Compare multiple machine learning architectures.
- Validate operational suitability for space weather forecasting.

---

# Evaluation Workflow

```text
Processed Dataset
        ↓
Train / Validation / Test Split
        ↓
Model Training
        ↓
Prediction Generation
        ↓
Performance Evaluation
        ↓
Model Comparison
        ↓
Best Model Selection
```

---

# Dataset Partitioning

A time-aware dataset split is employed to prevent temporal leakage.

| Dataset | Percentage |
|----------|------------|
| Training | 70% |
| Validation | 15% |
| Testing | 15% |

### Splitting Strategy

```text
Historical Data ─────► Training

Recent Historical Data ─────► Validation

Latest Observations ─────► Testing
```

This ensures that future observations are never used during training.

---

# Validation Strategy

## Time-Series Cross Validation

Traditional random splitting is unsuitable for time-series forecasting.

Therefore, the project adopts:

- Rolling Window Validation
- Expanding Window Validation

Example:

```text
Fold 1:
Train: Jan-Jun
Test : Jul

Fold 2:
Train: Jan-Jul
Test : Aug

Fold 3:
Train: Jan-Aug
Test : Sep
```

---

# Evaluation Metrics

## 1. Accuracy

Measures overall prediction correctness.

Formula:

```text
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

Where:

- TP = True Positives
- TN = True Negatives
- FP = False Positives
- FN = False Negatives

---

## 2. Precision

Measures how many predicted flare events were actually correct.

Formula:

```text
Precision = TP / (TP + FP)
```

High precision reduces false alarms.

---

## 3. Recall (Sensitivity)

Measures the model's ability to identify actual flare events.

Formula:

```text
Recall = TP / (TP + FN)
```

High recall ensures dangerous flares are not missed.

---

## 4. F1-Score

Balances precision and recall.

Formula:

```text
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

---

## 5. ROC-AUC Score

Measures the model's ability to distinguish between flare and non-flare events.

Interpretation:

| ROC-AUC | Performance |
|----------|-------------|
| 0.50 | Random |
| 0.70 - 0.80 | Good |
| 0.80 - 0.90 | Very Good |
| >0.90 | Excellent |

---

# Space Weather Specific Metrics

Since solar flare prediction is a space weather problem, specialized metrics are also employed.

---

## 6. True Skill Statistic (TSS)

Widely used in operational space weather forecasting.

Formula:

```text
TSS = Recall - False Positive Rate
```

Range:

```text
-1 to +1
```

Interpretation:

| TSS Value | Performance |
|------------|-------------|
| <0 | Poor |
| 0 | No Skill |
| 0.5 | Good |
| >0.7 | Excellent |

---

## 7. Heidke Skill Score (HSS)

Measures improvement over random forecasting.

Formula:

```text
HSS = (Observed Accuracy - Random Accuracy)
      / (1 - Random Accuracy)
```

Range:

```text
-∞ to 1
```

Higher values indicate better forecasting skill.

---

# Confusion Matrix Analysis

The confusion matrix provides detailed insight into prediction outcomes.

```text
                Predicted

              No     Flare

Actual No     TN       FP

Actual Flare  FN       TP
```

Interpretation:

- True Positive (TP): Correct flare prediction.
- True Negative (TN): Correct non-flare prediction.
- False Positive (FP): False alarm.
- False Negative (FN): Missed flare event.

Special emphasis is placed on minimizing:

- False Negatives (missed dangerous events).
- False Positives (unnecessary alerts).

---

# Model Comparison

The following models will be evaluated and compared.

| Model | Accuracy | F1 | ROC-AUC | TSS | HSS |
|--------|----------|----|---------|-----|-----|
| Random Forest | - | - | - | - | - |
| XGBoost | - | - | - | - | - |
| LSTM | - | - | - | - | - |
| CNN + LSTM | - | - | - | - | - |
| Transformer | - | - | - | - | - |

The final deployed model will be selected based on overall performance.

---

# Visualization-Based Evaluation

The following visualizations will be generated.

## Training Curves

- Training Loss vs Epochs
- Validation Loss vs Epochs

## Classification Visualizations

- Confusion Matrix
- ROC Curve
- Precision-Recall Curve

## Forecasting Visualizations

- Predicted vs Actual X-ray Flux
- Flare Probability Timeline

---

# Class Imbalance Evaluation

Solar flare datasets are highly imbalanced because M-class and X-class events are rare.

Evaluation strategies include:

- Weighted Metrics
- Macro F1-Score
- Focal Loss Analysis
- Precision-Recall Curves

---

# Robustness Testing

The model will be tested under:

- Noisy observations.
- Missing data scenarios.
- Sensor anomalies.
- Unseen temporal periods.

This ensures operational reliability.

---

# Expected Performance Targets

| Metric | Target |
|---------|--------|
| Accuracy | > 90% |
| Precision | > 85% |
| Recall | > 85% |
| F1-Score | > 85% |
| ROC-AUC | > 0.90 |
| TSS | > 0.70 |
| HSS | > 0.60 |

---

# Final Model Selection Criteria

The production model will be selected based on:

1. Highest validation performance.
2. Lowest false alarm rate.
3. Lowest missed flare rate.
4. Highest TSS and HSS.
5. Fast inference time.
6. Generalization capability.

---

# Evaluation Summary

The proposed evaluation framework combines conventional machine learning metrics with specialized space weather forecasting metrics to comprehensively assess the accuracy, reliability, and operational readiness of the solar flare forecasting system.