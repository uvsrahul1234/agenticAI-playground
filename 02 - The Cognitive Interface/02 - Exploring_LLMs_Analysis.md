# Analysis: Exploring LLMs Notebook

## Executive Summary

This notebook demonstrates **foundational agentic AI competencies** by building a **model-agnostic LLM interface** that compares responses from multiple providers (cloud and local). Students learn to orchestrate different "cognitive backends" and implement an **LLM-as-Judge evaluation pattern**—a critical skill for assessing agent performance in production systems.

---

## Course Mapping

### Primary Alignment
**Week 2: The Cognitive Interface (LLMs & APIs)**
- ✅ Building a model-agnostic interface that swaps backends dynamically
- ✅ Context windows, tokenization costs, and system prompting
- ✅ Comparing cloud vs. local inference trade-offs

---

## Agentic Terms & Definitions

### 1. **Model-Agnostic Interface**
**Definition:** A unified code structure that allows swapping between different LLM providers (OpenAI, Anthropic, local models) without changing application logic.

**Why It Matters for Agents:** Agentic systems need flexibility to route tasks to the most cost-effective or capable model. For example:
- Simple classification → Local Llama model (fast, free)
- Complex reasoning → Claude Opus (slower, expensive)

**Example from Notebook:**
```python
# Same messages array works across all providers
messages = [{"role": "user", "content": request}]

# OpenAI
openai.chat.completions.create(model=model, messages=messages)

# Anthropic (different API, same concept)
claude.messages.create(model=model, messages=messages, max_tokens=1000)

# Ollama (local, OpenAI-compatible)
ollama.chat.completions.create(model=model, messages=messages)
```

---

### 2. **LLM-as-Judge**
**Definition:** Using an LLM to evaluate the quality, accuracy, or adherence to criteria of outputs from other LLMs (or itself).

**Why It Matters for Agents:** In multi-agent systems, a "supervisor" agent often needs to assess whether worker agents produced acceptable outputs. This notebook shows:
- Feeding 6 responses to o3-mini
- Asking it to rank them by "clarity and strength"
- Returning structured JSON results

**Production Use Cases:**
- **Newsletter Crew:** Editor agent evaluates writer agent's drafts
- **AutoGen Debates:** Judge agent scores arguments
- **Evaluation Suite:** Automated quality checks before deployment

---

### 3. **Local vs. Cloud Inference**
**Definition:** 
- **Cloud Inference:** Sending requests to external APIs (OpenAI, Anthropic, Google)
  - Pros: Latest models, no GPU needed, automatic scaling
  - Cons: Cost per token, data privacy concerns, internet dependency
  
- **Local Inference:** Running models on your own hardware (Ollama, LM Studio)
  - Pros: Free after download, complete data privacy, works offline
  - Cons: Requires RAM/VRAM, smaller/quantized models, slower on CPU

**When Agents Use Each:**
- **Cloud:** Final production output, complex planning, high-stakes decisions
- **Local:** Development/testing, high-frequency tool calls, sensitive data processing

---

### 4. **OpenAI-Compatible API Pattern**
**Definition:** A standardized interface that many providers (Groq, Ollama, LM Studio) implement to mimic OpenAI's API format, enabling easy provider switching.

**Notebook Examples:**
```python
# Groq (hosted Llama)
groq = OpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")

# Ollama (local)
ollama = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

# LM Studio (local)
mistral = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
```
All use the same `OpenAI()` client—only `base_url` and `api_key` change.

---

### 5. **Service Availability Checking**
**Definition:** Programmatically verifying that required APIs or local servers are running before attempting to use them.

**Why It Matters for Agents:** Agentic workflows often involve multiple dependencies (vector databases, local models, APIs). The notebook's `is_service_running()` function prevents cryptic errors by checking upfront:

```python
def is_service_running(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        return False
    return False
```

**Production Pattern:** Before launching a CrewAI workflow with local tools, agents should validate:
- ✅ Ollama server is live
- ✅ Vector database is responding
- ✅ API keys are valid

---

### 6. **Structured Output Parsing**
**Definition:** Forcing LLMs to return data in predictable formats (JSON, XML) rather than free-form text, enabling reliable downstream processing.

**Notebook Implementation:**
The evaluator prompt explicitly requests:
```
Respond with JSON, and only JSON, with the following format:
{"results": ["best llm number", "second best llm number", ...]}
```

Then parses it:
```python
results_dict = json.loads(results)
ranks = results_dict["results"]
```

