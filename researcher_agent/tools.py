from typing import Optional
from researcher_agent.db import PlantStorage
from researcher_agent.schema import PlantData

def create_plant_storage_tools(storage: PlantStorage):
    def save_plant_data(plant_data: PlantData) -> str:
        storage.save_plant(plant_data)
        return

    def get_plant_data_by_name(plant_name: str) -> Optional[PlantData]:
        return storage.get_plant(plant_name)

    return [save_plant_data, get_plant_data_by_name]