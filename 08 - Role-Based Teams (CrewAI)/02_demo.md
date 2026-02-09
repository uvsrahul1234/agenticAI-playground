# Module 08: Role-Based Teams (CrewAI) - Demo Analysis

**Module Title:** Role-Based Teams with CrewAI  
**Phase:** Guided Analysis (The "How" - Observed)  
**Duration:** 45-60 Minutes  
**Goal:** Interactive, instructor-led demonstration of building a Newsletter Crew with real-time debugging and result analysis.

---

## Demo Overview

**What We're Building:** A 3-agent Newsletter Crew that researches AI trends, writes a newsletter draft, and edits it for publication.

**Agents:**
1. **Researcher** - Finds and synthesizes current AI trends
2. **Writer** - Transforms research into engaging newsletter content
3. **Editor** - Refines language, checks facts, ensures quality

**Process Type:** Sequential (Researcher → Writer → Editor)

**Source Material:** Analysis Notebook (Live Coding Session)

---

## Part 1: Environment & Safety Check

### Procedure: Demonstrate the "Wrong" Way, Then the "Right" Way

#### Security Focus: API Key Management

**🔴 WRONG - Never Do This:**
```python
import os
from crewai import Agent, Task, Crew

# Hardcoded API key - NEVER!
os.environ["OPENAI_API_KEY"] = "sk-1234567890abcdef"
```

**Why This Is Dangerous:**
- Keys get committed to version control
- Visible in process logs
- Exposed in error messages
- Anyone with file access has your key

**✅ RIGHT - Always Do This:**
```python
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# Load from .env file
load_dotenv()

# Verify key is loaded (without exposing it)
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment!")
```

**✅ .env File Structure:**
```bash
# .env file (never commit this!)
OPENAI_API_KEY=sk-your-actual-key-here
GROQ_API_KEY=gsk-your-groq-key-here  # Alternative model provider
```

**✅ .gitignore Must Include:**
```bash
.env
*.env
.env.*
```

---

### Common Error Simulation: Missing Dependencies

**Intentional Error to Trigger:**
```python
from crewai import Agent
```

**Expected Error:**
```
ModuleNotFoundError: No module named 'crewai'
```

**Correction - Show Terminal:**
```bash
# Check current environment
which python
python --version

# Install CrewAI
pip install crewai crewai-tools --break-system-packages

# Verify installation
python -c "import crewai; print(crewai.__version__)"
```

**Instructor Note:** Walk through the traceback line by line. Teach students to read errors from **bottom to top**.

---

## Part 2: The "Code-Along" Core Task

### Predict-Observe-Explain Pattern

**Before running each code block, ask students:**
- "What do you expect to happen?"
- "What might go wrong?"
- "How would you debug if it fails?"

---

### Step A: Defining Our Agents

**Prediction Question:** "If we give the Researcher agent a goal of 'Find information' and the Writer agent the same goal, will they behave differently?"

**Code Block:**
```python
from crewai import Agent

# Agent 1: The Researcher
researcher = Agent(
    role="AI Trends Researcher",
    goal="Identify the most significant AI developments in the past week",
    backstory="""You are an experienced technology journalist with a PhD in 
    Computer Science. You have a keen eye for distinguishing genuine innovation 
    from hype. You prioritize peer-reviewed sources and reputable tech blogs.""",
    verbose=True,  # See the agent's thought process
    allow_delegation=False  # This agent works independently
)

# Agent 2: The Writer
writer = Agent(
    role="Newsletter Content Writer",
    goal="Transform technical research into engaging, accessible newsletter content",
    backstory="""You are a skilled science communicator who has written for 
    Wired, MIT Technology Review, and The Verge. You excel at making complex 
    topics understandable without dumbing them down. Your writing style is 
    conversational yet authoritative.""",
    verbose=True,
    allow_delegation=False
)

# Agent 3: The Editor
editor = Agent(
    role="Senior Newsletter Editor",
    goal="Ensure factual accuracy, grammatical perfection, and audience engagement",
    backstory="""You are a veteran editor with 15 years at major publications. 
    You have a reputation for catching subtle errors and improving narrative flow. 
    You're diplomatic but uncompromising on quality standards.""",
    verbose=True,
    allow_delegation=False
)
```

**Observation:**
- Each agent prints its initialization (if `verbose=True`)
- No errors means agents are successfully created
- Agents don't *do* anything yet—they're just blueprints

