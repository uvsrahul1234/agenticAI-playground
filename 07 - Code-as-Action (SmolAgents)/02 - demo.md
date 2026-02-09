# Module 07: Code-as-Action (SmolAgents)
## Demo - Guided Analysis (Instructor-Led)

**Duration:** 60 minutes  
**Format:** Live coding with Predict-Observe-Explain methodology  
**Environment:** Google Colab or local Jupyter notebook  
**Pedagogical Approach:** Students observe, predict outcomes, and discuss results in real-time

---

## Demo Learning Objectives

By the end of this demo, students will be able to:
1. Initialize and configure a CodeAgent with different models
2. Observe how agents reason about problems before writing code
3. Understand the agent's thought process through log inspection
4. Compare local vs. sandbox execution
5. Debug agent-generated code in real-time

---

## Pre-Demo Setup (Instructor Preparation)

### Required Installations

```bash
# Core SmolAgents installation
pip install smolagents

# Optional: Install with toolkit for default tools
pip install 'smolagents[toolkit]'

# For sandbox execution (choose one):
pip install 'smolagents[modal]'    # Modal sandbox
pip install 'smolagents[docker]'   # Docker sandbox
```

### Environment Variables

Create a `.env` file or use Colab Secrets:

```python
# For HuggingFace models (optional, for higher rate limits)
HF_TOKEN = "your_huggingface_token_here"

# For LiteLLM models
ANTHROPIC_API_KEY = "your_anthropic_key_here"
# OR
OPENAI_API_KEY = "your_openai_key_here"
```

**Security Note:** Demonstrate BOTH the wrong way (hardcoded keys) and the right way (environment variables) to reinforce security practices.

---

## Demo Part 1: Basic CodeAgent with Fibonacci Problem

### Step 1.1: Environment Check (5 minutes)

**Instructor Action:** Show the "wrong way" first to demonstrate security vulnerability.

```python
# ❌ WRONG - Security Violation!
from smolagents import CodeAgent, InferenceClientModel

# Never do this in production!
model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-72B-Instruct",
    token="hf_ThisIsABadIdeaNeverHardcodeKeys"  # BAD!
)
```

**Instructor Says:** "Why is this bad? Anyone can see this token in your code, GitHub repo, or shared notebook. It's like leaving your house key under the doormat with a sign saying 'Key Here.'"

**Now show the RIGHT way:**

```python
# ✅ CORRECT - Using environment variables
import os
from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel

# Load environment variables
load_dotenv()

# Secure token handling
model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-72B-Instruct",
    token=os.getenv("HF_TOKEN")
)

print("✓ Model initialized securely")
```

**Predict-Observe-Explain Moment:**
- **Predict:** "What will happen if the HF_TOKEN environment variable is not set?"
- **Observe:** Run the code without setting the token (show the error)
- **Explain:** Discuss error handling and why clear error messages matter

---

### Step 1.2: Creating Your First CodeAgent (10 minutes)

```python
from smolagents import CodeAgent, InferenceClientModel

# Initialize the model
model = InferenceClientModel(model_id="Qwen/Qwen2.5-72B-Instruct")

# Create a CodeAgent with no tools (we'll use pure Python)
agent = CodeAgent(
    tools=[],  # Empty tool list - agent will use pure Python
    model=model,
    add_base_tools=False,  # We don't need web search for math
    verbosity_level=2  # High verbosity to see what's happening
)

print("✓ Agent created successfully")
print(f"Agent type: {type(agent)}")
print(f"Number of tools: {len(agent.tools)}")
```

**Instructor Narration:** "Notice we're creating a CodeAgent with NO tools. This means the agent can only use pure Python—no web searches, no external APIs. We're testing its ability to write algorithms from scratch."

**Discussion Question:** "Why might we want to start with zero tools instead of loading everything available?"

**Expected Student Responses:**
- Simpler debugging
- Forces the agent to solve problems algorithmically
- Reduces potential for errors
- Clearer understanding of what the agent can do

---

### Step 1.3: The Core Task - Fibonacci Sequence (15 minutes)

**Instructor Action:** Before running the code, engage students with prediction.

```python
# The task we'll give to the agent
task = "Could you give me the 100th number in the Fibonacci sequence?"

print("Task:", task)
```

**Predict-Observe-Explain: Round 1**

**PAUSE HERE** ⏸️

**Instructor Says:** "Before we run this, let's think like the agent. If YOU were the LLM and had to solve this problem by writing Python code, what would you do? Turn to your neighbor and discuss for 30 seconds."

**Expected Discussion Points:**
- Need to write a function to calculate Fibonacci
- Could use recursion or iteration
- 100th number will be large—need to handle big integers
- Should return the result using `final_answer()`

**Now run the agent:**

```python
# Execute the task
result = agent.run(task)

print("\n" + "="*50)
print("FINAL RESULT:")
print("="*50)
print(result)
```

