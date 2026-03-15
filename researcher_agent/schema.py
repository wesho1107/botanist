from typing import List, Optional
from pydantic import Annotated, BaseModel, Field
from enum import Enum

class LightExposure(Enum):
    full_sun = "FULL_SUN"
    part_sun = "PART_SUN"
    part_shade = "PART_SHADE"
    full_shade = "FULL_SHADE"
    low_indoor = "LOW_INDOOR"
    medium_indoor = "MEDIUM_INDOOR"
    high_indoor = "HIGH_INDOOR"

class WaterNeedLevel(Enum):
    very_low = "VERY_LOW"
    low = "LOW"
    medium = "MEDIUM"
    high = "HIGH"
    very_high = "VERY_HIGH"

class GrowthStage(Enum):
    germination = "GERMINATION"
    seedling = "SEEDLING"
    vegetative = "VEGETATIVE"
    flowering_fruiting = "FLOWERING_FRUITING"
    mature_maintenance = "MATURE_MAINTENANCE"

class BaseProfile(BaseModel):
    notes: Optional[str] = None

class QuantitativeRequirements(BaseModel):
    value_range: str = Field(..., description="e.g., '60-80%'")
    optimal: float = Field(..., description="The target value for automation")
    unit: Optional[str] = None

# Optimal nutrient required for plant
class NutrientProfile(BaseProfile):
    npk_ratio: str = Field(..., description="e.g, '10-20-30'")
    feeding_frequency_per_month: Optional[float]

class LightProfile(BaseProfile):
    daily_light_hours: QuantitativeRequirements
    light_intensity: QuantitativeRequirements

class WaterProfile(BaseProfile):
    watering_instructions: str
    need_level: Optional[WaterNeedLevel]
    frequency_per_week_min: Optional[float]
    frequency_per_week_max: Optional[float]

class SoilProfile(BaseProfile):
    soil_ph: Optional[QuantitativeRequirements]
    humidity: Optional[QuantitativeRequirements]

class AirProfile(BaseProfile):
    humidity: Optional[QuantitativeRequirements]
    temp_day_c: Optional[QuantitativeRequirements]
    temp_night_c: Optional[QuantitativeRequirements]

# Stage of plant: germination, seedling, etc.
class GrowthPhase(BaseModel):
    growth_stage: GrowthStage
    duration_days: Optional[str] = Field(..., description = "e.g., '~30 days'")

    light_requirements: Optional[LightProfile]
    water_requirements: Optional[WaterProfile]
    soil_requirements: Optional[SoilProfile]
    air_requirements: Optional[AirProfile]
    nutrients_requirements: Optional[NutrientProfile]

# Data representative of plant
class PlantData(BaseModel):
    common_name: str
    scientific_name: str
    summary: str = Field(..., description="A brief summary of the plant and its growth characteristics")
    lifecycle: List[GrowthPhase]