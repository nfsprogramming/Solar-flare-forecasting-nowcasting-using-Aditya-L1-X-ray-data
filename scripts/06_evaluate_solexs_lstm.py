import os
import sys
import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from torch.utils.data import DataLoader
from tqdm import tqdm

project_root = r"d:\NFS's Projects\Solar flare forecasting nowcasting using Aditya-L1 X-ray data"
sys.path.append(project_root)

from scripts.big_data_dataset import ParquetSequenceDataset
from scripts.train_lstm import FlareLSTM

def evaluate_on_dataset(model, dataset_path, device, dataset_name, feature_cols, max_batches=200):
    print(f"\n=============================================")
    print(f"Benchmarking against {dataset_name} Dataset")
    print(f"=============================================")
    
    dataset = ParquetSequenceDataset(dataset_path, window_size=60, forecast_horizon=10, feature_cols=feature_cols)
    dataloader = DataLoader(dataset, batch_size=2048, drop_last=True)
    
    all_targets = []
    all_probs = []
    
    model.eval()
    pbar = tqdm(dataloader, desc=f"Evaluating {dataset_name}", total=max_batches)
    
    batches = 0
    with torch.no_grad():
        for X_batch, y_batch in pbar:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            
            outputs = model(X_batch)
            probs = torch.sigmoid(outputs)
            
            all_targets.extend(y_batch.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
            
            batches += 1
            if batches >= max_batches:
                break
                
    all_targets = np.array(all_targets).flatten()
    all_probs = np.array(all_probs).flatten()
    
    # Calculate the optimal mathematical threshold using Precision-Recall Curve
    from sklearn.metrics import precision_recall_curve
    precisions, recalls, thresholds = precision_recall_curve(all_targets, all_probs)
    f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-8)
    optimal_idx = np.argmax(f1_scores)
    optimal_threshold = thresholds[optimal_idx] if optimal_idx < len(thresholds) else 0.5
    
    all_preds = (all_probs > optimal_threshold).astype(int)
    
    accuracy = accuracy_score(all_targets, all_preds)
    print(f"\n[{dataset_name} Benchmark Results]")
    print(f"Optimal Threshold (Auto-Tuned): {optimal_threshold:.4f}")
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(classification_report(all_targets, all_preds, labels=[0, 1], target_names=["Quiet (0)", "Flare (1)"], zero_division=0))
    
    # Plot Confusion Matrix
    cm = confusion_matrix(all_targets, all_preds)
    plt.figure(figsize=(6, 5))
    # Use Oranges color map for SoLEXS to distinguish from the blue HEL1OS matrix
    sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges', xticklabels=["Quiet", "Flare"], yticklabels=["Quiet", "Flare"])
    plt.title(f"{dataset_name} Confusion Matrix (SoLEXS Model)")
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    
    cm_path = os.path.join(project_root, f"{dataset_name.lower()}_solexs_confusion_matrix.png")
    plt.savefig(cm_path)
    print(f"Saved {dataset_name} Confusion Matrix to: {cm_path}")
    
def main():
    model_path = os.path.join(project_root, "models", "solexs_lstm_model.pth")
    if not os.path.exists(model_path):
        print(f"ERROR: Model not found at {model_path}. Is the training finished?")
        return
        
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Loading SoLEXS Model to Device: {device}")
    
    model = FlareLSTM(input_size=2, hidden_size=64, num_layers=2)
    model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
    model.to(device)
    
    solexs_path = os.path.join(project_root, "datasets", "processed", "solexs_dataset.parquet")
    
    # Evaluate on ~400,000 sequences of SoLEXS
    if os.path.exists(solexs_path):
        evaluate_on_dataset(model, solexs_path, device, "SoLEXS", feature_cols=['COUNTS', 'COUNTS_NORM'], max_batches=200)
    else:
        print("SoLEXS dataset not found, skipping...")

if __name__ == "__main__":
    main()
