# Module 09: Conversational Swarms (AutoGen)
## Lab - Independent Application

**Duration:** 90-120 Minutes (Take-Home)  
**Goal:** Build a three-agent debate system from scratch, demonstrating mastery of AutoGen's conversational swarm capabilities.

---

## Lab Overview

In the demo, you observed a two-agent system where a primary agent and an evaluator agent collaborated on a research task. In this lab, you will build a more complex **three-agent debate system** where two agents argue opposing sides of a topic while a third judge agent evaluates their arguments.

**The Twist:** You're not replicating the demo exactly. This variation ensures you understand the principles, not just the syntax.

---

## Learning Objectives

By completing this lab, you will:

1. ✅ **Design Multi-Agent Systems:** Create agent teams with distinct roles and personalities
2. ✅ **Implement Termination Logic:** Use appropriate stopping conditions for conversational workflows
3. ✅ **Analyze Agent Interactions:** Examine conversation patterns and emergent behaviors
4. ✅ **Evaluate Trade-offs:** Assess cost, quality, and performance implications
5. ✅ **Apply Production Best Practices:** Implement security, error handling, and logging

---

## System Requirements

### **Software Dependencies**

```bash
# Install required packages
pip install autogen-agentchat autogen-ext[openai] python-dotenv --break-system-packages

# Optional: For enhanced tool capabilities
pip install langchain langchain-community google-search-results --break-system-packages
```

### **API Keys Required**

Create a `.env` file in your working directory:

```
OPENAI_API_KEY=sk-proj-your-key-here
# Optional: For web search capabilities
SERPER_API_KEY=your-serper-key-here
```

**⚠️ CRITICAL:** Add `.env` to your `.gitignore` file. Never commit API keys to version control.

---

## Part 1: System Design (Planning Phase)

Before writing any code, answer these design questions. Include your answers in your final submission.

### **Question 1.1: Debate Topic Selection**

Choose a debate topic that has legitimate arguments on both sides. Your topic should be:
- Intellectually substantive (not trivial)
- Ethical and appropriate for academic discussion
- Specific enough to generate focused arguments

**Example Topics:**
- "Should AI development be paused until better safety measures exist?"
- "Is remote work more productive than office work for software teams?"
- "Should social media platforms be regulated as public utilities?"
- "Is universal basic income economically feasible?"

**Your Chosen Topic:**
```
[Write your debate topic here]
```

**Why This Topic:**
```
[Explain why this topic is suitable for a structured debate with clear opposing viewpoints]
```

---

### **Question 1.2: Agent Role Design**

For each of your three agents, define:

**Agent 1 - Pro Debater:**
- **Name:** [e.g., "pro_advocate"]
- **Stance:** [What position will this agent argue?]
- **Personality Traits:** [e.g., logical, data-driven, passionate]
- **Key Responsibilities:** [What should this agent accomplish?]

**Agent 2 - Con Debater:**
- **Name:** [e.g., "con_advocate"]
- **Stance:** [What opposing position will this agent argue?]
- **Personality Traits:** [e.g., skeptical, analytical, pragmatic]
- **Key Responsibilities:** [What should this agent accomplish?]

**Agent 3 - Judge:**
- **Name:** [e.g., "neutral_judge"]
- **Stance:** [Neutral/Impartial]
- **Personality Traits:** [e.g., fair, evidence-based, thorough]
- **Key Responsibilities:** [How will this agent evaluate and decide?]

---

### **Question 1.3: Termination Strategy**

Design your termination condition:

**Primary Termination:** [What phrase will end the debate? e.g., "VERDICT_REACHED"]

**Safety Mechanism:** [What max_turns value will you use? Why?]

**Rationale:** 
```
[Explain your termination strategy. Why did you choose this approach?]
```

---

## Part 2: Implementation (Coding Phase)

### **Task 2.1: Environment Setup**

Create a new Python notebook or script. Start with proper imports and environment loading.

**Required Code:**

```python
# Security: Load environment variables
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Verify API key is loaded (without exposing it)
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not found in environment"
print("✓ Environment configured securely")
```

**Required Imports:**

```python
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core import CancellationToken
import time
import json
```

**✅ Checkpoint:** Run this cell and verify no import errors occur.

---

### **Task 2.2: Model Client Initialization**

