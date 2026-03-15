from abc import ABC, abstractmethod
from typing import Any, Optional, Dict

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

from researcher_agent.schema import PlantData

load_dotenv()

class PlantStorage(ABC):
    @abstractmethod
    def save_plant(self, plant_data: PlantData) -> str:
        pass

    @abstractmethod
    def get_plant(self, plant_name: str) -> Optional[PlantData]:
        pass

class MongoPlantStorage(PlantStorage):
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))
        self.db = self.client["botanics"]
        self.collection = self.db["plants"]

    def save_plant(self, plant_data: PlantData) -> str:
        try:
            print(f"Saving plant data: {plant_data}")
            document = plant_data.model_dump() # .model_dump() converts Pydantic model to a dict for Mongo
            
            # Upsert based on scientific name to avoid duplicates
            result = self.collection.update_one(
                {"scientific_name": plant_data.scientific_name},
                {"$set": document},
                upsert=True
            )
            print(f"Result: {result}")
            return f"Successfully saved/updated: {result}"

        except PyMongoError as e:
            print(f"Database error: {str(e)}")
            return f"Database error: {str(e)}"

    def get_plant(self, plant_name: str) -> Optional[PlantData]:
        """Check if we already have this plant in the database."""
        # Search by common name or scientific name (case-insensitive)
        query = {
            "$or": [
                {"common_name": {"$regex": f"^{plant_name}$", "$options": "i"}},
                {"scientific_name": {"$regex": f"^{plant_name}$", "$options": "i"}}
            ]
        }
        return self.collection.find_one(query)