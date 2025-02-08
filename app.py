import streamlit as st
from langchain_community.llms import Ollama
import random

def generate_system_prompt(difficulty="medium"):
    difficulty_guidelines = {
        "easy": """
Level Mudah - Panduan Pembuatan Soal:
1. Gunakan konsep dasar yang sederhana
2. Berikan petunjuk yang jelas dalam kode
3. Sediakan komentar yang membantu
4. Fokus pada satu konsep dalam satu waktu
5. Gunakan angka bulat dan perhitungan sederhana
6. Berikan contoh output yang jelas
7. Sisakan 1-2 bagian kode untuk dilengkapi siswa
""",
        "medium": """
Level Menengah - Panduan Pembuatan Soal:
1. Kombinasikan 2-3 konsep dalam satu soal
2. Berikan petunjuk yang cukup dalam kode
3. Sediakan komentar untuk bagian penting
4. Gunakan perhitungan yang lebih kompleks
5. Sisakan 2-3 bagian kode untuk dilengkapi siswa
6. Tambahkan validasi input sederhana
7. Gunakan tipe data yang bervariasi
""",
        "hard": """
Level Sulit - Panduan Pembuatan Soal:
1. Integrasikan multiple konsep (3+ konsep)
2. Berikan minimal petunjuk dalam kode
3. Fokus pada logika yang kompleks
4. Sisakan 3-4 bagian kode untuk dilengkapi siswa
5. Masukkan multiple kasus pengecualian
6. Memerlukan validasi input yang ketat
7. Kombinasikan berbagai tipe data
"""
    }

    return f"""Anda adalah seorang instruktur pemrograman Java yang ahli dan berpengalaman dalam membuat soal-soal latihan.
Buatlah SATU soal pemrograman Java yang baru dan original dengan mengikuti pedoman berikut:

{difficulty_guidelines[difficulty]}

PENTING! Format respon Anda HARUS TEPAT seperti contoh berikut:

**Studi Kasus:**
[Deskripsi singkat konteks dunia nyata dalam bahasa Indonesia]

**Tugas:**
[Daftar bullet point yang jelas tentang apa yang harus dilengkapi, dalam bahasa Indonesia]

```java
// Kode dengan bagian yang harus dilengkapi ditandai dengan komentar dan tanda ... atau // Tulis kode di sini
// Pastikan kode belum berisi jawaban!
```

**Output yang Diharapkan:**
[Berikan contoh output yang diharapkan setelah kode diselesaikan dengan benar]

PANDUAN PENTING PEMBUATAN SOAL:
1. Semua teks penjelasan HARUS dalam bahasa Indonesia
2. Gunakan komentar berbahasa Indonesia dalam kode
3. Template kode HARUS memiliki bagian yang perlu dilengkapi (JANGAN berikan kode lengkap)
4. Gunakan tanda '...' atau '// Tulis kode di sini' untuk bagian yang harus dilengkapi
5. Pisahkan dengan jelas antara template kode dan contoh output
6. Berikan petunjuk yang sesuai dengan level kesulitan
7. Pastikan soal original dan berbeda dari template

CONTOH FORMAT PENULISAN TEMPLATE KODE:
```java
public class ContohSoal {{
    public static void main(String[] args) {{
        // Deklarasikan variabel di sini
        ...
        
        // Hitung total dengan rumus yang sesuai
        total = ... // Tulis rumus di sini
        
        System.out.println("Total: " + total);
    }}
}}
```

JANGAN memberikan jawaban langsung dalam template kode!
"""