Initialize your model client. You should use `gpt-4o-mini` for cost efficiency during development.

```python
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
print("✓ Model client initialized")
```

**Question:** Why use `gpt-4o-mini` instead of `gpt-4`? Include your answer in your reflection.

---

### **Task 2.3: Create Pro Debater Agent**

Build your first debater. This agent should argue the "pro" side of your chosen topic.

**Starter Template:**

```python
pro_agent = AssistantAgent(
    name="pro_advocate",
    model_client=model_client,
    system_message="""You are a skilled debater arguing in favor of [YOUR TOPIC].
    
    Your approach:
    - Present clear, logical arguments
    - Use evidence and examples to support your points
    - Anticipate counterarguments and address them
    - Be persuasive but respectful
    - Keep responses focused and concise (2-3 paragraphs max)
    
    Remember: Quality of argument matters more than length."""
)
```

**💡 Customization Required:** Modify the system message to match:
- Your specific debate topic
- The personality traits you defined in Question 1.2
- Any special instructions for argument structure

---

### **Task 2.4: Create Con Debater Agent**

Build your second debater. This agent should argue the "con" side of your topic.

**Requirements:**
- Use a different name (e.g., "con_advocate")
- System message should reflect opposing viewpoint
- Personality should contrast with pro_agent (different approach to argumentation)

**Your Code:**

```python
con_agent = AssistantAgent(
    name="con_advocate",
    model_client=model_client,
    system_message="""[YOUR SYSTEM MESSAGE HERE]"""
)
```

---

### **Task 2.5: Create Judge Agent**

Build your judge agent. This is the most critical agent as it must:
1. Evaluate arguments from both sides
2. Remain impartial
3. Declare a winner with clear reasoning

**Starter Template:**

```python
judge_agent = AssistantAgent(
    name="neutral_judge",
    model_client=model_client,
    system_message="""You are an impartial judge evaluating a debate.
    
    Your responsibilities:
    - Listen carefully to both sides
    - Evaluate arguments based on:
      * Logical coherence
      * Evidence quality
      * Persuasiveness
      * Addressing of counterarguments
    
    After [X] rounds of debate, provide a verdict:
    - Clearly state which side won
    - Explain your reasoning with specific examples
    - End your verdict with the phrase: VERDICT_REACHED
    
    You are fair and evidence-based. Your personal biases do not affect your judgment."""
)
```

**💡 Important Design Decision:** How many rounds should the judge wait before rendering a verdict? Consider:
- Too few rounds → Superficial debate
- Too many rounds → Diminishing returns, high cost
- Recommended: 4-6 rounds (2-3 turns per debater)

---

### **Task 2.6: Configure Termination Condition**

Set up your termination logic:

```python
# Termination condition - adjust keyword to match your judge's system message
text_termination = TextMentionTermination("VERDICT_REACHED")

# Safety net - prevents infinite loops
MAX_TURNS = 12  # Adjust based on your needs
```

**Design Question:** Why set `MAX_TURNS = 12` for three agents? 

**Answer:** With three agents in round-robin, 12 turns means each agent speaks 4 times. This provides sufficient depth while controlling cost.

---

### **Task 2.7: Assemble the Team**

Create your RoundRobinGroupChat:

```python
debate_team = RoundRobinGroupChat(
    participants=[pro_agent, con_agent, judge_agent],
    termination_condition=text_termination,
    max_turns=MAX_TURNS
)

print("✓ Debate team assembled")
print(f"  - Participants: {[agent.name for agent in [pro_agent, con_agent, judge_agent]]}")
print(f"  - Max turns: {MAX_TURNS}")
print(f"  - Termination: '{text_termination._text}' detected")
```

---

### **Task 2.8: Execute the Debate**

Run your debate system with timing and error handling:

```python
# Craft your debate prompt
debate_prompt = f"""
Topic: [YOUR DEBATE TOPIC]

Pro Advocate: Present your opening argument in favor.
Con Advocate: After hearing the pro argument, present your counter-argument.
Judge: After [X] rounds, evaluate both sides and declare a winner.

Begin the debate now.
"""

print("=" * 80)
print("DEBATE STARTING")
print("=" * 80)

# Execute with timing
start_time = time.time()

try:
    result = await debate_team.run(task=debate_prompt)
    end_time = time.time()
    
    print("\n" + "=" * 80)
    print("DEBATE COMPLETED")
    print("=" * 80)
    print(f"Duration: {end_time - start_time:.2f} seconds")
    print(f"Total messages: {len(result.messages)}")
    
except Exception as e:
    print(f"❌ Error during debate execution: {e}")
    raise
```

