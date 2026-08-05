import pandas as pd
import pyarrow.parquet as pq
import os

# Define relative paths to the datasets
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
hel1os_path = os.path.join(project_root, "datasets", "processed", "hel1os_dataset.parquet")
solexs_path = os.path.join(project_root, "datasets", "processed", "solexs_dataset.parquet")

print("="*50)
print("Verifying HEL1OS (hel1os_dataset.parquet)")
print("="*50)
if os.path.exists(hel1os_path):
    hel1os_meta = pq.read_metadata(hel1os_path)
    print(f"Total Rows: {hel1os_meta.num_rows:,}")
    print(f"Total Columns: {hel1os_meta.num_columns}")
    print("\nFirst 3 rows:")
    print(pd.read_parquet(hel1os_path).head(3))
else:
    print(f"File not found: {hel1os_path}")

print("\n" + "="*50)
print("Verifying SoLEXS (solexs_dataset.parquet)")
print("="*50)
if os.path.exists(solexs_path):
    solexs_meta = pq.read_metadata(solexs_path)
    print(f"Total Rows: {solexs_meta.num_rows:,}")
    print(f"Total Columns: {solexs_meta.num_columns}")
    print("\nFirst 3 rows:")
    print(pd.read_parquet(solexs_path).head(3))
else:
    print(f"File not found: {solexs_path}")
