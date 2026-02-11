# Module 12: Evaluation & Observability
## Lab - Independent Application (Take-Home Assignment)

**Module Title:** Evaluation & Observability - Independent Lab  
**Duration:** 90-120 Minutes (Take-Home)  
**Goal:** Build a complete evaluation and observability system for a production-ready AI agent.

---

## Lab Overview

### The Challenge

You will evaluate and optimize a **Financial Research Agent** that analyzes company earnings reports and generates investment summaries. This agent must be accurate, fast, and cost-effective.

### What Makes This Different from the Demo

| Demo | Lab |
|------|-----|
| Newsletter Agent | Financial Research Agent |
| General AI news | Specific company financials |
| Subjective quality | Objective accuracy required |
| Competitor mentions | Factual hallucinations |
| Brand tone | Regulatory compliance |

**The Variation:** You must define what "good" means for financial research, create domain-specific evaluations, and ensure the agent doesn't hallucinate numbers or make unsupported claims.

---

## Pre-Lab Setup (20 minutes)

### 1. Environment Configuration

#### Install Required Packages

```bash
pip install langfuse anthropic python-dotenv pandas pydantic requests beautifulsoup4
```

#### Create Your `.env` File

Create a file named `.env` in your project directory:

```env
# .env - NEVER commit this file to git!

# Anthropic API
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Langfuse (sign up at https://cloud.langfuse.com)
LANGFUSE_PUBLIC_KEY=pk-lf-your-key-here
LANGFUSE_SECRET_KEY=sk-lf-your-key-here
LANGFUSE_HOST=https://cloud.langfuse.com

# Optional: OpenRouter for model comparisons
OPENROUTER_API_KEY=sk-or-your-key-here
```

#### Verify Setup

```python
import os
from dotenv import load_dotenv
from langfuse import get_client

load_dotenv(override=True)

# Check environment variables
required_vars = ["ANTHROPIC_API_KEY", "LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"]
for var in required_vars:
    if not os.getenv(var):
        print(f"❌ Missing: {var}")
    else:
        print(f"✓ Found: {var}")

# Verify Langfuse connection
langfuse = get_client()
if langfuse.auth_check():
    print("✓ Langfuse authenticated successfully")
else:
    print("❌ Langfuse authentication failed")
```

**Pass Criterion:** All checks show ✓ before proceeding.

---

### 2. Download the Financial Research Agent

```python
# financial_agent.py (provided as starter code)

import anthropic
import os
from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class ResearchResult:
    """Results from financial research"""
    company: str
    summary: str
    key_metrics: Dict[str, float]
    recommendation: str
    confidence: float
    sources: List[str]
    token_count: int
    cost: float

class FinancialResearchAgent:
    """
    Agent that analyzes company financial data and generates summaries.
    
    NOTE: This agent has intentional bugs for you to find!
    """
    
    def __init__(self, api_key: str, enable_tracing: bool = True):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.enable_tracing = enable_tracing
        self.model = "claude-sonnet-4-20250514"
    
    def analyze_company(self, company: str, financial_data: str) -> ResearchResult:
        """
        Analyze a company based on financial data.
        
        Args:
            company: Company name
            financial_data: Raw financial data (e.g., earnings report text)
        
        Returns:
            ResearchResult with analysis
        """
        
        system_prompt = """
You are a financial analyst creating investment summaries.

Analyze the provided financial data and generate:
1. A brief summary (2-3 sentences)
2. Key financial metrics (revenue, profit, growth rate, etc.)
3. An investment recommendation (Buy/Hold/Sell)
4. Confidence level (0.0 to 1.0)

Be factual and cite specific numbers from the data.
"""
        
        user_prompt = f"""
Company: {company}

Financial Data:
{financial_data}

Provide your analysis in JSON format:
{{
    "summary": "Brief 2-3 sentence summary",
    "key_metrics": {{
        "revenue": <number>,
        "profit": <number>,
        "growth_rate": <number>
    }},
    "recommendation": "Buy|Hold|Sell",
    "confidence": <0.0-1.0>
}}
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        # Parse response
        response_text = response.content[0].text
        
        # Extract JSON (may be wrapped in markdown)
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            json_text = response_text[json_start:json_end].strip()
        else:
            json_text = response_text
        
        data = json.loads(json_text)
        
        # Calculate cost (Claude Sonnet 4.5 pricing)
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        cost = (input_tokens * 0.000003) + (output_tokens * 0.000015)
        
        return ResearchResult(
            company=company,
            summary=data["summary"],
            key_metrics=data["key_metrics"],
            recommendation=data["recommendation"],
            confidence=data["confidence"],
            sources=[],  # TODO: Extract sources
            token_count=input_tokens + output_tokens,
            cost=cost
        )
```

