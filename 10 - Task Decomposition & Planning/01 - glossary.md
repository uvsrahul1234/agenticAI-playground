# Module 10: Task Decomposition & Planning
## Glossary - Theory & Concepts (The Lecture)

**Module Title:** Task Decomposition & Planning  
**Target Audience:** Agentic AI Class  
**Duration:** 45-60 Minutes  
**Learning Objective:** Master the mental process of decomposing complex, vague goals into structured, executable subtasks suitable for multi-agent systems.

**Reading:** https://github.com/sarwarbeing-ai/Agentic_Design_Patterns 

---

## Introduction: The Central Challenge of Agentic AI

Before an agent can *act*, it must *think*. Before tools can be called, a plan must exist. The most sophisticated multi-agent architecture is useless if the system cannot answer the fundamental question: **"How do I break this complex goal into actionable steps?"**

This module focuses on the most critical skill in agentic AI: **Task Decomposition** — the ability to transform ambiguous, high-level objectives into concrete, executable workflows. This is not about writing code; it's about *thinking like an orchestrator* before becoming one.

### Why This Module is Different

In previous modules, you've built agents, connected tools, and orchestrated teams. But all of those exercises started with *pre-defined tasks*. Real-world scenarios begin with vague requests:
- "Plan my vacation"
- "Research market competitors"
- "Optimize our supply chain"

**The hard part isn't executing the plan — it's generating the plan in the first place.**

---

## Core Concept Definitions

### 1. **Task Decomposition**

**Definition:** The process of breaking a complex, high-level goal into smaller, manageable, and executable subtasks that can be assigned to agents or tools.

**Analogy:** Think of a head chef receiving an order for "Thanksgiving dinner." The chef doesn't cook everything at once. They decompose the task:
- Subtask 1: Prepare the turkey (4 hours)
- Subtask 2: Make the sides (parallel with turkey)
- Subtask 3: Bake desserts (can start early)
- Subtask 4: Set the table (final step)

Each subtask has dependencies, timing constraints, and required tools (oven, utensils, ingredients). An agentic system must do the same mental decomposition for abstract goals.

**Key Insight:** Decomposition is a *cognitive skill*, not a programming technique. The LLM must be prompted to *think* before it *acts*.

---

### 2. **Task Planning**

**Definition:** The structured organization of decomposed subtasks, including their sequence, dependencies, and resource allocation.

**Real-World Example:** Consider the request: "Plan my vacation to Japan."

A *naive agent* might immediately search for flights. A *planning agent* first decomposes:
1. **Clarify constraints:** Budget? Duration? Interests?
2. **Research destinations:** Tokyo, Kyoto, Osaka?
3. **Check logistics:** Visa requirements, travel insurance
4. **Book transportation:** Flights, trains (JR Pass?)
5. **Reserve accommodations:** Hotels vs. Airbnb
6. **Plan activities:** Temples, food tours, hiking
7. **Create itinerary:** Day-by-day schedule

Notice that Step 4 *depends on* Step 2. You can't book hotels without knowing which cities you're visiting. **Planning encodes these dependencies.**

**Critical Point:** Without explicit planning, agents take premature actions, waste API calls, and produce incoherent results.

---

### 3. **Hierarchical Planning**

**Definition:** Organizing tasks in a parent-child tree structure, where high-level goals contain nested sub-goals.

**Example Hierarchy:**
```
Goal: Write a Research Report
├── Subtask 1: Literature Review
│   ├── 1.1: Search academic databases
│   ├── 1.2: Filter relevant papers
│   └── 1.3: Summarize findings
├── Subtask 2: Data Collection
│   ├── 2.1: Design survey
│   └── 2.2: Analyze results
└── Subtask 3: Draft Report
    ├── 3.1: Write introduction
    ├── 3.2: Write methodology
    └── 3.3: Write conclusion
```

**Why Hierarchical?** Some subtasks are themselves complex goals. "Literature Review" isn't atomic — it requires multiple steps. Hierarchical planning allows agents to recursively decompose until reaching *primitive actions* (e.g., "call search API").

