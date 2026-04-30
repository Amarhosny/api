"""Prediction logic using the trained pipeline."""

import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any

# Model files location
MODEL_DIR = Path(__file__).parent.parent / "model"
PIPELINE_PATH = MODEL_DIR / "pipeline.pkl"
LABEL_ENCODER_PATH = MODEL_DIR / "label_encoder.pkl"

# Health score weights per class
HEALTH_WEIGHTS = {
    "Healthy": 1.0,
    "Maintenance_Issue": 0.9,
    "Sensor_Fault": 0.9,
    "Partial_Clogging": 0.85,
    "Mechanical_Stress": 0.85,
    "Leaching_Stress": 0.8,
    "Mild_Stress": 0.8,
    "Nutrient_Deficiency": 0.75,
    "Fertilizer_Burn": 0.75,
    "Heat_Stress": 0.7,
    "High_Alkalinity": 0.7,
    "Salinity_Stress": 0.65,
    "Chronic_Drought": 0.6,
    "Acute_Drought": 0.5,
    "Root_Suffocation": 0.4,
    "Critical_Multi_Stress": 0.2,
    "Alkaline_Shock": 0.3,
}


class PalmPredictor:
    """Singleton predictor that loads and caches the model pipeline."""

    _instance = None
    _pipeline = None
    _label_encoder = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load(self) -> None:
        """Load the pipeline and label encoder from disk."""
        if self._pipeline is None:
            self._pipeline = joblib.load(PIPELINE_PATH)
        if self._label_encoder is None:
            self._label_encoder = joblib.load(LABEL_ENCODER_PATH)

    @property
    def pipeline(self):
        """Lazy-load the pipeline."""
        if self._pipeline is None:
            self.load()
        return self._pipeline

    @property
    def label_encoder(self):
        """Lazy-load the label encoder."""
        if self._label_encoder is None:
            self.load()
        return self._label_encoder

    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict palm tree health status from a single sample.

        Parameters
        ----------
        input_data : dict
            Dictionary containing all required features.

        Returns
        -------
        dict
            Prediction results with status, confidence, top_3, and health_score.
        """
        # Convert dict to DataFrame (single row)
        input_df = pd.DataFrame([input_data])

        # Get prediction and probabilities
        pred_idx = self.pipeline.predict(input_df)[0]
        probabilities = self.pipeline.predict_proba(input_df)[0]
        class_names = self.label_encoder.classes_

        # Predicted status
        predicted_status = self.label_encoder.inverse_transform([pred_idx])[0]
        confidence = float(probabilities[pred_idx])

        # Top 3 predictions
        top3_indices = np.argsort(probabilities)[::-1][:3]
        top_3 = [
            {
                "status": self.label_encoder.inverse_transform([idx])[0],
                "probability": round(float(probabilities[idx]), 4)
            }
            for idx in top3_indices
        ]

        # Health score (weighted sum of probabilities * 100)
        health_score = 0.0
        for prob, cls in zip(probabilities, class_names):
            weight = HEALTH_WEIGHTS.get(cls, 0.5)
            health_score += prob * weight
        health_score = round(health_score * 100, 1)

        return {
            "predicted_status": predicted_status,
            "confidence": confidence,
            "top_3": top_3,
            "health_score": health_score,
        }


# Global predictor instance
predictor = PalmPredictor()


def predict_palm(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function for making predictions.

    Parameters
    ----------
    input_data : dict
        Input features dictionary.

    Returns
    -------
    dict
        Prediction results.
    """
    return predictor.predict(input_data)
