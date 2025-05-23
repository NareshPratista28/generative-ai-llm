import os
import re
import json
import random
import time
import logging
import requests
from dotenv import load_dotenv
from typing import Dict, Tuple, Any, Optional
from langchain_community.llms import Ollama
from app.models.lesson import LessonModel
from app.services.rag.rag_service import RAGService
from app.models.generation_history import GenerationHistory

load_dotenv()

class LLMService:
    """Service untuk menghasilkan pertanyaan latihan Java melalui Ollama LLM."""
    
    def __init__(self, 
                 model_name: str = None, 
                 base_url: str = None):
        """
        Inisialisasi LLMService.
        
        Args:
            model_name: Nama model Ollama yang digunakan
            base_url: URL endpoint Ollama
        """
        self.lesson_model = LessonModel()
        # Load configuration from environment variables if not provided
        self.model_name = model_name or os.getenv("LLM_MODEL_NAME")
        self.base_url = base_url or os.getenv("LLM_BASE_URL")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.8"))
        
        # Setup logging based on environment configuration
        log_level = os.getenv("LOG_LEVEL", "INFO")
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"LLMService initialized with model: {self.model_name}, base_url: {self.base_url}")

        self.rag_service = RAGService()
        self.history_model = GenerationHistory()
        self.successful_examples = []
    
    def get_llm_instance(self) -> Ollama:
        """
        Membuat dan mengembalikan instance LLM dengan konfigurasi yang tepat.
        
        Returns:
            Instance Ollama yang telah dikonfigurasi
        """
        return Ollama(
            model=self.model_name,
            base_url=self.base_url,
            temperature=0.7,
            top_p=0.85,
        )
    
    def _get_relevant_rag_examples(self, topic: str, content: str) -> str:
        """
        Mendapatkan contoh relevan dari RAG untuk disertakan dalam prompt.
        
        Args:
            topic: Topik pemrograman Java
            scenario: Skenario konteks aplikasi
        
        Returns:
            String berisi contoh-contoh relevan dalam format yang siap dimasukkan ke prompt
        """
        if not self.rag_service:
            self.logger.warning("RAG Service tidak tersedia, tidak bisa mendapatkan contoh relevan")
            return ""
        
        try:
            self.logger.info(f"Mencari contoh RAG yang relevan untuk topik '{topic}'dengan koteks tambahan")

            # Ekstrak konsep penting dari content jika tersedia
            context = ""
            if content and len(content) > 0:
                # Ambil beberapa kalimat pertama dari materi
                context = content.split(".")[0:3]
                context = ". ".join(context)
                self.logger.debug(f"Konteks tambahan: {context[:50]}...")


            examples = self.rag_service.get_relevant_examples(topic, context, n=2)

            if not examples:
                self.logger.info(f"Tidak ditemukan contoh RAG yang relevan untuk kombinasi topik dan skenario")
                return ""
            
            # Format contoh untuk prompt
            examples_text = "\n\nCONTOH SOAL LAINNYA YANG RELEVAN:\n"
            
            for i, example in enumerate(examples, 1):
                self.logger.debug(f"Contoh RAG #{i}: {example['studi_kasus'][:50]}...")
                examples_text += f"\nContoh {i}:\n"
                examples_text += f"**Studi Kasus:**\n{example['studi_kasus']}\n\n"
                examples_text += f"**Tugas:**\n{example['tugas']}\n\n"
                examples_text += f"```java\n{example['code']}\n```\n"
            
            self.logger.info(f"Berhasil mendapatkan {len(examples)} contoh RAG yang relevan")
            return examples_text
            
        except Exception as e:
            self.logger.error(f"Error saat mendapatkan contoh RAG: {str(e)}", exc_info=True)
            return ""
        

    # After generating a good response
    def _store_successful_example(self, result: Dict[str, str]):
        """Store successful examples to guide future generations."""
        if len(self.successful_examples) >= 5:
            self.successful_examples.pop(0)  # Remove oldest
        
        self.successful_examples.append({
            "studi_kasus": result["studi_kasus"],
            "tugas": result["tugas"],
            "code": result["code"]
        })
    
    def create_prompt(self, prompt_llm: str, content_text: str = "", task_type: str = None) -> str:
        """
        Menyusun prompt lengkap untuk LLM dengan menambahkan instruksi dan skenario acak.
        
        Args:
            prompt_llm: Prompt dasar dari model pelajaran
            content_text: Teks materi pembelajaran
            task_type: Judul materi/topik dari database
            
        Returns:
            Prompt yang lengkap untuk dikirim ke LLM
        """
        
        closing_variations = [
            "Pastikan kode belum berisi jawaban dan perlu dilengkapi oleh pengguna",
            "Kode template harus memiliki bagian yang perlu dilengkapi dengan tanda '...'",
            "Biarkan bagian kode yang harus dilengkapi kosong dengan tanda '...'",
            "Jangan berikan jawaban lengkap, beri tanda '...' untuk bagian yang harus diisi"
        ]
        
        closing = random.choice(closing_variations)
        timestamp = time.time()
        
        # Tambahkan materi pembelajaran jika tersedia
        max_content_length = 6000
        content_truncated = content_text
        if content_text and len(content_text) > max_content_length:
            content_truncated = content_text[:max_content_length] + "... [materi dipotong]"
            self.logger.info(f"Materi dipotong dari {len(content_text)} menjadi {max_content_length} karakter")

        # Ekstrak preview konten untuk RAG
        content = ""
        if content_text and len(content_text) > 0:
            # Ambil 200 karakter pertama untuk preview
            content = content_text[:200]
        
        # Ambil contoh RAG yang relevan dengan topik DAN preview konten
        rag_examples = self._get_relevant_rag_examples(task_type, content)
        
        content_section = ""
        if content_truncated and len(content_truncated.strip()) > 0:
            content_section = f"""
            MATERI PEMBELAJARAN (WAJIB DIJADIKAN REFERENSI SOAL):
            {content_truncated.strip()}
            
            """
        
        return f"""
        {prompt_llm}
        Topic: {task_type}
        Timestamp: {timestamp} 

        {content_section}

        You are an expert Java programming instructor with experience in creating programming exercises. Create a new and original Java exercise appropriate for beginner students by following these guidelines. ALL RESPONSES MUST BE IN INDONESIAN language.

        THE EXERCISE MUST BE DIRECTLY BASED ON THE LEARNING MATERIAL PROVIDED ABOVE.

        IMPORTANT! Make sure your exercise includes a clear case study and tasks. Your response format MUST EXACTLY follow this example without any additional text:

        **Studi Kasus:**
        [Deskripsi singkat konteks masalah dalam 2-3 kalimat bahasa Indonesia]

        **Tugas:**
        - [Tugas pertama yang harus dilengkapi]
        - [Tugas kedua yang harus dilengkapi]
        - [Tugas ketiga yang harus dilengkapi (jika ada)]

        ```java
        // Kode dengan bagian yang harus dilengkapi ditandai dengan komentar dan ... atau // Tulis kode di sini
        // {closing}
        ```

        MANDATORY RULES:
        1. Case Study: Provide a short and clear description in Indonesian, maximum 3 sentences.
        2. Tasks: Provide 2-4 specific tasks in bullet points format (starting with "-") in Indonesian.
        3. Code template: Provide incomplete Java code with "..." for parts that need to be filled.
        4. ALL TEXT MUST BE IN INDONESIAN, including comments in the code.
        5. DO NOT provide answers, solutions, or complete code in the template.
        6. Do not add text or explanations outside the specified format.
        7. Ensure the Java code is syntactically valid if filled correctly.

        CHARACTERISTICS OF GOOD EXERCISES:
        - Tasks must be clear and specific (example: "Add variable X declaration with the appropriate data type")
        - Code template provides a basic structure but has parts that need to be completed
        - Parts that need to be completed are marked with "..." or "// Write code here"
        - Exercise has appropriate difficulty level for beginner students
        - The problem is simple but has educational value
        - Code includes helpful comments

        SPECIFIC TASK EXAMPLES:
        - Deklarasikan variabel panjang, lebar, dan tinggi dengan tipe data yang sesuai
        - Implementasikan rumus volume balok "panjang * lebar * tinggi" pada baris yang ditandai
        - Tambahkan struktur kondisional if-else untuk memeriksa apakah nilai bilangan positif atau negatif
        - Lengkapi loop for untuk mencetak angka 1 sampai n

        DO NOT ADD ANYTHING OUTSIDE THE SPECIFIED FORMAT. DO NOT INCLUDE "OUTPUT PROGRAM:" OR ADDITIONAL EXPLANATIONS.

        EXAMPLE OF A GOOD EXERCISE:

        **Studi Kasus:**
        Sebuah aplikasi perlu menghitung volume dan luas permukaan tabung. Pengguna akan memasukkan nilai jari-jari dan tinggi tabung.

        **Tugas:**
        - Deklarasikan variabel jariJari, tinggi, volumeTabung, dan luasPermukaanTabung dengan tipe data double
        - Implementasikan rumus volume tabung "Math.PI * jariJari * jariJari * tinggi" pada baris yang ditandai
        - Implementasikan rumus luas permukaan tabung "2 * Math.PI * jariJari * (jariJari + tinggi)" pada baris yang ditandai

        ```java
        public class PerhitungnTabung {{
            public static void main(String args[]) {{
                // Deklarasikan variabel di sini
                ... jariJari, tinggi, volumeTabung, luasPermukaanTabung;
                
                // Inisialisasi nilai
                jariJari = 7.0;
                tinggi = 10.0;
                
                // Hitung volume tabung
                volumeTabung = ...;
                
                // Hitung luas permukaan tabung
                luasPermukaanTabung = ...;
                
                // Cetak hasil
                System.out.println("Volume tabung = " + volumeTabung);
                System.out.println("Luas permukaan tabung = " + luasPermukaanTabung);
            }}
        }}
        ```
        {rag_examples}

        CREATE A NEW EXERCISE DIFFERENT FROM THE EXAMPLE ABOVE. ENSURE YOU FOLLOW THE FORMAT EXACTLY AND DO NOT ADD TEXT OUTSIDE THE FORMAT. REMEMBER: ALL OUTPUT MUST BE IN INDONESIAN LANGUAGE.
        """
    
    def _validate_response(self, result: Dict[str, str]) -> bool:
        """Validates the quality of the generated response."""
        # Check for minimum content length
        if len(result.get("studi_kasus", "")) < 30:
            return False
            
        # Check that code contains expected placeholders
        if "..." not in result.get("code", ""):
            return False
            
        # Check that tasks are in bullet point format
        if not re.search(r"- .+", result.get("tugas", "")):
            return False
            
        return True
    
    def generate_question(self, content_id: int) -> Tuple[Dict[str, Any], float]:
        """
        Menghasilkan pertanyaan latihan Java berdasarkan ID konten.
        
        Args:
            content_id: ID konten pelajaran
            
        Returns:
            Tuple yang berisi hasil respons yang diparsing dan waktu pemrosesan
        """
        try:
            self.logger.info(f"===== MEMULAI PROSES GENERASI PERTANYAAN (ID: {content_id}) =====")

            # Mendapatkan prompt dari model pelajaran
            self.logger.info(f"[LANGKAH 1/5] Mengambil prompt_llm dan konten dari database (content_id: {content_id})")
            result = self.lesson_model.get_prompt_and_description(content_id)
            if not result:
                self.logger.error(f"Prompt dan konten tidak ditemukan untuk content_id: {content_id}")
                raise ValueError(f"Prompt dan konten tidak ditemukan untuk content_id: {content_id}")
            
            prompt_llm = result['prompt_llm']
            content_text = result['description']
            content_title = result['title']

            # Log panjang konten untuk debugging
            self.logger.info(f"Panjang prompt_llm: {len(prompt_llm)} karakter")
            self.logger.info(f"Panjang content_text: {len(content_text)} karakter")
            self.logger.info(f"Judul materi: {content_title}")

            # Ekstrak task_type dari konten daripada memilih secara acak
            self.logger.info(f"[LANGKAH 2/5] Menggunakan judul materi sebagai task_type: '{content_title}'")
           
            self.logger.info(f"[LANGKAH 3/5] Menyusun prompt lengkap dengan RAG examples dan materi pembelajaran")
            full_prompt = self.create_prompt(prompt_llm, content_text, content_title)
            self.logger.info(f"Prompt lengkap berhasil dibuat: {len(full_prompt)} karakter")

            # Mendapatkan instance LLM
            self.logger.info(f"[LANGKAH 4/5] Mengirim prompt ke model LLM {self.model_name}")
            llm = self.get_llm_instance()
            
            # Mengukur waktu pemrosesan
            start_time = time.time()
            response = llm.invoke(full_prompt)
            generation_time = time.time() - start_time
            
            self.logger.info(f"Model berhasil menghasilkan respons dalam {generation_time:.2f} detik")
            self.logger.info(f"Panjang respons: {len(response)} karakter")
            
            # Parsing respons
            self.logger.info(f"[LANGKAH 5/5] Mem-parsing respons model untuk ekstraksi komponen pertanyaan")
            result = self._parse_response(response)

            # Validasi hasil
            if self._validate_response(result):
                self.logger.info("Validasi berhasil: respons memenuhi semua kriteria kualitas")
                # Simpan contoh sukses untuk penggunaan di masa depan
                self._store_successful_example(result)
            else:
                self.logger.warning("Respons tidak memenuhi semua kriteria kualitas, tetapi tetap dikembalikan")
            
            self.logger.info(f"===== GENERASI PERTANYAAN SELESAI (ID: {content_id}) =====")

            # Simpan hasil ke history, sekarang dengan topic_title
            history_id = self.history_model.save_generation(
                content_id=content_id,
                topic_title=content_title,  # Menyimpan judul topik
                result=result,
                generation_time=generation_time
            )
            
            # Mengembalikan tiga nilai: hasil, waktu generasi, dan ID history
            return result, generation_time, history_id
            
        except Exception as e:
            self.logger.error(f"Gagal menghasilkan pertanyaan: {str(e)}", exc_info=True)
            raise
    
    def _parse_response(self, response: str) -> Dict[str, str]:
        """
        Mem-parsing respons LLM untuk mengekstrak kode Java dan respons lengkap.
        
        Args:
            response: Respons lengkap dari LLM
            
        Returns:
            Dictionary berisi respons mentah dan kode yang diekstrak
        """
        self.logger.debug("Memulai parsing respons LLM")

        result = {
            "raw_response": response,
            "code": "",
            "studi_kasus": "",
            "tugas": ""
        }
        
        # Extract the Java code using regex
        code_pattern = r"```java(.*?)```"
        code_matches = re.findall(code_pattern, response, re.DOTALL)
        if code_matches:
            result["code"] = code_matches[0].strip()
        
        # Extract Studi Kasus
        studi_kasus_pattern = r"\*\*Studi Kasus:\*\*(.*?)(?=\*\*Tugas:\*\*|\Z)"
        studi_kasus_matches = re.findall(studi_kasus_pattern, response, re.DOTALL)
        if studi_kasus_matches:
            result["studi_kasus"] = studi_kasus_matches[0].strip()
        
        # Extract Tugas
        tugas_pattern = r"\*\*Tugas:\*\*(.*?)(?=```|$)"
        tugas_matches = re.findall(tugas_pattern, response, re.DOTALL)
        if tugas_matches:
            result["tugas"] = tugas_matches[0].strip()

        # Log hasil ekstraksi
        if all(key in result and result[key] for key in ["code", "studi_kasus", "tugas"]):
            self.logger.info("Semua komponen berhasil diekstrak dari respons")
        else:
            self.logger.warning("Beberapa komponen tidak berhasil diekstrak dari respons")
        
        return result