# Module 11: Infrastructure for Multi-Agent Systems
## Lab - Independent Application

**Assignment Title:** Build Production Infrastructure for an Automated Data Analysis Platform

**Scenario:** You're building an automated data analysis service that helps business analysts understand their data without writing code. The system receives datasets (CSV files) and natural language questions, then provides insights, visualizations recommendations, and summary reports.

**Current Challenge:** The prototype uses GPT-4 for everything and costs are unsustainable at scale. Your task is to build production infrastructure with intelligent routing to reduce costs by 60%+ while maintaining quality.

---

## System Requirements

### Functional Requirements

The system must have **4 agents minimum**:

1. **Data Profiler Agent**
   - Analyzes dataset structure (columns, types, distributions)
   - Identifies data quality issues
   - Suggests data cleaning steps
   - High volume (every dataset analyzed)

2. **Query Interpreter Agent**
   - Converts natural language to analysis plans
   - Determines which statistical methods to use
   - Plans visualization strategies
   - Medium volume (one per user question)

3. **Insight Generator Agent**
   - Performs statistical analysis
   - Identifies patterns and anomalies
   - Generates business insights
   - Medium volume, high complexity

4. **Report Writer Agent**
   - Creates executive summaries
   - Explains findings in business terms
   - Generates recommendations
   - Low volume, quality-critical

### Performance Requirements

- **Cost:** Maximum $20/day for 500 analysis requests
- **Latency:** Average response under 8 seconds
- **Availability:** 99% uptime (fallbacks required)
- **Quality:** Insights must be accurate and actionable

---

## Part 1: Infrastructure Design (30 points)

### Deliverable 1.1: Backend Selection Strategy

Create `backend_strategy.md` documenting your infrastructure choices:

#### Section 1: Agent-Backend Mapping

For EACH of your 4+ agents, document:

```markdown
### Agent: [Name]

**Role:** [What does this agent do?]

**Characteristics:**
- Expected calls per day: [Number]
- Task complexity: [Low/Medium/High]
- Token usage estimate: [Input tokens / Output tokens]
- Latency requirement: [<500ms / <2s / <5s / flexible]
- Quality requirement: [Adequate/Good/Excellent]

**Selected Backend:** [Specific model and provider]

**Cost Calculation:**
- Token cost: [Tokens per call] × [$X per 1K tokens] = [$X per call]
- Daily cost: [Calls/day] × [$X per call] = [$X/day]

**Rationale:**
[Why this backend? Why not alternatives? What trade-offs?]

**Fallback Chain:**
1. Primary: [model]
2. Fallback 1: [model]
3. Emergency: [model]

**Justification for fallbacks:**
[Why these specific models in this order?]
```

**Requirements:**
- Total daily cost must be under $20
- At least ONE agent must use local infrastructure
- At least ONE agent must use cloud premium (Claude or GPT-4)
- At least ONE agent must use cloud budget (Groq, OpenRouter free)
- All agents must have fallback chains

---

#### Section 2: Infrastructure Architecture Diagram

Create a diagram showing:
```
┌─────────────────────────────────────────┐
│   Data Analysis Multi-Agent System      │
└─────────────────────────────────────────┘

          ↓ User Request

┌─────────────────────────────────────────┐
│         LiteLLM Gateway                 │
│         (localhost:4000)                │
└─────────────────────────────────────────┘
          ↓
    ┌─────┴─────┬─────────┬─────────┐
    ↓           ↓         ↓         ↓

[Local Tier] [Budget Cloud] [Premium Cloud] [Fallbacks]
  Ollama      Groq         Claude        [Chain]
  vLLM        OpenRouter   GPT-4
  
          ↓
    
[Your 4+ Agents with routing logic]

[Data flow between agents]
```

**Requirements:**
- Show all backends you're deploying
- Indicate which agents use which backends
- Show fallback paths
- Include latency estimates for each tier

---

#### Section 3: Cost-Benefit Analysis

**Complete this table:**

| Agent | Backend | Calls/Day | Cost/Call | Daily Cost | % of Budget |
|-------|---------|-----------|-----------|------------|-------------|
| Agent 1 | [model] | [number] | $[X] | $[Y] | [Z]% |
| Agent 2 | [model] | [number] | $[X] | $[Y] | [Z]% |
| Agent 3 | [model] | [number] | $[X] | $[Y] | [Z]% |
| Agent 4 | [model] | [number] | $[X] | $[Y] | [Z]% |
| **TOTAL** | - | **[sum]** | - | **$[total]** | **100%** |

