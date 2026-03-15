from typing import Optional
from db import PlantDataType, PlantStorage

def create_plant_storage_tools(storage: PlantStorage):
    def save_plant(plant_data: PlantDataType) -> str:
        storage.save_plant(plant_data)
        return

    def get_plant(plant_name: str) -> Optional[PlantDataType]:
        return storage.get_plant(plant_name)

    return [save_plant, get_plant]