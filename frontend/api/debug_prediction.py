import joblib
import pandas as pd
import numpy as np

# Load artifacts
model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')
imputer = joblib.load('imputer.pkl')
model_columns = joblib.load('model_columns.pkl')

def predict(quality, delivery, cost, payment, region):
    input_data = {
        'Quality_Score': [quality],
        'Delivery_Time_Days': [delivery],
        'Cost_Score': [cost],
        'Payment_Terms': [payment],
        'Region': [region]
    }
    df = pd.DataFrame(input_data)
    
    # 1. Handle Categorical Features
    df_encoded = pd.get_dummies(df)
    
    # 2. Realign columns
    for col in model_columns:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
            
    df_encoded = df_encoded[model_columns]
    
    # 3. Impute
    df_imputed = pd.DataFrame(imputer.transform(df_encoded), columns=df_encoded.columns)
    
    # 4. Scale
    df_scaled = pd.DataFrame(scaler.transform(df_imputed), columns=df_encoded.columns)
    
    # 5. Predict
    prediction = model.predict(df_scaled)[0]
    probs = model.predict_proba(df_scaled)[0]
    
    return prediction, probs

print("Testing with High Quality vendor (Quality=10, Delivery=1, Cost=10):")
pred, probs = predict(10.0, 1.0, 10.0, 'Net 30', 'North')
print(f"Prediction: {pred}, Probs: {probs}")

print("\nTesting with Low Quality vendor (Quality=1, Delivery=30, Cost=1):")
pred, probs = predict(1.0, 30.0, 1.0, 'Net 30', 'North')
print(f"Prediction: {pred}, Probs: {probs}")
