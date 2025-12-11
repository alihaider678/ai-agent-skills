import os
import subprocess
import json
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load the API Key from the .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def run_scanner():
    """Runs the scan.py script and captures the JSON output."""
    # Running the tool (The Hunter)
    result = subprocess.run(
        ["python", "scan.py", "../dummy_project"], 
        capture_output=True, 
        text=True
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return []

def read_docs():
    """Reads the instruction manual (The Knowledge)."""
    try:
        with open("docs.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "No documentation found."

def analyze_with_agent():
    print("🕵️  Agent is starting...")
    
    # --- Step 1: Use the Tool ---
    print("1. Running scan tool...")
    raw_findings = run_scanner()
    print(f"   -> Found {len(raw_findings)} potential matches.")

    # --- Step 2: Get the Knowledge ---
    print("2. Reading skill documentation...")
    rules = read_docs()

    # --- Step 3: Construct the Prompt ---
    # This combines the "Dumb" tool output with the "Smart" docs
    prompt = f"""
    You are a Senior Security Engineer.
    
    I have run a pattern matching tool to find secrets in my code.
    Here is the RAW OUTPUT from the tool:
    {json.dumps(raw_findings, indent=2)}

    Here are the RULES for analyzing these findings:
    {rules}

    TASK:
    Analyze the raw output against the rules.
    1. Filter out the False Positives (like placeholders or test files).
    2. Identify TRUE POSITIVES (Critical risks).
    3. For each True Positive, explain WHY it is dangerous based on the rules.
    
    Output format:
    Provide a concise report.
    """

    # --- Step 4: The Intelligence Layer (OpenAI) ---
    if api_key:
        print("3. Sending to OpenAI (GPT-4o) for analysis...")
        
        client = OpenAI(api_key=api_key)
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",  # You can use "gpt-4-turbo" or "gpt-3.5-turbo" too
                messages=[
                    {"role": "system", "content": "You are a helpful security assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            print("\n" + "="*40)
            print("🤖 AGENT REPORT")
            print("="*40)
            print(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
    else:
        print("\n❌ Error: No OPENAI_API_KEY found in .env file.")

if __name__ == "__main__":
    analyze_with_agent()