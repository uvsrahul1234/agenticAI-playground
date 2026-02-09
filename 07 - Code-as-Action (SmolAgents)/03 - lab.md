# Module 07: Code-as-Action (SmolAgents)
## Lab - Independent Application

**Duration:** 90-120 minutes (Take-Home)  
**Due:** [Instructor to specify]  
**Submission:** Jupyter Notebook (.ipynb) or Python script (.py) with markdown documentation  
**Goal:** Reinforce skills through independent construction with a novel problem

---

## Lab Learning Objectives

By completing this lab, you will demonstrate the ability to:
1. Set up a secure CodeAgent environment with proper API key management
2. Solve a novel algorithmic problem using code-generating agents
3. Compare local vs. sandbox execution empirically
4. Create and integrate custom tools into an agent's toolbox
5. Debug agent-generated code and analyze failure modes
6. Make engineering trade-off decisions between different agent architectures

---

## Lab Overview: The Twist

**⚠️ Important:** This lab intentionally uses a DIFFERENT problem than the demo to ensure you understand the underlying concepts, not just the Fibonacci example.

**Your Challenge:** Build a CodeAgent that solves logic puzzles and mathematical problems using dynamically generated code. Instead of Fibonacci, you'll work with:
- **Prime number generation and analysis**
- **Tower of Hanoi puzzle**
- **Custom data transformation problems**

---

## Pre-Lab Setup (15 minutes)

### Task 1: Environment Configuration

#### 1.1 Create a New Project Directory

```bash
mkdir smolagents_lab
cd smolagents_lab
```

#### 1.2 Install Required Packages

```bash
# Core installation
pip install smolagents

# Toolkit (for base tools)
pip install 'smolagents[toolkit]'

# Choose ONE sandbox option:
pip install 'smolagents[modal]'    # Recommended
# OR
pip install 'smolagents[docker]'   # Alternative

# Environment management
pip install python-dotenv
```

#### 1.3 Create Your .env File

**Create a file named `.env` in your project directory:**

```plaintext
# .env file
# DO NOT commit this to Git! Add to .gitignore

# HuggingFace Token (for models)
HF_TOKEN=your_token_here

# Optional: Other API keys
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

**✅ Checkpoint:** Verify your setup:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Check if token is loaded
token = os.getenv("HF_TOKEN")
if token:
    print("✓ HF_TOKEN loaded successfully")
    print(f"  Token length: {len(token)} characters")
else:
    print("❌ HF_TOKEN not found. Check your .env file")
```

---

## Part 1: Basic CodeAgent Setup (20 minutes)

### Task 1.1: Initialize a Secure CodeAgent

Create a Python script or Jupyter notebook and implement the following:

```python
"""
Lab 07 - Part 1: Basic CodeAgent Setup
Student Name: [Your Name]
Date: [Date]
"""

import os
from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel

# Load environment variables
load_dotenv()

# TODO: Initialize the model securely
# Requirements:
# - Use InferenceClientModel
# - Model ID: "Qwen/Qwen2.5-72B-Instruct"
# - Load token from environment variable (NOT hardcoded!)

# YOUR CODE HERE


# TODO: Create a CodeAgent with no tools
# Requirements:
# - Empty tools list
# - add_base_tools=False
# - verbosity_level=2 (so you can see what's happening)

# YOUR CODE HERE


# Test your agent
test_task = "What is the 50th prime number?"
print(f"Testing agent with task: {test_task}")

# TODO: Run the agent and store the result
# YOUR CODE HERE

print(f"Result: {result}")
```

**Expected Output:**
Your agent should generate code to find the 50th prime number and return: `229`

**Verification Questions (answer in comments):**
1. How many steps did your agent take to solve this problem?
2. What algorithm did the agent choose (Sieve of Eratosthenes, trial division, etc.)?
3. Did the agent use any error handling in its code?

---

### Task 1.2: Analyze Agent Logs

```python
# TODO: Inspect the agent's logs
# Print the following information:
# 1. Total number of steps
# 2. The reasoning/thought process before code generation
# 3. The actual code that was generated

# YOUR CODE HERE


# TODO: Convert logs to memory messages
# Compare the difference between raw logs and memory messages

# YOUR CODE HERE
```

**Reflection Question:** Write 2-3 sentences explaining the difference between `agent.logs` and `agent.write_memory_to_messages()`. When would you use each?

---

## Part 2: The Tower of Hanoi Challenge (25 minutes)

### Background: Tower of Hanoi

