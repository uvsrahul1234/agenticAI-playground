# Module 08: Role-Based Teams (CrewAI) - Independent Lab

**Module Title:** Role-Based Teams with CrewAI  
**Phase:** Independent Application (The "How" - Applied)  
**Duration:** 90-120 Minutes (Take-Home / Lab Time)  
**Goal:** Solidify skills through independent construction of a multi-agent system in a different problem domain.

---

## Lab Overview

**Important:** This lab builds upon concepts from the Demo, but challenges you to implement them independently in your own environment with a different use case.

**What Makes This Different from the Demo:**
- **Different Domain:** Market Research instead of Newsletter Generation
- **Added Complexity:** Structured data output (JSON) in addition to prose
- **Error Handling:** You must handle agent failures gracefully
- **Performance Requirement:** Optimize for execution time

---

## Pre-Lab Setup

### 1. Independent Environment Configuration

**Required Installations:**
```bash
# Create a new directory for this lab
mkdir module08_lab
cd module08_lab

# Create virtual environment (using uv as taught in Module 1)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install crewai crewai-tools python-dotenv langchain-openai

# Verify installation
python -c "import crewai; print(f'CrewAI version: {crewai.__version__}')"
```

---

### 2. API Key Configuration

**Create `.env` File:**
```bash
# .env
OPENAI_API_KEY=your_openai_key_here
SERPER_API_KEY=your_serper_key_here  # For web search (optional but recommended)
```

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Serper (free tier): https://serper.dev/

**Security Checklist:**
- [ ] Created .gitignore with `.env`
- [ ] Never hardcoded keys in Python files
- [ ] Verified keys load with `os.getenv("OPENAI_API_KEY")`

---

### 3. Project Structure

```
module08_lab/
│
├── .env                    # API keys (DO NOT COMMIT)
├── .gitignore             # Must include .env
├── requirements.txt       # Dependencies list
├── market_research_crew.py # Your main implementation
├── test_crew.py           # Testing script
└── outputs/               # Generated reports (optional)
```

---

## Lab Challenge: Market Research Crew

### Business Requirement

You are building a **Competitive Intelligence Crew** for a startup founder who needs to:

1. **Research** the top 3 competitors in a specific market
2. **Analyze** each competitor's strengths, weaknesses, pricing, and market positioning
3. **Synthesize** findings into a strategic brief with recommendations

**Output Requirements:**
- A markdown report (prose)
- A JSON file with structured competitor data
- Execution time under 3 minutes

---

## Part 1: The "Twist" (Differentiation from Demo)

### Key Differences

| Demo (Newsletter Crew) | Lab (Market Research Crew) |
|------------------------|----------------------------|
| 3 agents: Researcher, Writer, Editor | 3 agents: Market Analyst, Strategy Consultant, Data Synthesizer |
| Output: Single markdown newsletter | Output: Markdown report + JSON data |
| Focus: Recent trends (1 week) | Focus: Current competitive landscape |
| No tools required | Must use web search tool |
| Error handling optional | Error handling mandatory |

---

## Part 2: Agent Design Requirements

You must create **exactly 3 agents** with the following roles:

### Agent 1: Market Intelligence Analyst

**Role:** Competitive Intelligence Researcher  

**Goal:** Identify and research the top 3 competitors in a specified market segment.

**Required Capabilities:**
- Web search to find current competitors
- Extract key information: company size, founding year, funding, product offerings
- Identify market positioning and unique value propositions

**Backstory (You Design):**  
Create a compelling backstory that makes this agent act like an experienced market researcher. Consider:
- What's their professional background?
- What sources do they trust?
- What makes them good at this job?

**Required Tool:**  
Must include `SerperDevTool()` for web search.

**Constraints:**
- Must focus on **currently operating** companies (not defunct)
- Must provide **verifiable data** (no hallucinations)
- Must limit research to exactly 3 competitors

---

### Agent 2: Strategic Business Consultant

**Role:** Competitive Strategy Analyst

**Goal:** Analyze each competitor's strategic positioning and identify opportunities/threats.

**Required Capabilities:**
- SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
- Pricing strategy assessment
- Market differentiation identification

**Backstory (You Design):**  
What makes this agent qualified to assess business strategy?

**Input Context:**  
Must receive output from Agent 1 (Market Intelligence Analyst)

**Constraints:**
- Must provide **actionable insights**, not just descriptions
- Must identify at least 2 opportunities for the client

---

### Agent 3: Data Synthesis Specialist

**Role:** Report Generation and Data Structuring Expert

**Goal:** Convert analysis into both human-readable and machine-readable formats.

**Required Capabilities:**
- Generate professional markdown report
- Extract structured data into JSON format
- Ensure consistency between prose and structured data

**Backstory (You Design):**  
Why is this agent skilled at both narrative writing and data structuring?

