import streamlit as st
from langchain_community.llms import Ollama

# Define the function to generate questions
def getLLMResponse(content_id):
    llm = Ollama(
        model="llama3.1:8b",  
        base_url="http://localhost:11434",  
        temperature=0.9
    )

    templates = {
        "Tipe Data, Variabel, dan Operator": """Berikut adalah beberapa contoh format soal untuk referensi:
*Studi Kasus:*
**Lengkapilah kode program berdasarkan perintah berikut :**
* Tambahkan tipe data untuk variabel panjang, lebar, tinggi, Vbalok dan Lbalok berdasarkan nilai yang ada.
* Tambahkan rumus volume balok “panjang * lebar * tinggi” pada variabel Vbalok
* Tambahkan rumus volume balok “2*(panjang * lebar + panjang * tinggi + lebar * tinggi)” pada variabel Lbalok

```java
public class TipeData {
      public static void main(String args[]) {
             … panjang, lebar, tinggi, vBalok, lBalok;
             
             panjang = 10;
             lebar = 6;
             tinggi = 7;
             
             // volume balok
             vBalok = ……;
             
             // Luas permukaan balok
             lBalok = …..;
             
             System.out.print("Volume balok = "+ vBalok + ", ");
             System.out.print("Luas permukaan balok = "+ lBalok);
             
      }
}
```

*Studi Kasus:*
**Lengkapilah kode program berdasarkan perintah berikut :**
* Tambahkan tipe data yang sesuai untuk variabel alas, tinggiSegitiga, sisiA, sisiB, sisiC, luasSegitiga, dan kelilingSegitiga berdasarkan nilai yang ada.
* Tambahkan rumus luas segitiga 0.5 * alas * tinggiSegitiga pada variabel luasSegitiga.
* Tambahkan rumus keliling segitiga sisiA + sisiB + sisiC pada variabel kelilingSegitiga.

```java
public class TipeDataSegitiga {
      public static void main(String args[]) {
             … alas, tinggiSegitiga, sisiA, sisiB, sisiC, luasSegitiga, kelilingSegitiga;
             
             alas = 8;
             tinggiSegitiga = 5;
             sisiA = 8;
             sisiB = 6;
             sisiC = 10;
             
             // luas segitiga
             luasSegitiga = ……;
             
             // keliling segitiga
             kelilingSegitiga = …..;
             
             System.out.print("Luas Segitiga = "+ luasSegitiga + ", ");
             System.out.print("Keliling Segitiga = "+ kelilingSegitiga);
      }
}
```

*Studi Kasus:*
**Lengkapilah kode program berdasarkan perintah berikut :**
* Tambahkan tipe data yang sesuai untuk variabel jariJari, phi, luasLingkaran, dan kelilingLingkaran berdasarkan nilai yang ada.
* Gunakan nilai phi = 3.14.
* Tambahkan rumus luas lingkaran phi * jariJari * jariJari pada variabel luasLingkaran.
* Tambahkan rumus keliling lingkaran 2 * phi * jariJari pada variabel kelilingLingkaran.

```java
public class TipeDataLingkaran {
      public static void main(String args[]) {
             … jariJari, phi, luasLingkaran, kelilingLingkaran;
             
             phi = 3.14;
             jariJari = 7;
             
             // luas lingkaran
             luasLingkaran = ……;
             
             // keliling lingkaran
             kelilingLingkaran = …..;
             
             System.out.print("Luas Lingkaran = "+ luasLingkaran + ", ");
             System.out.print("Keliling Lingkaran = "+ kelilingLingkaran);
      }
}
```
 
Buatlah satu soal baru dengan format yang sama tentang penggunaan tipe data dalam Java. Soal harus berbeda dari contoh-contoh di atas.
""",
        "Sintaks Pemilihan If-Else": """Berikut adalah beberapa contoh format soal untuk referensi:

**Contoh 1:**
**Buatlah program dengan menggunakan pemilihan if-else untuk menentukan grade nilai dengan ketentuan berikut:**
* Nilai >= 90: Grade A
* Nilai >= 80: Grade B
* Nilai >= 70: Grade C
* Nilai >= 60: Grade D
* Nilai < 60: Grade F

```java
public class GradeCalculator {
    public static void main(String[] args) {
        int nilai = 85;
        String grade;
        
        // Tentukan grade berdasarkan nilai
        if (/* isi kondisi disini */) {
            // isi disini
        } else if (/* isi kondisi disini */) {
            // isi disini
        }
        // Lanjutkan kondisi lainnya
        
        System.out.println("Grade: " + grade);
    }
}
```

**Contoh 2:**
**Buatlah program dengan menggunakan pemilihan if-else untuk menentukan kategori BMI dengan ketentuan berikut:**
* BMI < 18.5: Underweight
* BMI >= 18.5 dan < 25: Normal
* BMI >= 25 dan < 30: Overweight
* BMI >= 30: Obese

```java
public class BMICalculator {
    public static void main(String[] args) {
        double bmi = 22.5;
        String category;
        
        // Tentukan kategori berdasarkan BMI
        if (/* isi kondisi disini */) {
            // isi disini
        } else if (/* isi kondisi disini */) {
            // isi disini
        }
        // Lanjutkan kondisi lainnya
        
        System.out.println("BMI Category: " + category);
    }
}
```

**Contoh 3:**
**Buatlah program dengan menggunakan pemilihan if-else untuk menentukan diskon belanja dengan ketentuan berikut:**
* Total belanja > 1000000: Diskon 15%
* Total belanja > 500000: Diskon 10%
* Total belanja > 200000: Diskon 5%
* Total belanja <= 200000: Tidak ada diskon

```java
public class DiscountCalculator {
    public static void main(String[] args) {
        double totalBelanja = 750000;
        double diskon;
        
        // Hitung diskon berdasarkan total belanja
        if (/* isi kondisi disini */) {
            // isi disini
        } else if (/* isi kondisi disini */) {
            // isi disini
        }
        // Lanjutkan kondisi lainnya
        
        System.out.println("Diskon: " + diskon + "%");
    }
}
```

Buatlah satu soal baru dengan format yang sama tentang penggunaan if-else dalam Java. Soal harus berbeda dari contoh-contoh di atas.
""",
        "Sintaks Pemilihan IF-ELSE IF-ELSE": """Berikut adalah beberapa contoh format soal untuk referensi:

**Contoh 1:**
**Buatlah program dengan menggunakan pemilihan switch-case untuk menentukan biaya parkir dengan ketentuan berikut:**
* Ketika jenis kendaraan "Motor", biaya = 2000
* Ketika jenis kendaraan "Mobil", biaya = 5000
* Ketika jenis kendaraan "Bus", biaya = 10000
* Nilai default 0

```java
public class ParkingFee {
    public static void main(String[] args) {
        String jenisKendaraan = "Mobil";
        int biaya;
        
        switch (jenisKendaraan) {
            case "Motor":
                // isi disini
                break;
            case "Mobil":
                // isi disini
                break;
            case "Bus":
                // isi disini
                break;
            default:
                // isi disini
        }
        
        System.out.println("Biaya parkir: " + biaya);
    }
}
```

**Contoh 2:**
**Buatlah program dengan menggunakan pemilihan switch-case untuk menentukan jumlah hari dalam bulan dengan ketentuan berikut:**
* Bulan 1,3,5,7,8,10,12 memiliki 31 hari
* Bulan 4,6,9,11 memiliki 30 hari
* Bulan 2 memiliki 28 hari
* Nilai default 0

```java
public class DaysInMonth {
    public static void main(String[] args) {
        int bulan = 3;
        int jumlahHari;
        
        switch (bulan) {
            case 1: case 3: case 5: case 7: case 8: case 10: case 12:
                // isi disini
                break;
            case 4: case 6: case 9: case 11:
                // isi disini
                break;
            case 2:
                // isi disini
                break;
            default:
                // isi disini
        }
        
        System.out.println("Jumlah hari: " + jumlahHari);
    }
}
```

**Contoh 3:**
**Buatlah program dengan menggunakan pemilihan switch-case untuk konversi nilai huruf ke bobot dengan ketentuan berikut:**
* Nilai A = 4.0
* Nilai B = 3.0
* Nilai C = 2.0
* Nilai D = 1.0
* Nilai E = 0.0
* Nilai default -1.0

```java
public class GradeConverter {
    public static void main(String[] args) {
        char nilaiHuruf = 'B';
        double bobot;
        
        switch (nilaiHuruf) {
            case 'A':
                // isi disini
                break;
            case 'B':
                // isi disini
                break;
            // Lanjutkan case lainnya
            default:
                // isi disini
        }
        
        System.out.println("Bobot nilai: " + bobot);
    }
}
```

Buatlah satu soal baru dengan format yang sama tentang penggunaan switch-case dalam Java. Soal harus berbeda dari contoh-contoh di atas.
""",
        "if_else": """Berikut adalah beberapa contoh format soal untuk referensi:

**Contoh 1:**
**Buatlah program dengan menggunakan pemilihan if-else untuk menentukan grade nilai dengan ketentuan berikut:**
* Nilai >= 90: Grade A
* Nilai >= 80: Grade B
* Nilai >= 70: Grade C
* Nilai >= 60: Grade D
* Nilai < 60: Grade F

```java
public class GradeCalculator {
    public static void main(String[] args) {
        int nilai = 85;
        String grade;
        
        // Tentukan grade berdasarkan nilai
        if (/* isi kondisi disini */) {
            // isi disini
        } else if (/* isi kondisi disini */) {
            // isi disini
        }
        // Lanjutkan kondisi lainnya
        
        System.out.println("Grade: " + grade);
    }
}
```
Buatlah satu soal baru dengan format yang sama tentang penggunaan switch-case dalam Java. Soal harus berbeda dari contoh-contoh di atas.
""",
    }

    # Generate the question directly using the template
    response = llm.invoke(templates[content_id])
    return response

# UI Starts here
st.set_page_config(
    page_title="Java Problem Generator",
    page_icon='☕',
    layout='centered',
    initial_sidebar_state='collapsed'
)
st.header("Generator Soal Java")
st.subheader("made by resh")

# Dropdown to select topic
content_id = st.selectbox(
    'Pilih topik pembelajaran:',
    ('Tipe Data, Variable,  ', 'if_else', 'switch_case'), 
    key=1
)

# Button to generate question
submit = st.button("Generate Soal")
if submit:
    with st.spinner('Generating soal...'):
        response = getLLMResponse(content_id)
        st.markdown(response)