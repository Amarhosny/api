# Palm Tree Health Classification API

Production-ready FastAPI service for palm tree health classification using XGBoost.

## Project Structure

```
API/
├── model/
│   ├── pipeline.pkl        # Trained sklearn pipeline (preprocessor + XGBoost)
│   └── label_encoder.pkl   # Label encoder for target classes
├── app/
│   ├── main.py             # FastAPI application
│   ├── predict.py          # Prediction logic
│   └── schemas.py          # Pydantic schemas
├── requirements.txt        # Python dependencies
└── README.md
```

## Installation

```bash
cd API
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Endpoints

### GET /
Health check endpoint.

### POST /predict
Make a prediction.

**Request Body:**
```json
{
  "Variety": "Medjool",
  "Age": 10,
  "Height": 4.5,
  "Trunk_Diam": 1.0,
  "Salinity": 900.0,
  "Moisture": 30.0,
  "pH": 7.1,
  "Fronds_Count": 52,
  "Leaf_Color": "Dark_Green",
  "Irrigation_Uniformity": 92.0,
  "Root_Zone_Variance": 2.8,
  "Canopy_Temp_Delta": 1.4,
  "Phenological_Stage": 4,
  "Irrigation_Vol_L": 185.0,
  "Frond_Health_Ratio": 0.93
}
```

**Response:**
```json
{
  "predicted_status": "Healthy",
  "confidence": 0.9995,
  "top_3": [
    {"status": "Healthy", "probability": 0.9995},
    {"status": "Partial_Clogging", "probability": 0.0005},
    {"status": "Maintenance_Issue", "probability": 0.0000}
  ],
  "health_score": 99.9
}
```

## Testing with curl

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Variety": "Medjool",
    "Age": 10,
    "Height": 4.5,
    "Trunk_Diam": 1.0,
    "Salinity": 900.0,
    "Moisture": 30.0,
    "pH": 7.1,
    "Fronds_Count": 52,
    "Leaf_Color": "Dark_Green",
    "Irrigation_Uniformity": 92.0,
    "Root_Zone_Variance": 2.8,
    "Canopy_Temp_Delta": 1.4,
    "Phenological_Stage": 4,
    "Irrigation_Vol_L": 185.0,
    "Frond_Health_Ratio": 0.93
  }'
```

## API Documentation

Interactive docs available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Model Details

- **Algorithm**: XGBoost Classifier
- **Preprocessing**: StandardScaler (numeric) + OneHotEncoder (categorical)
- **Classes**: 16 health status categories
- **Accuracy**: ~95.5%