**Input Context:**  
Must receive outputs from both Agent 1 and Agent 2

**Special Requirement:**  
This agent must output TWO things:
1. A markdown report (prose)
2. A JSON object with competitor data

---

## Part 3: Task Definitions

### Task 1: Market Intelligence Gathering

**Description:**
```
Research the top 3 competitors in the [USER-SPECIFIED MARKET, e.g., "AI-powered 
customer service chatbot"] space. For each competitor, gather:

1. Company name and website
2. Year founded
3. Estimated company size (employees)
4. Total funding raised (if available)
5. Core product/service offering
6. Key differentiators from alternatives
7. Target customer segment

Use only information from the past 6 months where possible.
```

**Expected Output:**
```
A detailed report with exactly 3 competitors, structured as:

## Competitor 1: [Company Name]
- Website: [URL]
- Founded: [Year]
- Company Size: [Estimate]
- Funding: [Amount if known, or "N/A"]
- Core Offering: [1-2 sentence description]
- Key Differentiator: [What makes them unique]
- Target Customers: [Who they serve]

(Repeat for Competitors 2 and 3)
```

**Agent Assignment:** Market Intelligence Analyst

---

### Task 2: Strategic Analysis

**Description:**
```
For each of the 3 competitors identified, perform a strategic analysis:

1. Strengths: What do they do exceptionally well?
2. Weaknesses: Where are they vulnerable?
3. Pricing Strategy: How do they price their offering? (freemium, enterprise, usage-based, etc.)
4. Market Position: Are they the leader, challenger, or niche player?

Then, identify:
- 2 opportunities our client could exploit (gaps in the market)
- 2 threats from these competitors our client should watch

Base your analysis on the research provided.
```

**Expected Output:**
```
# Strategic Analysis

## Competitor 1: [Name]
**Strengths:**
- [Bullet point]
- [Bullet point]

**Weaknesses:**
- [Bullet point]
- [Bullet point]

**Pricing Strategy:** [Description]

**Market Position:** [Leader/Challenger/Niche] because [reasoning]

(Repeat for Competitors 2 and 3)

---

## Opportunities for Our Client
1. [Opportunity with explanation]
2. [Opportunity with explanation]

## Competitive Threats
1. [Threat with explanation]
2. [Threat with explanation]
```

**Agent Assignment:** Strategic Business Consultant

**Context:** Receives output from Task 1

---

### Task 3: Report Synthesis

**Description:**
```
Generate two deliverables from the research and analysis:

DELIVERABLE 1 - Executive Brief (Markdown):
Write a professional 400-500 word executive brief that:
- Summarizes the competitive landscape
- Highlights the most critical findings
- Provides 2-3 strategic recommendations for our client
- Uses a confident, consultative tone

DELIVERABLE 2 - Structured Data (JSON):
Extract key data points into a JSON object with this structure:
{
  "market_segment": "[The market analyzed]",
  "analysis_date": "[Today's date]",
  "competitors": [
    {
      "name": "Company A",
      "website": "https://example.com",
      "founded_year": 2020,
      "key_strength": "One sentence",
      "key_weakness": "One sentence",
      "market_position": "Leader/Challenger/Niche"
    },
    (... for all 3 competitors)
  ],
  "top_opportunities": ["Opportunity 1", "Opportunity 2"],
  "top_threats": ["Threat 1", "Threat 2"]
}

Ensure the JSON is valid and can be parsed by Python's json.loads().
```

**Expected Output:**
```
# Executive Brief
[Markdown report here]

---

# Structured Data
```json
{JSON object here}
```
```

**Agent Assignment:** Data Synthesis Specialist

**Context:** Receives outputs from Task 1 and Task 2

---

## Part 4: Implementation Checklist

### [ ] Step 1: Load Environment
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Verify keys are loaded
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not found!"
```

---

### [ ] Step 2: Import CrewAI Components
```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
```

---

### [ ] Step 3: Define Your Three Agents
```python
# Agent 1: Market Intelligence Analyst
search_tool = SerperDevTool()

market_analyst = Agent(
    role="...",
    goal="...",
    backstory="...",
    tools=[search_tool],
    verbose=True,
    allow_delegation=False
)

# Agent 2: Strategic Business Consultant
strategy_consultant = Agent(
    role="...",
    goal="...",
    backstory="...",
    verbose=True,
    allow_delegation=False
)

# Agent 3: Data Synthesis Specialist
data_synthesizer = Agent(
    role="...",
    goal="...",
    backstory="...",
    verbose=True,
    allow_delegation=False
)
```

---

### [ ] Step 4: Define Your Three Tasks
```python
# Task 1
intelligence_task = Task(
    description="...",
    expected_output="...",
    agent=market_analyst
)

