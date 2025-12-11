# 🕵️ Agent Skill: Secrets Sniffer

A smart security auditing tool that uses **Agentic AI** to filter out false positives.

## The Problem

Traditional security tools use Regex. They flag everything, including:

- `api_key = "placeholder"` (Safe)
- `db_password = os.getenv("DB_PASS")` (Safe)

Developers get "alert fatigue" and ignore real warnings.

## The Solution

This tool uses the **Anthropic "Skills" Architecture**:

1. **The Tool (`scan.py`)**: A Python script finds *potential* matches using Regex.
2. **The Knowledge (`docs.md`)**: A rulebook that defines what a real secret looks like.
3. **The Agent (`analyze.py`)**: Uses LLM (GPT-4o) to read the code context and decide if it's a real risk.

## How to Run

1. Install dependencies: `pip install openai python-dotenv`
2. Set up your `.env` with `OPENAI_API_KEY`.
3. Run the agent:

   ```bash
   cd skill
   python analyze.py ../dummy_project
