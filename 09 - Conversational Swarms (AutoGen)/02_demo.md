# Module 09: Conversational Swarms (AutoGen)
## Demo - Guided Analysis (Live Coding Session)

**Duration:** 45-60 Minutes  
**Goal:** Observe a multi-agent debate system in real-time, predict outcomes, debug live errors, and analyze emergent behaviors together.

**Pedagogical Approach:** Predict-Observe-Explain (POE). Before running key cells, we'll predict what should happen, then observe the actual output, and finally explain any discrepancies.

---

## Demo Overview

**Scenario:** We will build a multi-agent system that simulates a debate between two AI agents moderated by a third evaluator agent. This demonstrates how conversational swarms can generate higher-quality outputs through iterative refinement.

**System Architecture:**
- **Primary Agent:** Researches and proposes solutions
- **Evaluation Agent:** Provides constructive criticism and feedback
- **Termination Condition:** Conversation stops when evaluator says "APPROVE"

---

## Phase 1: Environment & Safety Check

### **Step 1.1: The "Wrong" Way (Security Anti-Pattern)**

**Instructor Note:** Intentionally demonstrate the security violation first.

```python
# ❌ NEVER DO THIS
import openai
openai.api_key = "sk-proj-abc123..."  # Hardcoded API key = SECURITY VIOLATION
```

**Question to Class:** *"What's wrong with this approach? What happens if this code gets committed to GitHub?"*

**Expected Answer:** API keys would be exposed, leading to:
- Unauthorized usage of your account
- Unexpected charges
- Potential account ban
- Security breach

---

### **Step 1.2: The "Right" Way (Security Best Practice)**

```python
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# ✅ Correct: Keys loaded from .env file
# .env file is in .gitignore and never committed
```

**Your .env file should contain:**
```
OPENAI_API_KEY=sk-proj-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Question to Class:** *"Why use `override=True`? When would this matter?"*

**Expected Answer:** In Jupyter notebooks or long-running processes, you might reload the .env file after making changes. `override=True` ensures the new values replace old cached ones.

---

### **Step 1.3: Import Required Libraries**

```python
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core import CancellationToken
from autogen_ext.tools.langchain import LangChainToolAdapter
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool
```

**Prediction Question:** *"Before we run this, what happens if one of these imports fails?"*

**Intentional Error Simulation:**
```python
# Simulate missing package
from autogen_ext.tools.langchain import LangChainToolAdapter
```

**Expected Error:**
```
ModuleNotFoundError: No module named 'autogen_ext'
```

**Correction:**
```bash
pip install autogen-agentchat autogen-ext[openai] --break-system-packages
```

**Teaching Point:** Always check dependencies before starting. Read error messages carefully—they tell you exactly what's missing.

---

## Phase 2: Building the Agent Team

### **Step 2.1: Initialize Model Client**

```python
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
```

**Question to Class:** *"Why use gpt-4o-mini instead of gpt-4?"*

**Discussion Points:**
- Cost: 4o-mini is ~90% cheaper
- Speed: Faster response times
- Quality: For many tasks, mini is sufficient
- Iteration: Use mini during development, upgrade to full model for production

**Teaching Point:** Engineering is about making trade-offs under constraints. During development and testing, optimize for speed and cost. In production, optimize for quality.

---

### **Step 2.2: Set Up Web Search Tool (Optional but Realistic)**

```python
# Initialize Google Serper for web search
serper = GoogleSerperAPIWrapper()
langchain_serper = Tool(
    name="internet_search",
    func=serper.run,
    description="Search the internet for current information"
)
autogen_serper = LangChainToolAdapter(langchain_serper)
```

**Note:** This requires a Serper API key. If unavailable, we'll proceed without it to demonstrate the debate pattern itself.

**Question to Class:** *"Why wrap the LangChain tool in an adapter? Why not use LangChain directly?"*

**Expected Answer:** The adapter pattern allows AutoGen to use tools from multiple ecosystems. It translates between different tool interfaces, giving us flexibility and preventing vendor lock-in.

---

### **Step 2.3: Create Primary Research Agent**

```python
prompt = """Find a one-way non-stop flight from JFK to LHR in June 2025."""

