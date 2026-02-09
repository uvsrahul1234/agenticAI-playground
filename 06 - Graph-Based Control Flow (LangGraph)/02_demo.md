# Module 06: Graph-Based Control Flow (LangGraph)
## Phase 2: Instructor-Led Demonstration - Live Analysis

**Duration:** 60 minutes  
**Format:** Live coding with Predict-Observe-Explain methodology  
**Environment:** Jupyter Notebook or Google Colab  
**Learning Objective:** Observe the construction of a stateful, cyclic customer support agent in real-time

---

## Pre-Demo Setup

### Instructor Checklist:
- [ ] Jupyter Notebook or Google Colab ready
- [ ] `.env` file with `OPENAI_API_KEY` prepared (show redacted version to students)
- [ ] LangGraph and dependencies installed
- [ ] Sample "broken" code prepared to demonstrate common errors
- [ ] Visualization tools ready (`graphviz` for rendering)

### Required Installations:
```bash
pip install langgraph langchain-openai python-dotenv gradio
```

---

## Demo Structure

This demo follows the "Predict → Observe → Explain" pattern. Before running critical cells, pause and ask students to predict the output.

---

## Part 1: Environment & Safety Check (10 minutes)

### Demonstrate the WRONG Way First

**Instructor Script:**  
"Let's intentionally make a common mistake to see what happens when security best practices aren't followed."

```python
# ❌ BAD PRACTICE - Hardcoded API Key
import openai

openai.api_key = "sk-proj-abc123..."  # Never do this!

# Let's see what goes wrong...
```

**Intentional Error to Trigger:**
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key="sk-fake-key")
llm.invoke("Hello")
```

**Expected Output:**
```
AuthenticationError: Incorrect API key provided...
```

**Teaching Moment:**  
"Notice two problems here:
1. The API key is visible in our code (security risk if this gets committed to Git)
2. The error message is cryptic until you read it carefully—'Incorrect API key' means authentication failed."

---

### Now Demonstrate the RIGHT Way

```python
# ✅ GOOD PRACTICE - Environment Variables
from dotenv import load_dotenv
import os

load_dotenv()

# Verify (without printing the actual key)
if os.getenv("OPENAI_API_KEY"):
    print("✓ API key loaded successfully")
else:
    print("✗ API key not found - check your .env file")