**✅ Checkpoint:** Your debate should run to completion. Verify:
- All three agents participated
- Arguments were exchanged
- Judge provided a verdict
- Termination condition was triggered

---

## Part 3: Analysis & Reflection

### **Task 3.1: Conversation Log Analysis**

Create a formatted log of the entire debate:

```python
print("\n" + "=" * 80)
print("COMPLETE DEBATE TRANSCRIPT")
print("=" * 80 + "\n")

for i, message in enumerate(result.messages, 1):
    source = message.source if hasattr(message, 'source') else 'system'
    content = message.content if hasattr(message, 'content') else str(message)
    
    print(f"\n{'─' * 80}")
    print(f"Message {i} | Speaker: {source.upper()}")
    print(f"{'─' * 80}")
    print(content)

print("\n" + "=" * 80)
print("END OF TRANSCRIPT")
print("=" * 80)
```

**Deliverable:** Include this full transcript in your submission.

---

### **Task 3.2: Argument Quality Analysis**

Analyze the quality of arguments presented:

```python
# Extract messages by agent
pro_messages = [m.content for m in result.messages if hasattr(m, 'source') and m.source == 'pro_advocate']
con_messages = [m.content for m in result.messages if hasattr(m, 'source') and m.source == 'con_advocate']
judge_messages = [m.content for m in result.messages if hasattr(m, 'source') and m.source == 'neutral_judge']

print(f"\nArgument Statistics:")
print(f"  Pro Advocate turns: {len(pro_messages)}")
print(f"  Con Advocate turns: {len(con_messages)}")
print(f"  Judge interventions: {len(judge_messages)}")
```

**Analysis Questions (Answer in your submission):**

1. **Argument Evolution:** How did the arguments change from the first turn to the last? Did debaters address each other's points?

2. **Judge Decision:** What was the judge's verdict? Do you agree with the reasoning? Why or why not?

3. **Unexpected Behaviors:** Did any agent behave in ways you didn't anticipate? Describe any emergent patterns.

4. **Conversation Flow:** Was the round-robin pattern effective for this debate? Would a different orchestration pattern work better?

---

### **Task 3.3: Cost & Performance Analysis**

Calculate the financial and time costs:

```python
# Token estimation (rough approximation)
total_chars = sum(len(str(m.content)) for m in result.messages if hasattr(m, 'content'))
estimated_tokens = total_chars // 4  # Rough estimate: 1 token ≈ 4 characters

# Cost calculation for gpt-4o-mini (as of current pricing)
input_cost_per_1m = 0.15  # $0.15 per 1M input tokens
output_cost_per_1m = 0.60  # $0.60 per 1M output tokens

# Assuming 50/50 split between input and output
estimated_input_tokens = estimated_tokens // 2
estimated_output_tokens = estimated_tokens // 2

input_cost = (estimated_input_tokens / 1_000_000) * input_cost_per_1m
output_cost = (estimated_output_tokens / 1_000_000) * output_cost_per_1m
total_cost = input_cost + output_cost

print(f"\n{'=' * 60}")
print("COST & PERFORMANCE ANALYSIS")
print(f"{'=' * 60}")
print(f"Execution Time: {end_time - start_time:.2f} seconds")
print(f"Estimated Tokens: {estimated_tokens:,}")
print(f"Estimated Cost: ${total_cost:.4f}")
print(f"\nIf run 1,000 times daily:")
print(f"  Daily cost: ${total_cost * 1000:.2f}")
print(f"  Monthly cost: ${total_cost * 1000 * 30:.2f}")
```

**Economic Analysis Questions (Answer in your submission):**

1. **Cost Justification:** Is this cost reasonable for the quality of output? Why or why not?

2. **Optimization Strategies:** How could you reduce cost while maintaining quality?
   - Smaller model?
   - Fewer turns?
   - Caching common arguments?

