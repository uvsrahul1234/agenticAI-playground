
## **VS CODE SETUP**


### Anaconda 3

[https://www.anaconda.com/](https://www.anaconda.com/) (skip registration)


### **Google Drive for Desktop**

Talk about installing Google Drive for Desktop - [https://support.google.com/a/users/answer/13022292?hl=en](https://support.google.com/a/users/answer/13022292?hl=en) 


### VS Code

Install VS Code - [https://code.visualstudio.com/download](https://code.visualstudio.com/download) 


### VS Code **Extensions - The Core Essentials**

These are the absolute must-haves for any data science work in VS Code.



1. **[Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)** by *Microsoft*
    * **Why you need it:** This is the foundational extension. It provides rich support for the Python language, including IntelliSense (smart code completion), linting (finding errors), debugging, code navigation, and code formatting. It's the engine that powers almost everything else on this list.
2. **[Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)** by *Microsoft*
    * **Why you need it:** This extension transforms VS Code into a fully-featured Jupyter environment. It allows you to create, open, and edit .ipynb files directly. It includes a variable explorer, plot viewer, and data table viewer, giving you that classic notebook experience with the power of a modern IDE. (Note: This is often installed automatically with the main Python extension).
3. **[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)** by *Microsoft*
    * **Why you need it:** Pylance supercharges the Python extension with fast, feature-rich language support. It provides highly accurate type-checking and intelligent auto-completions that will significantly speed up your coding. (Note: This is also usually installed with the Python extension).


### **Data Exploration and Management**

These tools help you look at and interact with your data.



1. **[Data Wrangler](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.datawrangler)** by *Microsoft*
    * **Why you need it:** An incredible tool for data cleaning and preparation. It provides a graphical interface to view and transform your dataframes (like Pandas). It automatically generates the Python code for any cleaning operations you perform, which is fantastic for reproducibility.
2. **[Rainbow CSV](https://marketplace.visualstudio.com/items?itemName=mechatroner.rainbow-csv)** by mechatroner
    * **Why you need it:** This simple extension makes CSV files much more readable by highlighting each column in a different color. It's surprisingly effective when you're scanning through large datasets.


### Getting Started with a Notebook


### Prerequisites (a one-time setup)



1. **VS Code Installed**
2. **Python Extension Installed:** Make sure you have the official[ Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension from Microsoft installed. It comes bundled with the **Jupyter** extension, so you only need to install that one.
3. **A Python Interpreter:** You need a version of Python installed on your computer (e.g., from python.org or via **Anaconda**).


---


### The Easiest Way to Get Started:


#### Start with a blank workspace


### Create a New Notebook

If you don't have a notebook file yet, creating one is just as easy:



1. Open the VS Code Command Palette (Ctrl+Shift+P).
2. Type **Jupyter: Create New Jupyter Notebook** and press Enter.
3. A new, untitled notebook will open. You can start adding code and then save it (Ctrl+S) as a .ipynb file.


#### **1. Select Your Kernel**

The "kernel" is just the specific Python environment that will run your code.



* In the **top-right corner** of the notebook, click on **"Select Kernel"**.
* A dropdown list will appear showing all the Python interpreters VS Code has found on your system. **Just pick one. **Pick the one that has the highest version or starts with base.

**The Magic Step:** If your selected Python environment is missing the necessary packages (like ipykernel), **VS Code will automatically pop up a notification and offer to install them for you.** Just click "Install" and wait for it to finish. This is the main reason this method is so easy.


#### **3. Run Your Code Cells**

Now you are ready to run your code. You have two simple options:



* **Run a Single Cell:** To the left of each code cell, there is a "play" icon. Click it to execute only that cell.
* **Run the Entire Notebook:** In the toolbar at the top of the notebook, click the **"Run All"** button (double play icon). This will execute all the cells from top to bottom.

Try typing print(“Hello World!”) in the cell being sure not to have any spaces before print. Hit the run icon. The output will appear directly below the cell you ran.

That's it! You're now running a Jupyter Notebook natively within VS Code, with all the benefits of a powerful editor like IntelliSense, debugging, and Git integration right at your fingertips.


### 


### **Version Control & Collaboration**

Essential for tracking your work and collaborating with others.



1. **[GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)** by *GitKraken*
    * **Why you need it:** It supercharges the built-in Git capabilities of VS Code. You can see who wrote a line of code at a glance (git blame), view file history, compare branches, and much more, all without leaving your editor.


### **Productivity and AI Assistance**

These will make your workflow smoother and faster.



1. **[GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)** by *GitHub*
    * **Why you need it:** An AI pair programmer that suggests entire lines or blocks of code as you type. It's exceptionally good at boilerplate data science tasks, like writing plotting code, creating dataframes, or setting up machine learning models. Note that this is a paid subscription service, but there's a free trial.


### **How to Install Extensions**

You can install these directly from within VS Code:



1. Open VS Code.
2. Click on the **Extensions** icon in the Activity Bar on the side of the window (it looks like four squares). You can also use the shortcut Ctrl+Shift+X.
3. In the search bar, type the name of the extension you want to install.
4. Find the correct extension in the search results (check the author to be sure) and click the blue **Install** button.


---


### **Starter Pack Summary**

If you only install a few to begin, make it these:



* **Python** (this will likely bring Jupyter and Pylance with it).
* **Data Wrangler** for data exploration.
* **GitLens** for version control.

This setup will give you a robust and efficient environment for all your data science projects. Enjoy!