**Application in Multi-Agent Systems:** In CrewAI's hierarchical mode, the manager agent decomposes the top-level task and delegates child tasks to specialist agents. Each specialist might further decompose their assigned task.

---

## Reasoning Frameworks: How Agents Think

### 4. **Chain of Thought (CoT)**

**Definition:** A prompting technique that forces the LLM to explicitly articulate its reasoning steps before producing an answer.

**Without CoT:**
```
User: "What's 347 × 823?"
Agent: "285,481" (wrong, hallucinated)
```

**With CoT:**
```
User: "What's 347 × 823? Think step-by-step."
Agent: "Let me break this down:
  347 × 800 = 277,600
  347 × 23 = 7,981
  Total: 277,600 + 7,981 = 285,581" (correct)
```

**Application to Task Decomposition:** CoT forces the agent to show its planning process:
```
User: "Plan a week-long trip to Iceland."
Agent: "Let me think through this:
  1. First, I need to know the budget and interests
  2. Research Iceland's geography (Ring Road? Reykjavik only?)
  3. Check seasonal weather (Northern Lights season?)
  4. Identify must-see sites (Blue Lagoon, Golden Circle)
  5. Determine transportation (rent car vs. guided tours)
  6. Book accommodations along the route
  7. Create day-by-day itinerary"
```

**Implementation:** Add explicit prompts:
- "Before taking any actions, list the steps you'll need to complete."
- "Think through the dependencies: what must happen first?"

**Limitation:** CoT is *sequential*. It doesn't handle branching or backtracking well. That's where ReAct and Tree of Thoughts come in.

---

### 5. **ReAct (Reasoning + Acting)**

**Definition:** An interleaved pattern where the agent alternates between reasoning (thinking) and acting (using tools), adjusting its plan based on observations.

**The ReAct Loop:**
```
1. Thought: "I need to find the capital of Japan."
2. Action: web_search("capital of Japan")
3. Observation: "Tokyo is the capital."
4. Thought: "Now I need to find tourist attractions in Tokyo."
5. Action: web_search("Tokyo tourist attractions")
6. Observation: [list of attractions]
7. Thought: "I have enough info to make recommendations."
8. Action: final_answer([compiled results])
```

**Key Advantage Over CoT:** ReAct doesn't require a complete plan upfront. The agent adapts its reasoning after each action. If a tool call fails or returns unexpected data, the agent can *replan*.

**Example Scenario:**
```
Goal: "Book a flight to Paris on June 15."
Thought: "I'll search for flights."
Action: search_flights("Paris", "June 15")
Observation: "No direct flights available on June 15."
Thought: "I need to adjust. Let me check June 14 or 16."
Action: search_flights("Paris", "June 14")
Observation: "Flight found for $450."
Thought: "This is acceptable. I'll book it."
Action: book_flight(...)
```

**Notice:** The agent didn't have a rigid plan. It adapted when the initial search failed.

**When to Use ReAct:** 
- Dynamic environments where information is incomplete
- Tasks requiring exploratory search (research, debugging)
- Situations where the initial plan might fail

**Implementation in SmolAgents:** SmolAgents' `CodeAgent` naturally follows ReAct:
```python
agent = CodeAgent(tools=[web_search, calculator], model=model)
agent.run("Find the current GDP of France and compare it to Germany.")
```
The agent will:
1. Think: "I need both countries' GDP."
2. Act: `web_search("France GDP 2024")`
3. Observe: "$3.1 trillion"
4. Think: "Now Germany's GDP."
5. Act: `web_search("Germany GDP 2024")`
6. Observe: "$4.5 trillion"
7. Think: "Germany's is higher by $1.4 trillion."
8. Act: `final_answer("Germany's GDP exceeds France's by $1.4T")`

---

### 6. **Tree of Thoughts (ToT)**

**Definition:** An extension of CoT that explores *multiple reasoning paths simultaneously*, evaluating each path and pruning unproductive branches.

**Analogy:** Think of a chess player considering multiple moves:
```
Current State: My turn
├── Path A: Move knight → Opponent captures queen (bad)
├── Path B: Move bishop → Forced checkmate in 3 moves (excellent!)
└── Path C: Castle → Safe but passive (acceptable)
```

