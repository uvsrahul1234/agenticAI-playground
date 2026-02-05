# Getting Started Glossary - Development Environment Terms

## Quick Reference Guide for Environment Setup

This glossary defines all technical terms, tools, and concepts related to setting up a professional agentic AI development environment. Terms are organized by category for easy lookup.

---

## 🔧 Package Management

### UV
**Definition:** A modern, Rust-based Python package installer and resolver that is 10-100x faster than pip or conda.

**Key Features:**
- Deterministic dependency resolution (same result every time)
- Uses `uv.lock` to freeze exact package versions
- Replaces: pip, pip-tools, virtualenv, and poetry
- Built by Astral (creators of Ruff, the fastest Python linter)

**Core Commands:**
```bash
uv init project-name      # Create new project
uv sync                   # Install dependencies from pyproject.toml
uv add package-name       # Add and install a package
uv tool install crewai    # Install global CLI tool
```

**Why It Matters for Agents:**
Agentic projects have complex dependency trees (e.g., LangChain requires 50+ packages). UV's speed means you can iterate faster—adding a new framework takes seconds, not minutes.

**Comparison:**
| Operation | pip | conda | UV |
|-----------|-----|-------|-----|
| Install 50 packages | 2-5 min | 5-10 min | 5-15 sec |
| Reproducibility | Low | Medium | High |

---

### pip
**Definition:** The default Python package installer (stands for "Pip Installs Packages").

**Basic Usage:**
```bash
pip install package-name
pip freeze > requirements.txt  # Save installed packages
```

**Limitations:**
- Sequential dependency resolution (slow)
- No lock files by default (non-deterministic)
- Conflicting installs can break environments

**When to Use:** Only for one-off package testing. Production projects should use UV.

---

### Conda
**Definition:** A package and environment manager for Python and other languages, developed by Anaconda.

**Features:**
- Manages Python itself (pip only manages packages)
- Includes scientific computing packages pre-compiled
- Separate environment isolation

**Limitations:**
- Very slow dependency resolution (minutes for complex projects)
- Large disk footprint (base install ~3GB)
- Conflicts with pip if mixed carelessly

**Migration to UV:**
```bash
conda deactivate          # Exit conda environment
# Then use UV for all new projects
```

---

### Virtual Environment (.venv)
**Definition:** An isolated Python environment with its own packages and interpreter, separate from system Python.

**Why It Matters:**
- **Problem:** Installing packages globally can break system tools
- **Solution:** Each project gets its own `.venv` folder
- **Benefit:** Delete project = delete dependencies (no pollution)

**Structure:**
```
my-project/
├── .venv/              # Virtual environment
│   ├── bin/            # Executables (python, pip)
│   ├── lib/            # Installed packages
│   └── pyvenv.cfg      # Configuration
├── pyproject.toml      # Declares dependencies
└── main.py             # Your code
```

**Activation:**
```bash
# Mac/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Deactivate
deactivate
```

**VS Code:** Automatically activates when you select `.venv` as your kernel.

---

### pyproject.toml
**Definition:** A configuration file (TOML format) that declares project metadata and dependencies using PEP 621 standards.

**Replaces:**
- `setup.py` (old packaging standard)
- `requirements.txt` (no metadata, no versioning)
- `Pipfile` (poetry-specific)

**Example:**
```toml
[project]
name = "my-agentic-app"
version = "0.1.0"
requires-python = ">=3.12"

dependencies = [
    "openai>=1.0.0",        # Any version 1.0.0+
    "langchain==0.1.0",     # Exactly 0.1.0
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.0",          # Only for development
]
```

**Sections Explained:**
- `[project]`: Core metadata (name, version, dependencies)
- `[tool.uv]`: UV-specific settings (dev dependencies)

**Version Syntax:**
- `>=1.0.0`: "1.0.0 or higher" (flexible, recommended)
- `==1.0.0`: "Exactly 1.0.0" (rigid, only for known bugs)
- `~=1.0.0`: "Compatible with 1.0.0" (allows 1.0.x, not 1.1.0)

---

### uv.lock
**Definition:** An automatically generated file that locks exact versions of all dependencies (including transitive ones).

**Purpose:** Ensures everyone on the team installs identical package versions.

**Example Scenario:**
```
pyproject.toml says: openai>=1.0.0
Today UV installs:    openai==1.5.3
uv.lock records:      openai==1.5.3

Tomorrow, openai==1.6.0 releases
Your teammate runs:   uv sync
They get:             openai==1.5.3 (from uv.lock, not 1.6.0)
```