**Connection:** This foreshadows the "Pydantic validators" week, where we will learn to **enforce** schemas rather than just *requesting* them.

---

## Step-by-Step Implementation Guide

### **Section 1: Environment Setup**
**Learning Objective:** Secure API key management and service validation

#### Step 1.1: Install Dependencies
```bash
# In your activated uv environment:
uv pip install openai anthropic python-dotenv requests ipython
```

**Skills:** Package management, dependency isolation

---

#### Step 1.2: Create .env File
Create a file named `.env` in your project root:
```
OPENAI_API_KEY=sk-proj-xxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxx
GOOGLE_API_KEY=xxxxx
GROQ_API_KEY=gsk_xxxxx
HF_TOKEN=hf_xxxxx
```

**Concept:** Never hardcode API keys in notebooks—use environment variables for security and portability.

---

#### Step 1.3: Load and Validate Environment
**Code to Implement:**
```python
import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from IPython.display import Markdown, display

load_dotenv(override=True)

def is_service_running(url):
    """
    Checks if a service is running by attempting to connect to its URL.
    """
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.Timeout:
        return False
    return False

# Check for Ollama
ollama_url = 'http://localhost:11434'
if is_service_running(ollama_url):
    print("Ollama is running")
else:
    print("Ollama is not running")

# Check for LM Studio
lmstudio_url = 'http://localhost:1234'
if is_service_running(lmstudio_url):
    print("LM Studio is running")
else:
    print("LM Studio is not running")

# Validate API keys exist (but don't print them!)
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')
hf_token = os.getenv('HF_TOKEN')

for key_name, key_value in [
    ("OpenAI API Key", openai_api_key),
    ("Anthropic API Key", anthropic_api_key),
    ("Google API Key", google_api_key),
    ("Groq API Key", groq_api_key),
    ("Hugging Face Token", hf_token)
]:
    if key_value:
        print(f"{key_name} exists")
    else:
        print(f"{key_name} not set")
```

**Expected Output:**
```
Ollama is running
LM Studio is running
OpenAI API Key exists
Anthropic API Key exists
Google API Key exists
Groq API Key exists
Hugging Face Token exists
```

**Debugging Tips:**
- If Ollama/LM Studio show as "not running," start them manually
- If API keys show "not set," verify your .env file is in the correct directory
- Use `print(os.getcwd())` to confirm your working directory

---

### **Section 2: Multi-Provider LLM Integration**
**Learning Objective:** Build a model-agnostic interface for comparing LLM responses

#### Step 2.1: Define the Test Prompt
**Code to Implement:**
```python
# Create a thought-provoking prompt that requires reasoning
llms = []  # Track which models we test
responses = []  # Store their responses

request = "You are an AI tasked with writing a single, one-sentence instruction for a human to prevent a paradox in a time-travel scenario. What is that instruction?"
messages = [{"role": "user", "content": request}]
```

**Why This Prompt?** It tests:
- Logical reasoning (understanding causality)
- Conciseness (single-sentence constraint)
- Creativity (multiple valid answers exist)

---

#### Step 2.2: Query OpenAI (Cloud)
**Code to Implement:**
```python
# OpenAI (GPT-4o-mini)
openai = OpenAI()  # Automatically uses OPENAI_API_KEY from environment
model = "gpt-4o-mini"

response = openai.chat.completions.create(model=model, messages=messages)
result = response.choices[0].message.content

display(Markdown(result))
llms.append(model)
responses.append(result)
```

**Skills:**
- Using OpenAI SDK
- Extracting text from completion objects
- Rendering Markdown in Jupyter

**Concept:** The `OpenAI()` client automatically reads `OPENAI_API_KEY` from your environment—no need to pass it explicitly.

---

#### Step 2.3: Query Anthropic (Cloud)
**Code to Implement:**
```python
# Claude Sonnet
model = "claude-3-7-sonnet-latest"

claude = Anthropic()  # Uses ANTHROPIC_API_KEY from environment
response = claude.messages.create(
    model=model, 
    messages=messages, 
    max_tokens=1000  # Required for Anthropic API
)
result = response.content[0].text

display(Markdown(result))
llms.append(model)
responses.append(result)
```

**Key Difference from OpenAI:**
- Anthropic requires `max_tokens` parameter
- Response structure: `response.content[0].text` vs. `response.choices[0].message.content`

**Skill:** Adapting to provider-specific API patterns while maintaining conceptual consistency

---