The player mentally simulates multiple futures and picks the best path. ToT does the same for task decomposition.

**Example: "Plan my vacation to Italy"**

**Path 1: Rome-Focused Trip**
```
- Week 1: Rome (Colosseum, Vatican, Trastevere)
- Evaluation: Deep dive into history, but misses northern Italy
- Score: 7/10
```

**Path 2: Multi-City Tour**
```
- Day 1-3: Rome
- Day 4-5: Florence
- Day 6-7: Venice
- Evaluation: Covers major cities but feels rushed
- Score: 8/10
```

**Path 3: Regional Immersion**
```
- Week 1: Tuscany (Florence, Siena, countryside)
- Evaluation: Relaxed pace, wine tours, authentic experience
- Score: 9/10
```

**The agent evaluates all three paths before committing to Path 3.**

**Implementation Strategy:**
1. Generate 3-5 candidate plans
2. Use an "evaluator" LLM call to score each plan based on criteria (cost, feasibility, user preferences)
3. Select the highest-scoring plan
4. Execute that plan

**Code Sketch:**
```python
def tree_of_thoughts_planner(goal, criteria):
    plans = []
    for i in range(3):
        plan = llm.generate(f"Create vacation plan #{i+1} for: {goal}")
        score = llm.evaluate(plan, criteria)
        plans.append((plan, score))
    
    best_plan = max(plans, key=lambda x: x[1])
    return best_plan[0]
```

**When to Use ToT:**
- High-stakes decisions where exploring alternatives is valuable
- Creative tasks (multiple story outlines, marketing campaigns)
- Optimization problems (route planning, resource allocation)

**Trade-off:** ToT is expensive (multiple LLM calls). Use only when *quality* justifies the cost.

---

## Implementation Patterns

### 7. **Agent Orchestration**

**Definition:** The coordination of multiple agents to execute decomposed subtasks in a structured workflow.

**Key Question:** Once you've decomposed a task into subtasks, *who does what*?

**Example: Building a Newsletter (CrewAI Pattern)**
```
Task: "Create a weekly AI newsletter."
Decomposition:
  1. Research latest AI news
  2. Write article summaries
  3. Edit for tone and grammar
  4. Format as HTML email

Orchestration:
  Agent 1 (Researcher): Handles Step 1
    - Tools: web_search, article_fetcher
  Agent 2 (Writer): Handles Step 2
    - Tools: summarizer, style_guide
  Agent 3 (Editor): Handles Step 3
    - Tools: grammar_checker, fact_verifier
  Agent 4 (Formatter): Handles Step 4
    - Tools: html_generator, email_sender
```

