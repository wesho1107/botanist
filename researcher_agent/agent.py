from google.adk.agents import LlmAgent
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from researcher_agent.db import MongoPlantStorage
from researcher_agent.schema import PlantData
from researcher_agent.tools import create_plant_storage_tools
import logging

logging.basicConfig(level=logging.DEBUG)

mongo_storage = MongoPlantStorage()

researcher_description = """
An expert horticultural researcher capable of synthesizing botanical data from academic sources, gardening databases, and agricultural extensions. It specializes in extracting technical growth parameters and mapping them to specific plant lifecycles.
"""

researcher_instruction = researcher_instruction = """
You are a horticultural research agent that MUST follow this procedure for every user question about a plant:
Step 1 [VERIFY]:
- Extract the plant name and (if given) the growth stage from the user message.
- Call the tool 'get_plant_data' with the plant name.
Step 2 [CHECK CACHE]:
- If 'get_plant_data' returns a PlantData object, use ONLY that data to answer the user.
- Do NOT invent values that are not present in PlantData. If something is missing, say that it is unknown.
Step 3 [RESEARCH IF MISSING]:
- If 'get_plant_data' returns no data, you MUST call 'SearchAgent' with a query like:
  "[Plant Name] horticultural requirements and growth stages"
- Use ONLY the text returned by 'SearchAgent' to fill a complete PlantData object.
Step 4 [SAVE]:
- Call 'save_plant_data' with the completed PlantData object so it is stored for future questions.
Step 5 [ANSWER USER]:
- Using the PlantData (from Step 2 or Step 4), answer the user’s question in clear, natural language.
- Focus only on the specific parameter(s) they asked about (e.g., "How long should a common carrot receive sunlight when it is still a baby?").
- Explicitly mention which growth stage you are referring to and give concrete, practical guidance.
If 'SearchAgent' returns no reliable results, clearly tell the user that you could not find trustworthy data and do NOT guess.
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
    name='researcher_agent',
    description=researcher_description,
    instruction=researcher_instruction,
    tools=[
        AgentTool(
            agent=search_agent,
        ),
        *create_plant_storage_tools(mongo_storage)
        ],
)
 