**Requirements:**
- Total must be under $20/day
- Show calculations
- Identify most expensive agent

**Compare to Naive Baseline:**
```
Naive approach (all GPT-4):
- 500 requests/day
- 4 agents per request
- ~2000 tokens per agent
- Cost: 500 × 4 × (2000/1000) × $0.03 = $[calculate]

Your optimized approach:
- Total daily cost: $[from table above]
- Savings: $[difference]
- Percentage reduction: [%]
```

---

## Part 2: Infrastructure Implementation (40 points)

### Deliverable 2.1: LiteLLM Configuration

Create `litellm_config.yaml`:

```yaml
model_list:
  # TODO: Add ALL your backend configurations
  
  # Example cloud model
  - model_name: your-premium-model
    litellm_params:
      model: claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY
      
  # Example local model
  - model_name: your-local-model
    litellm_params:
      model: ollama/llama3.2
      api_base: http://localhost:11434
      
  # TODO: Add at least 4 different backends total

router_settings:
  routing_strategy: simple-shuffle  # or custom
  num_retries: 3
  timeout: 30
  allowed_fails: 2
  
# TODO: Configure fallbacks
fallbacks:
  - model: your-primary-model
    fallback_models:
      - your-fallback-1
      - your-fallback-2
```

**Requirements:**
- Minimum 4 different backends configured
- At least 1 local backend (Ollama or vLLM)
- At least 2 cloud backends
- Fallback chains for critical agents
- Valid API keys (use environment variables)

---

### Deliverable 2.2: Local Inference Setup

Create `local_setup.sh`:

```bash
#!/bin/bash

# local_setup.sh - Script to set up local inference

echo "🚀 Setting up local inference infrastructure"
echo "============================================="

# TODO: Install Ollama (if not installed)
# Check if ollama is already installed

# TODO: Pull required models
# Example: ollama pull llama3.2

# TODO: Start Ollama service
# Example: ollama serve &

# TODO: Wait for Ollama to be ready
# Check http://localhost:11434/api/tags

# TODO: Verify models are loaded
# curl http://localhost:11434/api/tags

# TODO: Optional - Set up vLLM (if using)
# Requires GPU and specific setup

echo "✅ Local inference setup complete"
```

**Requirements:**
- Functional setup script
- Installs/configures at least Ollama
- Includes verification steps
- Documented with comments

**Testing Script** - Create `test_local.py`:

```python
# test_local.py
import requests
import time

def test_ollama():
    """Test Ollama is running and responsive"""
    
    print("🧪 Testing Ollama...")
    
    try:
        # Check if service is running
        response = requests.get("http://localhost:11434/api/tags")
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama is running with {len(models)} models")
            
            for model in models:
                print(f"   • {model['name']}")
            
            # Test inference
            test_prompt = "Say 'hello' in one word"
            inference_response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": models[0]['name'],
                    "prompt": test_prompt,
                    "stream": False
                }
            )
            
            if inference_response.status_code == 200:
                print(f"✅ Inference test passed")
                return True
        else:
            print(f"❌ Ollama returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama - is it running?")
        print("   Start it with: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_ollama()
    exit(0 if success else 1)
```

---

### Deliverable 2.3: Agent Implementation

Create `agents.py`:

```python
# agents.py
from crewai import Agent
import os

# LiteLLM gateway URL
GATEWAY_URL = "http://localhost:4000/v1"

def create_data_profiler_agent():
    """
    Creates agent for analyzing dataset structure.
    
    Backend choice: [YOUR CHOICE]
    Reasoning: [WHY THIS BACKEND?]
    """
    return Agent(
        role="Data Profiler",
        goal="Analyze dataset structure and quality",
        backstory="""You are a data quality expert who quickly 
        assesses datasets for structure, types, and issues.""",
        llm_config={
            "config_list": [{
                "model": "YOUR-MODEL-HERE",  # TODO: Fill in
                "base_url": GATEWAY_URL,
                "api_key": "dummy",
                "temperature": 0.1  # Why this temperature?
            }]
        },
        verbose=True
    )

def create_query_interpreter_agent():
    """
    Creates agent for converting NL queries to analysis plans.
    
    Backend choice: [YOUR CHOICE]
    Reasoning: [WHY THIS BACKEND?]
    """
    # TODO: Implement
    pass

def create_insight_generator_agent():
    """
    Creates agent for generating business insights.
    
    Backend choice: [YOUR CHOICE]
    Reasoning: [WHY THIS BACKEND?]
    """
    # TODO: Implement
    pass

def create_report_writer_agent():
    """
    Creates agent for writing executive summaries.
    
    Backend choice: [YOUR CHOICE]
    Reasoning: [WHY THIS BACKEND?]
    """
    # TODO: Implement
    pass

# TODO: Create at least 4 agents total
# Each with appropriate backend selection
```