**Sample Expected Output:**
```
=== Agent thoughts:
I need to calculate the 100th Fibonacci number. I'll write a Python function
to compute this iteratively to avoid recursion depth issues.

>>> Agent is executing the code below:
def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

result = fibonacci(100)
final_answer(result)

==================================================
FINAL RESULT:
==================================================
354224848179261915075
```

**Instructor Highlights:**
1. **The agent reasoned first:** Notice the "thoughts" section before code generation
2. **Choice of algorithm:** The agent chose iteration over recursion (why?)
3. **Code quality:** The code is clean, readable, and correct
4. **final_answer() call:** This is how the agent signals completion

---

### Step 1.4: Inspecting Agent Logs (10 minutes)

**Instructor Action:** Now let's look "under the hood" at what happened.

```python
# Inspect the detailed logs
print("Number of steps taken:", len(agent.logs))
print("\n" + "="*50)
print("DETAILED LOG INSPECTION:")
print("="*50)

for i, log_entry in enumerate(agent.logs):
    print(f"\nStep {i + 1}:")
    print(f"Type: {log_entry.get('type', 'unknown')}")
    if 'llm_output' in log_entry:
        print(f"LLM Output: {log_entry['llm_output'][:200]}...")  # First 200 chars
    if 'tool_calls' in log_entry:
        print(f"Tool Calls: {log_entry['tool_calls']}")
```

**Discuss with Students:**
- How many steps did the agent take?
- What information is captured at each step?
- How could we use these logs for debugging?

**Memory vs. Logs:**

```python
# Compare logs to memory messages
memory_messages = agent.write_memory_to_messages()

print("\n" + "="*50)
print("MEMORY MESSAGES (Higher-level view):")
print("="*50)

for i, message in enumerate(memory_messages):
    print(f"\nMessage {i + 1}:")
    print(f"Role: {message.get('role', 'unknown')}")
    print(f"Content preview: {str(message.get('content', ''))[:150]}...")
```

**Key Teaching Point:** "Logs give you EVERYTHING. Memory gives you a conversation-like summary. Which one you use depends on whether you're debugging (logs) or building a conversational interface (memory)."

---

## Demo Part 2: Comparing Local vs. Sandbox Execution

### Step 2.1: Understanding the Security Risk (5 minutes)

**Instructor Action:** Demonstrate why sandboxing matters.

```python
# WARNING: This demonstrates a security vulnerability
# DO NOT run untrusted code like this in production!

malicious_task = """
Write Python code that prints 'Hello World' but also tries to read
a file called '/etc/passwd' (simulating malicious behavior).
"""

print("⚠️  SECURITY DEMONSTRATION ⚠️")
print("Task:", malicious_task)
print("\nWe will NOT actually run this with a real agent,")
print("but let's discuss: What could go wrong if we did?")
```

**Class Discussion Points:**
- Agent could try to read sensitive files
- Could attempt network connections
- Could try to delete or modify files
- Could consume excessive resources

**Instructor Says:** "This is why we need sandboxing. Let's see how to do it safely."

---

### Step 2.2: Local Execution (Default Behavior)

```python
# Local execution (what we've been doing)
from smolagents import CodeAgent, InferenceClientModel

model = InferenceClientModel(model_id="Qwen/Qwen2.5-72B-Instruct")
local_agent = CodeAgent(tools=[], model=model)

print("Execution mode: Local (in your Python environment)")
print("Security: Limited (safe functions only)")

result = local_agent.run("What is the 42nd Fibonacci number?")
print(f"Result: {result}")
```

---

### Step 2.3: Sandbox Execution with Modal (10 minutes)

**Prerequisites Check:**
```python
# Check if Modal is installed
try:
    import modal
    print("✓ Modal is installed")
except ImportError:
    print("❌ Modal not found. Install with: pip install 'smolagents[modal]'")
```

**Running in Modal Sandbox:**

```python
from smolagents import CodeAgent, InferenceClientModel

model = InferenceClientModel(model_id="Qwen/Qwen2.5-72B-Instruct")

# Using context manager for automatic cleanup
with CodeAgent(
    tools=[],
    model=model,
    executor_type="modal"  # This is the key change!
) as sandbox_agent:
    print("Execution mode: Modal Sandbox (isolated environment)")
    print("Security: High (complete isolation)")
    
    result = sandbox_agent.run("What is the 42nd Fibonacci number?")
    print(f"Result: {result}")

print("✓ Sandbox automatically cleaned up")
```

**Predict-Observe-Explain: Round 2**

**PAUSE HERE** ⏸️

**Instructor Says:** "Notice anything different about the execution time? Why might sandboxed execution be slower?"

**Expected Observations:**
- Slight delay for container initialization
- Network overhead for sending code to sandbox
- Cleanup time after execution

**Critical Question to Class:** "Given this performance trade-off, when would you DEFINITELY use a sandbox despite the slowdown?"

**Answer:** Production systems, untrusted inputs, internet-facing applications, multi-tenant systems

