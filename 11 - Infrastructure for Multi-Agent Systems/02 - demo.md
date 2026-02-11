# Module 11: Infrastructure for Multi-Agent Systems
## Demo - Guided Analysis (The Live Demo)

**Pedagogical Approach:** This demo uses **Predict-Observe-Explain (POE)** methodology. Before each step, we'll predict what should happen, observe the actual results, and explain any differences. This keeps you engaged and helps identify common misconceptions.

**Demo Objective:** Build production infrastructure for a multi-agent content generation system, demonstrating routing, optimization, and deployment patterns.

**Scenario:** A content marketing agency runs a 3-agent CrewAI system that generates blog posts:
- **Researcher Agent:** Gathers information on topics
- **Writer Agent:** Creates draft content  
- **Editor Agent:** Refines and polishes the draft

Currently, all agents use GPT-4, costing $0.15 per blog post. They generate 200 posts/day = **$30/day** = **$900/month**.

**Goal:** Reduce costs by 70% while maintaining quality through intelligent routing and infrastructure optimization.

---

## Phase 1: Infrastructure Setup

### Step 1: Current State Analysis

**Let's examine the existing (naive) implementation:**

```python
# current_system.py - What they have now
from crewai import Agent, Task, Crew

# All agents hardcoded to GPT-4
researcher = Agent(
    role="Research Specialist",
    goal="Gather information about given topic",
    backstory="Expert researcher with access to web",
    model="gpt-4",  # Expensive!
    api_key=os.getenv("OPENAI_API_KEY")
)

writer = Agent(
    role="Content Writer",
    goal="Write engaging blog posts",
    backstory="Professional content writer",
    model="gpt-4",  # Expensive!
    api_key=os.getenv("OPENAI_API_KEY")
)

editor = Agent(
    role="Copy Editor",
    goal="Polish and refine content",
    backstory="Experienced editor",
    model="gpt-4",  # Expensive!
    api_key=os.getenv("OPENAI_API_KEY")
)

# Process workflow
crew = Crew(agents=[researcher, writer, editor], ...)
result = crew.kickoff(inputs={"topic": "AI trends"})
```

**🤔 POE Moment #1: Predict - What are the problems with this setup?**

<details>
<summary>Click to see analysis</summary>

**Problems:**
1. ❌ All agents use expensive GPT-4 ($0.03/1K tokens)
2. ❌ Hardcoded to single provider (vendor lock-in)
3. ❌ No fallback if OpenAI has outage
4. ❌ No way to A/B test different models
5. ❌ No cost/performance monitoring
6. ❌ Can't optimize different agents differently

**Observe:** When we run this, it works but costs add up:
- Research: ~1500 tokens = $0.045
- Writing: ~2000 tokens = $0.060
- Editing: ~1500 tokens = $0.045
- **Total: $0.15 per post × 200/day = $30/day**

**Explain:** This is the "naive production" pattern - it works but doesn't scale economically.
</details>

---

### Step 2: Setting Up LiteLLM Gateway

**First, let's set up our routing infrastructure:**

```bash
# Terminal 1: Install LiteLLM
pip install litellm[proxy]

# Create config file
cat > litellm_config.yaml << EOF
model_list:
  # Cloud providers
  - model_name: gpt-4
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_API_KEY
      
  - model_name: claude-sonnet
    litellm_params:
      model: claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY
      
  - model_name: groq-fast
    litellm_params:
      model: groq/llama-3.1-70b-versatile
      api_key: os.environ/GROQ_API_KEY

  # Local models (we'll set these up next)
  - model_name: local-mistral
    litellm_params:
      model: ollama/mistral
      api_base: http://localhost:11434
      
  - model_name: local-llama
    litellm_params:
      model: ollama/llama3.2
      api_base: http://localhost:11434

# Router settings
router_settings:
  routing_strategy: simple-shuffle
  num_retries: 3
  timeout: 30
  
# Fallback configuration
fallbacks:
  - model: claude-sonnet
    fallback_models: 
      - groq-fast
      - local-mistral
EOF

# Start LiteLLM proxy
litellm --config litellm_config.yaml --port 4000
```

**Expected Output:**
```
INFO: Uvicorn running on http://0.0.0.0:4000 (Press CTRL+C to quit)
INFO: Proxy running on http://0.0.0.0:4000
INFO: Dashboard available at http://0.0.0.0:4000/ui
```

**🤔 POE Moment #2: Predict - What happens if we call an invalid model name?**

