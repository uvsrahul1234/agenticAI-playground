# Module 04: The Tooling Standard (MCP)
## Student Lab Assignment - Independent Application

**Duration:** 90-120 Minutes (Take-Home / Lab Time)  
**Goal:** Reinforcement of skills through independent construction with a domain variation from the demo.

**Due Date:** [Instructor: Set deadline]  
**Submission:** Upload all files to [Instructor: Specify platform]

---

## 🎯 Learning Objectives

By completing this lab, you will demonstrate your ability to:

1. Design and implement a modular MCP server from scratch
2. Apply the three-layer architecture pattern (data, logic, server)
3. Create properly typed and documented tool functions
4. Connect an AI agent to your custom MCP server
5. Debug and verify MCP tool execution
6. Analyze architectural trade-offs and make informed engineering decisions

---

## 📋 Pre-Lab Setup

### Step 1: Environment Configuration

Create a new directory for your lab:

```bash
mkdir mcp_lab_contact_manager
cd mcp_lab_contact_manager
```

### Step 2: Required Installations

Verify the following are installed:

```bash
# Check uv
uv --version

# If not installed:
# Windows (PowerShell):
# powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS/Linux:
# curl -LsSf https://astral.sh/uv/install.sh | sh

# Check Python
python --version  # Should be 3.10 or higher
```

### Step 3: Install Required Libraries (If Needed)

Create a `requirements.txt` file:

```txt
agents
pydantic
python-dotenv
asyncio
```

Install dependencies:

```bash
pip install -r requirements.txt
# Or use uv:
uv pip install -r requirements.txt
```

### Step 4: Environment Variables

Create a `.env` file in your project directory:

```env
OPENAI_API_KEY=sk-your-actual-key-here
# Or use another provider:
# ANTHROPIC_API_KEY=sk-ant-your-key-here
# GROQ_API_KEY=gsk-your-key-here
```

**⚠️ SECURITY CHECKPOINT:**
- [ ] Add `.env` to your `.gitignore` file
- [ ] Never hardcode API keys in your Python files
- [ ] Verify `.env` is not tracked by git: `git status` should not show it

### Step 5: Create Project Structure