3. **Production Viability:** If this were a production system serving thousands of users, what would need to change?

---

### **Task 3.4: Comparison with Single-Agent Approach**

Run a single-agent baseline for comparison:

```python
# Single-agent baseline
single_agent = AssistantAgent(
    name="solo_analyst",
    model_client=model_client,
    system_message="""You are an expert analyst. Examine both sides of this debate topic 
    and provide a balanced conclusion."""
)

single_prompt = f"""
Analyze the following debate topic from both perspectives and provide a conclusion:

Topic: [YOUR DEBATE TOPIC]

Present arguments for and against, then reach a verdict.
"""

single_start = time.time()
single_message = TextMessage(content=single_prompt, source="user")
single_result = await single_agent.on_messages([single_message], cancellation_token=CancellationToken())
single_end = time.time()

print("\n" + "=" * 80)
print("SINGLE-AGENT BASELINE")
print("=" * 80)
print(single_result.chat_message.content)
print(f"\nDuration: {single_end - single_start:.2f} seconds")
```

**Comparative Analysis Questions (Answer in your submission):**

1. **Quality Comparison:** Which approach produced a more thorough analysis? Why?

2. **Cost-Benefit Trade-off:** Is the multi-agent system worth the extra cost and complexity?

3. **Use Case Suitability:** When would you choose single-agent vs. multi-agent?

---

## Part 4: Extensions & Experimentation

### **Challenge 4.1: Add Dynamic Turn Allocation**

Modify your system so the judge can interrupt the debate early if one side is clearly winning:

**Hint:** Use a different termination condition or allow the judge to speak more frequently.

### **Challenge 4.2: Implement Argument Scoring**

Have the judge provide numerical scores after each round:
- Argument strength: 1-10
- Evidence quality: 1-10
- Rhetorical effectiveness: 1-10

**Use Pydantic for structured outputs:**

```python
from pydantic import BaseModel, Field

class ArgumentScore(BaseModel):
    argument_strength: int = Field(ge=1, le=10)
    evidence_quality: int = Field(ge=1, le=10)
    rhetoric: int = Field(ge=1, le=10)
    reasoning: str

judge_agent = AssistantAgent(
    name="scoring_judge",
    model_client=model_client,
    output_content_type=ArgumentScore,
    system_message="..."
)
```

### **Challenge 4.3: Add Web Search Tools**

Give both debaters access to real-time web search to support their arguments with current facts:

```python
from autogen_ext.tools.langchain import LangChainToolAdapter
from langchain_community.utilities import GoogleSerperAPIWrapper

# Requires SERPER_API_KEY in .env
serper = GoogleSerperAPIWrapper()
search_tool = LangChainToolAdapter(
    Tool(name="web_search", func=serper.run)
)

pro_agent = AssistantAgent(
    name="pro_advocate",
    model_client=model_client,
    tools=[search_tool],  # Add web search capability
    system_message="..."
)
```

**Analysis:** Does adding web search improve argument quality? Does it increase cost significantly?

---

## Submission Requirements

### **Required Deliverables**

Your lab submission must include:

1. **✅ Design Document** (from Part 1)
   - Chosen debate topic and rationale
   - Agent role definitions
   - Termination strategy

2. **✅ Complete Python Code**
   - Well-commented and organized
   - Includes all required sections
   - Runs without errors

3. **✅ Full Debate Transcript**
   - Output from Task 3.1
   - All agent messages captured

4. **✅ Analysis Report**
   - Answers to all reflection questions (Tasks 3.2, 3.3, 3.4)
   - Cost-benefit analysis
   - Single-agent comparison
   - Personal insights and lessons learned

5. **✅ (Optional) Extensions**
   - Any Challenge tasks you completed
   - Additional experiments or modifications

---

### **Assessment Rubric**

**Pass Criteria (Must Complete ALL):**

✅ **Environment Security (20 points)**
- API keys loaded from `.env` (not hardcoded)
- `.env` file in `.gitignore`
- Code runs on instructor's machine without modification

✅ **Functional Implementation (30 points)**
- All three agents created correctly
- RoundRobinGroupChat properly configured
- Debate executes to completion
- Termination condition works as intended

✅ **Code Quality (20 points)**
- Clear comments explaining logic
- Proper error handling
- Follows Python best practices
- No hardcoded values

