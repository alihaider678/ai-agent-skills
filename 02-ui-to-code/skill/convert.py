import os
import sys
import base64
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load API Key
load_dotenv("../../.env") # Looks for .env in the root folder
client = OpenAI()

def encode_image(image_path):
    """Encodes an image to base64 so GPT-4o can see it."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def read_design_system():
    """Reads the strict design rules."""
    try:
        with open("skill/design_system.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        # Fallback if running from inside the skill folder
        with open("design_system.md", "r") as f:
            return f.read()

def convert_ui(image_path, output_filename="index.html"):
    print(f"👁️  Analyzing {image_path}...")
    
    # 1. Prepare Data
    base64_image = encode_image(image_path)
    design_rules = read_design_system()
    
    # 2. The Prompt
    prompt = f"""
    You are an Expert Frontend Engineer. 
    I will provide a UI screenshot. Your job is to convert it into PIXEL-PERFECT HTML + Tailwind CSS.
    
    CRITICAL: You must follow the Design System rules below. 
    If the screenshot uses a color that doesn't match the system, snap it to the nearest allowed color in the system.
    
    DESIGN SYSTEM:
    {design_rules}
    
    Return ONLY the raw HTML code. Do not include markdown formatting like ```html.
    """

    # 3. Call GPT-4o (Vision)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        max_tokens=4000,
    )

    code = response.choices[0].message.content
    
    # Clean up markdown if the AI added it anyway
    code = code.replace("```html", "").replace("```", "")

    # 4. Save to file
    output_path = f"output_html/{output_filename}"
    with open(output_path, "w") as f:
        f.write(code)
        
    print(f"✅ Code generated! Saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py <image_path>")
    else:
        # Ensure output directory exists
        os.makedirs("output_html", exist_ok=True)
        convert_ui(sys.argv[1])