Create these empty files (you'll fill them in during the lab):

```
mcp_lab_contact_manager/
├── .env                          # API keys (DO NOT COMMIT)
├── .gitignore                    # Include: .env, data/, __pycache__/
├── requirements.txt              # Dependencies
├── database.py                   # Data persistence layer (YOU BUILD THIS)
├── contact_manager.py            # Business logic layer (YOU BUILD THIS)
├── contact_manager_server.py    # MCP server entry point (YOU BUILD THIS)
├── test_agent.py                 # Agent interaction script (YOU BUILD THIS)
└── data/                         # Will be created automatically
```

---

## 🔄 The Twist: Contact Management System

### Domain Change

**In the Demo:** You saw a **Task Management System** with:
- `create_task_list`, `add_task`, `complete_task`, `list_tasks`

**In Your Lab:** You will build a **Contact Management System** with:
- `create_contact_book`, `add_contact`, `update_contact`, `delete_contact`, `search_contacts`

This variation ensures you understand the underlying MCP patterns, not just how to copy the demo code.

---

## 🛠️ Part 1: Data Persistence Layer (20 minutes)

### Task 1.1: Create `database.py`

Implement the following functions:

#### Required Functions:

```python
import json
import os
from datetime import datetime

DATA_DIR = "data"

# TODO: Create the data directory if it doesn't exist

def read_contact_book(name: str):
    """
    Reads a contact book from disk.
    
    Args:
        name: Name of the contact book (e.g., "personal", "work")
    
    Returns:
        dict: Contact book data if found, None otherwise
    """
    # YOUR CODE HERE
    pass

def write_contact_book(name: str, data: dict):
    """
    Writes a contact book to disk.
    
    Args:
        name: Name of the contact book
        data: Contact book data to save
    """
    # YOUR CODE HERE
    pass

def write_log(name: str, module: str, message: str):
    """
    Appends a log entry for debugging and audit purposes.
    
    Args:
        name: Contact book name
        module: Module name (e.g., "contact_manager")
        message: Log message
    """
    # YOUR CODE HERE
    pass
```

### Task 1.2: Test Your Database Layer

Create a simple test to verify your functions work:

```python
# At the bottom of database.py, add:
if __name__ == "__main__":
    # Test write and read
    test_data = {"name": "test", "contacts": {}, "next_id": 1}
    write_contact_book("test", test_data)
    
    loaded_data = read_contact_book("test")
    print("Test passed!" if loaded_data == test_data else "Test failed!")
    
    # Test logging
    write_log("test", "database", "Test log entry")
    print("Check data/ directory for files")
```

Run the test:
```bash
uv run python database.py
```

**✓ Checkpoint:** You should see `data/contactbook_test.json` and `data/log_test.json` created.

---

## 🧠 Part 2: Business Logic Layer (40 minutes)

### Task 2.1: Create `contact_manager.py` (Data Models)

Define Pydantic models for your contacts:

```python
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Dict, Optional
from database import write_contact_book, read_contact_book, write_log

class Contact(BaseModel):
    """
    Represents a single contact with validation.
    
    TODO: Add the following fields with appropriate types:
    - id: int
    - name: str
    - email: EmailStr (Pydantic's email validator)
    - phone: Optional[str] (phone is optional)
    - notes: Optional[str] (notes are optional)
    - created_at: str
    - updated_at: str
    """
    # YOUR CODE HERE
    pass

    def __repr__(self):
        return f"Contact {self.id}: {self.name} ({self.email})"

class ContactBook(BaseModel):
    """
    Represents a collection of contacts.
    
    TODO: Add the following fields:
    - name: str
    - contacts: Dict[int, Contact] = {}
    - next_contact_id: int = 1
    """
    # YOUR CODE HERE
    pass

    @classmethod
    def get(cls, name: str):
        """
        Load existing contact book or create new one.
        
        TODO: Implement logic to:
        1. Try to read from database
        2. If not found, create new empty book
        3. Convert contact dicts to Contact objects
        4. Return ContactBook instance
        """
        # YOUR CODE HERE
        pass

    def save(self):
        """
        Persist current state to disk.
        
        TODO: Implement logic to:
        1. Convert Contact objects to dictionaries
        2. Save to database via write_contact_book()
        """
        # YOUR CODE HERE
        pass
```

**💡 Hint:** Look at the demo's `TaskList` class for reference on the `get()` and `save()` methods.

---

### Task 2.2: Create Tool Functions

Implement the following MCP tool functions. These will be automatically discovered by the MCP framework.

**CRITICAL:** Each function must have:
- Type hints for all parameters and return value
- A docstring explaining what it does
- Proper error handling with try/except
- Logging via `write_log()`

#### Function 1: `create_contact_book`

```python
def create_contact_book(name: str) -> str:
    """
    Initializes a new empty contact book with the given name.
    This tool will be exposed to the AI agent via MCP.
    
    Args:
        name: Name of the contact book (e.g., "personal", "work")
    
    Returns:
        str: Success or error message
    """
    # TODO: Implement this function
    # 1. Use ContactBook.get(name) to load or create
    # 2. Check if it already has contacts
    # 3. Save it if it's new
    # 4. Log the action
    # 5. Return appropriate message
    pass
```

#### Function 2: `add_contact`

```python
def add_contact(
    book_name: str, 
    name: str, 
    email: str, 
    phone: Optional[str] = None, 
    notes: Optional[str] = None
) -> str:
    """
    Adds a new contact to the specified contact book.
    This tool will be exposed to the AI agent via MCP.
    
    Args:
        book_name: Name of the contact book
        name: Contact's full name
        email: Contact's email address
        phone: Contact's phone number (optional)
        notes: Additional notes about the contact (optional)
    
    Returns:
        str: Success message with contact ID or error message
    """
    # TODO: Implement this function
    # 1. Load the contact book
    # 2. Create a new Contact with next_contact_id
    # 3. Set created_at and updated_at timestamps
    # 4. Add to book.contacts dictionary
    # 5. Increment next_contact_id
    # 6. Save the book
    # 7. Log the action
    # 8. Return success message with the new contact ID
    pass
```

#### Function 3: `update_contact`

```python
def update_contact(
    book_name: str,
    contact_id: int,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    notes: Optional[str] = None
) -> str:
    """
    Updates an existing contact's information.
    Only provided fields will be updated.
    This tool will be exposed to the AI agent via MCP.
    
    Args:
        book_name: Name of the contact book
        contact_id: ID of the contact to update
        name: New name (optional, keeps existing if not provided)
        email: New email (optional, keeps existing if not provided)
        phone: New phone (optional, keeps existing if not provided)
        notes: New notes (optional, keeps existing if not provided)
    
    Returns:
        str: Success or error message
    """
    # TODO: Implement this function
    # 1. Load the contact book
    # 2. Check if contact_id exists
    # 3. Update only the fields that are not None
    # 4. Update the updated_at timestamp
    # 5. Save the book
    # 6. Log the action
    # 7. Return success message
    pass
```

#### Function 4: `delete_contact`

```python
def delete_contact(book_name: str, contact_id: int) -> str:
    """
    Removes a contact from the contact book.
    This tool will be exposed to the AI agent via MCP.
    
    Args:
        book_name: Name of the contact book
        contact_id: ID of the contact to delete
    
    Returns:
        str: Success or error message
    """
    # TODO: Implement this function
    # 1. Load the contact book
    # 2. Check if contact_id exists
    # 3. Remove from book.contacts dictionary
    # 4. Save the book
    # 5. Log the action
    # 6. Return success message
    pass
```

#### Function 5: `search_contacts`

```python
def search_contacts(
    book_name: str, 
    query: str,
    search_in: str = "name"
) -> str:
    """
    Searches for contacts matching the query.
    This tool will be exposed to the AI agent via MCP.
    
    Args:
        book_name: Name of the contact book
        query: Search term
        search_in: Field to search in ("name", "email", "phone", "notes", or "all")
    
    Returns:
        str: JSON string of matching contacts or error message
    """
    # TODO: Implement this function
    # 1. Load the contact book
    # 2. Filter contacts based on query and search_in parameter
    # 3. Convert matching contacts to list of dicts
    # 4. Return as JSON string
    # 5. Handle case where no matches found
    
    # HINT: Use case-insensitive search with .lower()
    pass
```

---

## 🔌 Part 3: MCP Server Entry Point (5 minutes)

### Task 3.1: Create `contact_manager_server.py`

This is the simplest file—it just makes your functions discoverable by MCP.

```python
# contact_manager_server.py

# TODO: Import all five tool functions from contact_manager
from contact_manager import (
    # YOUR IMPORTS HERE
)

# That's it! The MCP framework will discover these functions automatically.
```

**✓ Checkpoint:** This file should be ~5 lines (imports only).

---

## 🤖 Part 4: Agent Integration (20 minutes)

### Task 4.1: Create `test_agent.py`

Create a script to test your MCP server with an AI agent:

```python
from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
import asyncio

# Load environment variables
load_dotenv(override=True)

# Define MCP server parameters
params = {
    "command": "uv", 
    "args": ["run", "contact_manager_server.py"]
}

# Agent instructions
instructions = """
You are a helpful contact management assistant. You can:
1. Create contact books
2. Add new contacts with their details
3. Update existing contact information
4. Delete contacts
5. Search for contacts

Always confirm actions and provide clear, concise feedback.
"""

async def test_tool_discovery():
    """First, verify that tools are properly exposed."""
    print("=" * 60)
    print("TEST 1: Tool Discovery")
    print("=" * 60)
    
    async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as server:
        tools = await server.list_tools()
        print(f"\n✓ Discovered {len(tools)} tools:\n")
        for tool in tools:
            print(f"  • {tool['name']}")
            print(f"    {tool['description']}")
            print()

async def test_agent_interaction():
    """Test the agent's ability to use your tools."""
    print("=" * 60)
    print("TEST 2: Agent Interaction")
    print("=" * 60)
    
    # Test request
    request = """
    Please do the following:
    1. Create a contact book called 'work'
    2. Add a contact: John Doe, john.doe@company.com, phone: 555-0123
    3. Add a contact: Jane Smith, jane.smith@company.com, notes: CEO
    4. Search for all contacts with 'company.com' in their email
    """
    
    async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as mcp_server:
        agent = Agent(
            name="contact_manager_agent",
            instructions=instructions,
            model="gpt-4o-mini",  # Or your preferred model
            mcp_servers=[mcp_server]
        )
        
        print("\n🤖 Running agent...\n")
        with trace("contact_manager_test"):
            result = await Runner.run(agent, request)
        
        print("\n📊 Agent Response:")
        print("-" * 60)
        print(result.final_output)
        print("-" * 60)

async def main():
    """Run all tests."""
    await test_tool_discovery()
    print("\n" * 2)
    await test_agent_interaction()

# Execute
if __name__ == "__main__":
    asyncio.run(main())
```

### Task 4.2: Run Your Tests

```bash
uv run python test_agent.py
```

**Expected Output:**
1. List of 5 discovered tools (create, add, update, delete, search)
2. Agent successfully executing the multi-step request
3. Confirmation messages for each action

**✓ Checkpoint:** 
- [ ] All 5 tools are discovered
- [ ] Agent successfully creates contact book
- [ ] Agent successfully adds contacts
- [ ] Agent successfully searches contacts
- [ ] Check `data/` directory for created files

---

## 🧪 Part 5: Verification & Testing (15 minutes)

### Task 5.1: Manual Verification

Verify your implementation by checking the data files:

```bash
# List all created files
ls data/

# View the contact book
cat data/contactbook_work.json

# View the logs
cat data/log_work.json
```

### Task 5.2: Edge Case Testing

Test these edge cases by creating additional agent requests:

1. **Duplicate Contact Book:**
   ```python
   request = "Create a contact book called 'work'"  # Should already exist
   ```

2. **Invalid Contact ID:**
   ```python
   request = "Update contact 999 in the 'work' book"  # ID doesn't exist
   ```

3. **Empty Search:**
   ```python
   request = "Search for 'nonexistent@email.com' in the 'work' book"
   ```

4. **Update Partial Fields:**
   ```python
   request = "Update contact 1 in 'work': change phone to 555-9999, keep everything else"
   ```

**Document Results:**
Create a file `test_results.md` and note which edge cases work correctly and which might need improvement.

---

## 📊 Part 6: Analysis & Reflection (20 minutes)

### Question 1: Architecture & Cost Analysis

**Scenario:** Your contact management system is deployed in production. It receives 10,000 contact additions per day, 5,000 searches per day, and 1,000 updates per day.

**a) Calculate Token Cost:**
- Assume average tool call: 100 input tokens + 50 output tokens
- Pricing: $0.15 per 1M input tokens, $0.60 per 1M output tokens (GPT-4o-mini rates)
- Calculate: Daily cost? Monthly cost? Annual cost?

