from pydantic import BaseModel, Field
from typing import Literal

class GuardFeedback(BaseModel):
    risk_score: int = Field(..., ge=0, le=10, description="0 is safe, 10 is critical failure")
    is_hallucination: bool = Field(..., description="True if the agent made up data")
    recommended_action: Literal["continue", "intercept", "retry"]
    reasoning: str = Field(..., description="Brief explanation for the score")