The Tower of Hanoi is a mathematical puzzle with three rods and n disks of different sizes. The objective is to move the entire stack from one rod to another, following these rules:
1. Only one disk can be moved at a time
2. A disk can only be moved if it's the uppermost disk on a stack
3. No disk may be placed on top of a smaller disk

### Task 2.1: Solving Tower of Hanoi with CodeAgent

```python
"""
Lab 07 - Part 2: Tower of Hanoi Solver
"""

# TODO: Create a new CodeAgent (reuse your setup from Part 1)
# YOUR CODE HERE

# The challenge
hanoi_task = """
Solve the Tower of Hanoi puzzle for n=5 disks.
Write Python code that:
1. Generates the sequence of moves
2. Counts the total number of moves
3. Returns both the move sequence and the count

The optimal number of moves for n disks is 2^n - 1.
Verify your solution gives the correct count.
"""

print("Tower of Hanoi Challenge (n=5):")
print("="*50)

# TODO: Run the agent with this task
# YOUR CODE HERE

print(f"Result: {result}")
```

**Expected Output:**
- Total moves: 31 (which is 2^5 - 1)
- A sequence showing each move (e.g., "Move disk 1 from A to C")

---

### Task 2.2: Scaling Analysis

```python
"""
Test how the agent handles different problem scales
"""

# TODO: Run the Tower of Hanoi for n=3, n=5, and n=7
# Record the execution time and verify the move count

import time

test_cases = [3, 5, 7]
results = {}

for n in test_cases:
    task = f"Solve Tower of Hanoi for {n} disks and return the total move count."
    
    # TODO: Time the execution and store results
    # YOUR CODE HERE
    
    print(f"n={n}: {results[n]['moves']} moves in {results[n]['time']:.2f} seconds")

# Analysis Question: Does execution time scale linearly with n? Why or why not?
```

**Reflection Questions:**
1. How did the agent approach this problem differently than the prime number problem?
2. Did the agent use recursion or iteration? Why might it have made that choice?
3. What would happen if you asked for n=20? Would the agent complete it?

---

## Part 3: Local vs. Sandbox Execution (20 minutes)

### Task 3.1: Benchmark Local Execution

```python
"""
Lab 07 - Part 3: Execution Environment Comparison
"""

import time
from smolagents import CodeAgent, InferenceClientModel

# Initialize model
model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-72B-Instruct",
    token=os.getenv("HF_TOKEN")
)

# Benchmark task
benchmark_task = "Calculate the sum of all prime numbers less than 1000"

# TODO: Create LOCAL execution agent
print("Testing LOCAL Execution:")
print("-"*50)

local_agent = CodeAgent(
    tools=[],
    model=model,
    # Note: No executor_type specified = local execution
)

start_time = time.time()
# YOUR CODE HERE - run the task
local_execution_time = time.time() - start_time

print(f"Local Execution Time: {local_execution_time:.2f} seconds")
print(f"Result: {local_result}")
```

---

### Task 3.2: Benchmark Sandbox Execution

```python
# TODO: Create SANDBOX execution agent
print("\nTesting SANDBOX Execution (Modal):")
print("-"*50)

with CodeAgent(
    tools=[],
    model=model,
    executor_type="modal"  # or "docker" if you prefer
) as sandbox_agent:
    
    start_time = time.time()
    # YOUR CODE HERE - run the same task
    sandbox_execution_time = time.time() - start_time
    
    print(f"Sandbox Execution Time: {sandbox_execution_time:.2f} seconds")
    print(f"Result: {sandbox_result}")

# Verify results match
assert local_result == sandbox_result, "Results don't match! Something's wrong."
print("\n✓ Results verified: Local and Sandbox match")
```

---

### Task 3.3: Performance Analysis

```python
# TODO: Create a comparison table
print("\nPerformance Comparison:")
print("="*60)
print(f"{'Metric':<30} {'Local':<15} {'Sandbox':<15}")
print("="*60)
print(f"{'Execution Time (seconds)':<30} {local_execution_time:<15.2f} {sandbox_execution_time:<15.2f}")

overhead = ((sandbox_execution_time - local_execution_time) / local_execution_time) * 100
print(f"{'Sandbox Overhead (%)':<30} {'—':<15} {overhead:<15.1f}")
print("="*60)
```

**Critical Analysis Questions (answer in markdown):**

1. **Performance:** What was the percentage overhead of sandbox execution? Is this acceptable for production use?

2. **Security:** Given this performance trade-off, in which scenarios would you MANDATE sandbox execution despite the overhead?

3. **Trade-offs:** For a high-volume production system (1000+ requests/day), how would you balance security and performance?

---

