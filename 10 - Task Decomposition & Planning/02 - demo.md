# Module 10: Task Decomposition & Planning
## Demo - Guided Analysis (The Live Demo)

**Duration:** 45-60 Minutes  
**Goal:** Live demonstration where students observe real-time task decomposition, predict outcomes, debug planning failures, and analyze agent reasoning.  
**Source Material:** This demonstration script (to be converted to executable Jupyter Notebook)  
**Pedagogy:** Predict-Observe-Explain (POE) — Students predict what will happen before each code cell runs.

---

## Pre-Demo Setup and Learning Objectives

### Today's Mission
By the end of this demo, you will have witnessed:
1. An agent **failing** to decompose a task (and why it happened)
2. The **same agent** succeeding after proper prompting
3. Multiple decomposition strategies (CoT, ReAct, ToT) applied to the same problem
4. A multi-agent system where the manager decomposes and delegates tasks
5. Live debugging of planning failures

### Environment & Safety Check

#### Security Focus: API Key Management
Let's verify your environment is secure before we start calling expensive LLM APIs.

```python
# ❌ WRONG WAY - Never do this
api_key = "sk-1234567890abcdef"  # Hardcoded key = instant security violation

# ✅ RIGHT WAY
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("API key not found. Check your .env file.")
print("✅ API key loaded securely")
```

**Common Error Simulation:** Let's intentionally trigger a connection error to practice debugging.

```python
# Intentional error: wrong API endpoint
try:
    import openai
    openai.api_base = "https://wrong-url.com"  # Wrong endpoint
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "test"}]
    )
except Exception as e:
    print(f"❌ Error caught: {e}")
    print("👉 Solution: Verify openai.api_base or remove it to use default")
    
# Fix it
openai.api_base = "https://api.openai.com/v1"  # Correct endpoint
print("✅ Connection fixed")
```

---

## Part 1: The Failure Case — Agent Without Decomposition

### The Scenario: Planning a Vacation (Naive Approach)

**Critical Question to Students (BEFORE running):** 
> "I'm going to give an agent the vague task: 'Plan my vacation.' What do you think will happen?"

**Expected Student Predictions:**
- "It will immediately search for flights"
- "It will ask clarifying questions"
- "It will generate a generic plan"

Let's see what actually happens:

```python
from smolagents import CodeAgent, InferenceClientModel, tool

# Simple agent with web search tool
@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    # Simulated search results
    results = {
        "flights": "Flight to Paris: $800",
        "hotels": "Hotel in Paris: $150/night",
        "weather": "Paris weather in June: 75°F"
    }
    return results.get(query, "No results found")

model = InferenceClientModel(model_id="Qwen/Qwen2.5-72B-Instruct")
agent = CodeAgent(tools=[web_search], model=model)

# The vague request
result = agent.run("Plan my vacation.")
print(result)
```

**❌ Expected Output (Failure Mode):**
```
Thought: I need to search for vacation destinations.
Action: web_search("vacation destinations")
Observation: No results found
Thought: Let me try searching for flights.
Action: web_search("flights")
Observation: Flight to Paris: $800
Final Answer: "You should fly to Paris for $800."
```

**Analysis (Class Discussion):**
- **What went wrong?** The agent took immediate action without understanding the user's constraints (budget, duration, interests, destination preferences).
- **Why did it fail?** No explicit instruction to *plan first* before acting.
- **Real-world consequence:** Wasted API calls, irrelevant recommendations, frustrated users.

---

## Part 2: Adding Chain-of-Thought (CoT) Decomposition

### The Fix: Force the Agent to Think

**Critical Question to Students:**
> "How would you modify the prompt to make the agent decompose the task first?"

**Expected Answers:**
- "Tell it to list all steps before taking action"
- "Ask it to clarify constraints first"
- "Use 'Think step-by-step' prompting"

Let's implement this:

```python
# Enhanced prompt with CoT instruction
enhanced_instructions = """
Before taking ANY actions, you must:
1. Identify what information is missing (budget, duration, destination, interests)
2. Create a step-by-step plan
3. List the subtasks in order
4. Only then begin executing

Think through the dependencies: what must you know before you can book flights?
"""

agent_with_cot = CodeAgent(
    tools=[web_search], 
    model=model,
    instructions=enhanced_instructions
)

result = agent_with_cot.run("Plan my vacation.")
print(result)
```

