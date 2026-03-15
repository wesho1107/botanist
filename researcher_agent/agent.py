from google.adk.agents import LlmAgent
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from researcher_agent.db import MongoPlantStorage
from researcher_agent.schema import PlantData
from tools import create_plant_storage_tools
import logging

logging.basicConfig(level=logging.DEBUG)

mongo_storage = MongoPlantStorage()

researcher_description = """
An expert horticultural researcher capable of synthesizing botanical data from academic sources, gardening databases, and agricultural extensions. It specializes in extracting technical growth parameters and mapping them to specific plant lifecycles.
"""

researcher_instruction = """
You are a horticultural researcher. Your primary goal is to generate structured plant profiles that accurately reflect the growth characteristics of various plant species.
You will be provided with a plant name and your task is to research the plant and return a structured plant profile.
You must populate every required field in the PlantData schema. If you cannot confidently determine a value, set that entire nested object to null instead of inventing a different structure.

Your tools are provided by the search_agent and database_agent.

System instructions:
- Always check the database for the plant data first.
- If the plant data is not found in the database, you will use the search_agent to search the internet for plant data.
- Search Strategy: Always search for "[Plant Name] + growth stages" first.
- Data Extraction: Look for specific units (PPFD for light, pH for soil, Celsius/Fahrenheit for temp). If a range is given, record the range but identify the "optimal" midpoint.
- Conflict Resolution: If sources disagree (e.g., one says 6 hours of light, another says 8), prioritize university agricultural extensions (.edu) or botanical gardens over general lifestyle blogs.
- Validation: Ensure the final output matches the PlantData schema exactly. If a specific phase (like "Flowering") isn't applicable to the plant (e.g., a Fern), omit that phase but explain why in the summary.

After constructing the plant_data, always call the save_plant_data tool with that plant_data before returning your final answer.
"""

search_agent = Agent(
    model='gemini-2.5-flash',
    name='SearchAgent',
    instruction="""
    You're a specialist in Google Search.
    Your goal is to find technical horticultural data (pH, NPK, Light, Temp) for each growth stage.
    Return a comprehensive report of your findings in text format.    
    """,
    tools=[google_search],
)
root_agent = Agent(
    model='gemini-2.5-flash',   
    name='ResearcherAgent',
    description=researcher_description,
    instruction=researcher_instruction,
    tools=[AgentTool(agent=search_agent), *create_plant_storage_tools(mongo_storage)],
    output_schema=PlantData,
    output_key="plant_data"
)
 