---

## Demo Part 3: Adding Tools to the Agent

### Step 3.1: Agent with Default Toolbox (10 minutes)

```python
from smolagents import CodeAgent, InferenceClientModel

model = InferenceClientModel(model_id="Qwen/Qwen2.5-72B-Instruct")

# Create agent with default tools
agent_with_tools = CodeAgent(
    tools=[],
    model=model,
    add_base_tools=True  # This adds web search, python interpreter, etc.
)

print(f"Number of tools available: {len(agent_with_tools.tools)}")
print("\nAvailable tools:")
for tool_name in agent_with_tools.tools.keys():
    print(f"  - {tool_name}")
```

**Task that requires web search:**

```python
task_with_search = """
What is the current price of Bitcoin in USD? 
Use web search to find the latest information.
"""

result = agent_with_tools.run(task_with_search)
print("\nResult:", result)
```

**Observe with Students:**
- How does the agent decide to use web search?
- What code does it generate to parse the search results?
- How does it handle uncertainty or conflicting information?

---

### Step 3.2: Creating a Custom Tool (5 minutes)

**Instructor Action:** Show how to extend agent capabilities.

```python
from smolagents import Tool

class TemperatureConverter(Tool):
    name = "temperature_converter"
    description = "Converts temperature between Celsius and Fahrenheit"
    
    inputs = {
        "temperature": {"type": "number", "description": "The temperature value"},
        "from_unit": {"type": "string", "description": "Either 'C' or 'F'"},
        "to_unit": {"type": "string", "description": "Either 'C' or 'F'"}
    }
    output_type = "number"
    
    def forward(self, temperature: float, from_unit: str, to_unit: str) -> float:
        if from_unit == "C" and to_unit == "F":
            return (temperature * 9/5) + 32
        elif from_unit == "F" and to_unit == "C":
            return (temperature - 32) * 5/9
        else:
            return temperature  # No conversion needed

# Add custom tool to agent
temp_tool = TemperatureConverter()
agent_with_tools.tools[temp_tool.name] = temp_tool

# Test the custom tool
task = "Convert 25 degrees Celsius to Fahrenheit"
result = agent_with_tools.run(task)
print(f"Result: {result}")
```

**Discussion:** "Why did we need to provide such detailed descriptions in the tool definition? How does this help the LLM?"

---

## Demo Part 4: Live Debugging Session

### Step 4.1: Intentional Error Demonstration

**Instructor Action:** Show what happens when things go wrong.

```python
# Task that might cause the agent to struggle
tricky_task = "What is the 1000th Fibonacci number modulo 1000000007?"

# Run with high verbosity to see the reasoning
agent = CodeAgent(tools=[], model=model, verbosity_level=2)
result = agent.run(tricky_task)
```

**Common Issues to Highlight:**
1. **Syntax errors in generated code**
2. **Logic errors** (wrong algorithm)
3. **Resource limits** (computation too slow)
4. **Misunderstood requirements**

**Live Debugging Steps:**

1. **Check the logs:**
```python
# Inspect what went wrong
for log in agent.logs:
    if 'error' in log:
        print("Error found:", log['error'])
```

2. **Examine the generated code:**
```python
# Find the code that was generated
for log in agent.logs:
    if 'code' in log:
        print("Generated code:")
        print(log['code'])
```

3. **Discuss with class:** "If YOU were debugging this, what would you change?"

---

## Demo Wrap-Up: Key Observations

### What We Learned Today:

1. **Security First:** Always use environment variables for API keys, never hardcode them

2. **Agent Reasoning:** CodeAgents think before they act—they reason about the problem in natural language before generating code

3. **Logs vs. Memory:** Logs give detailed step-by-step execution; memory gives conversation-like summaries

4. **Local vs. Sandbox:** Local is fast but risky; sandbox is slower but secure. Always sandbox in production.

5. **Tools Extend Capabilities:** Agents are only as powerful as their tools. Well-described tools enable better LLM decision-making.

6. **Debugging is Iterative:** When agents fail, inspect logs, examine generated code, and understand the reasoning process

---

## Critical Questions for Discussion

**Before you leave today, think about these:**

1. What types of problems are BEST suited for CodeAgent vs. ToolCallingAgent?

2. If you were building a production system, what additional safety measures would you implement beyond sandboxing?

3. How would you test an agent to ensure it's generating correct code consistently?

4. What are the ethical implications of agents that can write and execute arbitrary code?

---

## Preparation for Lab

In the lab, you will:
1. Set up your own CodeAgent environment
2. Solve a different logic puzzle (not Fibonacci!)
3. Implement both local and sandbox execution
4. Create a custom tool
5. Debug intentional errors
6. Analyze and compare agent performance

**The Twist:** Your lab will use a different algorithm problem to ensure you understand the concepts, not just the specific Fibonacci example.

---

*End of Demo - Proceed to Independent Lab*