**The orchestrator (manager agent) ensures:**
- Tasks flow in the right order (can't edit before writing)
- Agents don't conflict (two agents editing the same section)
- Failures are handled (if research fails, notify the Writer to wait)

**Contrast with Single-Agent:** A single agent might get confused juggling all four roles. Orchestration allows specialization.

---

### 8. **Workflow Orchestration**

**Definition:** Managing the flow, dependencies, and execution order of tasks, often using state machines or graphs.

**Implementation: LangGraph**

LangGraph represents workflows as directed graphs:
```python
from langgraph.graph import StateGraph

workflow = StateGraph()
workflow.add_node("research", research_agent)
workflow.add_node("write", writer_agent)
workflow.add_node("edit", editor_agent)

workflow.add_edge("research", "write")  # write depends on research
workflow.add_edge("write", "edit")      # edit depends on write

workflow.set_entry_point("research")
workflow.set_finish_point("edit")
```

**Key Feature:** Conditional edges. After research, the agent might decide:
- If sufficient sources found → proceed to write
- If insufficient → loop back to research with refined query

**Cyclic Workflows:**
```python
workflow.add_conditional_edge(
    "write",
    lambda state: "edit" if quality_check(state) else "research"
)
```

This allows the agent to *replan* mid-execution.

---

### 9. **Task Routing**

**Definition:** Dynamically assigning subtasks to the most appropriate specialized agent based on task requirements.

**Example: Multi-Domain Question Answering**
```
User: "Compare the GDP of Japan to the plot of Inception."

Task Router Analysis:
  - Subtask 1: "Find Japan's GDP" → Route to EconomicsAgent (has finance tools)
  - Subtask 2: "Summarize Inception plot" → Route to MediaAgent (has movie database)
  - Subtask 3: "Compare the two" → Route to SynthesisAgent (combines results)
```

**Implementation in AutoGen:**
```python
def route_task(task_description):
    if "GDP" in task_description or "economy" in task_description:
        return economics_agent
    elif "movie" in task_description or "film" in task_description:
        return media_agent
    else:
        return general_agent
```

**Advanced Routing:** Use an LLM to classify tasks:
```python
classification = llm.predict(f"Which agent should handle: {task}? Options: [economics, media, general]")
agent = agent_map[classification]
```

---

## Common Decomposition Strategies

### 10. **Sequential Decomposition**

**Definition:** Tasks must be completed in strict order (A → B → C). Each step depends on the previous step's output.

**Example: Software Installation**
```
1. Check system requirements
2. Download installer
3. Run installer
4. Configure settings
5. Verify installation
```

**Failure Mode:** If Step 3 fails (installer corrupted), Steps 4-5 cannot proceed. The agent must detect this and either retry or abort.

**Implementation:**
```python
steps = [check_requirements, download, install, configure, verify]
for step in steps:
    result = step()
    if result.failed:
        return f"Failed at {step.__name__}"
```

---

### 11. **Parallel Decomposition**

**Definition:** Independent tasks that can run simultaneously to save time.

**Example: Event Planning**
```
Parallel Tasks:
  - Task A: Book venue
  - Task B: Order catering
  - Task C: Send invitations

None of these depend on each other. All can start immediately.
```

**Implementation with asyncio:**
```python
import asyncio

async def plan_event():
    results = await asyncio.gather(
        book_venue(),
        order_catering(),
        send_invitations()
    )
    return results
```

**Key Advantage:** If each task takes 30 minutes, sequential execution takes 90 minutes. Parallel execution takes 30 minutes.

**When to Use:** When subtasks share no dependencies and don't conflict over shared resources.

---

### 12. **Hierarchical Decomposition**

**Definition:** Parent tasks contain child subtasks, which may themselves contain sub-subtasks, forming a tree structure.

**Example: "Launch a Product"**
```
Launch Product
├── Market Research
│   ├── Competitor analysis
│   ├── Customer surveys
│   └── Pricing strategy
├── Product Development
│   ├── Design prototype
│   ├── User testing
│   └── Final engineering
└── Marketing Campaign
    ├── Social media ads
    ├── Email campaign
    └── Press releases
```

**Each top-level task is decomposed recursively until reaching atomic actions.**

**Implementation in CrewAI (Hierarchical Mode):**
```python
manager = Agent(role="Project Manager", goal="Launch product", process=Process.hierarchical)
researcher = Agent(role="Market Researcher")
developer = Agent(role="Product Developer")
marketer = Agent(role="Marketing Specialist")

crew = Crew(agents=[manager, researcher, developer, marketer])
crew.kickoff()
```

The manager decomposes "Launch product" into three major tasks and delegates each to a specialist. Each specialist further decomposes their task.

---

### 13. **DAG (Directed Acyclic Graph) Decomposition**

**Definition:** Tasks have complex dependencies that form a graph structure (not just a tree or sequence).

**Example: Data Pipeline**
```
    ┌─→ Load Database A ─┐
    │                    ↓
Start ─┤              Join Data → Analyze → Report
    │                    ↑
    └─→ Load Database B ─┘
```

Dependencies:
- "Join Data" requires *both* Database A and B to be loaded
- "Analyze" depends on "Join Data"
- "Report" depends on "Analyze"

**This is a DAG:** There are multiple paths, but no cycles.

**Implementation with LangGraph:**
```python
workflow.add_node("load_a", load_database_a)
workflow.add_node("load_b", load_database_b)
workflow.add_node("join", join_data)
workflow.add_node("analyze", analyze_data)
workflow.add_node("report", generate_report)

workflow.add_edge("load_a", "join")
workflow.add_edge("load_b", "join")
workflow.add_edge("join", "analyze")
workflow.add_edge("analyze", "report")
```

**Key Feature:** The "join" node waits for both inputs before proceeding.

---

## Specialized Planning Frameworks

### 14. **ReWOO (Reasoning WithOut Observation)**

**Definition:** A two-phase approach where the agent plans *all* steps upfront (without executing them), then executes the plan in one batch.

**Phase 1: Planning**
```
Task: "Find the capital of France and its population."
Plan:
  Step 1: capital = web_search("capital of France")
  Step 2: population = web_search(f"population of {capital}")
  Step 3: final_answer(f"{capital} has {population} people")
```

**Phase 2: Execution**
```
Execute Step 1 → Observation: "Paris"
Execute Step 2 → Observation: "2.1 million"
Execute Step 3 → Output: "Paris has 2.1 million people"
```

**Key Advantage:** Predictable, parallelizable, no wasted LLM calls for re-planning.

**Key Disadvantage:** Cannot adapt if Step 1 fails or returns unexpected data.

**When to Use ReWOO:** When the task is well-defined and the environment is deterministic (e.g., querying databases, math calculations).

---

### 15. **Plan-and-Execute**

**Definition:** A two-phase approach similar to ReWOO, but the execution phase can trigger *re-planning* if needed.

**Example:**
```
Task: "Book the cheapest flight to Tokyo in June."

Initial Plan:
  1. Search for flights in June
  2. Sort by price
  3. Book the cheapest one

Execution:
  Step 1 → Result: No flights under $1000
  Trigger Re-Plan: "User's budget is $800. Suggest alternative dates or airlines."
  
Revised Plan:
  1. Search for flights in May or July
  2. Check budget airlines
  3. Book within budget
```

**Implementation:**
```python
def plan_and_execute(task):
    plan = generate_plan(task)
    
    for step in plan:
        result = execute_step(step)
        
        if result.failed:
            print(f"Step failed: {step}. Re-planning...")
            plan = replan(task, plan, result)  # Regenerate remaining steps
    
    return final_result
```

**When to Use:** Tasks where initial information is incomplete (e.g., booking travel, scheduling meetings).

---

## Architectural Visualization: The Decomposition Process

Let's visualize how decomposition works in a multi-agent system:

```
                     ┌─────────────────────┐
                     │   User Query:       │
                     │ "Plan my vacation"  │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │  Decomposition LLM  │
                     │  (Planner Agent)    │
                     └──────────┬──────────┘
                                │
                   Generates task breakdown
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
  ┌──────────┐          ┌──────────┐          ┌──────────┐
  │ Subtask 1│          │ Subtask 2│          │ Subtask 3│
  │ Research │          │ Book     │          │ Create   │
  │ Destination        │ Flights  │          │ Itinerary│
  └────┬─────┘          └────┬─────┘          └────┬─────┘
       │                     │                     │
       │                     │                     │
  Assigned to           Assigned to           Assigned to
  ResearchAgent         BookingAgent          PlannerAgent
       │                     │                     │
       ▼                     ▼                     ▼
  [web_search]          [flight_api]          [calendar_tool]
  [weather_tool]        [payment_tool]        [map_tool]
       │                     │                     │
       └─────────────────────┴─────────────────────┘
                             │
                    Results aggregated
                             │
                             ▼
                   ┌─────────────────────┐
                   │  Final Output:      │
                   │  "7-day Japan trip  │
                   │   with itinerary"   │
                   └─────────────────────┘
```

**Key Takeaway:** The planner doesn't execute tasks—it identifies them and delegates to specialists.

---

## Decision Matrix: Which Decomposition Strategy?

| **Scenario**                        | **Best Strategy**        | **Reasoning**                                                                 |
|-------------------------------------|--------------------------|-------------------------------------------------------------------------------|
| Steps must happen in order          | Sequential               | Each step depends on the previous result                                      |
| Steps are independent               | Parallel                 | Save time by running simultaneously                                           |
| Task has nested complexity          | Hierarchical             | Top-level goals contain sub-goals                                             |
| Complex dependencies                | DAG                      | Multiple paths converge (e.g., waiting for multiple data sources)             |
| Uncertain environment               | ReAct                    | Need to adapt plan based on observations                                      |
| Deterministic, batch operations     | ReWOO                    | Plan everything upfront, execute in batch                                     |
| Need to explore alternatives        | Tree of Thoughts         | Evaluate multiple plans before committing                                     |
| High-stakes, creative tasks         | ToT + Human-in-the-Loop  | Explore options, have human select best path                                  |

---

## Critical Insights: What Students Must Internalize

### 1. **Decomposition is the Bottleneck**
An agent with perfect tools but poor planning will fail. Conversely, a well-planned system with mediocre tools will succeed. **Invest time in prompt engineering the planning step.**

### 2. **Vague Goals are the Enemy**
"Plan my vacation" is a *bad* task for an agent. The agent must first *elicit constraints*:
- Budget? Duration? Interests? Mobility? Dietary restrictions?

**Better prompt:**
```
"Plan a 7-day vacation to Japan for 2 adults. Budget: $5000. Interests: history, food. 
 Prefer public transportation. Avoid hiking due to mobility issues."
```

Now the agent has *decomposable structure*.

### 3. **Planning Incurs Cost**
Every planning step is an LLM call. ToT might require 5x more tokens than ReAct. Design systems where the cost of planning is justified by the cost of failure. For simple tasks ("summarize this document"), skip elaborate planning.

### 4. **Humans Decompose Intuitively; LLMs Need Prompting**
You naturally break "make dinner" into "chop vegetables, cook rice, season meat." LLMs don't. They need:
- "Before cooking, list all ingredients and steps."
- "Think through dependencies: what must be prepped first?"

**Never assume the LLM will plan without explicit instruction.**

---

## Next Steps: From Theory to Practice

In the upcoming Demo (Phase 2), you will observe these concepts in action:
- Watching an agent transform "Plan my vacation" into a structured task graph
- Seeing ReAct vs. ReWOO in a live coding session
- Debugging when an agent skips planning and takes premature actions

In the Lab (Phase 3), you will implement your own decomposition system, forcing you to mentally experience the challenge of turning ambiguity into structure.

**Remember:** The goal isn't to memorize frameworks. The goal is to *think like a decomposer* — to instinctively recognize when a task is too complex for a single action and must be broken down.

---

## Summary: Key Terms at a Glance

| **Term**                  | **One-Sentence Definition**                                                                 |
|---------------------------|---------------------------------------------------------------------------------------------|
| Task Decomposition         | Breaking a complex goal into smaller, executable subtasks                                   |
| Task Planning              | Structuring subtasks with dependencies and execution order                                  |
| Hierarchical Planning      | Organizing tasks in a tree where parent goals contain child sub-goals                       |
| Chain of Thought (CoT)     | Forcing the LLM to articulate reasoning steps before answering                              |
| ReAct                      | Interleaving reasoning and action, adapting the plan based on observations                  |
| Tree of Thoughts (ToT)     | Exploring multiple reasoning paths and selecting the best one                               |
| Agent Orchestration        | Coordinating multiple specialized agents to execute decomposed tasks                        |
| Workflow Orchestration     | Managing task flow using state machines or graphs (e.g., LangGraph)                         |
| Task Routing               | Dynamically assigning subtasks to the most appropriate agent                                |
| Sequential Decomposition   | Tasks executed in strict order (A → B → C)                                                  |
| Parallel Decomposition     | Independent tasks executed simultaneously                                                   |
| Hierarchical Decomposition | Recursive task breakdown into nested subtasks                                               |
| DAG Decomposition          | Tasks with complex dependencies forming a directed acyclic graph                            |
| ReWOO                      | Planning all steps upfront, then executing in batch                                         |
| Plan-and-Execute           | Two-phase approach allowing re-planning if execution fails                                  |

---

**End of Glossary**

In the next phase, you'll see these concepts come alive in a live demonstration where we'll decompose a complex real-world task together.