✅ **Analysis & Reflection (20 points)**
- All reflection questions answered thoughtfully
- Cost analysis included
- Single-agent comparison completed
- Insights demonstrate understanding

✅ **The "Twist" Requirement (10 points)**
- Your debate system is NOT an exact copy of the demo
- Three-agent architecture implemented correctly
- Custom debate topic chosen appropriately

**Fail Criteria (Any ONE Results in Failure):**

❌ **Hardcoded API keys** (security violation)
❌ **Code crashes** due to missing dependencies or errors
❌ **Exact copy of demo** without the required three-agent modification
❌ **Missing required analysis** sections

---

### **Bonus Points (Optional)**

🌟 **Extra Credit Opportunities:**

- **+5 points:** Implement one Challenge task (4.1, 4.2, or 4.3)
- **+10 points:** Implement all three Challenge tasks
- **+5 points:** Add visualization of debate flow (e.g., message flow diagram)
- **+5 points:** Implement cost budgeting/alerts (stop debate if cost exceeds threshold)

---

## Tips for Success

### **💡 Start Early**
Multi-agent systems can have unexpected behaviors. Give yourself time to debug.

### **💡 Test Incrementally**
Don't build the entire system at once. Test each agent individually before combining them.

### **💡 Read Error Messages**
AutoGen error messages are usually informative. They tell you exactly what's wrong.

### **💡 Monitor Costs**
Check your OpenAI usage dashboard periodically. gpt-4o-mini is cheap, but costs add up with iteration.

### **💡 Adjust Expectations**
Your agents might not behave exactly as planned. That's normal and part of learning about emergent behavior.

### **💡 Keep System Messages Concise**
Longer ≠ better. Focus on clear, specific instructions.

### **💡 Save Your Work Frequently**
Jupyter notebooks can crash. Save often and consider version control.

---

## Common Pitfalls to Avoid

### **❌ Pitfall 1: Overly Complex System Messages**
**Problem:** Trying to control every aspect of agent behavior with long, detailed instructions.

**Solution:** Start simple. Add complexity only when needed.

---

### **❌ Pitfall 2: No Max Turns**
**Problem:** Forgetting the safety net, leading to runaway costs.

**Solution:** Always set `max_turns`. No exceptions.

---

### **❌ Pitfall 3: Hardcoding API Keys**
**Problem:** Exposing credentials in code.

**Solution:** Use `.env` files and environment variables exclusively.

---

### **❌ Pitfall 4: Ignoring Termination Keyword**
**Problem:** Setting termination to "APPROVE" but judge says "APPROVED" → Doesn't match!

**Solution:** Ensure exact string matching. "APPROVE" ≠ "APPROVED".

---

### **❌ Pitfall 5: Insufficient Analysis**
**Problem:** Submitting code without deep reflection on what happened.

**Solution:** Spend as much time on analysis as implementation. Understanding matters more than just having working code.

---

## Resources

### **Official Documentation**
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

### **Community Resources**
- AutoGen GitHub Issues (for troubleshooting)
- Course discussion forum

### **Debugging Tips**
- Enable verbose logging: `logging.basicConfig(level=logging.DEBUG)`
- Print intermediate messages: `print(result.messages)`
- Check token counts: Monitor OpenAI dashboard

---

## Final Thoughts

This lab challenges you to move beyond replication to genuine understanding. Multi-agent systems are complex, emergent, and sometimes unpredictable. Your goal is not just to make code run, but to understand:

- **Why** certain patterns work better than others
- **When** multi-agent approaches are worth the complexity
- **How** to balance cost, quality, and performance

Good engineering is about making informed trade-offs. This lab gives you the space to explore those trade-offs firsthand.

**Good luck, and may your agents debate wisely! 🎯**

---

## Submission Checklist

Before submitting, verify:

- [ ] All API keys in `.env` file only
- [ ] `.env` file in `.gitignore`
- [ ] Code runs without errors
- [ ] All three agents implemented
- [ ] Full debate transcript included
- [ ] All analysis questions answered
- [ ] Cost analysis completed
- [ ] Single-agent comparison done
- [ ] Code is well-commented
- [ ] Submission is properly formatted

**Submit your work via [course submission platform] by [deadline].**
