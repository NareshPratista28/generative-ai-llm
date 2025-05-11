import re
import json
import random
import time
import logging
import requests
from typing import Dict, Tuple, Any, Optional
from langchain_community.llms import Ollama
from app.models.lesson import LessonModel
from app.services.rag.rag_service import RAGService

class LLMService:
    """Service untuk menghasilkan pertanyaan latihan Java melalui Ollama LLM."""
    
    def __init__(self, model_name: str = "gemma3:12b", base_url: str = "http://labai.polinema.ac.id:114",):
        """
        Inisialisasi LLMService.
        
        Args:
            model_name: Nama model Ollama yang digunakan
            base_url: URL endpoint Ollama
        """
        self.lesson_model = LessonModel()
        self.model_name = model_name
        self.base_url = base_url
        self.temperature = 0.8
        self. logger = logging.getLogger(__name__)
        self.rag_service = RAGService()
        
        # Memindahkan scenario seeds ke konstanta kelas
        self.SCENARIO_SEEDS = [
            "sistem akademik sekolah", "manajemen perpustakaan", 
            "aplikasi kalkulator geometri", "sistem informasi mahasiswa",
            "aplikasi konversi satuan", "aplikasi manajemen tugas",
            "perhitungan statistika", "simulasi perbankan", 
            "aplikasi keuangan sederhana", "pengolahan data array"
        ]
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, 
                           format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    
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
    
    def _get_relevant_rag_examples(self, topic: str, scenario: str) -> str:
        """
        Mendapatkan contoh relevan dari RAG untuk disertakan dalam prompt.
        
        Args:
            topic: Topik pemrograman Java
        
        Returns:
            String berisi contoh-contoh relevan dalam format yang siap dimasukkan ke prompt
        """
        if not self.rag_service:
            self.logger.warning("RAG Service tidak tersedia, tidak bisa mendapatkan contoh relevan")
            return ""
        
        try:
                # Improve example relevance by combining the topic with the scenario
            combined_query = f"{topic} for {scenario} application"
            examples = self.rag_service.get_relevant_examples(combined_query, n=2)
            
            if not examples:
                self.logger.info(f"Tidak ditemukan contoh RAG yang relevan untuk topik: {topic}")
                return ""
            
            # Format contoh untuk prompt
            examples_text = "\n\nCONTOH SOAL LAINNYA YANG RELEVAN:\n"
            
            for i, example in enumerate(examples, 1):
                examples_text += f"\nContoh {i}:\n"
                examples_text += f"**Studi Kasus:**\n{example['studi_kasus']}\n\n"
                examples_text += f"**Tugas:**\n{example['tugas']}\n\n"
                examples_text += f"```java\n{example['code']}\n```\n"
            
            self.logger.info(f"Berhasil mendapatkan {len(examples)} contoh RAG untuk topik: {topic}")
            return examples_text
            
        except Exception as e:
            self.logger.error(f"Error saat mendapatkan contoh RAG: {str(e)}")
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
    
    def create_prompt(self, prompt_llm: str) -> str:
        """
        Menyusun prompt lengkap untuk LLM dengan menambahkan instruksi dan skenario acak.
        
        Args:
            prompt_llm: Prompt dasar dari model pelajaran
            
        Returns:
            Prompt yang lengkap untuk dikirim ke LLM
        """
        scenario = random.choice(self.SCENARIO_SEEDS)
        
        closing_variations = [
            "Pastikan kode belum berisi jawaban dan perlu dilengkapi oleh pengguna",
            "Kode template harus memiliki bagian yang perlu dilengkapi dengan tanda '...'",
            "Biarkan bagian kode yang harus dilengkapi kosong dengan tanda '...'",
            "Jangan berikan jawaban lengkap, beri tanda '...' untuk bagian yang harus diisi"
        ]
        
        task_types = [
            "implementasi rumus matematika",
            "pengolahan string",
            "perhitungan geometri",
            "manipulasi array",
            "penggunaan kondisional",
            "implementasi loop"
        ]
        
        task_type = random.choice(task_types)
        closing = random.choice(closing_variations)
        timestamp = time.time()

        rag_examples = self._get_relevant_rag_examples(task_type, scenario)
        if rag_examples:
            prompt_llm += rag_examples
        
        return f"""
        {prompt_llm}
        Context scenario: {scenario}
        Tast type: {task_type}
        Timestamp: {timestamp} 

        You are an expert Java programming instructor with experience in creating programming exercises. Create a new and original Java exercise appropriate for beginner students by following these guidelines. ALL RESPONSES MUST BE IN INDONESIAN language.

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
    
        return prompt
    
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
            # Mendapatkan prompt dari model pelajaran
            prompt_llm = self.lesson_model.get_prompt(content_id)
            if not prompt_llm:
                self.logger.error(f"Prompt tidak ditemukan untuk content_id: {content_id}")
                raise ValueError(f"Prompt tidak ditemukan untuk content_id: {content_id}")
            
            # Membuat prompt lengkap
            full_prompt = self.create_prompt(prompt_llm)
            
            # Mendapatkan instance LLM
            llm = self.get_llm_instance()
            
            # Mengukur waktu pemrosesan
            self.logger.info(f"Memulai pembuatan pertanyaan untuk content_id: {content_id}")
            start_time = time.time()
            response = llm.invoke(full_prompt)
            generation_time = time.time() - start_time
            
            self.logger.info(f"Pertanyaan berhasil dibuat dalam {generation_time:.2f} detik")
            
            # Parsing respons
            result = self._parse_response(response)
            return result, generation_time
            
        except Exception as e:
            self.logger.error(f"Gagal menghasilkan pertanyaan: {str(e)}")
            raise
    
    def _parse_response(self, response: str) -> Dict[str, str]:
        """
        Mem-parsing respons LLM untuk mengekstrak kode Java dan respons lengkap.
        
        Args:
            response: Respons lengkap dari LLM
            
        Returns:
            Dictionary berisi respons mentah dan kode yang diekstrak
        """
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
        
        return result