# Deteksi APD dengan YOLOv11

Tugas Akhir tentang deteksi Alat Pelindung Diri (PPE) menggunakan YOLOv11. Aplikasi web sederhana untuk demo hasil penelitian.

## Fitur

- Deteksi APD dari gambar
- Bisa atur confidence threshold sendiri
- Hasil ditampilkan dengan bounding box
- Ada metrics waktu inferensi dan FPS
- Bisa download hasil deteksi (gambar + CSV)

## Tech Stack

- Model: YOLOv11 dari Ultralytics
- Dataset: SH-17 PPE Dataset
- Framework: Streamlit (buat web app-nya)
- Deep Learning: PyTorch
- Computer Vision: OpenCV

## 📦 Instalasi

###Instalasi

Yang perlu disiapkan:

- Python 3.8 - 3.11
- pip

Cara install:

1. Clone repo ini

```bash
git clone https://github.com/Faqihaltaff/yolov11-ppe-detection.git
cd yolov11-ppe-detection
```

2. Bikin virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate  # di Windows
```

3. Install semua dependencies

```bash
pip install -r requirements.txt
```

4. Pastikan file `best.pt` ada di folder ini (model YOLOv11 yang udah di-training)

### Local Development

```bash
streamlit run app.py
```

Aplikasi akan berjalan di `http://localhost:8501`

## 🌐 Deployment

###Cara Jalanin

Gampang, tinggal:

```bash
streamlit run app.py
```

Nanti buka browser ke `http://localhost:8501`

## Deployment

Aplikasi ini udah di-deploy di Streamlit Cloud. Kalau mau deploy sendiri:

1. Push semua file ke GitHub
2. Buka streamlit.io/cloud
3. Login pake GitHub
4. Klik "New app" terus pilih repo ini
5. Main file path: `app.py`
6. Branch: `main`
7. Klik Deploy

Tunggu beberapa menit, aplikasi bakal live.

Note: Free tier Streamlit Cloud cuma 1GB RAM. Kalau model besar (>1GB), mending pake Hugging Face Spaces yang kasih 16GB RAM gratis.- Gambar akan ditampilkan untuk preview

3. **Jalankan Deteksi**

   - Click tombol "🔍 Jalankan Deteksi"
   - Tunggu proses inference

4. **Lihat Hasil**

   - Gambar dengan bounding boxes
   - Metrics: jumlah deteksi, inference time, FPS
   - Tabel detail dengan class, confidence, level

5. **Download Hasil**
   - Download gambar hasil annotated
   - Download CSV detail deteksi

## 📊 Struktur Project

```
Deploy-TA/
├── app.py              # Main Streamlit application
├── best.pt             # Trained YOLOv11 model
├── requirements.txt    # Python dependencies
├── README.md          # Documentation
└── .gitignore         # Git ignore rules
```

## 🔧 Troubleshooting

### Error: "No module named 'torch'"

```bash
pip install torch torchvision
```

###Cara Pakai

1. Buka aplikasi
2. Atur confidence threshold (default 0.25)
3. Upload gambar yang mau dideteksi (JPG/PNG)
4. Klik "Jalankan Deteksi"
5. Tunggu sebentar, hasil bakal muncul
6. Bisa download hasil deteksi dalam bentuk gambar atau CSV

- Dataset: SH-17 PPE Dataset
- Model: Ultralytics YOLOv11
- Framework: Streamlit
  Struktur File

```
.
├── app.py              # Aplikasi Streamlit
├── best.pt             # Model YOLOv11 yang udah di-training
├── requirements.txt    # Dependencies
├── README.md           # File ini
└── .streamlit/         # Config Streamlit
    └── config.toml
```

## Troubleshooting

**Error "No module named 'torch'"**

```bash
pip install torch torchvision
```

**Model tidak ditemukan**

- Cek file `best.pt` ada di folder yang sama dengan `app.py`

**Inference lambat**

- Wajar sih, soalnya pake CPU. Kalau mau cepet, butuh GPU
- Atau bisa pake model yang lebih kecil (YOLOv11n)

**Out of memory waktu deploy**

- Coba deploy di Hugging Face Spaces, RAMnya lebih gede

## Credits

- Dataset: SH-17 PPE Dataset
- YOLOv11: Ultralytics
- Framework: Streamlit

---

Tugas Akhir - Program Studi Informatika
