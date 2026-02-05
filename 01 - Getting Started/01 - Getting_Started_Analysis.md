# Getting Started - Detailed Instructor Analysis

## Course Framework Integration

### Three-Phase Learning Cycle

To maximize mastery of Agentic AI, this course utilizes a three-phase learning cycle for every module. We purposefully separate conceptual "Theory" from practical "Application" to ensure you understand not just how to write code, but why the architecture is designed that way.

For each topic, we follow this sequence:

#### 1. Theory & Concepts (The Lecture)
We begin by establishing the vocabulary and mental models required for the week. We cover definitions, architectural diagrams, and decision-making strategies without getting bogged down in syntax immediately. This phase ensures you understand the "blueprint" before building.

#### 2. Guided Analysis (The Live Demo)
Once theory is established, we move to an interactive, instructor-led demonstration in class. Rather than looking at static code, you can observe the workflow in real-time. We walk through an "Analysis Notebook" together, predicting outcomes, debugging live errors, and discussing results as they happen. This gives you a safe space to observe LLM behavior and ask "what if?" questions before working independently.

#### 3. Independent Lab (The Application)
Finally, you will solidify skills through a take-home Lab assignment. While the Lab builds upon concepts from the Demo, it challenges them to implement independently in your own environment. This ensures you encounter the material a second time—moving from observation in the classroom to execution on their own machine.

---

## Executive Summary

This **Getting Started** module establishes the foundational development environment required for all subsequent agentic AI coursework. Unlike later modules that focus on agent architecture and LLM integration, this module emphasizes **reproducible development environments, security best practices, and professional tooling workflows**.

You will learn to:
- Configure a modern Python environment using **UV** (fast, reliable package management)
- Secure API credentials using **.env files** and environment variables
- Set up VS Code with essential extensions for data science and AI development
- Organize projects using **Google Drive for Desktop** for collaboration
- Understand the tooling ecosystem that underpins production AI systems

**Why This Module Is Critical:** In production agentic systems, environment inconsistencies ("works on my machine") are the #1 cause of deployment failures. This module teaches you to build **reproducible, secure, portable** environments from day one.

---

## Module Learning Objectives

### Primary Competencies (from Course Framework)

#### **C1. Reproducible Environments (uv)**
**Skill:** Configure isolated Python environments with locked dependencies using UV

**Why It Matters:**
- Agentic projects have complex dependency trees (LangChain, CrewAI, vector databases)
- Traditional tools (pip, conda) are slow and inconsistent
- UV provides Rust-speed package resolution and deterministic builds

---

#### **D1. Security Best Practices**
**Skill:** Manage API keys securely using .env files and gitignore patterns

**Why It Matters:**
- Agentic systems connect to paid APIs (OpenAI, Anthropic)
- Exposing API keys in Git costs thousands (bots scrape GitHub for keys)
- Professional developers NEVER hardcode credentials

---

#### **C2. Professional Tooling Setup**
**Skill:** Configure VS Code with Jupyter, Python, and AI coding assistants

**Why It Matters:**
- VS Code is the industry-standard editor for AI development
- Extensions like Pylance and Copilot accelerate learning
- Jupyter integration enables iterative experimentation

---

### Secondary Competencies

#### **Project Organization**
**Skill (Optional):** Use Google Drive for Desktop to sync code across devices

**Why It Matters:**
- Automatic backups prevent data loss
- Enables collaboration on team projects
- Streamlines submission workflow for assignments

---

#### **Debugging Mindset**
**Skill:** Troubleshoot environment issues systematically

**Why It Matters:**
- 80% of frustration stems from setup problems
- Learning to debug PATH issues, permissions, and dependencies is transferable
- Builds confidence for later technical challenges

---

## Pedagogical Strategy

### Why We Start Here

**Traditional Approach (BAD):**
1. Dive into LangChain code immediately
2. Different Python versions, package managers, IDEs
3. "ImportErrors" 
4. Spending hours debugging environments

