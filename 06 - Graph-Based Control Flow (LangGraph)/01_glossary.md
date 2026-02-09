# Module 06: Graph-Based Control Flow (LangGraph)
## Phase 1: Theoretical Scaffolding - Glossary

**Module Duration:** 60 minutes (Lecture)  
**Pedagogical Strategy:** Vocabulary-first scaffolding to establish mental models before implementation  
**Learning Objective:** Understand the architectural principles of stateful, cyclic agent workflows

---

## 1. Core Concept Definitions

### **State Machine**
**Definition:** A computational model that exists in exactly one of a finite number of states at any given time, with defined rules for transitioning between states based on inputs or conditions.

**Real-World Analogy:** Think of a traffic light system. It can only be in one state at a time (Red, Yellow, or Green), and it transitions between states based on timer conditions or sensor inputs. Unlike a simple linear script that runs once and exits, a state machine continuously operates, maintaining awareness of where it is in the process.

**Why This Matters for Agents:** Traditional LLM applications are stateless—each call is independent. An agentic system needs to remember what step it's on (e.g., "I'm currently evaluating the user's request" vs. "I've finished evaluating and am now planning my response"). State machines provide this persistent context.

---

### **Cyclic Graph (vs. Directed Acyclic Graph - DAG)**
**Definition:** A graph structure where nodes (states) are connected by edges (transitions), and paths may loop back to previously visited nodes, forming cycles.

