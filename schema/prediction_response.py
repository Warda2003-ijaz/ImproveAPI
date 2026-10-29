from pydantic import BaseModel, Field
from typing import Dict

class PredictionResponse(BaseModel):
    predicted_risk: str = Field(..., description="High, Medium ya Low", examples=["Low"])
    confidence: float = Field(..., ge=0, le=1, description="Model kitna confident hai", examples=[0.85])
    class_probabilities: Dict[str, float] = Field(..., examples=[{"High": 0.05, "Low": 0.85, "Medium": 0.10}])