**Key Discussion Point:**  
*"Why does the backstory matter if the LLM is just generating text?"*

**Answer:** The backstory provides **system prompt context**. The LLM uses it to:
- Adjust tone (casual vs. formal)
- Prioritize certain information (peer-reviewed sources vs. Twitter threads)
- Make judgment calls (revolutionary vs. incremental changes)

**Experiment (Live):**  
Change the Researcher's backstory to: *"You are an excitable tech influencer who loves bold claims."*  
Predict how this would change the research output.

---

### Step B: Defining Tasks with Expected Outputs

**Prediction Question:** "If we don't specify an expected_output, will the agent still produce something?"

**Code Block:**
```python
from crewai import Task

# Task 1: Research
research_task = Task(
    description="""Research and identify the top 3 AI trends from the past 7 days. 
    For each trend:
    - Provide a clear headline
    - Explain the significance (2-3 sentences)
    - Include source citations
    
    Focus on developments in: LLMs, multimodal AI, AI safety, and enterprise adoption.""",
    
    expected_output="""A structured list with exactly 3 trends in this format:
    
    1. [Headline]
       Significance: [2-3 sentences]
       Source: [URL or publication name]
    
    2. [Headline]
       ...
    """,
    
    agent=researcher
)

# Task 2: Write Draft
writing_task = Task(
    description="""Using the research provided, write a newsletter draft with:
    - Engaging subject line
    - Brief introduction (2-3 sentences setting context)
    - One paragraph per trend (100-150 words each)
    - Conversational tone appropriate for tech-savvy professionals
    - A closing sentence that invites reader engagement""",
    
    expected_output="""A complete newsletter in markdown format with:
    - # Subject Line
    - Introduction paragraph
    - ## Trend 1: [Headline]
    - Content paragraph
    - (Repeat for trends 2 and 3)
    - Closing paragraph""",
    
    agent=writer,
    context=[research_task]  # Writer gets researcher's output
)

# Task 3: Edit and Finalize
editing_task = Task(
    description="""Review the newsletter draft and:
    - Fix any grammatical or spelling errors
    - Verify factual claims are supported by research
    - Improve sentence flow and readability
    - Ensure consistent tone throughout
    - Confirm all formatting is correct
    - Make the content 10% more concise without losing key information""",
    
    expected_output="""The final, publication-ready newsletter in markdown format.
    Include a brief editor's note at the end listing any major changes made.""",
    
    agent=editor,
    context=[research_task, writing_task]  # Editor sees both previous outputs
)
```

**Observation:**
- Tasks are created but not executed yet
- `context=[research_task]` creates dependency: Writer can't start until Researcher finishes
- `expected_output` guides the agent's output format

**Critical Question:**  
*"What happens if the Writer ignores the expected_output format?"*

**Answer:** CrewAI doesn't enforce schema (unlike Pydantic). It's a **guideline in the prompt**. The agent *usually* complies, but can deviate. This is why we have an Editor!

**Live Debugging Challenge:**  
Intentionally remove `expected_output` from research_task. Run it. Observe the unstructured mess. Revert and discuss the value of explicit output specifications.

---

### Step C: Assembling and Running the Crew

**Prediction Question:** "In what order will the tasks execute?"

**Code Block:**
```python
from crewai import Crew, Process

# Create the crew
newsletter_crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,  # Tasks run in order
    verbose=True  # Show detailed execution logs
)

# Kick off the crew!
print("🚀 Starting Newsletter Crew...\n")
result = newsletter_crew.kickoff()

print("\n" + "="*80)
print("📰 FINAL NEWSLETTER:")
print("="*80)
print(result)
```

**Before Running - Student Predictions:**
- How long will this take? (30 seconds? 5 minutes?)
- Will we see each agent's thoughts?
- What if the Researcher finds nothing relevant?

**Run the Code - Observe Together:**

1. **Researcher's Turn:**
   ```
   [Researcher] Starting task: Research and identify...
   [Researcher] Thought: I should search for recent AI news...
   [Researcher] Action: Searching...
   ```
   
   **Pause and Discuss:** "The Researcher is making decisions in real-time. What if we wanted it to use a specific web search tool instead of its default approach?"

