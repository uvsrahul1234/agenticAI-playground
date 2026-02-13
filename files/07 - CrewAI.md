## CrewAI

We will be using UV to work with CrewAI. Crews are valuable when you need autonomous problem-solving, creative collaborations, or exploratory tasks.



* crewai create crew project_name
* Creates 
    * agents.yaml
    * tasks.yaml
    * crew.py
    * main.py
* Select a provider…
    * 1. Openai
* Select a model…
    * Gpt-4o-mini
* Enter key
    * Enter key to skip because we already have a key
* Check new folders out (may need to create another folder for traditional folder structure)
* Config
    * Agents.yaml (provides template code, scaffolding)
        * In Agents.yaml add the model for each role such as model: llm: openai/gpt-4o-mini and llm: anthropic/claude-3-7-sonnet-latest
        * See LightLLM
    * Tasks.yaml (provides template code)
        * In tasks.yaml add output_file: output/research.md, etc
* Tools
    * Custom_tools.py (provides template code)
* crew.py (provides template code)
* main.py (provides template code)
    * Def run(): \
Try: \
Result = Debate().crew().kickoff(input=inputs) \
Print(result.raw)
* Cd project_name
* Remove newly created env file (assumes you have .env in the parent directory)
* crewai run
