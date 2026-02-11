# Module 11: Infrastructure for Multi-Agent Systems
## Glossary - Theory & Concepts (The Lecture)

**Module Focus:** This module covers the **infrastructure layer** for production multi-agent systems - routing gateways, optimization strategies, and deployment patterns. You already know how to design agent teams and decompose tasks. Now we focus on the production infrastructure that makes those systems cost-effective, performant, and reliable at scale.

**Prerequisites:**
- Multi-agent frameworks (CrewAI, AutoGen, LangGraph) 
- Task decomposition and planning
- Basic understanding of API costs and token pricing
- Docker and environment management basics

---

## Part 1: Routing Architecture

### Model Routing Gateway
A centralized service that provides a unified API interface for multiple LLM providers, allowing dynamic routing of requests based on configurable rules.

**Purpose:**
Instead of hardcoding model providers in your agents, a routing gateway provides:
- **Provider abstraction** - Change backends without changing agent code
- **Intelligent routing** - Route requests based on cost, latency, or quality requirements
- **Automatic failover** - If one provider is down, automatically try alternatives
- **Load balancing** - Distribute requests across multiple instances
- **Centralized monitoring** - Track usage, costs, and performance in one place

**Analogy:** Like a load balancer for web servers, but for LLM providers.

**Key Technologies:**
- **LiteLLM** - Open-source gateway you self-host
- **OpenRouter** - Hosted gateway service with 100+ models
- **BerriAI Proxy** - Enterprise-grade routing with advanced features

**Example Use Case:**
```python
# Without gateway - brittle and inflexible
agent = Agent(
    model="gpt-4",  # Hardcoded to OpenAI
    api_key=os.getenv("OPENAI_API_KEY")
)

# With gateway - flexible and resilient
agent = Agent(
    model="smart-router",  # Gateway decides which backend
    api_base="http://localhost:4000/v1"  # Your LiteLLM gateway
)
```

---

### Unified API Interface
A standardized API format that allows different LLM providers to be accessed through identical request/response structures.

**The Problem:**
Each provider has different APIs:
- OpenAI uses `/v1/chat/completions`
- Anthropic uses `/v1/messages`
- Google uses `/v1beta/generateContent`
- Different parameter names, formats, authentication

**The Solution:**
Routing gateways expose an OpenAI-compatible API that works with all providers.

**Benefits:**
- Write code once, work with any provider
- Easy provider switching (change config, not code)
- Consistent error handling across providers
- Simplified testing and development

**Standard Format (OpenAI-compatible):**
```python
{
  "model": "gpt-4",
  "messages": [
    {"role": "user", "content": "Hello"}
  ],
  "temperature": 0.7,
  "max_tokens": 100
}
```

All providers (Claude, Gemini, Llama) are translated to this format.

---

### Routing Strategy
The algorithm or rules used to select which backend provider should handle a specific request.

**Common Strategies:**

#### 1. Simple Round-Robin
Distribute requests evenly across all available backends.
- **Pro:** Simple, fair distribution
- **Con:** Doesn't consider backend capabilities

#### 2. Least-Latency First
Route to the fastest responding backend.
- **Pro:** Minimizes response time
- **Con:** May overload fast backends

#### 3. Cost-Optimized Routing
Route to cheapest backend that meets quality requirements.
- **Pro:** Minimizes costs
- **Con:** May sacrifice quality or speed

#### 4. Intelligent/Conditional Routing
Route based on request characteristics.

**Example Rules:**
```python
if complexity == "high":
    route_to("claude-3.5-sonnet")  # Best reasoning
elif length < 100 tokens:
    route_to("ollama/llama3.2")    # Quick, local, free
elif user_tier == "premium":
    route_to("gpt-4")              # Best quality
else:
    route_to("groq/llama-3.1-70b") # Fast and cheap
```

#### 5. Weighted Routing
Assign probability weights to backends.
```python
# 70% to cheap model, 30% to premium
weights = {
    "groq/llama-70b": 0.7,
    "gpt-4": 0.3
}
```

**Multi-Agent Context:**
Different agent roles may use different routing strategies:
- **Researcher agents:** Cost-optimized (high volume)
- **Analyst agents:** Quality-optimized (complex reasoning)
- **Coordinator agents:** Latency-optimized (in critical path)

---

### Fallback Chain
A prioritized list of alternative backends to try if the primary choice fails or is unavailable.

