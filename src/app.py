from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
from typing import List
import os
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib  # Thay pickle bằng joblib để lưu/load mô hình scikit-learn (tốt hơn)

app = FastAPI(title="Iris Classification API", version="1.0.0")

# Đường dẫn mô hình
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "iris_model.pkl")

# Biến toàn cục lưu mô hình
model = None

class PredictionInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class PredictionOutput(BaseModel):
    prediction: int
    class_name: str
    confidence: float

def train_and_save_model():
    """Huấn luyện mô hình mới và lưu xuống disk nếu chưa tồn tại"""
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Split đơn giản để có accuracy tham chiếu (không dùng trong production thực tế)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # Tạo thư mục models nếu chưa tồn tại
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Lưu mô hình bằng joblib (tốt hơn pickle cho scikit-learn)
    joblib.dump(rf_model, MODEL_PATH)
    print("New Iris model trained and saved at runtime.")
    return rf_model

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            print("Pre-trained model loaded successfully.")
        except Exception as e:
            print(f"Error loading pre-trained model: {e}. Training new model...")
            model = train_and_save_model()
    else:
        print("Pre-trained model not found. Training new model at runtime...")
        model = train_and_save_model()
    
    return model

@app.on_event("startup")
async def startup_event():
    load_model()

@app.get("/")
async def root():
    return {
        "message": "Iris Classification API",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Chuyển input thành array numpy
    features = np.array([[input_data.sepal_length,
                          input_data.sepal_width,
                          input_data.petal_length,
                          input_data.petal_width]])
    
    # Dự đoán
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    confidence = float(np.max(probabilities))
    
    # Map class index sang tên loài hoa
    class_names = ["setosa", "versicolor", "virginica"]
    class_name = class_names[prediction]
    
    return PredictionOutput(
        prediction=int(prediction),
        class_name=class_name,
        confidence=confidence
    )
