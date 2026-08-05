import os
import torch
import torch.nn as nn
import torch.optim as optim
import sys
from torch.utils.data import DataLoader
from tqdm import tqdm

project_root = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data"
sys.path.append(project_root)

# Import our custom IterableDataset
from scripts.big_data_dataset import ParquetSequenceDataset
from scripts.train_lstm import FlareLSTM

def train_bigdata_lstm():
    project_root = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data"
    hel1os_path = os.path.join(project_root, "datasets", "processed", "hel1os_dataset.parquet")
    model_save_path = os.path.join(project_root, "models", "hel1os_lstm_model.pth")
    
    # 1. Device Configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"=====================================")
    print(f"Training on Device: {device}")
    if torch.cuda.is_available():
        print(f"GPU Name: {torch.cuda.get_device_name(0)}")
    print(f"=====================================\n")
    
    # 2. Dataset and DataLoader
    print("Initializing Parquet Sequence Data Streamer...")
    dataset = ParquetSequenceDataset(hel1os_path, window_size=60, forecast_horizon=10, feature_cols=['CTR_NORM', 'STAT_ERR'])
    # Because it's an IterableDataset, we use a standard DataLoader but with batch_size
    dataloader = DataLoader(dataset, batch_size=2048, drop_last=True) # High batch size to saturate the RTX 4050
    
    # 3. Initialize Model
    # Input size is 2 (CTR_NORM, STAT_ERR), hidden size 64
    model = FlareLSTM(input_size=2, hidden_size=64, num_layers=2)
    model.to(device)
    
    # 4. Loss and Optimizer
    # Weighted loss because flares are rare. We'll use a strong weight for the positive class
    criterion = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([20.0]).to(device))
    optimizer = optim.Adam(model.parameters(), lr=0.0001)
    
    # 5. Training Loop
    num_epochs = 1 # Just 1 epoch because the dataset is so massive
    
    model.train()
    for epoch in range(num_epochs):
        epoch_loss = 0.0
        batches = 0
        
        # We wrap the dataloader in tqdm to see streaming progress
        pbar = tqdm(dataloader, desc=f"Epoch {epoch+1}/{num_epochs}")
        for X_batch, y_batch in pbar:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            
            optimizer.zero_grad()
            
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            
            loss.backward()
            
            # Gradient Clipper to prevent exploding gradients
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            
            optimizer.step()
            
            epoch_loss += loss.item()
            batches += 1
            
            pbar.set_postfix({'Loss': f"{loss.item():.4f}"})
            
            # Optional: break early for testing
            # if batches > 100:
            #     break
            
        print(f"Epoch {epoch+1} Complete. Avg Loss: {epoch_loss/batches:.4f}")
        
    # 6. Save Model
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    torch.save(model.state_dict(), model_save_path)
    print(f"Big Data Model saved to {model_save_path}")

if __name__ == "__main__":
    train_bigdata_lstm()
