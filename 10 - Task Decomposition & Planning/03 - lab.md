# Module 10: Task Decomposition & Planning
## Lab - Independent Application (The Lab Assignment)

**Duration:** 90-120 Minutes (Take-Home)  
**Goal:** Solidify your decomposition skills by independently building a planning agent that handles vague requests, decomposes tasks intelligently, and adapts when constraints change mid-execution.  
**Difficulty:** ⭐⭐⭐⭐ (Advanced - requires synthesis of multiple concepts)

---

## Overview: The Real-World Challenge

You are building an **Agentic Event Planning System**. Your client (the user) will give you vague, incomplete requests like:
- "Plan my wedding"
- "Organize a tech conference"
- "Set up a surprise birthday party for my mom"

Your agent must:
1. **Recognize ambiguity** — Identify what information is missing
2. **Decompose intelligently** — Break the event into logical subtasks
3. **Adapt dynamically** — Handle mid-execution changes (budget cuts, venue unavailable, date changes)
4. **Orchestrate tools** — Use multiple APIs (venue search, catering, invitations, etc.)

This is not a tutorial where you follow step-by-step instructions. This is a **real engineering challenge** where you must apply everything you've learned about task decomposition.

---

## Pre-Lab Setup

### 1. Environment Configuration

Create a new Python environment for this lab:

```bash
# Create isolated environment
uv venv event_planner_env
source event_planner_env/bin/activate  # On Windows: event_planner_env\Scripts\activate

# Install required packages
uv pip install smolagents openai python-dotenv pydantic
```

### 2. API Keys and Security

Create a `.env` file in your project directory:

```bash
# .env file
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here  # If using Claude
```

**Security Check:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Verify keys are loaded (but don't print them!)
assert os.getenv("OPENAI_API_KEY") is not None, "❌ OpenAI key not found"
assert os.getenv("OPENAI_API_KEY") != "your_key_here", "❌ Update your .env with real key"

print("✅ API keys loaded securely")
```

**Critical:** Add `.env` to your `.gitignore` file. Never commit API keys to version control.

---

## Part 1: Core Challenge — Build a Planning Agent

### Task 1: Implement a Decomposition-First Agent

**Objective:** Create an agent that **refuses to act** until it has generated a complete decomposition plan.

**Starter Code:**

```python
from smolagents import CodeAgent, InferenceClientModel, tool
import os

# Define your tools
@tool
def venue_search(location: str, capacity: int, date: str) -> dict:
    """
    Search for event venues.
    
    Args:
        location: City name
        capacity: Number of guests
        date: Event date (YYYY-MM-DD)
    
    Returns:
        Dictionary with venue options
    """
    # Simulated venue database
    venues = {
        "New York": [
            {"name": "Grand Ballroom", "capacity": 200, "price": 5000, "available": True},
            {"name": "Rooftop Terrace", "capacity": 100, "price": 3000, "available": True},
            {"name": "Garden Pavilion", "capacity": 150, "price": 4000, "available": False}
        ],
        "San Francisco": [
            {"name": "Bay View Hall", "capacity": 250, "price": 6000, "available": True},
            {"name": "Historic Mansion", "capacity": 80, "price": 3500, "available": True}
        ]
    }
    
    city_venues = venues.get(location, [])
    suitable = [v for v in city_venues if v["capacity"] >= capacity]
    return {"venues": suitable, "count": len(suitable)}


@tool
def catering_search(cuisine: str, guest_count: int, budget_per_person: int) -> dict:
    """
    Search for catering options.
    
    Args:
        cuisine: Type of cuisine (Italian, Mexican, Asian, etc.)
        guest_count: Number of guests
        budget_per_person: Budget per person in USD
    
    Returns:
        Dictionary with catering options
    """
    caterers = {
        "Italian": {"price_per_person": 45, "name": "Bella Cucina"},
        "Mexican": {"price_per_person": 35, "name": "Fiesta Catering"},
        "Asian": {"price_per_person": 40, "name": "Zen Kitchen"},
        "American": {"price_per_person": 38, "name": "Home Style Catering"}
    }
    
    option = caterers.get(cuisine, {"price_per_person": 50, "name": "Generic Catering"})
    total_cost = option["price_per_person"] * guest_count
    
    return {
        "caterer": option["name"],
        "price_per_person": option["price_per_person"],
        "total_cost": total_cost,
        "within_budget": option["price_per_person"] <= budget_per_person
    }


@tool
def send_invitations(guest_list: list, event_details: dict) -> dict:
    """
    Send invitations to guests.
    
    Args:
        guest_list: List of guest email addresses
        event_details: Dictionary with event info (date, venue, time)
    
    Returns:
        Confirmation of sent invitations
    """
    return {
        "status": "sent",
        "count": len(guest_list),
        "delivery_date": "2024-06-01"
    }


# TODO: Create your agent with decomposition-enforcing instructions
decomposition_instructions = """
CRITICAL: Before taking ANY actions, you MUST:

1. ANALYZE THE REQUEST
   - What type of event is this?
   - What information is provided?
   - What information is MISSING?

2. GENERATE A DECOMPOSITION PLAN
   Create a structured plan with:
   - Main goal
   - List of subtasks (numbered)
   - Dependencies between subtasks
   - Tools required for each subtask

3. IDENTIFY INFORMATION GAPS
   If critical information is missing, you MUST ask for it BEFORE proceeding.
   Critical information includes:
   - Budget
   - Date/Time
   - Location
   - Guest count
   - Event type specifics

4. ONLY AFTER PLANNING: Begin execution

Format your plan as:
```
DECOMPOSITION PLAN:
Main Goal: [state the goal]

Missing Information:
- [list missing items]

Subtasks:
1. [First subtask] → Tool: [tool_name] → Depends on: [none or previous task]
2. [Second subtask] → Tool: [tool_name] → Depends on: [task 1]
...

Execution Order: [1 → 2 → 3 or describe parallel tasks]
```

DO NOT skip this planning phase. Executing without a plan will result in failure.
"""

model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-72B-Instruct",
    api_key=os.getenv("OPENAI_API_KEY")  # Or your preferred model
)

