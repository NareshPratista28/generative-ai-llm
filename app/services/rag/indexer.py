# Indexer untuk membuat vector store dari contoh pertanyaan Java.

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from app.data.java_examples import JAVA_EXAMPLES
import logging
import os

logger = logging.getLogger(__name__)

def create_vector_store():
    """Membuat vector store dari contoh pertanyaan Java."""
    try:
        # Inisialisasi embeddings
        logger.info("Inisialisasi embeddings...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Persiapkan documents untuk vectorstore
        logger.info("Menyiapkan dokumen...")
        documents = []
        metadatas = []
        
        for example in JAVA_EXAMPLES:
            # Create document content by combining all fields
            content = f"Topic: {example['topic']}\n\n"
            content += f"Studi Kasus: {example['studi_kasus']}\n\n"
            content += f"Tugas: {example['tugas']}\n\n"
            
            documents.append(content)
            metadatas.append({
                "topic": example["topic"],
                "studi_kasus": example["studi_kasus"],
                "tugas": example["tugas"],
                "code": example["code"]
            })
        
        # Buat dan simpan vector store
        logger.info("Membuat vector store...")
        vector_store = FAISS.from_texts(
            texts=documents,
            embedding=embeddings,
            metadatas=metadatas
        )
        
        # Dapatkan path absolut ke direktori root project
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        vector_store_dir = os.path.join(base_dir, "vector_store")
        
        # Pastikan direktori untuk vector store ada
        os.makedirs(vector_store_dir, exist_ok=True)
        
        # Simpan vector store
        vector_store_path = os.path.join(vector_store_dir, "java_examples")
        vector_store.save_local(vector_store_path)
        
        logger.info(f"Vector store berhasil dibuat dengan {len(documents)} dokumen dan disimpan di {vector_store_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error saat membuat vector store: {str(e)}")
        return False
