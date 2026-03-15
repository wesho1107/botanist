from typing import List, Optional
from pydantic import BaseModel, Field
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
    value_range: Optional[str] = Field(None, description="e.g., '60-80%'")
    optimal: Optional[float] = Field(None, description="The target value for automation")
    unit: Optional[str] = None

# Optimal nutrient required for plant
class NutrientProfile(BaseProfile):
    npk_ratio: Optional[str] = Field(None, description="e.g, '10-20-30'")
    feeding_frequency_per_month: Optional[float] = None

class LightProfile(BaseProfile):
    daily_light_hours: Optional[QuantitativeRequirements] = None
    light_intensity: Optional[QuantitativeRequirements] = None

class WaterProfile(BaseProfile):
    watering_instructions: Optional[str] = None
    need_level: Optional[WaterNeedLevel] = None
    frequency_per_week_min: Optional[float] = None
    frequency_per_week_max: Optional[float] = None

class SoilProfile(BaseProfile):
    soil_ph: Optional[QuantitativeRequirements] = None
    humidity: Optional[QuantitativeRequirements] = None

class AirProfile(BaseProfile):
    humidity: Optional[QuantitativeRequirements] = None
    temp_day_c: Optional[QuantitativeRequirements] = None
    temp_night_c: Optional[QuantitativeRequirements] = None

# Stage of plant: germination, seedling, etc.
class GrowthPhase(BaseModel):
    growth_stage: GrowthStage
    duration_days: Optional[str] = Field(None, description = "e.g., '~30 days'")

    light_requirements: Optional[LightProfile] = None
    water_requirements: Optional[WaterProfile] = None
    soil_requirements: Optional[SoilProfile] = None
    air_requirements: Optional[AirProfile] = None
    nutrients_requirements: Optional[NutrientProfile] = None

# Data representative of plant
class PlantData(BaseModel):
    common_name: str
    scientific_name: str
    summary: str = Field(..., description="A brief summary of the plant and its growth characteristics")
    lifecycle: List[GrowthPhase]