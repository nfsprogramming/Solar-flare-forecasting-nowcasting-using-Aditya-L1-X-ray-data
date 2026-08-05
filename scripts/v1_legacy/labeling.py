import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def label_flares(df, column='CTR_NORM', prominence=0.05, distance=100):
    """
    Labels flares using peak detection on the normalized flux.
    """
    print(f"Detecting peaks on {column}...")
    flux = df[column].values
    
    # Detect peaks based on prominence (height above surrounding baseline)
    peaks, properties = find_peaks(flux, prominence=prominence, distance=distance)
    
    # Initialize binary label column
    df['is_flare'] = 0
    
    # Mark the peaks and their immediate surroundings (e.g. +/- 10 points) as active flares
    flare_window = 15
    for p in peaks:
        start = max(0, p - flare_window)
        end = min(len(df), p + flare_window)
        df.loc[start:end, 'is_flare'] = 1
        
    print(f"Detected {len(peaks)} flare peaks.")
    return df, peaks

def plot_labeled_data(df, peaks, save_path):
    plt.figure(figsize=(15, 6))
    
    plt.plot(df.index, df['CTR_NORM'], label='Normalized Flux', color='blue', alpha=0.7)
    
    # Highlight labeled flare regions
    flare_regions = df[df['is_flare'] == 1]
    plt.scatter(flare_regions.index, flare_regions['CTR_NORM'], color='red', label='Labeled Flare Region', s=10)
    
    # Plot exact peaks
    plt.plot(peaks, df['CTR_NORM'].iloc[peaks], "x", color='black', markersize=12, label='Detected Peak')
    
    plt.title('Automatic Flare Labeling via Peak Detection')
    plt.xlabel('Time Step')
    plt.ylabel('Normalized X-ray Flux')
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"Saved labeled plot to {save_path}")

if __name__ == '__main__':
    data_path = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\datasets\processed\sample_cleaned.csv"
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        df_labeled, peaks = label_flares(df)
        
        # Save labeled data
        out_path = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\datasets\processed\sample_labeled.csv"
        df_labeled.to_csv(out_path, index=False)
        print(f"Saved labeled data to {out_path}")
        
        # Plot
        artifact_dir = r"C:\Users\NFS Photographer\.gemini\antigravity-ide\brain\79d3e34d-4b55-4524-a972-89a9161d8826"
        plot_path = os.path.join(artifact_dir, "flare_labels.png")
        plot_labeled_data(df_labeled, peaks, plot_path)
    else:
        print(f"Error: {data_path} not found. Run data_preprocessing.py first.")
