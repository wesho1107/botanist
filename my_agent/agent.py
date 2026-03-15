from google.adk.agents.llm_agent import Agent
from my_agent.db import MongoPlantStorage
from tools import create_plant_storage_tools

mongo_storage = MongoPlantStorage()

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Tells the current time in a specified city.",
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    tools=create_plant_storage_tools(mongo_storage)
)
 