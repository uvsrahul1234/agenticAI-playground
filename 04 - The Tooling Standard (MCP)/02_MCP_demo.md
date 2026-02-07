# Module 04: The Tooling Standard (MCP)
## Instructor-Led Demonstration Script

**Duration:** 45-60 Minutes  
**Goal:** Live coding session where students observe the workflow, debug errors with the instructor, and analyze results in real-time using the Predict-Observe-Explain (POE) methodology.

**Source Material:** `MCP.ipynb` and supporting Python files

---

## Pre-Demo Setup Checklist

Before students arrive or at the start of class:

- [ ] Open terminal/command prompt
- [ ] Navigate to the demo directory
- [ ] Have three files ready (will create during demo):
  - `task_manager.py` (business logic)
  - `task_manager_server.py` (MCP server entry point)
  - `database.py` (data persistence)
- [ ] Have a Jupyter notebook or Python script ready for agent interaction
- [ ] Ensure `uv` is installed and in PATH
- [ ] Have environment variables set (API keys in `.env` file)
- [ ] Open the glossary document for reference

---

## Phase 1: Environment & Safety Check (15 minutes)

### 1.1 The "Wrong" Way (Intentional Error Demonstration)

**Instructor Note:** We deliberately start with a mistake to teach debugging skills.

**Say to Students:**  
*"Let's start by trying to run an MCP server the 'obvious' way—and watch it fail. Understanding common mistakes helps you debug faster later."*

#### Demo Step 1: Create a Simple Function File

Create `simple_function.py`:

```python
def greet(name: str) -> str:
    """Returns a greeting message."""
    return f"Hello, {name}!"

# This is what students often try first
if __name__ == "__main__":
    print(greet("World"))
```

#### Demo Step 2: Try to Use It Directly (This Will Fail)

In a Jupyter notebook or Python file:

```python
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

# INTENTIONAL ERROR: Wrong params format
params = {"command": "python", "args": ["simple_function.py"]}

async with MCPServerStdio(params=params) as server:
    tools = await server.list_tools()
    print(tools)
```

**PREDICT (Ask Students Before Running):**
*"What do you think will happen when we run this? Will it work? If not, what error might we see?"*

**OBSERVE (Run the Code):**
You'll likely see an error like:
```
Error: No tools found or server failed to start
```

**EXPLAIN:**
*"The server started, but it didn't expose any tools. Why? Because the MCP framework needs a specific entry point—we can't just run any Python file. We need to use `uv run` and properly import functions."*

---

### 1.2 The "Right" Way (Security & Proper Setup)

**Say to Students:**  
*"Now let's set up the environment correctly. We'll address three critical aspects: dependency management, environment security, and proper MCP server structure."*

#### Demo Step 3: Check uv Installation

```bash
# Run in terminal
uv --version
```

**If not installed:**
```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Demo Step 4: Demonstrate API Key Security

**Wrong Way (Show but Don't Do):**
```python
# ❌ NEVER DO THIS
openai_api_key = "sk-1234567890abcdef"  # Hardcoded = SECURITY VIOLATION
```

**Right Way:**
```python
# ✅ Correct approach
from dotenv import load_dotenv
import os

load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment")
```

Create `.env` file (show on screen but don't commit to version control):
```
OPENAI_API_KEY=sk-your-actual-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**DISCUSS:**
*"Why is this critical? If you hardcode keys and push to GitHub, bots will find and exploit them within minutes. Always use environment variables."*

---

## Phase 2: Core Task - Building a Task Manager MCP Server (25 minutes)

### 2.1 Create the Data Persistence Layer

**Say to Students:**  
*"We'll build from the bottom up: first data storage, then business logic, then the MCP server. This is the professional way to structure applications."*

#### Demo Step 5: Create `database.py`

**PREDICT:**  
*"Before I write this, what do we need for basic data persistence? What operations should a database layer support?"*

(Expected answers: read, write, logging)

**Code:**
```python
# database.py
import json
import os
from datetime import datetime

DATA_DIR = "data"

# Create data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
    print(f"Created {DATA_DIR} directory")

def _get_filepath(name: str, prefix: str) -> str:
    """Helper function to generate consistent file paths."""
    return os.path.join(DATA_DIR, f"{prefix}_{name}.json")

def read_task_list(name: str):
    """Reads a task list from disk. Returns None if not found."""
    filepath = _get_filepath(name, "tasklist")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

def write_task_list(name: str, data: dict):
    """Writes a task list to disk."""
    filepath = _get_filepath(name, "tasklist")
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Saved task list '{name}' to {filepath}")

def write_log(name: str, module: str, message: str):
    """Appends a log entry for debugging and audit purposes."""
    log_filepath = _get_filepath(name, "log")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}][{module}] {message}\n"
    with open(log_filepath, 'a') as f:
        f.write(log_entry)
```