```

**Instructor Note:** Show your `.env` file structure (with redacted key):
```bash
# .env file
OPENAI_API_KEY=sk-proj-••••••••••••••••
```

**Security Focus Question for Class:**  
*"What happens if I accidentally push my .env file to GitHub?"*

**Answer:** "That's why we add `.env` to `.gitignore`. The key would be exposed, and malicious actors could use it to rack up charges on your account. Always treat API keys like passwords."

---

## Part 2: Building the Basic StateGraph (20 minutes)

### Step 2A: Define the State Schema

**Before Running This Cell, Ask:**  
*"What information do you think our customer support bot needs to remember between steps?"*

**Student Predictions (write on board):**
- Conversation history
- Current step in the process
- Whether tools were called
- Whether the user's issue is resolved

```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    State schema for our customer support agent.
    
    'messages' is the conversation history.
    The add_messages annotation tells LangGraph to append new messages
    rather than overwriting the list.
    """
    messages: Annotated[list, add_messages]
```

**Explanation:**  
"The `add_messages` annotation is crucial. Without it, every node would replace the entire message list. With it, LangGraph intelligently appends new messages while preserving history."

---

### Step 2B: Create Simple Tools

**Instructor Script:**  
"In a real customer support bot, these tools would query databases or APIs. For our demo, they're simplified mock functions."

```python
from langchain_core.tools import tool

@tool
def check_order_status(order_id: str) -> str:
    """Check the status of an order by order ID."""
    # Mock implementation
    mock_statuses = {
        "12345": "Shipped - Arriving tomorrow",
        "67890": "Processing - Expected ship date: 2 days",
        "11111": "Delivered on Nov 20, 2024"
    }
    return mock_statuses.get(order_id, f"Order {order_id} not found in system")

@tool
def process_refund(order_id: str, reason: str) -> str:
    """Process a refund for an order."""
    return f"Refund initiated for order {order_id}. Reason: {reason}. Funds will return in 5-7 business days."

@tool
def escalate_to_human(issue_description: str) -> str:
    """Escalate complex issues to a human agent."""
    return f"Issue escalated: '{issue_description}'. A human agent will contact you within 24 hours."

tools = [check_order_status, process_refund, escalate_to_human]
```

**Critical Question for Class:**  
*"Why do we define tools as Python functions with docstrings?"*

**Answer:** "The LLM reads the docstring to understand what the tool does. The function signature tells it what parameters are required. This is how the LLM 'learns' what tools are available."

---

### Step 2C: Create the StateGraph Structure

```python
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition

# Initialize the LLM with tools
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# Create the graph
graph_builder = StateGraph(State)
```

**Pause for Prediction:**  
*"We've created an empty graph. What do you think we need to add next before it can run?"*

**Expected Answers:**
- Nodes (the actual functions that do work)
- Edges (how nodes connect)
- An entry point

---

### Step 2D: Add Nodes

**Before Running, Ask:**  
*"What should the 'chatbot' node do? What should it return?"*

```python
def chatbot(state: State):
    """
    Main agent node - calls the LLM with the current conversation history.
    """
    print(f"[CHATBOT NODE] Processing {len(state['messages'])} messages")
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# Add the chatbot node
graph_builder.add_node("chatbot", chatbot)

# Add the tools node (prebuilt by LangGraph)
graph_builder.add_node("tools", ToolNode(tools=tools))
```

**Teaching Moment:**  
"Notice that `chatbot` returns `{'messages': [response]}`, not `response`. The return value must match the State schema. LangGraph will merge this update into the existing state."

---

### Step 2E: Add Edges

**Instructor Script:**  
"Now we define the workflow. After the chatbot runs, it needs to decide: Did it call a tool, or is it done?"

```python
# Conditional edge: After chatbot, decide whether to use tools or end
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,  # Built-in function that checks if tools were called
)

# Regular edge: After tools run, always return to chatbot
graph_builder.add_edge("tools", "chatbot")

# Entry point: Start with the chatbot
graph_builder.add_edge(START, "chatbot")
```

**Critical Question:**  
*"Why does the tools node go back to the chatbot instead of ending?"*

**Answer:** "Because after a tool runs, the agent needs to interpret the results and incorporate them into its response. The tool output becomes part of the conversation history, and the agent formulates the final answer."

---

### Step 2F: Compile and Visualize

```python
graph = graph_builder.compile()

# Visualize the graph structure
from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))
```

**Expected Visualization:**
```
    ┌─────────┐
    │  START  │
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │ chatbot │──────┐
    └────┬────┘      │
         │           │
     [condition]     │
         │           │
    ┌────┴────┐      │
    │         │      │
    ▼         ▼      │
┌───────┐  ┌───────┐│
│ tools │  │  END  ││
└───┬───┘  └───────┘│
    │               │
    └───────────────┘
```

**Instructor Note:**  
"This diagram shows the actual execution flow LangGraph will follow. Notice the cycle: chatbot → tools → chatbot. This is what makes it 'agentic' rather than a simple one-shot response."

---

## Part 3: Testing the Agent (15 minutes)

### Test Case 1: Simple Query (No Tools Needed)

**Before Running, Predict:**  
*"The user asks, 'What are your business hours?' Will the agent call any tools?"*

```python
def run_agent(user_input: str):
    """Helper function to invoke the agent and display the result."""
    result = graph.invoke({
        "messages": [{"role": "user", "content": user_input}]
    })
    
    print("\n" + "="*60)
    print("AGENT RESPONSE:")
    print("="*60)
    print(result["messages"][-1].content)
    print("="*60 + "\n")
    
    return result

# Test 1
run_agent("What are your business hours?")
```

**Expected Behavior:**  
The agent responds directly without calling tools.

**Live Analysis Discussion:**  
*"Notice that the chatbot node ran, but the tools node did not. The conditional edge correctly determined that no tools were needed."*

---

### Test Case 2: Tool-Required Query

**Before Running, Predict:**  
*"The user asks, 'What's the status of my order 12345?' What will happen?"*

```python
run_agent("What's the status of my order 12345?")
```

**Expected Output:**
```
[CHATBOT NODE] Processing 1 messages
[CHATBOT NODE] Processing 3 messages  # Second call after tool execution

AGENT RESPONSE:
Your order 12345 has been shipped and will arrive tomorrow.
```

**Critical Discussion Point:**  
"Did you notice the chatbot node ran *twice*? First, to decide to call the tool. Second, to interpret the tool results and formulate the final response. This is the cyclic execution in action."

---

### Test Case 3: Multi-Turn Conversation (Introducing Memory)

**Instructor Script:**  
"Right now, each call to `run_agent()` starts fresh. The agent has no memory of previous interactions. Let's add persistence."

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# Create a session configuration
config = {"configurable": {"thread_id": "demo_session_1"}}

# Multi-turn conversation
print("Turn 1:")
graph.invoke(
    {"messages": [{"role": "user", "content": "I want to check my order 67890"}]},
    config=config
)

print("\nTurn 2 (in same session):")
graph.invoke(
    {"messages": [{"role": "user", "content": "Actually, I'd like to get a refund on that order"}]},
    config=config
)
```

**Before Running Turn 2, Ask:**  
*"The user says 'that order' without specifying the ID. How will the agent know which order they mean?"*

**Answer:** "Because we're using the same `thread_id`, the checkpointer has preserved the conversation history. The agent sees the previous message about order 67890 and understands the context."

---

### Inspecting the State History

```python
# View the current state
current_state = graph.get_state(config)
print("Current State:")
print(f"Number of messages: {len(current_state.values['messages'])}")

# View the state history (most recent first)
history = list(graph.get_state_history(config))
print(f"\nTotal state checkpoints saved: {len(history)}")

for i, checkpoint in enumerate(history[:3]):  # Show first 3
    print(f"\nCheckpoint {i+1}:")
    print(f"  - Next node to execute: {checkpoint.next}")
    print(f"  - Number of messages: {len(checkpoint.values['messages'])}")
```

**Teaching Moment:**  
"Each time the graph updates state, a checkpoint is saved. In production, this enables powerful debugging—you can 'time travel' to any previous state and see exactly what the agent was thinking at that moment."

---

## Part 4: Common Errors & Debugging (10 minutes)

### Error Demo 1: Missing Edge

**Instructor Script:**  
"Let's intentionally create a broken graph to see what happens."

```python
# Create a new graph with a mistake
broken_graph = StateGraph(State)
broken_graph.add_node("chatbot", chatbot)
broken_graph.add_node("tools", ToolNode(tools=tools))

# Oops! Forgot to connect the nodes
broken_graph.add_edge(START, "chatbot")

# Try to compile
try:
    broken_graph.compile()
except Exception as e:
    print(f"❌ Compilation Error: {e}")
```

**Expected Error:**
```
Missing outbound edge from node 'chatbot'
```

**Fix Discussion:**  
"The error message is very clear: 'chatbot' is a dead-end node. LangGraph won't compile a graph where a node has no way to exit. We must add either a regular edge or conditional edges."

---

### Error Demo 2: Incorrect State Return

```python
def broken_chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return response  # ❌ Wrong! Should return a dict

broken_graph_2 = StateGraph(State)
broken_graph_2.add_node("chatbot", broken_chatbot)
broken_graph_2.add_edge(START, "chatbot")

try:
    graph2 = broken_graph_2.compile()
    graph2.invoke({"messages": [{"role": "user", "content": "Hi"}]})
except Exception as e:
    print(f"❌ Runtime Error: {e}")
```

**Fix:**  
"Nodes must return a dictionary that matches the State schema. Change `return response` to `return {'messages': [response]}`."

---

## Part 5: Wrap-Up & Reflection (5 minutes)

### Key Observations From the Demo:

1. **State is Shared:** Every node receives the current state and returns updates
2. **Checkpointers Enable Memory:** Without them, the agent is stateless
3. **Conditional Edges Make Decisions:** The `tools_condition` examines the LLM's output to decide the next step
4. **Cycles Allow Iteration:** The tools → chatbot loop enables multi-step reasoning
5. **Visualization is Essential:** The graph diagram makes the workflow explicit and debuggable

---

### Preview of Student Lab

**Instructor Script:**  
"In your lab, you'll build a similar system but with a twist: instead of a customer support bot, you'll create a **research assistant** that loops through:
- **Evaluate:** Assess if the user's question is clear
- **Plan:** Decide which sources to search
- **Act:** Execute web searches
- **Synthesize:** Combine results into a coherent answer

Your agent will loop back to 'Plan' if the first search didn't provide sufficient information. This is a more complex cyclic pattern than what we built here."

---

### Pre-Lab Questions to Ponder:

1. What tools will your research assistant need?
2. How will you determine if the agent should stop researching and provide a final answer?
3. What edge cases might cause infinite loops, and how can you prevent them?

---

## Instructor Self-Checklist

- [ ] Demonstrated insecure vs. secure API key handling
- [ ] Built StateGraph step-by-step with student predictions
- [ ] Showed conditional edges in action (tool calling)
- [ ] Demonstrated memory with checkpointers and `thread_id`
- [ ] Triggered and fixed at least one common error
- [ ] Visualized the graph structure
- [ ] Connected the demo to the upcoming lab assignment

---

**Next Phase:** Students will independently implement a research assistant with a more complex cyclic workflow, encountering and debugging their own edge cases.
