import joblib
import pandas as pd
import numpy as np

def test_model():
    model = joblib.load('random_forest_model.pkl')
    scaler = joblib.load('scaler.pkl')
    imputer = joblib.load('imputer.pkl')
    model_columns = joblib.load('model_columns.pkl')
    
    print(f"Model columns: {model_columns}")
    
    # Create a dummy input that should be "High" performance
    # In training, high Quality_Score and low Delivery_Time_Days should be better
    test_data = {
        'Quality_Score': 10.0,
        'Delivery_Time_Days': 1.0,
        'Cost_Score': 10.0,
        'Payment_Terms': 'Net 30',
        'Region': 'North'
    }
    
    df = pd.DataFrame([test_data])
    df_encoded = pd.get_dummies(df)
    
    for col in model_columns:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
            
    df_encoded = df_encoded[model_columns]
    
    print("Encoded data (first 5 columns):")
    print(df_encoded.iloc[:, :5])
    
    df_imputed = pd.DataFrame(imputer.transform(df_encoded), columns=df_encoded.columns)
    df_scaled = pd.DataFrame(scaler.transform(df_imputed), columns=df_encoded.columns)
    
    prediction = model.predict(df_scaled)[0]
    probs = model.predict_proba(df_scaled)[0]
    
    print(f"Prediction: {prediction}")
    print(f"Probabilities: {probs}")

if __name__ == "__main__":
    test_model()
