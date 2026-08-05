import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, classification_report

def train_baseline():
    X_path = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\datasets\processed\X_sample.npy"
    y_path = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\datasets\processed\y_sample.npy"
    
    print("Loading datasets...")
    X = np.load(X_path)
    y = np.load(y_path)
    
    # Flatten 3D sequences (N, 60, 2) to 2D (N, 120) for Random Forest
    X_flat = X.reshape(X.shape[0], -1)
    print(f"Flattened X shape: {X_flat.shape}")
    
    # Split data (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X_flat, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"Training Random Forest on {len(X_train)} samples...")
    # Using balanced class weight due to highly imbalanced target
    clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced', n_jobs=-1)
    clf.fit(X_train, y_train)
    
    print("Evaluating baseline model...")
    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    roc = roc_auc_score(y_test, y_proba)
    
    print(f"--- Baseline Performance (Random Forest) ---")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"ROC-AUC:   {roc:.4f}")
    print("--------------------------------------------")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    models_dir = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\models"
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, 'rf_baseline.joblib')
    joblib.dump(clf, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_baseline()