---

## Part 1: Build Objective Evaluations (30 minutes)

### Task 1.1: Factual Accuracy Check

**Goal:** Verify that the agent doesn't hallucinate numbers.

**Create:** `eval_factual_accuracy.py`

```python
def eval_factual_accuracy(
    result: ResearchResult, 
    ground_truth: Dict[str, float]
) -> dict:
    """
    Check if reported metrics match ground truth data.
    
    Args:
        result: Agent's output
        ground_truth: Verified correct values
    
    Returns:
        Evaluation result with passed/failed and details
    """
    
    # TODO: Implement this function
    # 
    # Requirements:
    # 1. Compare each metric in result.key_metrics to ground_truth
    # 2. Allow 5% tolerance for rounding differences
    # 3. Return dict with:
    #    - "passed": bool
    #    - "accuracy_score": float (0.0-1.0)
    #    - "incorrect_metrics": list of metric names that failed
    #    - "details": human-readable explanation
    
    pass  # Your code here

# Example test case
ground_truth = {
    "revenue": 50000000000,  # $50B
    "profit": 5000000000,    # $5B
    "growth_rate": 0.15      # 15%
}

# Test with correct data
correct_result = ResearchResult(
    company="TestCorp",
    summary="Good performance",
    key_metrics={"revenue": 50.1e9, "profit": 5.0e9, "growth_rate": 0.15},
    recommendation="Buy",
    confidence=0.8,
    sources=[],
    token_count=500,
    cost=0.01
)

eval_result = eval_factual_accuracy(correct_result, ground_truth)
print(f"Should pass: {eval_result['passed']}")

# Test with incorrect data (hallucination)
hallucinated_result = ResearchResult(
    company="TestCorp",
    summary="Good performance",
    key_metrics={"revenue": 75e9, "profit": 10e9, "growth_rate": 0.25},  # WRONG!
    recommendation="Buy",
    confidence=0.8,
    sources=[],
    token_count=500,
    cost=0.01
)

eval_result = eval_factual_accuracy(hallucinated_result, ground_truth)
print(f"Should fail: {eval_result['passed']}")
print(f"Incorrect metrics: {eval_result['incorrect_metrics']}")
```

---

### Task 1.2: Output Format Validation

**Goal:** Ensure the agent returns valid, complete data.

```python
def eval_output_format(result: ResearchResult) -> dict:
    """
    Validate that the output has all required fields with correct types.
    
    Requirements:
    1. All fields are present (not None)
    2. summary is non-empty string
    3. key_metrics has at least 3 metrics
    4. recommendation is one of: Buy, Hold, Sell
    5. confidence is between 0.0 and 1.0
    
    Returns:
        Evaluation result with passed/failed and details
    """
    
    # TODO: Implement this function
    pass  # Your code here
```

---

### Task 1.3: Cost & Latency Limits

**Goal:** Ensure the agent operates within budget and performance constraints.

