import zipfile
import os
import glob
from astropy.io import fits
import pandas as pd
import matplotlib.pyplot as plt

def main():
    zip_path = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\datasets\HEL1OS\HLS_20231130_235953_28794sec_lev1_V111.zip"
    extract_dir = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\datasets\HEL1OS_sample"
    
    print(f"Extracting {zip_path} to {extract_dir}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        
    print("Extraction complete. Looking for FITS files...")
    fits_files = glob.glob(os.path.join(extract_dir, '**', '*.fits'), recursive=True)
    
    print(f"Found {len(fits_files)} FITS files:")
    for f in fits_files:
        print(f" - {f}")
        
    # Pick a likely data file (usually not in 'aux' if possible, or just the largest fits file)
    if not fits_files:
        print("No FITS files found.")
        return
        
    # Let's inspect all fits files headers
    for f in fits_files:
        print(f"\n--- Inspecting {os.path.basename(f)} ---")
        try:
            with fits.open(f) as hdul:
                hdul.info()
                
                # Check tables
                for idx, hdu in enumerate(hdul):
                    if isinstance(hdu, (fits.BinTableHDU, fits.TableHDU)):
                        print(f"  Table HDU {idx}: {hdu.name}")
                        print(f"  Columns: {hdu.columns.names}")
        except Exception as e:
            print(f"  Failed to read {f}: {e}")

if __name__ == "__main__":
    main()