**Requirements:**
- Implement minimum 4 agents
- Each has clear role and goal
- Each has justified backend selection
- Each has appropriate temperature setting
- All agents route through LiteLLM gateway

---

### Deliverable 2.4: Routing and Fallback Logic

Create `routing.py`:

```python
# routing.py
from litellm import completion
import time
from typing import Dict, List, Optional

class SmartRouter:
    """
    Intelligent routing with fallback support for multi-agent system.
    """
    
    def __init__(self):
        self.fallback_chains = {
            "data-profiler": {
                "primary": "your-model",
                "fallbacks": ["fallback-1", "fallback-2"]
            },
            # TODO: Add fallback chains for all agents
        }
    
    def route_with_fallback(self, agent_name: str, messages: List[Dict], 
                           max_tokens: int = 500) -> Dict:
        """
        Route request with automatic fallback on failure.
        
        Args:
            agent_name: Which agent is making the request
            messages: Chat messages
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dict with response, model used, latency, and success status
        """
        
        if agent_name not in self.fallback_chains:
            raise ValueError(f"Unknown agent: {agent_name}")
        
        chain = self.fallback_chains[agent_name]
        models = [chain["primary"]] + chain["fallbacks"]
        
        # TODO: Implement fallback logic
        # Try each model in sequence
        # Track which model succeeded
        # Return response with metadata
        
        for i, model in enumerate(models):
            try:
                # TODO: Make request
                # TODO: Track latency
                # TODO: Return on success
                pass
            except Exception as e:
                # TODO: Log failure
                # TODO: Try next model
                pass
        
        raise Exception(f"All models failed for {agent_name}")
    
    def get_routing_stats(self) -> Dict:
        """Return statistics about routing decisions"""
        # TODO: Track which models are used most
        # TODO: Track fallback frequency
        # TODO: Track failure rates
        pass

# TODO: Implement the router
# Should handle failures gracefully
# Should track metrics
```

**Requirements:**
- Implement complete fallback logic
- Try all models in chain before failing
- Track which model actually handled request
- Collect statistics on routing decisions

---

### Deliverable 2.5: Cost and Performance Monitoring

Create `monitoring.py`:

```python
# monitoring.py
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
import json

@dataclass
class RequestMetrics:
    """Metrics for a single LLM request"""
    timestamp: datetime
    agent_name: str
    model_used: str
    primary_model: str  # What we tried first
    fallback_occurred: bool
    input_tokens: int
    output_tokens: int
    latency_ms: float
    cost_usd: float
    success: bool

class PerformanceMonitor:
    """Track costs, latency, and routing decisions"""
    
    # TODO: Add pricing for your models
    PRICING = {
        "gpt-4": 0.03,
        "claude-sonnet": 0.015,
        "groq-fast": 0.0005,
        "local-model": 0.0,
    }
    
    def __init__(self):
        self.requests: List[RequestMetrics] = []
    
    def record_request(self, agent_name: str, model_used: str, 
                      primary_model: str, input_tokens: int, 
                      output_tokens: int, latency_ms: float, 
                      success: bool = True):
        """Record metrics for a request"""
        
        # Calculate cost
        total_tokens = input_tokens + output_tokens
        cost = (total_tokens / 1000) * self.PRICING.get(model_used, 0)
        
        # Determine if fallback occurred
        fallback = (model_used != primary_model)
        
        metrics = RequestMetrics(
            timestamp=datetime.now(),
            agent_name=agent_name,
            model_used=model_used,
            primary_model=primary_model,
            fallback_occurred=fallback,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            cost_usd=cost,
            success=success
        )
        
        self.requests.append(metrics)
    
    def get_summary(self) -> Dict:
        """Generate comprehensive summary"""
        
        if not self.requests:
            return {"error": "No requests recorded"}
        
        # TODO: Calculate summary statistics
        # - Total cost
        # - Cost by agent
        # - Cost by model
        # - Average latency
        # - Fallback rate
        # - Success rate
        # - Daily projection
        
        pass
    
    def print_report(self):
        """Print formatted performance report"""
        
        summary = self.get_summary()
        
        print("\n" + "="*70)
        print("PERFORMANCE & COST REPORT")
        print("="*70)
        
        # TODO: Print formatted report
        # Include all key metrics
        # Compare to budget
        # Highlight issues (over budget, high latency, failures)
        
        pass
    
    def check_budget_compliance(self, daily_budget: float = 20.0):
        """Check if system is within budget"""
        
        # TODO: Calculate daily cost projection
        # TODO: Compare to budget
        # TODO: Return compliance status and warnings
        
        pass
    
    def export_metrics(self, filename: str = "metrics.json"):
        """Export detailed metrics to JSON"""
        # TODO: Export all request data
        # TODO: Include summary
        pass

# Global monitor instance
monitor = PerformanceMonitor()
```

