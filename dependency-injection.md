## Overview
This markdown file serves as a personal development log to highlight certain decisions made and learnings from this project. In this case, it is about reducing coupling between components in an agentic system by dependency injection.

## Motivation
What motivated the need for reducing coupling is the changing choices of databases in the future. Currently, I am making use of MongoDB as my database to store information about plants, where the agent interacts with through tool use. The initial code had high coupling between the agent and MongoDB client.
```python
# tools.py
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))
db = client["farm"]
plants_collection = db["plants"]

def save_plant(plant_data) -> str:
    try:
        result = plants_collection.update_one(...)
    except Exception as e:
        return f"Error"

def get_plant(plant_name) -> str:
    try:
        ...
    except Exception as e:
        return f"Error"
```

In the case where the user needs to change the database from MongoDB to PostgreSQL or local storage/mock for testing, he will have to change the code at several places: changing the provider, changing internal implementation depending on database API. 


## Solutions

### Abstract classes / interfaces as contract of the tool functions

An abstract method is a method declared without implementation but defines a method signature that subclasses are required to follow. The idea is to create an abstract class for any database providers such that they folow this "contract", ensuring that regardless of which database is chosen, they will provide the same method signatures to be used.

```python
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from pymongo import MongoClient

class Storage(ABC):
    @abstractmethod
    def save_plant(self, plant_data) -> str:
        pass

    @abstractmethod
    def get_plant(self, plant_name) -> str:
        pass

class MongoStorage(Storage):
    def __init__(self, connection_uri: str):
        self.client = MongoClient(...)

    def save_plant(self, plant_data) -> str:
        # Mongo-specific logic: collection.update_one(...)

    def get_plant(self, plant_name) -> str:
        # Mongo-specific logic: collection.find_one(...)

class PostgreSQLStorage(Storage):
    def __init__(self, connection_uri: str):
        # Setup local storage

    def save_plant(self, plant_data) -> str:
        # Logic to save to local JSON or csv

    def get_plant(self, plant_name) -> str:
        # Logic to read from local file
```

With this, the idea formed is to use these instead of coupling the database for your tools.


### Injecting and binding storage to agent tools

Initially, the idea of dependency injection is to pass the dependency into a scope where it is needed. In our case, passing the storage of choice as argument in the function tools.
```python
def save_plant_to_db(storage: Storage, plant_data: dict) -> str:
    # Implementation details

def get_plant_from_db(storage: Storage, plant_data: dict) -> str:
    # Implementation details
```

While this approach follows the spirit of dependency injection by referencing the interfaces, for agents it will not work well.

In most agent frameworks, the agent calls a tool by providing only the arguments it "understands". In our use case for an agent that researches about plants, it only knows arguments like `plant_name` or `plant_data`. The agent will not know how to provide `storage` object. Since from the LLM's perspective it does not understand what `storage` object is or how to instantiate one, there will be execution errors when agent tries to call the tool: failing to provide the argument or even "hallucinate" an invalid storage parameter.


### Closure/Factory approach
To resolve the issue above, a simple method is to use Factory pattern and bind `storage` to the closure of the tool functions instead of providing as a parameter
```python
def create_tool_functions(storage: Storage):
    def save_plant_to_db(plant_data: dict) -> str:
        # Implementation details

    def get_plant_from_db(plant_data: dict) -> str:
        # Implementation details
    
    return [save_plant_to_db, get_plant_from_db]

mongo_storage = MongoClient(...)
# The agent only sees functions that takes plant_data or plant_name
# Storage already binded to the scope/closure of these tool functions
tool_functions = create_tool_functions(mongo_storage) # can subsequently be passed to agent
```


### Dependency Injector Framework (in consideration for learning)