**Structure:**
```
Primary → Fallback 1 → Fallback 2 → Emergency Fallback
```

**Example:**
```python
fallback_chain = [
    "anthropic/claude-3.5-sonnet",  # Try best model first
    "openai/gpt-4",                 # Fallback to alternative premium
    "groq/llama-3.1-70b",           # Fallback to fast open-source
    "ollama/llama3.2"               # Emergency local fallback
]
```

**When Fallbacks Trigger:**
- API rate limit exceeded (429 error)
- Service timeout (504 error)
- Provider downtime (503 error)
- Model not available (404 error)
- Context length exceeded (400 error)

**Critical for Production:**
Multi-agent systems can't stop because one API provider has an outage. Fallback chains ensure resilience.

**Configuration Example (LiteLLM):**
```yaml
model_list:
  - model_name: "smart-claude"
    litellm_params:
      model: "claude-3-5-sonnet-20241022"
      api_key: "sk-ant-..."
    
  - model_name: "smart-claude"  # Same name!
    litellm_params:
      model: "gpt-4"  # Different backend
      api_key: "sk-..."
      
# LiteLLM automatically tries second when first fails
```

---

### Load Balancing
Distributing requests across multiple instances of the same model or provider to prevent overloading and improve throughput.

**Why It Matters:**
- **Rate limits:** OpenAI free tier = 3 RPM (requests/minute)
- **Throughput:** Single instance may be slow
- **Availability:** Distribute load to prevent bottlenecks

**Types:**

#### 1. Provider-Level Load Balancing
Multiple API keys for same provider:
```python
openai_keys = [
    "sk-key-1",
    "sk-key-2", 
    "sk-key-3"
]
# Distribute requests across keys to 3× rate limit
```

#### 2. Instance-Level Load Balancing
Multiple vLLM or Ollama instances:
```python
vllm_instances = [
    "http://gpu-server-1:8000",
    "http://gpu-server-2:8000",
    "http://gpu-server-3:8000"
]
# Each handles 33% of requests
```

#### 3. Geographic Load Balancing
Route to nearest region for lower latency:
```python
if user_location == "US":
    route_to("us-east-api.com")
elif user_location == "EU":
    route_to("eu-west-api.com")
```

**Multi-Agent Benefit:**
A 5-agent crew making 100 requests/minute needs load balancing to avoid rate limit errors.

---

## Part 2: Local Deployment Infrastructure

### Local Inference Engine
Software that runs LLM inference directly on your hardware without external API calls.

**Key Technologies:**

#### vLLM
Production-grade inference engine optimized for throughput and efficiency.

**Features:**
- **PagedAttention:** Reduces GPU memory waste by 80%
- **Continuous batching:** Process multiple requests simultaneously
- **Multi-GPU support:** Scale across multiple GPUs with tensor parallelism
- **High throughput:** Up to 24× faster than naive implementations

**When to Use:**
- ✅ High-volume inference (1000s of requests/day)
- ✅ Need sub-100ms latency
- ✅ Have GPU hardware available
- ✅ Production deployment requiring reliability
- ❌ Occasional use (hardware sits idle)
- ❌ Need 70B+ models without multiple GPUs

**Typical Deployment:**
```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct \
    --port 8000 \
    --gpu-memory-utilization 0.9 \
    --max-model-len 8192 \
    --tensor-parallel-size 2
```

---

#### Ollama
User-friendly local inference with Docker-based deployment.

**Features:**
- **One-command setup:** `ollama run llama3.2`
- **Model library:** Easy access to popular open-source models
- **OpenAI-compatible API:** Works with existing code
- **Automatic GPU detection:** Uses CUDA/Metal when available

**When to Use:**
- ✅ Development and testing
- ✅ Quick prototyping
- ✅ Desktop/laptop deployment
- ✅ Teams without DevOps expertise
- ❌ Maximum performance required
- ❌ Large-scale production deployment

**Typical Use:**
```bash
# Install and run
ollama run llama3.2

# Use in agents
api_base = "http://localhost:11434/v1"
```

---

#### LM Studio
GUI-based local LLM application with point-and-click model management.

**Features:**
- **Visual interface:** No command line required
- **Model discovery:** Browse and download from HuggingFace
- **Chat interface:** Test models before deployment
- **API server:** Toggle on to expose OpenAI-compatible endpoint

**When to Use:**
- ✅ Non-technical team members need local AI
- ✅ Desktop application for individual use
- ✅ Demos and presentations
- ❌ Server deployment
- ❌ Automated workflows