## Part 4: Custom Tool Creation (25 minutes)

### Task 4.1: Create a Data Validator Tool

```python
"""
Lab 07 - Part 4: Custom Tool Integration
"""

from smolagents import Tool

# TODO: Implement a custom tool that validates if a number is a perfect square
class PerfectSquareChecker(Tool):
    name = "perfect_square_checker"
    description = "Checks if a given number is a perfect square and returns the square root if it is"
    
    inputs = {
        "number": {
            "type": "number",
            "description": "The number to check"
        }
    }
    output_type = "string"
    
    def forward(self, number: float):
        """
        TODO: Implement the logic
        - Check if number is a perfect square
        - If yes, return: "Yes, {number} is a perfect square. Square root: {sqrt}"
        - If no, return: "No, {number} is not a perfect square"
        """
        # YOUR CODE HERE
        pass
```

---

### Task 4.2: Integrate Custom Tool with Agent

```python
# TODO: Create agent and add your custom tool
model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-72B-Instruct",
    token=os.getenv("HF_TOKEN")
)

agent = CodeAgent(tools=[], model=model)

# Add your custom tool
perfect_square_tool = PerfectSquareChecker()
agent.tools[perfect_square_tool.name] = perfect_square_tool

print(f"Tools available: {list(agent.tools.keys())}")

# Test the custom tool integration
test_task = """
Use the perfect_square_checker tool to verify if the following numbers
are perfect squares: 144, 150, 169, 200, 225

Return a summary of which numbers are perfect squares.
"""

result = agent.run(test_task)
print("Result:", result)
```

**Verification:** Your agent should identify that 144 (12²), 169 (13²), and 225 (15²) are perfect squares, while 150 and 200 are not.

---

### Task 4.3: Create a Second Custom Tool

**Challenge:** Create a tool that generates the first n numbers in the Collatz sequence for a given starting number.

**Background:** The Collatz conjecture states that for any positive integer n:
- If n is even: divide it by 2
- If n is odd: multiply by 3 and add 1
- Repeat until you reach 1

```python
# TODO: Implement CollatzSequenceGenerator tool
class CollatzSequenceGenerator(Tool):
    # YOUR CODE HERE
    pass

# TODO: Add to agent and test with starting number 27
# YOUR CODE HERE
```

---

## Part 5: Debugging & Error Handling (20 minutes)

### Task 5.1: Intentional Error Scenario

```python
"""
Lab 07 - Part 5: Debugging Agent Failures
"""

# This task is intentionally ambiguous and may cause errors
problematic_task = """
Find the largest prime factor of 600851475143 and then
calculate its factorial.
"""

agent = CodeAgent(tools=[], model=model, verbosity_level=2)

try:
    result = agent.run(problematic_task)
    print("Result:", result)
except Exception as e:
    print(f"Error occurred: {e}")
    
# TODO: Inspect the logs to understand what went wrong
# YOUR CODE HERE
```

**Debugging Checklist:**
1. ✅ Did the agent correctly identify the largest prime factor?
2. ✅ Did the factorial calculation complete or time out?
3. ✅ Were there any syntax errors in the generated code?
4. ✅ If it failed, at which step did the failure occur?

---

### Task 5.2: Implement Guardrails

```python
# TODO: Modify the agent to have a maximum step limit
agent_with_limit = CodeAgent(
    tools=[],
    model=model,
    max_steps=5  # Limit to 5 steps maximum
)

# Test with a task that might run long
long_task = "Generate the first 1000 prime numbers and return their sum"

# YOUR CODE HERE - run and observe behavior
```

**Analysis Question:** What happened when the agent hit the step limit? How did it handle the incomplete task?

---

## Part 6: Comparative Analysis (15 minutes)

### Task 6.1: CodeAgent vs. ToolCallingAgent

```python
"""
Lab 07 - Part 6: Architecture Comparison
"""

from smolagents import CodeAgent, ToolCallingAgent, InferenceClientModel

model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-72B-Instruct",
    token=os.getenv("HF_TOKEN")
)

# Same task for both agents
comparison_task = "What is the greatest common divisor (GCD) of 48 and 18?"

# TODO: Test with CodeAgent
code_agent = CodeAgent(tools=[], model=model)
code_result = code_agent.run(comparison_task)
print("CodeAgent result:", code_result)

# TODO: Test with ToolCallingAgent
# Note: You'll need to add a GCD tool first
# YOUR CODE HERE
```

---

### Task 6.2: Decision Matrix

Create a markdown table comparing when to use each agent type:

