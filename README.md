# 🦺 Sistem Deteksi Alat Pelindung Diri (APD)

Aplikasi web untuk deteksi Alat Pelindung Diri (Personal Protective Equipment/PPE) menggunakan YOLOv11. Dikembangkan sebagai bagian dari Tugas Akhir.

## 🎯 Fitur

- ✅ Deteksi APD real-time pada gambar statis
- ✅ Konfigurasi confidence threshold
- ✅ Visualisasi hasil dengan bounding boxes
- ✅ Metrics inference (waktu, FPS, jumlah deteksi)
- ✅ Tabel detail hasil deteksi dengan level confidence
- ✅ Export hasil (gambar annotated + CSV)
- ✅ Interface berbahasa Indonesia

## 🛠️ Teknologi

- **Model**: YOLOv11 (Ultralytics)
- **Dataset**: SH-17 PPE Dataset
- **Framework**: Streamlit
- **Deep Learning**: PyTorch
- **Computer Vision**: OpenCV

## 📦 Instalasi

### Prasyarat

- Python 3.8 - 3.11
- pip

### Langkah-langkah

1. **Clone repository**

```bash
git clone <repository-url>
cd Deploy-TA
```

2. **Buat virtual environment (opsional tapi disarankan)**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Pastikan file model ada**

- File `best.pt` harus ada di root directory
- Ini adalah trained YOLOv11 model untuk deteksi APD

## 🚀 Menjalankan Aplikasi

### Local Development

```bash
streamlit run app.py
```

Aplikasi akan berjalan di `http://localhost:8501`

## 🌐 Deployment

### Streamlit Community Cloud (Gratis)

1. **Push ke GitHub**

   - Create repository baru di GitHub
   - Push semua files termasuk `best.pt`

2. **Deploy ke Streamlit Cloud**

   - Kunjungi [streamlit.io/cloud](https://streamlit.io/cloud)
   - Sign in dengan GitHub
   - Click "New app"
   - Pilih repository, branch, dan `app.py`
   - Click "Deploy"

3. **Catatan**:
   - Free tier: 1GB RAM, 1 CPU
   - Jika model >1GB, pertimbangkan platform lain

### Hugging Face Spaces

1. **Create Space**

   - Kunjungi [huggingface.co/spaces](https://huggingface.co/spaces)
   - Create new Space, pilih Streamlit SDK

2. **Upload Files**

   - Upload `app.py`, `requirements.txt`, `best.pt`
   - Space akan auto-build dan deploy

3. **Kelebihan**:
   - 16GB RAM (lebih besar dari Streamlit Cloud)
   - Cocok untuk model yang lebih besar

### Docker (Advanced)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build dan run:

```bash
docker build -t ppe-detection .
docker run -p 8501:8501 ppe-detection
```

## 📝 Cara Penggunaan

1. **Konfigurasi Deteksi**

   - Atur confidence threshold (0.10 - 1.00)
   - Default: 0.25

2. **Upload Gambar**

   - Pilih gambar JPG/JPEG/PNG
   - Gambar akan ditampilkan untuk preview

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

### Error: "Model file not found"

- Pastikan `best.pt` ada di root directory
- Check path di `app.py` line 26

### Inference sangat lambat

- Pastikan PyTorch menggunakan GPU jika tersedia
- Check dengan: `import torch; print(torch.cuda.is_available())`
- Atau gunakan model lebih kecil (YOLOv11n/YOLOv11s)

### Out of Memory saat deployment

- Gunakan platform dengan RAM lebih besar (Hugging Face Spaces)
- Pertimbangkan model quantization
- Atau export ke ONNX format

## 📄 License

Dikembangkan untuk keperluan Tugas Akhir - Program Studi Informatika

## 👤 Author

Tugas Akhir - Deteksi APD dengan YOLOv11

## 🙏 Acknowledgments

- Dataset: SH-17 PPE Dataset
- Model: Ultralytics YOLOv11
- Framework: Streamlit
