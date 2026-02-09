# Module 07: Code-as-Action (SmolAgents)
## Glossary - Theory & Concepts

**Target Audience:** Agentic AI Class  
**Module Duration:** 60 minutes (Lecture)  
**Learning Objective:** Understand the theoretical foundations of code-generating agents and the paradigm shift from text prediction to executable action.

---

## Core Concept Definitions

### 1. Code-as-Action Paradigm

**Definition:** A design philosophy where agents solve problems by dynamically generating and executing code rather than simply predicting text or calling predefined API endpoints.

**Why It Matters:** Research papers, including "Executable Code Actions Elicit Better LLM Agents," demonstrate that having LLMs write actions in code significantly outperforms JSON-based tool calling for complex, multi-step reasoning tasks.

**Real-World Analogy:** Think of the difference between giving someone a restaurant menu (JSON tool calling) versus teaching them to cook (code generation). The menu limits them to predefined options, while cooking skills let them create novel dishes by combining ingredients dynamically.

---

### 2. CodeAgent vs. ToolCallingAgent

SmolAgents provides two distinct agent architectures representing different paradigms for how agents interact with tools.

#### **CodeAgent**

**Definition:** An agent that generates tool calls as Python code snippets and executes them either locally or in a secure sandbox environment.

**Characteristics:**
- **Tools are exposed as:** Python functions (via bindings)
- **Execution:** Code is executed in Python interpreter
- **Example of tool call:**
```python
result = search_docs("What is the capital of France?")
print(result)
```

**Strengths:**
- **Highly expressive:** Allows for complex logic, control flow, and can combine tools, loop, transform, and reason
- **Flexible:** No need to predefine every possible action; can dynamically generate new actions
- **Emergent reasoning:** Ideal for multi-step problems or dynamic logic
- **Composability:** Can nest function calls, define variables, create loops, and build complex workflows

**Limitations:**
- **Risk of errors:** Must handle syntax errors and exceptions
- **Less predictable:** More prone to unexpected or unsafe outputs
- **Requires secure execution environment:** Code execution can be dangerous if not sandboxed properly

**When to use CodeAgent:**
- You need reasoning, chaining, or dynamic composition
- Tools are functions that can be combined (e.g., parsing + math + querying)
- Your agent is a problem solver or programmer
- You're tackling algorithmic or computational problems

---

#### **ToolCallingAgent**

**Definition:** An agent that writes tool calls as structured JSON, following the common format used in many frameworks (OpenAI API, Anthropic, etc.).

**Characteristics:**
- **Tools are defined as:** JSON schema with name, description, parameter types
- **Execution:** Structured and validated against schema
- **Example of tool call:**
```json
{
  "tool_call": {
    "name": "search_docs",
    "arguments": {
      "query": "What is the capital of France?"
    }
  }
}
```

**Strengths:**
- **Reliable:** Less prone to hallucination; outputs are structured and validated
- **Safe:** Arguments are strictly validated; no risk of arbitrary code running
- **Interoperable:** Easy to map to external APIs or services

**Limitations:**
- **Low expressivity:** Can't easily combine or transform results dynamically
- **Inflexible:** Must define all possible actions in advance; limited to predefined tools
- **No code synthesis:** Limited to tool capabilities as defined

**When to use ToolCallingAgent:**
- You have simple, atomic tools (e.g., call an API, fetch a document)
- You want high reliability and clear validation
- Your agent is like a dispatcher or controller
- You're working with external APIs that require strict validation

---

### 3. Tools in SmolAgents

**Definition:** A tool is an atomic function to be used by an agent. To be used by an LLM, it needs a few attributes that constitute its API.

**Required Tool Attributes:**
- **Name:** Identifier for the tool
- **Description:** Explains what the tool does (crucial for LLM understanding)
- **Input types and descriptions:** What parameters the tool accepts
- **Output type:** What the tool returns
- **Forward method:** The actual implementation that performs the action

**How Tools Work:**
When an agent is initialized, tool attributes are used to generate a tool description which is baked into the agent's system prompt. This lets the agent know which tools it can use and why.