#### Step 2.4: Query Google Gemini (Cloud)
**Code to Implement:**
```python
# Google Gemini (using OpenAI-compatible endpoint)
gemini = OpenAI(
    api_key=google_api_key, 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = "gemini-2.0-flash"

response = gemini.chat.completions.create(model=model, messages=messages)
result = response.choices[0].message.content

display(Markdown(result))
llms.append(model)
responses.append(result)
```

**Note:** Google provides an OpenAI-compatible wrapper—same client, different `base_url`.

**Possible Error:** "Generative Language API has not been enabled." 
- **Fix:** Enable it in Google Cloud Console → APIs & Services

---

#### Step 2.5: Query Groq (Hosted Open Models)
**Code to Implement:**
```python
# Groq (ultra-fast hosted Llama models)
groq = OpenAI(
    api_key=groq_api_key, 
    base_url="https://api.groq.com/openai/v1"
)
model = "llama-3.3-70b-versatile"

response = groq.chat.completions.create(model=model, messages=messages)
result = response.choices[0].message.content

display(Markdown(result))
llms.append(model)
responses.append(result)
```

**Why Groq?** Free tier, extremely fast inference (LPU architecture), good for development.

---

#### Step 2.6: Query Ollama (Local)
**Code to Implement:**
```python
# Ollama (local inference)
ollama = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
model = "llama3.2"

response = ollama.chat.completions.create(model=model, messages=messages)
result = response.choices[0].message.content

display(Markdown(result))
llms.append(model)
responses.append(result)
```

**Prerequisite:** Run `ollama pull llama3.2` in terminal before executing this cell.

**Trade-offs:**
- ✅ Free, private, works offline
- ❌ Slower than cloud (unless you have a GPU)
- ❌ Smaller/quantized model (lower quality than GPT-4)

---

#### Step 2.7: Query LM Studio (Local)
**Code to Implement:**
```python
# LM Studio (local inference with GUI)
mistral = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
model = "mistral_instruct_7b"

response = mistral.chat.completions.create(model=model, messages=messages)
result = response.choices[0].message.content

display(Markdown(result))
llms.append(model)
responses.append(result)
```

**Prerequisites:**
1. Download a model in LM Studio (e.g., `mistral-7b-instruct-v0.2.Q4_K_M.gguf`)
2. Load it in the GUI
3. Start the local server (click "Start Server" button)

**Troubleshooting:** If you get a connection error, verify the server is running at `http://localhost:1234`

---

#### Step 2.8: Prepare Responses for Evaluation
**Code to Implement:**
```python
# Format all responses into a single text block
text_prep = ""

for index, response in enumerate(responses):
    text_prep += f"# Response from llm {index+1}\n\n"
    text_prep += response + "\n\n"
```

**Purpose:** Create a structured prompt for the LLM-as-Judge in the next section.

---

### **Section 3: LLM-as-Judge Evaluation**
**Learning Objective:** Use an LLM to programmatically rank outputs from multiple models

#### Step 3.1: Build the Evaluation Prompt
**Code to Implement:**
```python
evaluator = f"""You are evaluating responses from {len(llms)} LLMs.
Each model has been given this question:

{request}

Your job is to evaluate each response for clarity and strength of argument, and rank them in order of best to worst.
Respond with JSON, and only JSON, with the following format:
{{"results": ["best llm number", "second best llm number", "third best llm number", ...]}}

Here are the responses from each llm:

{text_prep}

Now, please respond with the ranked order of the llms using JSON, nothing else. Do not include markdown formatting or code blocks."""

print(evaluator)
```

**Prompt Engineering Techniques:**
1. **Role Assignment:** "You are evaluating..."
2. **Clear Criteria:** "clarity and strength of argument"
3. **Structured Output Enforcement:** "Respond with JSON, and only JSON"
4. **Example Schema:** Shows the exact format expected
5. **Explicit Constraints:** "Do not include markdown formatting"

**Why This Matters:** Proper prompts are critical in agentic systems—agents act on LLM outputs, so reliability is paramount.

---

#### Step 3.2: Execute Evaluation with o3-mini
**Code to Implement:**
```python
evaluator_messages = [{"role": "user", "content": evaluator}]

openai = OpenAI()
response = openai.chat.completions.create(
    model="o3-mini",  # Reasoning model optimized for evaluation
    messages=evaluator_messages,
)
results = response.choices[0].message.content
print(results)
```

**Expected Output:**
```json
{"results": ["1", "2", "6", "4", "5", "3"]}
```

**Why o3-mini?** OpenAI's reasoning-optimized model excels at comparative analysis tasks.

---