**Comparison:**
- **DAG (Directed Acyclic Graph):** Workflows that move strictly forward without loops. Example: ETL pipeline (Extract → Transform → Load → End).
- **Cyclic Graph:** Workflows that can return to previous states. Example: Customer support bot (Evaluate → Plan → Act → Evaluate again if the response wasn't sufficient).

**Visual Metaphor:**
```
DAG (Linear):  Start → Step A → Step B → End
Cyclic:        Start → Evaluate ⇄ Plan ⇄ Act → End
                        ↑__________________|
```

**Critical Distinction:** In a DAG, once you leave a node, you never return to it. In a cyclic graph, you can loop back—this is essential for agents that need to refine their approach based on evaluation.

---

### **Conditional Branching**
**Definition:** The ability to dynamically choose the next state/node in the graph based on the output or evaluation of the current state, rather than following a predetermined path.

**Concrete Example:**  
After an agent generates a response, it might:
- **Branch A:** If the response is complete → Route to "End"
- **Branch B:** If additional tools are needed → Route to "Tool Execution Node"
- **Branch C:** If the response failed validation → Route back to "Regenerate Response"

**Technical Implementation in LangGraph:** Uses a `tools_condition` function that examines the agent's output and returns the name of the next node to execute.

**Key Benefit:** Agents can make runtime decisions about their workflow rather than following a rigid script.

---

### **StateGraph (LangGraph's Core Abstraction)**
**Definition:** A Python object that defines the structure of your agent's workflow by declaring:
1. **Nodes:** Individual functions or agents that perform work
2. **Edges:** Connections between nodes that define possible transitions
3. **State:** A shared data structure (typically a Python dict or TypedDict) that is passed between nodes

**Formal Structure:**
```python
from langgraph.graph import StateGraph

# Define what data the graph maintains
class State(TypedDict):
    messages: list
    current_step: str
    tool_results: dict

# Create the graph
graph_builder = StateGraph(State)
```

**Mental Model:** Think of StateGraph as the "blueprint" or "city map" of your agent. It defines:
- What locations (nodes) exist
- What roads (edges) connect them
- What information (state) travelers carry as they move between locations

---

### **Nodes (State Functions)**
**Definition:** Individual units of work in your graph. Each node is a Python function that:
1. Receives the current state as input
2. Performs some operation (calls an LLM, executes a tool, makes a decision)
3. Returns updates to the state

**Example Node Types:**
- **LLM Node:** Calls an LLM with the current conversation history
- **Tool Node:** Executes functions/tools requested by the LLM
- **Evaluation Node:** Checks if the agent's response meets quality criteria
- **Human-in-the-Loop Node:** Pauses execution and waits for human approval

**Code Pattern:**
```python
def my_agent_node(state: State):
    # Access current state
    messages = state["messages"]
    
    # Perform work
    response = llm.invoke(messages)
    
    # Return state updates (these get merged with existing state)
    return {"messages": messages + [response]}
```

**Important:** Nodes don't replace the state—they return updates that get merged into it. This is like editing a shared document rather than rewriting it from scratch.

---

### **Edges (Transitions)**
**Definition:** The connections between nodes that define how the graph flows. LangGraph supports three types:

1. **Regular Edges:** Unconditional transitions. "After Node A, always go to Node B."
   ```python
   graph_builder.add_edge("node_a", "node_b")
   ```

2. **Conditional Edges:** Runtime decisions. "After Node A, examine the state and decide which node to go to next."
   ```python
   graph_builder.add_conditional_edges(
       "node_a",           # Source node
       routing_function,   # Function that decides next node
       {"option1": "node_b", "option2": "node_c"}
   )
   ```

3. **Entry Points:** Where the graph starts.
   ```python
   from langgraph.graph import START
   graph_builder.add_edge(START, "first_node")
   ```

**Decision Framework for Edge Types:**
- Use **regular edges** when the flow is deterministic (always do X after Y)
- Use **conditional edges** when the agent needs to make decisions (if the response contains tool calls, go to the tool node; otherwise, end)

---

### **Checkpointer (Persistence & Memory)**
**Definition:** A mechanism that saves the state of the graph at each step, enabling:
1. **Memory across conversations** (resume previous sessions)
2. **Fault tolerance** (restart from last successful state if something crashes)
3. **Time travel** (inspect or revert to previous states for debugging)

**Two Main Types:**
- **MemorySaver:** Stores state in RAM (lost when program ends, good for testing)
- **SqliteSaver:** Stores state in a SQLite database (persistent, production-ready)

**Configuration Pattern:**
```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# Each conversation gets a unique thread_id
config = {"configurable": {"thread_id": "user_123_session_5"}}
result = graph.invoke({"messages": [user_message]}, config=config)
```

**Critical Use Case:** Without a checkpointer, your agent forgets everything between calls. With a checkpointer, it can maintain context across multiple turns of conversation.

---

### **Compilation (Graph → Executable Workflow)**
**Definition:** The process of converting your StateGraph definition (nodes + edges) into a runnable application.

**What Happens During Compilation:**
1. Validates that all edges point to existing nodes
2. Checks that the graph structure is valid (has an entry point, no orphaned nodes)
3. Creates an execution engine that manages state updates and node transitions
4. Integrates the checkpointer (if provided) for state persistence

**Code:**
```python
graph = graph_builder.compile(checkpointer=memory)  # Now ready to run
```

**Analogy:** Compilation is like taking your architectural blueprint and constructing the actual building. The blueprint (StateGraph) defines the design, but the compiled graph is what you actually interact with.

---

## 2. Architectural Visualization

### The Evaluation → Plan → Act Cycle (Customer Support Bot Pattern)

```
                    ┌─────────────────┐
                    │   START         │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   EVALUATE      │◄────┐
                    │ (Understand the │     │
                    │  customer need) │     │
                    └────────┬────────┘     │
                             │              │
                    Is the request clear?   │
                             │              │
                    ┌────────┴────────┐     │
                    │                 │     │
                 YES│              NO│      │
                    │                 │     │
                    ▼                 ▼     │
           ┌─────────────┐   ┌─────────────┤
           │    PLAN     │   │ Request     │
           │ (Determine  │   │ Clarification│
           │  solution)  │   └─────────────┘
           └──────┬──────┘           │
                  │                  │
                  │                  │
                  ▼                  │
           ┌─────────────┐           │
           │     ACT     │           │
           │ (Execute    │           │
           │  tools)     │           │
           └──────┬──────┘           │
                  │                  │
                  │                  │
     Is solution satisfactory?      │
                  │                  │
         ┌────────┴────────┐         │
         │                 │         │
      YES│              NO│          │
         │                 │         │
         ▼                 └─────────┘
    ┌─────────┐
    │   END   │
    └─────────┘
```

**Key Takeaway:** The cyclic nature allows the bot to loop back to evaluation if its first attempt wasn't sufficient. This is impossible in a linear DAG.

---

### LangGraph Node-Edge Diagram

```
StateGraph Structure:

    Nodes = Functions that do work
    Edges = Rules for transitioning between nodes
    State = Shared data passed between nodes

           ┌──────────────────────────────────────┐
           │         State (shared memory)        │
           │  {                                   │
           │    messages: [...],                  │
           │    step_count: 0,                    │
           │    user_satisfied: False             │
           │  }                                   │
           └──────────────────────────────────────┘
                          ▲
                          │ Each node reads
                          │ and updates state
                          │
    ┌─────────────┬───────┴────────┬─────────────┐
    │             │                │             │
    ▼             ▼                ▼             ▼
┌────────┐   ┌────────┐       ┌────────┐   ┌────────┐
│ Node A │───│ Node B │──────▶│ Node C │───│ Node D │
│(Chatbot│   │(Tools) │       │(Eval)  │   │(End)   │
└────────┘   └────────┘       └────────┘   └────────┘
     │            │                │
     │            │                │
     │            └────────────────┘
     │               Conditional
     └─────────────▶ Routing
           If tools_needed → Node B
           Else → Node C
```

---

## 3. Decision Matrix (Theory)

### When to Use LangGraph vs. Other Frameworks

| Use Case | LangGraph | LangChain | CrewAI |
|----------|-----------|-----------|--------|
| **Simple Q&A Bot** | ❌ Overkill | ✅ Perfect fit | ❌ Overkill |
| **Agent with Conditional Logic** | ✅ Ideal | ⚠️ Possible but awkward | ⚠️ Not designed for this |
| **Multi-turn Debugging Loop** | ✅ Ideal (cycles!) | ❌ No cycle support | ❌ No cycle support |
| **Multi-agent Collaboration** | ⚠️ Possible but verbose | ❌ Not supported | ✅ Designed for this |
| **Need State Persistence** | ✅ Built-in (checkpointer) | ⚠️ Manual implementation | ⚠️ Manual implementation |

---

### Trade-offs in Graph-Based Architectures

#### **Trade-off 1: Flexibility vs. Complexity**
- **Pro:** Cyclic graphs can model arbitrarily complex workflows (loops, branches, error recovery)
- **Con:** Requires more upfront design. You must think through all possible states and transitions.
- **Recommendation:** Start with a simple DAG. Add cycles only when you have a clear use case (e.g., "retry on failure," "iterative refinement").

#### **Trade-off 2: Observability vs. Debuggability**
- **Pro:** Because each state transition is explicit, you can visualize and debug the exact path your agent took.
- **Con:** More nodes and edges mean more code to maintain and more potential points of failure.
- **Mitigation:** Use LangGraph's built-in visualization (`graph.get_graph().draw_mermaid_png()`) and logging at each node.

#### **Trade-off 3: Memory Overhead vs. Fault Tolerance**
- **Pro:** Checkpointers enable powerful features (pause/resume, time travel debugging, conversation memory)
- **Con:** Every state update is serialized and saved, which adds latency and storage costs.
- **Recommendation:** 
  - Use `MemorySaver` (RAM-only) during development for speed
  - Use `SqliteSaver` in production only when you need persistent memory

#### **Trade-off 4: Synchronous vs. Asynchronous Execution**
- **Pro:** LangGraph supports async execution, enabling parallel tool calls and non-blocking operations
- **Con:** Async code is harder to debug and reason about
- **Recommendation:** Start synchronous (`graph.invoke()`), optimize to async (`graph.ainvoke()`) only when performance metrics show it's necessary

---

## 4. Mental Model Checkpoint

Before moving to code, ask yourself:

1. **Can I draw the state diagram of my agent on paper?**  
   (If not, the graph structure isn't clear enough yet)

2. **What data needs to persist across nodes?**  
   (This defines your State schema)

3. **Which transitions are conditional vs. unconditional?**  
   (This determines regular edges vs. conditional edges)

4. **Does my agent need memory across sessions?**  
   (This determines whether you need a checkpointer)

5. **What happens if a node fails?**  
   (This determines whether you need error-handling nodes)

---

## 5. Vocabulary Summary

| Term | One-Sentence Definition |
|------|------------------------|
| **State Machine** | A system that exists in one state at a time and transitions between states based on rules |
| **Cyclic Graph** | A graph where execution paths can loop back to previous nodes |
| **Conditional Branching** | Choosing the next node dynamically based on the current state |
| **StateGraph** | LangGraph's class for defining nodes, edges, and shared state |
| **Node** | A function that performs work and updates the state |
| **Edge** | A connection between nodes defining workflow transitions |
| **Checkpointer** | A system for saving and restoring state at each step |
| **Compilation** | Converting a StateGraph definition into an executable workflow |

---

## 6. Key Design Principle

**The Agent Loop Pattern (Perception → Brain → Action) in LangGraph:**

```
Perception = EVALUATE node (understands input)
Brain      = PLAN node (decides strategy)
Action     = ACT node (executes tools)
```

**Unlike a simple chatbot that does this once:**
```
Input → LLM → Output
```

**An agentic system powered by LangGraph does this cyclically:**
```
Input → EVALUATE → PLAN → ACT → (Did it work?) → EVALUATE → ...
```

This is the fundamental architectural shift from **reactive** to **agentic** AI systems.

---

## Pre-Lab Preparation Questions

Before the live demo, reflect on:

1. **Scenario Design:** Think of a task that cannot be solved in a single LLM call but requires iteration (e.g., researching a topic, debugging code, booking a complex trip).

2. **State Definition:** What information must persist between steps? (e.g., conversation history, tool results, error counts)

3. **Exit Conditions:** How does your agent know when to stop looping and provide a final answer?

---

**Next Phase:** You will observe a live implementation where we build this architecture step-by-step, predict outcomes before execution, and debug errors in real-time.
