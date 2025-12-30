import os
import glob
import webvtt
import chromadb
from yt_dlp import YoutubeDL
from chromadb.utils import embedding_functions
from src.config import settings

class KnowledgeBase:
    """
    Manages the Vector Database.
    Uses yt-dlp to robustly download transcripts when standard APIs fail.
    """
    
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(settings.DB_PATH))
        
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=settings.OPENAI_API_KEY,
            model_name=settings.EMBEDDING_MODEL
        )
        
        self.collection = self.client.get_or_create_collection(
            name=settings.COLLECTION_NAME,
            embedding_function=openai_ef
        )
        print(f"💾 Connected to Knowledge Base: {settings.DB_PATH}")

    def download_and_clean_subs(self, url: str) -> str:
        """
        Uses yt-dlp to download subtitles, cleans them, and returns pure text.
        """
        print("   🚜 Starting yt-dlp (The Tank)...")
        
        # Configuration to download ONLY subs (no video)
        ydl_opts = {
            'skip_download': True,      # Don't download video
            'writeautomaticsub': True,  # Get auto-generated subs
            'writesubtitles': True,     # Get manual subs if exist
            'subtitleslangs': ['en'],   # English only
            'outtmpl': 'temp_subs',     # Save as 'temp_subs'
            'quiet': True,
        }

        # 1. Download the .vtt file
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            raise Exception(f"yt-dlp failed: {e}")

        # 2. Find the file (it adds extensions like .en.vtt)
        vtt_files = glob.glob("temp_subs*.vtt")
        if not vtt_files:
            raise Exception("No subtitle file found! Video might not have captions.")
        
        vtt_path = vtt_files[0]

        # 3. Clean the text using WebVTT
        print(f"   🧹 Cleaning transcript file: {vtt_path}")
        clean_text = ""
        for caption in webvtt.read(vtt_path):
            clean_text += caption.text + " "

        # 4. Cleanup (Delete the temp file)
        os.remove(vtt_path)
        
        return clean_text

    def ingest_youtube_video(self, url: str):
        """
        The ETL Pipeline: Downloads (yt-dlp) -> Chunks -> Stores.
        """
        print(f"\n📺 Processing URL: {url}...")

        try:
            # --- STEP A: EXTRACT ---
            full_text = self.download_and_clean_subs(url)
            print(f"   ✅ Extracted {len(full_text)} characters.")

            # --- STEP B: TRANSFORM (Chunking) ---
            chunk_size = 1000
            chunks = []
            ids = []
            metadatas = []
            
            # Simple unique ID based on URL hash to prevent duplicates
            video_hash = str(abs(hash(url)))
            
            for i in range(0, len(full_text), chunk_size):
                chunk = full_text[i : i + chunk_size]
                chunks.append(chunk)
                ids.append(f"{video_hash}_chunk_{i}")
                metadatas.append({"source": url, "type": "youtube"})
            
            print(f"   🔪 Split into {len(chunks)} knowledge chunks.")

            # --- STEP C: LOAD ---
            print("   🧠 Embedding and saving to ChromaDB...")
            self.collection.add(
                documents=chunks,
                ids=ids,
                metadatas=metadatas
            )
            print("   🎉 Knowledge Saved Successfully!")

        except Exception as e:
            print(f"❌ Error ingesting video: {e}")

if __name__ == "__main__":
    kb = KnowledgeBase()
    # Test with the Prompt Engineering Course
    TEST_URL = "https://www.youtube.com/watch?v=jC4v5AS4RIM" 
    kb.ingest_youtube_video(TEST_URL)