<details>
<summary>Click to test</summary>

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:4000/v1",
    api_key="any-string-works"  # LiteLLM doesn't validate
)

# Try invalid model
response = client.chat.completions.create(
    model="nonexistent-model",
    messages=[{"role": "user", "content": "Hello"}]
)
```

**Observe:** We get an error:
```
litellm.exceptions.NotFoundError: Model nonexistent-model not found
```

**Explain:** LiteLLM validates model names against the config. This prevents typos from causing silent failures.
</details>

---

### Step 3: Setting Up Local Inference (Ollama)

**Terminal 2: Start Ollama**

```bash
# Install Ollama (if not already installed)
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve

# In another terminal, pull models
ollama pull llama3.2     # 3B model, fast
ollama pull mistral      # 7B model, better quality

# Verify models are running
curl http://localhost:11434/api/tags

# Test inference
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Hello, what is 2+2?",
  "stream": false
}'
```

**Expected Response:**
```json
{
  "model": "llama3.2",
  "response": "2+2 equals 4.",
  "done": true
}
```

**🤔 POE Moment #3: Predict - How much does this local inference cost?**

<details>
<summary>Click to see answer</summary>

**Cost: $0 per request!**

**But consider:**
- Initial setup time: 30 minutes
- Model download: 2GB bandwidth
- Ongoing: Electricity (~$50/month for always-on server)
- Hardware: Needs 8-16GB RAM

**Observe:** First request is slow (5-10 seconds - cold start)
**Observe:** Subsequent requests are fast (100-500ms - warm)

**Explain:** 
- Local inference trades upfront cost (hardware, setup) for $0 per-request cost
- Makes sense when volume is high (>1000 requests/day)
- Break-even analysis: 1000 requests/day × $0.001 = $1/day = $30/month
- Local pays for itself after ~2 months of operation
</details>

---

### Step 4: Verify Gateway Routing

**Test the complete routing setup:**

```python
# test_routing.py
import openai
import time

client = openai.OpenAI(
    base_url="http://localhost:4000/v1",
    api_key="dummy"
)

def test_model(model_name):
    """Test a specific model through the gateway"""
    print(f"\n🧪 Testing {model_name}...")
    
    start = time.time()
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": "Say 'hello' in one word"}
            ],
            max_tokens=10
        )
        latency = (time.time() - start) * 1000  # Convert to ms
        
        print(f"✅ Success!")
        print(f"   Response: {response.choices[0].message.content}")
        print(f"   Latency: {latency:.0f}ms")
        print(f"   Model: {response.model}")
        
        return True, latency
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False, 0

# Test all configured models
models_to_test = [
    "gpt-4",
    "claude-sonnet",
    "groq-fast",
    "local-mistral",
    "local-llama"
]

results = {}
for model in models_to_test:
    success, latency = test_model(model)
    results[model] = {"success": success, "latency": latency}

# Summary
print("\n" + "="*60)
print("ROUTING TEST SUMMARY")
print("="*60)
for model, result in results.items():
    status = "✅" if result["success"] else "❌"
    latency = f"{result['latency']:.0f}ms" if result["success"] else "N/A"
    print(f"{status} {model:20s} - {latency}")
```

**Expected Output:**
```
🧪 Testing gpt-4...
✅ Success!
   Response: Hello
   Latency: 1250ms
   Model: gpt-4

🧪 Testing claude-sonnet...
✅ Success!
   Response: Hello
   Latency: 980ms
   Model: claude-3-5-sonnet-20241022

🧪 Testing groq-fast...
✅ Success!
   Response: Hello
   Latency: 245ms
   Model: llama-3.1-70b-versatile

🧪 Testing local-mistral...
✅ Success!
   Response: Hello
   Latency: 156ms
   Model: mistral

🧪 Testing local-llama...
✅ Success!
   Response: Hello
   Latency: 89ms
   Model: llama3.2

