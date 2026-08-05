import pyarrow.parquet as pq
import pandas as pd
import os
import json

project_root = r"d:\NFS's Projects\Solar flare forecasting nowcasting using Aditya-L1 X-ray data"
parquet_path = os.path.join(project_root, "datasets", "processed", "hel1os_dataset.parquet")

print("Scanning the 106 GB Parquet file for Solar Flares...")
pf = pq.ParquetFile(parquet_path)

flares = []

for i in range(pf.num_row_groups):
    df_chunk = pf.read_row_group(i).to_pandas()
    
    # Check for major flares (CTR_NORM > 0.8)
    if 'CTR_NORM' in df_chunk.columns:
        flare_mask = df_chunk['CTR_NORM'] > 0.8
        if flare_mask.any():
            flare_df = df_chunk[flare_mask].copy()
            max_row = flare_df.loc[flare_df['CTR_NORM'].idxmax()]
            
            mjd = max_row['MJD']
            flux = max_row['CTR_NORM']
            
            dt = pd.to_datetime((mjd - 40587) * 86400, unit='s')
            
            flares.append({
                "Date": dt.strftime('%Y-%m-%d'),
                "Time": dt.strftime('%H:%M:%S UTC'),
                "Max Flux": round(flux, 4)
            })
            print(f"Detected Flare: {dt} (Flux: {flux})")

flares.sort(key=lambda x: x["Max Flux"], reverse=True)

with open(os.path.join(project_root, "flare_events.json"), "w") as f:
    json.dump(flares, f, indent=4)

print(f"\nScan complete! Found {len(flares)} major solar flare events.")
