# Getting Started - Student Lab Guide

## Welcome to Agentic AI!

This lab establishes your development environment for the entire course. Think of it as building your workshop before learning carpentry—you need the right tools before creating anything meaningful.

**Time Required:** 2-3 hours (includes installations and testing)  
**Difficulty:** Beginner-friendly, but attention to detail is critical

---

## Learning Approach

### Three-Phase Learning Cycle

This course uses a proven three-phase model for every module:

#### 1. Theory & Concepts (The Lecture)
We begin by establishing vocabulary and mental models. You'll learn **why** before **how**—understanding the blueprint before building.

#### 2. Guided Analysis (The Live Demo)
We work through examples together in class. You'll observe workflows in real-time, predict outcomes, and debug errors as they happen—all in a safe, guided environment.

#### 3. Independent Lab (The Application)
You solidify skills through hands-on practice. This lab challenges you to implement concepts independently, ensuring you can work in your own environment.

**Today's Focus:** You're in Phase 3—time to build your development environment!

---

## What You'll Build

By the end of this lab, you'll have:
- ✅ VS Code configured with 7+ essential extensions
- ✅ UV package manager for fast, reproducible Python environments
- ✅ A secure `.env` file for API keys (never hardcode secrets!)
- ✅ Google Drive for Desktop (optional but recommended)
- ✅ A working test script that calls OpenAI's API

---

## Part 0: Pre-Lab Checklist

Before starting, ensure you have:
- [ ] A computer with administrator access
- [ ] Stable internet connection (for downloads)
- [ ] At least 5GB free disk space
- [ ] A Google account (for Drive, optional)
- [ ] OpenAI account created at: https://platform.openai.com/signup

**Time Check:** If you haven't done these, complete them now. Installations during class waste valuable time.

---

## Part 1: Google Drive for Desktop (Optional - 15 min)

### Why Use Google Drive?

**Problem:** Losing code to hard drive failures, forgetting to backup, or needing files on multiple devices.

**Solution:** Google Drive for Desktop mounts cloud storage as a local folder—automatic backups, accessible everywhere.

### Installation

1. **Download:**
   - Visit: https://www.google.com/drive/download/
   - Click "Download Drive for desktop"

2. **Install:**
   - **Windows:** Run `.exe` installer, follow prompts
   - **Mac:** Open `.dmg` file, drag to Applications

3. **Configure:**
   - Sign in with your Google account
   - Choose **"Stream files"** mode (saves disk space)
   - Select folders to sync (or sync everything)

4. **Verify:**
   - **Windows:** Check File Explorer → "Google Drive"
   - **Mac:** Check Finder → "Google Drive"

### Using Drive for This Course

**Best Practices:**
- ✅ Store: Code, notebooks, data files, documentation
- ✅ Mark project folders as "Available offline" for stable access
- ❌ **Do NOT store:** `.env` files (security risk if Drive hacked)
- ❌ **Do NOT sync:** `node_modules`, `.venv`, `__pycache__` (bloat)

**Folder Structure Suggestion:**
```
Google Drive/
└── Agentic_AI_Course/
    ├── Week_01_Setup/
    ├── Week_02_LLMs/
    ├── Week_03_Async/
    └── ...
```

---

## Part 2: VS Code Installation & Configuration (30 min)

### Step 1: Install VS Code

1. **Download:**
   - Visit: https://code.visualstudio.com/download
   - Select your OS (Windows, Mac, Linux)

2. **Install:**
   - **Windows:** Run installer, check "Add to PATH"
   - **Mac:** Move to Applications folder
   - **Linux:** Follow distro-specific instructions

3. **Launch:**
   - Open VS Code
   - You should see the Welcome screen

---

### Step 2: Install Extensions

Extensions transform VS Code from a text editor into a full AI development environment.

**How to Install:**
1. Click the **Extensions** icon (4 squares) on the left sidebar
2. Or press: `Ctrl+Shift+X` (Windows/Linux) / `Cmd+Shift+X` (Mac)
3. Search for each extension below
4. Click **Install** (blue button)

---

#### Core Extensions (Install All)

##### 1. Python (by Microsoft)
- **Search:** "Python"
- **Why:** Foundation for all Python development
- **Features:** Autocomplete, debugging, linting

##### 2. Jupyter (by Microsoft)
- **Search:** "Jupyter"
- **Why:** Run `.ipynb` notebooks inside VS Code
- **Note:** Often auto-installs with Python extension

##### 3. Pylance (by Microsoft)
- **Search:** "Pylance"
- **Why:** Fast, intelligent Python language server
- **Note:** Also auto-installs with Python extension