**✅ Expected Output (Success):**
```
Thought: Before I can plan a vacation, I need to gather essential information.

Missing Information:
1. Budget - How much can the user spend?
2. Duration - How many days?
3. Destination preferences - Beach, city, mountains?
4. Interests - Food, culture, adventure, relaxation?
5. Travel dates - When do they want to go?

Step-by-Step Plan:
1. Ask user for missing information
2. Research destinations matching their preferences
3. Check flight availability and costs
4. Check accommodation options
5. Research activities based on interests
6. Create day-by-day itinerary
7. Calculate total cost

Action: Ask user for clarification
"To plan your vacation, I need to know:
- What's your budget?
- How many days?
- Where do you want to go?
- What are you interested in?"
```

**Analysis (Class Discussion):**
- **What changed?** The agent now recognizes the task is *underspecified*.
- **Key insight:** CoT forces the agent to expose its reasoning, revealing gaps in information.
- **Trade-off:** More tokens used for planning, but prevents wasted tool calls.

---

## Part 3: ReAct in Action — Adaptive Decomposition

### The Scenario: Agent Adapts Mid-Execution

Now let's give the agent more specific information and watch it adapt:

```python
@tool
def flight_search(origin: str, destination: str, date: str) -> dict:
    """Search for flights between two cities."""
    # Simulated API
    flights = {
        ("NYC", "Paris", "2024-06-15"): {"price": 800, "available": True},
        ("NYC", "Paris", "2024-06-16"): {"price": 650, "available": True},
        ("NYC", "London", "2024-06-15"): {"price": 900, "available": False}
    }
    key = (origin, destination, date)
    return flights.get(key, {"price": None, "available": False})

@tool
def hotel_search(city: str, checkin: str, nights: int) -> dict:
    """Search for hotels in a city."""
    return {
        "city": city,
        "price_per_night": 120,
        "available": True,
        "total": 120 * nights
    }

agent_react = CodeAgent(
    tools=[flight_search, hotel_search], 
    model=model,
    instructions="Use ReAct: alternate between Thought and Action. Adapt your plan if tools return unexpected results."
)

# More specific request
task = """Plan a 5-day trip to Paris from NYC, leaving June 15, 2024. 
Budget: $2000. Interested in museums and food."""

result = agent_react.run(task)
```

**Critical Question (BEFORE output):**
> "Predict: What will the agent do first? What might cause it to re-plan?"

**✅ Expected Output (ReAct Loop):**
```
Thought: I need to check flight availability for June 15 from NYC to Paris.
Action: flight_search("NYC", "Paris", "2024-06-15")
Observation: {"price": 800, "available": True}

Thought: Flight is available at $800. That leaves $1200 for 5 nights of hotel + activities.
          $1200 / 5 nights = $240/night budget for hotel.
Action: hotel_search("Paris", "2024-06-15", 5)
Observation: {"price_per_night": 120, "total": 600}

Thought: Perfect! Hotel costs $600 total, leaving $600 for activities (museums, food).
         This fits the budget. Now I'll create the itinerary.

Subtask Plan:
1. ✅ Book flight: $800
2. ✅ Book hotel: $600
3. ⏳ Research museums (Louvre, Musée d'Orsay)
4. ⏳ Research food tours
5. ⏳ Create day-by-day schedule

Final Answer: "5-day Paris trip planned:
- Flight: $800
- Hotel: $600 (5 nights @ $120/night)
- Remaining for activities: $600
[Detailed itinerary would follow]"
```

**Now let's inject a failure:**

```python
# What if the first flight is unavailable?
task_with_conflict = """Plan a 5-day trip to London from NYC, leaving June 15, 2024. 
Budget: $2000."""

result_conflict = agent_react.run(task_with_conflict)
```

**Expected ReAct Adaptation:**
```
Thought: I'll check for flights to London on June 15.
Action: flight_search("NYC", "London", "2024-06-15")
Observation: {"price": 900, "available": False}

Thought: ❌ No flights available on June 15. I need to replan.
         Let me check alternate dates.
Action: flight_search("NYC", "London", "2024-06-16")
Observation: {"price": 850, "available": True}

Thought: ✅ Found a flight on June 16 for $850. I'll adjust the plan to start on June 16.
[Continues with hotel search for June 16...]
```

**Key Observation for Students:**
- The agent didn't blindly follow a pre-made plan.
- When the tool returned `available: False`, it *re-planned*.
- This is the power of ReAct: **dynamic adaptation**.

---

## Part 4: Tree of Thoughts — Exploring Alternatives

### The Scenario: Which Vacation Plan is Best?

Let's give the agent a creative task: generate 3 different vacation plans and pick the best one.