============================================================
ROUTING TEST SUMMARY
============================================================
✅ gpt-4                 - 1250ms
✅ claude-sonnet         - 980ms
✅ groq-fast             - 245ms
✅ local-mistral         - 156ms
✅ local-llama           - 89ms
```

**🤔 POE Moment #4: Predict - Why is local-llama faster than groq-fast?**

<details>
<summary>Click to see explanation</summary>

**Latency Breakdown:**

**Local (89ms):**
- Network: 0ms (localhost)
- Model inference: 89ms
- **Total: 89ms**

**Groq Cloud (245ms):**
- Network round-trip: ~100ms
- Model inference: ~145ms
- **Total: 245ms**

**Observe:** Local is 2.7× faster despite Groq having optimized infrastructure

**Explain:** 
- Network latency matters! ~100ms just to reach cloud
- Local inference eliminates network overhead
- For simple queries, network time dominates
- For complex queries (1000+ tokens), cloud may be faster (better hardware)

**Key Insight:** Local models win on latency for short queries, lose on quality/capability
</details>

---

## Phase 2: Building the Optimized Multi-Agent System

### Step 5: Agent Backend Selection Strategy

**Now let's redesign our agents with intelligent backend selection:**

```python
# optimized_system.py
from crewai import Agent, Task, Crew
import openai

# Point all agents to our LiteLLM gateway
GATEWAY_URL = "http://localhost:4000/v1"
client = openai.OpenAI(base_url=GATEWAY_URL, api_key="dummy")

# Backend selection based on agent role
RESEARCHER_CONFIG = {
    "model": "groq-fast",  # Fast, cheap, good enough for research
    "temperature": 0.3,
    "reasoning": """
    Researcher does simple web search and extraction.
    - Complexity: LOW (no deep reasoning)
    - Volume: HIGH (called for every blog post)
    - Quality: MEDIUM needed (accuracy important but not critical)
    → Decision: Use Groq (fast, cheap at $0.0005/1K tokens)
    """
}

WRITER_CONFIG = {
    "model": "claude-sonnet",  # High quality writing
    "temperature": 0.7,
    "reasoning": """
    Writer creates the main content - quality matters most.
    - Complexity: HIGH (creative writing)
    - Volume: MEDIUM (once per blog post)
    - Quality: HIGH needed (client-facing output)
    → Decision: Use Claude (best writing quality at $0.015/1K tokens)
    """
}

EDITOR_CONFIG = {
    "model": "local-mistral",  # Good enough for grammar/polish
    "temperature": 0.2,
    "reasoning": """
    Editor fixes grammar, improves flow.
    - Complexity: MEDIUM (pattern recognition)
    - Volume: HIGH (called for every blog post)
    - Quality: MEDIUM needed (fixing obvious issues)
    → Decision: Use local Mistral (FREE, fast, adequate quality)
    """
}

# Create optimized agents
researcher = Agent(
    role="Research Specialist",
    goal="Gather information about given topic",
    backstory="Expert researcher with access to web",
    llm_config={
        "config_list": [{
            "model": RESEARCHER_CONFIG["model"],
            "base_url": GATEWAY_URL,
            "api_key": "dummy",
            "temperature": RESEARCHER_CONFIG["temperature"]
        }]
    },
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Write engaging blog posts",
    backstory="Professional content writer",
    llm_config={
        "config_list": [{
            "model": WRITER_CONFIG["model"],
            "base_url": GATEWAY_URL,
            "api_key": "dummy",
            "temperature": WRITER_CONFIG["temperature"]
        }]
    },
    verbose=True
)

editor = Agent(
    role="Copy Editor",
    goal="Polish and refine content",
    backstory="Experienced editor",
    llm_config={
        "config_list": [{
            "model": EDITOR_CONFIG["model"],
            "base_url": GATEWAY_URL,
            "api_key": "dummy",
            "temperature": EDITOR_CONFIG["temperature"]
        }]
    },
    verbose=True
)

print("✅ Optimized agents configured:")
print(f"   Researcher → {RESEARCHER_CONFIG['model']}")
print(f"   Writer     → {WRITER_CONFIG['model']}")
print(f"   Editor     → {EDITOR_CONFIG['model']}")
```

**🤔 POE Moment #5: Predict - Why didn't we use GPT-4 anywhere?**

<details>
<summary>Click to see reasoning</summary>

**Analysis by agent:**

**Researcher:**
- Task: Web search and summarization
- Could use GPT-4 ($0.03/1K) but Groq ($0.0005/1K) is 60× cheaper
- Quality difference: Minimal for research tasks
- **Decision:** Groq wins on cost/performance ratio

**Writer:**
- Task: Creative long-form content
- GPT-4 ($0.03/1K) vs Claude Sonnet ($0.015/1K)
- Claude has slightly better writing style
- 50% cheaper than GPT-4
- **Decision:** Claude wins on quality AND cost

**Editor:**
- Task: Grammar, flow, polish
- Could use GPT-4 but local Mistral is FREE
- Quality: 90% as good is acceptable for editing
- **Decision:** Local wins on cost (FREE!)

**Observe:** GPT-4 isn't always the best choice!
**Explain:** Different models excel at different tasks. Don't default to most expensive.
</details>

---

### Step 6: Implementing Cost Tracking

**Add monitoring to track actual costs:**

```python
# cost_tracker.py
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
import json