planning_agent = CodeAgent(
    tools=[venue_search, catering_search, send_invitations],
    model=model,
    instructions=decomposition_instructions
)

# Test Case 1: Vague request (should trigger planning)
result = planning_agent.run("I want to plan a birthday party.")

print("=" * 80)
print("AGENT RESPONSE:")
print("=" * 80)
print(result)
```

**Expected Behavior:**

Your agent should output something like:

```
DECOMPOSITION PLAN:
Main Goal: Plan a birthday party

Missing Information:
- Guest count (how many people?)
- Budget (total available funds)
- Location/City (where will this take place?)
- Date (when is the party?)
- Birthday person's preferences (theme, food, activities?)
- Venue type preference (indoor/outdoor?)

Subtasks:
[Cannot proceed until missing information is provided]

REQUEST TO USER:
"To plan your birthday party, I need the following information:
1. How many guests will attend?
2. What is your total budget?
3. What city will the party be in?
4. What date are you planning?
5. Any preferences for food, theme, or venue type?"
```

**❌ FAIL Criteria:**
- Agent immediately calls `venue_search` without knowing the city
- Agent doesn't identify missing information
- Agent provides a generic answer without a structured plan

**✅ PASS Criteria:**
- Agent recognizes ambiguity
- Agent generates a clear decomposition plan
- Agent asks for missing information before proceeding

---

### Task 2: Implement the Full Planning-to-Execution Pipeline

Now give your agent complete information and verify it executes the plan correctly:

```python
# Test Case 2: Complete request (should decompose and execute)
complete_request = """
Plan a 30th birthday party with these details:
- Guest count: 50 people
- Budget: $3,000
- Location: New York
- Date: 2024-07-20
- Preferences: Italian food, elegant venue, indoor
- Need to send invitations to: [list of 50 emails]
"""

result_complete = planning_agent.run(complete_request)

# Verify the output
print("\n" + "=" * 80)
print("COMPLETE REQUEST RESULT:")
print("=" * 80)
print(result_complete)
```

**Expected Output:**

```
DECOMPOSITION PLAN:
Main Goal: Plan a 30th birthday party in New York for 50 guests with $3,000 budget

All required information provided ✅

Subtasks:
1. Search for venues → Tool: venue_search(location="New York", capacity=50, date="2024-07-20")
2. Select venue within budget → Depends on: Task 1
3. Search for Italian catering → Tool: catering_search(cuisine="Italian", guest_count=50, budget_per_person=?)
4. Calculate per-person catering budget → Depends on: Task 2 (remaining budget after venue)
5. Book catering if within budget → Depends on: Task 3, 4
6. Send invitations → Tool: send_invitations(guest_list=[...], event_details={...})

Execution Order: 1 → 2 → 3 → 4 → 5 → 6 (Sequential, with budget check at Step 4)

---

EXECUTING PLAN:

Step 1: Searching venues in New York for 50 guests on 2024-07-20...
Action: venue_search("New York", 50, "2024-07-20")
Observation: 
{
  "venues": [
    {"name": "Grand Ballroom", "capacity": 200, "price": 5000},
    {"name": "Rooftop Terrace", "capacity": 100, "price": 3000}
  ],
  "count": 2
}