**OBSERVE:**  
Run a quick test:
```python
# In Jupyter or Python console
from database import write_log

write_log("demo", "test", "Database layer working!")
# Check that data/log_demo.json was created
```

**EXPLAIN:**  
*"Notice the separation of concerns. This module knows nothing about tasks or MCP—it just handles files. We can swap this for PostgreSQL later without changing other code."*

---

### 2.2 Create the Business Logic Layer

#### Demo Step 6: Create `task_manager.py` (Part 1 - Models)

**Say to Students:**  
*"Now we define what a 'task' and 'task list' actually are using Pydantic for data validation."*

```python
# task_manager.py
from pydantic import BaseModel
from datetime import datetime
from typing import Dict
from database import write_task_list, read_task_list, write_log

class Task(BaseModel):
    """Represents a single task with validation."""
    id: int
    description: str
    is_completed: bool = False
    created_at: str

    def __repr__(self):
        status = "✓" if self.is_completed else "○"
        return f"[{status}] Task {self.id}: {self.description}"

class TaskList(BaseModel):
    """Represents a collection of tasks."""
    name: str
    tasks: Dict[int, Task] = {}
    next_task_id: int = 1

    @classmethod
    def get(cls, name: str):
        """Load existing task list or create new one."""
        data = read_task_list(name.lower())
        if not data:
            data = {
                "name": name.lower(),
                "tasks": {},
                "next_task_id": 1
            }
            write_task_list(name.lower(), data)
        
        # Convert task dicts back to Task objects
        if 'tasks' in data and isinstance(data['tasks'], dict):
            data['tasks'] = {int(k): Task(**v) for k, v in data['tasks'].items()}
        
        return cls(**data)

    def save(self):
        """Persist current state to disk."""
        serializable_tasks = {k: v.model_dump() for k, v in self.tasks.items()}
        data_to_save = self.model_dump()
        data_to_save['tasks'] = serializable_tasks
        write_task_list(self.name.lower(), data_to_save)
```

**PREDICT:**  
*"Why are we using Pydantic's `BaseModel` instead of regular Python classes or dictionaries?"*

(Expected answers: validation, type checking, automatic JSON serialization)

**EXPLAIN:**  
*"Pydantic enforces that `id` must be an integer and `description` must be a string. If corrupted data tries to load, we'll get a clear error instead of silent failures downstream."*

---

#### Demo Step 7: Create `task_manager.py` (Part 2 - Tool Functions)

**Say to Students:**  
*"These are the actual tools that will be exposed through MCP. Notice they're standalone functions, not class methods."*

```python
# Continue in task_manager.py

def create_task_list(name: str) -> str:
    """
    Initializes a new empty task list.
    This will be exposed as an MCP tool.
    """
    try:
        task_list = TaskList.get(name)
        if task_list.tasks or task_list.next_task_id > 1:
            return f"Task list '{name}' already exists."
        else:
            task_list.save()
            write_log(name, "task_manager", f"Created new task list '{name}'")
            return f"✓ Task list '{name}' created successfully."
    except Exception as e:
        write_log(name, "task_manager", f"Error creating '{name}': {e}")
        return f"✗ Error: {e}"

def add_task(list_name: str, task_description: str) -> str:
    """
    Adds a new task to the specified list.
    This will be exposed as an MCP tool.
    """
    try:
        task_list = TaskList.get(list_name)
        new_task_id = task_list.next_task_id
        
        new_task = Task(
            id=new_task_id,
            description=task_description,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        task_list.tasks[new_task_id] = new_task
        task_list.next_task_id += 1
        task_list.save()
        
        write_log(list_name, "task_manager", f"Added task {new_task_id}: '{task_description}'")
        return f"✓ Task '{task_description}' added with ID: {new_task_id}"
    except Exception as e:
        write_log(list_name, "task_manager", f"Error adding task: {e}")
        return f"✗ Error: {e}"

def complete_task(list_name: str, task_id: int) -> str:
    """
    Marks a task as completed.
    This will be exposed as an MCP tool.
    """
    try:
        task_list = TaskList.get(list_name)
        
        if task_id not in task_list.tasks:
            return f"✗ Task ID {task_id} not found in '{list_name}'"
        
        task = task_list.tasks[task_id]
        if task.is_completed:
            return f"Task {task_id} is already completed"
        
        task.is_completed = True
        task_list.save()
        
        write_log(list_name, "task_manager", f"Completed task {task_id}")
        return f"✓ Task {task_id} marked as complete"
    except Exception as e:
        return f"✗ Error: {e}"

def list_tasks(list_name: str, include_completed: bool = False) -> str:
    """
    Returns all tasks in a list.
    This will be exposed as an MCP tool.
    """
    try:
        task_list = TaskList.get(list_name)
        tasks_to_return = []
        
        for task_id in sorted(task_list.tasks.keys()):
            task = task_list.tasks[task_id]
            if include_completed or not task.is_completed:
                tasks_to_return.append(task.model_dump())
        
        if not tasks_to_return:
            return f"No tasks found in '{list_name}'"
        
        import json
        return json.dumps(tasks_to_return, indent=2)
    except Exception as e:
        return f"✗ Error: {e}"
```

