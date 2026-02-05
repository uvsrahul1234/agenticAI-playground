# Agentic AI Glossary - Terms

## Quick Reference Guide for Students

This glossary defines all agentic AI concepts, frameworks, and patterns demonstrated in the "Exploring LLMs" notebook. Terms are organized by category for easy lookup.

---

## 🧠 Core Agentic Concepts

### Agent
**Definition:** An autonomous system that perceives its environment, reasons about actions, and executes tasks to achieve goals—typically using an LLM as its "brain."

**Components of an Agent:**
1. **Perception:** Gathering information (e.g., user queries, database results)
2. **Reasoning:** Planning actions using an LLM
3. **Action:** Executing tools (e.g., API calls, database queries)
4. **Memory:** Retaining context across interactions

**Example:** A customer support agent that:
- Perceives: User asks "Where's my order?"
- Reasons: "I need to check the order database"
- Acts: Queries database with order ID
- Responds: "Your order shipped yesterday"

---

### Agentic System
**Definition:** A collection of one or more agents that can:
- Make decisions autonomously
- Use tools/APIs
- Maintain stateful conversations
- Collaborate with other agents

**Key Distinction:** 
- ❌ **Not Agentic:** A chatbot that just generates text based on a prompt
- ✅ **Agentic:** A system that can decide "I need to search the web" and execute that action

---

### Model-Agnostic Interface
**Definition:** A unified code structure that allows swapping between different LLM providers without changing application logic.

**Why It Matters:**
Agentic systems often need to:
- Route simple tasks to cheap models (e.g., local Llama for classification)
- Escalate complex reasoning to expensive models (e.g., GPT-4 for planning)
- Fall back to alternatives when one provider has an outage

**Implementation Pattern:**
```python
# Same messages array works everywhere
messages = [{"role": "user", "content": "Hello"}]

# Just change the client and model
openai.chat.completions.create(model="gpt-4o", messages=messages)
claude.messages.create(model="claude-3-7-sonnet", messages=messages)
ollama.chat.completions.create(model="llama3.2", messages=messages)
```

**Real-World Use:** 
A newsletter generation crew might:
1. Use local Llama for topic extraction (cheap, fast)
2. Use Claude for writing (high quality)
3. Use GPT-4 for final editing (expensive, best)

---

### LLM-as-Judge
**Definition:** Using an LLM to evaluate the quality, accuracy, or adherence to criteria of outputs from other LLMs (or itself).

**Use Cases in Agentic Systems:**
1. **Quality Control:** An editor agent grades a writer agent's output
2. **Debate Resolution:** A judge agent scores arguments from two debating agents
3. **Automated Testing:** Checking if agent responses meet standards
4. **A/B Testing:** Comparing which prompt engineering technique works best

**Implementation Pattern:**
```python
evaluator_prompt = f"""
You are evaluating {len(responses)} agent outputs.
Rank them by [criteria] from best to worst.
Respond with JSON: {{"results": ["1", "2", "3"]}}
"""
```

**Critical Considerations:**
- **Bias:** The judge's training affects its preferences
- **Criteria:** Vague instructions ("rank by quality") produce unreliable results
- **Structured Output:** Force JSON to enable programmatic use

**Connection:** CrewAI's "hierarchical" mode uses this pattern—a manager agent evaluates worker agents.

---

## 🔌 API & Integration Concepts

### OpenAI-Compatible API
**Definition:** A standardized interface that many providers (Groq, Ollama, LM Studio, OpenRouter) implement to mimic OpenAI's API format.

**Why It Exists:**
OpenAI's API became the de facto standard, so other providers adopted the same structure for easy migration.

**Key Pattern:**
```python
# All use the same OpenAI client
from openai import OpenAI

# Just change base_url and api_key
groq = OpenAI(api_key="...", base_url="https://api.groq.com/openai/v1")
ollama = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
```

**What's Standardized:**
- Message format: `[{"role": "user", "content": "..."}]`
- Response structure: `response.choices[0].message.content`
- Streaming interface: `for chunk in stream: ...`

**What's NOT Standardized:**
- Model names (each provider has different options)
- Extra parameters (e.g., Anthropic requires `max_tokens`)
- Rate limits and pricing

---

### Base URL
**Definition:** The root web address where an API's endpoints are hosted.

**Examples:**
- OpenAI: `https://api.openai.com/v1`
- Groq: `https://api.groq.com/openai/v1`
- Ollama: `http://localhost:11434/v1` (local)
- LM Studio: `http://localhost:1234/v1` (local)

**Why It Matters:** Changing just the `base_url` lets you redirect API calls to different providers.

---

### Environment Variables
**Definition:** Configuration values stored outside your code (e.g., in a `.env` file) that are loaded at runtime.