##### 4. Data Wrangler (by Microsoft)
- **Search:** "Data Wrangler"
- **Why:** Visual dataframe cleaning
- **Use Case:** Preparing data for AI models

##### 5. Rainbow CSV (by mechatroner)
- **Search:** "Rainbow CSV"
- **Why:** Color-codes CSV columns
- **Use Case:** Reading tool outputs

##### 6. GitLens (by GitKraken)
- **Search:** "GitLens"
- **Why:** Enhanced Git integration
- **Features:** File history, blame annotations, branch comparison

##### 7. GitHub Copilot (by GitHub) - Optional
- **Search:** "GitHub Copilot"
- **Cost:** $10/month (free for students via GitHub Education)
- **Why:** AI code suggestions
- **Ethical Use:** Great for boilerplate, but understand before accepting

---

### Step 3: Create Your First Notebook

Let's test the setup:

1. **Open Command Palette:**
   - Press: `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)

2. **Create Notebook:**
   - Type: "Jupyter: Create New Jupyter Notebook"
   - Press Enter

3. **Select Kernel:**
   - Top-right corner: Click "Select Kernel"
   - Choose any Python interpreter for now (we'll fix this after UV setup)

4. **Test Code:**
   - Type in the first cell:
   ```python
   print("Hello from VS Code!")
   ```
   - Click the **Play** button (▶️) to the left of the cell
   - Output should appear below

**Expected Output:**
```
Hello from VS Code!
```

**If It Doesn't Work:**
- Check that Python extension is installed
- Reload VS Code: `Ctrl+Shift+P` → "Developer: Reload Window"
- Verify Python is installed: Open terminal and type `python --version`

---

## Part 3: UV Package Manager Setup (30 min)

### Why UV Instead of Pip/Conda?

| Feature | pip | conda | UV |
|---------|-----|-------|-----|
| **Speed** | Slow | Very Slow | 10-100x Faster |
| **Lock Files** | No | No | Yes |
| **Reproducibility** | Poor | Medium | Excellent |
| **Disk Space** | Small | Large | Small |

**Bottom Line:** UV is the modern standard for Python projects.

---

### Step 1: Install UV

#### For Windows:
1. Open **PowerShell as Administrator**:
   - Press Windows key
   - Type "PowerShell"
   - Right-click → "Run as administrator"

2. Run installer:
   ```powershell
   irm https://astral.sh/uv/install.ps1 | iex
   ```

3. Restart PowerShell (to refresh PATH)

#### For Mac/Linux:
1. Open **Terminal**

2. Run installer:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Restart terminal

---

### Step 2: Verify Installation

```bash
uv --version
```

**Expected Output:**
```
uv 0.x.x
```

**If "command not found":**
- **Windows:** Add `C:\Users\YourName\.cargo\bin` to System PATH
- **Mac/Linux:** Add `export PATH="$HOME/.cargo/bin:$PATH"` to `~/.bashrc` or `~/.zshrc`

---

### Step 3: Update UV

```bash
uv self update
```

Always run this before starting a project—UV evolves quickly.

---

### Step 4: Deactivate Conda (If Installed)

If you have Anaconda/Miniconda:

```bash
conda deactivate
```

**Why?** Conda and UV can conflict. Use one or the other (we use UV).

---

### Step 5: Initialize a Test Project

1. **Create project folder:**
   ```bash
   # Navigate to where you want to work
   cd ~/Desktop  # Or your preferred location
   
   # Create project
   uv init agentic-ai-test
   cd agentic-ai-test
   ```

2. **Verify structure:**
   ```bash
   ls  # or dir on Windows
   ```

   You should see:
   ```
   pyproject.toml
   hello.py
   ```

---

### Step 6: Edit pyproject.toml

Open `pyproject.toml` in VS Code and replace contents with:

```toml
[project]
name = "agentic-ai-test"
version = "0.1.0"
description = "Week 1 setup test"
requires-python = ">=3.12"

dependencies = [
    "openai>=1.0.0",
    "python-dotenv>=1.0.0",
]

[tool.uv]
dev-dependencies = [
    "ipykernel>=6.0.0",
    "jupyter>=1.0.0",
]
```

**What This Means:**
- **Line 5:** Requires Python 3.12+
- **Lines 7-10:** Packages needed to run your code
- **Lines 13-16:** Packages only needed for development (Jupyter)

---

### Step 7: Install Dependencies

```bash
uv sync
```

**What Happens:**
1. UV reads `pyproject.toml`
2. Downloads packages from PyPI
3. Creates a `.venv` folder (virtual environment)
4. Generates `uv.lock` (locks exact versions)

**Expected Output:**
```
Resolved 12 packages in 145ms
Downloaded 5 packages in 823ms
Installed 12 packages in 234ms
```

**Note:** Your numbers will vary, but should complete in <5 seconds.

---

### Step 8: Verify Environment

Check that `.venv` was created:

```bash
# Mac/Linux
ls -la | grep .venv