**CRITICAL QUESTION (Ask Students):**  
*"Why are these standalone functions instead of methods of the `TaskList` class?"*

**EXPLAIN:**  
*"MCP servers need to discover functions at the module level. If these were methods, the MCP framework would need to create a TaskList instance first—adding complexity. This 'manager pattern' separates the data model (TaskList class) from the service layer (these functions)."*

---

### 2.3 Create the MCP Server

#### Demo Step 8: Create `task_manager_server.py`

```python
# task_manager_server.py
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio
import json

from task_manager import (
    create_task_list,
    add_task,
    complete_task,
    list_tasks
)

# Create the server instance
server = Server("task-manager")

@server.list_tools()
async def list_available_tools() -> list[Tool]:
    """List all available task management tools."""
    return [
        Tool(
            name="create_task_list",
            description="Create a new task list",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the task list"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="add_task",
            description="Add a new task to a list",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_name": {
                        "type": "string",
                        "description": "Name of the task list"
                    },
                    "task_description": {
                        "type": "string",
                        "description": "Description of the task"
                    }
                },
                "required": ["list_name", "task_description"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_name": {
                        "type": "string",
                        "description": "Name of the task list"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to complete"
                    }
                },
                "required": ["list_name", "task_id"]
            }
        ),
        Tool(
            name="list_tasks",
            description="List all tasks in a task list",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_name": {
                        "type": "string",
                        "description": "Name of the task list"
                    },
                    "include_completed": {
                        "type": "boolean",
                        "description": "Include completed tasks",
                        "default": False
                    }
                },
                "required": ["list_name"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "create_task_list":
            result = create_task_list(arguments["name"])
        elif name == "add_task":
            result = add_task(arguments["list_name"], arguments["task_description"])
        elif name == "complete_task":
            result = complete_task(arguments["list_name"], arguments["task_id"])
        elif name == "list_tasks":
            include_completed = arguments.get("include_completed", False)
            result = list_tasks(arguments["list_name"], include_completed)
        else:
            result = f"Unknown tool: {name}"
        
        return [TextContent(type="text", text=result)]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    """Run the server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**EXPLAIN:**  
In this MCP implementation, tools are manually defined in `task_manager_server.py`. The `@server.list_tools()` decorator registers a function that returns a list of `Tool` objects, where each Tool includes a manually-written name, description, and JSON schema for inputs.

The `@server.call_tool()` decorator handles incoming tool calls and routes them to the appropriate functions in `task_manager.py`.

---

## Phase 3: Live Agent Interaction (15 minutes)

### 3.1 Discover Available Tools

**Say to Students:**  
*"Before we build an agent, let's verify our MCP server actually exposes the tools we expect."*

#### Demo Step 9: Test Tool Discovery

Create a Jupyter cell or Python script:

```python
from agents.mcp import MCPServerStdio
import asyncio

# Define how to start the server
params = {"command": "uv", "args": ["run", "task_manager_server.py"]}

async def discover_tools():
    async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as server:
        print("🔍 Discovering MCP tools...")
        tools = await server.list_tools()
        
        print(f"\n✓ Found {len(tools)} tools:\n")
        for tool in tools:
            print(f"  • {tool.name}")
            print(f"    Description: {tool.description}")
            print()

