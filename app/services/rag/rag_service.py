# Service untuk Retrieval-Augmented Generation (RAG) pada sistem pertanyaan Java.

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List, Dict, Any
import logging, os

class RAGService:
    """Inisialisasi RAG Service."""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None
        self._load_vector_store()
    
    def _load_vector_store(self):
        """Load vector store dari file lokal."""
        try:
            # Dapatkan path absolut ke direktori root project
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            vector_store_path = os.path.join(base_dir, "vector_store", "java_examples")
            
            # Periksa apakah vector store sudah ada
            if os.path.exists(vector_store_path):
                self.vector_store = FAISS.load_local(
                    vector_store_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                self.logger.info("Vector store berhasil dimuat")
            else:
                self.logger.warning(f"Vector store tidak ditemukan di {vector_store_path}")
                self.vector_store = None
        except Exception as e:
            self.logger.error(f"Gagal memuat vector store: {str(e)}")
            self.vector_store = None
    
    def get_relevant_examples(self, topic: str, n: int = 2) -> List[Dict[str, Any]]:
        """
        Mendapatkan contoh soal yang relevan dengan topik.
        
        Args:
            topic: Topik Java yang ingin dicari contohnya
            n: Jumlah contoh yang ingin diambil
            
        Returns:
            List contoh soal yang relevan
        """
        if not self.vector_store:
            self.logger.warning("Vector store tidak tersedia, tidak bisa mendapatkan contoh relevan")
            return []
            
        try:
            # Cari dokumen yang relevan dengan topik
            docs = self.vector_store.similarity_search(topic, k=n)
            
            # Extract metadata dan siapkan contoh untuk dikembalikan
            examples = []
            for doc in docs:
                example = {
                    "studi_kasus": doc.metadata.get("studi_kasus", ""),
                    "tugas": doc.metadata.get("tugas", ""),
                    "code": doc.metadata.get("code", "")
                }
                examples.append(example)
                
            self.logger.info(f"Berhasil mengambil {len(examples)} contoh relevan untuk '{topic}'")
            return examples
            
        except Exception as e:
            self.logger.error(f"Error saat mencari contoh relevan: {str(e)}")
            return []