```python
def tree_of_thoughts_vacation(budget: int, days: int):
    """Generate and evaluate multiple vacation plans."""
    
    # Phase 1: Generate 3 candidate plans
    plans = []
    
    plan_1 = {
        "destination": "Paris",
        "style": "Cultural immersion",
        "activities": ["Louvre", "Eiffel Tower", "Food tours"],
        "cost": 1800,
        "pros": "Rich history, world-class museums",
        "cons": "Expensive dining"
    }
    
    plan_2 = {
        "destination": "Barcelona",
        "style": "Beach + Culture",
        "activities": ["Sagrada Familia", "Beach time", "Tapas hopping"],
        "cost": 1500,
        "pros": "Great weather, affordable, diverse activities",
        "cons": "Very touristy in summer"
    }
    
    plan_3 = {
        "destination": "Prague",
        "style": "Budget adventure",
        "activities": ["Castle tour", "Beer tasting", "Old Town exploration"],
        "cost": 1200,
        "pros": "Affordable, underrated architecture",
        "cons": "Less English spoken"
    }
    
    plans = [plan_1, plan_2, plan_3]
    
    # Phase 2: Evaluate each plan
    evaluation_prompt = f"""
    User constraints:
    - Budget: ${budget}
    - Duration: {days} days
    - Interests: Culture, food, some relaxation
    
    Evaluate these 3 plans and score each from 1-10 based on:
    - Budget fit (does it stay under budget?)
    - Activity variety
    - Value for money
    - Overall appeal
    
    Plans:
    {plans}
    
    Return: {{"best_plan": <destination>, "reasoning": <why>, "score": <1-10>}}
    """
    
    # Call LLM to evaluate
    evaluation = agent_react.run(evaluation_prompt)
    return evaluation

# Run ToT
print("🌳 Tree of Thoughts: Exploring 3 vacation plans...")
best_plan = tree_of_thoughts_vacation(budget=2000, days=5)
print(best_plan)
```

**Expected Output:**
```json
{
  "best_plan": "Barcelona",
  "reasoning": "Barcelona fits the budget perfectly at $1500, offers both beach relaxation and cultural activities (Sagrada Familia), and has excellent food (tapas). Prague is cheaper but doesn't offer beach relaxation. Paris exceeds the budget with expensive dining.",
  "score": 9
}
```

**Class Discussion:**
- **When is ToT worth the cost?** When the decision is high-stakes (spending $2000) and exploring alternatives adds value.
- **When is it overkill?** For simple tasks like "summarize this document."
- **Trade-off:** ToT requires 3-5x more LLM calls (one for each plan + one evaluation).

---

## Part 5: Multi-Agent Decomposition with CrewAI

### The Scenario: Hierarchical Planning

Now let's see how a *manager agent* decomposes and delegates:

```python
from crewai import Agent, Task, Crew, Process

# Define specialized agents
researcher = Agent(
    role="Travel Researcher",
    goal="Find the best travel deals and destination information",
    backstory="Expert at finding hidden gems and good deals",
    tools=[web_search]
)

planner = Agent(
    role="Itinerary Planner",
    goal="Create detailed day-by-day itineraries",
    backstory="Expert at optimizing time and creating balanced schedules"
)

budget_analyst = Agent(
    role="Budget Analyst",
    goal="Ensure the trip stays within budget",
    backstory="Expert at cost optimization and finding savings"
)

# Define tasks
research_task = Task(
    description="Research the best European destinations for a 5-day trip under $2000",
    agent=researcher,
    expected_output="List of 3 destinations with pros/cons"
)

itinerary_task = Task(
    description="Create a detailed 5-day itinerary for the chosen destination",
    agent=planner,
    expected_output="Day-by-day schedule with activities and timing"
)

budget_task = Task(
    description="Break down the costs and ensure we stay under budget",
    agent=budget_analyst,
    expected_output="Itemized budget with total cost"
)

# Create crew with hierarchical process
crew = Crew(
    agents=[researcher, planner, budget_analyst],
    tasks=[research_task, itinerary_task, budget_task],
    process=Process.hierarchical,
    verbose=True
)

# The manager (implicitly created) will decompose the goal
result = crew.kickoff(inputs={"budget": 2000, "days": 5, "interests": "culture, food"})
```

**Live Demo Output (Step-by-Step):**

