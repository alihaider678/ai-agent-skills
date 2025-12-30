# 🎓 AI Tutor: RAG Knowledge Pipeline

> **A Retrieval Augmented Generation (RAG) system that transforms raw video content into an intelligent, interactive teaching assistant.**

---

## 🚀 Overview

Standard LLMs (like ChatGPT) hallucinate when asked about specific, private data. This project solves that by building a **Ground-Truth Knowledge Base**. 

It implements a robust ETL (Extract, Transform, Load) pipeline that can ingest video content, "memorize" it into a Vector Database, and allow users to chat with the content with zero hallucinations. It is designed to work even in network-restricted environments using robust extraction tools.

## 🛠️ Tech Stack

*   **LLM & Embeddings:** OpenAI (GPT-4o, text-embedding-3-small)
*   **Vector Database:** ChromaDB (Persistent Storage)
*   **ETL Pipeline:** yt-dlp (Extraction), WebVTT (Cleaning)
*   **Search Logic:** Semantic Similarity Search

## ✨ Key Features

1.  **🚜 Robust Data Ingestion (The Tank):**
    *   Uses `yt-dlp` instead of standard APIs to bypass region blocks and restrictions.
    *   Automatically extracts subtitles, cleans timestamps, and formats text for AI processing.

2.  **🧠 Persistent Memory:**
    *   Uses **ChromaDB** to store knowledge on disk.
    *   You only need to ingest a video *once*. The AI remembers it forever, even after restarting the computer.

3.  **🔍 Smart Semantic Search:**
    *   Doesn't just match keywords. It understands *meaning*.
    *   Example: Searching for "How to prompt" will successfully find content discussing "Instructions for LLMs."

4.  **🛡️ Hallucination Guardrails:**
    *   The system uses strict System Prompts to ensure it **only** answers based on the provided video context. If the answer isn't in the video, it admits ignorance rather than lying.

## 💼 Business Use Cases

*   **Corporate Onboarding:** Ingest 50 hours of internal training videos so new employees can ask, "How do I file expenses?" and get an instant answer.
*   **Content Creator Tools:** Allow YouTubers/Podcasters to search their own back-catalog to find exact moments they mentioned a topic.
*   **EdTech:** Create personalized tutors for university lectures where students can ask questions about specific parts of a recorded class.

## ⚙️ How to Run

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Secrets:**
    Create a `.env` file:
    ```env
    OPENAI_API_KEY="sk-..."
    ```

3.  **Step 1: Ingest Data (Teach the AI)**
    This downloads the video and saves it to the Brain (`db/` folder).
    ```bash
    python -m src.ingest
    ```

4.  **Step 2: Start the Tutor (Chat)**
    This launches the interactive session.
    ```bash
    python -m src.tutor
    ```

## 🧠 Architecture Flow

1.  **User Input:** "Summarize the key points."
2.  **Embedding:** Query is converted to a Vector (List of numbers).
3.  **Retrieval:** ChromaDB finds the top 7 most relevant chunks of text from the video.
4.  **Synthesis:** GPT-4o reads the chunks + the user question and generates a fact-based answer.

---
*Built as part of the AI Agent Skills Portfolio.*