---

### 4. Default Toolbox

SmolAgents comes with a default toolbox (installed with `smolagents[toolkit]`) that can be added to your agent with `add_base_tools=True`:

1. **DuckDuckGo Web Search:** Performs web searches using DuckDuckGo browser
2. **Python Code Interpreter:** Runs LLM-generated Python code in a secure environment (only added to ToolCallingAgent with `add_base_tools=True`, since CodeAgent already natively executes Python code)
3. **Transcriber:** Speech-to-text pipeline built on Whisper-Turbo

---

### 5. Execution Environments: Local vs. Sandbox

One of the critical security considerations in code-generating agents is **where** the code executes.

#### **Local Execution**

**Definition:** Python code execution happens in your local Python environment.

**Characteristics:**
- **Simple to set up:** Default behavior for CodeAgent
- **Limited safety:** Only functions that can be called are provided tools and predefined safe functions (print, math module)
- **Risk:** Still executing potentially dangerous code locally

**When safe to use:**
- Trusted models
- Simple, well-understood tools
- Development/testing environments

---

#### **Sandbox Execution**

**Definition:** Python code executes in an isolated environment separate from your main system.

**Two Approaches:**

##### **Approach 1: Running Individual Code Snippets in a Sandbox**
- Only the agent-generated Python code snippets run in sandbox
- Rest of the agentic system (agent, model, tools) stays in local environment
- Simpler to set up using: `executor_type="blaxel"`, `executor_type="e2b"`, `executor_type="modal"`, or `executor_type="docker"`
- **Limitation:** Doesn't support multi-agent systems; still requires passing state data between environments

##### **Approach 2: Running the Entire Agentic System in a Sandbox**
- Everything (agent, model, tools) runs within the sandbox environment
- Better isolation and security
- More complex setup; may require passing sensitive credentials (API keys) to sandbox
- Supports multi-agent architectures

**Supported Sandbox Options:**
- **E2B Sandbox:** Cloud-based secure sandbox
- **Modal:** Serverless platform for running Python code
- **Docker:** Containerized local execution
- **Blaxel:** Lightweight sandboxing solution

---

### 6. Agent Memory and Logging

Understanding how agents track their work is crucial for debugging and optimization.

#### **agent.logs**

**Definition:** Stores fine-grained logs of the agent. At every step of the agent's run, everything gets stored in a dictionary that is then appended to `agent.logs`.

**Use case:** Detailed debugging and understanding every single step

#### **agent.write_memory_to_messages()**

**Definition:** Writes the agent's memory as a list of chat messages for the Model to view. This method goes over each step of the log and only stores what it's interested in as messages.

**What gets stored:**
- System prompt and task in separate messages
- LLM output as a message for each step
- Tool call output as another message

**Use case:** Higher-level view of what happened; not every log will be transcribed by this method

---

### 7. Why Code is Better Than JSON for Tool Calling

Based on research and practical experience, code provides superior expressiveness for agentic actions:

**Advantages of Code Over JSON:**

1. **Composability:** Can you nest JSON actions within each other or define a set of JSON actions to reuse later, the same way you could define a Python function? No.

2. **Object Management:** How do you store the output of an action like `generate_image()` in JSON? It's awkward and limited.

3. **Generality:** Code is built to express simply anything you can have a computer do. JSON is designed for data serialization.

4. **Representation in LLM Training Corpus:** Why not leverage the fact that plenty of quality actions have already been included in LLM training corpus as code? LLMs have seen millions of examples of Python code solving problems.

**The Bottom Line:** If JSON snippets were a better way to express actions, our programming languages would have been written in JSON. Code is fundamentally better suited for expressing computational actions.

---

## Architectural Visualization

### The CodeAgent Execution Flow

