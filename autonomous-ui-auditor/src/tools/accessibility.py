import os
import urllib.request
from playwright.async_api import Page
from src.config import settings

class AccessibilityTool:
    """
    The 'Inspector' of the agent.
    Injects the axe-core engine (Industry Standard) to find code errors.
    """
    
    # We will save the engine here so we don't need to download it every time
    AXE_LOCAL_PATH = settings.BASE_DIR / "src" / "tools" / "axe.min.js"
    AXE_URL = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.7.2/axe.min.js"

    @classmethod
    async def _ensure_engine_exists(cls):
        """
        Self-Healing Mechanism:
        Checks if the auditing engine exists locally. If not, downloads it.
        """
        if not os.path.exists(cls.AXE_LOCAL_PATH):
            print("📥 Downloading Accessibility Engine (First Run Only)...")
            try:
                # Use standard library to avoid extra dependencies
                urllib.request.urlretrieve(cls.AXE_URL, cls.AXE_LOCAL_PATH)
                print("✅ Engine downloaded successfully.")
            except Exception as e:
                print(f"❌ Failed to download engine: {e}")
                return False
        return True

    @staticmethod
    async def scan_page(page: Page) -> str:
        """
        Injects the 'axe-core' auditing engine into the page and runs a scan.
        """
        try:
            print("🩺 Injecting Accessibility Engine (Axe-Core)...")
            
            # 1. Ensure we have the engine file locally
            engine_ready = await AccessibilityTool._ensure_engine_exists()
            if not engine_ready:
                return "⚠️ SKIPPED: Could not download auditing engine."

            # 2. Inject the local file (No internet required for this part)
            await page.add_script_tag(path=str(AccessibilityTool.AXE_LOCAL_PATH))
            
            # 3. Run the audit inside the browser console
            results = await page.evaluate("""async () => {
                const results = await axe.run();
                return results.violations;
            }""")
            
            # 4. Process results
            if not results:
                return "✅ PASS: No accessibility violations found."

            report = f"🚨 FAILED: Found {len(results)} Accessibility Violations:\n"
            for i, violation in enumerate(results, 1):
                report += f"\n{i}. Issue: {violation['help']}\n"
                report += f"   - Impact: {violation['impact'].upper()}\n"
                report += f"   - Description: {violation['description']}\n"
                report += f"   - Affected Elements: {len(violation['nodes'])}\n"
            
            return report

        except Exception as e:
            print(f"❌ Scan Error: {e}")
            return f"❌ Accessibility Scan Failed: {str(e)}"