@dataclass
class RequestMetrics:
    timestamp: datetime
    agent: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    cost_usd: float

class CostTracker:
    """Track costs and performance across the multi-agent system"""
    
    # Pricing per 1K tokens (input + output averaged)
    PRICING = {
        "gpt-4": 0.03,
        "claude-sonnet": 0.015,
        "groq-fast": 0.0005,
        "local-mistral": 0.0,  # Free!
        "local-llama": 0.0     # Free!
    }
    
    def __init__(self):
        self.requests: List[RequestMetrics] = []
    
    def record(self, agent: str, model: str, input_tokens: int, 
               output_tokens: int, latency_ms: float):
        """Record a single request"""
        total_tokens = input_tokens + output_tokens
        cost = (total_tokens / 1000) * self.PRICING.get(model, 0)
        
        metrics = RequestMetrics(
            timestamp=datetime.now(),
            agent=agent,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            cost_usd=cost
        )
        
        self.requests.append(metrics)
    
    def get_summary(self) -> Dict:
        """Generate cost summary"""
        if not self.requests:
            return {"error": "No requests recorded"}
        
        total_cost = sum(r.cost_usd for r in self.requests)
        total_tokens = sum(r.input_tokens + r.output_tokens for r in self.requests)
        avg_latency = sum(r.latency_ms for r in self.requests) / len(self.requests)
        
        # Cost by agent
        agent_costs = {}
        for req in self.requests:
            if req.agent not in agent_costs:
                agent_costs[req.agent] = 0
            agent_costs[req.agent] += req.cost_usd
        
        # Cost by model
        model_costs = {}
        for req in self.requests:
            if req.model not in model_costs:
                model_costs[req.model] = 0
            model_costs[req.model] += req.cost_usd
        
        return {
            "total_requests": len(self.requests),
            "total_cost": total_cost,
            "total_tokens": total_tokens,
            "avg_latency_ms": avg_latency,
            "cost_by_agent": agent_costs,
            "cost_by_model": model_costs,
            "cost_per_workflow": total_cost / len(set(r.timestamp.minute for r in self.requests))
        }
    
    def print_summary(self):
        """Print formatted summary"""
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print("COST & PERFORMANCE SUMMARY")
        print("="*60)
        
        print(f"\n📊 Overall Metrics:")
        print(f"   Total requests: {summary['total_requests']}")
        print(f"   Total cost: ${summary['total_cost']:.4f}")
        print(f"   Total tokens: {summary['total_tokens']:,}")
        print(f"   Avg latency: {summary['avg_latency_ms']:.0f}ms")
        print(f"   Cost per workflow: ${summary['cost_per_workflow']:.4f}")
        
        print(f"\n💰 Cost by Agent:")
        for agent, cost in summary['cost_by_agent'].items():
            pct = (cost / summary['total_cost']) * 100 if summary['total_cost'] > 0 else 0
            print(f"   {agent:15s} ${cost:.4f} ({pct:.1f}%)")
        
        print(f"\n🔧 Cost by Model:")
        for model, cost in summary['cost_by_model'].items():
            pct = (cost / summary['total_cost']) * 100 if summary['total_cost'] > 0 else 0
            print(f"   {model:15s} ${cost:.4f} ({pct:.1f}%)")
    
    def export_json(self, filename="metrics.json"):
        """Export metrics to JSON"""
        data = {
            "summary": self.get_summary(),
            "requests": [
                {
                    "timestamp": r.timestamp.isoformat(),
                    "agent": r.agent,
                    "model": r.model,
                    "tokens": r.input_tokens + r.output_tokens,
                    "latency_ms": r.latency_ms,
                    "cost_usd": r.cost_usd
                }
                for r in self.requests
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✅ Metrics exported to {filename}")

# Global tracker instance
tracker = CostTracker()
```

---

### Step 7: Running the Optimized System

**Execute the complete workflow with monitoring:**

```python
# run_optimized.py
import time
from optimized_system import researcher, writer, editor
from cost_tracker import tracker
from crewai import Task, Crew

def create_blog_workflow(topic: str):
    """Create tasks for blog generation"""
    
    research_task = Task(
        description=f"""
        Research the topic: {topic}
        
        Find:
        - Key concepts and definitions
        - Recent trends and developments
        - Expert opinions
        - Relevant statistics
        
        Return a structured summary of findings.
        """,
        expected_output="Research summary with key points",
        agent=researcher
    )
    
    writing_task = Task(
        description="""
        Based on the research, write a 500-word blog post.
        
        Requirements:
        - Engaging introduction
        - Clear structure with headers
        - Concrete examples
        - Actionable conclusion
        
        Write in a professional but conversational tone.
        """,
        expected_output="Complete blog post in markdown",
        agent=writer,
        context=[research_task]  # Depends on research
    )
    
    editing_task = Task(
        description="""
        Edit and polish the blog post.
        
        Check for:
        - Grammar and spelling
        - Flow and readability
        - Consistent tone
        - Clear structure
        
        Return the final polished version.
        """,
        expected_output="Final polished blog post",
        agent=editor,
        context=[writing_task]  # Depends on writing
    )
    
    return [research_task, writing_task, editing_task]

# Create crew
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[],  # Tasks created dynamically
    process="sequential",
    verbose=True
)

# Generate blog post with monitoring
topic = "The Future of AI in Healthcare"

print(f"\n🚀 Generating blog post about: {topic}")
print("="*60)

start_time = time.time()

# Create tasks for this topic
crew.tasks = create_blog_workflow(topic)

# Execute
result = crew.kickoff()

total_time = time.time() - start_time

print("\n✅ Blog post generated!")
print(f"   Total time: {total_time:.1f}s")

# Simulate recording metrics (in real implementation, this would be automated)
# For demo purposes, we'll manually record based on expected usage

# Research phase: Groq, ~800 input + 700 output tokens
tracker.record(
    agent="researcher",
    model="groq-fast",
    input_tokens=800,
    output_tokens=700,
    latency_ms=1200
)

# Writing phase: Claude, ~1200 input + 1800 output tokens  
tracker.record(
    agent="writer",
    model="claude-sonnet",
    input_tokens=1200,
    output_tokens=1800,
    latency_ms=3500
)

# Editing phase: Local Mistral, ~2000 input + 1500 output tokens
tracker.record(
    agent="editor",
    model="local-mistral",
    input_tokens=2000,
    output_tokens=1500,
    latency_ms=850
)

# Print summary
tracker.print_summary()

# Calculate savings
naive_cost = 0.15  # Original system cost
optimized_cost = tracker.get_summary()['cost_per_workflow']
savings = naive_cost - optimized_cost
savings_pct = (savings / naive_cost) * 100

print(f"\n💡 Cost Comparison:")
print(f"   Naive (all GPT-4): ${naive_cost:.4f}/post")
print(f"   Optimized:         ${optimized_cost:.4f}/post")
print(f"   Savings:           ${savings:.4f}/post ({savings_pct:.1f}%)")
print(f"\n   Daily (200 posts):")
print(f"   Naive:             ${naive_cost * 200:.2f}/day")
print(f"   Optimized:         ${optimized_cost * 200:.2f}/day")
print(f"   Monthly savings:   ${savings * 200 * 30:.2f}")

# Export metrics
tracker.export_json("optimization_results.json")
```

**Expected Output:**
```
🚀 Generating blog post about: The Future of AI in Healthcare
============================================================

[Research phase logs...]
[Writing phase logs...]
[Editing phase logs...]

✅ Blog post generated!
   Total time: 5.6s

============================================================
COST & PERFORMANCE SUMMARY
============================================================

📊 Overall Metrics:
   Total requests: 3
   Total cost: $0.0453
   Total tokens: 8,000
   Avg latency: 1850ms
   Cost per workflow: $0.0453

💰 Cost by Agent:
   researcher      $0.0008 (1.7%)
   writer          $0.0450 (99.3%)
   editor          $0.0000 (0.0%)

🔧 Cost by Model:
   groq-fast       $0.0008 (1.7%)
   claude-sonnet   $0.0450 (99.3%)
   local-mistral   $0.0000 (0.0%)

💡 Cost Comparison:
   Naive (all GPT-4): $0.1500/post
   Optimized:         $0.0453/post
   Savings:           $0.1047/post (69.8%)

   Daily (200 posts):
   Naive:             $30.00/day
   Optimized:         $9.06/day
   Monthly savings:   $628.20

✅ Metrics exported to optimization_results.json
```

**🤔 POE Moment #6: Why does the writer agent cost 99% of total?**

<details>
<summary>Click to analyze</summary>

**Cost Breakdown:**
- Researcher (Groq): 1500 tokens × $0.0005/1K = **$0.0008**
- Writer (Claude): 3000 tokens × $0.015/1K = **$0.0450**
- Editor (Local): 3500 tokens × $0/1K = **$0.0000**

**Observe:** Claude is 56× more expensive than Groq per token

**Explain:** 
- Even though Claude is cheaper than GPT-4, it's still the cost center
- This is expected - quality writing requires premium model
- The optimization came from using cheaper models for research and editing
- We saved 70% by using appropriate models, not by downgrading everywhere

**Key Insight:** Don't make everything cheap - make expensive things rare!
</details>

---

## Phase 3: Advanced Optimization

### Step 8: Implementing Fallback Chains

**Add resilience with automatic failover:**

```python
# fallback_config.py
from litellm import completion
import time

def smart_completion_with_fallback(messages, agent_name, primary_model, fallback_chain):
    """
    Try primary model, fallback to alternatives on failure.
    """
    
    all_models = [primary_model] + fallback_chain
    
    for i, model in enumerate(all_models):
        try:
            print(f"   [{agent_name}] Trying {model}...")
            start = time.time()
            
            response = completion(
                model=model,
                messages=messages,
                api_base="http://localhost:4000/v1"
            )
            
            latency = (time.time() - start) * 1000
            print(f"   [{agent_name}] ✅ Success with {model} ({latency:.0f}ms)")
            
            # Track which model actually handled request
            return response, model, latency
            
        except Exception as e:
            print(f"   [{agent_name}] ❌ {model} failed: {e}")
            
            # If we have more fallbacks, continue
            if i < len(all_models) - 1:
                print(f"   [{agent_name}] Falling back to next option...")
                continue
            else:
                # No more fallbacks
                raise Exception(f"All models failed for {agent_name}")

# Fallback configurations per agent role
FALLBACK_CHAINS = {
    "researcher": {
        "primary": "groq-fast",
        "fallbacks": ["local-mistral", "local-llama"]
    },
    "writer": {
        "primary": "claude-sonnet",
        "fallbacks": ["gpt-4", "groq-fast"]
    },
    "editor": {
        "primary": "local-mistral",
        "fallbacks": ["local-llama", "groq-fast"]
    }
}

# Test fallback behavior
def test_fallback_chain():
    """Simulate primary failure to test fallback"""
    
    print("\n🧪 Testing Fallback Chains\n")
    
    # Simulate researcher with primary (Groq) unavailable
    print("Scenario: Groq API is down")
    print("-" * 60)
    
    # Temporarily set Groq to invalid endpoint to simulate failure
    messages = [{"role": "user", "content": "Test message"}]
    
    response, used_model, latency = smart_completion_with_fallback(
        messages=messages,
        agent_name="researcher",
        primary_model="groq-fast-OFFLINE",  # Simulate failure
        fallback_chain=["local-mistral", "local-llama"]
    )
    
    print(f"\n   ✅ Workflow succeeded using fallback: {used_model}")
    print(f"   Latency: {latency:.0f}ms")
    
test_fallback_chain()
```

**Expected Output:**
```
🧪 Testing Fallback Chains

Scenario: Groq API is down
------------------------------------------------------------
   [researcher] Trying groq-fast-OFFLINE...
   [researcher] ❌ groq-fast-OFFLINE failed: Model not found
   [researcher] Falling back to next option...
   [researcher] Trying local-mistral...
   [researcher] ✅ Success with local-mistral (156ms)

   ✅ Workflow succeeded using fallback: local-mistral
   Latency: 156ms
```

**🤔 POE Moment #7: What happens if ALL models in the chain fail?**

<details>
<summary>Click to see</summary>

```python
# All models offline (unrealistic but possible)
try:
    response, model, latency = smart_completion_with_fallback(
        messages=messages,
        agent_name="researcher",
        primary_model="offline-1",
        fallback_chain=["offline-2", "offline-3"]
    )
except Exception as e:
    print(f"❌ Complete system failure: {e}")
```

**Observe:** System raises exception and stops

**Explain:** 
- Fallback chains increase reliability but aren't magic
- If all backends fail, workflow must stop
- In production, alert operators when fallback chains are exhausted
- Consider queuing requests to retry later

**Production Pattern:**
```python
try:
    result = agent.run()
except AllBackendsFailedError:
    # Add to retry queue
    retry_queue.add(task, retry_after=60)
    # Alert operations team
    send_alert("All backends failed for agent X")
```
</details>

---

### Step 9: Comparing Local vs. Cloud Performance

**Benchmark different deployment strategies:**

```python
# performance_comparison.py
import time
import statistics

def benchmark_model(model_name, num_runs=10):
    """Benchmark a model's performance"""
    
    prompt = "Summarize the key benefits of cloud computing in one sentence."
    latencies = []
    
    print(f"\n🔬 Benchmarking {model_name}...")
    
    for i in range(num_runs):
        start = time.time()
        
        response = completion(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            api_base="http://localhost:4000/v1"
        )
        
        latency = (time.time() - start) * 1000
        latencies.append(latency)
        
        print(f"   Run {i+1}: {latency:.0f}ms")
    
    return {
        "model": model_name,
        "avg_latency": statistics.mean(latencies),
        "p50_latency": statistics.median(latencies),
        "p95_latency": statistics.quantiles(latencies, n=20)[18],  # 95th percentile
        "min_latency": min(latencies),
        "max_latency": max(latencies)
    }

# Benchmark all models
models = ["gpt-4", "claude-sonnet", "groq-fast", "local-mistral", "local-llama"]
results = []

for model in models:
    result = benchmark_model(model, num_runs=10)
    results.append(result)

# Print comparison table
print("\n" + "="*80)
print("PERFORMANCE COMPARISON")
print("="*80)
print(f"{'Model':<20} {'Avg':<10} {'P50':<10} {'P95':<10} {'Min':<10} {'Max':<10}")
print("-"*80)

for r in results:
    print(f"{r['model']:<20} "
          f"{r['avg_latency']:>8.0f}ms "
          f"{r['p50_latency']:>8.0f}ms "
          f"{r['p95_latency']:>8.0f}ms "
          f"{r['min_latency']:>8.0f}ms "
          f"{r['max_latency']:>8.0f}ms")

# Determine fastest
fastest = min(results, key=lambda x: x['avg_latency'])
print(f"\n🏆 Fastest model: {fastest['model']} ({fastest['avg_latency']:.0f}ms avg)")

# Determine most consistent (lowest variance)
variances = [(r['model'], r['max_latency'] - r['min_latency']) for r in results]
most_consistent = min(variances, key=lambda x: x[1])
print(f"📊 Most consistent: {most_consistent[0]} ({most_consistent[1]:.0f}ms range)")
```

**Expected Output:**
```
================================================================================
PERFORMANCE COMPARISON
================================================================================
Model                Avg        P50        P95        Min        Max       
--------------------------------------------------------------------------------
gpt-4                   1234ms     1198ms     1456ms      987ms     1523ms
claude-sonnet            987ms      956ms     1123ms      845ms     1234ms
groq-fast                245ms      238ms      298ms      198ms      345ms
local-mistral            156ms      152ms      178ms      134ms      189ms
local-llama               89ms       87ms      102ms       78ms      112ms

🏆 Fastest model: local-llama (89ms avg)
📊 Most consistent: local-llama (34ms range)
```

**🤔 POE Moment #8: Should we use local-llama for everything?**

<details>
<summary>Click to think through this</summary>

**Temptation:** "Local-llama is fastest and free - use it everywhere!"

**Reality Check:**

**Quality Test:**
```python
test_prompt = "Explain quantum entanglement in simple terms"

# Local-llama response:
"Quantum entanglement is when particles are connected..."
[Basic, somewhat vague]

# Claude response:
"Quantum entanglement is a phenomenon where two or more particles become 
interconnected in such a way that the quantum state of each particle 
cannot be described independently..."
[Detailed, accurate, clear]
```

**Observe:** Local-llama is 11× faster but quality suffers

**Decision Framework:**
- **Use local-llama when:** Speed critical, quality acceptable (>90%)
- **Use Claude when:** Quality critical, speed acceptable
- **Don't:** Optimize everything for speed

**Key Insight:** Fastest ≠ Best. Match capability to requirement.
</details>

---

## Phase 4: Production Recommendations

### Step 10: Deployment Architecture

**Let's design the production architecture:**

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION SETUP                          │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│  Load Balancer       │
│  (nginx/HAProxy)     │
└───────────┬──────────┘
            │
     ┌──────┴──────┐
     │             │
┌────▼─────┐  ┌───▼──────┐
│ LiteLLM  │  │ LiteLLM  │  (Multiple instances for HA)
│ Instance │  │ Instance │
│    :4000 │  │    :4001 │
└────┬─────┘  └────┬─────┘
     │             │
     └──────┬──────┘
            │
     ┌──────┴──────────────────────────────┐
     │                                     │
     │  Routes to:                         │
     │                                     │
     │  ┌─────────────────────────┐       │
     │  │ Local Infrastructure    │       │
     │  │ - vLLM (GPU servers)    │       │
     │  │ - Ollama (CPU servers)  │       │
     │  │ - Redis (caching)       │       │
     │  └─────────────────────────┘       │
     │                                     │
     │  ┌─────────────────────────┐       │
     │  │ Cloud Providers         │       │
     │  │ - OpenAI (premium)      │       │
     │  │ - Anthropic (quality)   │       │
     │  │ - Groq (speed)          │       │
     │  └─────────────────────────┘       │
     │                                     │
     └─────────────────────────────────────┘
            │
     ┌──────▼──────────┐
     │  Monitoring     │
     │  - Prometheus   │
     │  - Grafana      │
     │  - Alerting     │
     └─────────────────┘
```

**Key Components:**

1. **Load Balancer:** Distribute traffic across LiteLLM instances
2. **Multiple LiteLLM instances:** High availability
3. **Local inference tier:** vLLM for production workloads
4. **Cloud backup tier:** Premium models when needed
5. **Monitoring:** Track everything

---

### Step 11: Key Takeaways and Best Practices

```python
# best_practices.py

INFRASTRUCTURE_GUIDELINES = {
    "routing": {
        "DO": [
            "Use gateway (LiteLLM/OpenRouter) for flexibility",
            "Configure fallback chains for all agents",
            "Route based on agent role, not one-size-fits-all",
            "Test routing before production"
        ],
        "DON'T": [
            "Hardcode model names in agent definitions",
            "Use same model for all agents",
            "Ignore failure scenarios",
            "Skip load testing"
        ]
    },
    
    "optimization": {
        "DO": [
            "Use local models for high-volume agents",
            "Reserve premium models for complex tasks",
            "Measure costs per agent/model",
            "Implement caching for repeated queries"
        ],
        "DON'T": [
            "Use premium models for everything",
            "Optimize prematurely - measure first",
            "Sacrifice quality for tiny cost savings",
            "Ignore latency requirements"
        ]
    },
    
    "deployment": {
        "DO": [
            "Deploy local infrastructure for volume",
            "Keep local models warm (preloaded)",
            "Use Docker for consistency",
            "Monitor health of all backends"
        ],
        "DON'T": [
            "Deploy local without cost analysis",
            "Mix model versions (use specific tags)",
            "Run production on laptop/desktop",
            "Forget about GPU memory limits"
        ]
    },
    
    "monitoring": {
        "DO": [
            "Track costs per agent and model",
            "Monitor latency percentiles (P95, P99)",
            "Set alerts for budget overruns",
            "Log all routing decisions"
        ],
        "DON'T": [
            "Deploy without monitoring",
            "Only track averages (misleading)",
            "Ignore error rates",
            "Wait for users to report issues"
        ]
    }
}

def print_guidelines():
    for category, guidelines in INFRASTRUCTURE_GUIDELINES.items():
        print(f"\n{'='*60}")
        print(f"{category.upper()} BEST PRACTICES")
        print('='*60)
        
        print("\n✅ DO:")
        for item in guidelines["DO"]:
            print(f"   • {item}")
        
        print("\n❌ DON'T:")
        for item in guidelines["DON'T"]:
            print(f"   • {item}")

print_guidelines()
```

---

## Summary: What We Built

**Starting Point:**
- 3 agents, all using GPT-4
- Cost: $30/day ($900/month)
- No monitoring, no fallbacks, no flexibility

**Ending Point:**
- 3 agents with optimized backends
- Cost: $9/day ($270/month) - **70% savings**
- Full routing infrastructure with fallbacks
- Comprehensive monitoring and cost tracking
- Production-ready architecture

**Key Achievements:**
1. ✅ Set up LiteLLM routing gateway
2. ✅ Deployed local inference (Ollama)
3. ✅ Configured multi-backend routing
4. ✅ Implemented fallback chains
5. ✅ Added cost and performance monitoring
6. ✅ Optimized each agent independently
7. ✅ Designed production architecture

---

## Next Steps

**In the Lab, you'll:**
1. Set up your own routing infrastructure
2. Deploy at least one local backend
3. Build a multi-agent system with 4+ agents
4. Implement intelligent routing for each agent
5. Monitor and optimize costs
6. Compare against a naive baseline

**Remember:** The goal isn't to make everything cheap - it's to use the right tool for each job!
