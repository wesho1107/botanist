## Botanist Researcher Agent

This project provides a horticultural research agent powered by Google's Agent Development Kit (ADK) and backed by MongoDB for caching structured plant data.

### 1. Environment setup

- **Install Python**
  - Use **Python 3.12** (recommended).

- **Create and activate a virtual environment**

  ```bash
  python -m venv .venv
  # On macOS / Linux (bash)
  source .venv/bin/activate

  # On Windows (PowerShell)
  .venv\Scripts\Activate.ps1
  ```

### 2. Install dependencies

- **Install from `requirements.txt`**

  From the project root:

  ```bash
  pip install -r requirements.txt
  ```

### 3. Create `.env` file

In the `researcher_agent` folder (or alongside your agent code), create a `.env` file with the following variables:

```bash
GOOGLE_API_KEY=your_google_api_key_here
MONGODB_URI=your_mongodb_uri_here
```

Make sure `MONGODB_URI` points to a running MongoDB instance the agent can access.

### 4. Running the agent

- **From the root directory (where the agent folders live)** you can launch the web UI:

  ```bash
  adk web
  ```

- **To run a specific agent from its folder**, use:

  ```bash
  adk run <agent_folder>
  ```

For this project, if your folder is named `researcher_agent`, you would run:

```bash
adk run researcher_agent
```

### 5. Common issues

- **Agent folder name must match `root_agent` name**

  The folder name for the agent **must** be the same as the `name` of the `root_agent`. In this project, the root agent is defined in `researcher_agent/agent.py` like this:

  ```python
  root_agent = Agent(
      model="gemini-2.5-flash",
      name="researcher_agent",
      description=researcher_description,
      instruction=researcher_instruction,
      tools=[
          AgentTool(agent=search_agent),
          *create_plant_storage_tools(mongo_storage),
      ],
  )
  ```

  - **Folder name requirement**: The folder that contains this agent code should be named:

    ```text
    researcher_agent
    ```

  - If the folder name and the `root_agent` name do **not** match (for example, a typo like `reseracher_agent`), `adk run` / `adk web` may fail to locate or load the agent correctly.

  - If you change the `name` field of `root_agent`, make sure to also rename the folder to match.

