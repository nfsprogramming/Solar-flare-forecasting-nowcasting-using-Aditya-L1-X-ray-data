import os

def get_dir_size(path, extension=None):
    total_size = 0
    file_count = 0
    if not os.path.exists(path):
        return 0, 0
        
    if os.path.isfile(path):
        if extension is None or path.endswith(extension):
            return os.path.getsize(path), 1
        return 0, 0

    for root, dirs, files in os.walk(path):
        for f in files:
            if extension is None or f.endswith(extension):
                total_size += os.path.getsize(os.path.join(root, f))
                file_count += 1
    return total_size, file_count

def format_size(size_bytes):
    if size_bytes == 0:
        return "0 MB"
    mb = size_bytes / (1024 * 1024)
    if mb >= 1024:
        return f"{mb / 1024:.2f} GB"
    return f"{mb:.2f} MB"

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Raw Datasets (ZIP or CSV)
raw_dir = os.path.join(project_dir, "datasets", "raw")
zip_size, zip_count = get_dir_size(raw_dir, ".zip")
csv_size, csv_count = get_dir_size(raw_dir, ".csv")

print("=== RAW DATA ===")
if zip_count > 0:
    print(f"Total Raw ZIP Files: {zip_count} files -> {format_size(zip_size)}")
if csv_count > 0:
    print(f"Total Raw CSV Files: {csv_count} files -> {format_size(csv_size)}")

# 2. Processed Parquet Files
print("\n=== PROCESSED DATA (PARQUET) ===")
hel1os_pq = os.path.join(project_dir, "datasets", "processed", "hel1os_dataset.parquet")
h_size, _ = get_dir_size(hel1os_pq)
print(f"HEL1OS Parquet (hel1os_dataset.parquet): {format_size(h_size)}")

solexs_pq = os.path.join(project_dir, "datasets", "processed", "solexs_dataset.parquet")
s_size, _ = get_dir_size(solexs_pq)
print(f"SoLEXS Parquet (solexs_dataset.parquet): {format_size(s_size)}")

# 3. Models
print("\n=== AI MODELS ===")
model_dir = os.path.join(project_dir, "models")
for f in os.listdir(model_dir):
    f_path = os.path.join(model_dir, f)
    if os.path.isfile(f_path):
        m_size, _ = get_dir_size(f_path)
        print(f"Model ({f}): {format_size(m_size)}")