2. **Writer's Turn:**
   ```
   [Writer] Starting task: Transform technical research...
   [Writer] Context received from previous task: [Shows research output]
   [Writer] Thought: I need to make this accessible...
   ```
   
   **Pause and Discuss:** "Notice the Writer receives the exact output from the Researcher. This is automatic context passing in sequential process."

3. **Editor's Turn:**
   ```
   [Editor] Starting task: Review the newsletter...
   [Editor] Thought: Checking for factual accuracy...
   [Editor] Action: Verifying claims...
   ```
   
   **Pause and Discuss:** "The Editor sees BOTH the research and the draft. Why is this important?"

---

## Part 3: Live Analysis of Results

### Result Analysis Framework

**Step 1: Read the Output Together**
Display the final newsletter on screen. Ask:
- Is it well-formatted?
- Does it address the original goal (top 3 AI trends)?
- Is the tone appropriate for the target audience?

**Step 2: Trace the Decision Chain**
Go back through the logs to identify:
- What sources did the Researcher choose?
- How did the Writer interpret the research?
- What changes did the Editor make?

**Step 3: Evaluate Against Expected Outputs**
Check each task's output against its `expected_output`:
- Did Researcher provide exactly 3 trends with citations?
- Did Writer follow the markdown structure?
- Did Editor include an editor's note?

---

### Discussion Points

**Point 1: Quality Variance**
*"If we run this again with the same prompt, will we get the exact same output?"*

**Answer:** No. LLMs are stochastic. Each run produces variations. This is both a feature (creativity) and a bug (unpredictability).

**Live Experiment:** Run `newsletter_crew.kickoff()` a second time. Compare the two newsletters side-by-side. Discuss:
- Which version is better?
- How would you decide?
- What if this variation is unacceptable in production?

---

**Point 2: Error Propagation**
*"What if the Researcher hallucinates a fake AI breakthrough?"*

**Scenario Simulation:**
```python
# Manually inject fake research
fake_research = """
1. GPT-5 Released
   Significance: OpenAI secretly released GPT-5 yesterday.
   Source: trust-me-bro.com
"""

# What happens when Writer and Editor process this?
```

**Discussion:** 
- Will the Editor catch the hallucination?
- Should we add a fact-checking tool?
- Where in the pipeline should validation occur?

---

**Point 3: Bottleneck Identification**
*"Which agent took the longest? Is that acceptable?"*

**Timing Analysis:**
```python
import time

start = time.time()
result = newsletter_crew.kickoff()
total_time = time.time() - start

print(f"Total execution time: {total_time:.2f} seconds")
```

**Typical Breakdown:**
- Researcher: 40% of time (web searches, API calls)
- Writer: 35% of time (generation is fast, thinking is slow)
- Editor: 25% of time (fewer changes needed)

**Optimization Question:** "If we need this newsletter generated every hour, and Researcher takes 2 minutes, how do we speed it up?"

**Answers:**
- Cache research results (update every 6 hours, not every run)
- Use faster models for less critical agents (Writer and Editor use GPT-3.5, Researcher uses GPT-4)
- Parallel execution where possible (though this specific workflow is inherently sequential)

---

### Variables to Change (Live Experiments)

**Experiment 1: Change the Researcher's Focus**
```python
# Original: "Focus on LLMs, multimodal AI, AI safety, enterprise adoption"
# New: "Focus on AI in healthcare and medical imaging"

# Predict: How will downstream outputs change?
```

**Experiment 2: Remove the Editor**
```python
newsletter_crew = Crew(
    agents=[researcher, writer],  # No editor!
    tasks=[research_task, writing_task],
    process=Process.sequential
)

# Predict: Will quality suffer noticeably?
```

**Experiment 3: Swap Agent Roles**
```python
# Make the Writer do research
research_task.agent = writer
writing_task.agent = researcher

# Predict: What breaks? What still works?
```

---

## Part 4: Common Pitfalls & Debugging

### Pitfall 1: Agent Doesn't Follow Instructions

**Symptom:** Researcher returns 5 trends instead of 3.

**Debugging Steps:**
1. Check the task description—is it clear and unambiguous?
2. Look at the agent's verbose output—did it misunderstand?
3. Strengthen the expected_output with explicit constraints
4. Consider adding a validation tool

**Fix Example:**
```python
expected_output="""EXACTLY 3 trends. No more, no less. 
If you provide 4 or more, your output will be rejected."""
```

---

### Pitfall 2: Context Not Passing Between Tasks

