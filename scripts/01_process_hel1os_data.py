import os
import glob
import zipfile
import shutil
import argparse
import pandas as pd
import numpy as np
from astropy.io import fits
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler

def process_single_fits(fits_path, hdu_index=5):
    """Reads a single FITS file and returns a preprocessed dataframe."""
    try:
        with fits.open(fits_path) as hdul:
            data = hdul[hdu_index].data
            
        df = pd.DataFrame({
            'MJD': data['MJD'].astype(float),
            'CTR': data['CTR'].astype(float),
            'STAT_ERR': data['STAT_ERR'].astype(float)
        })
        df = df.sort_values(by='MJD').reset_index(drop=True)
        
        # Clean
        df['CTR'] = df['CTR'].replace([np.inf, -np.inf], np.nan)
        df.loc[df['CTR'] <= 0, 'CTR'] = np.nan
        df['CTR'] = df['CTR'].interpolate(method='linear').bfill().ffill()
        
        # Normalize
        scaler = MinMaxScaler()
        df['CTR_NORM'] = scaler.fit_transform(df[['CTR']])
        
        return df
    except Exception as e:
        print(f"  Error processing {fits_path}: {e}")
        return None

def batch_process_datasets(data_dir, output_parquet, max_files=None):
    zip_files = glob.glob(os.path.join(data_dir, '**', '*.zip'), recursive=True)
    if not zip_files:
        print(f"No zip files found in {data_dir}")
        return
        
    print(f"Found {len(zip_files)} ZIP files to process.")
    if max_files:
        zip_files = zip_files[:max_files]
        print(f"DRY RUN: Limiting to first {max_files} files.")
        
    temp_dir = os.path.join(data_dir, 'temp_extract_pipeline')
    os.makedirs(temp_dir, exist_ok=True)
    
    append_mode = False
    if os.path.exists(output_parquet):
        print(f"Warning: {output_parquet} already exists. We will append to it.")
        append_mode = True
        
    for i, zip_path in enumerate(tqdm(zip_files, desc="Processing Datasets")):
        try:
            # 1. Extract ONLY the necessary file to save time and prevent file lock errors
            extracted_file_path = None
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                target_name = None
                for name in zip_ref.namelist():
                    if name.endswith('lightcurve_cdte1.fits'):
                        target_name = name
                        break
                
                # Fallback if specific file isn't found
                if not target_name:
                    for name in zip_ref.namelist():
                        if 'cdte' in name and name.endswith('.fits'):
                            target_name = name
                            break
                            
                if target_name:
                    zip_ref.extract(target_name, temp_dir)
                    extracted_file_path = os.path.join(temp_dir, target_name)
                    
            if extracted_file_path and os.path.exists(extracted_file_path):
                # 2. Process
                df = process_single_fits(extracted_file_path)
                
                if df is not None and len(df) > 0:
                    # 3. Append to Parquet
                    if append_mode:
                        df.to_parquet(output_parquet, engine='fastparquet', append=True)
                    else:
                        df.to_parquet(output_parquet, engine='fastparquet', append=False)
                        append_mode = True 
            
        except Exception as e:
            print(f"Failed to process {zip_path}: {e}")
            
        finally:
            # 4. Aggressive cleanup to free disk space
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
                os.makedirs(temp_dir, exist_ok=True)
            except:
                pass

    # Final Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"\nBatch processing complete! Master dataset saved to {output_parquet}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Process Aditya-L1 ZIPs")
    parser.add_argument("--dry-run", action="store_true", help="Only process the first 3 files for testing")
    args = parser.parse_args()
    
    project_root = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data"
    data_dir = os.path.join(project_root, "datasets", "HEL1OS")
    output_parquet = os.path.join(project_root, "datasets", "processed", "hel1os_dataset.parquet")
    
    max_files = 3 if args.dry_run else None
    
    batch_process_datasets(data_dir, output_parquet, max_files=max_files)
