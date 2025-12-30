# 🕵️‍♂️ Autonomous UI/UX Auditor

> **An intelligent agent that crawls websites, simulates multi-device viewports, performs technical accessibility audits (Axe-Core), and provides AI-driven design fixes.**

---

## 🚀 Overview

This is not just a chatbot; it is a **Quality Assurance Automation Pipeline**.
Most AI design tools only "look" at a screenshot. This agent combines **Computer Vision** (GPT-4o) with **Ground-Truth Data** (DOM Injection) to provide audits that are both creatively insightful and mathematically accurate.

It features an **Autonomous Spider** that can discover internal links and audit an entire portfolio or documentation site in one batch process.

## 🛠️ Tech Stack

* **Core Logic:** Python 3.10+, AsyncIO
* **Browser Automation:** Playwright (Headless Chromium)
* **AI Vision:** OpenAI GPT-4o
* **Technical Audit Engine:** Axe-Core (Injected via JavaScript)
* **Data Handling:** Base64 Image Processing, Regex Pattern Matching

## ✨ Key Features

1. **🕷️ Autonomous Crawling:**
    * Starts at a homepage and intelligently finds internal links (e.g., `/about`, `/services`).
    * Uses a Queue system to audit multiple pages automatically without human intervention.
    * Implements Domain Locking to prevent wandering off to external sites (like Instagram/LinkedIn).

2. **📱 Multi-Viewport Analysis:**
    * Simulates real mobile devices (iPhone/Pixel viewports) to check Responsive Design.
    * Captures **Full-Page** screenshots (scrolling capture), not just "above the fold."

3. **🩺 Hybrid Auditing:**
    * **Visual:** Uses GPT-4o Vision to critique color hierarchy, whitespace, and branding.
    * **Technical:** Injects `axe-core` libraries into the browser to detect WCAG compliance failures (contrast ratios, missing ARIA labels).

4. **🛡️ Self-Healing Infrastructure:**
    * Automatically downloads necessary dependencies (like the Axe engine) locally if internet access is restricted.

## 💼 Business Use Cases

* **Web Development Agencies:** Run this agent before launching a client site to catch embarrassing errors (broken mobile views, missing alt tags).
* **Compliance Automation:** Ensure websites meet **ADA/WCAG Legal Standards** for accessibility without hiring expensive manual auditors.
* **CI/CD Integration:** Can be deployed in a GitHub Action to block code merges if the design score drops below a certain threshold.

## ⚙️ How to Run

1. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    playwright install chromium
    ```

2. **Configure Secrets:**
    Create a `.env` file and add your OpenAI Key:

    ```env
    OPENAI_API_KEY="sk-..."
    ```

3. **Run the Agent:**
    To start the autonomous crawler on a target site:

    ```bash
    python -m src.main
    ```

## 📊 Sample Output

The agent generates a structured report for every page visited:

> **✅ REPORT FOR: ABOUT_PAGE**
>
> * **Visuals:** "The contrast on the 'Call to Action' button is too low for mobile users."
> * **Accessibility:** "Critical: Missing <main> landmark. Found 3 buttons without ARIA labels."
> * **Code Fix:** "Recommended Tailwind change: `text-gray-400` -> `text-gray-700`."

---
*Built as part of the AI Agent Skills Portfolio.*
