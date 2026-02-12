<div align="center">
<img src="https://github.com/gitmystuff/agentic-playground/blob/main/files/playground01.jpg?raw=True" alt="agentic playground"/>
</div>

Maintained by Hoang Ky Nguyen

### Prerequisites - Install Required Software

* Open Command Prompt or PowerShell

#### Checking python version (should be greater than or equal to 3.12 and strictly less than 3.13 for CrewAI installation later)
* python --version 

#### Checking Git version 
* git --version

Refer to the following for installation if needed:
* Python: Download from python.org (greater than or equal to 3.12 and less than 3.13)
* Git: Download from git-scm.com
* VSCode: Download from code.visualstudio.com

### Install VSCode

* Install VS Code - https://code.visualstudio.com/download 

#### VS Code Extensions - The Core Essentials
These are the absolute must-haves for any data science work in VS Code.
* **Python by Microsoft** - Why you need it: This is the foundational extension. It provides rich support for the Python language, including IntelliSense (smart code completion), linting (finding errors), debugging, code navigation, and code formatting. It's the engine that powers almost everything else on this list.
* **Jupyter by Microsoft** - Why you need it: This extension transforms VS Code into a fully-featured Jupyter environment. It allows you to create, open, and edit .ipynb files directly. It includes a variable explorer, plot viewer, and data table viewer, giving you that classic notebook experience with the power of a modern IDE. (Note: This is often installed automatically with the main Python extension).
* **Pylance by Microsoft** - Why you need it: Pylance supercharges the Python extension with fast, feature-rich language support. It provides highly accurate type-checking and intelligent auto-completions that will significantly speed up your coding. (Note: This is also usually installed with the Python extension).
* **Data Exploration and Management** - These tools help you look at and interact with your data.
* **Data Wrangler by Microsoft** - Why you need it: An incredible tool for data cleaning and preparation. It provides a graphical interface to view and transform your dataframes (like Pandas). It automatically generates the Python code for any cleaning operations you perform, which is fantastic for reproducibility.
* **Rainbow CSV by mechatroner** - Why you need it: This simple extension makes CSV files much more readable by highlighting each column in a different color. It's surprisingly effective when you're scanning through large datasets.

### Install UV (Python Package Manager)

By default, uv is installed to a path like ~/.cargo/bin on Unix-like systems, which may require the user to close and reopen their terminal (or run a shell-specific command like source ~/.bashrc) to have the uv command available globally in that session.

**Note:** After running the installation script, you may need to close and reopen your Command Prompt/PowerShell/Terminal or run a command like source ~/.bashrc (if applicable) for the uv command to be recognized globally.

#### On Windows (PowerShell) 
* powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

#### On Mac/Linux
* curl -LsSf https://astral.sh/uv/install.sh | sh

#### Verify installation
* uv --version

### Clone the Repository
* Open VS Code terminal and run cd ~/Documents # or wherever you prefer 

#### Clone the repository 
* git clone https://github.com/gitmystuff/agentic-playground.git 

#### Navigate into the project 
* cd agentic-playground

### Setup Environment 

* Run command uv self update 
* **Deactivate Anconda -> conda deactivate** Important if you use Anaconda 

#### 1\. Open the Project Folder in VS Code

Open the **VS Code** application.

  * Go to **File** in the top menu bar.
  * Select **Open Folder...** (or **Open...** on macOS).
  * Navigate to and select the folder named **agentic-playground**.

#### 2\. Open the Integrated Terminal

Once the folder is open in VS Code, open the integrated terminal:

  * Go to **Terminal** in the top menu bar.
  * Select **New Terminal**.
      * *Alternatively, you can use the keyboard shortcut:* $\text{Ctrl} + \text{\`}$ (Windows/Linux) or $\text{Cmd} + \text{\`}$ (macOS).

#### 3\. Confirm Your Directory (Working Directory)

The terminal's prompt should show you are currently inside the **agentic-playground** folder.

  * **Check:** Look at the path displayed in the terminal. You need to verify that the file named **`pyproject.toml`** is directly visible in this current directory.
  * **Command (Optional Check):** You can run the following command to list the contents of the current directory and confirm the file is there:
      * On Windows/Linux/macOS: `ls`
      * On Windows (if `ls` isn't available): `dir`

#### 4\. Run `uv sync`

With the terminal open and confirmed to be in the correct folder (the one containing `pyproject.toml`), execute the following command:

```bash
uv sync
```

This command uses the **`uv`** package manager to synchronize your project's dependencies based on the configuration in your `pyproject.toml` file.

#### 5\. Uv will now install everything (may take a while)

### Activating the Environment

In VS Code, "activating" an environment usually means two things: making sure your terminal recognizes the environment and ensuring the Python extension is using the correct interpreter for IntelliSense and linting.

Since `uv` creates a standard virtual environment in a folder named `.venv` by default, here is the best way to handle it:

#### 1. Let VS Code Handle it (Recommended)

VS Code can automatically detect and "activate" the environment for you every time you open a terminal.

1. Open the **Command Palette** (**Ctrl + Shift + P**).
2. Type **"Python: Select Interpreter"**.
3. Look for the entry that points to `./.venv/Scripts/python.exe`. It will usually be labeled with **('venv')**.
4. Once selected, **kill your current terminal** (click the trash can icon) and open a new one (**Ctrl + Shift + `**).

VS Code will now automatically run the activation script for you every time you open that terminal.

---

#### 2. Manual Activation

If you prefer to do it yourself via the command line, run the activation script based on your terminal type:

| Terminal Type | Command |
| --- | --- |
| **PowerShell** | `.venv\Scripts\activate.ps1` |
| **Command Prompt (cmd)** | `.venv\Scripts\activate.bat` |
| **Git Bash / Zsh** | `source .venv/Scripts/activate` |

---

#### 3. The `uv run` Way (Modern Approach)

One of the best features of `uv` is that you don't actually *need* to activate the environment to run scripts. You can let `uv` handle the context for you:

```powershell
uv run my_script.py

```

This command automatically finds the `.venv`, ensures it is up to date, and runs your code inside it without you ever needing to type "activate."

---

#### Pro Tip: The `.python-version` file

If you run `uv venv`, `uv` creates a `.python-version` file in your project root. VS Code reads this file to automatically suggest the correct interpreter, saving you from having to hunt for it in the settings.

**Is VS Code successfully showing the "(.venv)" indicator in your terminal prompt now?**

### Install CrewAI

* Run uv tool install crewai (Note: CrewAI requires Python versions greater than or equal to 3.12 and strictly less than 3.13)
* Run uv tool list to verify CrewAI
* Run cls (or clear)
