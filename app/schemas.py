"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field
from typing import List, Literal


class PalmInput(BaseModel):
    """Input schema for palm tree prediction."""

    Variety: Literal["Medjool", "Siwi", "Barhi"] = Field(
        ...,
        description="Palm variety"
    )
    Age: int = Field(..., description="Age in years")
    Height: float = Field(..., description="Height in meters")
    Trunk_Diam: float = Field(..., description="Trunk diameter in meters")
    Salinity: float = Field(..., description="Salinity level (ppm)")
    Moisture: float = Field(..., description="Soil moisture percentage")
    pH: float = Field(..., description="Soil pH level")
    Fronds_Count: int = Field(..., description="Number of fronds")
    Leaf_Color: Literal["Dark_Green", "Pale_Green", "Yellowish_Green", "Browning_Edges"] = Field(
        ...,
        description="Leaf color observation"
    )
    Irrigation_Uniformity: float = Field(..., description="Irrigation uniformity percentage")
    Root_Zone_Variance: float = Field(..., description="Root zone variance")
    Canopy_Temp_Delta: float = Field(..., description="Canopy temperature delta")
    Phenological_Stage: int = Field(..., description="Phenological growth stage (1-5)")
    Irrigation_Vol_L: float = Field(..., description="Irrigation volume in liters")
    Frond_Health_Ratio: float = Field(..., description="Frond health ratio (0-1)")


class PredictionResult(BaseModel):
    """Single prediction result."""

    status: str
    probability: float


class PalmPredictionResponse(BaseModel):
    """Response schema for prediction endpoint."""

    predicted_status: str
    confidence: float
    top_3: List[PredictionResult]
    health_score: float


class HealthCheck(BaseModel):
    """Health check response."""

    status: str
    model_loaded: bool
