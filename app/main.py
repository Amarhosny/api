"""FastAPI application for Palm Tree Health Classification."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.schemas import PalmInput, PalmPredictionResponse, HealthCheck
from app.predict import predictor, predict_palm

app = FastAPI(
    title="Palm Tree Health Classification API",
    description="API for predicting palm tree health status using XGBoost model",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Load model on startup."""
    predictor.load()


@app.get("/", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    return HealthCheck(
        status="healthy",
        model_loaded=predictor._pipeline is not None
    )


@app.post("/predict", response_model=PalmPredictionResponse)
async def predict(input_data: PalmInput):
    """
    Predict palm tree health status.

    Returns:
        - predicted_status: The predicted health status
        - confidence: Model confidence (0-1)
        - top_3: Top 3 predictions with probabilities
        - health_score: Overall health score (0-100)
    """
    try:
        result = predict_palm(input_data.model_dump())
        return PalmPredictionResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