**Common Usage:**
```
# .env file
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
```

**Security Benefits:**
1. ✅ Keys aren't visible in code repositories (Git)
2. ✅ Different values for dev/staging/production
3. ✅ Easy to rotate keys without changing code

**Python Implementation:**
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
```

**Best Practice:** Add `.env` to `.gitignore` immediately.

---

### Service Availability Checking
**Definition:** Programmatically verifying that required APIs or servers are reachable before attempting to use them.

**Purpose:** Fail fast with clear error messages instead of cryptic network errors.

**Implementation:**
```python
def is_service_running(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False

if is_service_running('http://localhost:11434'):
    print("✅ Ollama ready")
else:
    print("❌ Start Ollama: ollama serve")
```

**Agentic Use Case:**
Before launching a multi-agent workflow, verify:
- ✅ Vector database is responding
- ✅ Local LLM server is running
- ✅ All API keys are valid

---

## 🖥️ Local vs. Cloud Inference

### Cloud Inference
**Definition:** Sending prompts to external APIs (OpenAI, Anthropic, Google) where models run on the provider's servers.

**Characteristics:**
- ✅ Latest/best models (GPT-4, Claude Opus)
- ✅ No local compute required
- ✅ Automatic scaling
- ❌ Costs per token
- ❌ Data leaves your control
- ❌ Requires internet connection
- ❌ Latency from network round-trips

**When to Use:**
- Final production outputs
- Complex reasoning tasks
- When quality matters more than cost
- Prototyping without local GPU

---

### Local Inference
**Definition:** Running LLM models on your own hardware (laptop, server) using tools like Ollama or LM Studio.

**Characteristics:**
- ✅ Free after model download
- ✅ Complete data privacy
- ✅ Works offline
- ✅ No rate limits
- ❌ Requires RAM/VRAM (8GB+ recommended)
- ❌ Smaller/quantized models (lower quality)
- ❌ Slower without GPU acceleration

**When to Use:**
- Development/testing (save API costs)
- High-frequency tool calls in agents
- Sensitive data (HIPAA, GDPR compliance)
- Demos without internet
- High-volume classification tasks

---

### Quantization
**Definition:** Reducing a model's precision (e.g., from 16-bit to 4-bit numbers) to make it smaller and faster at the cost of some quality.

**Example:**
- Original Llama 3 70B: ~140GB
- Q4_K_M quantized: ~38GB (fits in consumer RAM)

**File Extensions:**
- `.gguf` - Common format for quantized models (Ollama, LM Studio)
- `Q4_0`, `Q4_K_M`, `Q8_0` - Different quantization levels

**Trade-offs:**
- Q8 (8-bit): Minimal quality loss, still large
- Q4 (4-bit): Noticeable quality loss, much smaller
- Q2 (2-bit): Significant degradation, very small

**Agentic Application:**
A local Q4 model might be "good enough" for:
- Extracting keywords from documents
- Routing user queries to specialized agents
- Simple yes/no classification

But you'd still use cloud models for:
- Writing high-quality content
- Complex multi-step reasoning
- Tasks where accuracy is critical

---

## 📊 Evaluation & Quality Control

### Structured Output
**Definition:** Forcing LLMs to return data in predictable formats (JSON, XML) rather than free-form text.

**Why It Matters:**
Agents act on LLM outputs—if the format is inconsistent, the agent breaks.

**Without Structure:**
```
Response: "I think gpt-4o-mini was best, then claude..."
# ❌ Can't parse this programmatically
```

**With Structure:**
```json
{"results": ["1", "2", "3"]}
// ✅ Can reliably extract rankings
```

**Methods to Enforce:**
1. **Prompt Engineering:** "Respond with JSON, nothing else"
2. **JSON Mode:** OpenAI's `response_format={"type": "json_object"}`
3. **Function Calling:** Define explicit schemas 
4. **Pydantic Validation:** Type-checked parsing 

---

### Evaluation Criteria
**Definition:** Specific, measurable standards used to judge LLM outputs.

**Examples:**
- ✅ **Good Criteria:** "Clarity (1-10): Is the instruction understandable to non-experts?"
- ❌ **Vague Criteria:** "Quality" (too subjective)

**Multi-Dimensional Evaluation:**
Instead of a single score, rate on multiple axes:
```json
{
  "clarity": 8,
  "creativity": 7,
  "factual_accuracy": 9,
  "conciseness": 6
}
```

**Connection:** Production evaluation suites test agents on domain-specific criteria (e.g., "Does the customer support agent resolve issues in <3 messages?").

---

### Ranking vs. Rating
**Ranking:** Order items from best to worst (relative comparison)
- Example: `["model_1", "model_3", "model_2"]`
- Good for: Choosing which model to deploy

**Rating:** Assign absolute scores to each item
- Example: `{"model_1": 8.5, "model_2": 7.2, "model_3": 9.1}`
- Good for: Understanding *how much* better one option is

**Notebook Uses Ranking:** Simpler for LLMs to compare than assign precise numerical scores.

---

## 🛠️ Tools & Frameworks

### Ollama
**Definition:** An open-source command-line tool and server for running quantized LLMs locally.

**Key Features:**
- One-command model download: `ollama pull llama3.2`
- OpenAI-compatible API: Works with existing code
- Automatic quantization: Models are optimized for your hardware
- Multi-model support: Run multiple models simultaneously

**Common Commands:**
```bash
ollama list              # Show installed models
ollama pull llama3.2     # Download a model
ollama serve             # Start API server (usually auto-starts)
ollama run llama3.2      # Interactive chat
```

**Agentic Use Case:** Background server that agents call for cheap, fast classifications.

---

### LM Studio
**Definition:** A desktop GUI application for running local LLMs with a user-friendly interface.

**Key Features:**
- Model marketplace: Search/download from Hugging Face
- Built-in chat interface: Test models before coding
- Local API server: OpenAI-compatible endpoint
- GPU acceleration: Automatically uses NVIDIA/Apple Silicon

**Advantages over Ollama:**
- Visual model browsing
- Real-time performance stats
- Easier for non-technical users

**Agentic Use Case:** Rapid experimentation with different models during agent development.

---

### dotenv (python-dotenv)
**Definition:** A Python library that loads key-value pairs from a `.env` file into environment variables.

**Usage:**
```python
from dotenv import load_dotenv
load_dotenv()  # Reads .env file in current directory
```

**Why Not Just Use os.environ?**
- ✅ Keeps secrets separate from code
- ✅ Easy to have different .env files per environment (dev/prod)
- ✅ Supported by deployment platforms (Heroku, Vercel)

---

## 🧩 Advanced Patterns (Preview)

### Async/Await 
**Definition:** Running multiple operations concurrently without blocking.

**Example:**
```python
# Sequential (slow)
response1 = openai.chat.completions.create(...)  # Wait 2 seconds
response2 = claude.messages.create(...)          # Wait 2 seconds
# Total: 4 seconds

# Concurrent (fast)
import asyncio
response1, response2 = await asyncio.gather(
    openai_async_call(),
    claude_async_call()
)
# Total: ~2 seconds (both run simultaneously)
```

**Why Agents Need This:**
When calling 6 LLMs sequentially (as in the notebook), you waste time waiting. Async lets agents:
- Query multiple tools in parallel
- Handle many user requests simultaneously
- Stream responses while processing next steps

---

### Pydantic Models 
**Definition:** Python classes that validate and type-check data at runtime.

**Example:**
```python
from pydantic import BaseModel

class EvaluationResult(BaseModel):
    results: list[str]
    confidence: float

# This will error if JSON doesn't match
result = EvaluationResult.model_validate_json(llm_output)
```

**Why Agents Need This:**
LLMs are stochastic—they might return:
```json
{"results": [1, 2, 3]}  // ❌ Integers instead of strings
{"results": "1,2,3"}     // ❌ String instead of list
```

Pydantic catches these issues before they crash your agent.

---

### Model Context Protocol (MCP) 
**Definition:** Anthropic's open standard for safely connecting LLMs to external tools (filesystems, databases, APIs).

**How It Relates to This Notebook:**
The notebook demonstrates the *concept* of swapping backends—MCP formalizes this with:
- Standardized tool definitions
- Security boundaries (what files can agents access?)
- Stateful connections (agents remember database sessions)

**Implementation:**
Instead of manually coding each tool, MCP provides:
```python
# Declarative tool definition
@mcp_tool
def search_files(query: str) -> list[str]:
    # Search implementation
```

And agents automatically discover it.

---

### Function Calling 
**Definition:** OpenAI's (and others') API feature that lets you define tools LLMs can invoke.

**How It Works:**
1. You define a tool schema: "Here's a `search_web(query: str)` function"
2. LLM decides: "I need to call `search_web('current weather')`"
3. Your code executes the function
4. LLM receives results and responds to user

**Notebook Connection:**
The "OpenAI-compatible API" pattern is the foundation—function calling is the next layer.

---

## 🎯 Production Patterns

### Model Routing
**Definition:** Dynamically selecting which LLM to use based on task requirements.

**Decision Factors:**
1. **Complexity:** Simple tasks → cheap models
2. **Latency:** Real-time chat → fast models (Groq)
3. **Privacy:** Sensitive data → local models
4. **Cost:** High-volume tasks → free tiers

**Example Routing Logic:**
```python
def route_to_model(task_complexity: int):
    if task_complexity < 3:
        return "llama3.2"  # Local, free
    elif task_complexity < 7:
        return "gpt-4o-mini"  # Cloud, cheap
    else:
        return "claude-opus"  # Cloud, expensive, best
```

---

### Fallback Strategies
**Definition:** Plans for when primary models fail (rate limits, outages, errors).

**Implementation:**
```python
models = ["gpt-4o", "claude-sonnet", "llama-local"]

for model in models:
    try:
        response = call_model(model, prompt)
        break  # Success
    except Exception as e:
        print(f"Failed {model}: {e}")
        continue  # Try next model
```

**Agentic Reliability:**
Production agents should NEVER crash because one API is down.

---

### Cost Tracking
**Definition:** Monitoring token usage and expenses across multiple providers.

**Basic Implementation:**
```python
costs = {
    "gpt-4o-mini": 0.00015,  # per 1K tokens
    "claude-sonnet": 0.003,
}

total_cost = 0
for response in responses:
    tokens = response.usage.total_tokens
    total_cost += (tokens / 1000) * costs[model]

print(f"Experiment cost: ${total_cost:.4f}")
```

**Why It Matters:**
A poorly optimized agent making 1M API calls/day could cost thousands of dollars.

---

## 📚 Additional Terms

### Token
**Definition:** The smallest unit of text an LLM processes—roughly ¾ of a word in English.

**Examples:**
- "Hello" → 1 token
- "Hello, world!" → 4 tokens
- "GPT-4" → 3 tokens (G, PT, -4)

**Why It Matters:**
- Cloud APIs charge per token
- Context windows have token limits (e.g., 128K tokens ≈ 96K words)

---

### Context Window
**Definition:** The maximum amount of text (input + output) an LLM can process in a single request.

**Sizes:**
- GPT-4o: 128K tokens (~300 pages)
- Claude Opus: 200K tokens (~500 pages)
- Llama 3.2: 8K tokens (~20 pages)

**Agentic Implication:**
Agents with long conversations or large documents may exceed context windows—requiring:
- Summarization
- Vector databases (RAG)
- Conversation compression

---

### Temperature
**Definition:** A parameter (0.0-2.0) controlling randomness in LLM outputs.

**Values:**
- 0.0: Deterministic, always picks most likely token
- 1.0: Balanced (default)
- 2.0: Very creative, sometimes nonsensical

**Agentic Use:**
- Low (0.1): Structured tasks (JSON generation, classification)
- High (1.5): Creative tasks (brainstorming, storytelling)

---

### Latency
**Definition:** The time between sending a request and receiving the first token of the response.

**Typical Values:**
- Groq: ~50ms (LPU architecture)
- OpenAI: ~300ms
- Local CPU: 2000ms+
- Local GPU: ~200ms

**Why It Matters:**
In real-time agentic apps (chatbots, voice assistants), latency affects user experience.

---

### Rate Limit
**Definition:** The maximum number of requests allowed per time period.

**Examples:**
- OpenAI Free Tier: 3 RPM (requests per minute)
- Groq Free Tier: 30 RPM
- Local models: Unlimited (but slower)

**Agentic Challenge:**
Agents making rapid tool calls can hit rate limits—solutions:
- Exponential backoff (wait, retry)
- Request batching
- Model routing (fallback to local)

---

## Quick Reference Table

| Term | Definition | Why It Matters |
|------|-----------|----------------|
| **Agent** | Autonomous system using LLM to reason and act | Core concept of the course |
| **Model-Agnostic** | Code that works across providers | Enables flexible model routing |
| **LLM-as-Judge** | Using LLM to evaluate outputs | Automates quality control |
| **OpenAI-Compatible** | Standard API format | Easy provider switching |
| **Cloud Inference** | Using external APIs | Latest models, no local compute |
| **Local Inference** | Running models locally | Privacy, cost, offline use |
| **Structured Output** | JSON/XML responses | Reliable downstream processing |
| **Quantization** | Compressing models | Runs large models on consumer hardware |
| **Environment Variables** | Config stored outside code | Security and flexibility |

---

## Study Questions

1. When would you use a local model instead of GPT-4?
2. Why is "LLM-as-Judge" better than manual evaluation for agents?
3. What's the risk of not using structured outputs?
4. How does model-agnostic design relate to Model Context Protocol?
5. Why does Anthropic's API require `max_tokens` but OpenAI's doesn't?

---

**Moving Forward**

Refer back to this document as you build agentic systems in later weeks. Understanding these terms will help you make informed architectural decisions.
