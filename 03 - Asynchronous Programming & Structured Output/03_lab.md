# Module 03: Asynchronous Programming & Structured Output
## Student Lab Guide - Independent Application

**Estimated Time:** 90-120 minutes  
**Difficulty:** Intermediate  
**Prerequisites:** Completed the Glossary reading and attended the Instructor Demo

---

## Learning Objectives

By the end of this lab, you will be able to:
1. Set up and configure an async Python environment with multiple LLM providers
2. Define custom tools for domain-specific calculations
3. Implement input and output guardrails for agent safety
4. Create Pydantic models for structured, validated outputs
5. Build a multi-agent system with handoffs and tool calling
6. Handle asynchronous errors and debug async workflows

---

## The Challenge: Medical Dosage Calculator Agent

### Context

You are building an AI agent for a medical clinic that helps nurses calculate safe medication dosages based on patient weight, age, and drug type. The system must:

- Calculate precise dosages using medical formulas
- Check for dangerous drug interactions
- Validate inputs to prevent calculation errors
- Block inappropriate queries (patient privacy, unauthorized drug access)
- Return structured data that can be logged to a patient database

**Critical Difference from Demo:**
- **Demo:** Financial calculations (compound interest)
- **Lab:** Medical calculations (drug dosages)
- **Why This Matters:** You must understand the *architecture* of agents with tools and guardrails, not just copy financial code

---

## Part 1: Environment Setup (20 minutes)

### Step 1: Create Your Project Directory

```bash
mkdir module03_lab
cd module03_lab
```

### Step 2: Create and Activate Virtual Environment

**Option A: Using `venv` (Standard Python)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Option B: Using `uv` (Recommended for this course)**
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install Required Packages (If Needed)

```bash
pip install pydantic-ai python-dotenv nest-asyncio openai requests
```

**Package Purpose:**
- `pydantic-ai`: Agent framework with structured outputs
- `python-dotenv`: Load API keys from `.env` file
- `nest-asyncio`: Allow nested event loops (for Jupyter/Colab compatibility)
- `openai`: Async OpenAI client (works with OpenAI, Ollama, Groq, etc.)
- `requests`: HTTP library for service checks

### Step 4: Create `.env` File

Create a file named `.env` in your project directory:

```env
# Cloud API Keys (Optional - only if using cloud models)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
GROQ_API_KEY=your_groq_key_here

# Local Services (Free - recommended for this lab)
# Make sure Ollama is running: ollama serve
# Download a model: ollama pull llama3.2
```

**Important:** Add `.env` to your `.gitignore` file to prevent committing secrets!

### Step 5: Verify Local Services

**Option A: Ollama (Recommended)**
```bash
# Start Ollama service if needed
ollama serve

# In a new terminal, pull a model if needed
ollama pull llama3.2
```

**Option B: LM Studio (if needed)**
1. Download LM Studio from https://lmstudio.ai/
2. Load a model (e.g., Llama 3.2)
3. Start the local server (default port: 1234)

### Step 6: Environment Check Script

