from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib

# Load ML model
try:
    model = joblib.load("logistic_regression_model.pkl")
except Exception as e:
    raise RuntimeError("Model failed to load. Check logistic_regression_model.pkl") from e

# FastAPI app
app = FastAPI()

# Input features
FEATURES = ['TX_AMOUNT', 'TX_TIME_SECONDS', 'TX_TIME_DAYS', 'TRIES', 'CUSTOMER_ID', 'TERMINAL_ID']

# Input schema
class Transaction(BaseModel):
    TX_AMOUNT: float
    TX_TIME_SECONDS: float
    TX_TIME_DAYS: float
    TRIES: int
    CUSTOMER_ID: int
    TERMINAL_ID: int

@app.post("/predict/")
def predict(transaction: Transaction):
    try:
        # Convert to model input shape
        data = np.array([[getattr(transaction, f) for f in FEATURES]])
        prediction = model.predict(data)[0]
        proba = model.predict_proba(data)[0][1] if hasattr(model, "predict_proba") else None

        return {
            "is_fraud": bool(prediction),
            "fraud_probability": proba
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
