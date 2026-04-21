# Vendor Performance Analysis & Prediction

An end-to-end full-stack application designed to analyze vendor performance and predict future performance classes using Machine Learning. This project features a FastAPI backend for data processing and model inference, and a modern React frontend for interactive data visualization.

## 🚀 Features

- **Performance Prediction**: Predict vendor performance levels (Low, Medium, High) based on metrics like Quality Score, Delivery Time, and Cost Score.
- **Interactive Dashboard**: Real-time visualization of vendor statistics, including quality vs. cost correlations and regional distributions.
- **Vendor Directory**: A comprehensive list of all vendors with their historical performance data.
- **Machine Learning Integration**: Powered by a Random Forest model trained on historical vendor datasets.

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Server**: Uvicorn
- **Serialization**: Joblib (for model persistence)

### Frontend
- **Framework**: React (Vite)
- **Styling**: Vanilla CSS (Modern Design)
- **Data Visualization**: Recharts
- **Icons**: Lucide React

## 📂 Project Structure

```text
├── backend/                # FastAPI application
│   ├── main.py             # API routes and ML inference logic
│   ├── train_model.py      # Script to train and save the ML model
│   ├── requirements.txt    # Python dependencies
│   └── *.pkl               # Saved ML models and preprocessors
├── frontend/               # React application
│   ├── src/                # Component and styling source
│   ├── index.html          # App entry point
│   └── package.json        # Node dependencies
└── vendor_dataset.csv      # The dataset used for analysis and training
```

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js & npm

### 1. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) Train the model:
   ```bash
   python train_model.py
   ```
5. Start the server:
   ```bash
   python -m uvicorn main:app --reload
   ```

### 2. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## 📊 API Endpoints

- `GET /`: API Health Check
- `POST /predict`: Submit vendor metrics to receive a performance class prediction.
- `GET /vendors`: Retrieve the full list of vendors from the dataset.
- `GET /stats`: Get aggregate statistics for the dashboard visualizations.

## 📝 License
This project is for educational and analytical purposes.