def getLLMResponse(content_id, difficulty="medium"):
    llm = Ollama(
        model="llama3.1:8b",  
        base_url="http://localhost:11434",  
        temperature=0.8
    )

    topic_guidelines = {
        "Tipe Data, Variabel, dan Operator": {
            "easy": """
Panduan Pembuatan Template Kode:
1. Siapkan struktur kode dasar
2. Sisakan bagian untuk:
   - Deklarasi tipe data
   - Inisialisasi variabel
   - Operasi matematika sederhana
3. Berikan komentar yang jelas untuk setiap bagian yang harus dilengkapi
4. Gunakan placeholder '...' atau '// Tulis kode di sini'
""",
            "medium": """
Panduan Pembuatan Template Kode:
1. Siapkan struktur kode dengan multiple variabel
2. Sisakan bagian untuk:
   - Deklarasi beberapa tipe data
   - Operasi matematika kombinasi
   - Casting tipe data
3. Berikan komentar panduan untuk setiap bagian
""",
            "hard": """
Panduan Pembuatan Template Kode:
1. Siapkan struktur kode kompleks
2. Sisakan bagian untuk:
   - Multiple tipe data dan operasi
   - Konversi tipe data kompleks
   - Perhitungan dengan presisi
3. Berikan komentar minimal
"""
        },
        "Sintaks Pemilihan If-Else": {
            "easy": """
Panduan Pembuatan Template Kode:
1. Siapkan struktur if-else dasar
2. Sisakan bagian untuk:
   - Kondisi if
   - Perintah dalam blok if/else
3. Berikan komentar yang menjelaskan kondisi yang diharapkan
""",
            "medium": """
Panduan Pembuatan Template Kode:
1. Siapkan struktur dengan nested if-else
2. Sisakan bagian untuk:
   - Multiple kondisi
   - Operator logika
   - Blok kode yang sesuai
3. Berikan komentar panduan
""",
            "hard": """
Panduan Pembuatan Template Kode:
1. Siapkan struktur kompleks
2. Sisakan bagian untuk:
   - Kondisi kompleks
   - Multiple operator logika
   - Nested conditions
3. Berikan komentar minimal
"""
        },
        "Sintaks Pemilihan IF-ELSE IF-ELSE": {
            "easy": """
Panduan Pembuatan Template Kode:
1. Siapkan struktur if-else if-else dasar
2. Sisakan bagian untuk:
   - 2-3 kondisi sederhana
   - Perintah dalam setiap blok
3. Berikan komentar jelas untuk setiap kondisi
""",
            "medium": """
Panduan Pembuatan Template Kode:
1. Siapkan struktur dengan multiple conditions
2. Sisakan bagian untuk:
   - 3-4 kondisi dengan operator logika
   - Blok kode yang sesuai
   - Validasi input
3. Berikan komentar panduan
""",
            "hard": """
Panduan Pembuatan Template Kode:
1. Siapkan struktur kompleks
2. Sisakan bagian untuk:
   - 5+ kondisi kompleks
   - Multiple operator logika
   - Validasi kompleks
3. Berikan komentar minimal
"""
        },
        "Sintaks Pemilihan Switch-Case": {
            "easy": """
Panduan Pembuatan Template Kode:
1. Siapkan struktur switch-case dasar
2. Sisakan bagian untuk:
   - 2-3 case sederhana
   - Perintah dalam setiap case
3. Berikan komentar untuk setiap case
""",
            "medium": """
Panduan Pembuatan Template Kode:
1. Siapkan struktur dengan multiple cases
2. Sisakan bagian untuk:
   - 4-5 case dengan logika
   - Fall-through cases
   - Default case
3. Berikan komentar panduan
""",
            "hard": """
Panduan Pembuatan Template Kode:
1. Siapkan struktur kompleks
2. Sisakan bagian untuk:
   - 6+ case kompleks
   - Multiple tipe data
   - Logika kompleks
3. Berikan komentar minimal
"""
        }
    }

    scenario_seeds = [
        "toko online", "sistem akademik", "manajemen inventori", 
        "perbankan", "stasiun cuaca", "skor game", "tracking kesehatan",
        "media sosial", "transportasi", "sistem pemesanan restoran",
        "perpustakaan", "rental kendaraan", "manajemen proyek",
        "sistem parkir", "aplikasi fitness"
    ]
    
    prompt = f"""
{generate_system_prompt(difficulty)}

{topic_guidelines[content_id][difficulty]}

Konteks skenario: {random.choice(scenario_seeds)}

PANDUAN TAMBAHAN PENTING:
1. Pastikan semua teks, pesan, dan komentar dalam bahasa Indonesia
2. Sesuaikan kompleksitas soal dengan level {difficulty}
3. Berikan nama variabel yang bermakna dalam konteks Indonesia
4. JANGAN berikan jawaban dalam template kode
5. Pisahkan dengan jelas antara template kode dan contoh output
6. Berikan petunjuk yang membantu tanpa memberikan jawaban langsung

Format output yang diharapkan HARUS mengikuti contoh di atas dengan tepat!
"""
     
    response = llm.invoke(prompt)
    return response

# UI Components
st.set_page_config(
    page_title="Generator Soal Java",
    page_icon='☕',
    layout='centered',
    initial_sidebar_state='expanded'
)

st.title("Generator Soal Java")
st.markdown("""
Buat soal latihan pemrograman Java yang disesuaikan untuk siswa.
Pilih topik dan tingkat kesulitan untuk membuat soal latihan.
""")

# Sidebar for settings
with st.sidebar:
    st.header("Pengaturan Generator")
    difficulty = st.select_slider(
        "Tingkat Kesulitan",
        options=["easy", "medium", "hard"],
        value="medium",
        help="Pilih tingkat kesulitan soal yang akan dibuat"
    )
    
    st.markdown("""
    **Tingkat Kesulitan:**
    - Easy: Penerapan konsep dasar
    - Medium: Integrasi beberapa konsep
    - Hard: Pemecahan masalah kompleks
    """)

# Main content
content_id = st.selectbox(
    'Pilih Topik Java:',
    ('Tipe Data, Variabel, dan Operator', 
     'Sintaks Pemilihan If-Else', 
     'Sintaks Pemilihan IF-ELSE IF-ELSE', 
     'Sintaks Pemilihan Switch-Case'),
    key="topic_selector"
)

col1, col2 = st.columns([4,1])
with col1:
    generate = st.button("Generate Soal", type="primary")
with col2:
    refresh = st.button("🔄 Versi Baru")

if generate or refresh:
    with st.spinner('Membuat soal...'):
        response = getLLMResponse(content_id, difficulty)
        st.markdown(response)
        
        # Add copy button for code
        code_sections = response.split("```java")
        if len(code_sections) > 1:
            code = code_sections[1].split("```")[0]
            st.code(code, language="java", line_numbers=True)
            st.button("Salin Kode", key="copy_btn", help="Salin kode ke clipboard")

# Footer
st.markdown("---")
st.markdown("*Dibuat dengan ❤️ untuk pembelajar Java*")