**Our Approach (GOOD):**
1. **One week** of unified setup (this module)
2. Everyone has identical environments (UV + pyproject.toml)
3. Common problems solved once via documentation
4. Moving onwards: focus on AI concepts, not tooling

---

## Module Content Breakdown

### Component 1: Google Drive for Desktop (Optional but Recommended)

#### Learning Objectives
- Understand cloud storage vs. local storage
- Configure streaming file access to save disk space
- Enable offline mode for critical files

#### Conceptual Framework

**The Problem:** Loosing work, forgeting to backup, or accessing files across devices.

**The Solution:** Google Drive for Desktop mounts cloud storage as a local drive.

**Key Concepts:**
1. **Streaming vs. Offline:** Files download on-demand unless marked "available offline"
2. **Automatic Sync:** Changes propagate bidirectionally (local ↔ cloud)
3. **Collaboration:** Multiple team members can work on shared folders

#### Implementation Details

**Installation:**
- Download from: https://www.google.com/drive/download/
- Follow platform-specific wizard (Windows/Mac)
- Sign in with Google account
- Choose "Stream files" mode (saves disk space)

**Best Practices:**
- Keep `.env` files OUTSIDE the Drive folder (security)
- Use Drive for: code, notebooks, data files, documentation
- Mark project folders as "available offline" for stable access

**Common Issues:**
- **Sync conflicts:** Occur when editing same file on multiple devices simultaneously
  - Solution: Close files when switching devices
- **Quota limits:** Free accounts have 15GB
  - Solution: Clean up old files or upgrade
- **Slow sync:** Large files can take time
  - Solution: Use .gitignore patterns to exclude `venv`, `__pycache__`

---

### Component 2: VS Code Setup

#### Learning Objectives
- Install VS Code and essential extensions
- Configure Python interpreter selection
- Run a Jupyter notebook within VS Code
- Understand the role of each extension

#### Conceptual Framework

**The Problem:** Default text editors lack AI/data science features (autocomplete, debugging, variable inspection).

**The Solution:** VS Code with extensions transforms into a full-featured IDE.

**Why VS Code vs. Alternatives:**
- **Jupyter Lab:** Good for notebooks, weak for code projects
- **PyCharm:** Powerful but heavy, slow startup
- **VS Code:** Fast, extensible, industry standard

#### Core Extensions Explained

##### 1. Python (by Microsoft)
**Purpose:** Foundation for all Python development

**Features:**
- IntelliSense: Autocomplete based on imports and type hints
- Debugging: Set breakpoints, inspect variables
- Linting: Catch syntax errors before running
- Testing: Integrated pytest/unittest runners

**Agentic Use Case:** When building multi-file agent projects (Week 8+), IntelliSense suggests class methods from imported modules.

---

##### 2. Jupyter (by Microsoft)
**Purpose:** Run .ipynb notebooks natively in VS Code

**Features:**
- Variable explorer: See dataframe contents without print()
- Plot viewer: Interactive matplotlib/plotly graphs
- Cell execution: Run individual cells or entire notebook

**Why Not Use Browser Jupyter?**
- ✅ VS Code has better autocomplete
- ✅ Integrated with Git for version control
- ✅ Can edit .py files and .ipynb side-by-side

**Agentic Use Case:** All demo notebooks (Weeks 2-12) run in VS Code Jupyter.

---

##### 3. Pylance (by Microsoft)
**Purpose:** Fast, intelligent Python language server

**Features:**
- Type checking: Warns about mismatched types
- Import suggestions: Auto-adds missing imports
- Parameter hints: Shows function signatures as you type

**Technical Detail:** Pylance is a Rust-based rewrite of Python language tools, making it 5-10x faster than alternatives.

**Agentic Use Case:** When using Pydantic models (Week 3), Pylance catches schema mismatches before running code.

---

##### 4. Data Wrangler (by Microsoft)
**Purpose:** Visual dataframe cleaning and transformation

**Features:**
- GUI for pandas operations (filter, sort, drop columns)
- Auto-generates Python code for reproducibility
- Handles large datasets (100K+ rows)