**Multi-Agent Integration:**
LM Studio runs on localhost:1234, agents connect just like any API.

---

### Quantization
Reducing model weight precision (e.g., 32-bit → 4-bit) to decrease memory usage and increase speed with minimal quality loss.

**Precision Levels:**

| Format | Bits | Memory (7B model) | Quality | Speed |
|--------|------|-------------------|---------|-------|
| FP32 | 32 | 28 GB | 100% (baseline) | 1× |
| FP16 | 16 | 14 GB | 99.9% | 1.5× |
| INT8 | 8 | 7 GB | 98% | 2× |
| INT4 | 4 | 3.5 GB | 95% | 3-4× |

**Practical Impact:**
```python
# Won't fit on consumer GPU
model_fp16 = "llama-3.1-70b-fp16"  # Needs 140 GB

# Fits on 2× consumer GPUs  
model_int4 = "llama-3.1-70b-4bit"   # Needs ~35 GB
```

**Trade-off:**
- Lower bits = less memory, faster inference
- But quality degrades (4-bit loses 5% quality)
- For most tasks, INT4 is "good enough"

**Multi-Agent Strategy:**
- **Simple tasks:** INT4 is fine (scraping, parsing)
- **Complex reasoning:** Use FP16 or cloud models
- **Cost-conscious:** Start with INT4, upgrade if quality issues

**Model Naming Convention:**
- `llama-3.1-8b-Q4_K_M.gguf` → 4-bit quantized
- `mistral-7b-instruct-v0.2-Q8_0.gguf` → 8-bit quantized

---

### Context Window
The maximum number of tokens a model can process in a single request (input + output).

**Common Limits:**

| Provider | Model | Context Window |
|----------|-------|----------------|
| OpenAI | GPT-4 Turbo | 128K tokens |
| Anthropic | Claude 3.5 Sonnet | 200K tokens |
| Google | Gemini 2.0 Flash | 1M tokens |
| Local | Llama 3.2 8B | 8K tokens |
| Local | Llama 3.1 70B | 128K tokens |

**Infrastructure Impact:**

**Scenario:** Agent needs to analyze 50-page PDF (100K tokens)

**Option 1: Large context cloud model**
- Use Gemini 2.0 (1M context)
- Single API call
- Cost: ~$1.50

**Option 2: Local model with chunking**
- Use vLLM Llama 8B (8K context)
- Split into 13 chunks
- Process in parallel on local GPU
- Cost: $0 (local)
- Time: ~30 seconds with parallelization

**Multi-Agent Consideration:**
If multiple agents need context, passing full context repeatedly is expensive. Better to:
1. Summarize once (local model)
2. Pass summary to downstream agents
3. Only use full context for final synthesis (premium model)

---

### GPU Memory Management
The process of efficiently allocating and using GPU memory for LLM inference.

**GPU Memory Components:**
1. **Model weights:** The bulk of memory (7B model ≈ 14GB FP16)
2. **KV cache:** Stores attention keys/values during generation
3. **Activations:** Temporary memory during forward pass

**vLLM's PagedAttention:**
Traditional inference wastes 20-40% of GPU memory due to fragmentation.
PagedAttention treats memory like virtual memory in operating systems:
- Memory allocated in pages
- Pages can be non-contiguous
- Dynamic allocation as needed
- Can serve 2-3× more requests with same GPU

**Practical Settings:**
```bash
# Conservative (safe)
vllm serve model --gpu-memory-utilization 0.8

# Aggressive (maximum throughput)
vllm serve model --gpu-memory-utilization 0.95

# Multi-GPU
vllm serve model --tensor-parallel-size 2
```

**Multi-Agent Scaling:**
Better GPU utilization = more concurrent agent requests = lower latency for your crew.

---

## Part 3: Optimization Strategies

### Cost Optimization
Strategies to minimize LLM API costs while maintaining acceptable quality for multi-agent systems.

**The Multi-Agent Cost Problem:**

**Naive approach:**
```
5 agents × 200 calls each × $0.03/call = $30/workflow
At 100 workflows/day = $3,000/day = $90,000/month
```

**Optimized approach:**
```
Agent 1 (coordinator): Ollama local × 200 calls = $0
Agent 2 (scraper): vLLM local × 200 calls = $0  
Agent 3 (parser): vLLM local × 200 calls = $0
Agent 4 (analyst): Claude × 200 calls = $3
Agent 5 (writer): GPT-4 × 200 calls = $6

Total per workflow: $9 (70% savings!)
At 100 workflows/day = $900/day = $27,000/month
```