Thought: Grand Ballroom exceeds budget ($5000 > $3000). Rooftop Terrace is exactly $3000.
         If we book Rooftop Terrace, we have $0 left for catering. This is a problem.
         Let me check if there are smaller/cheaper options...

[CRITICAL DECISION POINT]
Thought: None of the venues fit the budget while leaving room for catering.
         I need to replan. Options:
         A) Suggest increasing budget
         B) Suggest reducing guest count
         C) Look for a cheaper venue outside the database

Decision: I will inform the user of the budget constraint.

Result: "Budget constraint detected. Rooftop Terrace costs $3,000, leaving no funds for 
catering (~$45/person × 50 guests = $2,250 needed). 

Suggested solutions:
1. Increase budget to $5,250 minimum
2. Reduce guest count to 30 people (Rooftop Terrace $3000 + catering $1350 = $4350)
3. Consider alternative venues or potluck-style event"
```

**Key Observation:** The agent detected a failure mid-execution (budget insufficient) and *re-planned* instead of blindly proceeding.

---

## Part 2: The Twist — Adaptive Re-Planning

### The Challenge: Midway Through, Constraints Change

This is where your agent will be truly tested. You must implement logic to handle **mid-execution changes**.

**Scenario:**

```python
# User starts with initial request
initial_request = """
Plan a tech conference:
- Location: San Francisco
- Date: 2024-09-15
- Expected attendees: 200
- Budget: $50,000
- Needs: Venue, catering, AV equipment
"""

# Agent starts executing...

# TWIST: Midway through, budget is cut
budget_change = """
UPDATE: The budget has been reduced to $30,000. 
Please revise the plan without canceling any already-booked items.
"""

# Your agent must handle this gracefully
```

**Your Task:** Modify your agent to:
1. Track what has been "booked" (state management)
2. When a constraint changes, re-decompose only the affected subtasks
3. Provide revised recommendations

**Implementation Hint:**

```python
class EventPlanningState:
    """Track the state of the planning process."""
    def __init__(self):
        self.booked_venue = None
        self.booked_catering = None
        self.invitations_sent = False
        self.total_spent = 0
        self.budget_remaining = 0
    
    def book_venue(self, venue_cost):
        self.booked_venue = True
        self.total_spent += venue_cost
        self.budget_remaining = self.initial_budget - self.total_spent
    
    def handle_budget_change(self, new_budget):
        """Recalculate remaining budget and replan."""
        old_budget = self.initial_budget
        self.initial_budget = new_budget
        self.budget_remaining = new_budget - self.total_spent
        
        return {
            "old_budget": old_budget,
            "new_budget": new_budget,
            "already_spent": self.total_spent,
            "remaining": self.budget_remaining,
            "needs_replanning": self.budget_remaining < 0
        }

# Integrate this state tracking into your agent's workflow
```

**Expected Behavior:**

```
Initial Plan Execution:
✅ Venue booked: Bay View Hall ($6,000)
✅ Total spent: $6,000
✅ Remaining: $44,000

[Budget change received: New budget $30,000]

RE-PLANNING TRIGGERED:
- Already spent: $6,000
- New budget: $30,000
- New remaining: $24,000 (vs. original $44,000)

Affected subtasks:
- Catering budget must reduce from $88/person to $60/person
- May need to cut AV equipment upgrades
- Invitations not yet sent, can still adjust RSVP strategy

Revised Plan:
1. ✅ Venue: Already booked (no changes)
2. 🔄 Catering: Switch from premium to standard menu ($60/person instead of $88)
3. 🔄 AV: Rent basic setup instead of premium ($2,000 instead of $5,000)
4. ⏳ Invitations: Proceed with revised budget

