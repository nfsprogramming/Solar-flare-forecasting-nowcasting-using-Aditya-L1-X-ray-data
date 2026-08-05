import os
import zipfile
import shutil
import argparse
import pandas as pd
import numpy as np
from astropy.io import fits
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler

def process_solexs_fits(fits_path, hdu_index=1):
    """Reads a SoLEXS lightcurve FITS file and returns a preprocessed dataframe."""
    try:
        with fits.open(fits_path) as hdul:
            data = hdul[hdu_index].data
            
        df = pd.DataFrame({
            'TIME': data['TIME'].astype(float),
            'COUNTS': data['COUNTS'].astype(float)
        })
        df = df.sort_values(by='TIME').reset_index(drop=True)
        
        # Clean
        df['COUNTS'] = df['COUNTS'].replace([np.inf, -np.inf], np.nan)
        df.loc[df['COUNTS'] <= 0, 'COUNTS'] = np.nan
        df['COUNTS'] = df['COUNTS'].interpolate(method='linear').bfill().ffill()
        
        # Normalize
        scaler = MinMaxScaler()
        df['COUNTS_NORM'] = scaler.fit_transform(df[['COUNTS']])
        
        return df
    except Exception as e:
        print(f"  Error processing {fits_path}: {e}")
        return None

def batch_process_solexs(zip_path, output_parquet, max_files=None):
    if not os.path.exists(zip_path):
        print(f"Error: Could not find {zip_path}")
        return
        
    # We will read the massive zip file
    print(f"Inspecting {zip_path}...")
    
    with zipfile.ZipFile(zip_path, 'r') as z:
        # Find all lightcurve files
        lc_files = [name for name in z.namelist() if name.endswith('.lc.gz')]
        print(f"Found {len(lc_files)} .lc.gz files to process.")
        
        if max_files:
            lc_files = lc_files[:max_files]
            print(f"DRY RUN: Limiting to first {max_files} files.")
            
        temp_dir = os.path.join(os.path.dirname(zip_path), 'temp_solexs_pipeline')
        os.makedirs(temp_dir, exist_ok=True)
        
        append_mode = False
        if os.path.exists(output_parquet):
            print(f"Warning: {output_parquet} already exists. We will append to it.")
            append_mode = True
            
        for name in tqdm(lc_files, desc="Processing SoLEXS"):
            try:
                # Extract one specific file
                z.extract(name, temp_dir)
                extracted_file_path = os.path.join(temp_dir, name)
                
                # Process
                df = process_solexs_fits(extracted_file_path)
                
                if df is not None and len(df) > 0:
                    if append_mode:
                        df.to_parquet(output_parquet, engine='fastparquet', append=True)
                    else:
                        df.to_parquet(output_parquet, engine='fastparquet', append=False)
                        append_mode = True 
                
            except Exception as e:
                print(f"Failed to process {name}: {e}")
                
            finally:
                # Cleanup aggressively
                try:
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    os.makedirs(temp_dir, exist_ok=True)
                except:
                    pass

    # Final Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"\nSoLEXS Batch processing complete! Master dataset saved to {output_parquet}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Process SoLEXS payload")
    parser.add_argument("--dry-run", action="store_true", help="Only process the first 3 files for testing")
    args = parser.parse_args()
    
    project_root = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data"
    zip_path = os.path.join(project_root, "datasets", "SoLEXS", "SoLEXS.zip")
    output_parquet = os.path.join(project_root, "datasets", "processed", "solexs_dataset.parquet")
    
    max_files = 3 if args.dry_run else None
    
    batch_process_solexs(zip_path, output_parquet, max_files=max_files)
