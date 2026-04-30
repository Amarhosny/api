1 -# Palm Tree Health Classification API
        1 +# 🌴 Palm Tree Health Classification API
        2
        3 -Production-ready FastAPI service for palm tree health classification using XGBoost.
        3 +[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
        4 +[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
        5 +[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-orange.svg)](https://xgboost.ai)
        6 +[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
        7
        5 -## Project Structure
        8 +Production-ready REST API for palm tree health classification using machine learning. Detects 16 different health c
          +onditions including drought stress, nutrient deficiencies, diseases, and environmental stresses.
        9
       10 +---
       11 +
       12 +## 📋 Features
       13 +
       14 +- **16-Class Classification** - Identifies specific health conditions from Healthy to Critical_Multi_Stress
       15 +- **End-to-End Pipeline** - Sklearn ColumnTransformer + XGBoost in a single serialized pipeline
       16 +- **Confidence Scores** - Returns prediction confidence and top-3 alternatives
       17 +- **Health Score** - 0-100 weighted health index for quick assessment
       18 +- **Validated Input** - Pydantic schemas ensure data integrity
       19 +- **Auto-Scaling** - Preprocessing handled internally (no manual scaling required)
       20 +
       21 +---
       22 +
       23 +## 🏗️ Architecture
       24 +
       25  ```
       26 +┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
       27 +│   JSON Input    │ ──► │  Pydantic Schema │ ──► │   PalmPredictor │
       28 +└─────────────────┘     └──────────────────┘     └────────┬────────┘
       29 +                                                          │
       30 +                             ┌────────────────────────────┼────────────────────────────┐
       31 +                             │                            ▼                            │
       32 +                             │     ┌─────────────────────────────────┐                 │
       33 +                             │     │      sklearn Pipeline           │                 │
       34 +                             │     │  ┌─────────────┐ ┌───────────┐  │                 │
       35 +                             │     │  │ColumnTrans. │ │ XGBoost   │  │                 │
       36 +                             │     │  │ - Scaler    │ │ Classifier│  │                 │
       37 +                             │     │  │ - OHE       │ │           │  │                 │
       38 +                             │     │  └─────────────┘ └───────────┘  │                 │
       39 +                             │     └─────────────────────────────────┘                 │
       40 +                             │                            │                            │
       41 +                             └────────────────────────────┼────────────────────────────┘
       42 +                                                          ▼
       43 +                                          ┌───────────────────────────┐
       44 +                                          │  Prediction Response      │
       45 +                                          │  - status, confidence     │
       46 +                                          │  - top_3, health_score    │
       47 +                                          └───────────────────────────┘
       48 +```
       49 +
       50 +---
       51 +
       52 +## 📁 Project Structure
       53 +
       54 +```
       55  API/
       56  ├── model/
       10 -│   ├── pipeline.pkl        # Trained sklearn pipeline (preprocessor + XGBoost)
       11 -│   └── label_encoder.pkl   # Label encoder for target classes
       57 +│   ├── pipeline.pkl          # Trained sklearn pipeline (preprocessor + XGBoost)
       58 +│   └── label_encoder.pkl     # Label encoder for target classes
       59  ├── app/
       13 -│   ├── main.py             # FastAPI application
       14 -│   ├── predict.py          # Prediction logic
       15 -│   └── schemas.py          # Pydantic schemas
       16 -├── requirements.txt        # Python dependencies
       60 +│   ├── __init__.py
       61 +│   ├── main.py               # FastAPI application & endpoints
       62 +│   ├── predict.py            # Prediction logic & PalmPredictor class
       63 +│   └── schemas.py            # Pydantic input/output schemas
       64 +├── requirements.txt          # Python dependencies
       65  └── README.md
       66  ```
       67
       20 -## Installation
       68 +---
       69
       70 +## 🚀 Quick Start
       71 +
       72 +### Prerequisites
       73 +
       74 +- Python 3.10+
       75 +- pip
       76 +
       77 +### Installation
       78 +
       79  ```bash
       80 +# Clone or navigate to the API directory
       81  cd API
       82 +
       83 +# Install dependencies
       84  pip install -r requirements.txt
       85  ```
       86
       27 -## Running the API
       87 +### Run the Server
       88
       89  ```bash
       30 -uvicorn app.main:app --reload
       90 +# Development mode (auto-reload)
       91 +uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
       92 +
       93 +# Production mode
       94 +uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
       95  ```
       96
       33 -The API will be available at `http://localhost:8000`
       97 +### Test the API
       98
       35 -## Endpoints
       99 +```bash
      100 +# Health check
      101 +curl http://localhost:8000/
      102
       37 -### GET /
       38 -Health check endpoint.
      103 +# Make a prediction
      104 +curl -X POST "http://localhost:8000/predict" \
      105 +  -H "Content-Type: application/json" \
      106 +  -d '{
      107 +    "Variety": "Medjool",
      108 +    "Age": 10,
      109 +    "Height": 4.5,
      110 +    "Trunk_Diam": 1.0,
      111 +    "Salinity": 900.0,
      112 +    "Moisture": 30.0,
      113 +    "pH": 7.1,
      114 +    "Fronds_Count": 52,
      115 +    "Leaf_Color": "Dark_Green",
      116 +    "Irrigation_Uniformity": 92.0,
      117 +    "Root_Zone_Variance": 2.8,
      118 +    "Canopy_Temp_Delta": 1.4,
      119 +    "Phenological_Stage": 4,
      120 +    "Irrigation_Vol_L": 185.0,
      121 +    "Frond_Health_Ratio": 0.93
      122 +  }'
      123 +```
      124
       40 -### POST /predict
       41 -Make a prediction.
      125 +---
      126
       43 -**Request Body:**
      127 +## 📡 API Reference
      128 +
      129 +### `GET /`
      130 +Health check endpoint.
      131 +
      132 +**Response:**
      133  ```json
      134  {
       46 -  "Variety": "Medjool",
       47 -  "Age": 10,
       48 -  "Height": 4.5,
       49 -  "Trunk_Diam": 1.0,
       50 -  "Salinity": 900.0,
       51 -  "Moisture": 30.0,
       52 -  "pH": 7.1,
       53 -  "Fronds_Count": 52,
       54 -  "Leaf_Color": "Dark_Green",
       55 -  "Irrigation_Uniformity": 92.0,
       56 -  "Root_Zone_Variance": 2.8,
       57 -  "Canopy_Temp_Delta": 1.4,
       58 -  "Phenological_Stage": 4,
       59 -  "Irrigation_Vol_L": 185.0,
       60 -  "Frond_Health_Ratio": 0.93
      135 +  "status": "healthy",
      136 +  "model_loaded": true
      137  }
      138  ```
      139
      140 +---
      141 +
      142 +### `POST /predict`
      143 +Predict palm tree health status.
      144 +
      145 +**Request Body:**
      146 +| Field | Type | Description |
      147 +|-------|------|-------------|
      148 +| Variety | string | `Medjool`, `Siwi`, or `Barhi` |
      149 +| Age | integer | Age in years |
      150 +| Height | float | Height in meters |
      151 +| Trunk_Diam | float | Trunk diameter in meters |
      152 +| Salinity | float | Salinity level (ppm) |
      153 +| Moisture | float | Soil moisture percentage |
      154 +| pH | float | Soil pH level |
      155 +| Fronds_Count | integer | Number of fronds |
      156 +| Leaf_Color | string | `Dark_Green`, `Pale_Green`, `Yellowish_Green`, `Browning_Edges` |
      157 +| Irrigation_Uniformity | float | Irrigation uniformity percentage |
      158 +| Root_Zone_Variance | float | Root zone variance |
      159 +| Canopy_Temp_Delta | float | Canopy temperature delta |
      160 +| Phenological_Stage | integer | Growth stage (1-5) |
      161 +| Irrigation_Vol_L | float | Irrigation volume in liters |
      162 +| Frond_Health_Ratio | float | Frond health ratio (0-1) |
      163 +
      164  **Response:**
      165  ```json
      166  {
     ...
      169    "top_3": [
      170      {"status": "Healthy", "probability": 0.9995},
      171      {"status": "Partial_Clogging", "probability": 0.0005},
       72 -    {"status": "Maintenance_Issue", "probability": 0.0000}
      172 +    {"status": "Maintenance_Issue", "probability": 0.0}
      173    ],
      174    "health_score": 99.9
      175  }
      176  ```
      177
       78 -## Testing with curl
      178 +**Response Fields:**
      179 +| Field | Type | Description |
      180 +|-------|------|-------------|
      181 +| predicted_status | string | Predicted health condition |
      182 +| confidence | float | Model confidence (0-1) |
      183 +| top_3 | array | Top 3 predictions with probabilities |
      184 +| health_score | float | Overall health index (0-100) |
      185
       80 -```bash
       81 -curl -X POST "http://localhost:8000/predict" \
       82 -  -H "Content-Type: application/json" \
       83 -  -d '{
       84 -    "Variety": "Medjool",
       85 -    "Age": 10,
       86 -    "Height": 4.5,
       87 -    "Trunk_Diam": 1.0,
       88 -    "Salinity": 900.0,
       89 -    "Moisture": 30.0,
       90 -    "pH": 7.1,
       91 -    "Fronds_Count": 52,
       92 -    "Leaf_Color": "Dark_Green",
       93 -    "Irrigation_Uniformity": 92.0,
       94 -    "Root_Zone_Variance": 2.8,
       95 -    "Canopy_Temp_Delta": 1.4,
       96 -    "Phenological_Stage": 4,
       97 -    "Irrigation_Vol_L": 185.0,
       98 -    "Frond_Health_Ratio": 0.93
       99 -  }'
      186 +---
      187 +
      188 +## 🧠 Model Details
      189 +
      190 +### Training Configuration
      191 +
      192 +| Parameter | Value |
      193 +|-----------|-------|
      194 +| Algorithm | XGBoost Classifier |
      195 +| Objective | multi:softprob |
      196 +| Max Depth | 6 |
      197 +| Learning Rate | 0.05 |
      198 +| Estimators | 1000 (early stopping @ 50) |
      199 +| Subsample | 0.80 |
      200 +| Colsample_bytree | 0.80 |
      201 +| Reg Alpha | 0.10 |
      202 +| Reg Lambda | 1.50 |
      203 +
      204 +### Performance Metrics
      205 +
      206 +| Metric | Score |
      207 +|--------|-------|
      208 +| Accuracy | 95.58% |
      209 +| Balanced Accuracy | 94.19% |
      210 +| F1 Macro | 94.37% |
      211 +
      212 +### Detected Conditions (16 Classes)
      213 +
      214 +1. **Healthy** - Optimal health status
      215 +2. **Maintenance_Issue** - Requires attention
      216 +3. **Sensor_Fault** - Potential sensor error
      217 +4. **Partial_Clogging** - Irrigation blockage
      218 +5. **Mechanical_Stress** - Physical damage
      219 +6. **Leaching_Stress** - Nutrient leaching
      220 +7. **Nutrient_Deficiency** - Missing nutrients
      221 +8. **Fertilizer_Burn** - Over-fertilization
      222 +9. **Heat_Stress** - Temperature stress
      223 +10. **High_Alkalinity** - Elevated pH
      224 +11. **Salinity_Stress** - Salt stress
      225 +12. **Chronic_Drought** - Long-term water deficit
      226 +13. **Acute_Drought** - Severe water deficit
      227 +14. **Root_Suffocation** - Poor root aeration
      228 +15. **Critical_Multi_Stress** - Multiple severe stresses
      229 +16. **Alkaline_Shock** - Sudden pH increase
      230 +
      231 +### Health Score Mapping
      232 +
      233 +| Condition | Weight |
      234 +|-----------|--------|
      235 +| Healthy | 1.00 |
      236 +| Maintenance_Issue, Sensor_Fault | 0.90 |
      237 +| Partial_Clogging, Mechanical_Stress | 0.85 |
      238 +| Leaching_Stress, Mild_Stress | 0.80 |
      239 +| Nutrient_Deficiency, Fertilizer_Burn | 0.75 |
      240 +| Heat_Stress, High_Alkalinity | 0.70 |
      241 +| Salinity_Stress | 0.65 |
      242 +| Chronic_Drought | 0.60 |
      243 +| Acute_Drought | 0.50 |
      244 +| Root_Suffocation | 0.40 |
      245 +| Alkaline_Shock | 0.30 |
      246 +| Critical_Multi_Stress | 0.20 |
      247 +
      248 +---
      249 +
      250 +## 🧪 Testing
      251 +
      252 +### Using Python
      253 +
      254 +```python
      255 +import requests
      256 +
      257 +url = "http://localhost:8000/predict"
      258 +
      259 +payload = {
      260 +    "Variety": "Siwi",
      261 +    "Age": 12,
      262 +    "Height": 4.2,
      263 +    "Trunk_Diam": 0.93,
      264 +    "Salinity": 1800.0,
      265 +    "Moisture": 12.0,
      266 +    "pH": 7.3,
      267 +    "Fronds_Count": 45,
      268 +    "Leaf_Color": "Pale_Green",
      269 +    "Irrigation_Uniformity": 62.0,
      270 +    "Root_Zone_Variance": 14.5,
      271 +    "Canopy_Temp_Delta": 7.2,
      272 +    "Phenological_Stage": 2,
      273 +    "Irrigation_Vol_L": 58.0,
      274 +    "Frond_Health_Ratio": 0.54
      275 +}
      276 +
      277 +response = requests.post(url, json=payload)
      278 +print(response.json())
      279  ```
      280
      102 -## API Documentation
      281 +### Using Interactive Docs
      282
      104 -Interactive docs available at:
      105 -- Swagger UI: `http://localhost:8000/docs`
      106 -- ReDoc: `http://localhost:8000/redoc`
      283 +Open your browser to:
      284 +- **Swagger UI:** http://localhost:8000/docs
      285 +- **ReDoc:** http://localhost:8000/redoc
      286
      108 -## Model Details
      287 +---
      288
      110 -- **Algorithm**: XGBoost Classifier
      111 -- **Preprocessing**: StandardScaler (numeric) + OneHotEncoder (categorical)
      112 -- **Classes**: 16 health status categories
      113 -- **Accuracy**: ~95.5%
      289 +## 📦 Dependencies
      290 +
      291 +| Package | Version | Purpose |
      292 +|---------|---------|---------|
      293 +| FastAPI | >=0.104.0 | Web framework |
      294 +| Uvicorn | >=0.24.0 | ASGI server |
      295 +| Pydantic | >=2.0.0 | Data validation |
      296 +| XGBoost | >=2.0.0 | ML classifier |
      297 +| Scikit-Learn | >=1.3.0 | Preprocessing pipeline |
      298 +| Pandas | >=2.0.0 | Data handling |
      299 +| Joblib | >=1.3.0 | Model serialization |
      300 +
      301 +---
      302 +
      303 +## 🔒 Security Considerations
      304 +
      305 +- **Input Validation:** All requests validated against Pydantic schemas
      306 +- **No External Preprocessing:** Pipeline handles all transformations internally
      307 +- **Stateless:** No session data stored between requests
      308 +- **Model Isolation:** Model files loaded once at startup (singleton pattern)
      309 +
      310 +---
      311 +
      312 +## 🚀 Deployment
      313 +
      314 +### Docker
      315 +
      316 +```dockerfile
      317 +FROM python:3.11-slim
      318 +
      319 +WORKDIR /app
      320 +
      321 +COPY requirements.txt .
      322 +RUN pip install --no-cache-dir -r requirements.txt
      323 +
      324 +COPY . .
      325 +
      326 +CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
      327 +```
      328 +
      329 +### Environment Variables
      330 +
      331 +| Variable | Default | Description |
      332 +|----------|---------|-------------|
      333 +| HOST | 0.0.0.0 | Server bind address |
      334 +| PORT | 8000 | Server port |
      335 +| WORKERS | 1 | Number of worker processes |
      336 +
      337 +---
      338 +
      339 +## 📄 License
      340 +
      341 +This project is licensed under the MIT License.
      342 +
      343 +---
      344 +
      345 +## 👨‍💻 Author
      346 +
      347 +**Amar Hosny**
      348 +
      349 +---
      350 +
      351 +## 🤝 Contributing
      352 +
      353 +Contributions are welcome! Please feel free to submit a Pull Request.
      354 +
      355 +---
      356 +
      357 +## 📞 Support
      358 +
      359 +For issues or questions, please open an issue on the GitHub repository.