# Task 2
analysis_task = Task(
    description="...",
    expected_output="...",
    agent=strategy_consultant,
    context=[intelligence_task]
)

# Task 3
synthesis_task = Task(
    description="...",
    expected_output="...",
    agent=data_synthesizer,
    context=[intelligence_task, analysis_task]
)
```

---

### [ ] Step 5: Assemble the Crew
```python
market_research_crew = Crew(
    agents=[market_analyst, strategy_consultant, data_synthesizer],
    tasks=[intelligence_task, analysis_task, synthesis_task],
    process=Process.sequential,
    verbose=True
)
```

---

### [ ] Step 6: Execute with Input
```python
# Prompt user for market segment
market_segment = input("Enter the market to research (e.g., 'AI-powered CRM software'): ")

# Inject user input into task description
intelligence_task.description = intelligence_task.description.replace(
    "[USER-SPECIFIED MARKET]",
    market_segment
)

# Run the crew
import time
start_time = time.time()

result = market_research_crew.kickoff()

execution_time = time.time() - start_time

print("\n" + "="*80)
print("FINAL REPORT")
print("="*80)
print(result)
print(f"\nExecution Time: {execution_time:.2f} seconds")
```

---

## Part 5: Error Handling (Required)

### Scenario: Agent Fails to Complete Task

**Implementation:**
```python
try:
    result = market_research_crew.kickoff()
except Exception as e:
    print(f"Crew execution failed: {e}")
    print("Attempting fallback strategy...")
    
    # Fallback: Use smaller model or retry
    # Your implementation here
```

**Requirements:**
1. Catch exceptions during execution
2. Log the error details
3. Implement at least one fallback strategy:
   - Retry with simplified task description
   - Switch to a different model
   - Use cached/default data

---

## Part 6: Performance Optimization

### Requirement: Execution Time < 3 Minutes

**Strategies to Try:**

1. **Model Selection:**
```python
from crewai import LLM

# Fast model for non-critical agents
fast_llm = LLM(model="gpt-3.5-turbo")
data_synthesizer.llm = fast_llm
```

2. **Task Simplification:**
```python
# Original: "Analyze pricing, positioning, SWOT, and market share"
# Optimized: "Analyze pricing and key strengths/weaknesses only"
```

3. **Caching Research (Advanced):**
```python
import json
from pathlib import Path

cache_file = Path("competitor_cache.json")

if cache_file.exists():
    # Load from cache if recent
    with open(cache_file) as f:
        cached_data = json.load(f)
    # Use cached data instead of re-researching
```

**Measurement:**
```python
import time

start = time.time()
result = market_research_crew.kickoff()
elapsed = time.time() - start

if elapsed > 180:  # 3 minutes
    print(f"⚠️ Warning: Execution took {elapsed:.2f}s (target: <180s)")
else:
    print(f"✅ Performance target met: {elapsed:.2f}s")
```

---

## Part 7: Output Validation

### Validate Markdown Report

**Requirements:**
- [ ] Report is between 400-500 words
- [ ] All 3 competitors are mentioned
- [ ] At least 2 strategic recommendations are provided

**Validation Code:**
```python
def validate_report(markdown_text):
    word_count = len(markdown_text.split())
    print(f"Word count: {word_count}")
    
    # Check for competitor mentions
    competitors_found = markdown_text.count("Competitor")
    print(f"Competitors mentioned: {competitors_found}")
    
    # Check for recommendations
    has_recommendations = "recommend" in markdown_text.lower()
    print(f"Contains recommendations: {has_recommendations}")
    
    return 400 <= word_count <= 500 and competitors_found >= 3 and has_recommendations

is_valid = validate_report(result)
print(f"Report validation: {'PASS' if is_valid else 'FAIL'}")
```

---

### Validate JSON Output

**Requirements:**
- [ ] Valid JSON syntax
- [ ] Contains exactly 3 competitors
- [ ] All required fields present

**Validation Code:**
```python
import json
import re

def extract_and_validate_json(result_text):
    # Extract JSON block
    json_match = re.search(r'```json\n(.*?)\n```', result_text, re.DOTALL)
    if not json_match:
        print("❌ No JSON block found in output")
        return False
    
    json_str = json_match.group(1)
    
    try:
        data = json.loads(json_str)
        print("✅ Valid JSON syntax")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False
    
    # Validate structure
    required_keys = ["market_segment", "competitors", "top_opportunities", "top_threats"]
    for key in required_keys:
        if key not in data:
            print(f"❌ Missing required key: {key}")
            return False
    
    if len(data["competitors"]) != 3:
        print(f"❌ Expected 3 competitors, found {len(data['competitors'])}")
        return False
    
    print("✅ JSON structure is valid")
    return True