**Requirements:**
- Track all required metrics
- Calculate costs accurately
- Check budget compliance
- Generate readable reports
- Export data for analysis

---

## Part 3: System Testing and Analysis (40 points)

### Deliverable 3.1: Complete Working System

Create `main.py`:

```python
# main.py
import time
from agents import (
    create_data_profiler_agent,
    create_query_interpreter_agent,
    create_insight_generator_agent,
    create_report_writer_agent
)
from routing import SmartRouter
from monitoring import monitor
from crewai import Task, Crew

def create_analysis_workflow(dataset_info: str, user_question: str):
    """
    Create tasks for data analysis workflow.
    
    Args:
        dataset_info: Description of the dataset
        user_question: User's natural language question
    """
    
    # TODO: Create tasks for each agent
    # Task 1: Profile the dataset
    # Task 2: Interpret the user's question
    # Task 3: Generate insights
    # Task 4: Write summary report
    
    # TODO: Set up proper dependencies (context)
    
    pass

def run_analysis(dataset_info: str, user_question: str):
    """Run complete analysis workflow"""
    
    print(f"\n🔬 Analyzing dataset...")
    print(f"📊 Dataset: {dataset_info}")
    print(f"❓ Question: {user_question}")
    print("="*70)
    
    start_time = time.time()
    
    # TODO: Create agents
    # TODO: Create crew
    # TODO: Run analysis
    # TODO: Track metrics
    
    total_time = time.time() - start_time
    
    print(f"\n✅ Analysis complete!")
    print(f"   Total time: {total_time:.1f}s")
    
    # Print performance report
    monitor.print_report()
    
    # Check budget compliance
    monitor.check_budget_compliance(daily_budget=20.0)

def run_load_test(num_requests: int = 50):
    """Simulate production load"""
    
    print(f"\n🚀 Running load test with {num_requests} requests...")
    print("="*70)
    
    # Sample datasets and questions
    test_cases = [
        ("sales_data.csv (50k rows)", "What are our top selling products?"),
        ("customer_churn.csv (10k rows)", "Which factors predict churn?"),
        ("marketing_campaigns.csv (5k rows)", "Which campaigns had best ROI?"),
        # TODO: Add more test cases
    ]
    
    for i in range(num_requests):
        case = test_cases[i % len(test_cases)]
        print(f"\n[{i+1}/{num_requests}] Processing request...")
        
        try:
            run_analysis(case[0], case[1])
        except Exception as e:
            print(f"❌ Request {i+1} failed: {e}")
    
    # Final summary
    print("\n" + "="*70)
    print("LOAD TEST SUMMARY")
    print("="*70)
    
    monitor.print_report()
    
    # Export results
    monitor.export_metrics(f"load_test_{num_requests}_requests.json")

if __name__ == "__main__":
    # Run single analysis
    run_analysis(
        dataset_info="sales_data.csv with 50,000 rows (date, product, revenue, region)",
        user_question="What products had the highest revenue growth in Q4?"
    )
    
    # Run load test to simulate production
    run_load_test(num_requests=50)
```

