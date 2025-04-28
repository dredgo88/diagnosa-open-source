# Diagnosa Open Source Medis berbasis ChatGPT

Proyek ini bertujuan untuk membantu dokter dan klinik dalam:
- Menyusun daftar differential diagnosis.
- Membuat rencana tatalaksana awal.
- Memberikan edukasi pasien.
- Menyarankan pemeriksaan penunjang.

## 📦 Teknologi yang Digunakan
- FastAPI
- OpenAI ChatGPT API
- FPDF2 untuk membuat PDF
- Jinja2 Templates
- Python 3.9+

## 🚀 Cara Menjalankan
1. Clone repository ini:
```
git clone https://github.com/yourusername/diagnosa-open-source.git
```

2. Masuk ke folder project:
```
cd diagnosa-open-source
```

3. Buat virtual environment dan aktifkan:
```
python3 -m venv env
source env/bin/activate
```

4. Install dependencies:
```
pip install -r requirements.txt
```

5. Siapkan file .env dengan isi:
```
OPENAI_API_KEY=your_openai_api_key
```

6. Jalankan server:
```
uvicorn main:app --reload
```

7. Akses di browser:
```
http://127.0.0.1:8000
```

## 📃 License
MIT License