extract_and_validate_json(result)
```

---

## Part 8: Analysis & Reflection

### Answer These Questions in Your Submission

1. **Design Decisions:**
   - Why did you choose the backstories you did for each agent?
   - Did you add any additional tools beyond SerperDevTool? Why or why not?

2. **Performance Analysis:**
   - What was your crew's execution time?
   - Which agent took the longest? Why?
   - What optimization strategies did you implement?

3. **Quality Assessment:**
   - Did your crew produce factually accurate research?
   - Were any claims hallucinated?
   - How did you verify accuracy?

4. **Error Scenarios:**
   - Did your crew fail at any point during testing?
   - What errors did you encounter?
   - How did your error handling respond?

5. **Comparison to Demo:**
   - Was building a Market Research Crew harder or easier than the Newsletter Crew from the demo?
   - What was the most challenging part of this lab?
   - What would you do differently if you built this again?

---

## Part 9: Extension Challenges (Optional)

### Challenge 1: Add a Fourth Agent - "Risk Assessor"

**Goal:** Identify legal, regulatory, or ethical risks in the competitive landscape.

**Requirements:**
- Create a new agent and task
- Insert it between the Strategy Consultant and Data Synthesizer
- Update context dependencies

**Expected Output:** A risk assessment section in the final report.

---

### Challenge 2: Support Multiple Output Formats

**Goal:** Generate not just markdown + JSON, but also:
- HTML report
- CSV of competitor data
- PowerPoint slides (using python-pptx)

**Hint:** Create specialized tasks for each format, or have one agent generate multiple formats.

---

### Challenge 3: Parallel Execution (Advanced)

**Goal:** Research all 3 competitors in parallel instead of sequentially.

**Approach:**
- Create 3 "Sub-Researcher" agents
- Each researches 1 competitor
- A "Coordinator" agent aggregates their findings

**Note:** This requires understanding CrewAI's hierarchical process, not covered in the demo.

---

### Challenge 4: Real-World Deployment

**Goal:** Turn this into a serverless function that runs on a schedule.

**Requirements:**
- Package as AWS Lambda / Google Cloud Function
- Trigger weekly via EventBridge / Cloud Scheduler
- Email results to stakeholders
- Store historical reports in S3 / Cloud Storage

---

## Submission Requirements

### Files to Submit:

1. **market_research_crew.py** - Your full implementation
2. **requirements.txt** - Your dependencies
3. **sample_output.md** - One complete execution output
4. **reflection.md** - Your answers to Part 8 questions
5. **performance_log.txt** - Execution time measurements

### Grading Criteria:

| Category | Points | Requirements |
|----------|--------|--------------|
| **Implementation** | 40 | All 3 agents and tasks correctly defined |
| **Functionality** | 20 | Crew executes successfully and produces expected outputs |
| **Error Handling** | 15 | Try-except blocks with meaningful fallbacks |
| **Performance** | 10 | Execution time < 3 minutes |
| **Output Quality** | 10 | Valid markdown + JSON, meets word count |
| **Reflection** | 5 | Thoughtful answers to analysis questions |

**Total:** 100 points

---

## Helpful Resources

### CrewAI Documentation
- Official Docs: https://docs.crewai.com/
- GitHub Examples: https://github.com/joaomdmoura/crewAI-examples

### Debugging Tips
```python
# Enable maximum verbosity
import logging
logging.basicConfig(level=logging.DEBUG)

# Inspect agent thoughts
for step in market_research_crew.tasks[0].output:
    print(step)

# Test individual agents
test_result = market_analyst.execute_task(intelligence_task)
print(test_result)
```

### Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: crewai` | Not installed | `pip install crewai` |
| `OPENAI_API_KEY not found` | .env not loaded | Check `load_dotenv()` called |
| Agent runs forever | Infinite reasoning loop | Add `max_iter=10` to agent |
| Invalid JSON output | Agent ignored format | Strengthen `expected_output` |
| API rate limit | Too many requests | Add sleep between tasks |

---

## Final Notes

**Time Management:**
- Reading & Setup: 20 minutes
- Agent Implementation: 30 minutes
- Task Definitions: 20 minutes
- Testing & Debugging: 30 minutes
- Optimization & Validation: 20 minutes
- **Total:** ~2 hours

**Don't Get Stuck:**
- If you're blocked for >15 minutes, ask for help or move to a simpler version
- You can use GPT-3.5-turbo instead of GPT-4 to reduce costs during testing
- Start with the simplest possible implementation, then add complexity

**Success Criteria:**
You've completed the lab successfully when:
- [ ] Your crew runs without errors
- [ ] Both markdown and JSON outputs are generated
- [ ] Execution time is acceptable
- [ ] Error handling is implemented
- [ ] You can explain your design decisions

---

**Good luck! Remember: The goal is not perfection, but understanding. Focus on learning from failures as much as successes.**