**Requirements:**
- Complete end-to-end workflow
- Proper task dependencies
- Comprehensive error handling
- Metrics collection throughout
- Load testing capability

---

### Deliverable 3.2: Performance Analysis

Create `analysis.md`:

#### Section 1: Cost Analysis

**Daily Cost Breakdown:**

| Metric | Value |
|--------|-------|
| Test requests processed | [number] |
| Total cost for test | $[X] |
| Projected daily cost (500 requests) | $[Y] |
| Budget limit | $20.00 |
| Budget compliance | ✅/❌ |
| Cost per request | $[Z] |

**Cost by Agent:**

| Agent | Requests | Model Used | Cost | % of Total |
|-------|----------|------------|------|------------|
| Agent 1 | [num] | [model] | $[X] | [Y]% |
| Agent 2 | [num] | [model] | $[X] | [Y]% |
| Agent 3 | [num] | [model] | $[X] | [Y]% |
| Agent 4 | [num] | [model] | $[X] | [Y]% |

**Cost by Model:**

| Model | Requests | Total Cost | % of Total |
|-------|----------|------------|------------|
| [model] | [num] | $[X] | [Y]% |

**Analysis Questions:**

1. Which agent contributes most to costs? Why?
2. Are any agents over-provisioned (expensive model for simple task)?
3. Could any agents be moved to cheaper backends without quality loss?
4. What's your most expensive model? Is it justified?

---

#### Section 2: Latency Analysis

**Latency Breakdown:**

| Stage | Agent | Avg Latency | P95 Latency | Max Latency |
|-------|-------|-------------|-------------|-------------|
| 1 | [agent] | [X]ms | [Y]ms | [Z]ms |
| 2 | [agent] | [X]ms | [Y]ms | [Z]ms |
| 3 | [agent] | [X]ms | [Y]ms | [Z]ms |
| 4 | [agent] | [X]ms | [Y]ms | [Z]ms |
| **Total Pipeline** | - | **[X]ms** | **[Y]ms** | **[Z]ms** |

**Analysis Questions:**

1. What's the slowest agent in your pipeline?
2. Does average latency meet the 8-second requirement?
3. Are P95/P99 latencies acceptable?
4. Which agents could be parallelized to reduce total latency?
5. How does local vs. cloud affect latency?

---

#### Section 3: Fallback Analysis

**Fallback Statistics:**

| Agent | Total Requests | Primary Success | Fallback Used | Fallback Rate |
|-------|---------------|-----------------|---------------|---------------|
| [agent] | [num] | [num] | [num] | [X]% |

**Analysis Questions:**

1. Did any fallbacks trigger during testing?
2. Which agent had highest fallback rate?
3. Are fallback chains configured correctly?
4. What would happen if primary AND fallback failed?

---

#### Section 4: Comparison to Naive Baseline

**Create comparison table:**

| Metric | Naive (All GPT-4) | Optimized (Your System) | Improvement |
|--------|-------------------|-------------------------|-------------|
| Cost per request | $[X] | $[Y] | [Z]% reduction |
| Daily cost (500 req) | $[X] | $[Y] | $[savings] saved |
| Monthly cost | $[X] | $[Y] | $[savings] saved |
| Average latency | [X]ms | [Y]ms | [Z]% faster/slower |

**Calculate naive baseline:**
```
Assumptions:
- 4 agents per request
- 2000 tokens per agent (1000 input + 1000 output)
- GPT-4 pricing: $0.03 per 1K tokens

Cost per request:
= 4 agents × 2000 tokens × ($0.03 / 1000)
= 4 × 2 × $0.03
= $0.24

Daily cost (500 requests):
= $0.24 × 500
= $120/day

Monthly cost:
= $120 × 30
= $3,600/month
```

**Your optimized system:**
```
Cost per request: $[from your testing]
Daily cost: $[your cost] 
Monthly cost: $[your cost × 30]

Savings: $[baseline - optimized]
Percentage: [savings / baseline × 100]%
```

---

### Deliverable 3.3: Optimization Recommendations

**Provide 3-5 specific optimization ideas:**