primary_agent = AssistantAgent(
    name="primary",
    model_client=model_client,
    tools=[autogen_serper],  # Comment out if no Serper API
    system_message="""You are a helpful AI research assistant who looks for 
    precise, factual information. When given a task, you research thoroughly 
    and provide detailed answers with sources. Be specific and cite your sources."""
)
```

**Prediction Question:** *"What do you expect this agent to do when given the prompt about flights?"*

**Expected Behavior:**
1. Agent will attempt to call the internet_search tool
2. It will query for "non-stop flights JFK to LHR June 2025"
3. It will parse results and provide a structured answer

---

### **Step 2.4: Create Evaluation Agent**

```python
evaluation_agent = AssistantAgent(
    name="evaluator",
    model_client=model_client,
    system_message="""Provide constructive feedback on the primary agent's response. 
    
    Check for:
    - Factual accuracy
    - Completeness of information
    - Citation of sources
    - Clarity and usefulness
    
    If the response meets all criteria, respond with 'APPROVE' to signal completion.
    If not, provide specific feedback on what needs improvement."""
)
```

**Discussion Point:** *"Why does the evaluator NOT have tools? What's the architectural reason?"*

**Expected Answer:** Separation of concerns. The primary agent gathers data, the evaluator judges quality. This prevents the evaluator from doing the primary agent's work and ensures a true review process.

---

### **Step 2.5: Create Termination Condition**

```python
text_termination = TextMentionTermination("APPROVE")
```

**Prediction Question:** *"What happens if the evaluator never says 'APPROVE'? Could this run forever?"*

**Expected Answer:** Yes! That's why we need a safety mechanism...

---

### **Step 2.6: Assemble the Team**

```python
team = RoundRobinGroupChat(
    [primary_agent, evaluation_agent],
    termination_condition=text_termination,
    max_turns=10  # Safety net!
)
```

**Critical Teaching Point:** The `max_turns` parameter is your safety net. Without it, agent conversations could theoretically continue indefinitely, burning through your API budget.

**Question to Class:** *"In a round-robin with 2 agents and max_turns=10, how many total messages will be exchanged before forced termination?"*

**Expected Answer:** Up to 20 messages (10 turns × 2 agents per turn), plus the initial prompt.

---

## Phase 3: Live Execution and Analysis

### **Step 3.1: Run the Team**

**Before Running:** *"Let's predict what will happen. Who speaks first? How many turns will it take?"*

```python
result = await team.run(task=prompt)
```

**Observe Live Output:** Watch the conversation unfold in real-time.

**Expected Flow:**
```
Turn 1:
[primary] I searched for non-stop flights from JFK to LHR in June 2025...

Turn 2:
[evaluator] Your response needs improvement. You didn't specify airlines, prices, or exact dates...

Turn 3:
[primary] Based on your feedback, I conducted a more detailed search. Here are specific options:
- British Airways Flight BA112: June 15, 2025, $850
- American Airlines AA100: June 20, 2025, $920
...

Turn 4:
[evaluator] APPROVE - This response is comprehensive and well-sourced.
```

**Termination:** Conversation stops when "APPROVE" is detected.

---

### **Step 3.2: Analyze the Message History**

```python
print(f"\n{'='*60}")
print("CONVERSATION ANALYSIS")
print(f"{'='*60}\n")

for i, message in enumerate(result.messages):
    print(f"Message {i+1} - Source: {message.source}")
    print(f"Content: {message.content[:200]}...")  # Truncated for readability
    print("-" * 60)
```

**Analysis Questions:**

1. **Turn Count:** *"How many turns did it actually take? Why?"*
   
2. **Quality Evolution:** *"Compare the first and last responses from the primary agent. What changed?"*

3. **Feedback Effectiveness:** *"What specific feedback did the evaluator provide? Was it actionable?"*

4. **Termination:** *"When did the evaluator finally approve? What criteria were met?"*

---

### **Step 3.3: Examine Tool Calls (if applicable)**

```python
# Extract tool calls from inner messages
for message in result.messages:
    if hasattr(message, 'inner_messages'):
        for inner in message.inner_messages:
            if 'tool_call' in str(inner):
                print(f"Tool Call Detected: {inner}")
```

**Question to Class:** *"How many times did the agent call the search tool? Why multiple times?"*

**Expected Pattern:** The agent might call the tool multiple times based on evaluator feedback, refining its search queries.

---

## Phase 4: Experimentation and Variables

### **Experiment 1: Changing the Termination Word**

```python
# Change termination condition
text_termination = TextMentionTermination("PERFECT")

# Update evaluator's system message
evaluation_agent = AssistantAgent(
    name="evaluator",
    model_client=model_client,
    system_message="""Provide constructive feedback. 
    Respond with 'PERFECT' when the response is flawless."""
)

# Recreate team and run again
team = RoundRobinGroupChat(
    [primary_agent, evaluation_agent],
    termination_condition=text_termination,
    max_turns=10
)

result = await team.run(task=prompt)
```

**Prediction Question:** *"Will changing 'APPROVE' to 'PERFECT' change behavior? How?"*

**Discussion:** Higher standards might lead to more iterations. The evaluator might be more critical.

---

### **Experiment 2: Adding a Third Agent (Judge)**

```python
judge_agent = AssistantAgent(
    name="judge",
    model_client=model_client,
    system_message="""You are a neutral judge. Review the conversation between 
    the primary agent and evaluator. Determine if consensus has been reached. 
    Say 'CONSENSUS' when both agents agree."""
)

