import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
import matplotlib.pyplot as plt

class FlareLSTM(nn.Module):
    def __init__(self, input_size=2, hidden_size=64, num_layers=2):
        super(FlareLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size, 1)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        # out: tensor of shape (batch_size, seq_length, hidden_size)
        out, _ = self.lstm(x)
        # Decode the hidden state of the last time step
        out = self.fc(out[:, -1, :])
        return self.sigmoid(out)

def train_lstm():
    X_path = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\datasets\processed\X_sample.npy"
    y_path = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\datasets\processed\y_sample.npy"
    
    print("Loading datasets...")
    X = np.load(X_path)
    y = np.load(y_path)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Convert to PyTorch tensors
    X_train_t = torch.tensor(X_train, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    X_test_t = torch.tensor(X_test, dtype=torch.float32)
    y_test_t = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)
    
    # Calculate positive weight for imbalanced dataset
    num_pos = np.sum(y_train)
    num_neg = len(y_train) - num_pos
    pos_weight = torch.tensor([num_neg / max(1, num_pos)], dtype=torch.float32)
    
    train_data = TensorDataset(X_train_t, y_train_t)
    train_loader = DataLoader(train_data, batch_size=128, shuffle=True)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    model = FlareLSTM().to(device)
    criterion = nn.BCELoss(weight=None) # We will apply custom weighting if needed, but BCELoss doesn't take pos_weight directly. Let's use BCEWithLogitsLoss if we drop sigmoid, but for simplicity let's stick to standard BCE and we can rely on Adam.
    # Actually BCEWithLogitsLoss is better for pos_weight
    # Let's override
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight.to(device))
    # We must remove Sigmoid from model for BCEWithLogitsLoss
    model.sigmoid = nn.Identity() 
    
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    epochs = 10
    train_losses = []
    
    print("Starting Training...")
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item()
        
        avg_loss = epoch_loss / len(train_loader)
        train_losses.append(avg_loss)
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}")
        
    print("Evaluating LSTM model...")
    model.eval()
    with torch.no_grad():
        X_test_t = X_test_t.to(device)
        logits = model(X_test_t)
        probs = torch.sigmoid(logits).cpu().numpy()
        preds = (probs > 0.5).astype(int)
        
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, zero_division=0)
    rec = recall_score(y_test, preds)
    roc = roc_auc_score(y_test, probs)
    
    print(f"--- Deep Learning Performance (LSTM) ---")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"ROC-AUC:   {roc:.4f}")
    print("----------------------------------------")
    
    # Save Model
    models_dir = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\models"
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, 'lstm_flare.pth')
    torch.save(model.state_dict(), model_path)
    
    # Save training plot
    plt.figure()
    plt.plot(range(1, epochs+1), train_losses, marker='o')
    plt.title('LSTM Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('BCE Loss')
    
    artifact_dir = r"C:\Users\NFS Photographer\.gemini\antigravity-ide\brain\79d3e34d-4b55-4524-a972-89a9161d8826"
    plot_path = os.path.join(artifact_dir, "lstm_loss.png")
    plt.savefig(plot_path)
    print(f"Training plot saved to {plot_path}")

if __name__ == "__main__":
    train_lstm()