```python
def eval_efficiency(result: ResearchResult, max_cost: float = 0.05, max_tokens: int = 5000) -> dict:
    """
    Check if the agent stayed within cost and token budgets.
    
    Args:
        result: Agent's output
        max_cost: Maximum allowed cost per request in dollars
        max_tokens: Maximum allowed tokens per request
    
    Returns:
        Evaluation result with passed/failed and details
    """
    
    # TODO: Implement this function
    #
    # Should check:
    # 1. result.cost <= max_cost
    # 2. result.token_count <= max_tokens
    # 3. Return both individual results and combined pass/fail
    
    pass  # Your code here
```

---

## Part 2: Build Subjective Evaluations (25 minutes)

### Task 2.1: Summary Quality (LLM-as-Judge)

**Goal:** Use Claude to evaluate the quality of the investment summary.

```python
def eval_summary_quality(result: ResearchResult, financial_data: str, api_key: str) -> dict:
    """
    Use Claude as a judge to evaluate summary quality.
    
    Criteria:
    1. Accuracy - Does it reflect the data?
    2. Clarity - Is it easy to understand?
    3. Completeness - Does it cover key points?
    4. Professional tone - Appropriate for investors?
    
    Returns:
        Evaluation with score (0-5) and reasoning
    """
    
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    
    judge_prompt = f"""
You are evaluating an investment summary for quality.

Financial Data:
{financial_data}

Generated Summary:
{result.summary}

Evaluate on these criteria (rate each 0-5):
1. ACCURACY: Does the summary accurately reflect the financial data?
2. CLARITY: Is it clear and easy to understand?
3. COMPLETENESS: Does it cover the most important points?
4. TONE: Is the tone professional and appropriate for investors?

Respond in JSON:
{{
    "accuracy_score": <0-5>,
    "clarity_score": <0-5>,
    "completeness_score": <0-5>,
    "tone_score": <0-5>,
    "overall_score": <average of above>,
    "reasoning": "<explain your scores>",
    "strengths": "<what was good>",
    "improvements": "<what could be better>"
}}
"""
    
    # TODO: Complete the implementation
    # 1. Call Claude API with judge_prompt
    # 2. Parse the JSON response
    # 3. Return formatted result with "passed" (overall_score >= 3.0)
    
    pass  # Your code here
```

---

### Task 2.2: Recommendation Justification

**Goal:** Verify that the investment recommendation is supported by the data.

```python
def eval_recommendation_justification(result: ResearchResult, financial_data: str, api_key: str) -> dict:
    """
    Use Claude to check if the recommendation is well-justified.
    
    For example:
    - "Buy" recommendation should cite positive metrics
    - "Sell" recommendation should cite negative metrics
    - Confidence should match the strength of evidence
    
    Returns:
        Evaluation with justified (bool) and reasoning
    """
    
    # TODO: Implement this evaluation
    # Similar to eval_summary_quality but focused on recommendation logic
    
    pass  # Your code here
```

---

## Part 3: Implement Tracing & Monitoring (20 minutes)

### Task 3.1: Instrument the Agent

Modify `financial_agent.py` to include Langfuse tracing:

```python
from langfuse.decorators import observe, langfuse_context

class FinancialResearchAgent:
    # ... existing code ...
    
    @observe()  # Add this decorator
    def analyze_company(self, company: str, financial_data: str) -> ResearchResult:
        """Analyze a company based on financial data."""
        
        # Set useful metadata
        langfuse_context.update_current_observation(
            metadata={
                "company": company,
                "model": self.model,
                "data_length": len(financial_data)
            }
        )
        
        # ... rest of existing code ...
        
        # Before returning, log the result
        langfuse_context.update_current_observation(
            output={
                "recommendation": data["recommendation"],
                "confidence": data["confidence"],
                "cost": cost,
                "tokens": input_tokens + output_tokens
            }
        )
        
        return ResearchResult(...)
```

---

### Task 3.2: Run Evaluation Suite

Create a script that runs all evaluations and logs to Langfuse:

```python
# run_evaluation_suite.py

import os
from dotenv import load_dotenv
from financial_agent import FinancialResearchAgent, ResearchResult
from langfuse import Langfuse
import json

load_dotenv(override=True)

# Test cases
TEST_CASES = [
    {
        "company": "TechCorp Inc.",
        "financial_data": """
Q4 2024 Earnings Report - TechCorp Inc.
Revenue: $52.3 billion (up 18% YoY)
Net Profit: $6.1 billion (up 22% YoY)
Operating Margin: 28%
Guidance: Expecting 15-20% growth in 2025
""",
        "ground_truth": {
            "revenue": 52.3e9,
            "profit": 6.1e9,
            "growth_rate": 0.18
        }
    },
    {
        "company": "RetailCo",
        "financial_data": """
Q4 2024 Earnings Report - RetailCo
Revenue: $38.1 billion (down 5% YoY)
Net Profit: $1.2 billion (down 15% YoY)
Operating Margin: 12%
Guidance: Flat growth expected in 2025
""",
        "ground_truth": {
            "revenue": 38.1e9,
            "profit": 1.2e9,
            "growth_rate": -0.05
        }
    },
    # TODO: Add 3 more test cases covering different scenarios
]

def run_evaluation_suite():
    """Run the complete evaluation suite on all test cases."""
    
    agent = FinancialResearchAgent(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        enable_tracing=True
    )
    
    langfuse = Langfuse()
    
    results = []
    
    for i, test_case in enumerate(TEST_CASES):
        print(f"\n{'='*60}")
        print(f"Test Case {i+1}: {test_case['company']}")
        print(f"{'='*60}")
        
        # Run the agent
        result = agent.analyze_company(
            company=test_case["company"],
            financial_data=test_case["financial_data"]
        )
        
        # Run all evaluations
        evals = {
            "factual_accuracy": eval_factual_accuracy(result, test_case["ground_truth"]),
            "output_format": eval_output_format(result),
            "efficiency": eval_efficiency(result),
            "summary_quality": eval_summary_quality(result, test_case["financial_data"], os.getenv("ANTHROPIC_API_KEY")),
            "recommendation_justification": eval_recommendation_justification(result, test_case["financial_data"], os.getenv("ANTHROPIC_API_KEY"))
        }
        
        # Calculate overall pass rate
        passed_count = sum(1 for e in evals.values() if e.get("passed", False))
        total_count = len(evals)
        pass_rate = passed_count / total_count
        
        # Log to Langfuse
        trace = langfuse.trace(
            name=f"financial_research_{test_case['company']}",
            metadata={
                "company": test_case["company"],
                "pass_rate": pass_rate,
                "cost": result.cost,
                "tokens": result.token_count
            }
        )
        
        # Log each evaluation as a score
        for eval_name, eval_result in evals.items():
            trace.score(
                name=eval_name,
                value=1.0 if eval_result.get("passed", False) else 0.0,
                comment=eval_result.get("details", "")
            )
        
        # Store results
        results.append({
            "company": test_case["company"],
            "pass_rate": pass_rate,
            "cost": result.cost,
            "evals": evals,
            "result": result
        })
        
        # Print summary
        print(f"\nResults:")
        print(f"  Pass Rate: {pass_rate:.1%}")
        print(f"  Cost: ${result.cost:.4f}")
        print(f"  Recommendation: {result.recommendation} (confidence: {result.confidence:.2f})")
        
        for eval_name, eval_result in evals.items():
            status = "✓" if eval_result.get("passed", False) else "✗"
            print(f"  {status} {eval_name}")
    
    return results

if __name__ == "__main__":
    results = run_evaluation_suite()
    
    # Print final summary
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")
    
    avg_pass_rate = sum(r["pass_rate"] for r in results) / len(results)
    total_cost = sum(r["cost"] for r in results)
    
    print(f"Average Pass Rate: {avg_pass_rate:.1%}")
    print(f"Total Cost: ${total_cost:.4f}")
    print(f"Cost per Test: ${total_cost/len(results):.4f}")
    
    # Identify weakest evaluation
    eval_failures = {}
    for result in results:
        for eval_name, eval_result in result["evals"].items():
            if not eval_result.get("passed", False):
                eval_failures[eval_name] = eval_failures.get(eval_name, 0) + 1
    
    if eval_failures:
        print(f"\nMost Common Failures:")
        for eval_name, count in sorted(eval_failures.items(), key=lambda x: x[1], reverse=True):
            print(f"  {eval_name}: {count}/{len(results)} failures")
```