```
🎯 Manager Agent: Analyzing task "Plan 5-day vacation"

Decomposition:
├── Subtask 1: Research destinations → Assign to Travel Researcher
│   └── Tools: web_search
├── Subtask 2: Create itinerary → Assign to Itinerary Planner
│   └── Depends on: Subtask 1 results
└── Subtask 3: Budget validation → Assign to Budget Analyst
    └── Depends on: Subtask 2 results

Executing...

👤 Travel Researcher:
"I found 3 destinations:
1. Barcelona - $1500 total
2. Prague - $1200 total
3. Lisbon - $1400 total
Recommendation: Barcelona for best value"

👤 Itinerary Planner:
"5-day Barcelona itinerary:
Day 1: Sagrada Familia, Gothic Quarter
Day 2: Park Güell, Beach time
Day 3: Food tour, Montjuïc
Day 4: Day trip to Montserrat
Day 5: La Rambla, shopping, departure"

👤 Budget Analyst:
"Budget breakdown:
- Flights: $650
- Hotel (4 nights): $480
- Activities: $250
- Food: $300
Total: $1680 ✅ Under budget by $320"

✅ Manager: All subtasks complete. Final plan approved.
```

**Critical Discussion Points:**
1. **Division of Labor:** Each agent focused on their specialty.
2. **Dependency Management:** Planner couldn't start until Researcher finished.
3. **Manager's Role:** Orchestrated the flow, ensured no conflicts.

**Live Debugging Exercise:**

Let's intentionally break something:

```python
# What if the Budget Analyst finds the plan exceeds budget?
# Simulate by manually setting flights to $900

# Expected behavior:
# Manager detects failure → triggers re-planning → asks Researcher for cheaper destination
```

**Have students predict:** 
> "What should the manager do if the budget check fails?"

---

## Part 6: Comparing Decomposition Strategies

### Live Comparison: Same Task, Different Approaches

Let's solve the same task with 3 different strategies and compare:

**Task:** "Find the best laptop for a college student under $1000."

#### Strategy 1: No Decomposition (Baseline)
```python
result_naive = agent.run("Find the best laptop for a college student under $1000.")
```

**Output:**
```
Action: web_search("best laptop under 1000")
Final Answer: "Buy the Dell XPS 13 for $999"
```

**Problem:** No consideration of student needs (gaming? programming? note-taking?).

---

#### Strategy 2: Chain of Thought
```python
result_cot = agent.run("""
Find the best laptop for a college student under $1000.
Think step-by-step:
1. What do college students need in a laptop?
2. What are the key specs to look for?
3. Compare options in that price range.
""")
```

**Output:**
```
Thought: College students need:
- Long battery life (all-day classes)
- Lightweight (carrying to campus)
- Good keyboard (lots of typing)
- Sufficient RAM (multitasking)

Key specs: 8GB RAM minimum, SSD, 8+ hour battery

Comparing options:
- Dell XPS 13: Great keyboard, but expensive at $999
- MacBook Air M1: Excellent battery, but $999
- Lenovo IdeaPad: Good value at $650

Recommendation: Lenovo IdeaPad for budget-conscious student
```

**Better!** The agent considered *why* the laptop is being purchased.

---

#### Strategy 3: ReAct with Tool Use
```python
@tool
def laptop_database(price_max: int, specs: dict) -> list:
    """Search laptop database with filters."""
    return [
        {"name": "Lenovo IdeaPad", "price": 650, "battery": 10, "weight": 3.5},
        {"name": "HP Pavilion", "price": 750, "battery": 8, "weight": 4.2},
        {"name": "ASUS ZenBook", "price": 899, "battery": 12, "weight": 2.9}
    ]

result_react = agent_react.run("Find the best laptop for a college student under $1000.")
```

**Output:**
```
Thought: I need to search with specific criteria for students.
Action: laptop_database(1000, {"battery": ">8", "weight": "<4"})
Observation: [Lenovo IdeaPad, ASUS ZenBook]

Thought: ASUS ZenBook has better battery (12h) and lighter weight, but costs $899.
         Lenovo is $650 with 10h battery.
         
For a budget-conscious student, Lenovo is better value.
For a student who prioritizes portability and battery, ASUS is worth the extra $249.

Final Answer: "I recommend Lenovo IdeaPad ($650) for best value, 
or ASUS ZenBook ($899) if you prioritize ultra-portability and all-day battery."
```

**Analysis:**
- **Naive:** 1 tool call, generic answer
- **CoT:** 2-3 calls, better reasoning
- **ReAct:** 3-4 calls, tailored recommendations with trade-offs

---

## Part 7: Debugging Exercise — When Decomposition Fails

### Common Failure Mode: Premature Optimization

Let's watch an agent over-decompose:

```python
result_overplanning = agent.run("""
Task: "Add 2 + 2"

Instructions: 
1. Break this task into subtasks
2. Create a detailed plan
3. Consider all edge cases
4. Validate the result
""")
```