# Windows
dir /a | findstr .venv
```

You should see a `.venv` folder.

---

### Step 9: Select UV Environment in VS Code

1. **Open VS Code** in your project folder:
   ```bash
   code .
   ```

2. **Create a test notebook:**
   - `Ctrl+Shift+P` → "Jupyter: Create New Jupyter Notebook"
   - Save as `test_setup.ipynb`

3. **Select Kernel:**
   - Top-right corner: Click "Select Kernel"
   - Choose "Python Environments"
   - Select the one labeled `.venv` (it will show the full path)

4. **Test:**
   ```python
   import sys
   print(f"Python path: {sys.executable}")
   print(f"OpenAI installed: {'openai' in sys.modules or True}")
   
   # Try importing
   import openai
   print("✅ OpenAI SDK loaded successfully!")
   ```

**Expected Output:**
```
Python path: /Users/yourname/Desktop/agentic-ai-test/.venv/bin/python
OpenAI installed: True
✅ OpenAI SDK loaded successfully!
```

---

## Part 4: Environment Variables & API Keys (20 min)

### Why Environment Variables?

**❌ BAD: Hardcoding**
```python
api_key = "sk-proj-abc123xyz..."  # NEVER DO THIS
```

**Problems:**
1. If you push to GitHub, bots steal your key in minutes
2. Stolen keys can cost thousands in API charges
3. Can't share code without exposing your key

**✅ GOOD: Environment Variables**
```python
import os
api_key = os.getenv('OPENAI_API_KEY')  # Key stored separately
```

---

### Step 1: Create .env File

In your `agentic-ai-test` folder, create a file named `.env` (note the dot!).

**Contents:**
```
OPENAI_API_KEY=your_actual_key_here
```

**How to Get Your OpenAI Key:**
1. Visit: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Name it "Agentic AI Course"
4. Copy the key (starts with `sk-proj-...`)
5. Paste into `.env` file

**Important:** Replace `your_actual_key_here` with your real key!

---

### Step 2: Secure Your Key

Create a `.gitignore` file in your project:

```
# .gitignore
.env
.env.local
.env.*
*.key
.venv/
__pycache__/
*.pyc
```

**This prevents accidentally committing secrets to Git.**

---

### Step 3: Test Loading the Key

Create a new notebook cell:

```python
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Retrieve key
api_key = os.getenv('OPENAI_API_KEY')

# Debug: Show first 10 characters (never show full key!)
if api_key:
    print(f"✅ Key loaded: {api_key[:10]}...")
else:
    print("❌ Key not found. Check your .env file.")
```

**Expected Output:**
```
✅ Key loaded: sk-proj-ab...
```

**If You See "Key not found":**
- Verify `.env` file is in the same directory as your notebook
- Check spelling: `OPENAI_API_KEY` (all caps, underscores)
- Make sure there are no spaces around `=` in `.env`

---

## Part 5: Complete Integration Test (20 min)

Now let's put it all together with a real API call!

### Step 1: Install Additional Packages

```bash
uv add anthropic requests ipython
```

This updates `pyproject.toml` and installs packages immediately.

---

### Step 2: Create Test Script

In VS Code, create a new notebook: `integration_test.ipynb`

**Cell 1: Setup**
```python
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

print("=== Environment Check ===")
print(f"Python: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print(f".venv active: {'.venv' in sys.executable}")
print()
```

**Cell 2: Load API Key**
```python
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file")

print(f"✅ API Key loaded: {api_key[:10]}...")
```

**Cell 3: Test API Call**
```python
print("Making API call to OpenAI...")

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-4o-mini",  # Cheapest model (~$0.15/1M tokens)
    messages=[
        {"role": "user", "content": "Say 'Setup complete!' if you can read this."}
    ],
    max_tokens=50
)

result = response.choices[0].message.content
print(f"\n🎉 {result}")
```

**Expected Output:**
```
Making API call to OpenAI...