**When to Update Lock:**
```bash
uv sync --upgrade  # Get latest compatible versions
```

**Commit to Git:** Yes! This ensures reproducible builds.

---

### Transitive Dependencies
**Definition:** Packages that your direct dependencies require (but you don't import directly).

**Example:**
```
You install:     langchain
LangChain needs: pydantic, requests, tenacity
Pydantic needs:  typing-extensions
```

Your `pyproject.toml` lists `langchain`, but `uv.lock` pins ALL of these.

**Why It Matters:** Without lock files, different team members might get different versions of transitive dependencies, causing "works on my machine" bugs.

---

## 🖥️ Development Tools

### VS Code (Visual Studio Code)
**Definition:** A free, open-source code editor by Microsoft that's become the industry standard for Python development.

**Why VS Code Over Alternatives:**
| Feature | VS Code | PyCharm | Jupyter Lab | Notepad/Vim |
|---------|---------|---------|-------------|-------------|
| **Speed** | Fast | Slow startup | Fast | Very fast |
| **Extensions** | 30,000+ | Built-in | Limited | None |
| **Jupyter Support** | Excellent | Good | Native | No |
| **Free** | Yes | Community only | Yes | Yes |
| **AI Features** | Copilot, IntelliCode | AI Assistant | No | No |

**Key Shortcuts:**
- `Ctrl+Shift+P`: Command Palette (access all features)
- `Ctrl+``: Toggle integrated terminal
- `Ctrl+B`: Toggle sidebar
- `F5`: Start debugging

---

### Extensions (VS Code)
**Definition:** Add-on modules that extend VS Code's functionality for specific languages, frameworks, or workflows.

**Installation:**
1. Click Extensions icon (4 squares) in left sidebar
2. Search for extension name
3. Click "Install"

**How They Work:** Extensions run in separate processes, so a buggy extension won't crash VS Code itself.

---

### Jupyter Notebook (.ipynb)
**Definition:** An interactive document format that mixes code cells, outputs, and markdown text.

**Structure:**
```json
{
  "cells": [
    {
      "cell_type": "code",
      "source": ["print('Hello')"],
      "outputs": ["Hello"]
    },
    {
      "cell_type": "markdown",
      "source": ["# Title"]
    }
  ]
}
```

**Why Use Notebooks:**
- ✅ Immediate feedback (run cells individually)
- ✅ Visualize data inline (plots, dataframes)
- ✅ Mix documentation with code
- ❌ Harder to version control (JSON format)
- ❌ Can't easily refactor across cells

**Agentic Use Case:** Perfect for experimenting with prompts, comparing LLM outputs, and iterative development.

---

### Kernel
**Definition:** The computational engine that runs code in a Jupyter notebook—essentially a Python interpreter running in the background.

**How It Works:**
1. You type code in a cell
2. Notebook sends code to kernel
3. Kernel executes and returns results
4. Notebook displays output

**Selecting Kernel:**
- In VS Code: Top-right corner → "Select Kernel"
- Choose: Python environment (`.venv`) that has your packages

**Kernel States:**
- **Idle:** Ready to execute
- **Busy:** Running code
- **Dead:** Crashed (restart required)

**Common Issue:** Kernel shows "busy" forever → Code has infinite loop or waiting for input → Click "Interrupt Kernel"

---

### IntelliSense
**Definition:** AI-powered code completion that suggests functions, variables, and parameters as you type.

**How It Works:**
- Analyzes imported libraries
- Reads type hints
- Suggests completions based on context

**Example:**
```python
import pandas as pd
df = pd.DataFrame(...)
df.  # IntelliSense shows: sort_values, groupby, drop, etc.
```

**Dependencies:**
- Python extension
- Pylance (language server)
- Type hints in your code

**Why It Matters:** Speeds up coding by 30-50%—you don't need to remember exact function names.

---

### Pylance
**Definition:** Microsoft's fast Python language server that powers IntelliSense, type checking, and code navigation.

**Technical Detail:** Built with Rust (not Python), making it 5-10x faster than the older Python Language Server.

**Features:**
- Auto-imports: Types a function name → suggests import
- Parameter hints: Hover over function → see expected arguments
- Type checking: Warns about type mismatches before running

**Comparison:**
| Language Server | Speed | Type Checking | Auto-Import |
|----------------|-------|---------------|-------------|
| Pylance (Rust) | ⚡⚡⚡ | Strict | Yes |
| Jedi (Python) | ⚡ | None | Limited |

---

### Linting
**Definition:** Automated code analysis that finds errors, style issues, and potential bugs without running the code.

**Example Linter Output:**
```python
def calculate(x, y)  # ❌ Linter: Missing colon
    result = x + y
    return reuslt    # ❌ Linter: Undefined variable 'reuslt'
```

**Common Linters:**
- **Pylint:** Comprehensive but slow
- **Flake8:** Fast, focused on PEP 8 style
- **Ruff:** Rust-based, 10-100x faster than others (recommended)

**VS Code Integration:** Python extension runs linters automatically. Errors show as red squiggles.

---

### Git / Version Control
**Definition:** A system for tracking changes to files over time, enabling collaboration and rollback.

**Core Concepts:**
- **Repository (repo):** Project folder tracked by Git
- **Commit:** Snapshot of your code at a point in time
- **Branch:** Parallel version of code (e.g., feature branch)
- **Merge:** Combine changes from two branches

**Basic Workflow:**
```bash
git init              # Start tracking project
git add file.py       # Stage changes
git commit -m "msg"   # Save snapshot
git push              # Upload to GitHub
```

**Why It Matters:** In team projects (Weeks 8-11), Git enables multiple developers to work simultaneously without overwriting each other.

---

### .gitignore
**Definition:** A file that tells Git which files/folders to never track.

**Common Patterns:**
```
# .gitignore
.env                 # Never commit secrets
.venv/               # Don't commit virtual environments
__pycache__/         # Ignore Python bytecode
*.pyc                # Ignore compiled Python files
.DS_Store            # Ignore Mac system files
```

**Why It's Critical:** Prevents committing:
- API keys (security)
- Virtual environments (bloat—100MB+ of dependencies)
- System files (not portable across OSes)

**Verification:**
```bash
git status  # Check what Git is tracking
# .env should NOT appear here
```

---

### GitHub Copilot
**Definition:** An AI coding assistant by GitHub/OpenAI that suggests entire lines or blocks of code as you type.

**How It Works:**
- Trained on billions of lines of public code
- Analyzes your current file and project context
- Generates suggestions in real-time (appears as gray text)

**Example:**
```python
# You type:
def fetch_user_data(

# Copilot suggests:
def fetch_user_data(user_id: int) -> dict:
    """Fetch user data from API."""
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()
```

**Ethical Use:**
- ✅ **Good:** Boilerplate code (API calls, data processing)
- ⚠️ **Caution:** Understanding what it generates (don't blindly accept)
- ❌ **Bad:** Using for homework without learning the concepts

**Cost:** $10/month (free for students via GitHub Education Pack)

---

## 🔐 Security & Configuration

### Environment Variables
**Definition:** Key-value pairs stored at the operating system level that programs can access at runtime.

**How They Work:**
```bash
# Terminal
export OPENAI_API_KEY="sk-proj-abc123"

# Python
import os
key = os.getenv('OPENAI_API_KEY')  # Retrieves "sk-proj-abc123"
```

**Common Environment Variables:**
- `PATH`: Where to search for executable programs
- `HOME`: Current user's home directory (Linux/Mac)
- `USER`: Current username
- `OPENAI_API_KEY`: (custom) Your API key

**Viewing All:**
```bash
# Mac/Linux
printenv

# Windows
set
```

---

### .env File
**Definition:** A plain text file containing environment variables in `KEY=value` format, loaded into your program via libraries like `python-dotenv`.

**Format Rules:**
```
# .env file
VARIABLE_NAME=value
ANOTHER_VAR=another value
# Comments start with #

# ❌ WRONG (spaces around =)
API_KEY = sk-proj-...

# ✅ CORRECT (no spaces)
API_KEY=sk-proj-...
```

**Why Use .env Instead of Hardcoding:**
| Approach | Security | Shareable | Easy to Change |
|----------|----------|-----------|----------------|
| Hardcoded `key = "sk-..."` | ❌ Exposed in code | ❌ No | ❌ Edit every file |
| .env file | ✅ Outside code | ✅ Use .env.example | ✅ Edit one file |

---

### python-dotenv
**Definition:** A Python library that reads `.env` files and loads them into `os.environ`.

**Installation:**
```bash
uv add python-dotenv
```

**Usage:**
```python
from dotenv import load_dotenv
import os

# Load .env file (searches current directory and parents)
load_dotenv()

# Access variables
api_key = os.getenv('OPENAI_API_KEY')
```

**Advanced:**
```python
# Explicitly specify path
load_dotenv(dotenv_path='/path/to/.env')

# Override existing environment variables
load_dotenv(override=True)

# Return dict instead of setting os.environ
from dotenv import dotenv_values
config = dotenv_values('.env')  # {'API_KEY': 'sk-...'}
```

---

### API Key
**Definition:** A secret token that authenticates your requests to a third-party service (like OpenAI's API).

**Format Examples:**
```
OpenAI:     sk-proj-abc123xyz...    (~60 chars)
Anthropic:  sk-ant-def456uvw...     (~50 chars)
Google:     AIzaSy...                (~40 chars)
```

**Security Best Practices:**
1. ✅ Store in `.env`, load with `python-dotenv`
2. ✅ Add `.env` to `.gitignore`
3. ✅ Rotate keys every 3-6 months
4. ✅ Use separate keys for dev/prod
5. ❌ NEVER hardcode in source code
6. ❌ NEVER commit to GitHub

**If You Leak a Key:**
1. Immediately delete key from provider's dashboard
2. Generate new key
3. Update `.env` file
4. Force-push to remove from Git history:
   ```bash
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch .env' HEAD
   ```

---

### .env.example
**Definition:** A template file that documents required environment variables without exposing actual values.

**Purpose:** Show collaborators which keys they need to set up the project.

**Example:**
```
# .env.example
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
DATABASE_URL=postgresql://user:pass@localhost/db
```

**Workflow:**
1. Clone project from GitHub
2. Copy `.env.example` to `.env`
3. Fill in real values
4. Run project

**Commit to Git:** Yes! This file has NO secrets, only placeholders.

---

### Rate Limiting
**Definition:** A restriction on how many API requests you can make per time period (enforced by the API provider).

**Common Limits:**
| Provider | Free Tier | Paid Tier |
|----------|-----------|-----------|
| OpenAI | 3 RPM (requests/min) | 3,500 RPM |
| Anthropic | 5 RPM | 1,000 RPM |
| Groq | 30 RPM | 6,000 RPM |

**Error Example:**
```
RateLimitError: Rate limit reached for gpt-4o-mini in organization org-abc
```

**Solutions:**
1. Wait 60 seconds between requests
2. Implement exponential backoff:
   ```python
   import time
   for attempt in range(5):
       try:
           response = openai.chat.completions.create(...)
           break
       except RateLimitError:
           time.sleep(2 ** attempt)  # 1s, 2s, 4s, 8s, 16s
   ```
3. Upgrade to paid tier
4. Use local models (no limits, but lower quality)

---

## 💾 File Formats & Standards

### TOML (Tom's Obvious, Minimal Language)
**Definition:** A configuration file format designed to be easy to read and write (used by `pyproject.toml`).

**Example:**
```toml
# Comment
[section]
string = "value"
integer = 42
float = 3.14
boolean = true
array = ["item1", "item2"]
date = 2024-01-20T15:30:00Z

[nested.section]
key = "value"
```

**Comparison:**
| Format | Readability | Comments | Data Types |
|--------|-------------|----------|------------|
| JSON | Medium | No | Limited |
| YAML | High | Yes | Many |
| TOML | Very High | Yes | Many |

**Why TOML for pyproject.toml:** Easier for humans to edit than JSON, less indentation-fragile than YAML.

---

### Markdown (.md)
**Definition:** A lightweight markup language for formatting plain text (used in Jupyter notebooks and documentation).

**Syntax:**
```markdown
# Heading 1
## Heading 2
**bold** *italic* `code`
- Bullet point
1. Numbered list
[Link](https://example.com)
![Image](image.png)
```

**Usage in Course:**
- Jupyter notebooks: Markdown cells for explanations
- README.md: Project documentation
- GitHub: Automatically renders `.md` files

---

### JSON (JavaScript Object Notation)
**Definition:** A text format for representing structured data (used by `.ipynb` notebook files).

**Example:**
```json
{
  "name": "John",
  "age": 30,
  "skills": ["Python", "AI"],
  "active": true
}
```

**Python Interaction:**
```python
import json

# Parse JSON string
data = json.loads('{"key": "value"}')

# Convert Python dict to JSON
json_str = json.dumps({"key": "value"})
```

**Why Notebooks Use JSON:** Allows storing code, outputs, and metadata in a single file that's both human-readable and machine-parsable.

---

## 🌐 Cloud & Collaboration

### Google Drive for Desktop
**Definition:** An application that mounts Google Drive cloud storage as a local folder on your computer.

**How It Works:**
```
Cloud Storage (Google Drive)
         ↕ (automatic sync)
Local Folder (~/Google Drive/)
         ↕
Your Applications (VS Code, etc.)
```

**Modes:**
1. **Stream:** Files download on-demand (saves disk space)
2. **Mirror:** All files stored locally (works offline)

**Benefits:**
- ✅ Automatic backups
- ✅ Access files from any device
- ✅ Collaboration (shared folders)

**Drawbacks:**
- ❌ Requires internet for streaming
- ❌ Sync conflicts if editing same file on multiple devices
- ❌ Free tier limited to 15GB

**Best Practices for This Course:**
- Store: Code, notebooks, data files
- Don't store: `.env` files (security), `.venv` folders (bloat)
- Mark project folders "Available offline" for stable access

---

### Quota
**Definition:** The maximum storage space or usage limit imposed by a service.

**Google Drive Free Tier:**
- 15GB total (shared across Drive, Gmail, Photos)

**What Takes Up Space:**
- `.ipynb` notebooks: ~100KB each
- Data files: Varies (CSVs, images)
- **NOT counted:** `.venv` folders (if excluded properly)

**Managing Quota:**
1. Clean up old files
2. Compress large datasets
3. Use `.gitignore` to exclude virtual environments
4. Upgrade to Google One ($1.99/month for 100GB)

---

### Streaming vs. Offline Files
**Definition:** Two modes for how Google Drive for Desktop stores files locally.

**Streaming (Default):**
- Files appear in folder but don't take disk space
- Download when you open them
- Auto-delete after period of inactivity

**Offline (Manual):**
- Right-click file/folder → "Make available offline"
- Fully downloaded to local disk
- Always accessible without internet

**Use Offline For:**
- Project folders you're actively working on
- Large data files you'll access repeatedly

**Use Streaming For:**
- Archive folders
- Reference materials

---

## 🛠️ Advanced Concepts

### PATH (Environment Variable)
**Definition:** A list of directories where the operating system searches for executable programs.

**Example:**
```bash
# Mac/Linux
/usr/bin:/usr/local/bin:/home/user/.cargo/bin

# Windows
C:\Windows\System32;C:\Program Files\Python312;C:\Users\User\.cargo\bin
```

**How It Works:**
```bash
# You type:
python main.py

# OS searches PATH for "python":
1. Check /usr/bin/python → Not found
2. Check /usr/local/bin/python → Not found
3. Check /home/user/.venv/bin/python → Found! Execute.
```

**Common Issues:**
- "Command not found" → Program not in PATH
- Wrong version runs → Earlier PATH entry takes precedence

**Fixing:**
```bash
# Mac/Linux (.bashrc or .zshrc)
export PATH="/new/directory:$PATH"

# Windows (System Properties → Environment Variables)
Add C:\new\directory to PATH
```

---

### PEP (Python Enhancement Proposal)
**Definition:** Design documents that propose new features or standards for Python.

**Relevant PEPs:**
- **PEP 8:** Style guide (how to format code)
- **PEP 621:** `pyproject.toml` standard (metadata format)
- **PEP 668:** Prevents system Python modification (use venvs)

**Example:**
```
PEP 621 defines:
[project]
name = "my-package"
^^^^^
Must be lowercase with hyphens (not underscores)
```

**Why It Matters:** Tools like UV follow PEPs, ensuring your projects work across different systems.

---

### Deterministic Builds
**Definition:** When running the same build process always produces identical outputs (same package versions).

**Non-Deterministic (pip):**
```bash
# Day 1
pip install langchain  # Installs langchain==0.1.0 + deps

# Day 2 (langchain releases 0.1.1)
pip install langchain  # Installs langchain==0.1.1 + deps
                       # Different packages! 😱
```

**Deterministic (UV):**
```bash
# Day 1
uv sync  # Reads uv.lock → installs langchain==0.1.0

# Day 2
uv sync  # Reads uv.lock → installs langchain==0.1.0
         # Same packages! ✅
```

**Why It Matters:** Prevents "works on my machine" bugs. Everyone on the team gets identical environments.

---

### Quantization
**Definition:** Reducing the numerical precision of a model's weights (e.g., from 32-bit to 4-bit) to make it smaller and faster.

**Example:**
```
Original Llama 3 70B:  140GB (16-bit floats)
Quantized (Q4):        38GB  (4-bit integers)
Quality loss:          ~5-10%
```

**Why Mentioned Here:** When running local models (Week 2+), you'll download quantized versions via Ollama or LM Studio to fit in consumer RAM.

**File Extensions:**
- `.gguf` - Common format for quantized models
- `Q4_0`, `Q4_K_M` - Different quantization methods

---

## 📊 Quick Reference Table

| Term | Category | Why It Matters |
|------|----------|----------------|
| **UV** | Package Manager | 100x faster than pip, reproducible builds |
| **.venv** | Virtual Environment | Isolates project dependencies |
| **pyproject.toml** | Configuration | Single source of truth for dependencies |
| **VS Code** | IDE | Industry-standard editor with AI features |
| **Jupyter Notebook** | Interactive Coding | Experiment with prompts, visualize data |
| **.env** | Security | Stores API keys outside code |
| **.gitignore** | Version Control | Prevents committing secrets/bloat |
| **IntelliSense** | Productivity | Auto-complete saves time |
| **API Key** | Authentication | Required for LLM API access |
| **Rate Limiting** | Cost Control | Prevents accidental overspending |

---

## 🎓 Study Questions

1. **Why is UV better than pip for agentic AI projects?**
   - Answer: Faster (10-100x), deterministic (uv.lock), replaces multiple tools

2. **What's the difference between `dependencies` and `dev-dependencies` in pyproject.toml?**
   - Answer: Dependencies are runtime requirements; dev-dependencies are only for development (testing, Jupyter)

3. **Why should you never commit .env files to Git?**
   - Answer: API keys can be stolen by bots, costing thousands in charges

4. **What is a virtual environment and why do we use them?**
   - Answer: Isolated Python environment per project to prevent dependency conflicts

5. **How does python-dotenv load environment variables?**
   - Answer: Reads `.env` file and sets values in `os.environ`

6. **What's the purpose of uv.lock?**
   - Answer: Locks exact package versions for reproducible builds across team members

7. **Why do we use .gitignore?**
   - Answer: Prevent committing secrets (`.env`), bloat (`.venv`), and system files

8. **What's the difference between streaming and offline files in Google Drive?**
   - Answer: Streaming downloads on-demand (saves space); offline stores locally (works without internet)

---

## 💡 Pro Tips

### For Students:
1. **Run `uv self update` weekly** — UV evolves rapidly
2. **Check `uv.lock` into Git** — Ensures teammates have same versions
3. **Never edit `.env` in public places** — Coffee shop WiFi can be monitored
4. **Use `.env.example` for documentation** — Help future you remember what keys are needed
5. **Activate .venv before installing packages** — Prevents polluting system Python

### For Instructors:
1. **Standardize on UV early** — Saves hours of debugging later
2. **Create setup videos** — Students can watch at their own pace
3. **Provide a pre-configured pyproject.toml** — Reduces initial friction
4. **Office hours = mostly PATH issues** — Create a troubleshooting wiki
5. **Demo leaked key scenario** — Shows real consequences of bad security

---

## 🔗 Official Documentation

### Tools
- **UV:** https://docs.astral.sh/uv/
- **VS Code:** https://code.visualstudio.com/docs
- **Python:** https://docs.python.org/3/
- **Git:** https://git-scm.com/doc

### Standards
- **PEP 621 (pyproject.toml):** https://peps.python.org/pep-0621/
- **TOML:** https://toml.io/en/

### Libraries
- **python-dotenv:** https://pypi.org/project/python-dotenv/
- **OpenAI Python SDK:** https://platform.openai.com/docs/libraries/python-library

---

## 🆘 Common Error Messages Decoded

### "uv: command not found"
**Cause:** UV not in PATH  
**Fix:** Add `~/.cargo/bin` (Mac/Linux) or `C:\Users\User\.cargo\bin` (Windows) to PATH

### "KeyError: 'OPENAI_API_KEY'"
**Cause:** `.env` not loaded or variable misspelled  
**Fix:** Call `load_dotenv()` before accessing, verify `.env` exists

### "No Python interpreter selected"
**Cause:** VS Code can't find your `.venv`  
**Fix:** Run `uv sync`, then select `.venv` as kernel

### "RateLimitError: Rate limit reached"
**Cause:** Too many API requests  
**Fix:** Wait 60 seconds or implement exponential backoff

### "PermissionError: [Errno 13] Permission denied"
**Cause:** Trying to install packages system-wide  
**Fix:** Use `uv sync` (creates venv automatically)

---

**Glossary Complete!**

Refer back to this document whenever you encounter unfamiliar setup terminology. Mastering these foundational tools sets you up for success in building agentic AI systems.
