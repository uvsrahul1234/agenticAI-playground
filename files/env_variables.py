from dotenv import load_dotenv
import requests
import os

load_dotenv(override=True)

def is_service_running(url):
    """
    Checks if a service is running by attempting to connect to its URL.
    """
    try:
        response = requests.get(url, timeout=5)
        # Ollama and LM Studio return "Ollama is running" or similar on their base URL
        # A 200 status code indicates the server is up.
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.Timeout:
        return False
    return False

openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')
hf_token = os.getenv('HF_TOKEN')
ollama_url = 'http://localhost:11434'
lmstudio_url = 'http://localhost:1234'

def check_services():
    print("--- Local LLM Service Checks ---")
    # Check for Ollama    
    if is_service_running(ollama_url):
        print("Ollama is running")
    else:
        print("Ollama is not running")

    # Check for LM Studio    
    if is_service_running(lmstudio_url):
        print("LM Studio is running")
    else:
        print("LM Studio is not running")

    if openai_api_key:
        print(f"OpenAI API Key exists")
    else:
        print("OpenAI API Key not set")

    if anthropic_api_key:
        print(f"Anthropic API Key exists")
    else:
        print("Anthropic API Key not set")

    if google_api_key:
        print(f"Google API Key exists")
    else:
        print("Google API Key not set")

    if deepseek_api_key:
        print(f"DeepSeek API Key exists")
    else:
        print("DeepSeek API Key not set")

    if groq_api_key:
        print(f"Groq API Key exists")
    else:
        print("Groq API Key not set")
        
    if hf_token:
        print(f"Hugging Face Token exists")
    else:
        print("Hugging Face Token not set")
