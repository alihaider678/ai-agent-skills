import asyncio
import base64
import os
from openai import AsyncOpenAI
from playwright.async_api import async_playwright
from src.config import settings
from src.tools.browser import BrowserTool
from src.tools.accessibility import AccessibilityTool

# Initialize OpenAI Client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def run_audit_agent(url: str):
    """
    The Main Brain. 
    Orchestrates the browser, the vision analysis, and the technical audit.
    """
    print(f"\n🤖 AGENT ACTIVATED: Auditing {url}\n" + "="*50)

    async with async_playwright() as p:
        # 1. Launch Browser
        browser = await p.chromium.launch(headless=True) # Set False to watch it work
        page = await browser.new_page()
        
        # 2. Navigate
        print("🌍 Navigating to site...")
        await page.goto(url, timeout=settings.TIMEOUT_MS, wait_until="domcontentloaded")

        # 3. TOOL 1: Take Screenshot (Visual Data)
        print("👁️  Agent is looking at the page...")
        screenshot_path = settings.OUTPUT_DIR / "audit_screenshot.png"
        await page.screenshot(path=str(screenshot_path), full_page=False)
        
        # Convert image for OpenAI
        with open(screenshot_path, "rb") as img:
            base64_image = base64.b64encode(img.read()).decode('utf-8')

        # 4. TOOL 2: Run Technical Scan (Code Data)
        print("🧠 Agent is running technical diagnostics...")
        tech_report = await AccessibilityTool.scan_page(page)
        
        # 5. The Analysis (Send everything to GPT-4o)
        print("📝 Generating Final Report...")
        
        PROMPT = f"""
        You are a Senior UI/UX Engineer and Accessibility Expert.
        
        I have provided you with:
        1. A screenshot of the website (Visual Context).
        2. A technical accessibility report (Code Context).

        TECHNICAL REPORT:
        {tech_report}

        YOUR TASK:
        Analyze this website and provide a professional audit.
        1. VISUAL DESIGN: Critique color, spacing, and layout.
        2. ACCESSIBILITY: Summarize the technical errors found.
        3. CODE FIXES: Provide specific Tailwind CSS or HTML fixes for the errors.
        
        Be critical and precise.
        """

        response = await client.chat.completions.create(
            model="gpt-4o", # We need the Vision model
            messages=[
                {
                    "role": "system", 
                    "content": "You are a pixel-perfect design auditor."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ],
                }
            ],
            max_tokens=1000
        )

        # 6. Output the Result
        final_advice = response.choices[0].message.content
        print("\n" + "="*50)
        print("📄 FINAL AUDIT REPORT")
        print("="*50)
        print(final_advice)
        
        # Cleanup
        await browser.close()

if __name__ == "__main__":
    # Change this URL to whatever you want to test
    TARGET_URL = "https://google.com" 
    asyncio.run(run_audit_agent(TARGET_URL))