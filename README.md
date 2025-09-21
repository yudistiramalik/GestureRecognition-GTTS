# GestureRecognition-GTTS

Sistem Pengenalan Gesture Tangan dengan Output Suara (Text-to-Speech) secara real-time menggunakan  
MediaPipe Hands dan Google Text-to-Speech (gTTS) dengan Python.

---

## ✨ Fitur
- Deteksi gesture tangan secara real-time menggunakan kamera
- Mendukung gesture "Halo", "Perkenalan", "Salam", dan "Terima Kasih"
- Output suara hasil gesture menggunakan gTTS
- Pemutaran suara dengan pygame secara non-blocking (tidak ganggu performa kamera)
- Tampilan garis-garis jari (hand landmarks) pada frame kamera
- Teks gesture terakhir tampil stabil di frame kamera tanpa kedip

---

## 🛠 Teknologi yang Digunakan
- Python 3.10+
- OpenCV untuk pengolahan video dan tampilan grafis
- MediaPipe Hands untuk deteksi landmark tangan
- Google Text-to-Speech (gTTS) untuk konversi teks ke suara
- pygame untuk pemutaran suara
- threading Python untuk menjalankan TTS di background

---

## ⚙️ Instalasi

1. Clone repositori ini
   ```bash
   git clone https://github.com/username/GestureRecognition-GTTS.git
   cd GestureRecognition-GTTS
2. (Opsional) Buat virtual environment
   ```bash
    python -m venv venv
    venv\Scripts\activate   # Windows
    source venv/bin/activate # Linux/Mac
3. Install dependencies
    ```bash
    pip install -r requirements.txt

## Cara Menggunakan
    python gesture_speech.py
Arahkan tangan ke kamera dan lakukan gesture yang tersedia.
Sistem akan mendeteksi dan mengucapkan gesture secara otomatis.

Tekan q untuk keluar dari aplikasi.

## 🤝 Kontribusi
Kontribusi sangat diterima!
Silakan buat pull request atau laporkan isu di repositori ini.


