from typing import List, Optional
from pydantic import Annotated, BaseModel, Field

# Environment need type
class EnvironmentalNeed(BaseModel):
    value_range: str = Field(..., description="e.g., '60-80%'")
    optimal: float = Field(..., description="The target value for automation")
    unit: Optional[str] = None
    notes: Optional[str] = None

# Optimal nutrient required for plant
class NutrientProfile(BaseModel):
    npk_ratio: str = Field(..., description="e.g, '10-20-30'")
    frequency_days: int

# Stage of plant: germination, seedling, etc.
class GrowthPhase(BaseModel):
    phase_name: str
    duration_days: Optional[str] = Field(..., description = "e.g., '~30 days'")

    light_intensity: EnvironmentalNeed
    light_hours: EnvironmentalNeed
    temp_day_c: EnvironmentalNeed
    temp_night_c: EnvironmentalNeed
    soil_ph: EnvironmentalNeed

    watering_instructions: str = Field(..., description="Millilitres of water per day")
    nutrients: Optional[NutrientProfile] = None

# Data representative of plant
class PlantData(BaseModel):
    common_name: str
    scientific_name: str
    summary: str
    lifecycle: List[GrowthPhase]