JAVA_EXAMPLES = [
    {
        "topic": "Tipe Data, Variabel dan Operator",
        "studi_kasus": "Sebuah program perhitungan sederhana untuk menghitung luas persegi panjang.",
        "tugas": "- Deklarasikan variabel panjang, lebar, dan luas dengan tipe data yang sesuai\n- Implementasikan rumus luas persegi panjang: panjang * lebar\n- Tampilkan hasil perhitungan",
        "code": """
public class LuasPersegiPanjang {
    public static void main(String[] args) {
        // Deklarasikan variabel dengan tipe data yang sesuai
        int panjang = 7;
        int lebar = 5;
        int ...;
        
        // Hitung luas persegi panjang
        luas = ... * ...;
        
        // Tampilkan hasil
        System.out.println("Persegi panjang dengan:");
        System.out.println("Panjang: " + panjang);
        System.out.println("Lebar: " + lebar);
        System.out.println("Memiliki luas: " + luas);
    }
}"""
    },
    {
        "topic": "Sintaks Pemilihan IF-ELSE",
        "studi_kasus": "Program untuk menentukan apakah sebuah bilangan genap atau ganjil.",
        "tugas": "- Deklarasikan variabel angka dan hasilCek\n- Implementasikan struktur if-else untuk menentukan bilangan genap atau ganjil\n- Gunakan operator modulo (%) untuk memeriksa apakah angka habis dibagi 2",
        "code": """
public class CekGenapGanjil {
    public static void main(String[] args) {
        int angka = 7;
        String hasilCek;
        
        // Implementasikan struktur if-else
        if (...) {
            hasilCek = "Genap";
        } else {
            hasilCek = "Ganjil";
        }
        
        System.out.println("Angka " + angka + " adalah bilangan " + hasilCek);
    }
}"""
    },
    {
        "topic": "Sintaks Pemilihan IF-ELSE IF-ELSE",
        "studi_kasus": "Program untuk menentukan kategori usia seseorang.",
        "tugas": "- Deklarasikan variabel usia dan kategori\n- Implementasikan struktur if-else if-else untuk menentukan kategori\n- Kategorikan sebagai: Anak-anak (0-12), Remaja (13-17), Dewasa (18-59), Lansia (60+)",
        "code": """
public class KategoriUsia {
    public static void main(String[] args) {
        int usia = 25;
        String kategori;
        
        // Implementasikan struktur if-else if-else
        if (...) {
            kategori = "Anak-anak";
        } else if (...) {
            kategori = "Remaja";
        } else if (...) {
            kategori = "Dewasa";
        } else {
            kategori = "Lansia";
        }
        
        System.out.println("Usia " + usia + " tahun termasuk kategori: " + kategori);
    }
}"""
    },
    {
        "topic": "Sintaks Pemilihan switch-case",
        "studi_kasus": "Program untuk menampilkan nama hari berdasarkan nomor hari.",
        "tugas": "- Deklarasikan variabel nomorHari dan namaHari\n- Implementasikan struktur switch-case untuk menentukan nama hari\n- Buat case untuk nomor 1-7 dan default untuk nomor yang tidak valid",
        "code": """
public class NamaHari {
    public static void main(String[] args) {
        int nomorHari = 3;
        String namaHari;
        
        // Implementasikan switch-case
        switch(nomorHari) {
            case 1:
                namaHari = "Senin";
                ...;
            case 2:
                namaHari = "Selasa";
                break;
            case ...:
                namaHari = "Rabu";
                break;
            case 4:
                namaHari = ...;
                break;
            case 5:
                namaHari = "Jumat";
                break;
            case 6:
                namaHari = "Sabtu";
                break;
            case 7:
                namaHari = "Minggu";
                break;
            default:
                namaHari = "Nomor hari tidak valid";
        }
        
        System.out.println("Hari ke-" + nomorHari + " adalah " + namaHari);
    }
}"""
    },
    {
        "topic": "Perulangan dengan for",
        "studi_kasus": "Program untuk mencetak deret angka dari 1 sampai 10.",
        "tugas": "- Implementasikan perulangan for untuk mencetak angka 1 sampai 10\n- Gunakan variabel i sebagai counter\n- Cetak nilai i pada setiap iterasi",
        "code": """
public class DeretAngka {
    public static void main(String[] args) {
        System.out.println("Deret angka dari 1 sampai 10:");
        
        // Implementasikan perulangan for
        for(...) {
            System.out.print(i + " ");
        }
    }
}"""
    },
    {
        "topic": "Perulangan dengan While",
        "studi_kasus": "Program untuk mencetak deret angka mundur dari 5 sampai 1.",
        "tugas": "- Deklarasikan variabel counter dengan nilai awal 5\n- Implementasikan perulangan while untuk mencetak angka mundur\n- Kurangi nilai counter pada setiap iterasi",
        "code": """
public class DeretMundur {
    public static void main(String[] args) {
        System.out.println("Deret angka mundur dari 5 sampai 1:");
        
        // Inisialisasi counter
        int counter = ...;
        
        // Implementasikan perulangan while
        while(...) {
            System.out.print(counter + " ");
            counter = ...;
        }
    }
}"""
    },
    {
        "topic": "Perulangan dengan Do-While",
        "studi_kasus": "Program untuk mencetak deret angka dari 1 sampai 5.",
        "tugas": "- Deklarasikan variabel counter dengan nilai awal 1\n- Implementasikan perulangan do-while untuk mencetak angka\n- Naikkan nilai counter pada setiap iterasi",
        "code": """
public class DeretDoWhile {
    public static void main(String[] args) {
        System.out.println("Deret angka dari 1 sampai 5:");
        
        // Inisialisasi counter
        int counter = 1;
        
        // Implementasikan perulangan do-while
        do {
            System.out.print(... + " ");
            counter++;
        } while(...);
    }
}"""
    },
    {
        "topic": "Perulangan Bersarang",
        "studi_kasus": "Program untuk mencetak pola segitiga bintang.",
        "tugas": "- Deklarasikan variabel tinggi untuk menentukan tinggi segitiga\n- Implementasikan perulangan bersarang dengan loop luar untuk baris\n- Loop dalam untuk mencetak bintang pada setiap baris",
        "code": """
public class PolaSegitiga {
    public static void main(String[] args) {
        // Tinggi segitiga
        int tinggi = 5;
        
        System.out.println("Pola segitiga bintang:");
        
        // Implementasikan loop luar untuk baris
        for(int i = 1; i <= tinggi; i++) {
            // Implementasikan loop dalam untuk kolom
            for(int j = 1; j <= ...; j++) {
                System.out.print("* ");
            }
            // Pindah ke baris baru
            System.out.println();
        }
    }
}"""
    },
    {
        "topic": "Array Satu Dimensi",
        "studi_kasus": "Program untuk menghitung rata-rata dari sekumpulan nilai.",
        "tugas": "- Deklarasikan array nilai untuk menyimpan beberapa nilai\n- Implementasikan perulangan untuk menjumlahkan semua nilai\n- Hitung rata-rata dengan membagi jumlah dengan banyaknya nilai",
        "code": """
public class RataNilai {
    public static void main(String[] args) {
        // Deklarasikan dan inisialisasi array
        int[] nilai = {75, 80, 90, 70, 85};
        
        // Variabel untuk menyimpan jumlah
        int jumlah = 0;
        
        // Hitung jumlah semua nilai
        for(int i = 0; i < nilai.length; i++) {
            jumlah += ...;
        }
        
        // Hitung rata-rata
        double rataRata = ...;
        
        System.out.println("Nilai: ");
        for(int n : nilai) {
            System.out.print(n + " ");
        }
        System.out.println("\nRata-rata: " + rataRata);
    }
}"""
    },
    {
        "topic": "Array Multidimensi",
        "studi_kasus": "Program untuk mencetak matriks 2x3.",
        "tugas": "- Deklarasikan array 2D matriks dengan ukuran 2x3\n- Isi matriks dengan beberapa nilai\n- Gunakan perulangan bersarang untuk mencetak isi matriks",
        "code": """
public class Matriks {
    public static void main(String[] args) {
        // Deklarasikan matriks 2x3
        int[][] matriks = {
            {1, 2, 3},
            {4, 5, 6}
        };
        
        System.out.println("Matriks 2x3:");
        
        // Cetak matriks
        for(int i = 0; i < matriks.length; i++) {
            for(int j = 0; j < matriks[i].length; j++) {
                System.out.print(matriks[...][...] + " ");
            }
            System.out.println();
        }
    }
}"""
    },
    {
        "topic": "Fungsi Static",
        "studi_kasus": "Program untuk menghitung keliling dan luas persegi.",
        "tugas": "- Implementasikan fungsi static hitungKeliling() untuk menghitung keliling persegi\n- Implementasikan fungsi static hitungLuas() untuk menghitung luas persegi\n- Panggil kedua fungsi dari method main()",
        "code": """
public class Persegi {
    // Fungsi untuk menghitung keliling persegi
    public static int hitungKeliling(int sisi) {
        return ... * ...;
    }
    
    // Fungsi untuk menghitung luas persegi
    public static int hitungLuas(int sisi) {
        return ...;
    }
    
    public static void main(String[] args) {
        int sisi = 5;
        
        // Panggil fungsi hitungKeliling
        int keliling = ...;
        
        // Panggil fungsi hitungLuas
        int luas = ...;
        
        System.out.println("Persegi dengan sisi " + sisi);
        System.out.println("Keliling: " + keliling);
        System.out.println("Luas: " + luas);
    }
}"""
    },
    {
        "topic": "Fungsi Rekursif",
        "studi_kasus": "Program untuk menghitung bilangan Fibonacci.",
        "tugas": "- Implementasikan fungsi rekursif fibonacci() yang menghitung nilai Fibonacci untuk n\n- Tentukan basis rekursi untuk n=0 dan n=1\n- Panggil fungsi untuk beberapa nilai n",
        "code": """
public class Fibonacci {
    // Fungsi rekursif untuk menghitung Fibonacci
    public static int fibonacci(int n) {
        // Basis rekursi
        if(n == 0 || n == 1) {
            return ...;
        }
        
        // Panggilan rekursif
        return ... + ...;
    }
    
    public static void main(String[] args) {
        System.out.println("Deret Fibonacci:");
        
        for(int i = 0; i < 10; i++) {
            System.out.print(fibonacci(i) + " ");
        }
    }
}"""
    }
]