**b) Identify Bottlenecks:**
- Which operation (add, search, update) would be slowest at scale?
- Where in your code would you add caching?
- How would you optimize the `search_contacts` function for 100,000 contacts?

**Write your analysis in `analysis.md`.**

---

### Question 2: Security & Privacy

**Scenario:** Your contact management system will store sensitive customer information (emails, phone numbers, notes).

**a) Current Security Vulnerabilities:**
List 3 security issues with the current implementation:
1. ?
2. ?
3. ?

**b) Proposed Solutions:**
For each vulnerability, propose a concrete fix:
1. ?
2. ?
3. ?

**c) Data Privacy:**
- Should the agent have access to a `delete_all_contacts` tool? Why or why not?
- How would you implement audit logging to track who accessed which contacts?
- What data should never be logged (even in `log_*.json` files)?

**Write your answers in `analysis.md`.**

---

### Question 3: Design Decision Justification

**a) Why Three Files?**
Explain why we separate `database.py`, `contact_manager.py`, and `contact_manager_server.py`. What would be the consequences of combining them into one file?

**b) Pydantic vs. Plain Dictionaries:**
Your Contact model uses Pydantic. What happens if someone tries to create a contact with `email="not-an-email"`? How is this better than using plain Python dictionaries?

**c) stdio vs. SSE:**
Compare these two deployment scenarios:
- **Scenario A:** Personal desktop app (only you use it)
- **Scenario B:** Team collaboration tool (10 people use it)

