from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
import openai
import os
from fpdf import FPDF
from dotenv import load_dotenv

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Load .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Inisialisasi FastAPI
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templating engine
templates = Jinja2Templates(directory="templates")

hasil_terakhir_text = ""  # Variabel global sementara untuk isi hasil

# Form input
@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Proses form
@app.post("/", response_class=HTMLResponse)
async def form_post(
    request: Request,
    nama: str = Form(""),
    usia: int = Form(...),
    jenis_kelamin: str = Form(...),
    keluhan_utama: str = Form(...),
    riwayat_penyakit: str = Form(...),
    pemeriksaan_fisik: str = Form(...),
    gejala_tambahan: str = Form(...)
):
    global hasil_terakhir_text

    prompt = f"""
    Berikut adalah data pasien:
    - Nama: {nama}
    - Usia: {usia} tahun
    - Jenis Kelamin: {jenis_kelamin}
    - Keluhan Utama: {keluhan_utama}
    - Riwayat Penyakit Sebelumnya: {riwayat_penyakit}
    - Pemeriksaan Fisik: {pemeriksaan_fisik}
    - Gejala Tambahan: {gejala_tambahan}

    Berdasarkan data di atas, buatkan:
    1. Differential diagnosis.
    2. Rencana tatalaksana awal.
    3. Edukasi pasien.
    4. Saran pemeriksaan penunjang.
    Formatkan jawaban menggunakan teks biasa, bukan HTML.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Kamu adalah asisten medis profesional."},
            {"role": "user", "content": prompt}
        ]
    )

    hasil = response['choices'][0]['message']['content']

    hasil_terakhir_text = hasil  # simpan untuk PDF

    return templates.TemplateResponse("result.html", {"request": request, "hasil": hasil.replace("\n", "<br>")})

# Download hasil sebagai PDF
@app.get("/download-pdf")
async def download_pdf():
    global hasil_terakhir_text

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Bagi hasil ke beberapa baris untuk PDF
    for line in hasil_terakhir_text.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf.output("hasil_diagnosis.pdf")
    return FileResponse('hasil_diagnosis.pdf', filename="hasil_diagnosis.pdf", media_type='application/pdf')