**Symptom:** Writer produces generic content, ignoring research.

**Debugging Steps:**
1. Verify `context=[research_task]` is set
2. Check if research_task actually completed successfully
3. Print the context explicitly:
   ```python
   print("Context being passed to writer:")
   print(research_task.output)
   ```

**Common Cause:** Research task failed silently, passing empty context.

---

### Pitfall 3: Execution Takes Too Long

**Symptom:** Crew runs for 5+ minutes.

**Debugging Steps:**
1. Check which agent is slow (verbose logs show this)
2. Verify API rate limits aren't being hit
3. Simplify task descriptions (fewer words = less reasoning)
4. Switch to a faster model for non-critical agents

**Emergency Fix:**
```python
from crewai import LLM

fast_llm = LLM(model="gpt-3.5-turbo")  # Faster, cheaper
writer.llm = fast_llm  # Override default
```

---

## Part 5: Extending the System

### Adding Tools to Agents

**Why Tools Matter:**  
By default, agents use the LLM's built-in knowledge (which has a knowledge cutoff). Tools give them real-time capabilities.

**Example: Adding Web Search to Researcher**
```python
from crewai_tools import SerperDevTool

# Requires SERPER_API_KEY in .env
search_tool = SerperDevTool()

researcher = Agent(
    role="AI Trends Researcher",
    goal="Identify the most significant AI developments in the past week",
    backstory="...",
    tools=[search_tool],  # Now has web search!
    verbose=True
)
```

**Live Demonstration:**  
Run the crew with and without the search tool. Compare:
- Are the trends more current with the tool?
- Are citations more accurate?
- Did execution time increase?

---

### Adding a Fourth Agent: Fact-Checker

**Design Question:** "Should fact-checking happen before or after editing?"

**Option A: Sequential (Research → Write → Edit → Fact-Check)**
- Pro: Catches errors in final version
- Con: Too late if errors are deep in narrative

**Option B: Parallel (Research → [Write + Fact-Check] → Edit)**
- Pro: Writer and fact-checker work simultaneously
- Con: CrewAI's sequential process doesn't natively support this

**Instructor Decision:** Show Option A for simplicity.

```python
fact_checker = Agent(
    role="AI Fact Verification Specialist",
    goal="Verify all technical claims and statistics are accurate",
    backstory="Former academic researcher with expertise in AI systems...",
    tools=[search_tool],
    verbose=True
)

fact_check_task = Task(
    description="Verify every factual claim. Flag anything suspicious.",
    expected_output="List of verified facts and any concerns",
    agent=fact_checker,
    context=[research_task, writing_task, editing_task]
)

# Updated crew
newsletter_crew = Crew(
    agents=[researcher, writer, editor, fact_checker],
    tasks=[research_task, writing_task, editing_task, fact_check_task],
    process=Process.sequential
)
```

---

## Part 6: Reflection Questions

**Ask Students:**

1. **Specialization Trade-Off:**  
   "We used 3 specialized agents. Could one powerful agent do this job just as well? Why or why not?"

2. **Context Passing:**  
   "The Editor receives context from both Researcher and Writer. Is that necessary, or would just the Writer's output be enough?"

3. **Error Recovery:**  
   "If the Researcher fails (API error, timeout), should the Writer proceed with its existing knowledge, or should the entire crew fail fast?"

4. **Real-World Deployment:**  
   "How would you turn this demo into a production system that generates newsletters every Monday at 9 AM?"

---

## Summary: Key Observations

1. **Sequential Process = Natural Quality Gates**  
   Each agent reviews and refines the previous agent's work.

2. **Context Is King**  
   Explicit context passing is what makes the pipeline coherent.

3. **Verbose Mode = Debugger's Best Friend**  
   Seeing the agent's reasoning helps diagnose failures.

4. **Expected Output Guides, But Doesn't Guarantee**  
   Agents usually comply, but validation is still necessary.

5. **Tools Extend Capabilities**  
   Without tools, agents are limited to training data knowledge.

---

## Homework Preview

In the Lab, you will:
- Build your own 3-agent crew (different domain than newsletters)
- Handle a scenario where one agent fails
- Add at least one tool to one agent
- Measure and optimize execution time

**The Twist:** Your crew must handle a multi-format output (text + structured data), not just prose.

---

**Next Phase:** Independent Lab where you apply these concepts to a different problem domain.