🎉 Setup complete!
```

---

### Step 3: Verify Cost

Check how many tokens you used:

```python
usage = response.usage
print(f"\nTokens used: {usage.total_tokens}")
print(f"Estimated cost: ${usage.total_tokens * 0.00000015:.6f}")
```

**Example Output:**
```
Tokens used: 23
Estimated cost: $0.000003
```

Don't worry—this test costs less than a penny!

---

## Part 6: Lab Submission (10 min)

### Deliverable Checklist

Submit **ONE screenshot** showing all of the following:

1. **VS Code window** with:
   - Extensions sidebar visible (showing installed extensions)
   - Your `integration_test.ipynb` notebook open
   - Cell output showing "Setup complete!" from OpenAI

2. **Terminal window** (can be VS Code integrated terminal) showing:
   ```bash
   uv --version
   ```

3. **File explorer** showing:
   - `.env` file exists
   - `.gitignore` file exists
   - `.venv` folder exists

### How to Take Screenshot

- **Windows:** Windows Key + Shift + S
- **Mac:** Cmd + Shift + 4
- **Linux:** Varies by distro (usually Shift + PrtScn)

### Submission Format

Save as: `lastname_firstname_week1_setup.png`

Upload to: [Canvas/LMS submission link]

---

## Troubleshooting Guide

### Problem: "uv: command not found"

**Solution:**
```bash
# Check if UV is installed
which uv  # Mac/Linux
where uv  # Windows

# If not found, reinstall and restart terminal
```

---

### Problem: "Python interpreter not found"

**Solution:**
1. Run `uv python list` to see available versions
2. Install Python 3.12: `uv python install 3.12`
3. Pin to project: `uv python pin 3.12`
4. Sync again: `uv sync`

---

### Problem: "OpenAI API key invalid"

**Possible Causes:**
1. Copied key incorrectly (extra spaces/newlines)
2. Key expired or deleted from OpenAI dashboard
3. Wrong variable name in `.env`

**Debug:**
```python
# Print exactly what was loaded
key = os.getenv('OPENAI_API_KEY')
print(f"Key length: {len(key) if key else 0}")
print(f"Key starts with: {key[:7] if key else 'None'}")
```

Valid keys start with `sk-proj-` and are ~60 characters long.

---

### Problem: "RateLimitError"

**Cause:** Free tier has 3 requests/minute limit.

**Solution:** Wait 60 seconds between API calls.

---

### Problem: "Module not found"

**Cause:** Package installed in wrong environment.

**Solution:**
```bash
# Verify you're in project directory
pwd  # or cd on Windows

# Reinstall packages
uv sync

# Verify installation
uv pip list | grep openai
```

---

## Next Steps

Congratulations! You've built a production-ready development environment. 

**What You've Learned:**
- ✅ Modern Python environments with UV
- ✅ Secure API key management
- ✅ Professional IDE setup
- ✅ Making your first LLM API call

**Coming in Week 2:**
- Comparing multiple LLM providers (OpenAI, Anthropic, Google)
- Building model-agnostic interfaces
- Understanding token costs and latency

**Recommended Practice:**
Experiment with different prompts to `gpt-4o-mini`:
- "Explain quantum computing in one sentence"
- "Write a haiku about AI"
- "What is 17 * 23?"

Each call costs ~$0.00001. Feel free to explore!

---

## Additional Resources

### Official Documentation
- **UV:** https://docs.astral.sh/uv/
- **VS Code Python:** https://code.visualstudio.com/docs/python/python-tutorial
- **OpenAI API:** https://platform.openai.com/docs/api-reference
- **python-dotenv:** https://pypi.org/project/python-dotenv/

### Video Tutorials
- UV Setup Walkthrough: [YouTube link]
- VS Code Extensions Tour: [YouTube link]
- API Key Security: [YouTube link]

### Getting Help
- **Discord:** [Course server link]
- **Office Hours:** [Schedule link]
- **TA Email:** [Contact info]

---

## Frequently Asked Questions

**Q: Do I need to keep VS Code open for UV to work?**  
**A:** No. UV is a command-line tool. VS Code just makes it easier to use.

**Q: Can I use a different editor?**  
**A:** Yes, but course demos use VS Code. You'll need to figure out equivalents for your editor.

**Q: What if I already have a pip/conda project?**  
**A:** You can migrate by creating `pyproject.toml` and running `uv sync`. Keep your old venv as backup.

**Q: Is it safe to commit .venv to Git?**  
**A:** No! Add it to `.gitignore`. Virtual environments should be recreated via `uv sync`.

**Q: How much will API calls cost for this course?**  
**A:** Expect $5-10 total if you use `gpt-4o-mini` for all assignments. We'll discuss cost optimization in Week 2.

**Q: Can I use the free tier for everything?**  
**A:** OpenAI's free tier has strict rate limits (3 RPM). You may need to upgrade for larger projects.

**Q: Is there an alternative to OpenAI's free tier**  
**A:** Yes, you can use OpenRouter for better free access. Check out our instructions on how to get your free API key here: [OpenRouter More Info](https://github.com/gitmystuff/agentic-playground/blob/main/files/OpenRouter.md)


---

**Lab Complete! 🎉**

You're now ready for Week 2: The Cognitive Interface (LLMs & APIs). See you in class!