```markdown
### Optimization 1: [Title]

**Current State:**
[What's the situation now?]

**Proposed Change:**
[What would you change?]

**Expected Impact:**
- Cost: [Increase/Decrease] by [X]%
- Latency: [Better/Worse] by [X]ms
- Quality: [Impact on quality]

**Implementation Complexity:** [Low/Medium/High]

**Should implement?** [Yes/No - justify]

---

### Optimization 2: [Title]

[Repeat structure]
```

**Example Optimization Ideas:**
- Move additional agent to local infrastructure
- Implement response caching for repeated queries
- Use async parallel execution for independent agents
- Add request batching
- Implement dynamic routing based on query complexity

---

## Part 4: Deployment and Documentation (20 points)

### Deliverable 4.1: Setup Instructions

Create `README.md`:

```markdown
# Data Analysis Platform Infrastructure

## Overview
[Brief description of your system]

## Architecture
[Include your architecture diagram]

## Prerequisites
- Docker Desktop
- Python 3.10+
- 8GB+ RAM
- API keys for: [list required keys]

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Start Local Infrastructure
```bash
./local_setup.sh
```

### 4. Start LiteLLM Gateway
```bash
litellm --config litellm_config.yaml --port 4000
```

### 5. Run Tests
```bash
python test_local.py
python main.py
```

## Usage

### Run Single Analysis
```bash
python main.py
```

### Run Load Test
```bash
python main.py --load-test --requests 50
```

## Monitoring

Access LiteLLM dashboard at: http://localhost:4000/ui

View metrics: `python -m monitoring --report`

## Troubleshooting

### Ollama Not Starting
[Solutions]

### API Key Errors
[Solutions]

### High Latency
[Solutions]

## Cost Monitoring

Budget: $20/day
Current: Check `python -m monitoring --budget`

## Performance Benchmarks

[Your actual benchmark results]
```

**Requirements:**
- Clear, step-by-step instructions
- Complete prerequisites list
- Troubleshooting section
- Actual performance data

---

### Deliverable 4.2: Requirements File

Create `requirements.txt`:

```
crewai>=0.1.0
litellm>=1.0.0
openai>=1.0.0
anthropic>=0.8.0
ollama>=0.1.0
requests>=2.31.0
python-dotenv>=1.0.0
pydantic>=2.0.0
# Add all other dependencies
```

---

### Deliverable 4.3: Environment Template

Create `.env.example`:

```bash
# API Keys (get from respective providers)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GROQ_API_KEY=gsk_...

# Optional
OPENROUTER_API_KEY=sk-or-...

# Local Infrastructure
OLLAMA_BASE_URL=http://localhost:11434
VLLM_BASE_URL=http://localhost:8000

# LiteLLM Settings
LITELLM_PORT=4000
LITELLM_LOG=INFO

# Monitoring
ENABLE_MONITORING=true
METRICS_EXPORT_PATH=./metrics/
```

---

## Submission Requirements

### Required Files

```
infrastructure_lab/
├── README.md                    # Setup and usage instructions
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── backend_strategy.md          # Part 1: Design document
├── litellm_config.yaml          # Part 2.1: LiteLLM config
├── local_setup.sh               # Part 2.2: Local setup
├── test_local.py                # Part 2.2: Local testing
├── agents.py                    # Part 2.3: Agent definitions
├── routing.py                   # Part 2.4: Routing logic
├── monitoring.py                # Part 2.5: Metrics tracking
├── main.py                      # Part 3.1: Main application
├── analysis.md                  # Part 3.2: Performance analysis
├── load_test_results.json       # Generated by testing
└── architecture_diagram.png     # System diagram
```

### Submission Checklist

- [ ] All 13+ files included
- [ ] Code runs without errors
- [ ] Infrastructure successfully deploys
- [ ] Load test completes successfully
- [ ] Cost analysis shows <$20/day
- [ ] At least 4 agents implemented
- [ ] At least 1 local backend deployed
- [ ] Fallback chains implemented
- [ ] Monitoring and metrics working
- [ ] README has complete instructions
- [ ] Analysis answers all questions

---

## Grading Rubric (200 points)

### Part 1: Design (30 points)
- [ ] Agent-backend mapping complete and justified (15 pts)
- [ ] Architecture diagram clear and accurate (8 pts)
- [ ] Cost analysis under budget with calculations (7 pts)