---

## Part 4: Error Analysis & Optimization (25 minutes)

### Task 4.1: Identify Issues

Run your evaluation suite and answer these questions in `analysis.md`:

```markdown
# Financial Research Agent - Error Analysis

## Evaluation Results

### Overall Performance
- Pass Rate: [X%]
- Average Cost: [$X]
- Most Common Failure: [evaluation name]

### Failed Test Cases
List each test case that failed any evaluation:

1. **[Company Name]**
   - Failed Evaluations: [list]
   - Root Cause: [your analysis]
   - Example Issue: [quote from output]

## Identified Bugs

### Bug 1: [Name]
- **Description:** [what's wrong]
- **Evidence:** [specific outputs showing the bug]
- **Impact:** [how it affects users]
- **Proposed Fix:** [how to fix it]

[Repeat for each bug found]

## Performance Bottlenecks

### Bottleneck 1: [Area]
- **Issue:** [description]
- **Impact:** [latency/cost increase]
- **Solution:** [optimization approach]

## Recommendations

Based on the evaluation results, I recommend:

1. [Specific improvement]
   - Reason: [why this matters]
   - Expected Impact: [quantify if possible]

2. [Another improvement]
   ...
```

---

### Task 4.2: Implement Fixes

Choose **at least 2 bugs or issues** you identified and fix them:

```python
# improved_financial_agent.py

class ImprovedFinancialResearchAgent(FinancialResearchAgent):
    """
    Improved version of the financial research agent with bug fixes.
    
    Improvements:
    1. [Bug fix 1 description]
    2. [Bug fix 2 description]
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add any new configuration
    
    def analyze_company(self, company: str, financial_data: str) -> ResearchResult:
        """
        Improved analysis with bug fixes.
        """
        
        # IMPROVED SYSTEM PROMPT
        system_prompt = """
You are a financial analyst creating investment summaries.

CRITICAL REQUIREMENTS:
1. ONLY cite numbers that appear in the provided financial data
2. Do NOT make up or estimate any financial figures
3. If a metric is not provided, set it to null in the JSON
4. Be conservative with confidence scores (0.6-0.8 for typical analyses)

[... rest of improved prompt ...]
"""
        
        # ... rest of implementation with fixes ...
```

---

### Task 4.3: Validate Improvements

Re-run your evaluation suite with the improved agent:

```python
# Compare original vs improved
original_results = run_evaluation_suite()  # Using FinancialResearchAgent
improved_results = run_evaluation_suite()  # Using ImprovedFinancialResearchAgent

# Generate comparison report
print("\n" + "="*60)
print("IMPROVEMENT COMPARISON")
print("="*60)

print(f"\nPass Rate:")
print(f"  Original: {avg_pass_rate_original:.1%}")
print(f"  Improved: {avg_pass_rate_improved:.1%}")
print(f"  Change: +{(avg_pass_rate_improved - avg_pass_rate_original):.1%}")

print(f"\nAverage Cost:")
print(f"  Original: ${avg_cost_original:.4f}")
print(f"  Improved: ${avg_cost_improved:.4f}")
print(f"  Change: {((avg_cost_improved - avg_cost_original)/avg_cost_original):.1%}")
```

---

## Part 5: Reflection Questions (15 minutes)

Answer these questions in `reflection.md`:

### Question 1: Economic Analysis
**Calculate the cost of running this agent at scale:**