# Run it
await discover_tools()  # If in Jupyter
# asyncio.run(discover_tools())  # If in regular Python
```

**OBSERVE (Expected Output):**
```
🔍 Discovering MCP tools...

✓ Found 4 tools:

  • create_task_list
    Description: Initializes a new empty task list.

  • add_task
    Description: Adds a new task to the specified list.

  • complete_task
    Description: Marks a task as completed.

  • list_tasks
    Description: Returns all tasks in a list.
```

**DISCUSS:**  
*"Notice how the docstrings became the tool descriptions? This is why good documentation isn't optional—it directly informs the AI what each tool does."*

---

### 3.2 Build and Run the Agent

#### Demo Step 10: Create the Agent

```python
from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
import asyncio

load_dotenv(override=True)

# Server params
params = {"command": "uv", "args": ["run", "task_manager_server.py"]}

# Agent instructions
instructions = """
You are a helpful task management assistant. You can:
1. Create task lists
2. Add tasks to lists
3. Mark tasks as complete
4. Show all tasks

Always confirm actions with the user and provide clear feedback.
"""

# The actual user request
request = """
Please create a task list called 'demo' and add these three tasks:
1. Review MCP documentation
2. Complete the lab assignment
3. Submit project deliverables
"""

async def run_agent_demo():
    # Start MCP server and create agent
    async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as mcp_server:
        agent = Agent(
            name="task_manager_agent",
            instructions=instructions,
            model="gpt-4o-mini",  # or your preferred model
            mcp_servers=[mcp_server]
        )
        
        print("🤖 Running agent...\n")
        with trace("demo_task_manager"):
            result = await Runner.run(agent, request)
        
        print("\n📊 Agent Response:")
        print(result.final_output)

# Execute
if __name__ == "__main__":
    asyncio.run(run_agent_demo())