### Part 2: Implementation (40 points)
- [ ] LiteLLM configured correctly (8 pts)
- [ ] Local infrastructure deploys successfully (8 pts)
- [ ] All 4+ agents implemented with justification (10 pts)
- [ ] Routing with fallbacks functional (8 pts)
- [ ] Monitoring tracks all metrics (6 pts)

### Part 3: Testing & Analysis (40 points)
- [ ] Complete working system (10 pts)
- [ ] Load test runs successfully (10 pts)
- [ ] Cost analysis accurate and complete (10 pts)
- [ ] Performance analysis thorough (10 pts)

### Part 4: Documentation (20 points)
- [ ] README clear and complete (10 pts)
- [ ] All setup files included (5 pts)
- [ ] System actually works per instructions (5 pts)

### Code Quality (20 points)
- [ ] Code is well-documented (8 pts)
- [ ] Follows Python best practices (7 pts)
- [ ] Error handling implemented (5 pts)

### Infrastructure Understanding (50 points)
- [ ] Demonstrates understanding of routing concepts (15 pts)
- [ ] Appropriate backend selection decisions (15 pts)
- [ ] Successful deployment of local infrastructure (10 pts)
- [ ] Thoughtful optimization recommendations (10 pts)

**Total: 200 points**

---

## Success Criteria

Your lab is successful if:

✅ System processes 50+ requests in load test
✅ Daily cost projection is under $20
✅ Average latency is under 8 seconds  
✅ At least 1 local backend operational
✅ Fallbacks trigger correctly when tested
✅ Monitoring exports complete metrics
✅ Setup instructions work on fresh machine
✅ Shows 60%+ cost reduction vs. naive baseline

---

## Extension Challenges (Bonus Points)

### Challenge 1: Dynamic Routing (10 points)
Implement routing that adapts based on:
- Current API rate limits
- Time of day (use cheaper models during high-load hours)
- Remaining daily budget

### Challenge 2: Advanced Caching (10 points)
Implement intelligent caching:
- Cache similar queries (use embeddings for similarity)
- LRU cache with size limits
- Cache invalidation strategy
- Measure cache hit rate and cost savings

### Challenge 3: Multi-Model Consensus (15 points)
For critical analyses:
- Query 3 different models
- Compare responses
- Use a judge agent to select best answer
- Track consensus rate

### Challenge 4: Real-Time Dashboard (15 points)
Build a web dashboard showing:
- Live request rate
- Current costs vs. budget
- Agent latency distribution
- Fallback frequency
- Model usage distribution

---

## Common Pitfalls

❌ **Don't:** Use same model for all agents
✅ **Do:** Match backend to agent requirements

❌ **Don't:** Forget to start local infrastructure before LiteLLM
✅ **Do:** Start services in correct order (Ollama → LiteLLM → Agents)

❌ **Don't:** Ignore fallback chains
✅ **Do:** Test that fallbacks actually work

❌ **Don't:** Use production API keys in code
✅ **Do:** Use environment variables

❌ **Don't:** Skip cost calculations
✅ **Do:** Track every penny to stay under budget

---

## Getting Started Tips

1. **Start with architecture** - Design before coding
   - Spend 2-3 hours on Part 1 (design)
   - Calculate costs before implementing
   
2. **Deploy infrastructure incrementally**
   - Get Ollama working first
   - Then LiteLLM
   - Then one agent at a time

3. **Test continuously**
   - Test local infrastructure immediately
   - Test each agent as you build it
   - Don't wait until the end

4. **Monitor from the beginning**
   - Implement monitoring early
   - Track costs from first request
   - Don't optimize blindly

5. **Budget is non-negotiable**
   - If over budget, redesign
   - Don't sacrifice functionality - optimize routing

---

## Resources

- LiteLLM Docs: https://docs.litellm.ai/
- Ollama Docs: https://ollama.ai/
- CrewAI Docs: https://docs.crewai.com/
- Your glossary and demo from this module

---

## Questions?

If stuck, check:
1. Is local infrastructure actually running? (test_local.py)
2. Is LiteLLM gateway accessible? (curl localhost:4000/health)
3. Are agents configured with correct model names?
4. Are fallback chains defined for all critical agents?
5. Is monitoring recording all requests?

**Due Date:** [Instructor will announce]

**Submit to:** [Platform TBD]

Good luck building production-grade infrastructure! 🚀
