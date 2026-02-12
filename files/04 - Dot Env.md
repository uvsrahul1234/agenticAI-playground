## **DOTENV**

The **.env file** is a plain text file used to store **environment-specific configuration variables** for an application, especially in development and testing. ⚙️


### **Description of the .env File**



* **Purpose:** It holds configuration settings like **database credentials** (usernames, passwords), **API keys**, **secret keys**, and other values that might change depending on the environment (e.g., development, staging, production) or that need to be kept out of the main codebase for security reasons.
* **Format:** Variables are typically defined in a simple **key=value** format, one per line (e.g., DB_HOST=localhost, API_KEY="your-secret-key").
* **Security:** A critical use is to keep sensitive secrets **out of version control** (like Git) by adding .env to the project's .gitignore file. This prevents accidentally exposing credentials when sharing code.


### **DOTENV**

The following statement

 from dotenv import load_dotenv 

is used to load the variables stored in the .env file into your application's **runtime environment variables**.



1. **Import:** The load_dotenv function is imported, typically from the popular Python **python-dotenv** library.
2. **Execution:** When you call load_dotenv(), the function:
    * **Searches** for a file named .env in the current directory and parent directories.
    * **Reads** the key=value pairs from the file.
    * **Sets** those key=value pairs as operating system **environment variables** (accessible via os.environ in Python).
3. **Usage in Code:** Once loaded, your application can access the values using standard environment variable retrieval methods, such as:

This allows the code to access configuration securely without hardcoding secrets directly into source files.

Here is an example of the content in the .env file.

MY_VARIABLE=example_value

OPENAI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

HF_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

WEATHER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

GEO_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

GROQ_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
