# /parent_directory/current_directory/my_script.py

import os
import sys


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import env_variables as ev


print("\n--- Running Script Logic ---")

ev.check_services()

# Access the keys
print(f"OpenAI Key is loaded: {'Yes' if ev.openai_api_key else 'No'}")
print(f"Groq Key is loaded: {'Yes' if ev.groq_api_key else 'No'}")

# Use the service check function
if ev.is_service_running(ev.lmstudio_url):
    print("LM Studio is available.")
else:
    print("LM Studio is NOT available.")
    
if ev.is_service_running(ev.ollama_url):
    print("Ollama is available.")
else:
    print("Ollama is NOT available.")

# Example of a new task
if ev.openai_api_key:
    print("Ready to make an OpenAI API call!")