Assumptions:
- 1,000 financial analyses per day
- 365 days per year
- Use your measured average cost per analysis

1. Daily cost: $___
2. Annual cost: $___
3. Cost per analysis: $___

**Would you deploy this agent at this cost? Why or why not?**

---

### Question 2: Safety & Trustworthiness
**Which model would you trust with sensitive financial data?**

Consider:
- Data privacy (local vs. cloud)
- Accuracy requirements
- Regulatory compliance (SEC, FINRA)

**Your choice:** [Claude Sonnet 4.5 / Local Llama 3 / Other]  
**Justification:** [your reasoning]

---

### Question 3: Evaluation Coverage
**What types of failures might your evaluations miss?**

Think about:
- Edge cases not in your test suite
- Subjective quality issues
- Context-dependent errors
- Adversarial inputs

**List at least 3 potential gaps in your evaluation coverage.**

---

### Question 4: Production Readiness
**Is this agent ready for production? What's missing?**

Consider:
- Evaluation coverage
- Error handling
- Monitoring and alerts
- Failover strategies
- Human-in-the-loop workflows

**Your assessment:** [Yes/No/Conditional]  
**Justification and next steps:**

---

## Submission Requirements

### Required Files

Your submission must include:

1. **Code Files:**
   - `eval_factual_accuracy.py` - Objective eval for accuracy
   - `eval_output_format.py` - Format validation eval
   - `eval_efficiency.py` - Cost and latency eval
   - `eval_summary_quality.py` - LLM-as-judge for quality
   - `eval_recommendation_justification.py` - LLM-as-judge for recommendations
   - `improved_financial_agent.py` - Your bug fixes
   - `run_evaluation_suite.py` - Complete evaluation runner

2. **Analysis Files:**
   - `analysis.md` - Your error analysis and identified bugs
   - `reflection.md` - Answers to reflection questions
   - `results.json` - Raw evaluation results (exported)

3. **Evidence:**
   - Screenshots or exported traces from Langfuse showing:
     - At least 5 test case executions
     - Evaluation scores logged
     - Cost and latency metrics

---

### Pass Criteria

**To pass this lab, you must:**

1. ✅ **Environment is Reproducible**
   - Code runs on instructor machine without modification
   - No hardcoded paths or keys

2. ✅ **Security Requirements Met**
   - API keys in `.env` file (not committed)
   - `.gitignore` includes `.env`
   - No keys in any code files

3. ✅ **All Evaluation Functions Implemented**
   - 5 evaluation functions working correctly
   - Each returns proper dict format with "passed" field
   - Test cases pass correctly

4. ✅ **Tracing Configured**
   - Langfuse integration working
   - Traces visible in dashboard
   - Scores logged for each evaluation

5. ✅ **Bugs Identified and Fixed**
   - At least 2 bugs found and documented
   - Fixes implemented in improved agent
   - Improvement validated with before/after metrics

6. ✅ **Reflection Questions Answered**
   - All 4 questions answered with data/reasoning
   - Economic analysis shows calculations
   - Thoughtful consideration of trade-offs

---

### Fail Criteria (Automatic Failure)

**You will fail if:**

- ❌ Hardcoded API keys in any file
- ❌ Code crashes due to missing dependencies
- ❌ Lab is an exact copy of the Demo (Newsletter Agent instead of Financial Agent)
- ❌ No Langfuse traces generated
- ❌ Evaluation functions don't actually test anything (just return True)
- ❌ No bugs identified or fixed
- ❌ Reflection questions left blank

---

## Stretch Goals (Optional)

If you finish early or want to go deeper:

### Stretch Goal 1: Ensemble Judging
Implement a system where 3 different LLMs judge the same output and vote:

```python
def eval_with_ensemble(result, financial_data):
    """Use multiple LLMs as judges and take majority vote."""
    # Use Claude, GPT-4, and Llama 3 as judges
    # Compare their scores
    # Return consensus and disagreements
```

