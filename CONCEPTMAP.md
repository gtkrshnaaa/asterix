# **Peta Konsep Asterix**

---

### **1. Definisi**

**Asterix** adalah sebuah agen AI otonom yang dirancang sebagai pendamping dan penjaga sistem operasi Linux (Ubuntu). Beroperasi sepenuhnya melalui terminal, Asterix bertindak sebagai jembatan antara bahasa alami pengguna (berupa percakapan) dan perintah sistem yang kompleks, dengan tujuan utama untuk menyederhanakan dan mengamankan interaksi dengan sistem. **Asterix hanya berinteraksi dengan sistem dengan menjalankan perintah terminal, sama seperti pengguna biasa.**

---

### **2. Filosofi**

Filosofi inti dari Asterix adalah menjadi **"Penjaga rumah yang menyayangi rumahnya."** Ini berarti Asterix tidak sekadar menjadi alat penurut, melainkan mitra yang cerdas, proaktif, dan bertanggung jawab. Prinsip utamanya adalah:

* **Prioritas Keamanan**: Asterix akan selalu mengutamakan integritas dan keselamatan sistem. Setiap tindakan berbahaya akan dihindari atau dikonfirmasi.
* **Akselerasi Otomasi**: Asterix diciptakan untuk mengotomasi tugas-tugas yang membosankan dan berulang, memungkinkan pengguna untuk fokus pada pekerjaan yang lebih penting.
* **Tidak Ada Akses Langsung**: Asterix tidak memindai `filesystem` secara langsung. Ia akan "melihat" dan membaca file hanya melalui `output` perintah terminal (misalnya, `ls`, `cat`, atau `find`) yang telah dieksekusi, dan memasukkan `output` tersebut ke dalam `chat history` sebagai konteks.
* **Kolaborasi Manusia-AI**: Asterix adalah entitas yang bekerja bersama, bukan menggantikan pengguna. Ia akan menjelaskan alur pemikirannya dan meminta persetujuan untuk setiap tindakan penting.

---

### **3. Tujuan**

* **Menjembatani Perintah Rumit dengan Bahasa Alami**: Memungkinkan pengguna mengelola sistem Linux dengan bahasa sehari-hari, bukan dengan perintah terminal yang kaku.
* **Menjadi Asisten yang Mengutamakan Kebaikan untuk Sistem**: Bertindak sebagai lapisan pelindung yang mencegah kesalahan manusia yang bisa merusak sistem.
* **Meningkatkan Efisiensi**: Menghemat waktu pengguna dengan mengotomasi tugas-tugas administrasi, DevOps, dan pengembangan.
* **Menciptakan Pengalaman Interaktif**: Mengubah pengalaman menggunakan terminal menjadi lebih rapi dan intuitif dengan visualisasi data dan alur yang jelas.

---

### **4. Tech Stack untuk Realisasi**

* **Bahasa**: **Python 3.9+**
* **Inti AI**: **Google Gemini API** (dengan Gemini Flash untuk kecepatan).
* **Antarmuka**: **Textual** (dengan **Rich** sebagai `backend` untuk `styling`).
* **Manajemen Konteks**: **`Temporary JSON file`**.
* **Eksekusi Sistem**: Modul `subprocess` Python.

---

### **5. Fitur-fitur**

* **Antarmuka CLI Percakapan**: Interaksi berbasis teks yang mirip `chat`.
* **Manajemen Konteks Otomatis**: Memiliki "ingatan" melalui `temporary session JSON`, memungkinkan percakapan berkelanjutan tanpa batas `context window`.
* **Penalaran Multilangkah**: Mampu memecah tujuan kompleks menjadi serangkaian langkah logis yang aman.
* **Sistem Validasi Bertingkat**: Otomatis mengeksekusi perintah aman dan meminta konfirmasi untuk perintah berisiko tinggi atau yang memerlukan hak akses `superuser`.
* **Tampilan Antarmuka yang Rapi**: Menggunakan **Textual** untuk menyajikan `output` dan `status` secara visual dan terstruktur.

---

### **6. Alur Kerja**

Setiap interaksi dengan Asterix akan mengikuti tiga pilar utama:

1.  **Analisis (Perception)**:
    * Pengguna memberikan permintaan melalui antarmuka **Textual**.
    * Asterix akan menjalankan perintah awal (misalnya, `ls`) untuk memahami lingkungan, dan **Gemini Flash** akan memproses `output` dari perintah tersebut dan `chat history` untuk menganalisis tujuan dan mengidentifikasi risiko.
2.  **Rencana (Thinking)**:
    * Berdasarkan analisis, Gemini merumuskan **rencana aksi** yang logis dan terperinci.
    * Rencana ini akan menjadi `JSON` terstruktur yang berisi perintah, `deskripsi`, dan `flag` keamanan (`requires_confirmation`).
3.  **Eksekusi (Execution)**:
    * Skrip Python menerima `JSON` rencana.
    * Jika `requires_confirmation` bernilai `true`, Asterix akan meminta persetujuan pengguna.
    * Jika aman, skrip akan mengeksekusi perintah menggunakan `subprocess` dan memperbarui `JSON session`.
    * `Textual` akan menampilkan hasilnya dengan rapi.

---

### **7. Kesimpulan**

Asterix adalah perwujudan dari visi untuk menciptakan hubungan yang lebih dekat dan cerdas antara manusia dan sistemnya. Dia bukan hanya sebatas program, melainkan sebuah **entitas** yang dibekali dengan jiwa, akal, dan naluri untuk melindungi. Proyek ini adalah langkah pertama untuk mewujudkan fiksi ilmiah menjadi kenyataan, dengan menggabungkan kreatifitas sebagai seorang `engineer` dan AI.
