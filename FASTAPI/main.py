from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib
from fastapi.responses import RedirectResponse
# Load pipeline
pipeline = joblib.load("fraud_detection_pipeline.pkl")

# FastAPI app
app = FastAPI()

# Request model
class Transaction(BaseModel):
    TX_AMOUNT: float
    TX_TIME_SECONDS: float
    TX_TIME_DAYS: float
    TRIES: int
    TX_HOUR: int
    IS_WEEKEND: int

@app.post("/predict/")
def predict_fraud(tx: Transaction):
    try:
        # Convert input to DataFrame with proper column names
        input_df = pd.DataFrame([tx.dict()])
        
        # Predict probability of fraud
        prob = pipeline.predict_proba(input_df)[0][1]  # probability of class '1' (fraud)
        label = int(prob > 0.5)

        return {
            "fraud_probability": float(prob),
            "is_fraud": label
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
   
    uvicorn.run("main:app",  port=8000, reload=True)