**Optimization Techniques:**

#### 1. Role-Based Backend Selection
Match agent role to appropriate infrastructure:
- **High-frequency:** Local (coordinators, parsers, judges)
- **High-value:** Cloud premium (analysts, writers)
- **Medium complexity:** Cloud budget (Groq, OpenRouter free tier)

#### 2. Caching
Store and reuse expensive API responses:
```python
# First call: $0.03
response = expensive_model("Analyze market trends")

# Subsequent identical calls: $0 (cached)
cached_response = cache.get("Analyze market trends")
```

**Where to Cache:**
- Research queries (same questions asked repeatedly)
- Template generation (similar outputs)
- Validation checks (deterministic results)

#### 3. Batch Processing
Process multiple items together to reduce overhead:
```python
# Expensive: 100 calls × $0.03 = $3
for item in items:
    result = model.process(item)

# Cheaper: 1 call × $0.05 = $0.05
results = model.process_batch(items)
```

#### 4. Prompt Optimization
Shorter prompts = lower costs:
```python
# Wasteful: 1000 tokens input
prompt = f"""
You are an expert analyst with 20 years of experience...
[500 words of backstory]
Now analyze this: {data}
"""

# Efficient: 100 tokens input
prompt = f"Analyze: {data}"
```

#### 5. Graduated Response
Start with cheap model, upgrade only if needed:
```python
# Try cheap model first
result = ollama_model(query)
confidence = judge(result)

if confidence < 0.7:
    # Retry with better model
    result = claude_model(query)
```

---

### Latency Optimization
Strategies to minimize response time in multi-agent workflows.

**The Latency Problem:**

**Sequential execution:**
```
Agent 1 (200ms) → Agent 2 (200ms) → Agent 3 (200ms) → Agent 4 (200ms)
= 800ms total
```

**Latency Sources:**
1. **Network round-trip:** 50-150ms per API call
2. **Model inference:** 100-500ms depending on model size
3. **Queue wait time:** Variable (higher under load)
4. **Processing overhead:** Serialization, validation

**Optimization Techniques:**

#### 1. Parallel Execution
Run independent agents simultaneously:
```python
# Sequential: 800ms
result1 = agent1.run()
result2 = agent2.run()
result3 = agent3.run()

# Parallel: 200ms (max of three)
results = await asyncio.gather(
    agent1.run_async(),
    agent2.run_async(),
    agent3.run_async()
)
```

#### 2. Local Deployment for Critical Path
Agents in the critical path should be local:
```
❌ Cloud → Cloud → Cloud (600ms+ network)
✅ Local → Cloud → Local (200ms network)
```

#### 3. Streaming Responses
Start processing before full response received:
```python
# Blocking: Wait for full 1000 tokens
response = model.complete(prompt)
process(response)

# Streaming: Process as tokens arrive
for token in model.stream(prompt):
    process_incremental(token)
```

#### 4. Connection Pooling
Reuse HTTP connections instead of creating new ones:
```python
# Slow: New connection each call
for _ in range(100):
    response = requests.post(url, ...)

# Fast: Reuse connection
session = requests.Session()
for _ in range(100):
    response = session.post(url, ...)
```

#### 5. Model Preloading
Keep models in memory (local deployment):
```bash
# Cold start: 10-30 seconds to load model
vllm serve model

# Warm: <50ms inference once loaded
```

**Multi-Agent Strategy:**
- Parallelize data collection agents
- Use local models for coordinator agents (in critical path)
- Stream outputs from writing/generation agents
- Pre-load commonly used local models

---

### Quality vs. Cost Trade-off Matrix
A framework for deciding when to prioritize quality (expensive models) versus cost efficiency (cheap/local models).

**Decision Factors:**

| Factor | Use Premium Model | Use Budget Model |
|--------|------------------|------------------|
| **Task Complexity** | High reasoning required | Simple/deterministic |
| **Error Cost** | Mistakes are expensive | Mistakes are cheap |
| **Volume** | Low frequency (<100/day) | High frequency (1000+/day) |
| **User Facing** | Client sees output | Internal processing |
| **Latency** | Not critical | Must be fast |

**Example Decisions:**