```
┌─────────────────┐
│   User Task     │
│ "Calculate the  │
│  100th Fibonacci│
│    number"      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│   LLM (Language Model)          │
│  - Receives task                │
│  - Has access to system prompt  │
│  - Knows available tools        │
└────────┬────────────────────────┘
         │ Generates
         ▼
┌─────────────────────────────────┐
│   Python Code Snippet           │
│                                 │
│  def fibonacci(n):              │
│      if n <= 1: return n        │
│      a, b = 0, 1                │
│      for _ in range(2, n + 1):  │
│          a, b = b, a + b        │
│      return b                   │
│                                 │
│  result = fibonacci(100)        │
│  final_answer(result)           │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Code Executor                  │
│  (Local or Sandbox)             │
│  - Parses Python code           │
│  - Executes in safe environment │
│  - Returns result               │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Final Answer                   │
│  354224848179261915075          │
└─────────────────────────────────┘
```

**Key Architectural Insight:** The agent doesn't just retrieve information—it **computes** solutions by writing and executing algorithms on the fly.

---

## Decision Matrix: When to Use SmolAgents

### Trade-off 1: Expressiveness vs. Safety

| Dimension | CodeAgent | ToolCallingAgent |
|-----------|-----------|------------------|
| **Expressiveness** | High - Can write arbitrary logic | Low - Limited to predefined tools |
| **Safety** | Requires sandboxing | Inherently safer, validated inputs |
| **Best for** | Complex reasoning tasks | Simple API calls |

**Engineering Decision:** For production systems handling untrusted inputs, always use sandboxed execution with CodeAgent. For controlled environments with complex logic requirements, CodeAgent is superior.

---

### Trade-off 2: Flexibility vs. Predictability

| Dimension | CodeAgent | ToolCallingAgent |
|-----------|-----------|------------------|
| **Flexibility** | Can solve novel problems | Constrained to tool definitions |
| **Predictability** | May produce unexpected code | Structured, validated outputs |
| **Debugging** | Harder - arbitrary code | Easier - known tool contracts |

**Engineering Decision:** For exploratory, research-oriented tasks (data analysis, algorithm design), CodeAgent shines. For production pipelines with known workflows, ToolCallingAgent provides more predictability.

---

### Trade-off 3: Local vs. Sandbox Execution

| Dimension | Local Execution | Sandbox Execution |
|-----------|-----------------|-------------------|
| **Setup Complexity** | Simple | More complex |
| **Security** | Limited - code runs in your environment | High - isolated execution |
| **Performance** | Faster - no overhead | Slightly slower - container/VM overhead |
| **Multi-Agent Support** | Yes | Depends on approach |

**Engineering Decision:** Always use sandbox execution for:
- Production applications
- Untrusted models
- Internet-facing systems
- Multi-tenant environments

Use local execution only for:
- Development and testing
- Trusted, well-understood models
- Personal, non-production experimentation

---

## Key Takeaways

1. **Code-as-action is fundamentally more expressive than JSON-based tool calling** because programming languages are designed specifically for expressing computational actions.

2. **CodeAgent is ideal for problems requiring reasoning, composition, and dynamic logic**, while ToolCallingAgent is better for simple, atomic tool calls with strict validation requirements.

3. **Security requires sandboxing**: Always execute agent-generated code in isolated environments (E2B, Modal, Docker) for production use cases.

4. **Tools are the building blocks**: A well-designed tool with clear descriptions enables the LLM to understand when and how to use it effectively.

5. **SmolAgents represents a paradigm shift from "LLMs that predict text" to "LLMs that execute actions"** by leveraging the full power of programming languages.

---

## Preparation for Demo

In the next phase, you'll see a live demonstration of a CodeAgent solving the classic Fibonacci problem. Pay attention to:

1. How the agent **reasons** about the problem before writing code
2. The **structure** of the generated Python code
3. How **tools** are made available to the agent
4. The **difference** between local and sandbox execution
5. How to **debug** when the agent generates incorrect code

**Thought Exercise Before Demo:** If you were an LLM, would you prefer to express "get the 100th Fibonacci number" as a JSON object or as Python code? Why?

---

*End of Glossary - Proceed to Demo (Analysis)*
