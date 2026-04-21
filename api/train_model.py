import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

def generate_mock_dataset(filepath):
    """Generate a mock dataset if the original is not provided."""
    print("Generating mock dataset...")
    np.random.seed(42)
    n_samples = 200
    
    data = {
        'Vendor_ID': [f'V{str(i).zfill(3)}' for i in range(1, n_samples + 1)],
        'Vendor_Name': [f'Vendor {i}' for i in range(1, n_samples + 1)],
        'Quality_Score': np.random.uniform(1, 10, n_samples),
        'Delivery_Time_Days': np.random.uniform(1, 30, n_samples),
        'Cost_Score': np.random.uniform(1, 10, n_samples),
        'Payment_Terms': np.random.choice(['Net 30', 'Net 60', 'Net 90'], n_samples),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], n_samples),
    }
    # Base performance on features to create a learnable pattern
    # Quality_Score (1-10), Delivery_Time_Days (1-30), Cost_Score (1-10)
    # Higher quality, lower delivery time, and higher cost score should lead to higher performance
    
    # Normalize delivery time to 0-1 range (inverted so lower is better)
    delivery_perf = 1 - (np.array(data['Delivery_Time_Days']) / 30.0)
    quality_perf = np.array(data['Quality_Score']) / 10.0
    cost_perf = np.array(data['Cost_Score']) / 10.0
    
    # Weighted average + some noise
    perf_base = (quality_perf * 0.5 + delivery_perf * 0.3 + cost_perf * 0.2) * 10
    noise = np.random.normal(0, 1, n_samples)
    
    data['Performance_Score'] = np.clip(perf_base + noise, 1, 10)
    
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    print(f"Mock dataset saved to {filepath}")

def train_and_save_model():
    dataset_path = '../vendor_dataset.csv'
    
    if not os.path.exists(dataset_path):
        print(f"Dataset {dataset_path} not found.")
        generate_mock_dataset(dataset_path)
    
    print("Loading dataset...")
    data = pd.read_csv(dataset_path)
    
    print("Preprocessing data...")
    # Separate features and target
    X = data.drop(['Vendor_ID', 'Vendor_Name', 'Performance_Score'], axis=1)
    y = data['Performance_Score']
    
    # Handle categorical data
    # Save the categories for encoding at prediction time
    categorical_cols = ['Payment_Terms', 'Region']
    X_encoded = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
    
    # We need to save the columns after get_dummies to ensure matching features during prediction
    model_columns = list(X_encoded.columns)
    joblib.dump(model_columns, 'model_columns.pkl')
    
    # Handle missing values
    imputer = SimpleImputer(strategy='mean')
    X_imputed = pd.DataFrame(imputer.fit_transform(X_encoded), columns=X_encoded.columns)
    
    # Scale numerical features to 1-10
    scaler = MinMaxScaler(feature_range=(1, 10))
    X_scaled = scaler.fit_transform(X_imputed)
    X_scaled = pd.DataFrame(X_scaled, columns=X_encoded.columns)
    
    # Discretize Performance_Score into 3 classes: Low (0), Medium (1), High (2)
    # y_class = pd.cut(y, bins=[0, 4, 7, 10], labels=[0, 1, 2])
    # The notebook did this, let's replicate:
    y_class = pd.cut(y, bins=[0, 4, 7, 10], labels=[0, 1, 2], include_lowest=True)
    
    # Drop rows where target is NaN (if any due to out of bounds)
    valid_idx = y_class.notna()
    X_scaled = X_scaled[valid_idx]
    y_class = y_class[valid_idx]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_class, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    y_pred = rf.predict(X_test)
    print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    
    print("Saving models and transformers...")
    joblib.dump(rf, 'random_forest_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(imputer, 'imputer.pkl')
    print("Done! Model artifacts saved in backend directory.")

if __name__ == "__main__":
    train_and_save_model()