### Stretch Goal 2: Regression Testing
Build a system that detects when agent quality degrades:

```python
def check_for_regression(new_results, baseline_results):
    """Alert if new version performs worse than baseline."""
    # Compare pass rates
    # Check if any previously passing test now fails
    # Flag statistically significant degradation
```

### Stretch Goal 3: Cost Optimization
Experiment with different model configurations to reduce cost while maintaining quality:

- Try Claude Haiku 4.5 (cheaper)
- Try prompt caching
- Try shorter prompts
- Document cost vs. quality trade-offs

### Stretch Goal 4: Real-World Data
Use actual SEC filings (10-K, 10-Q) as input instead of simplified examples:

```python
import requests

def fetch_sec_filing(ticker, filing_type="10-Q"):
    """Download actual SEC filings for testing."""
    # Use SEC EDGAR API
    # Parse the filing
    # Extract financial statements
    # Return formatted data for agent
```

---

## Tips for Success

### Tip 1: Start Small
Don't try to implement everything at once. Get one evaluation working, then add the next.

### Tip 2: Test Your Tests
Make sure your evaluations can both pass AND fail. Create test cases you know should fail.

### Tip 3: Read the Traces
When something goes wrong, open Langfuse and read through the entire trace. The answer is usually there.

### Tip 4: LLM-as-Judge is Probabilistic
Run subjective evaluations multiple times to see if scores are consistent. If they vary wildly, refine your judging prompt.

### Tip 5: Document as You Go
Don't wait until the end to write `analysis.md`. Document bugs as you find them.

### Tip 6: Compare to Baseline
Always compare your improved agent to the original. Quantify the improvement.

---

## Getting Help

### Common Issues

**Issue:** Langfuse traces not showing up  
**Fix:** Check that `enable_tracing=True` and `@observe()` decorator is present

**Issue:** JSON parsing errors from Claude  
**Fix:** Be more explicit in your prompt about the exact JSON format expected

**Issue:** Evaluation always passes/fails  
**Fix:** Print intermediate values to debug your logic

**Issue:** High costs during testing  
**Fix:** Use `max_tokens=500` during development, increase for final runs

---

## Assessment Rubric

| Criterion | Points | Description |
|-----------|--------|-------------|
| **Setup & Security** | 10 | Environment configured correctly, keys secured |
| **Objective Evals** | 20 | 3 objective evaluations implemented correctly |
| **Subjective Evals** | 20 | 2 LLM-as-judge evaluations with good prompts |
| **Tracing & Monitoring** | 15 | Langfuse integration working, traces visible |
| **Error Analysis** | 15 | Bugs identified with evidence, root causes analyzed |
| **Bug Fixes** | 10 | At least 2 improvements implemented and validated |
| **Reflection** | 10 | All questions answered with depth and data |
| **Total** | 100 | |

**Grading Scale:**
- 90-100: Excellent - Production-ready evaluation system
- 80-89: Good - Most evaluations working, minor issues
- 70-79: Satisfactory - Basic evaluations present, needs improvement
- Below 70: Needs work - Missing key components or major bugs

---

## Conclusion

**Remember:** "Building trustworthy AI isn't a one-time task. It's an ongoing process. A commitment to quality and responsibility at every single stage of the lifecycle."

This lab has given you the tools to:
- Systematically evaluate AI agents
- Identify and fix bugs through error analysis
- Monitor performance and costs in production
- Make data-driven decisions about agent improvements

These skills are essential for building production-grade agentic AI systems.

**Final Question:** How will YOU ensure your agents remain effective, safe, and trustworthy at scale?

---

## Submission

Submit your completed lab via [course submission system] by [deadline].

Include:
- All code files (zipped)
- Analysis and reflection markdown files
- Screenshots of Langfuse traces
- (Optional) Video walkthrough of your evaluation system

**Good luck! 🚀**
