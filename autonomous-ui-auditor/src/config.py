import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Centralized configuration for the Autonomous UI Auditor.
    Acts as the single source of truth for file paths and settings.
    """
    
    # 1. Project Paths
    # We use .resolve() to get the absolute path of 'src/config.py'
    # .parent gives 'src', .parent.parent gives 'autonomous-ui-auditor' root
    BASE_DIR = Path(__file__).resolve().parent.parent
    OUTPUT_DIR = BASE_DIR / "output"
    
    # 2. Browser Settings
    # We define standard viewports for Responsive Design testing
    VIEWPORTS = {
        "desktop": {"width": 1920, "height": 1080},
        "tablet": {"width": 768, "height": 1024},
        "mobile": {"width": 375, "height": 667}
    }
    
    # 3. Timeouts (in milliseconds)
    # Give the page 15 seconds to load (safer for slow sites)
    TIMEOUT_MS = 30000  # 30 Seconds
    
    # 4. Agent Identity
    AGENT_NAME = os.getenv("AGENT_NAME", "UI-Auditor-v1")
    
    # Ensure output directory exists when config is loaded
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Create a global instance
settings = Config()