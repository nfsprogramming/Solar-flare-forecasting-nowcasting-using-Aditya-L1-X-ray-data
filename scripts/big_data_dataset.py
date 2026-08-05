import os
import torch
import pyarrow.parquet as pq
import numpy as np
from torch.utils.data import IterableDataset

class ParquetSequenceDataset(IterableDataset):
    """
    An IterableDataset that streams data directly from a huge Parquet file 
    and yields sliding window sequences on the fly.
    """
    def __init__(self, parquet_path, window_size=60, forecast_horizon=10, feature_cols=['CTR_NORM', 'STAT_ERR']):
        self.parquet_path = parquet_path
        self.window_size = window_size
        self.forecast_horizon = forecast_horizon
        self.feature_cols = feature_cols
        
        # We read metadata to get total rows without loading into memory
        self.parquet_file = pq.ParquetFile(parquet_path)
        
    def __iter__(self):
        # We iterate over row groups in the parquet file
        for batch_index in range(self.parquet_file.num_row_groups):
            # Read one row group into pandas dataframe
            df = self.parquet_file.read_row_group(batch_index, columns=self.feature_cols).to_pandas()
            features = df[self.feature_cols].values
            
            # 1. Chunk-wise StandardScaler
            # Protect against division by zero with 1e-8
            mean = np.mean(features, axis=0)
            std = np.std(features, axis=0) + 1e-8
            features = (features - mean) / std
            
            # 2. Dynamic Target Thresholding
            # Label as flare (1) only if the flux is in the top 1% of the current chunk
            flux_column = df[self.feature_cols[0]].values
            chunk_threshold = np.percentile(flux_column, 99)
            targets = (flux_column > chunk_threshold).astype(int)
            
            chunk_length = len(features)
            
            for i in range(chunk_length - self.window_size - self.forecast_horizon):
                x_seq = features[i : i + self.window_size]
                y_horizon = targets[i + self.window_size : i + self.window_size + self.forecast_horizon]
                y_label = 1 if np.sum(y_horizon) > 0 else 0
                
                # Yield single sequence and label
                yield torch.tensor(x_seq, dtype=torch.float32), torch.tensor([y_label], dtype=torch.float32)

if __name__ == "__main__":
    # Test the dataset
    project_root = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data"
    hel1os_path = os.path.join(project_root, "datasets", "processed", "hel1os_dataset.parquet")
    
    if os.path.exists(hel1os_path):
        dataset = ParquetSequenceDataset(hel1os_path)
        iterator = iter(dataset)
        x, y = next(iterator)
        print(f"Sample X shape: {x.shape}")
        print(f"Sample Y shape: {y.shape}")
        print("IterableDataset is working correctly!")
    else:
        print("Master dataset not found.")