```markdown
## My Architecture Decision Matrix

| Scenario | CodeAgent | ToolCallingAgent | Justification |
|----------|-----------|------------------|---------------|
| Math puzzle solving | [Your answer] | [Your answer] | [Your reasoning] |
| API data fetching | [Your answer] | [Your answer] | [Your reasoning] |
| Multi-step data transformation | [Your answer] | [Your answer] | [Your reasoning] |
| Production financial calculations | [Your answer] | [Your answer] | [Your reasoning] |
```

---

## Lab Submission Requirements

### Deliverables

1. **Code Submission:**
   - Jupyter Notebook (.ipynb) OR Python script (.py)
   - All code cells must execute without errors
   - Include markdown documentation for each section

2. **Required Files:**
   - `lab07_submission.ipynb` or `lab07_submission.py`
   - `.env.example` file (without actual keys) showing required environment variables
   - `README.md` explaining setup instructions

3. **Analysis Report:**
   Include written responses to all reflection questions:
   - Part 1.2: Logs vs. Memory analysis
   - Part 2.2: Scaling analysis
   - Part 3.3: Performance trade-off analysis
   - Part 5.2: Guardrails behavior analysis
   - Part 6.2: Decision matrix with justifications

---

## Assessment Rubric

### Pass Criteria (100 points total)

#### Technical Implementation (60 points)
- ✅ **Environment Setup (10 pts):** Secure .env configuration, no hardcoded keys
- ✅ **Basic CodeAgent (10 pts):** Successfully solves prime number and Tower of Hanoi
- ✅ **Execution Comparison (10 pts):** Both local and sandbox execution working
- ✅ **Custom Tools (15 pts):** Two working custom tools integrated correctly
- ✅ **Debugging (15 pts):** Successful error analysis and guardrails implementation

#### Analysis & Reflection (30 points)
- ✅ **Log Analysis (5 pts):** Clear understanding of logs vs. memory
- ✅ **Performance Analysis (10 pts):** Comprehensive comparison of local vs. sandbox
- ✅ **Architecture Decisions (10 pts):** Well-reasoned decision matrix
- ✅ **Code Quality (5 pts):** Clean, documented, reproducible code

#### Reproducibility (10 points)
- ✅ **Setup Documentation (5 pts):** Clear instructions for running your code
- ✅ **Execution (5 pts):** Code runs on instructor's machine without modification

---

### Fail Criteria (Automatic Failure)

❌ **Security Violation:** Hardcoded API keys anywhere in submitted code  
❌ **Non-Reproducible:** Code crashes due to missing dependencies or environment issues  
❌ **Plagiarism:** Code copied from demo without "The Twist" implementation  
❌ **Lab is Exact Demo Copy:** Must solve different problems than demo examples

---

## Bonus Challenges (Optional - Extra Credit)

### Bonus 1: Multi-Agent Coordination (10 points)
Implement a scenario where one CodeAgent generates code and another CodeAgent reviews and improves it.

### Bonus 2: Cost Optimization (10 points)
Calculate the token cost of your agent runs and propose strategies to reduce costs by 50% while maintaining quality.

### Bonus 3: Custom Evaluation Suite (15 points)
Create an automated testing framework that runs your agent against 10 different logic puzzles and reports success rate.

---

## Resources & Help

### Troubleshooting Guide

**Problem:** "ModuleNotFoundError: No module named 'smolagents'"
- **Solution:** Run `pip install smolagents`

**Problem:** "Token not found" errors
- **Solution:** Check your .env file is in the correct directory and `load_dotenv()` is called

**Problem:** Sandbox execution fails
- **Solution:** Check Modal/Docker installation and credentials

**Problem:** Agent generates incorrect code
- **Solution:** Increase `verbosity_level`, inspect logs, check tool descriptions

### Additional Resources
- SmolAgents Documentation: https://github.com/huggingface/smolagents
- HuggingFace Inference API: https://huggingface.co/docs/api-inference
- Modal Documentation: https://modal.com/docs

---

## Final Reflection (Required)

After completing all tasks, write a 1-2 paragraph reflection addressing:

1. What was the most challenging aspect of this lab?
2. How does the Code-as-Action paradigm differ from traditional chatbots?
3. In what real-world applications would you use CodeAgent over ToolCallingAgent?
4. What ethical concerns should developers consider when deploying code-generating agents?

---

**Good luck, and remember:** The goal isn't to copy the demo exactly—it's to understand the principles deeply enough to apply them to novel problems. If you truly understand SmolAgents, you should be able to solve ANY logic puzzle, not just Fibonacci!

---

*End of Lab Assignment*
