from typing import List, Optional
from pydantic import BaseModel, Field

class GrowthPhase(BaseModel):
    # Core Phase Info
    growth_stage: str
    duration_days: Optional[str] = Field(None, description="e.g., '~30 days'")
    
    # Light Requirements
    light_hours_range: Optional[str] = Field(None, description="e.g., '12-14 hours'")
    light_hours_optimal: Optional[float] = None
    light_intensity_value: Optional[str] = Field(None, description="e.g., '600-800 PPFD'")
    light_notes: Optional[str] = None

    # Water Requirements
    watering_instructions: Optional[str] = None
    water_need_level: Optional[str] = Field(None, description="Low, Medium, or High")
    water_freq_week_min: Optional[float] = None
    water_freq_week_max: Optional[float] = None
    water_notes: Optional[str] = None

    # Soil & Air
    soil_ph_optimal: Optional[float] = None
    soil_humidity_optimal: Optional[float] = None
    air_humidity_range: Optional[str] = None
    air_temp_day_c_optimal: Optional[float] = None
    air_temp_night_c_optimal: Optional[float] = None
    
    # Nutrients
    npk_ratio: Optional[str] = Field(None, description="e.g., '10-20-10'")
    feeding_frequency_per_month: Optional[float] = None

class PlantData(BaseModel):
    common_name: str
    scientific_name: str
    summary: str = Field(..., description="Brief summary of the plant")
    research_sources: List[str] = Field(..., description="List of URLs used to find this data. MANDATORY.")
    # keep 'lifecycle' as a list because a plant has multiple distinct stages
    lifecycle: List[GrowthPhase]