New total: $6,000 + $12,000 + $2,000 = $20,000 ✅ Under new budget
```

---

## Part 3: Multi-Strategy Implementation

### Challenge: Implement THREE Different Approaches

You will build three versions of your planning agent, each using a different decomposition strategy:

#### Version 1: Chain-of-Thought (CoT) Agent
- Plans all steps upfront
- No adaptation mid-execution
- Fast but rigid

#### Version 2: ReAct Agent
- Interleaves thinking and action
- Adapts based on tool outputs
- Slower but flexible

#### Version 3: Hybrid Plan-and-Execute Agent
- Initial planning phase
- Execution phase with checkpoints
- Re-plans if checkpoint fails
- Balanced approach

**Your Task:** Implement all three and compare their performance on the following test cases:

**Test Case A: Simple Event (Wedding Reception)**
- All information provided upfront
- No surprises during execution
- **Prediction:** Which strategy performs best? Why?

**Test Case B: Complex Event with Unknowns (Tech Conference)**
- Some venue availability unknown until searched
- Catering options vary by venue
- **Prediction:** Which strategy performs best? Why?

**Test Case C: Event with Mid-Execution Changes (Corporate Retreat)**
- Budget cut happens midway
- Venue becomes unavailable 
- **Prediction:** Which strategy performs best? Why?

---

## Part 4: Analysis & Reflection

### Metacognition: Engineering Judgment

After implementing your three agent versions, answer these questions with data and reasoning:

#### Question 1: Cost Analysis

Calculate the token cost for each strategy on Test Case B:

| Strategy | Total Tokens | LLM Calls | Estimated Cost ($) |
|----------|--------------|-----------|-------------------|
| CoT      | ?            | ?         | ?                 |
| ReAct    | ?            | ?         | ?                 |
| Hybrid   | ?            | ?         | ?                 |

**Prompt:** 
```
For a production system handling 10,000 event planning requests per month, 
calculate the monthly cost for each strategy. Assume GPT-4 pricing: 
$0.03 per 1K input tokens, $0.06 per 1K output tokens.

Which strategy is most cost-effective? Under what conditions?
```

#### Question 2: Reliability Analysis

**Scenario:** In your testing, what was the failure rate for each strategy when faced with:
- Missing information
- Tool failures (API timeout)
- Mid-execution changes

Create a failure analysis table:

| Failure Type | CoT Success Rate | ReAct Success Rate | Hybrid Success Rate |
|--------------|------------------|--------------------|--------------------|
| Missing info | ?%               | ?%                 | ?%                 |
| Tool failure | ?%               | ?%                 | ?%                 |
| Constraint change | ?%          | ?%                 | ?%                 |

**Reflection:**
```
Which strategy is most robust? Why?
In a production system where reliability > cost, which would you choose?
```

#### Question 3: Ethical & Safety Considerations

**Scenario:** Your event planning agent is being deployed for a hospital charity gala.

**Constraints:**
- Must comply with HIPAA (no patient data in venue bookings)
- Must ensure wheelchair accessibility
- Must handle dietary restrictions (allergies)
- Must have backup plans (weather-dependent outdoor events)

**Question:** 
```
How would you modify your decomposition logic to enforce these safety constraints?
Provide specific code examples showing:
1. Where in the planning phase you'd check for accessibility
2. How you'd validate dietary restrictions before booking catering
3. What guardrails you'd implement to prevent privacy violations
```

#### Question 4: Scalability Analysis

**Scenario:** Your agent is a hit! You now need to handle:
- 1,000 concurrent planning requests
- Events in 50 different cities
- 10 different event types (weddings, conferences, parties, galas, etc.)

**Question:**
```
Redesign your architecture to scale. Consider:
1. Should you use a single general agent or specialized agents per event type?
2. How would you handle concurrent requests without tools interfering with each other?
3. Would you use a database to cache venue/catering options, or always query live?
4. How would you implement rate limiting on external APIs?

Provide a system architecture diagram and justify your design decisions.
```

---

## Assessment Rubric

### Pass Criteria (Must meet ALL):

#### Core Functionality (40 points)
- [ ] Agent refuses to act on vague requests until information is gathered (10 pts)
- [ ] Agent generates a clear, structured decomposition plan (10 pts)
- [ ] Agent correctly identifies dependencies between subtasks (10 pts)
- [ ] Agent successfully executes the plan when given complete information (10 pts)

#### Adaptation & Robustness (30 points)
- [ ] Agent handles budget changes mid-execution (10 pts)
- [ ] Agent re-plans when tool calls fail (10 pts)
- [ ] Agent tracks state (what's been booked vs. what's pending) (10 pts)

#### Code Quality & Security (20 points)
- [ ] API keys stored in `.env` file, not hardcoded (5 pts)
- [ ] Code runs on instructor's machine without modification (5 pts)
- [ ] Proper error handling (try/except blocks) (5 pts)
- [ ] Clear code comments explaining decomposition logic (5 pts)

#### Analysis & Reflection (10 points)
- [ ] All 4 reflection questions answered with data/reasoning (5 pts)
- [ ] Cost analysis includes actual calculations (3 pts)
- [ ] Ethical considerations addressed concretely (2 pts)

### Fail Criteria (Automatic failure if ANY of these occur):

- ❌ Hardcoded API keys (security violation)
- ❌ Code crashes due to missing dependencies (not reproducible)
- ❌ Agent is an exact copy of demo code without the required "twist" adaptation
- ❌ No decomposition implemented (agent just calls tools randomly)
- ❌ Reflection questions answered with generic statements instead of data from your implementation

---

## Submission Requirements

### What to Submit:

1. **Code Files:**
   - `planning_agent.py` — Your main agent implementation
   - `tools.py` — Your tool definitions
   - `requirements.txt` — Generated via `uv pip freeze > requirements.txt`
   - `.env.example` — Template showing what env variables are needed (without real keys)

2. **Analysis Document:**
   - `analysis.md` — Your answers to all 4 reflection questions with data/graphs

3. **Demo Video (Optional but Recommended):**
   - 5-minute screen recording showing:
     - Your agent handling a vague request
     - Your agent handling a complete request
     - Your agent adapting to a mid-execution change

### How to Submit:

```bash
# Create submission folder
mkdir module10_submission
cp planning_agent.py module10_submission/
cp tools.py module10_submission/
cp requirements.txt module10_submission/
cp analysis.md module10_submission/

