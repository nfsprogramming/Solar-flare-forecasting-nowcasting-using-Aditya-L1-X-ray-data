# Dataset Documentation

## Project Title

**Solar Flare Forecasting and Nowcasting using Aditya-L1 X-ray Data**

---

# Overview

This project utilizes solar X-ray observations and historical solar flare records to train Artificial Intelligence models capable of performing real-time solar flare nowcasting and forecasting.

The dataset consists of time-series measurements of solar X-ray flux along with corresponding flare event labels.

---

# Dataset Sources

## Primary Dataset

### Aditya-L1 Solar X-ray Observations

The primary data source for this project is X-ray observations obtained from the Aditya-L1 mission.

These observations provide continuous measurements of solar X-ray flux, which are critical indicators of solar flare activity.

### Parameters

- Observation Timestamp
- X-ray Flux Intensity
- Energy Band Information
- Observation Metadata

---

## Supplementary Datasets

Due to the limited availability of publicly accessible long-duration Aditya-L1 historical data, additional datasets are incorporated for model training and benchmarking.

### GOES X-ray Flux Dataset

The Geostationary Operational Environmental Satellite (GOES) mission provides long-term solar X-ray observations widely used by the space weather community.

Dataset characteristics:

- Continuous X-ray flux measurements.
- Multiple decades of historical observations.
- High temporal resolution.

---

### Historical Solar Flare Catalog

Historical flare event catalogs are used to obtain ground-truth labels.

Each event record contains:

- Flare start time
- Peak time
- End time
- Flare class
- Event location (if available)

---

# Dataset Structure

## X-ray Flux Dataset

| Feature Name | Data Type | Description |
|-------------|------------|-------------|
| timestamp | DateTime | Observation time |
| xrsa_flux | Float | Short wavelength X-ray flux |
| xrsb_flux | Float | Long wavelength X-ray flux |
| quality_flag | Integer | Observation quality indicator |

---

## Flare Event Dataset

| Feature Name | Data Type | Description |
|-------------|------------|-------------|
| event_id | String | Unique flare identifier |
| start_time | DateTime | Flare start time |
| peak_time | DateTime | Flare peak time |
| end_time | DateTime | Flare end time |
| flare_class | String | A/B/C/M/X |
| intensity | Float | Peak intensity |

---

# Data Format

Supported formats:

```text id="fmt001"
CSV
NetCDF
FITS
JSON
```

Example:

```csv id="csv001"
timestamp,xrsa_flux,xrsb_flux
2024-01-01 00:00:00,1.2e-7,3.5e-7
2024-01-01 00:01:00,1.3e-7,3.6e-7
2024-01-01 00:02:00,1.5e-7,3.9e-7
```

---

# Data Collection Workflow

```text id="wf001"
Aditya-L1 Observations
            +
GOES X-ray Data
            +
Historical Flare Catalogs
            |
            ▼
Central Dataset Repository
            |
            ▼
Preprocessing Pipeline
```

---

# Dataset Statistics

The final dataset will contain:

- Historical solar X-ray observations.
- Corresponding flare event labels.
- Time-windowed sequences for model training.

Expected characteristics:

| Attribute | Value |
|-----------|-------|
| Temporal Resolution | 1 minute |
| Observation Type | Time Series |
| Prediction Task | Classification + Forecasting |
| Sequence Length | 30–120 minutes |
| Target Classes | No Flare, C, M, X |

---

# Data Preprocessing

The following preprocessing steps are performed.

## Missing Value Handling

Missing observations are handled using:

- Linear interpolation
- Forward filling
- Backward filling

---

## Noise Removal

Noise reduction techniques include:

- Moving Average Filtering
- Smoothing Operations

---

## Normalization

Features are normalized using:

```text id="norm001"
Min-Max Scaling

or

Z-score Standardization
```

---

## Time Window Generation

Time-series sequences are generated using sliding windows.

Example:

```text id="window001"
Input:
Previous 60 minutes of X-ray flux

Output:
Probability of flare in next 60 minutes
```

---

# Label Generation

Training labels are generated from historical flare catalogs.

Example:

| Observation Window | Target Label |
|-------------------|--------------|
| No Event | No Flare |
| C-class Event | C |
| M-class Event | M |
| X-class Event | X |

---

# Train-Test Split

Recommended split:

| Dataset Partition | Percentage |
|-------------------|------------|
| Training | 70% |
| Validation | 15% |
| Testing | 15% |

Time-aware splitting is adopted to prevent temporal leakage.

```text id="split001"
Past Data → Training

Recent Data → Validation

Latest Data → Testing
```

---

# Data Challenges

## Class Imbalance

Extreme events such as X-class flares are rare.

Mitigation techniques:

- Weighted loss functions
- Oversampling
- Focal Loss

---

## Missing Observations

Occasional sensor gaps may occur.

Solutions:

- Interpolation
- Data quality filtering

---

## Noise and Outliers

Solar observations can contain spikes and anomalies.

Solutions:

- Smoothing filters
- Outlier detection

---

# Dataset Storage Structure

```text id="storage001"
datasets/
│
├── raw/
│   ├── aditya_l1/
│   ├── goes/
│   └── flare_catalogs/
│
├── processed/
│
├── features/
│
└── labels/
```

---

# Ethical and Scientific Considerations

- All datasets used are publicly available scientific observations.
- Proper attribution will be provided to respective data providers.
- No personally identifiable information (PII) is involved.

---

# Expected Dataset Outcome

The final processed dataset will provide high-quality, time-aligned solar X-ray sequences suitable for training advanced machine learning models for solar flare forecasting and nowcasting.

---

# Dataset Summary

The dataset integrates Aditya-L1 observations, historical solar flare catalogs, and supplementary space weather datasets to create a comprehensive foundation for AI-driven solar flare prediction.