Which communication method (stdio or SSE) would you choose for each? Justify your answer.

**Write your answers in `analysis.md`.**

---

### Question 4: Extension Challenge (Optional Bonus)

**Design (don't implement) a new tool:** `export_contacts`

**Requirements:**
- Export all contacts to CSV format
- Include command-line option to choose fields (e.g., only name and email)
- Handle special characters in notes field (commas, quotes)

**Write a design specification in `analysis.md`:**
1. Function signature with type hints
2. Docstring
3. Pseudocode or flowchart
4. Edge cases to handle
5. Example CSV output

---

## 📦 Submission Requirements

### Required Files

Post this to your appropriate GitHub repository:

```
mcp_lab_contact_manager
├── database.py                    # Your data persistence layer
├── contact_manager.py             # Your business logic (models + tools)
├── contact_manager_server.py      # Your MCP server entry point
├── test_agent.py                  # Your agent test script
├── test_results.md                # Edge case test results
├── analysis.md                    # Answers to reflection questions
├── requirements.txt               # Dependencies list
└── data/                          # Sample data files (at least one contact book)
    ├── contactbook_work.json
    └── log_work.json
```

**DO NOT INCLUDE:**
- `.env` file (contains secrets!)
- `__pycache__/` directories
- `.venv/` or virtual environment folders

---

## ✅ Assessment Rubric

### Pass Criteria (Required for Credit):

| **Criterion**                                  | **Points** | **Description**                                                                 |
|------------------------------------------------|------------|---------------------------------------------------------------------------------|
| **Environment is Reproducible**                | 15         | Code runs on instructor machine without modification                           |
| **API Keys Secured**                           | 10         | No hardcoded keys; uses `.env` properly                                         |
| **All 5 Tools Implemented**                    | 25         | create, add, update, delete, search all work correctly                          |
| **Proper Type Hints**                          | 10         | All functions have complete type annotations                                    |
| **Docstrings Present**                         | 5          | All tools have descriptive docstrings                                           |
| **Three-Layer Architecture**                   | 10         | Clear separation: database, logic, server                                       |
| **Agent Successfully Executes**                | 10         | test_agent.py runs without errors                                               |
| **Reflection Questions Answered**              | 15         | All analysis questions answered with reasoning                                  |

**Total: 100 points**

---

### Bonus Points (Optional):

| **Criterion**                                  | **Points** |
|------------------------------------------------|------------|
| **Edge Case Handling**                         | +5         | Gracefully handles all edge cases listed                                        |
| **Extension Challenge Design**                 | +5         | Well-thought-out design for `export_contacts` tool                              |
| **Performance Optimization**                   | +3         | Implements caching or search optimization                                       |
| **Comprehensive Testing**                      | +2         | Additional test cases beyond requirements                                       |

**Maximum Score: 115 points**

---

### Fail Criteria (Automatic Zero):

- ❌ Hardcoded API keys in any file
- ❌ Code does not run (missing dependencies, syntax errors)
- ❌ Lab is exact copy of demo (task manager instead of contact manager)
- ❌ Missing required files (database.py, contact_manager.py, server.py)
- ❌ No agent integration (test_agent.py missing or doesn't work)

---

## 🆘 Common Issues & Troubleshooting

### Issue 1: "No tools discovered"

**Symptoms:** `test_agent.py` reports 0 tools found.

**Causes:**
- Missing imports in `contact_manager_server.py`
- Functions don't have type hints
- Functions don't have docstrings

**Fix:**
1. Verify all 5 functions are imported in `contact_manager_server.py`
2. Check every function has `-> str` return type
3. Add docstrings to all functions

---

### Issue 2: "Pydantic validation error"

**Symptoms:** Error message mentions "validation error" or "input should be..."

**Causes:**
- Passing wrong data type to Pydantic model
- Email format invalid (EmailStr requires proper email)
- Required field is None

**Fix:**
1. Check the error message—it tells you which field and what type is expected
2. Verify Contact model fields match function parameters
3. Use Optional[str] for fields that can be None

---

### Issue 3: "Connection timeout" or "Server failed to start"

**Symptoms:** Agent hangs or reports timeout error.

**Causes:**
- uv not installed or not in PATH
- Syntax error in your Python files prevents server from starting
- Wrong file name in params (e.g., "task_manager_server.py" instead of "contact_manager_server.py")

**Fix:**
1. Test manually: `uv run contact_manager_server.py` in terminal
2. Check for syntax errors: `python -m py_compile contact_manager.py`
3. Verify file names match exactly in `test_agent.py`

---

### Issue 4: "File not found" when running agent

**Symptoms:** Agent reports contact book doesn't exist even after creating it.

**Causes:**
- Not saving after creating ContactBook
- Wrong directory (`data/` folder not created)
- Name mismatch (searching for "Work" but created "work")

**Fix:**
1. Verify `data/` directory exists in your project root
2. Check file names: `ls data/`
3. Ensure `ContactBook.save()` is called after modifications
4. Use `.lower()` for consistent naming

---

## 📚 Resources & References

### Official Documentation:
- **Pydantic:** https://docs.pydantic.dev/
- **Agents Framework:** https://docs.agents.dev/
- **Asyncio:** https://docs.python.org/3/library/asyncio.html

### Course Materials:
- Glossary (Module 04)
- Instructor Demo (Module 04)
- Week 2: LLM APIs & Structured Output

### Getting Help:
1. **Re-watch the Demo:** Review the instructor demonstration video
2. **Check Logs:** Look at `data/log_*.json` for error details
3. **Office Hours:** [Instructor: Add times]
4. **Discussion Forum:** [Instructor: Add link]
5. **Pair Programming:** Work with a classmate (but submit individual work)

---

## 🎓 Learning Outcomes Verification

Before submitting, verify you can answer "yes" to these questions:

- [ ] I can explain what MCP is and why it's useful
- [ ] I can describe the three-layer architecture pattern
- [ ] I can create Pydantic models with proper validation
- [ ] I can write MCP tool functions with type hints and docstrings
- [ ] I can connect an AI agent to a custom MCP server
- [ ] I can debug tool execution issues
- [ ] I can analyze architectural trade-offs
- [ ] I understand security implications of AI tool access

---

## 🚀 After Submission: Next Steps

**Advanced Extension:**
If you finish early and want a challenge, try:
1. Add a `merge_contact_books` tool that combines two books
2. Implement fuzzy search (handles typos in search queries)
3. Add a `backup_to_cloud` tool using an S3 MCP server
4. Create a web interface using Streamlit to visualize contacts

---

**End of Lab Assignment**  

**Good luck! Remember: Focus on understanding the patterns, not just completing the checklist. The goal is to build mental models you can apply to any MCP server design.**

**Questions? See the "Getting Help" section above.**