# Create .env.example (remove real values)
echo "OPENAI_API_KEY=your_key_here" > module10_submission/.env.example

# Zip it
zip -r module10_submission.zip module10_submission/

# Submit module10_submission.zip to the course portal
```

---

## Bonus Challenges (Optional)

### Bonus 1: Implement Tree of Thoughts (ToT) ⭐
Generate 3 different event plans for the same request and use an LLM as a judge to pick the best one.

### Bonus 2: Multi-Agent Orchestration ⭐⭐
Reimplement your system using CrewAI or AutoGen with multiple specialized agents (VenueAgent, CateringAgent, BudgetAgent, etc.).

### Bonus 3: Persistent State with Database ⭐⭐⭐
Store event planning state in a SQLite database so the agent can resume if interrupted.

### Bonus 4: Real API Integration ⭐⭐⭐⭐
Replace simulated tools with real APIs:
- Google Places API for venue search
- Eventbrite API for ticketing
- SendGrid API for sending invitations

---

## Troubleshooting Guide

### Common Issues and Solutions

#### Issue 1: "Agent keeps acting without planning"
**Solution:** Your instructions aren't strong enough. Try:
```python
instructions = """
MANDATORY: You are FORBIDDEN from calling any tools until you have:
1. Listed ALL missing information
2. Generated a complete task decomposition
3. Received explicit user approval to proceed

If you call a tool before completing these steps, the system will halt and require a restart.
"""
```

#### Issue 2: "Agent plans but doesn't execute"
**Solution:** You may have made the planning phase too strict. Add:
```python
"After completing the decomposition plan and receiving all required information, 
you MUST proceed to execution. Do not wait for further instructions."
```

#### Issue 3: "Agent doesn't adapt when budget changes"
**Solution:** Implement explicit state tracking:
```python
class AgentState:
    def __init__(self):
        self.completed_tasks = []
        self.pending_tasks = []
        self.constraints = {}
    
    def update_constraint(self, key, new_value):
        old_value = self.constraints.get(key)
        self.constraints[key] = new_value
        
        # Mark pending tasks as needing review
        for task in self.pending_tasks:
            if key in task.dependencies:
                task.needs_replanning = True
```

#### Issue 4: "Too many LLM calls, exceeding budget"
**Solution:** Implement caching:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_venue_search(location, capacity, date):
    # Cache results for 1 hour to avoid repeated API calls
    return venue_search(location, capacity, date)
```

---

## Learning Outcomes Check

By completing this lab, you should be able to:

- [ ] Recognize when a task is too vague to execute directly
- [ ] Generate structured decomposition plans with dependencies
- [ ] Implement agents that plan before acting
- [ ] Handle mid-execution failures and constraint changes
- [ ] Compare different decomposition strategies (CoT, ReAct, Hybrid)
- [ ] Analyze trade-offs between cost, reliability, and flexibility
- [ ] Design scalable multi-agent architectures
- [ ] Implement security best practices (API key management)

---

## Final Reminder: This Lab Tests YOUR Decomposition Skills

This lab is intentionally challenging. You're not being asked to copy the demo — you're being asked to **apply the mental model of decomposition** to a new problem.

**Before you write any code, answer these questions on paper:**
1. What is the high-level goal?
2. What are the major subtasks?
3. What are the dependencies?
4. What information might be missing?
5. Where might failures occur?
6. How would I adapt if constraints change?

**If you can answer those questions, the code will follow naturally.**

Good luck! 🚀

---

**End of Lab Assignment**