**Output (Anti-Pattern):**
```
Decomposition:
1. Verify that 2 is an integer
2. Verify that the second 2 is an integer
3. Check if addition is the correct operation
4. Perform addition
5. Validate result is numeric
6. Check for overflow
7. Return result

[Executes all 7 steps]

Final Answer: 4
```

**Problem:** Task was too simple to warrant this complexity!

**Class Discussion:**
> "When is decomposition overkill? How do we know when to *not* decompose?"

**Rule of Thumb:**
- If the task can be solved in 1 LLM call, don't decompose.
- Decompose when:
  - Multiple tools needed
  - Dependencies exist
  - Decision points arise mid-execution

---

## Live Analysis: Does the Class Agree?

**Exercise:** Show an agent's plan and ask students to critique it:

```python
plan = """
Task: "Book a restaurant for dinner tonight"

Agent's Plan:
1. Search for restaurants near user's location
2. Filter by cuisine type
3. Check availability
4. Make reservation
5. Send confirmation email
"""
```

**Discussion Questions:**
1. Is this a good decomposition? (Yes, logical flow)
2. What's missing? (User preferences: cuisine, price range, party size)
3. Can any steps run in parallel? (No, they're sequential dependencies)
4. What if Step 3 (availability) fails? (Agent should re-plan with different restaurant)

---

## Variables to Change: Hands-On Experimentation

**Instructor:** Now let's modify parameters and re-run. Students predict outcomes.

### Experiment 1: Change Temperature
```python
# High temperature = more creative plans
agent_creative = CodeAgent(model=model, temperature=0.9)

# Low temperature = deterministic plans
agent_deterministic = CodeAgent(model=model, temperature=0.1)

task = "Plan a unique 3-day weekend trip"

result_creative = agent_creative.run(task)      # Might suggest skydiving in Iceland
result_deterministic = agent_deterministic.run(task)  # Likely suggests Paris or Rome
```

**Question:** Which temperature is better for vacation planning?

---

### Experiment 2: Change Max Planning Depth
```python
# Shallow decomposition (max 2 levels)
agent_shallow = CodeAgent(instructions="Break tasks into maximum 2 levels")

# Deep decomposition (recursive)
agent_deep = CodeAgent(instructions="Recursively decompose until reaching atomic actions")

task = "Launch a new product"

result_shallow = agent_shallow.run(task)
# Output: 1. Research, 2. Build, 3. Market

result_deep = agent_deep.run(task)
# Output: 20+ subtasks with 3 levels of nesting
```

**Question:** When is deep decomposition necessary?

---

## Final Live Demo: Putting It All Together

Let's end with a complex, real-world scenario:

```python
complex_task = """
You are an executive assistant. Your boss just said:
"I need to visit our Tokyo office next month for 3 days, 
meet with the local team, and also have a day to explore the city."

Decompose this task and execute it using:
- flight_search tool
- hotel_search tool
- meeting_scheduler tool
- city_guide tool

Budget: $3000
"""

# Students predict: What should the agent do FIRST?
# Answer: Clarify "next month" — which dates specifically?

result_complex = agent_react.run(complex_task)
```

**Expected Output:**
```
Thought: I'm missing specific dates. I'll assume 15-18 of next month.

Decomposition:
1. ⏳ Search flights (need dates confirmed)
2. Book hotel near Tokyo office
3. Schedule meetings with local team
4. Research 1 day of activities
5. Create itinerary PDF

Action: Assuming June 15-18. Searching flights...
[Continues with ReAct loop]
```

---

## Summary: What We Observed

Today you witnessed:
1. ❌ **Failure without decomposition** → Agent took random actions
2. ✅ **Success with CoT** → Agent planned before acting
3. 🔄 **ReAct adapting** → Agent re-planned when tools failed
4. 🌳 **Tree of Thoughts** → Explored multiple plans, picked best
5. 👥 **Multi-agent hierarchical** → Manager decomposed, agents specialized
6. ⚠️ **Debugging pitfalls** → Over-planning and under-specifying

**Key Takeaway:** Decomposition is the difference between an agent that *responds* and an agent that *solves problems*.

---

## Homework Preview: Lab Assignment

In the next phase (Lab), you will:
1. Build a vacation planning agent that MUST decompose tasks before acting
2. Implement both ReAct and Plan-and-Execute strategies
3. Handle a "twist" — midway through, the user changes constraints (budget cut, date change)
4. Your agent must *re-plan* without crashing

**The Challenge:** We're giving you a vague task. You must force the agent to clarify constraints, decompose intelligently, and adapt to changes.

**End of Demo**

Next: Independent Lab where you implement these concepts yourself.