Create a file `check_environment.py`:

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def is_service_running(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False

print("=== Environment Check ===\n")

# Check local services
print("Local Services:")
print(f"  Ollama:    {'✅' if is_service_running('http://localhost:11434') else '❌'}")
print(f"  LM Studio: {'✅' if is_service_running('http://localhost:1234') else '❌'}")

# Check API keys (optional)
print("\nAPI Keys:")
for key in ['OPENAI_API_KEY', 'GROQ_API_KEY', 'ANTHROPIC_API_KEY']:
    status = '✅ Set' if os.getenv(key) else '❌ Not Set'
    print(f"  {key}: {status}")

print("\nIf all checks passed, you're ready to start the lab!")
```

Run it:
```bash
python check_environment.py
```

**Expected Output:**
```
=== Environment Check ===

Local Services:
  Ollama:    ✅
  LM Studio: ❌

API Keys:
  OPENAI_API_KEY: ❌ Not Set
  GROQ_API_KEY: ✅ Set
  ANTHROPIC_API_KEY: ❌ Not Set

If all checks passed, you're ready to start the lab!
```

**Required:** At least one LLM service (local or cloud) must be available.

---

## Part 2: Define Your Domain Tools (25 minutes)

### Task 2.1: Drug Dosage Calculator Tool

Create a file `medical_tools.py` with the following tools:

**Tool 1: Calculate Dosage**

```python
from pydantic_ai import function_tool
from typing import Literal

@function_tool
def calculate_drug_dosage(
    patient_weight_kg: float,
    drug_name: Literal["ibuprofen", "acetaminophen", "amoxicillin"],
    age_years: int
) -> dict:
    """
    Calculates safe drug dosage based on patient weight and age.
    
    Dosage formulas (simplified for educational purposes):
    - Ibuprofen: 10 mg/kg (max 800mg single dose)
    - Acetaminophen: 15 mg/kg (max 1000mg single dose)  
    - Amoxicillin: 20 mg/kg (max 500mg single dose)
    
    Age restrictions:
    - Ibuprofen: 6 months+
    - Acetaminophen: 2 years+
    - Amoxicillin: 1 year+
    
    Args:
        patient_weight_kg: Patient weight in kilograms
        drug_name: Name of the drug (must be from approved list)
        age_years: Patient age in years
    
    Returns:
        Dictionary with dosage info and safety warnings
    """
    # Dosage formulas (mg per kg)
    formulas = {
        "ibuprofen": {"dose_per_kg": 10, "max_dose": 800, "min_age": 0.5},
        "acetaminophen": {"dose_per_kg": 15, "max_dose": 1000, "min_age": 2},
        "amoxicillin": {"dose_per_kg": 20, "max_dose": 500, "min_age": 1}
    }
    
    drug_info = formulas[drug_name.lower()]
    
    # Check age restriction
    if age_years < drug_info["min_age"]:
        return {
            "status": "UNSAFE",
            "drug": drug_name,
            "recommended_dose_mg": 0,
            "warning": f"Patient too young. Minimum age: {drug_info['min_age']} years"
        }
    
    # Calculate dosage
    calculated_dose = patient_weight_kg * drug_info["dose_per_kg"]
    safe_dose = min(calculated_dose, drug_info["max_dose"])
    
    # Generate warning if dose was capped
    warning = None
    if calculated_dose > drug_info["max_dose"]:
        warning = f"Calculated dose ({calculated_dose:.1f}mg) exceeds maximum. Capped at {safe_dose:.1f}mg"
    
    return {
        "status": "SAFE",
        "drug": drug_name,
        "patient_weight_kg": patient_weight_kg,
        "recommended_dose_mg": round(safe_dose, 1),
        "warning": warning
    }
```

**Tool 2: Check Drug Interactions**

```python
@function_tool
def check_drug_interaction(drug1: str, drug2: str) -> dict:
    """
    Checks if two drugs have dangerous interactions.
    
    Args:
        drug1: Name of first drug
        drug2: Name of second drug
    
    Returns:
        Dictionary with interaction status and details
    """
    # Simplified interaction database (real systems use comprehensive databases)
    known_interactions = {
        ("ibuprofen", "acetaminophen"): {
            "severity": "MODERATE",
            "description": "Both are pain relievers. Consult physician before combining."
        },
        ("ibuprofen", "aspirin"): {
            "severity": "HIGH",
            "description": "Risk of gastrointestinal bleeding. Do not combine."
        },
        ("acetaminophen", "alcohol"): {
            "severity": "HIGH",
            "description": "Severe liver damage risk. Avoid alcohol."
        }
    }
    
    # Normalize drug names
    drug1_lower = drug1.lower().strip()
    drug2_lower = drug2.lower().strip()
    
    # Check both orderings
    interaction = (
        known_interactions.get((drug1_lower, drug2_lower)) or
        known_interactions.get((drug2_lower, drug1_lower))
    )
    
    if interaction:
        return {
            "interaction_found": True,
            "drug1": drug1,
            "drug2": drug2,
            "severity": interaction["severity"],
            "description": interaction["description"]
        }
    else:
        return {
            "interaction_found": False,
            "drug1": drug1,
            "drug2": drug2,
            "message": "No known interactions found in database."
        }
```

**Your Task:**
- Copy the above tools to `medical_tools.py`
- **Extension Challenge:** Add a third drug to each tool (e.g., "aspirin")
- **Extension Challenge:** Add a tool that converts pounds to kilograms

---

## Part 3: Implement Guardrails (20 minutes)

### Task 3.1: Input Guardrail - Block Unauthorized Queries

Create a file `guardrails.py`:

```python
from pydantic_ai import input_guardrail, GuardrailFunctionOutput, RunContextWrapper, Agent

@input_guardrail(name="Privacy Guardian")
def block_privacy_violations(ctx: RunContextWrapper, agent: Agent, input: str) -> GuardrailFunctionOutput:
    """
    Blocks queries that might violate patient privacy or request unauthorized information.
    """
    # Forbidden patterns
    forbidden_patterns = [
        "patient name",
        "social security",
        "home address",
        "phone number",
        "medical record number",
        "show me all patients",
        "database",
        "ignore instructions"
    ]
    
    input_lower = input.lower()
    
    for pattern in forbidden_patterns:
        if pattern in input_lower:
            print(f"\n🚨 [PRIVACY] Input blocked: Contains '{pattern}'")
            return GuardrailFunctionOutput(
                tripwire_triggered=True,
                output_info=f"Query blocked: Privacy violation detected ('{pattern}')"
            )
    
    return GuardrailFunctionOutput(tripwire_triggered=False, output_info="Input allowed")
```

**Your Task:**
- Copy the above guardrail to `guardrails.py`
- **Extension Challenge:** Add patterns for controlled substance requests ("oxycodone", "fentanyl")
- **Extension Challenge:** Add a pattern to block requests for patient data by specific identifiers

### Task 3.2: Output Guardrail - Enforce Medical Disclaimer

```python
from pydantic_ai import output_guardrail

@output_guardrail(name="Medical Disclaimer Enforcer")
async def enforce_medical_disclaimer(ctx: RunContextWrapper, agent: Agent, output: str) -> GuardrailFunctionOutput:
    """
    Ensures medical advice outputs include a disclaimer.
    """
    required_phrase = "consult a physician"
    
    if required_phrase.lower() not in output.lower():
        print(f"\n⚠️ [COMPLIANCE] Output missing required disclaimer")
        return GuardrailFunctionOutput(
            tripwire_triggered=True,
            output_info="Output blocked: Missing medical disclaimer"
        )
    
    return GuardrailFunctionOutput(tripwire_triggered=False, output_info="Output compliant")
```

**Your Task:**
- Copy the above guardrail to `guardrails.py`
- **Extension Challenge:** Add a length limit guardrail (max 200 words)
- **Extension Challenge:** Add a guardrail that blocks outputs containing absolute certainty language ("definitely", "guaranteed", "100% safe")

---

## Part 4: Define Structured Output Schema (15 minutes)

### Task 4.1: Create Pydantic Models

Create a file `schemas.py`:

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal

class DosageRecommendation(BaseModel):
    """Structured output for drug dosage calculations"""
    patient_weight_kg: float = Field(description="Patient weight in kilograms")
    patient_age_years: int = Field(description="Patient age in years")
    drug_name: str = Field(description="Name of prescribed drug")
    recommended_dose_mg: float = Field(description="Recommended dosage in milligrams")
    safety_status: Literal["SAFE", "UNSAFE", "CAUTION"] = Field(description="Safety assessment")
    warnings: Optional[str] = Field(default=None, description="Safety warnings or contraindications")
    disclaimer: str = Field(default="Always consult a physician before administering medication.")

class DrugInteractionCheck(BaseModel):
    """Structured output for drug interaction analysis"""
    drug1: str = Field(description="First drug name")
    drug2: str = Field(description="Second drug name")
    interaction_found: bool = Field(description="Whether an interaction was detected")
    severity: Optional[Literal["LOW", "MODERATE", "HIGH"]] = Field(default=None)
    recommendation: str = Field(description="Medical recommendation")
```

**Your Task:**
- Copy the above schemas to `schemas.py`
- **Extension Challenge:** Add a `timestamp` field to track when the calculation was performed
- **Extension Challenge:** Add a `pharmacist_review_required` boolean field for high-severity cases

---

## Part 5: Build the Multi-Agent System (30 minutes)

### Task 5.1: Create the Medical Agent

Create a file `medical_agent.py`:

```python
import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic_ai import Agent, Runner
from pydantic_ai.models import OpenAIChatCompletionsModel

# Import your tools, guardrails, and schemas
from medical_tools import calculate_drug_dosage, check_drug_interaction
from guardrails import block_privacy_violations, enforce_medical_disclaimer
from schemas import DosageRecommendation

load_dotenv()

# Configure your model
OLLAMA_BASE_URL = "http://localhost:11434/v1"
ollama_client = AsyncOpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")
ollama_model = OpenAIChatCompletionsModel(model="llama3.2", openai_client=ollama_client)

# Create the Dosage Specialist Agent
dosage_agent = Agent(
    name='DosageSpecialist',
    instructions=(
        'You are a medical dosage calculation specialist. '
        'Use the calculate_drug_dosage tool to determine safe medication doses. '
        'Always include the disclaimer: "Always consult a physician before administering medication." '
        'Be precise and show your calculations.'
    ),
    tools=[calculate_drug_dosage],
    output_type=DosageRecommendation,
    model=ollama_model
)

# Create the Triage Agent (entry point)
triage_agent = Agent(
    name='MedicalTriage',
    instructions=(
        'You are a medical triage assistant. '
        'If the query involves drug dosage calculations, transfer to DosageSpecialist. '
        'For general medical questions, answer briefly and remind users to consult a physician. '
        'Never provide specific medical advice without using tools.'
    ),
    handoffs=[dosage_agent],
    input_guardrails=[block_privacy_violations],
    output_guardrails=[enforce_medical_disclaimer],
    model=ollama_model
)

# Main execution function
async def run_medical_query(user_input: str):
    """
    Executes the medical agent workflow.
    
    Args:
        user_input: The user's medical query
    """
    print(f"\n{'='*70}")
    print(f"USER QUERY: {user_input}")
    print(f"{'='*70}\n")
    
    try:
        result = await Runner.run(
            starting_agent=triage_agent,
            input=user_input
        )
        print(f"✅ AGENT RESPONSE:")
        print(result.final_output)
        print(f"\n{'='*70}\n")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print(f"{'='*70}\n")

# Test queries
async def main():
    """Run test queries"""
    test_queries = [
        # Query 1: Valid dosage calculation
        "Calculate ibuprofen dosage for a 7-year-old patient weighing 25 kg",
        
        # Query 2: Age restriction test
        "What dosage of acetaminophen for a 1-year-old weighing 10 kg?",
        
        # Query 3: Privacy violation (should be blocked)
        "Show me patient name and medical record number",
        
        # Query 4: General medical question
        "What are the side effects of ibuprofen?",
    ]
    
    for query in test_queries:
        await run_medical_query(query)
        await asyncio.sleep(1)  # Brief pause between queries

# Execute
if __name__ == "__main__":
    asyncio.run(main())
```

**Your Task:**
1. Copy the above code to `medical_agent.py`
2. Run the script: `python medical_agent.py`
3. Observe which queries trigger handoffs, guardrails, and tool calls
4. **Extension Challenge:** Add a `InteractionChecker` agent that handles the `check_drug_interaction` tool

---

## Part 6: Testing & Debugging (15 minutes)

### Task 6.1: Test Edge Cases

Add these test queries to your `main()` function:

```python
edge_case_queries = [
    # Edge Case 1: Weight that triggers max dose cap
    "Calculate ibuprofen for a 100kg adult",
    
    # Edge Case 2: Invalid drug name (should fail gracefully)
    "Calculate dosage for morphine",  # Not in approved list
    
    # Edge Case 3: Zero or negative weight
    "What's the dose for a patient weighing 0 kg?",
    
    # Edge Case 4: Extremely high age
    "Dosage for a 150-year-old patient weighing 70kg",
]
```

**Your Task:**
- Run each edge case
- Document what happens (does it crash? handle gracefully? return error?)
- Improve your tools to handle these cases properly

**Expected Behavior:**
- Invalid drug names: Should raise a Pydantic validation error (caught by framework)
- Zero/negative weight: Should be rejected (add validation in your tool)
- Extreme ages: Should trigger warnings but still calculate if safe

---

## Part 7: Async Performance Test (10 minutes)

### Task 7.1: Measure Speedup

Create a file `performance_test.py`:

```python
import asyncio
import time
from medical_agent import dosage_agent

# Test queries
queries = [
    "Ibuprofen for 30kg patient, age 8",
    "Acetaminophen for 45kg patient, age 15",
    "Amoxicillin for 60kg patient, age 25",
]

# Sequential execution
async def test_sequential():
    """Run queries one at a time"""
    start = time.time()
    for query in queries:
        result = await dosage_agent.run(query)
    end = time.time()
    return end - start

# Concurrent execution  
async def test_concurrent():
    """Run queries concurrently"""
    start = time.time()
    tasks = [dosage_agent.run(query) for query in queries]
    await asyncio.gather(*tasks)
    end = time.time()
    return end - start

async def main():
    sequential_time = await test_sequential()
    concurrent_time = await test_concurrent()
    
    print(f"\nPerformance Results:")
    print(f"Sequential: {sequential_time:.2f} seconds")
    print(f"Concurrent: {concurrent_time:.2f} seconds")
    print(f"Speedup: {sequential_time / concurrent_time:.2f}x")

asyncio.run(main())
```

**Your Task:**
- Run `python performance_test.py`
- Record the speedup factor
- **Reflection:** Why is the speedup less than 3x even with 3 queries?

---

## Part 8: Reflection Questions (Graded)

Answer these questions in a file named `REFLECTION.md`:

### Architectural Questions

**Q1:** Explain the agent handoff mechanism. Why did we use two agents (Triage → Dosage) instead of one agent with both capabilities?

**Q2:** In your implementation, where does the actual Python code execution happen?
- [ ] Inside the LLM
- [ ] In the Pydantic AI framework
- [ ] On the cloud provider's servers
- [ ] In your local Python environment

**Q3:** Draw (or describe) the data flow when a user asks: "Calculate ibuprofen for a 25kg child"
- Start from user input
- Show every step: triage, handoff, tool call, validation, response
- Indicate where guardrails check the data

### Cost & Performance Questions

**Q4:** You need to calculate dosages for 100 patients. Estimate the cost and time if you use:
- **Option A:** Sequential calls to GPT-4 ($0.03 per 1K tokens, ~500 tokens per call)
- **Option B:** Concurrent calls to local Ollama (free, ~2 seconds per call)

**Q5:** Your medical agent currently validates age restrictions in the tool. Should this validation be moved to a guardrail instead? Why or why not?

### Safety & Ethics Questions

**Q6:** Your input guardrail blocks queries containing "patient name." A doctor asks: "Calculate dose for patient John Smith." The query is blocked, but this is a legitimate medical professional.
- What's the problem with the current guardrail?
- How would you fix it while maintaining privacy protections?

**Q7:** The output guardrail enforces: "Always consult a physician." A user asks: "What's the capital of France?" The agent answers correctly but the guardrail blocks it (no disclaimer).
- Why is this happening?
- How would you fix the guardrail to only check medical outputs?

**Q8:** If this system were deployed in a real hospital, what additional safety mechanisms would you add?

---

## Part 9: Extension Challenges (Optional, Extra Credit)

### Challenge 1: Multi-Drug Interaction Checker

Extend your system to handle this query:
"Check if there are any interactions between ibuprofen, acetaminophen, and aspirin"

Requirements:
- Must check all pairwise combinations
- Use `check_drug_interaction` tool multiple times
- Run checks concurrently (not sequentially)
- Return a structured summary

### Challenge 2: Retry Logic with Exponential Backoff

Simulate API rate limiting and implement retry logic:

```python
import random

async def flaky_api_call():
    """Simulates unreliable API that fails randomly"""
    if random.random() < 0.6:  # 60% failure rate
        raise Exception("Rate limit exceeded")
    return "Success"

# Your task: Implement retry_with_backoff()
async def retry_with_backoff(func, max_retries=3):
    """
    Retries a function with exponential backoff.
    Wait 1s, then 2s, then 4s between retries.
    """
    # YOUR CODE HERE
    pass
```

### Challenge 3: Agent Observability

Add logging to track:
- Which agent handled each query
- Which tools were called
- How long each step took
- Whether any guardrails were triggered

Requirements:
- Log to a file `agent_logs.json`
- Include timestamps
- Structure logs as JSON for easy parsing

---

## Submission Requirements

### What to Submit

Create a folder in your GitHub repository` named `module03_[YourName]` containing:

1. **Code Files:**
   - `medical_tools.py`
   - `guardrails.py`
   - `schemas.py`
   - `medical_agent.py`
   - `performance_test.py`

2. **Documentation:**
   - `REFLECTION.md` (answers to all reflection questions)
   - `README.md` (setup instructions for running your code)

3. **Test Output:**
   - `test_results.txt` (copy-paste of your terminal output showing all test queries)

### Grading Rubric

**Pass Criteria (80% minimum):**
- ✅ Environment is reproducible (code runs on instructor's machine)
- ✅ All tools are implemented and functional
- ✅ At least 2 guardrails are implemented (input and output)
- ✅ Pydantic schema returns structured output
- ✅ Multi-agent handoff works correctly
- ✅ Reflection questions answered with reasoning (not just "yes/no")
- ✅ Code follows proper async patterns (no blocking calls)

**Fail Criteria (Auto-Zero):**
- ❌ Hardcoded API keys in code (security violation)
- ❌ Code crashes with unhandled exceptions
- ❌ Lab is an exact copy of the Demo without the required medical scenario variation
- ❌ Missing reflection answers

**Excellence Criteria (90%+):**
- 🌟 Completed at least one extension challenge
- 🌟 Added additional tools beyond the requirements
- 🌟 Comprehensive error handling with try-except blocks
- 🌟 Clear, well-documented code with docstrings
- 🌟 Thoughtful reflection answers demonstrating deep understanding

---

## Troubleshooting Guide

### Issue 1: "Event loop is already running"

**Solution:**
```python
import nest_asyncio
nest_asyncio.apply()
```

### Issue 2: "Module 'medical_tools' not found"

**Solution:**
- Ensure all files are in the same directory
- Check that file names match exactly (case-sensitive)
- Verify you're running from the correct directory

### Issue 3: Ollama connection refused

**Solution:**
```bash
# Start Ollama service
ollama serve

# Verify it's running
curl http://localhost:11434
```

### Issue 4: "Guardrail triggered but I don't know why"

**Solution:**
- Add print statements in your guardrails to see exactly what triggered them
- Check the `output_info` field in the GuardrailFunctionOutput
- Test the guardrail in isolation with different inputs

### Issue 5: Pydantic validation error

**Solution:**
- Read the error message carefully (Pydantic gives detailed feedback)
- Check that your tool returns data matching your schema
- Use `.dict()` on Pydantic objects to inspect their structure

---

## Resources

- **Asyncio Tutorial:** https://realpython.com/async-io-python/
- **Pydantic AI Docs:** https://ai.pydantic.dev/
- **Pydantic Validation:** https://docs.pydantic.dev/latest/concepts/validators/
- **Ollama Documentation:** https://ollama.com/docs

---

## Final Checklist

Before submitting, verify:

- [ ] Code runs without errors on a fresh environment
- [ ] `.env` file **IS NOT** excluded in your repository
- [ ] All reflection questions are answered
- [ ] Test output demonstrates successful runs
- [ ] README includes setup instructions
- [ ] Code is commented and readable
- [ ] File names match the submission requirements

---

**Good luck! Remember: The goal is to understand async agent architectures, not to build a production medical system. Focus on learning the patterns and principles.**

**Questions?** Post in the course discussion forum or attend office hours.
