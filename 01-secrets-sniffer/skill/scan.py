import os
import re
import json
import sys

# Regex patterns to catch potential secrets
# Updated to be more permissive to catch our "Fake" GitHub-safe keys
PATTERNS = {
    "AWS Key": r"AKIA[0-9A-Z]{16}",
    # Matches anything starting with sk_live_ (non-whitespace)
    "Stripe Key": r"sk_live_\S+", 
    # Catch generic keys/passwords that are 8+ chars long
    "Generic Secret": r"(key|password|secret|token)\s*=\s*['\"][a-zA-Z0-9_\-]{8,}['\"]"
}

def scan_directory(directory):
    results = []
    
    # Walk through the directory
    for root, _, files in os.walk(directory):
        for file in files:
            # Skip python cache or git files
            if "__pycache__" in root or ".git" in root:
                continue
                
            filepath = os.path.join(root, file)
            
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    
                for line_num, line in enumerate(lines, 1):
                    for label, pattern in PATTERNS.items():
                        if re.search(pattern, line):
                            results.append({
                                "file": filepath,
                                "line_number": line_num,
                                "type": label,
                                "content": line.strip() 
                            })
            except Exception as e:
                # Ignore files we can't read (like images)
                continue
                
    return results

if __name__ == "__main__":
    # Default to scanning the dummy_project folder if no arg provided
    target_dir = "../dummy_project"
    
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
        
    # NOTE: We removed the print("Scanning...") line here
    # so the output is PURE JSON for the Agent to read.
    
    matches = scan_directory(target_dir)
    print(json.dumps(matches, indent=2))