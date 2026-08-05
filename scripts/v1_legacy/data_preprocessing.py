import os
import pandas as pd
import numpy as np
from astropy.io import fits
from sklearn.preprocessing import MinMaxScaler

def preprocess_fits_to_dataframe(fits_path, hdu_index=5):
    """
    Reads a HEL1OS lightcurve FITS file and returns a preprocessed Pandas DataFrame.
    """
    print(f"Reading {fits_path} (HDU {hdu_index})...")
    with fits.open(fits_path) as hdul:
        data = hdul[hdu_index].data
        
    df = pd.DataFrame({
        'MJD': data['MJD'].astype(float),
        'CTR': data['CTR'].astype(float),
        'STAT_ERR': data['STAT_ERR'].astype(float)
    })
    
    # Sort by time just in case
    df = df.sort_values(by='MJD').reset_index(drop=True)
    
    # Handle missing values (e.g. <= 0 flux if applicable, or NaNs)
    # We will interpolate any missing/NaN values
    df['CTR'] = df['CTR'].replace([np.inf, -np.inf], np.nan)
    df.loc[df['CTR'] <= 0, 'CTR'] = np.nan
    df['CTR'] = df['CTR'].interpolate(method='linear').bfill().ffill()
    
    # Normalize the Flux (CTR) using Min-Max Scaling
    scaler = MinMaxScaler()
    df['CTR_NORM'] = scaler.fit_transform(df[['CTR']])
    
    print(f"Preprocessed DataFrame with {len(df)} rows.")
    return df, scaler

if __name__ == '__main__':
    # Test run
    sample_file = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\datasets\HEL1OS_sample\2023\12\01\HLS_20231130_235953_28794sec_lev1_V111\cdte\lightcurve_cdte1.fits"
    df, _ = preprocess_fits_to_dataframe(sample_file)
    print(df.head())
    
    # Save the cleaned DataFrame
    os.makedirs(r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\datasets\processed", exist_ok=True)
    out_path = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\datasets\processed\sample_cleaned.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved to {out_path}")
