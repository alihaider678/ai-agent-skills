# 🎨 Agent Skill: UI Vision & Design System Enforcer

> **"Most AI tools copy pixels. This Agent follows the rules."**

An intelligent Frontend Agent that converts raw UI screenshots into pixel-perfect **HTML + Tailwind CSS**, while strictly enforcing a company's specific **Design System** (Colors, Typography, Spacing).

---

## 🚀 The "Wow" Factor (Why this matters)

If you give a screenshot of **Spotify** (Black & Green) to standard Generative AI, it will generate code with **Green buttons**. That is a brand violation for your company.

**This Agent is different.**
It uses the **Anthropic "Skills" Architecture** to decouple *Intelligence* (Vision) from *Expertise* (Brand Rules).

1. **Input:** A screenshot of a completely different app (e.g., Spotify).
2. **The Brain:** The Agent analyzes the layout, spacing, and text hierarchy.
3. **The Skill:** It references `design_system.md` (The "Acme Corp" Rulebook).
4. **Output:** It refactors the design to use **Acme Blue** and **Slate**, ignoring the original Green colors.

**Result:** Automatic Brand Safety & Compliance.

---

## 📂 Architecture

This project follows the **Agent Skills** pattern:

```text
02-ui-to-code/
├── input_images/       # 📥 Drop screenshots here
├── output_html/        # 📤 Agent generates code here
└── skill/
    ├── design_system.md  # 🧠 THE BRAIN: Strict rules for Colors/Fonts
    └── convert.py        # 🛠️ THE TOOL: Python script connecting Vision AI
```

## The Tech Stack

* Model: GPT-4o (Vision Capabilities)
* Language: Python
* Framework: Tailwind CSS (CDN)
* Concept: Retrieval Augmented Generation (RAG) applied to Design Systems.

## 🛠️ How to Run

1. Prerequisites: Ensure you have your .env file in the root directory with OPENAI_API_KEY.
2. Install Dependencies:

```bash
pip install openai python-dotenv
```

1. Add a Target Image: Save a screenshot (e.g., spotify.png or napkin_sketch.jpg) into the input_images/ folder.
2. Run the Agent:

```bash
cd 02-ui-to-code
python skill/convert.py input_images/your_image.png
```

1. View Results: Open output_html/index.html in your browser.

## 🧪 Experiments & Proof

We tested this agent against "Design Drift":

| Input Image (Spotify) | Agent Output (Acme Corp) | Analysis |
|----------------------|--------------------------|----------|
| Background: Black (#000) | Background: Gray (bg-gray-50) | ✅ Adjusted to Theme |
| Button: Neon Green | Button: Brand Blue (bg-blue-600) | ✅ Enforced Brand Rule |
| Font: Circular | Font: Inter (Google Fonts) | ✅ Enforced Typography |

## 📜 The Skill Definition (design_system.md)

The Agent was given these strict instructions:

"You are the Frontend Engineering Agent for Acme Corp. Do not guess colors. Snap all analyzed colors to the nearest variable: Primary Blue (#2563EB), Secondary Slate (#1E293B)."
