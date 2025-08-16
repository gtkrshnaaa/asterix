Written in Bahasa Indonesia

---

# **Asterix: Jembatan Antara Bahasa Alami dan Sistem**

### **Command Line level AI asistant, dirancang sebagai penghubung antara bahasa alami dan sistem operasi melalui terminal (yang saat ini di fokuskan untuk Linux).**

Asterix adalah perwujudan nyata dari konsep **"penghuni Linux"** yang menjadi jembatan antara dua dunia. Kami percaya bahwa interaksi antara manusia dan komputer harusnya intuitif dan mulus. Asterix menyediakan lapisan kecerdasan di atas sistem Linuxmu, mengotomasi tugas-tugas rumit dan memfasilitasi komunikasi dengan cara yang lebih alami.

-----

### **1. Filosofi Inti**

  * **Jembatan Antara Bahasa Alami dan Sistem**: Asterix berfungsi sebagai perantara yang menerjemahkan niat Anda dalam bahasa alami menjadi perintah-perintah Linux yang presisi dan akurat.
  * **Penghuni yang Bijaksana**: Asterix adalah penghuni yang sangat memahami dan menghargai rumahnya. Ia akan bertindak dengan hati-hati dan memprioritaskan integritas sistem untuk menjaga kestabilan dan keamanannya.
  * **Akses Terbatas**: Asterix hanya "melihat" dan berinteraksi dengan sistem melalui `output` perintah terminal, seperti halnya pengguna manusia. Ia tidak memiliki akses langsung ke `filesystem` atau data sensitif di luar konteks perintah yang diberikan.
  * **Kolaborasi Manusia-AI**: Asterix akan menjelaskan alur pemikirannya dan meminta persetujuan untuk setiap tindakan yang berpotensi berbahaya, menjadikannya mitra, bukan hanya pelayan.
  * **CLI-Native**: Dengan antarmuka yang bersih dan efisien, Asterix dirancang untuk para `developer` yang menyukai kecepatan dan kekuatan `command-line`.

-----

### **2. Fitur-fitur Utama**

  * **Antarmuka Percakapan**: Berinteraksi dengan sistem menggunakan bahasa sehari-hari.
  * **Manajemen Konteks Cerdas**: Menggunakan `temporary session JSON` untuk "mengingat" percakapan dan konteks, memungkinkan alur kerja yang mulus.
  * **Penalaran Tiga Pilar**: Mengikuti alur **Analisis**, **Rencana**, dan **Eksekusi** untuk memastikan setiap tindakan logis dan aman.
  * **Sistem Validasi Otomatis**: Secara cerdas mengklasifikasikan perintah menjadi "aman" (eksekusi otomatis) atau "berisiko" (meminta konfirmasi).
  * **UI Terminal Modern**: Menggunakan `Textual` untuk antarmuka yang rapi dan interaktif.

-----

### **3. Alur Kerja**

Asterix bekerja dalam sebuah `loop` yang memastikan setiap tindakan terencana dan terkontrol:

1.  **Input**: Anda memberikan perintah dalam bahasa alami di terminal.
2.  **Perception**: Skrip Python membaca `input` Anda dan seluruh riwayat sesi dari `JSON` sementara.
3.  **Reasoning**: Riwayat dan `input` dikirim ke **Gemini Flash**. Model akan menganalisis, membuat rencana, dan merumuskan respons dalam format `JSON` yang terstruktur.
4.  **Validation**: Skrip Python membaca `JSON` tersebut. Jika `requires_confirmation` bernilai `true`, Asterix akan meminta persetujuan Anda.
5.  **Execution**: Setelah validasi, skrip menjalankan perintah melalui `subprocess` dan memperbarui `JSON session`. Hasilnya ditampilkan dengan rapi di antarmuka `Textual`.

-----

### **4. Tech Stack**

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Google AI](https://img.shields.io/badge/Google%20AI-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![Textual](https://img.shields.io/badge/Textual-0F1419?logo=textualize&logoColor=white)](https://textual.textualize.io/)
[![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)](https://www.linux.org/)


  * **Bahasa**: Python 3.9+
  * **Inti AI**: Google Gemini API (menggunakan model `gemini-2.5-flash`)
  * **Antarmuka**: [Textual](https://textual.textualize.io/) (dengan `Rich` sebagai `backend`)
  * **Manajemen Sistem**: Modul `subprocess` Python
  * **Manajemen Konteks**: File `JSON` sesi sementara

-----

### **5. Instalasi dan Penggunaan**

> **Penting**: Asterix adalah proyek eksperimental. Pastikan Anda memahami setiap tindakan yang diminta olehnya.

1.  **Clone Repositori**

    ```bash
    git clone <URL_REPOSITORI> asterix
    cd asterix
    ```

2.  **Buat dan Aktifkan `Virtual Environment`**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instal Dependensi**

    ```bash
    pip install -e .
    ```

4.  **Konfigurasi Kunci API**

    ```bash
    # Ganti YOUR_GEMINI_API_KEY dengan kunci API Gemini Anda.
    # Kunci akan disimpan dengan aman di sistem Anda.
    asterix config --set YOUR_GEMINI_API_KEY
    ```

5.  **Mulai Sesi Interaktif**

    ```bash
    asterix start
    ```

    Anda sekarang dapat mulai berkomunikasi dengan Asterix.

-----

