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
Step 1 [VERIFY]: Use 'get_plant_data' for the plant name provided.
Step 2 [RESEARCH]: If Step 1 yields no data, you MUST call 'SearchAgent' with the query: '[Plant Name] horticultural requirements and growth stages'.
Step 3 [EXTRACT]: Use ONLY the text returned by 'SearchAgent' to fill the PlantData schema.
Step 4 [SAVE]: Call 'save_plant_data' with the completed profile.

If 'SearchAgent' returns no results, stop and inform the user you could not find reliable data.
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
    tools=[
        AgentTool(
            agent=search_agent,
            description="Use this tool to search the internet for plant growth stages, NPK, pH, and temperature data if not found in the database."
            ),
        *create_plant_storage_tools(mongo_storage)
        ],
    output_schema=PlantData,
    output_key="plant_data"
)
 