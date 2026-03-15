from abc import ABC, abstractmethod
from typing import Any, Optional, Dict

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

PlantDataType = Dict[str, Any]

class PlantStorage(ABC):
    @abstractmethod
    def save_plant(self, plant_data: PlantDataType) -> str:
        pass

    @abstractmethod
    def get_plant(self, plant_name: str) -> Optional[PlantDataType]:
        pass

class MongoPlantStorage(PlantStorage):
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))
        self.db = self.client["botanics"]
        self.collection = self.db["plants"]

    def save_plant(self, plant_data: PlantDataType) -> str:
        self.collection.insert_one(plant_data)
        return f"Saved to MongoDB"

    def get_plant(self, plant_name: str) -> Optional[PlantDataType]:
        query_filter = {}
        data = self.collection.find_one(filter=query_filter)
        return data