#### Step 3.3: Parse and Display Rankings
**Code to Implement:**
```python
results_dict = json.loads(results)
ranks = results_dict["results"]

for index, result in enumerate(ranks):
    llm = llms[int(result)-1]
    print(f"Rank {index+1}: {llm}")
```

**Expected Output:**
```
Rank 1: gpt-4o-mini
Rank 2: claude-3-7-sonnet-latest
Rank 3: mistral_instruct_7b
Rank 4: llama-3.3-70b-versatile
Rank 5: llama3.2
Rank 6: gemini-2.0-flash
```

**Skills:**
- JSON parsing with error handling
- Array indexing manipulation
- Programmatic result presentation

---

## Advanced Extensions (Optional Challenges)

### Challenge 1: Add Error Handling
Wrap API calls in try-except blocks:
```python
try:
    response = openai.chat.completions.create(model=model, messages=messages)
    result = response.choices[0].message.content
except Exception as e:
    print(f"Error with {model}: {e}")
    result = "ERROR: Unable to generate response"
```

**Skill:** Building robust agent systems that gracefully handle failures

---

### Challenge 2: Compare Cost vs. Performance
Add token counting:
```python
tokens_used = response.usage.total_tokens
cost = tokens_used * COST_PER_TOKEN[model]
print(f"{model}: {tokens_used} tokens, ${cost:.4f}")
```

**Skill:** Optimizing agentic workflows for production budgets

---

### Challenge 3: Implement Pydantic Validation
Replace `json.loads()` with a typed model:
```python
from pydantic import BaseModel

class EvaluationResult(BaseModel):
    results: list[str]

# Force o3-mini to match this schema
results_dict = EvaluationResult.model_validate_json(results)
```

**Skill:** Structured output enforcement

---

### Challenge 4: Multi-Criteria Evaluation
Modify the evaluator to score on multiple dimensions:
```json
{
  "rankings": [
    {"llm": "1", "clarity": 9, "creativity": 7, "accuracy": 8},
    {"llm": "2", "clarity": 8, "creativity": 8, "accuracy": 9}
  ]
}
```

**Skill:** Building sophisticated evaluation frameworks for agent systems

---

## Key Takeaways

1. **There is no "best" LLM**—different models excel at different tasks
2. **Local models trade quality for privacy/cost**—know when to use each
3. **Evaluation is subjective**—the judge's biases matter (even o3-mini has preferences)
4. **Structured outputs require careful prompting**—"respond with JSON" isn't always enough

Students completing this lab can confidently integrate any LLM provider into their Capstone projects.

---

## Common Errors & Solutions

### Error 1: "Connection refused" for Ollama/LM Studio
**Cause:** Local server not running  
**Fix:** Start the service before running the notebook

### Error 2: "Invalid API key" for cloud providers
**Cause:** .env file not loaded or keys expired  
**Fix:** 
```python
print(os.getenv('OPENAI_API_KEY'))  # Debug: check if loaded
load_dotenv(override=True)  # Force reload
```

### Error 3: "JSONDecodeError" when parsing results
**Cause:** o3-mini returned markdown-wrapped JSON (```json ... ```)  
**Fix:**
```python
results = results.strip().removeprefix("```json").removesuffix("```")
results_dict = json.loads(results)
```

### Error 4: Rate limits on free tiers
**Cause:** Too many requests in short period  
**Fix:** Add delays between API calls:
```python
import time
time.sleep(1)  # Wait 1 second between requests
```

---

## Further Reading

### Agentic AI Evaluation
- [LangSmith Evaluation Guide](https://docs.smith.langchain.com/evaluation)
- [OpenAI Evals Framework](https://github.com/openai/evals)
- [Anthropic's Constitutional AI Paper](https://arxiv.org/abs/2212.08073) (LLMs judging LLMs)

### Multi-Provider Integration
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Ollama GitHub](https://github.com/ollama/ollama)

### Production Patterns
- [LangChain Model I/O](https://python.langchain.com/docs/modules/model_io/)
- [LiteLLM](https://github.com/BerriAI/litellm) (Unified LLM interface library)

---

## Next Steps

After completing this notebook, you should:
1. ✅ Be comfortable calling any LLM API
2. ✅ Understand cost/performance trade-offs
3. ✅ Know when to use local vs. cloud inference
4. ✅ Be ready for Async Programming & Structured Output

**Suggested Homework:** Modify the notebook to evaluate LLMs on a domain-specific task (e.g., "Write SQL for this natural language query") and analyze which models excel at code generation.