**Scenario 1: Legal Contract Review**
- Complexity: HIGH
- Error Cost: HIGH (legal liability)
- Volume: LOW (10 contracts/day)
- **Decision:** Use premium model (GPT-4, Claude)
- **Cost:** $5/day acceptable for accuracy

**Scenario 2: Email Spam Detection**
- Complexity: LOW
- Error Cost: LOW (user can correct)
- Volume: HIGH (10,000 emails/day)
- **Decision:** Use local model (vLLM)
- **Cost:** $0/day required for scale

**Scenario 3: Content Summarization**
- Complexity: MEDIUM
- Error Cost: MEDIUM
- Volume: MEDIUM (500/day)
- **Decision:** Use mid-tier (Groq, Mistral)
- **Cost:** $5/day reasonable

**Multi-Agent Application:**
Different agents in same crew may use different quality levels:
```python
crew = [
    Scraper(model="ollama"),      # Low quality OK
    Parser(model="vllm"),          # Medium quality OK
    Analyst(model="claude"),       # High quality required
    Writer(model="gpt-4"),         # Highest quality required
    Judge(model="vllm")            # Medium quality OK, high volume
]
```

---

## Part 4: Production Patterns

### Health Checks and Monitoring
Systems for verifying backend availability and tracking performance metrics.

**Health Check Types:**

#### 1. Backend Availability Check
```python
def check_backend_health(endpoint):
    try:
        response = requests.get(f"{endpoint}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

# Check all backends
backends = {
    "ollama": "http://localhost:11434",
    "vllm": "http://localhost:8000",
    "litellm": "http://localhost:4000"
}

for name, url in backends.items():
    status = "✅" if check_backend_health(url) else "❌"
    print(f"{name}: {status}")
```

#### 2. Model Loading Verification
```python
# Verify model is actually loaded
response = requests.get("http://localhost:8000/v1/models")
models = response.json()['data']
assert len(models) > 0, "No models loaded!"
```

#### 3. Inference Test
```python
# End-to-end smoke test
response = litellm.completion(
    model="test-model",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=10
)
assert response.choices[0].message.content, "Inference failed!"
```

**Monitoring Metrics:**

**Essential Metrics:**
1. **Request rate:** Requests per minute
2. **Latency:** P50, P95, P99 response times
3. **Error rate:** Failed requests per minute
4. **Cost:** Spend per hour/day
5. **Token usage:** Input/output tokens per request

**Monitoring Tools:**
- **Prometheus + Grafana:** Time-series metrics and dashboards
- **LiteLLM built-in:** Dashboard at `http://localhost:4000/ui`
- **LangSmith:** LangChain-specific monitoring
- **Custom logging:** Track in database or file

**Alert Conditions:**
```python
if error_rate > 0.05:  # >5% errors
    alert("High error rate!")

if p95_latency > 5000:  # >5 seconds
    alert("High latency!")

if hourly_cost > budget_limit:
    alert("Over budget!")

if backend_health == False:
    alert("Backend down!")
```

---

### Rate Limit Management
Strategies for handling API rate limits across multiple agents and backends.

**Common Rate Limits:**

| Provider | Free Tier | Paid Tier |
|----------|-----------|-----------|
| OpenAI | 3 RPM, 40k TPM | 10k RPM, 10M TPM |
| Anthropic | 5 RPM, 20k TPM | Varies by tier |
| Groq | 30 RPM | 500 RPM |
| Local | Unlimited | Unlimited |

**RPM** = Requests Per Minute  
**TPM** = Tokens Per Minute

**The Multi-Agent Challenge:**
```python
# 5 agents, each making 2 calls per workflow
# 10 concurrent workflows
= 5 × 2 × 10 = 100 requests in <10 seconds
= ~600 RPM burst
```

This exceeds most free tier limits!

**Management Strategies:**

#### 1. Request Throttling
```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=30, period=60)  # 30 calls per 60 seconds
def call_groq_api(prompt):
    return groq.complete(prompt)
```

#### 2. Queue-Based Processing
```python
import asyncio

async def process_with_rate_limit(items, rpm_limit=30):
    delay = 60 / rpm_limit  # seconds between requests
    
    for item in items:
        await process_item(item)
        await asyncio.sleep(delay)
```

#### 3. Load Balancing Across Keys
```python
keys = ["key-1", "key-2", "key-3"]  # 3× rate limit
current_key = 0

def get_next_key():
    global current_key
    key = keys[current_key]
    current_key = (current_key + 1) % len(keys)
    return key
```