# Three-agent team
team = RoundRobinGroupChat(
    [primary_agent, evaluation_agent, judge_agent],
    termination_condition=TextMentionTermination("CONSENSUS"),
    max_turns=15
)
```

**Prediction Question:** *"How will adding a third agent change the conversation dynamics?"*

**Expected Outcome:** More complex conversations, potentially better consensus, but higher cost and latency.

---

### **Experiment 3: Changing the Task Complexity**

**Simple Task:**
```python
prompt = "What is 2+2?"
```

**Prediction:** Should terminate in 1-2 turns. The evaluator will likely approve immediately since the answer is trivial.

**Complex Task:**
```python
prompt = """Compare the economic policies of Keynesian economics versus 
Austrian economics. Provide historical examples of each approach's successes 
and failures."""
```

**Prediction:** Many turns. The evaluator will request more detail, specific examples, and balanced analysis.

**Question to Class:** *"How does task complexity affect the number of iterations? Is there a relationship between ambiguity and turn count?"*

---

## Phase 5: Error Scenarios and Debugging

### **Intentional Error 1: Infinite Loop (No Max Turns)**

```python
# Remove max_turns - DANGEROUS!
team = RoundRobinGroupChat(
    [primary_agent, evaluation_agent],
    termination_condition=TextMentionTermination("APPROVE")
    # No max_turns!
)
```

**Warning:** This could run indefinitely if evaluator never approves.

**Teaching Point:** Always include safety mechanisms. Production systems should have:
- Max turns
- Timeouts
- Cost limits
- Circuit breakers

---

### **Intentional Error 2: Conflicting System Messages**

```python
# Both agents told to dominate conversation
primary_agent = AssistantAgent(
    name="primary",
    model_client=model_client,
    system_message="Argue strongly. Never back down. Insist you are right."
)

evaluation_agent = AssistantAgent(
    name="evaluator",
    model_client=model_client,
    system_message="Find flaws in everything. Never approve anything."
)
```

**Prediction:** This will hit max_turns without reaching APPROVE.

**Question to Class:** *"What's the architectural lesson here? How do we prevent this?"*

**Expected Answer:** System messages must be aligned with the workflow goal. Adversarial agents can be useful for thorough vetting, but they need eventual convergence criteria.

---

## Phase 6: Cost and Performance Analysis

### **Calculate Cost and Latency**

```python
import time

start_time = time.time()
result = await team.run(task=prompt)
end_time = time.time()

print(f"\nPerformance Metrics:")
print(f"Total Duration: {end_time - start_time:.2f} seconds")
print(f"Number of Turns: {len(result.messages)}")
print(f"Number of LLM Calls: {len(result.messages)}")  # Approximate

# Rough cost estimate (gpt-4o-mini pricing)
input_tokens_estimate = sum(len(m.content) // 4 for m in result.messages)
output_tokens_estimate = sum(len(m.content) // 4 for m in result.messages)

input_cost = (input_tokens_estimate / 1_000_000) * 0.15  # $0.15/1M input tokens
output_cost = (output_tokens_estimate / 1_000_000) * 0.60  # $0.60/1M output tokens

print(f"Estimated Cost: ${input_cost + output_cost:.4f}")
```

**Question to Class:** *"If we scale this to 1,000 conversations per day, what's our monthly cost? Is this sustainable?"*

**Discussion Points:**
- Cost-quality trade-offs
- When to use cheaper models
- Caching strategies
- Rate limiting

---

## Phase 7: Key Observations and Discussion

### **Discussion Topic 1: Emergent Behavior**

*"Did you notice any unexpected behaviors? Did the conversation go in directions you didn't predict?"*

**Common Emergent Patterns:**
- Agents becoming more formal/specific over iterations
- Unexpected tool usage patterns
- Self-correction without explicit instructions
- Hallucination detection by peer review

---

### **Discussion Topic 2: Single Agent vs. Multi-Agent**

*"How would the quality differ if we used a single agent instead of this two-agent debate?"*

**Expected Insights:**
- Single agent more likely to be overconfident
- No built-in validation or review
- Multi-agent catches errors through dialogue
- But: higher cost and latency

---

### **Discussion Topic 3: Production Readiness**

*"What would we need to add to make this production-ready?"*

**Key Additions:**
- Proper error handling and retries
- Logging and observability
- Rate limiting
- Cost budgets and alerts
- Caching of common queries
- User feedback mechanisms

---

## Phase 8: Summary and Transition

### **What We Learned**

1. **Multi-agent systems** can produce higher quality outputs through peer review
2. **Termination conditions** are critical for cost control
3. **System messages** define agent behavior and must be carefully crafted
4. **Round-robin orchestration** enables iterative refinement
5. **Trade-offs** exist between quality, cost, and latency

### **Key Architectural Takeaway**

The conversation pattern itself—not just the individual agent capabilities—determines system behavior. Orchestration matters as much as intelligence.

---

## Transition to Lab

Now it's your turn. In the **Independent Lab**, you'll build your own multi-agent debate system from scratch. However, there's a twist: instead of replicating exactly what we did in this demo, you'll implement a **three-agent debate system** where:

1. Two agents argue opposing viewpoints
2. A third judge agent evaluates arguments and declares a winner
3. You'll choose your own debate topic

This variation ensures you understand the underlying principles, not just how to copy code.

**Lab Challenge Preview:** Your system must:
- Include all three agents
- Use appropriate termination conditions
- Log the full conversation history
- Analyze which agent won and why
- Reflect on cost and quality trade-offs

See you in the Lab phase! 🚀
