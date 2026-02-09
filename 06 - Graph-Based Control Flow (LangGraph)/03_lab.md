# Module 06: Graph-Based Control Flow (LangGraph)
## Phase 3: Independent Lab - Research Assistant with Cyclic Workflow

**Duration:** 90-120 minutes (Take-home assignment)  
**Submission:** Jupyter Notebook (.ipynb) + Written Reflection (PDF)  
**Pedagogical Goal:** Apply graph-based control flow to a new problem domain, demonstrating transfer of learning from the customer support bot demo

---

## Lab Overview

In the demo, you observed the construction of a **customer support bot** with a simple cyclic pattern:
```
chatbot → tools (if needed) → chatbot → end
```

In this lab, you will build a **Research Assistant Agent** with a more complex multi-stage cycle:
```
EVALUATE → PLAN → SEARCH → SYNTHESIZE → EVALUATE (loop if needed)
```

This agent will:
1. **Evaluate** if the user's research question is clear and answerable
2. **Plan** which information sources to query
3. **Search** using mock research tools
4. **Synthesize** the results into a coherent answer
5. **Evaluate again** to determine if more research is needed or if the answer is sufficient

---

## Learning Objectives

By completing this lab, you will:
- [ ] Design a StateGraph with at least 4 nodes
- [ ] Implement conditional edges based on custom logic (not just tool detection)
- [ ] Use a checkpointer to maintain conversation history across multiple research iterations
- [ ] Handle edge cases that could cause infinite loops
- [ ] Visualize and debug a complex cyclic workflow
- [ ] Reflect on architectural trade-offs

---

## Pre-Lab Setup

### 1. Environment Configuration

If this is a stand alone project, create a new Python environment using `uv` but not needed if a part in this project:

```bash
uv venv research-assistant
source research-assistant/bin/activate  # On Windows: research-assistant\Scripts\activate
```

Install dependencies:
```bash
uv pip install langgraph langchain-openai python-dotenv
```

### 2. API Key Setup

Create a `.env` file in your project directory:
```bash
OPENAI_API_KEY=your-key-here
```

**Security Requirement:** Your submission must NOT contain hardcoded API keys. We will check for this in code review.

---

## Part 1: The "Twist" - Design Your State Schema (15 minutes)

Unlike the demo where we provided the state structure, **you must design your own state schema** for the research assistant.

### Required State Fields:

Your `State` class must include:
- `messages`: Conversation history (same as demo)
- `research_query`: The current question being researched
- `search_iterations`: How many search cycles have been performed (to prevent infinite loops)
- `research_complete`: Boolean flag indicating if enough information has been gathered

### Optional State Fields (Your Design Choice):

Consider adding:
- `sources_checked`: List of sources already consulted (to avoid duplicates)
- `confidence_score`: Numeric assessment of answer quality
- `pending_subtopics`: Queue of related topics to explore

**Deliverable 1:** Define your State schema with docstring explaining your design choices.

```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class ResearchState(TypedDict):
    """
    State schema for the Research Assistant Agent.
    
    TODO: Add docstring explaining:
    - Why you included each field
    - What values they can take
    - How nodes will update them
    """
    messages: Annotated[list, add_messages]
    # Add your fields here
```

---

## Part 2: Define Research Tools (20 minutes)

Create **at least 3 mock tools** that simulate research capabilities:

### Required Tools:

```python
from langchain_core.tools import tool

@tool
def search_academic_papers(topic: str) -> str:
    """Search for academic papers on a given topic."""
    # TODO: Implement mock logic
    # Return 2-3 fake paper titles and abstracts
    pass

@tool
def search_news_articles(topic: str, days_back: int = 7) -> str:
    """Search for recent news articles on a topic."""
    # TODO: Implement mock logic
    pass

@tool
def query_knowledge_base(question: str) -> str:
    """Query an internal knowledge base."""
    # TODO: Implement mock logic
    pass
```