#### 4. Automatic Fallback on Rate Limit
```python
try:
    response = primary_api.call()
except RateLimitError:
    # Fallback to unlimited local model
    response = ollama_api.call()
```

#### 5. Request Prioritization
```python
# High-priority requests use paid tier
if priority == "high":
    response = paid_api.call()
# Low-priority uses free tier (might queue)
else:
    response = free_api.call()
```

**Multi-Agent Best Practice:**
- Use local models for high-frequency agents
- Reserve cloud APIs for complex reasoning
- Implement request queuing for bursts
- Monitor rate limit headers in responses

---

### Deployment Patterns

#### Pattern 1: Hybrid Local + Cloud
Use local for high-volume, cloud for high-complexity.

**Architecture:**
```
┌─────────────────────────────────────┐
│   Multi-Agent System                │
│                                     │
│  ┌──────────────────────────────┐  │
│  │ High-Frequency Agents        │  │
│  │ (Coordinators, Parsers)      │  │
│  │ → Local vLLM/Ollama          │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │ High-Value Agents            │  │
│  │ (Analysts, Writers)          │  │
│  │ → Cloud APIs (Claude, GPT-4) │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Benefits:**
- Best of both worlds
- Cost-effective at scale
- High quality where it matters

**Use When:**
- Have GPU resources available
- Predictable high-volume workloads
- Budget-conscious but need quality

---

#### Pattern 2: Gateway-Routed Cloud
All backends in cloud, intelligent routing via gateway.

**Architecture:**
```
┌──────────────────────────────────┐
│    LiteLLM Gateway (Self-hosted) │
│                                  │
│  Routes to:                      │
│  - OpenAI (premium)              │
│  - Anthropic (quality)           │
│  - Groq (speed)                  │
│  - OpenRouter (cost)             │
└──────────────────────────────────┘
```

**Benefits:**
- No GPU management
- Easy scaling
- Provider diversity
- Automatic failover

**Use When:**
- No GPU infrastructure
- Variable workloads
- Need maximum flexibility
- Global deployment

---

#### Pattern 3: Fully Local
All inference on owned hardware.

**Architecture:**
```
┌─────────────────────────────┐
│  GPU Server(s)              │
│                             │
│  - vLLM (primary models)    │
│  - Ollama (backup models)   │
│  - Model registry           │
└─────────────────────────────┘
```

**Benefits:**
- Zero per-request cost
- Maximum privacy
- No rate limits
- Predictable performance

**Use When:**
- Very high volume (millions of requests)
- Strict data privacy requirements
- Have GPU infrastructure
- Long-term deployment

---

#### Pattern 4: Serverless Functions
Deploy inference as serverless functions.

**Architecture:**
```
AWS Lambda / GCP Cloud Functions
→ Load model on cold start
→ Serve inference
→ Auto-scale
```

**Benefits:**
- Pay only for compute time
- Automatic scaling
- No server management

**Challenges:**
- Cold start latency (10-30s)
- Memory limits (10GB max)
- Timeout limits (15 min max)

**Use When:**
- Sporadic/unpredictable load
- Willing to accept cold starts
- Small models only (<10GB)

---

## Part 5: Decision Frameworks

### The Backend Selection Framework

**For each agent, evaluate:**

**1. Volume Analysis**
```
Calls per day?
- Low (<100): Any backend OK
- Medium (100-1000): Consider cost
- High (>1000): MUST be local/cheap
```

**2. Complexity Assessment**
```
Task complexity?
- Simple (extraction, parsing): Local models fine
- Medium (classification, summarization): Mid-tier OK
- Complex (reasoning, analysis): Premium models
```

**3. Latency Requirements**
```
Response time critical?
- Interactive (<100ms): Local required
- Responsive (<1s): Local preferred
- Batch (>1s): Cloud acceptable
```

**4. Quality Standards**
```
Error tolerance?
- Zero tolerance: Premium models
- Low tolerance: Good models
- Acceptable errors: Budget models OK
```

**5. Data Sensitivity**
```
Privacy concerns?
- Public data: Any backend
- Internal: Self-hosted preferred
- PII/PHI: Local REQUIRED
```

**Example Decision Tree:**
```
Is this agent called >1000 times/day?
├─ YES → Must be local (vLLM/Ollama)
└─ NO → Is task complex?
    ├─ YES → Use cloud premium (Claude/GPT-4)
    └─ NO → Use cloud budget (Groq/OpenRouter)
