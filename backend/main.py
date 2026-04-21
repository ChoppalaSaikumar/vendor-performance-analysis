from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(title="Vendor Analysis API")

# Configure CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML artifacts
# In a real app, you might want to load these dynamically or handle errors better
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "random_forest_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")
IMPUTER_PATH = os.path.join(BASE_DIR, "imputer.pkl")
COLUMNS_PATH = os.path.join(BASE_DIR, "model_columns.pkl")
DATASET_PATH = os.path.join(BASE_DIR, "vendor_dataset.csv")

model = None
scaler = None
imputer = None
model_columns = None

@app.on_event("startup")
async def startup_event():
    global model, scaler, imputer, model_columns
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            scaler = joblib.load(SCALER_PATH)
            imputer = joblib.load(IMPUTER_PATH)
            model_columns = joblib.load(COLUMNS_PATH)
            print("Successfully loaded ML models!")
        else:
            print(f"Warning: Model file {MODEL_PATH} not found. Please run train_model.py first.")
    except Exception as e:
        print(f"Error loading models: {e}")

class VendorFeatures(BaseModel):
    Quality_Score: float
    Delivery_Time_Days: float
    Cost_Score: float
    Payment_Terms: str
    Region: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Vendor Analysis API. Use /predict to get predictions."}

@app.post("/predict")
def predict_performance(features: VendorFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please train the model first.")
        
    try:
        # Convert input to DataFrame
        input_data = {
            'Quality_Score': [features.Quality_Score],
            'Delivery_Time_Days': [features.Delivery_Time_Days],
            'Cost_Score': [features.Cost_Score],
            'Payment_Terms': [features.Payment_Terms],
            'Region': [features.Region]
        }
        df = pd.DataFrame(input_data)
        
        # 1. Handle Categorical Features (get_dummies)
        df_encoded = pd.get_dummies(df)
        
        # 2. Realign columns to match training data
        # Fill missing columns with 0
        for col in model_columns:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
                
        # Ensure column order matches exactly
        df_encoded = df_encoded[model_columns]
        
        # 3. Impute
        df_imputed = pd.DataFrame(imputer.transform(df_encoded), columns=df_encoded.columns)
        
        # 4. Scale
        df_scaled = pd.DataFrame(scaler.transform(df_imputed), columns=df_encoded.columns)
        
        # 5. Predict
        prediction = model.predict(df_scaled)[0]
        
        # Map back to human readable classes
        class_mapping = {0: "Low", 1: "Medium", 2: "High"}
        predicted_class = class_mapping.get(int(prediction), "Unknown")
        
        # You could also return probabilities if desired
        # probabilities = model.predict_proba(df_scaled)[0].tolist()
        
        return {
            "prediction_code": int(prediction),
            "prediction_class": predicted_class,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vendors")
def get_vendors():
    if not os.path.exists(DATASET_PATH):
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    try:
        df = pd.read_csv(DATASET_PATH)
        # Fill NaN with None for JSON compatibility
        df = df.where(pd.notnull(df), None)
        # Limit to 100 for performance if needed, but 200 is fine
        return df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_stats():
    if not os.path.exists(DATASET_PATH):
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    try:
        df = pd.read_csv(DATASET_PATH)
        
        # Performance distribution
        df['Performance_Class'] = pd.cut(df['Performance_Score'], bins=[0, 4, 7, 10], labels=['Low', 'Medium', 'High'], include_lowest=True)
        
        class_counts = df['Performance_Class'].value_counts().to_dict()
        region_counts = df['Region'].value_counts().to_dict()
        
        avg_quality = float(df['Quality_Score'].mean())
        avg_delivery = float(df['Delivery_Time_Days'].mean())
        avg_cost = float(df['Cost_Score'].mean())
        
        # Enhanced Quality vs Cost data for scatter plot
        # Add a category column for easier coloring in frontend
        scatter_df = df[['Quality_Score', 'Cost_Score', 'Performance_Score']].dropna().copy()
        scatter_df['Category'] = pd.cut(
            scatter_df['Performance_Score'], 
            bins=[0, 4, 7, 10], 
            labels=['Low', 'Medium', 'High'], 
            include_lowest=True
        )
        
        scatter_data = scatter_df.head(200).to_dict(orient='records')
        
        return {
            "class_distribution": [{"name": k, "value": v} for k, v in class_counts.items()],
            "region_distribution": [{"name": k, "value": v} for k, v in region_counts.items()],
            "averages": {
                "quality": round(avg_quality, 2),
                "delivery": round(avg_delivery, 2),
                "cost": round(avg_cost, 2)
            },
            "total_vendors": len(df),
            "scatter_data": scatter_data
        }
    except Exception as e:
        print(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
