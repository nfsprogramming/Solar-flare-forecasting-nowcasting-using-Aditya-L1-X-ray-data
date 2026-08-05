import os
import pandas as pd
import numpy as np

def generate_sequences(df, feature_cols, target_col, window_size=60, forecast_horizon=10):
    """
    Generates sliding window sequences.
    window_size: Number of past time steps to look at.
    forecast_horizon: How far in the future to predict (e.g., 10 time steps ahead).
    """
    print(f"Generating sequences (Window: {window_size}, Horizon: {forecast_horizon})...")
    
    X, y = [], []
    data_features = df[feature_cols].values
    data_targets = df[target_col].values
    
    for i in range(len(df) - window_size - forecast_horizon):
        # The input window
        X.append(data_features[i : i + window_size])
        
        # The target label is 1 if any flare occurs within the forecast horizon
        horizon_labels = data_targets[i + window_size : i + window_size + forecast_horizon]
        has_flare = 1 if np.sum(horizon_labels) > 0 else 0
        y.append(has_flare)
        
    X = np.array(X)
    y = np.array(y)
    
    print(f"Generated X shape: {X.shape}")
    print(f"Generated y shape: {y.shape}")
    print(f"Class balance: {np.sum(y)} flares, {len(y) - np.sum(y)} non-flares")
    
    return X, y

if __name__ == '__main__':
    data_path = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\datasets\processed\sample_labeled.csv"
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        
        # Features: Normalized Flux, Statistical Error
        # Target: is_flare
        X, y = generate_sequences(df, feature_cols=['CTR_NORM', 'STAT_ERR'], target_col='is_flare')
        
        # Save sequences
        np.save(r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\datasets\processed\X_sample.npy", X)
        np.save(r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\datasets\processed\y_sample.npy", y)
        print("Successfully saved sequences to .npy files.")
    else:
        print(f"Error: {data_path} not found. Run labeling.py first.")