```

---

### The Cost-Performance-Quality Triangle

**The Three Constraints:**
You can optimize for any two, but not all three:

**1. Low Cost + High Performance**
→ Quality suffers
- Use fast local models (quantized)
- Accept 90-95% quality
- Example: vLLM with 4-bit models

**2. Low Cost + High Quality**
→ Performance suffers
- Use premium models sparingly
- Queue requests, batch processing
- Example: Rate-limited Claude API

**3. High Performance + High Quality**
→ Cost is high
- Use premium models with no limits
- Dedicated infrastructure
- Example: GPT-4 with high rate limits

**Multi-Agent Strategy:**
Different agents sit in different corners:
```
Coordinator: Performance + Cost (local, fast)
Analyst: Quality + Cost (premium, rate-limited)
Writer: Quality + Performance (premium, unlimited)
```

---

## Part 6: Common Pitfalls

### Pitfall 1: Hardcoded Model Names
**Problem:**
```python
agent = Agent(model="gpt-4", api_key="...")
```

**Issues:**
- Can't switch providers without code changes
- No automatic failover
- Can't optimize costs dynamically

**Solution:**
```python
agent = Agent(
    model="smart-router",
    api_base="http://localhost:4000"
)
# Router handles provider selection
```

---

### Pitfall 2: Ignoring Rate Limits
**Problem:**
```python
# Burst of 1000 requests
for item in items:
    agent.process(item)  # Hit rate limit!
```

**Solution:**
```python
# Batch with throttling
batches = chunk(items, size=30)
for batch in batches:
    process_batch(batch)
    time.sleep(60)  # Respect rate limit
```

---

### Pitfall 3: No Fallback Strategy
**Problem:**
```python
# Single point of failure
response = openai.complete(prompt)
```

**Solution:**
```python
for backend in ["openai", "anthropic", "ollama"]:
    try:
        return call_backend(backend, prompt)
    except:
        continue
raise Exception("All backends failed")
```

---

### Pitfall 4: Inefficient Local Deployment
**Problem:**
```bash
# Naive local deployment
python -m transformers.inference model.bin
# 1-2 tokens/second, 90% memory waste
```

**Solution:**
```bash
# Optimized with vLLM
vllm serve model --gpu-memory-utilization 0.9
# 50-100 tokens/second, 10% memory waste
```

---

### Pitfall 5: No Monitoring
**Problem:**
```python
# "It's slow but I don't know why"
agent.run()
```

**Solution:**
```python
import time
start = time.time()
response = agent.run()
latency = time.time() - start

metrics.record({
    'agent': agent.name,
    'latency': latency,
    'tokens': response.usage.total_tokens,
    'cost': calculate_cost(response)
})
```

---

## Key Takeaways

### 1. Infrastructure Enables Scale
Without proper infrastructure:
- Multi-agent systems are too expensive to run at scale
- Latency compounds across agent chains
- Systems are brittle (single points of failure)

### 2. Routing is Foundation
A routing gateway provides:
- Provider flexibility (swap without code changes)
- Automatic failover (resilience)
- Cost optimization (use cheap when possible)
- Centralized monitoring

### 3. Local + Cloud Hybrid
The optimal pattern for most multi-agent systems:
- Local for high-volume, low-complexity
- Cloud for low-volume, high-complexity
- Gateway to orchestrate between them

### 4. Monitor Everything
You can't optimize what you don't measure:
- Track costs per agent
- Monitor latency per backend
- Measure quality scores
- Alert on anomalies

### 5. Plan for Failure
Production systems need:
- Fallback chains
- Health checks
- Rate limit handling
- Retry logic

---

## Prerequisites Review

Before the demo, ensure you have:
- [ ] Docker Desktop installed and running
- [ ] Basic understanding of CrewAI or AutoGen
- [ ] Completed task decomposition module (Week 10)
- [ ] At least one API key (OpenAI, Anthropic, or Groq)
- [ ] 8GB+ RAM for local inference (optional but recommended)

---

## Coming Up in Demo

In the demo, we'll:
1. Set up LiteLLM as a routing gateway
2. Configure multiple backends (local + cloud)
3. Build a multi-agent system with intelligent routing
4. Measure cost and performance metrics
5. Optimize based on real data

In the lab, you'll:
1. Design your own routing strategy
2. Deploy both local and cloud backends
3. Implement fallback chains
4. Monitor and optimize your system
