import base64
from typing import Dict, Any
from playwright.async_api import async_playwright
from src.config import settings

class BrowserTool:
    """
    The 'Eyes' of the agent. 
    Handles browser automation, viewport resizing, and screenshot capture.
    """

    @staticmethod
    async def capture_screenshot(url: str, device_type: str = "desktop") -> Dict[str, Any]:
        """
        Navigates to a URL and captures a screenshot for the specific device type.
        Returns a base64 encoded image string (AI friendly format).
        """
        
        # Validation: Fail fast if the device type is wrong
        if device_type not in settings.VIEWPORTS:
            return {"error": f"Invalid device type. Choose: {list(settings.VIEWPORTS.keys())}"}

        viewport = settings.VIEWPORTS[device_type]
        screenshot_path = settings.OUTPUT_DIR / f"screenshot_{device_type}.png"

        try:
            # Context Manager handles opening/closing the browser automatically
            async with async_playwright() as p:
                # Launch Chromium (Headless = No visible UI, faster)
                # Note: If debugging, set headless=False to watch the robot work
                browser = await p.chromium.launch(headless=True)
                
                # Create a context with the specific screen size
                context = await browser.new_context(
                    viewport=viewport,
                    user_agent="Mozilla/5.0 (compatible; UI-Auditor/1.0)"
                )
                
                page = await context.new_page()
                
                # Navigate and wait for network to be idle (page fully loaded)
                print(f"🌍 Navigating to {url} on {device_type}...")
                await page.goto(url, timeout=settings.TIMEOUT_MS, wait_until="domcontentloaded")
                
                # Snap the picture
                await page.screenshot(path=str(screenshot_path), full_page=False)
                print(f"📸 Screenshot saved to {screenshot_path}")
                
                # Convert to Base64 (So the AI can 'see' it without opening the file)
                with open(screenshot_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

                await browser.close()

                return {
                    "status": "success",
                    "path": str(screenshot_path),
                    "viewport": device_type,
                    "image_data": encoded_string
                }

        except Exception as e:
            # Professional Error Handling: Catch it, report it, don't crash
            print(f"❌ Error: {e}")
            return {"status": "error", "message": str(e)}

# Quick Test to verify this file works in isolation
if __name__ == "__main__":
    import asyncio
    
    # 1. Define a test function
    async def test_run():
        print("🚀 Starting Test Run...")
        # Check Google on Mobile
        result = await BrowserTool.capture_screenshot("https://google.com", "mobile")
        
        if result['status'] == 'success':
            print("✅ Test Passed!")
        else:
            print("⛔ Test Failed!")

    # 2. Execute the test
    asyncio.run(test_run())