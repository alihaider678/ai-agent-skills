# Security Secrets Sniffer Skill

## Description
This skill detects hardcoded secrets, API keys, and passwords in a codebase. 
It combines script-based pattern matching with Agentic reasoning to filter out false positives.

## How to use
1. Run the `scan.py` script.
2. The script returns a JSON list of "Potential Matches".
3. The Agent must analyze the context using the Rules below.

## Analysis Rules

### 🔴 FLAG THESE (High Risk):
- Variables assigned to hardcoded strings (e.g., `api_key = "sk_live_..."`).
- Passwords in plain text (excluding lock files).
- AWS Access Keys (starting with AKIA...).

### 🟢 IGNORE THESE (False Positives):
- Variables inside `/test/`, `/spec/`, or `/mocks/` folders.
- Variables using `os.getenv()` or `process.env`.
- Placeholder text (e.g., "YOUR_KEY_HERE").

## Output Format
If a REAL secret is found:
🚨 **CRITICAL**: Found [Type] in [File]:[Line]. Reasoning: [Context].