**Requirements:**
- Each tool must have a descriptive docstring (the LLM reads these!)
- Each tool must return a string (even if it's mock data)
- At least one tool should accept multiple parameters

**Critical Thinking Question (include in your reflection):**  
*Why do we mock these tools instead of making real API calls to Google Scholar or NewsAPI?*

---

## Part 3: Build the Graph Nodes (30 minutes)

Implement the following nodes. **Unlike the demo, these are NOT provided—you must write them from scratch.**

### Node 1: `evaluate_query`

**Purpose:** Assess if the research question is clear and actionable.

**Logic:**
- If the query is too vague (e.g., "Tell me about science"), return a clarification request
- If the query is clear, proceed to planning
- Update state field `research_query` with the clarified question

```python
def evaluate_query(state: ResearchState):
    """
    Evaluates whether the user's question is specific enough to research.
    """
    # TODO: Implement logic
    # Hint: You might call the LLM here with a specialized system prompt
    # Return: Updated state dict
    pass
```

---

### Node 2: `plan_research`

**Purpose:** Decide which tools to use and in what order.

**Logic:**
- Analyze the research query
- Decide if you need academic sources, news, or both
- Update state with a plan (could be a new state field `research_plan`)

```python
def plan_research(state: ResearchState):
    """
    Creates a research plan based on the query.
    """
    # TODO: Implement logic
    # Consider: Should you search papers first, or news first?
    pass
```

---

### Node 3: `execute_search`

**Purpose:** Call the appropriate research tools.

**Logic:**
- Based on the plan, invoke 1 or more tools
- Store results in the state (perhaps in a new field `search_results`)
- Increment `search_iterations` counter

```python
def execute_search(state: ResearchState):
    """
    Executes the research tools based on the plan.
    """
    # TODO: Implement logic
    # Hint: This might call multiple tools in sequence
    pass
```

---

### Node 4: `synthesize_answer`

**Purpose:** Combine search results into a coherent response.

**Logic:**
- Call the LLM with a synthesis prompt
- Provide all gathered research results as context
- Generate a final answer
- Update state field `research_complete` based on answer quality

```python
def synthesize_answer(state: ResearchState):
    """
    Synthesizes all gathered information into a final response.
    """
    # TODO: Implement logic
    # Critical: Set research_complete = True if answer is sufficient
    pass
```

---

## Part 4: Define Conditional Routing Logic (20 minutes)

**This is the most critical part of the lab.** You must implement custom routing functions.

### Routing Function 1: After `evaluate_query`

**Decision Point:** Should we proceed to planning, or ask for clarification?

```python
def after_evaluate(state: ResearchState) -> str:
    """
    Determines next step after query evaluation.
    
    Returns:
        "plan_research" if query is clear
        "request_clarification" if query is too vague
    """
    # TODO: Implement decision logic
    # Hint: Check the last LLM message or a state flag
    pass
```

---

### Routing Function 2: After `synthesize_answer`

**Decision Point:** Is the research complete, or do we need another iteration?

```python
def after_synthesis(state: ResearchState) -> str:
    """
    Determines if more research is needed.
    
    Returns:
        END if research is sufficient
        "plan_research" if more iteration needed
    """
    # TODO: Implement decision logic
    # Critical: Must prevent infinite loops!
    
    # Safety Check:
    if state.get("search_iterations", 0) >= 3:
        return END  # Force stop after 3 iterations
    
    if state.get("research_complete"):
        return END
    else:
        return "plan_research"
```

**Deliverable 2:** Explain your stopping criteria in the reflection document.

---

## Part 5: Assemble the Graph (15 minutes)

Now that you have all the pieces, assemble them into a StateGraph:

```python
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create graph
graph_builder = StateGraph(ResearchState)

# TODO: Add nodes
# graph_builder.add_node("evaluate_query", evaluate_query)
# ...

# TODO: Add edges
# graph_builder.add_edge(START, "evaluate_query")
# graph_builder.add_conditional_edges("evaluate_query", after_evaluate, {...})
# ...

# Compile with memory
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

conn = sqlite3.connect("research_memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

graph = graph_builder.compile(checkpointer=checkpointer)
```

**Requirement:** Your graph must have:
- At least 4 nodes
- At least 2 conditional edges
- A cycle (some path must loop back to a previous node)

---

## Part 6: Visualize Your Graph (5 minutes)

Generate and include the graph visualization in your submission:

```python
from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))
```

**Deliverable 3:** Screenshot of your graph visualization showing the cyclic structure.

---

## Part 7: Test Cases (20 minutes)

Run your agent on these test scenarios and document the results:

### Test 1: Simple Query (Should Complete in 1 Iteration)

```python
config = {"configurable": {"thread_id": "test_1"}}

result = graph.invoke({
    "messages": [{"role": "user", "content": "What are the main causes of climate change?"}]
}, config=config)

print("Final Response:", result["messages"][-1].content)
print("Iterations Used:", result.get("search_iterations"))
```

**Expected Behavior:** Agent searches, synthesizes, and stops.

---

### Test 2: Vague Query (Should Request Clarification)

```python
config = {"configurable": {"thread_id": "test_2"}}

result = graph.invoke({
    "messages": [{"role": "user", "content": "Tell me about technology."}]
}, config=config)
```

**Expected Behavior:** Agent asks user to be more specific.

---

### Test 3: Complex Query (Should Require Multiple Iterations)

```python
config = {"configurable": {"thread_id": "test_3"}}

result = graph.invoke({
    "messages": [{"role": "user", "content": "Compare the economic impacts of renewable energy vs. fossil fuels in the last decade, considering both environmental costs and job creation."}]
}, config=config)
```

**Expected Behavior:** Agent performs 2-3 research cycles before synthesizing.

---

### Test 4: Infinite Loop Prevention

```python
# Manually create a state that would cause infinite looping
dangerous_state = {
    "messages": [...],
    "search_iterations": 10,  # Exceeds limit
    "research_complete": False
}

# Your routing logic should force END even though research isn't complete
```

**Requirement:** Document how your safety mechanisms prevent infinite loops.

---

## Part 8: State Inspection & Debugging (10 minutes)

After running Test 3, inspect the state history:

```python
history = list(graph.get_state_history(config))

print(f"Total checkpoints: {len(history)}")

for i, checkpoint in enumerate(history[:5]):
    print(f"\nCheckpoint {i+1}:")
    print(f"  Next node: {checkpoint.next}")
    print(f"  Iterations: {checkpoint.values.get('search_iterations')}")
    print(f"  Research complete: {checkpoint.values.get('research_complete')}")
```

**Deliverable 4:** Include a screenshot or text dump of your state history for one of the test cases.

---

## Part 9: Reflection & Analysis (Required Written Component)

Create a separate PDF document answering these questions:

### Question 1: Architectural Design (15 points)

**Prompt:**  
*"Explain your state schema design. Why did you include each field? Were there any fields you considered but decided not to include? Why?"*

**Grading Criteria:**
- Demonstrates understanding of state persistence
- Justifies design decisions with technical reasoning
- Considers trade-offs (e.g., "I didn't include X because it would increase memory overhead without providing sufficient value")

---

### Question 2: Stopping Criteria (15 points)

**Prompt:**  
*"How does your agent decide when to stop researching? What happens if your stopping criteria are too strict? Too lenient? Describe at least one edge case you encountered during testing."*

**Grading Criteria:**
- Identifies multiple stopping conditions (iteration limit, quality threshold, etc.)
- Discusses failure modes
- Provides concrete example from testing

---

### Question 3: Comparison to Linear Workflows (10 points)

**Prompt:**  
*"Could you have solved this problem with a simple DAG (no cycles)? What would you lose? What would you gain?"*

**Expected Answer Themes:**
- DAGs are simpler to debug but less adaptive
- Cycles enable iterative refinement but risk infinite loops
- Demonstrates critical thinking about when complexity is justified

---

### Question 4: Cost & Performance Analysis (10 points)

**Prompt:**  
*"Estimate the API cost of running your agent on Test 3. If you ran this 1,000 times per day, what would be the monthly cost? How could you optimize for cost without sacrificing quality?"*

**Hints:**
- GPT-4-mini costs approximately $0.150 per 1M input tokens, $0.600 per 1M output tokens
- Assume each LLM call consumes ~500 input tokens and ~200 output tokens
- Count how many LLM calls occur per research cycle

**Optimization Strategies to Discuss:**
- Caching tool results
- Using cheaper models for certain nodes
- Batching queries

---

## Submission Requirements

Your submission must include:

1. **Jupyter Notebook (.ipynb)** containing:
   - [ ] All code cells (runnable from top to bottom)
   - [ ] Markdown cells explaining your approach
   - [ ] Output of all test cases
   - [ ] Graph visualization
   - [ ] State history dump

2. **Reflection Document (PDF)** with:
   - [ ] Answers to all 4 reflection questions
   - [ ] Screenshots of key outputs
   - [ ] Your name and student ID

3. **Environment File:**
   - [ ] `requirements.txt` (generated via `uv pip freeze > requirements.txt`)
   - [ ] Do NOT include `.env` with your actual API key

---

## Assessment Rubric

### Code Quality (40 points)

- **State Schema Design** (10 pts)
  - Includes all required fields
  - Fields are properly typed
  - Clear docstrings

- **Node Implementation** (15 pts)
  - All 4 nodes are functional
  - Proper state updates (returns dicts, not raw objects)
  - Handles edge cases

- **Graph Assembly** (10 pts)
  - Correct edge definitions
  - Conditional routing works as intended
  - Graph compiles without errors

- **Testing** (5 pts)
  - All test cases run successfully
  - Outputs are documented

### Architectural Understanding (40 points)

- **Reflection Question 1** (15 pts)
- **Reflection Question 2** (15 pts)
- **Reflection Question 3** (10 pts)

### Engineering Practices (20 points)

- **Reproducibility** (10 pts)
  - Code runs on instructor's machine from `requirements.txt`
  - No hardcoded API keys
  - Clear instructions for setup

- **Performance Analysis** (10 pts)
  - Reflection Question 4 (cost estimation)

---

## Pass/Fail Criteria

### **Pass Criteria:**
- Environment is reproducible (code runs on instructor machine)
- API keys are secured (not hardcoded)
- All 4 required nodes are implemented
- Graph contains at least one cycle
- All reflection questions are answered with technical depth

### **Fail Criteria:**
- Hardcoded API keys anywhere in submission (immediate fail for security violation)
- Code crashes due to missing dependencies or syntax errors
- Lab is an exact copy of the demo (no research assistant implementation)
- Reflection answers lack technical reasoning (e.g., "I included this field because I thought it would be useful" without justification)

---

## Common Pitfalls & How to Avoid Them

### Pitfall 1: Infinite Loops

**Symptom:** Your agent runs forever, never reaching END.

**Cause:** Your `after_synthesis` routing function never returns END.

**Fix:**
```python
def after_synthesis(state: ResearchState) -> str:
    # Always add a safety counter
    if state.get("search_iterations", 0) >= 3:
        return END
    
    # Then check your actual conditions
    if state.get("research_complete"):
        return END
    else:
        return "plan_research"
```

---

### Pitfall 2: State Not Updating

**Symptom:** Your nodes run, but the state never changes.

**Cause:** You're returning the wrong data structure.

**Fix:**
```python
# ❌ WRONG
def my_node(state):
    return "some value"

# ✅ CORRECT
def my_node(state):
    return {"my_field": "some value"}
```

---

### Pitfall 3: Tools Not Being Called

**Symptom:** Your LLM never invokes the research tools.

**Cause:** The tools aren't bound to the LLM, or the docstrings are unclear.

**Fix:**
```python
# Ensure tools are bound BEFORE using in nodes
llm_with_tools = llm.bind_tools(tools)

# Make sure your tool docstrings are descriptive
@tool
def search_papers(topic: str) -> str:
    """Search for academic papers on a specific topic.
    
    Args:
        topic: A clear, specific research topic (e.g., 'quantum computing')
    """
```

---

## Extension Challenges (Optional, Extra Credit)

### Challenge 1: Human-in-the-Loop (10 bonus points)

Add a node that pauses execution and asks the user for feedback:
- "I found 3 sources. Do you want me to search for more?"
- Implement using LangGraph's `interrupt` functionality

---

### Challenge 2: Advanced Routing (10 bonus points)

Instead of simple conditionals, implement a routing function that uses an LLM to decide the next step:

```python
def llm_based_routing(state: ResearchState) -> str:
    """Use an LLM to intelligently decide the next node."""
    routing_prompt = f"""
    Based on the current research state:
    - Iterations: {state['search_iterations']}
    - Query: {state['research_query']}
    
    Should I:
    A) Continue research (more sources needed)
    B) Synthesize current findings
    C) Stop (sufficient information gathered)
    
    Respond with only the letter.
    """
    # TODO: Implement
```

---

### Challenge 3: Parallel Tool Execution (10 bonus points)

Modify your `execute_search` node to call multiple tools simultaneously using async:

```python
async def execute_search_parallel(state: ResearchState):
    """Execute multiple searches concurrently."""
    import asyncio
    
    tasks = [
        search_academic_papers.ainvoke(state['research_query']),
        search_news_articles.ainvoke(state['research_query']),
        query_knowledge_base.ainvoke(state['research_query'])
    ]
    
    results = await asyncio.gather(*tasks)
    # TODO: Process results
```

---

## Getting Help

### Debugging Checklist

If your code isn't working:

1. **Does your graph compile?**
   ```python
   try:
       graph = graph_builder.compile(checkpointer=memory)
       print("✓ Graph compiled successfully")
   except Exception as e:
       print(f"✗ Compilation error: {e}")
   ```

2. **Do all nodes return dicts?**
   ```python
   test_state = {"messages": [], "search_iterations": 0}
   result = my_node(test_state)
   assert isinstance(result, dict), "Node must return a dict!"
   ```

3. **Are your conditional edges returning valid node names?**
   ```python
   next_node = after_synthesis(test_state)
   assert next_node in ["plan_research", END], f"Invalid routing: {next_node}"
   ```

4. **Is your LLM receiving the right prompts?**
   - Add print statements in your nodes to see what's being sent to the LLM

---

### Office Hours Topics

Come to office hours if you need help with:
- Designing your state schema
- Debugging conditional routing logic
- Understanding checkpointer behavior
- Optimizing for cost or performance

---

## Final Checklist Before Submission

- [ ] Code runs without errors
- [ ] Graph visualization included
- [ ] All test cases documented
- [ ] State history inspected and included
- [ ] Reflection PDF is complete (all 4 questions answered)
- [ ] No hardcoded API keys
- [ ] `requirements.txt` is included
- [ ] I've re-read my reflection to ensure technical depth

---

**Good luck! This lab represents the culmination of everything you've learned about stateful, cyclic, agentic workflows. By completing it, you're building systems that go far beyond simple chatbots.**
