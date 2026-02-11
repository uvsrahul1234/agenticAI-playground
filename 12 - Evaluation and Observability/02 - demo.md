# Module 12: Evaluation & Observability
## Demo - Guided Analysis (The Live Demo)

**Module Title:** Evaluation & Observability - Live Demonstration  
**Duration:** 45-60 Minutes  
**Goal:** Observe evaluation and monitoring systems in action through instructor-led demonstration with real-time debugging and analysis.

**Source Material:** Analysis Notebook (to be distributed in class)

---

## Pre-Demo Setup Checklist

### Student Preparation
Before class, students should review:
- [ ] The glossary definitions for trace, span, and observability
- [ ] The four dimensions of evaluation
- [ ] The concept of LLM-as-judge

### Instructor Environment
- [ ] Langfuse account configured (https://cloud.langfuse.com)
- [ ] Demo agent workflow ready (Newsletter Crew from Week 8 recommended)
- [ ] Intentional bugs seeded in the demo agent
- [ ] Environment variables properly configured
- [ ] Demo notebook tested and ready

---

## Phase 1: Environment & Safety Check (10 minutes)

### The Wrong Way (Intentional Demonstration)

**Instructor:** "Before we do this right, let me show you what NOT to do."

#### Step 1: Hardcoded API Keys (WRONG)
```python
# ❌ NEVER DO THIS
import anthropic

client = anthropic.Anthropic(
    api_key="sk-ant-1234567890"  # SECURITY VIOLATION!
)
```

**Ask Students:** "What's wrong with this approach?"

**Expected Answers:**
- Keys exposed in code
- Keys in version control history
- Keys visible in logs
- No rotation capability

---

#### Step 2: No Observability (WRONG)
```python
# ❌ RUNNING BLIND
result = agent.run("Write a newsletter about AI")
print(result)
```

**Ask Students:** "If this fails, how would we debug it?"

**Expected Answers:**
- No trace of intermediate steps
- Can't see which tool failed
- No cost information
- Can't reproduce the issue

---

### The Right Way (Secure + Observable)

#### Step 1: Environment Variables
```python
# ✅ CORRECT APPROACH
import os
from dotenv import load_dotenv

load_dotenv(override=True)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
```

**Demonstrate:** Show the `.env` file structure (without revealing actual keys)

```env
# .env file structure
ANTHROPIC_API_KEY=sk-ant-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

---

#### Step 2: Initialize Observability
```python
# ✅ SET UP TRACING
from langfuse import get_client

langfuse = get_client()

# Verify connection
if langfuse.auth_check():
    print("✓ Langfuse client authenticated")
else:
    print("✗ Authentication failed")
```

**Instructor:** "Now let's intentionally break this to see what happens."

**Live Error Simulation:**
```python
# Temporarily use wrong secret key
os.environ["LANGFUSE_SECRET_KEY"] = "wrong-key-123"
langfuse = get_client()
```

**Ask Students:** "What error message should we expect?"

**Demonstrate:** Show the actual error, read the traceback together, and correct it.

---

## Phase 2: The Core Demonstration - Newsletter Agent (30 minutes)

### Context Setting

**Scenario:** We built a Newsletter Crew in Week 8 with three agents:
1. **Researcher Agent** - Searches for AI news
2. **Writer Agent** - Drafts the newsletter
3. **Editor Agent** - Reviews and finalizes

**Today's Goal:** Evaluate this crew's performance and identify problems.

---

### Step 2A: Run the Agent (Baseline)

```python
from newsletter_crew import NewsletterCrew

# Initialize the crew
crew = NewsletterCrew(
    topic="Latest developments in AI agents",
    enable_tracing=True
)

# Run the workflow
result = crew.run()
```

**Predict-Observe-Explain Moment:**

**Instructor:** "Before I hit run, predict what you think will happen. What steps will execute?"

**Expected Student Responses:**
- Web search for AI agent news
- Extract article content
- Draft newsletter text
- Review and edit

**Instructor:** "Let's see what actually happens..."

**[Run the cell]**

**Observe together:**
- Watch the console output
- Note any unexpected behavior
- Time the execution

---

### Step 2B: Examine the Trace (Observability in Action)

**Instructor:** "Now let's look under the hood. Open Langfuse..."

**Navigate to:** `https://cloud.langfuse.com/projects`

#### Demonstration Points:

1. **Trace Overview**
   - Show the complete execution timeline
   - Point out each agent's span
   - Identify tool calls

2. **Click into the Researcher Agent Span**
   - Show the search query used
   - Examine the returned results
   - Check token usage for this step

3. **Click into the Writer Agent Span**
   - Show the draft newsletter generated
   - Look at the prompt sent to the LLM
   - Note the token count

**Critical Question for Class:**
"Looking at these traces, does anything surprise you? Do you see any inefficiencies?"

---

### Step 2C: Cost Analysis (Live Calculation)

**Instructor:** "Let's calculate the actual cost of this workflow."

```python
# Extract cost information from trace
trace_id = result.trace_id
trace = langfuse.get_trace(trace_id)

total_tokens = 0
total_cost = 0.0

for span in trace.spans:
    if span.usage:
        input_tokens = span.usage.input
        output_tokens = span.usage.output
        
        # Claude Sonnet 4.5 pricing (example)
        cost = (input_tokens * 0.000003) + (output_tokens * 0.000015)
        
        total_tokens += (input_tokens + output_tokens)
        total_cost += cost
        
        print(f"{span.name}:")
        print(f"  Tokens: {input_tokens + output_tokens}")
        print(f"  Cost: ${cost:.4f}")

print(f"\nTotal Cost: ${total_cost:.4f}")
print(f"Total Tokens: {total_tokens}")
```

**Ask Students:**
"If we run this 1,000 times per day, what's our monthly cost?"

**Calculate together:**
- Daily: $X × 1,000
- Monthly: Daily × 30
- Discuss: Is this sustainable?

---

### Step 2D: Identify a Bug (Error Analysis)

**Instructor:** "I seeded a bug in this agent. Let's find it together."

**Intentional Bug:** The agent mentions competitors in the newsletter.

**Example Output:**
```
Latest AI Developments

This week saw major advances in agent frameworks. 
Unlike OpenAI's Assistants API, our open-source solution...
```

**Ask Class:** "What's the problem here?"

**Discussion Points:**
- Business policy: Don't mention competitors
- How did this happen?
- Where in the pipeline did it occur?

---

### Step 2E: Build an Objective Eval (Live Coding)

**Instructor:** "Let's write code to catch this automatically."

```python
def eval_competitor_mentions(output: str) -> dict:
    """
    Objective eval: Check if output mentions competitors.
    
    Returns:
        dict with 'passed' (bool) and 'details' (str)
    """
    competitors = [
        "OpenAI",
        "Google Gemini",
        "Microsoft Copilot",
        "Anthropic Claude"  # Yes, even ourselves in some contexts
    ]
    
    output_lower = output.lower()
    mentioned = []
    
    for competitor in competitors:
        if competitor.lower() in output_lower:
            mentioned.append(competitor)
    
    passed = len(mentioned) == 0
    
    return {
        "passed": passed,
        "details": f"Mentioned competitors: {mentioned}" if mentioned else "No competitors mentioned",
        "count": len(mentioned)
    }

# Test it
eval_result = eval_competitor_mentions(result.output)
print(f"Passed: {eval_result['passed']}")
print(f"Details: {eval_result['details']}")
```

**Instructor:** "This is an objective eval - either it mentions competitors or it doesn't. No LLM needed."

---

### Step 2F: Build a Subjective Eval (LLM-as-Judge)

**Instructor:** "Now let's evaluate newsletter quality, which is subjective."

```python
import anthropic

def eval_newsletter_quality(newsletter: str) -> dict:
    """
    Subjective eval: Use Claude as a judge to rate quality.
    
    Returns:
        dict with 'score', 'reasoning', and 'passed'
    """
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    judge_prompt = f"""
You are a professional editor evaluating a newsletter about AI.

Evaluate this newsletter on the following criteria:
1. Factual accuracy (no misinformation)
2. Clarity and readability
3. Engaging tone
4. Proper structure (headline, body, conclusion)

Newsletter to evaluate:
{newsletter}

Respond in this exact JSON format:
{{
    "score": <1-5>,
    "reasoning": "<explain your score>",
    "strengths": "<what was good>",
    "weaknesses": "<what needs improvement>"
}}
"""
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": judge_prompt}]
    )
    
    # Parse response (simplified)
    import json
    result = json.loads(response.content[0].text)
    result["passed"] = result["score"] >= 3
    
    return result

# Test it
quality_result = eval_newsletter_quality(result.output)
print(f"Score: {quality_result['score']}/5")
print(f"Reasoning: {quality_result['reasoning']}")
```

**Discussion:**
- Why is this subjective?
- Could a human disagree with the score?
- What are the limitations of LLM-as-judge?

---

### Step 2G: Compare Multiple Runs (Regression Testing)

**Instructor:** "Let's run the agent 5 times and see if quality is consistent."

```python
results = []

for i in range(5):
    print(f"\n=== Run {i+1} ===")
    
    # Run the agent
    output = crew.run()
    
    # Run both evals
    competitor_eval = eval_competitor_mentions(output.text)
    quality_eval = eval_newsletter_quality(output.text)
    
    results.append({
        "run": i+1,
        "competitor_pass": competitor_eval["passed"],
        "quality_score": quality_eval["score"],
        "token_count": output.token_count,
        "cost": output.cost
    })

# Analyze results
import pandas as pd
df = pd.DataFrame(results)
print("\n=== Summary Statistics ===")
print(df.describe())

print(f"\nCompetitor Mention Rate: {(~df['competitor_pass']).mean():.1%}")
print(f"Average Quality Score: {df['quality_score'].mean():.2f}/5")
print(f"Average Cost: ${df['cost'].mean():.4f}")
```

**Ask Students:**
"What patterns do you see? Is the agent consistent? Where should we focus improvement efforts?"

---

## Phase 3: Live Analysis & Discussion (15 minutes)

### Debugging Session

**Instructor:** "Let's diagnose why the agent mentions competitors."

#### Step 1: Examine the Prompt
```python
# Show the actual prompt sent to the Writer agent
writer_span = trace.get_span("writer_agent")
prompt = writer_span.input.messages[0].content

print("=== Writer Agent Prompt ===")
print(prompt)
```

**Ask Class:** "Do you see the problem?"

**Likely Issue:** Prompt doesn't explicitly forbid competitor mentions.

---

#### Step 2: Proposed Fix
```python
# Updated system prompt for Writer agent
WRITER_SYSTEM_PROMPT = """
You are a professional newsletter writer for our AI company.

IMPORTANT RULES:
1. Write engaging, informative content about AI developments
2. Keep a professional but accessible tone
3. NEVER mention competitor companies by name (OpenAI, Google, Microsoft, etc.)
4. Focus on technologies and trends, not specific vendors

Your goal is to educate and inform our readers about the AI landscape.
"""
```

---

#### Step 3: Re-run and Validate
```python
# Update the crew configuration
crew.update_system_prompt("writer", WRITER_SYSTEM_PROMPT)

# Run again
improved_output = crew.run()

# Re-evaluate
new_competitor_eval = eval_competitor_mentions(improved_output.text)
print(f"Competitor mentions fixed: {new_competitor_eval['passed']}")
```

---

### Performance Optimization Discussion

**Instructor:** "Looking at our traces, what's taking the most time?"

**Examine together:**
- Which span has the longest duration?
- Are there unnecessary tool calls?
- Can any steps run in parallel?

**Optimization Ideas:**
1. Cache frequent web searches
2. Parallelize independent tool calls
3. Use faster models for simple tasks
4. Implement result streaming for better UX

---

### Variables to Change (Experimentation)

**Instructor:** "Let's experiment with one variable and observe the impact."

**Option 1: Temperature**
```python
# Current setting
crew.set_temperature(0.7)

# More creative
crew.set_temperature(0.9)

# More deterministic
crew.set_temperature(0.3)
```

**Option 2: Model Selection**
```python
# Current: Claude Sonnet 4.5 (most capable)
crew.set_model("claude-sonnet-4-20250514")

# Cheaper: Claude Haiku 4.5 (faster, cheaper)
crew.set_model("claude-haiku-4-5-20251001")
```

**Re-run and compare:**
- Does quality change?
- Does cost change?
- Does latency change?

---

## Key Insights from Demo

### Insight 1: Observability is Essential
"Without Langfuse, we would be debugging blind. The traces showed us exactly where the problem occurred."

### Insight 2: Mix Evaluation Types
"We used objective evals (competitor mentions) for binary checks and subjective evals (quality scoring) for nuanced assessment. Both are necessary."

### Insight 3: Evaluation Drives Improvement
"We didn't know about the competitor mention bug until we built an eval. The eval revealed the problem, and tracing helped us fix it."

### Insight 4: Cost Management Requires Monitoring
"Without tracking tokens and cost per run, we'd have no idea if our agent is economically viable at scale."

### Insight 5: Consistency Requires Testing
"Running the agent 5 times revealed variability. Production systems need regression testing to catch degradation."

---

## Preparation for Lab

### What You'll Do in the Lab

In the independent lab, you will:
1. **Set up your own evaluation environment** (Langfuse, .env files)
2. **Build objective evals** for a different use case
3. **Implement LLM-as-judge** for subjective criteria
4. **Analyze traces** to identify bottlenecks
5. **Optimize your agent** based on eval results

### The Twist

**Demo Task:** Evaluate a Newsletter Agent  
**Lab Task:** Evaluate a Research Agent analyzing financial reports

The concepts are the same, but the domain is different. You must:
- Define what "good" means for financial research
- Create custom evaluation criteria
- Build evals that make sense for financial accuracy

---

## Common Questions

### Q: "How many evals should I build?"
**A:** Start with 3-5 evals covering:
1. Critical safety/policy checks (objective)
2. Output format validation (objective)
3. Quality assessment (subjective)
4. Cost and latency limits (objective)

### Q: "Should I test every agent run in production?"
**A:** For high-stakes applications, yes (with sampling for cost management). For low-stakes, sample 10-20% of runs.

### Q: "What if my eval contradicts human judgment?"
**A:** Evals are tools, not truth. Always validate your evals with human review and adjust them based on real user feedback.

### Q: "How do I handle flaky evals?"
**A:** LLM-as-judge can be inconsistent. Run multiple times and average, or use ensemble judging (multiple LLMs vote).

---

## Next Steps

1. **Review:** Re-read the glossary definitions for any unclear concepts
2. **Prepare:** Set up your development environment for the lab
3. **Think:** What could go wrong with a financial research agent?
4. **Lab:** Apply these concepts independently to a new problem

---

## Additional Resources

- **Langfuse Docs:** https://langfuse.com/docs
- **Evaluation Best Practices:** Andrew Ng's Agentic AI Course
- **OpenTelemetry Standard:** https://opentelemetry.io
- **LiteLLM Monitoring:** https://docs.litellm.ai/docs/proxy/cost_tracking

---

**Remember:** "The ability to do evals and error analysis is a really key skill. This makes a huge difference in your ability to build agents effectively."
