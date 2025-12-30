import os
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from colorama import Fore, Style, init
from src.config import settings

# Initialize Colors for the Terminal
init(autoreset=True)

class AITutor:
    """
    The RAG Brain.
    Retrieves knowledge from ChromaDB and generates answers using GPT-4o.
    """
    
    def __init__(self):
        # 1. Connect to the same DB where we saved the data
        self.client = chromadb.PersistentClient(path=str(settings.DB_PATH))
        
        # 2. Use the exact same translator (Embedding Function)
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.EMBEDDING_MODEL
        )
        
        self.collection = self.client.get_collection(
            name=settings.COLLECTION_NAME,
            embedding_function=openai_ef
        )
        
        self.ai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        print(f"{Fore.GREEN}✅ Tutor Online. Connected to Knowledge Base.")

    def ask(self, query: str):
        """
        The Thinking Process: Search -> Contextualize -> Answer.
        """
        print(f"{Fore.CYAN}🔍 Searching knowledge base...")
        
        # --- STEP 1: RETRIEVAL ---
        # Search the DB for the 3 most relevant chunks
        results = self.collection.query(
            query_texts=[query],
            n_results=7
        )
        
        # Extract the text from the search results
        context_chunks = results['documents'][0]
        
        if not context_chunks:
            return "I couldn't find any relevant information in the video."

        # Combine chunks into a single block of text
        context_text = "\n\n".join(context_chunks)
        
        # --- STEP 2: GENERATION ---
        print(f"{Fore.CYAN}🧠 Thinking...")
        
        PROMPT = f"""
        You are an expert AI Tutor. 
        Answer the question based on the context provided below.
        If the context contains partial information, summarize what is there.
        Only say "I don't know" if the context is completely irrelevant.

        --- CONTEXT FROM VIDEO ---
        {context_text}
        --------------------------

        QUESTION: {query}
        """

        response = self.ai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful teacher."},
                {"role": "user", "content": PROMPT}
            ]
        )
        
        return response.choices[0].message.content

# Main Chat Loop
if __name__ == "__main__":
    tutor = AITutor()
    
    print(f"\n{Fore.YELLOW}🎓 AI TUTOR READY! (Type 'quit' to exit)")
    print("Ask me anything about the video you just ingested.")
    print("-" * 50)
    
    while True:
        user_input = input(f"\n{Fore.WHITE}You: ")
        if user_input.lower() in ["quit", "exit"]:
            break
            
        answer = tutor.ask(user_input)
        print(f"\n{Fore.GREEN}Tutor:{Style.RESET_ALL} {answer}")
        print("-" * 50)