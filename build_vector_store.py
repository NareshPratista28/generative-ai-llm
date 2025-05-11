"""
Script untuk membuat vector store dari contoh pertanyaan Java.
"""

import logging
import sys
from app.services.rag.indexer import create_vector_store

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

if __name__ == "__main__":
    print("=== Memulai proses pembuatan vector store ===")
    success = create_vector_store()
    
    if success:
        print("=== Vector store berhasil dibuat! ===")
    else:
        print("=== Gagal membuat vector store! ===")