**Use Case:** Preparing training data for fine-tuning (Week 11).

---

##### 5. Rainbow CSV (by mechatroner)
**Purpose:** Color-code CSV columns for readability

**Why It's Useful:** When inspecting tool outputs (e.g., web scraping results), colored columns prevent column misalignment errors.

---

##### 6. GitLens (by GitKraken)
**Purpose:** Supercharged Git integration

**Features:**
- Git blame: See who wrote each line
- File history: Visual timeline of changes
- Branch comparison: Diff between feature branches

**Agentic Use Case:** In team projects (Week 9+), trace which team member wrote a particular agent function.

---

##### 7. GitHub Copilot (by GitHub) - Optional but Recommended
**Purpose:** AI-powered code suggestions

**Features:**
- Completes entire functions from comments
- Suggests boilerplate code (API calls, data loading)
- Learns from your project's context

**Cost:** $10/month (free for students via GitHub Education)

**Ethical Note:** 
- ✅ Good for boilerplate (reducing tedious typing)
- ⚠️ Bad for learning (don't blindly accept suggestions)
- ❌ Never use on assignments without understanding the code

**Agentic Use Case:** Copilot can scaffold agent class structures, saving time on repetitive patterns.

---

#### Kernel Selection (Critical Step)

**What Is a Kernel?**
A kernel is the Python interpreter that executes notebook cells. It runs in the background as a separate process.

**Why Multiple Kernels?**
- System Python: `/usr/bin/python3` (don't use—no isolation)
- Anaconda base: `~/anaconda3/bin/python` (better, but shared)
- **UV environment: `~/project/.venv/bin/python` (best—project-specific)**

**Selection Process:**
1. Open a notebook in VS Code
2. Top-right corner: "Select Kernel"
3. Choose: "Python Environments" → select `.venv` folder
4. VS Code auto-installs `ipykernel` if missing

**Common Issue:** If kernel shows as "busy" forever:
- **Cause:** Python process crashed or infinite loop
- **Solution:** Interrupt kernel (stop button) or restart kernel (refresh button)

---

### Component 3: Environment Variables & .env Files

#### Learning Objectives
- Understand the difference between hardcoded secrets and environment variables
- Create and configure a .env file
- Load environment variables using python-dotenv
- Add .env to .gitignore

#### Conceptual Framework

**The Problem:** API keys are long, random strings. Developers are tempted to:
```python
# ❌ BAD: Hardcoded API key
openai_api_key = "sk-proj-abc123xyz..."
```

**Why This Is Dangerous:**
1. **GitHub Scrapers:** Bots scan public repos for `sk-` patterns
2. **Cost:** Stolen keys can rack up thousands in API charges
3. **Collaboration:** Hard to share code without exposing your personal keys
4. **Rotation:** If you change keys, you must edit every file

**The Solution:** Environment variables separate secrets from code.

---

#### How Environment Variables Work

**Operating System Level:**
Every process (Python script, terminal session) has access to a key-value store called "environment variables."

**Examples:**
- `PATH`: Directories to search for executables
- `HOME`: Current user's home directory
- `OPENAI_API_KEY`: Your API key (custom)

**Viewing in Terminal:**
```bash
# Windows
echo %OPENAI_API_KEY%

# Mac/Linux
echo $OPENAI_API_KEY
```

**Setting Temporarily:**
```bash
# Windows
set OPENAI_API_KEY=sk-proj-...

# Mac/Linux
export OPENAI_API_KEY=sk-proj-...
```

**Problem:** This only works for current terminal session. Close terminal → variable gone.

---

#### The .env File Solution

**Purpose:** Persistent storage for environment variables that loads automatically.

**Format:**
```
# .env file
KEY_NAME=value
ANOTHER_KEY=another_value
```

**Rules:**
- No spaces around `=`
- No quotes needed (unless value contains special characters)
- Comments start with `#`
- One variable per line

**Example .env for This Course:**
```
OPENAI_API_KEY=sk-proj-abc123xyz...
ANTHROPIC_API_KEY=sk-ant-def456uvw...
GROQ_API_KEY=gsk_ghi789rst...
GEMINI_API_KEY=AIzaSyjkl012mno...
HF_TOKEN=hf_pqr345stu...
WEATHER_API_KEY=wx_vwx678yz...
GEO_API_KEY=geo_abc901def...
```

---

#### Using python-dotenv

**Installation (should already be availabe but if needed):**
```bash
uv pip install python-dotenv
```

**Usage in Code:**
```python
import os
from dotenv import load_dotenv

# Load .env file into os.environ
load_dotenv()

# Access variables
api_key = os.getenv('OPENAI_API_KEY')
print(f"Key loaded: {api_key[:10]}...")  # Only show first 10 chars
```

**How It Works:**
1. `load_dotenv()` searches current directory (and parents) for `.env`
2. Parses each `KEY=value` line
3. Sets `os.environ['KEY'] = 'value'`
4. Your code retrieves via `os.getenv('KEY')`

**Important:** `load_dotenv()` should be called ONCE at the start of your script/notebook.

---

#### Security Best Practices

##### 1. Never Commit .env to Git

**Create .gitignore:**
```
# .gitignore
.env
.env.local
.env.production
*.key
```

**Verify:**
```bash
git status  # .env should NOT appear
```

**If You Accidentally Commit:**
```bash
# Remove from Git history (requires force push)
git rm --cached .env
git commit -m "Remove .env from tracking"
```

⚠️ **Even after removal, keys in Git history are compromised. Rotate all keys immediately.**

---

##### 2. Use .env.example for Documentation

**Create .env.example:**
```
# .env.example
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

**Purpose:** Shows collaborators which keys they need without exposing actual values.

**Workflow:**
1. Clone project
2. Copy `.env.example` to `.env`
3. Fill in real API keys
4. Run project

---

##### 3. Rotate Keys Periodically

**Why:** Even secure storage can be compromised (laptop stolen, phishing attack).

**Schedule:**
- High-value keys (payment APIs): Monthly
- Development keys: Every 3-6 months
- After team member leaves: Immediately

**How to Rotate:**
1. Generate new key in provider's dashboard
2. Update `.env` file
3. Delete old key from provider
4. Test that project still works

---

#### Common Errors & Solutions

##### Error 1: "KeyError: 'OPENAI_API_KEY'"
**Cause:** Variable not set in `.env` or `load_dotenv()` not called

**Solution:**
```python
# Debug: Print what's loaded
print(os.getenv('OPENAI_API_KEY'))  # Should not be None

# Use .get() with default
api_key = os.getenv('OPENAI_API_KEY', 'default_value')
```

---

##### Error 2: ".env file not found"
**Cause:** Working directory doesn't contain `.env`

**Solution:**
```python
# Explicitly specify path
from pathlib import Path
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)
```

---

##### Error 3: "API key invalid"
**Cause:** Copied key incorrectly (spaces, newlines)

**Solution:**
```python
# Strip whitespace
api_key = os.getenv('OPENAI_API_KEY', '').strip()
```

---

#### Assessment
- [ ] Created `.env` file with at least one API key
- [ ] Added `.env` to `.gitignore`
- [ ] Successfully loaded and printed API key (first 10 chars only)
- [ ] Understands why hardcoding keys is dangerous

---

### Component 4: UV Package Manager

#### Learning Objectives
- Understand why UV is superior to pip/conda
- Initialize a project with `pyproject.toml`
- Install dependencies with `uv sync`
- Manage tools with `uv tool install`

#### Conceptual Framework

**The Problem with Pip:**
- **Slow:** Resolves dependencies sequentially (minutes for complex projects)
- **Non-deterministic:** Different runs can install different versions
- **No locking:** `requirements.txt` doesn't pin transitive dependencies

**The Problem with Conda:**
- **Even slower:** Package resolution can take 10+ minutes
- **Bloated:** Installs many unnecessary packages
- **Conflicting ecosystems:** Mixing conda and pip causes chaos

**The UV Solution:**
- **Rust-based:** 10-100x faster than pip
- **Deterministic:** `uv.lock` ensures reproducible installs
- **PEP 621 compliant:** Uses modern `pyproject.toml` standard
- **Unified:** Replaces pip, pip-tools, virtualenv, and more

---

#### Installation

**Recommended: Standalone Installer**
```bash
# Mac/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

**Verify:**
```bash
uv --version  # Should show v0.x.x
```

**Update:**
```bash
uv self update
```

---

#### Project Structure

**Traditional Python Project:**
```
my_project/
├── main.py
├── requirements.txt  # ❌ No version locking
└── venv/             # ❌ Manual creation
```

**UV-Managed Project:**
```
my_project/
├── pyproject.toml    # ✅ Declares dependencies
├── uv.lock           # ✅ Locks exact versions
├── .venv/            # ✅ Auto-created
└── main.py
```

---

#### pyproject.toml Explained

**File Purpose:** Single source of truth for project metadata and dependencies.

**Example:**
```toml
[project]
name = "agentic-ai-project"
version = "0.1.0"
description = "Week 2 lab for Agentic AI course"
requires-python = ">=3.12"

dependencies = [
    "openai>=1.0.0",
    "anthropic>=0.8.0",
    "python-dotenv>=1.0.0",
    "requests>=2.31.0",
]

[tool.uv]
dev-dependencies = [
    "ipykernel>=6.0.0",
    "jupyter>=1.0.0",
]
```

**Sections Explained:**

##### `[project]`
- **name:** Package name (lowercase, hyphens)
- **version:** Semantic versioning (major.minor.patch)
- **requires-python:** Minimum Python version
- **dependencies:** Required for runtime

##### `dependencies = [...]`
- **Syntax:** `"package>=version"` or `"package==version"`
- **`>=` vs. `==`:**
  - `>=1.0.0`: Any version 1.0.0 or higher (flexible)
  - `==1.0.0`: Exactly 1.0.0 (rigid, rarely needed)
  - **Best Practice:** Use `>=` for libraries, `==` for known-broken versions

##### `[tool.uv]`
- **dev-dependencies:** Only needed for development (Jupyter, testing tools)
- **Not installed in production:** Keeps deployments lightweight

---

#### Core UV Commands

##### 1. Initialize a New Project
```bash
# Create project structure
uv init my-agentic-project
cd my-agentic-project

# Creates:
# ├── pyproject.toml
# └── hello.py (example file)
```

---

##### 2. Sync Dependencies
```bash
uv sync
```

**What It Does:**
1. Reads `pyproject.toml`
2. Resolves compatible versions (checks PyPI)
3. Downloads packages
4. Creates/updates `.venv/`
5. Generates `uv.lock` (exact versions)

**When to Run:**
- First time setting up project
- After editing `pyproject.toml`
- After `git pull` (someone added dependencies)

**Output:**
```
Resolved 47 packages in 312ms
Downloaded 12 packages in 1.2s
Installed 47 packages in 456ms
```

---

##### 3. Add a Dependency
```bash
# Add to pyproject.toml and install
uv add langchain

# Add specific version
uv add "langchain>=0.1.0"

# Add dev dependency
uv add --dev pytest
```

---

##### 4. Remove a Dependency
```bash
uv remove langchain
```

---

##### 5. Install Tools Globally
```bash
# Install crewai CLI globally (not project-specific)
uv tool install crewai

# Upgrade global tools
uv tool upgrade crewai

# List installed tools
uv tool list
```

**Use Case:** Tools like `crewai kickstart` that generate project templates.

---

##### 6. Python Version Management
```bash
# List available Python versions
uv python list

# Install a specific version
uv python install 3.12

# Pin project to specific version
uv python pin 3.12
```

---

#### Activating the Environment

**VS Code (Automatic):**
- Select `.venv` as kernel → automatically activated

**Terminal (Manual):**
```bash
# Mac/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Deactivate
deactivate
```

**How to Know It's Activated:**
```bash
# Prompt changes
(.venv) user@computer:~/project$

# Python points to venv
which python  # /home/user/project/.venv/bin/python
```

---

#### Migrating from Conda

**If You Have Conda Active:**
```bash
# Deactivate conda
conda deactivate

# Remove from PATH (optional, prevents conflicts)
# Edit ~/.bashrc or ~/.zshrc and comment out conda init lines
```

**Convert requirements.txt to pyproject.toml:**
```bash
# Read existing requirements
cat requirements.txt

# Manually add to pyproject.toml
uv add package1 package2 package3
```

---

#### Common Issues

##### Issue 1: "uv: command not found"
**Cause:** UV not in PATH

**Solution (Mac/Linux):**
```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

**Solution (Windows):**
Add `C:\Users\YourName\.cargo\bin` to System PATH.

---

##### Issue 2: "Cannot find package X"
**Cause:** Package name typo or not on PyPI

**Solution:**
```bash
# Search PyPI
uv pip search package_name

# Or visit: https://pypi.org
```

---

##### Issue 3: "Conflicting dependencies"
**Cause:** Two packages require incompatible versions

**Example:**
```
package-a requires requests>=2.31.0
package-b requires requests<2.30.0
```

**Solution:**
1. Check if newer versions resolve conflict
2. Use alternative packages
3. Pin to compatible versions manually

---

#### Assessment
- [ ] UV installed and updated to latest version
- [ ] Created a `pyproject.toml` for a test project
- [ ] Ran `uv sync` successfully
- [ ] Installed and listed tools with `uv tool install`
- [ ] Activated `.venv` and verified Python path

---

### Issue: VS Code Can't Find Python

**Symptoms:** "No Python interpreter selected"

**Diagnosis:**
1. Check if `.venv` folder exists
2. Check VS Code Python extension installed

**Solution:**
1. Run `uv sync` to create `.venv`
2. Reload VS Code window (Cmd+Shift+P → "Reload Window")
3. Manually select interpreter: Cmd+Shift+P → "Python: Select Interpreter" → Choose `.venv`

---

### Issue: API Call Fails

**Symptoms:** "AuthenticationError" or "KeyError"

**Diagnosis:**
1. Check if `.env` exists
2. Check if `load_dotenv()` called before accessing key
3. Check API key validity (expired/wrong)

**Solution:**
```python
# Debug script
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('OPENAI_API_KEY')

if key is None:
    print("❌ Key not loaded from .env")
elif not key.startswith('sk-proj-'):
    print("❌ Key format invalid")
else:
    print(f"✅ Key loaded: {key[:10]}...")
```

---

## Additional Resources

### Video Tutorials (Create These)
1. "UV Setup for Windows" (10 min)
2. "UV Setup for Mac" (10 min)
3. "VS Code Extensions Walkthrough" (15 min)
4. "API Key Security Best Practices" (5 min)

---

### Documentation Links
- UV Official Docs: https://docs.astral.sh/uv/
- VS Code Python Tutorial: https://code.visualstudio.com/docs/python/python-tutorial
- python-dotenv: https://pypi.org/project/python-dotenv/
- TOML Format: https://toml.io/en/

---

**Common Questions:**

**Q: "Do I need Anaconda if I have UV?"**
**A:** No. UV replaces both pip and conda. Deactivate conda with `conda deactivate`.

**Q: "Can I use PyCharm instead of VS Code?"**
**A:** Yes, but course demos use VS Code. You're responsible for figuring out PyCharm equivalents.

**Q: "What if I already have a project in pip/conda?"**
**A:** Migrate by creating `pyproject.toml` and running `uv sync`. Keep old venv as backup.

**Q: "Is UV safe? It's so new."**
**A:** Built by Astral (creators of Ruff linter). Backed by venture capital, used by companies like Anthropic.

---

This module is the foundation for everything that follows. Invest the time upfront, and the rest of the course runs smoothly.