```

**PREDICT (Before Running):**  
*"What sequence of tool calls do you expect the agent to make? In what order?"*

(Expected: create_task_list → add_task → add_task → add_task)

**OBSERVE:**  
Watch the agent execute. You should see tool calls happening in real-time.

**EXPLAIN:**  
*"The agent is reasoning about which tools to call and in what order. It's not following a hardcoded script—it's using the tool descriptions we provided to decide the right sequence."*

---

### 3.3 Verify Persistence

#### Demo Step 11: Check the Files

```bash
# Run in terminal
ls data/
cat data/tasklist_demo.json
cat data/log_demo.json
```

**OBSERVE:**  
Show students the JSON structure:
```json
{
    "name": "demo",
    "tasks": {
        "1": {
            "id": 1,
            "description": "Review MCP documentation",
            "is_completed": false,
            "created_at": "2025-01-15 14:30:22"
        },
        // ... more tasks
    },
    "next_task_id": 4
}
```

**DISCUSS:**  
*"This is real data persistence. If we restart the agent, the tasks are still there. This is why we separated the database layer—easy to verify and debug."*

---

## Phase 4: Live Debugging Session (5-10 minutes)

### 4.1 Introduce an Error (Intentional)

**Say to Students:**  
*"Let's break something on purpose and practice debugging."*

#### Demo Step 12: Cause a Type Error

Modify `task_manager.py` temporarily:

```python
def add_task(list_name: str, task_description: str) -> str:
    # Intentional bug: pass int instead of str for task_id
    new_task = Task(
        id="not_an_integer",  # ❌ This will fail
        description=task_description,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    # ... rest of code
```

**Run the agent again with:**
```python
request = "Add a task to 'demo': Test debugging"
```

**OBSERVE:**  
You'll get a Pydantic validation error:
```
ValidationError: 1 validation error for Task
id
  Input should be a valid integer [type=int_type, input_value='not_an_integer']
```

**EXPLAIN:**  
*"This is Pydantic protecting us. The error message is clear: 'id' must be an integer. This is why we use type hints—errors happen at the right level with clear messages."*

**Fix it together** (change back to `id=new_task_id`) and rerun successfully.

---

### 4.2 Debugging Strategy Discussion

**Ask Students:**  
*"If the agent calls a tool and gets an error, what's your debugging process?"*

**Suggested Debugging Order:**
1. **Check agent logs:** What did the agent try to call?
2. **Check MCP server terminal:** Did the server receive the request?
3. **Check application logs:** (`data/log_*.json`) What happened in business logic?
4. **Check data files:** Is the stored data corrupted?
5. **Reproduce manually:** Can you call the function directly in Python?

---

## Phase 5: Analysis & Key Insights (5 minutes)

### 5.1 Critical Questions for Discussion

**Ask Students:**

1. **Architecture Question:**  
   *"We have three files: `database.py`, `task_manager.py`, and `task_manager_server.py`. If I wanted to change from JSON files to a PostgreSQL database, which files would I modify?"*
   
   **Answer:** Only `database.py`. This demonstrates proper separation of concerns.

2. **Security Question:**  
   *"Our agent can create, add, complete, and list tasks. What if we wanted to add a 'delete all tasks' function? Should we? What precautions would you take?"*
   
   **Discussion Points:** Guardrails, confirmation prompts, audit logging, role-based access control.

3. **Performance Question:**  
   *"Every tool call reads from and writes to disk. If we had 10,000 tool calls, what would be slow? How could we optimize?"*
   
   **Answer:** Add caching, use in-memory state, batch operations, or switch to a proper database.

---

### 5.2 The "Aha!" Moments

**Recap with Students:**

1. **MCP is Just a Doorway:**  
   The actual business logic (`task_manager.py`) knows nothing about MCP. We could use these same functions in a web API, CLI tool, or any other context.

2. **Type Hints Are Non-Negotiable:**  
   The MCP framework needs type hints to generate tool schemas. Without them, tools aren't discoverable.

3. **Separation of Concerns Works:**  
   We debugged errors quickly because each layer had a single responsibility. When the error was in data validation, we knew it was in `task_manager.py`, not the server code.

4. **Agents Are Reasoning Systems:**  
   The agent didn't follow a hardcoded script. It read tool descriptions and decided the sequence of calls. This is the power of agentic systems—they adapt to novel requests.

---

## Conclusion & Bridge to Lab

**Say to Students:**  
*"You've now seen a complete MCP server built from scratch. In your lab, you'll build something similar but with a twist—instead of task management, you'll implement a different domain. This ensures you understand the underlying patterns, not just how to copy code."*

**Preview the Lab:**
- **Same Structure:** Three files (data layer, business logic, server entry point)
- **Different Domain:** [Instructor: reveal the lab twist—e.g., contact management, inventory tracking, note-taking]
- **Additional Challenges:** You'll need to decide which tools to expose and handle edge cases we didn't cover here

**Final Reminders:**
1. Start with the data layer (`database.py` equivalent)
2. Build your business logic with Pydantic models
3. Create the minimal server entry point
4. Test tool discovery before building the agent
5. Use type hints and docstrings for everything

**Questions?**

---

## Instructor Notes & Timing Guide

### Actual Time Allocation:
- **Phase 1 (Environment & Safety):** 12-15 minutes
  - Wrong way demo: 3 minutes
  - Right way setup: 9-12 minutes
  
- **Phase 2 (Core Task):** 20-25 minutes
  - Database layer: 5 minutes
  - Business logic Part 1 (models): 7 minutes
  - Business logic Part 2 (functions): 8 minutes
  - Server entry point: 3-5 minutes
  
- **Phase 3 (Agent Interaction):** 12-15 minutes
  - Tool discovery: 3 minutes
  - Agent execution: 6 minutes
  - Persistence verification: 3-6 minutes
  
- **Phase 4 (Debugging):** 5-8 minutes
  - Intentional error: 2 minutes
  - Discussion: 3-6 minutes
  
- **Phase 5 (Analysis):** 5 minutes

**Total:** 54-68 minutes (target: 60 minutes)

### Common Student Questions & Answers:

**Q:** "Why use `async/await` everywhere?"  
**A:** "MCP servers handle I/O (file reading, network calls). Async prevents blocking while waiting for responses."

**Q:** "Can I use this with LangChain instead of the `agents` library?"  
**A:** "Yes! MCP is framework-agnostic. LangChain has `MCPTool` integration."

**Q:** "How do I deploy this to production?"  
**A:** "Replace stdio with SSE servers, add authentication, use a real database, implement rate limiting. We'll cover deployment strategies in Module 12."

**Q:** "What if my agent calls the wrong tool?"  
**A:** "Improve tool docstrings, add examples in descriptions, or implement guardrails that check tool call validity before execution."

---

**End of Instructor Demo Script**  
**Next:** Students proceed to independent lab assignment.
