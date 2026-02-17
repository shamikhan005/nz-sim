# data model

from pydantic import BaseModel
from typing import Dict, Optional

class Transport(BaseModel):
    distance_km: float
    fuel_liters: float

class ScenarioInput(BaseModel):
    energy_mix: Dict[str, float]
    production_output: float
    energy_intensity_kwh_per_unit: float
    transport: Transport
    reported_co2_tons: float
    sustainability_claim: Optional[str] = None
