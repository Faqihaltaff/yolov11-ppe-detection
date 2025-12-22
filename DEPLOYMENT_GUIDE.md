# Panduan Deploy ke Berbagai Platform

## 🚀 Quick Deploy ke Streamlit Cloud (TERMUDAH & GRATIS)

### Persiapan

1. **Pastikan semua file sudah ada:**

   - ✅ app.py
   - ✅ requirements.txt
   - ✅ best.pt
   - ✅ README.md
   - ✅ .gitignore

2. **Buat GitHub Repository:**

   ```bash
   # Initialize git (jika belum)
   git init

   # Add all files
   git add .

   # Commit
   git commit -m "Initial commit: YOLOv11 PPE Detection"

   # Create repo di GitHub, lalu:
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

3. **Deploy ke Streamlit Cloud:**
   - Buka https://streamlit.io/cloud
   - Sign in dengan GitHub
   - Klik "New app"
   - Pilih repository Anda
   - Branch: main
   - Main file path: app.py
   - Klik "Deploy"
   - Tunggu 5-10 menit, aplikasi akan live!

### ⚠️ Catatan Penting untuk Streamlit Cloud:

- **Ukuran model best.pt harus < 1GB** (batas free tier)
- Jika model > 1GB, gunakan Hugging Face Spaces atau platform lain
- Resource: 1GB RAM, 1 CPU (cukup untuk demo)

---

## 🤗 Deploy ke Hugging Face Spaces (Untuk Model Besar)

### Keuntungan:

- 16GB RAM (lebih besar dari Streamlit Cloud)
- Cocok untuk model > 1GB
- Gratis dan mudah

### Langkah-langkah:

1. **Buat Space:**

   - Kunjungi https://huggingface.co/spaces
   - Klik "Create new Space"
   - Pilih SDK: Streamlit
   - Pilih visibility: Public
   - Klik "Create Space"

2. **Upload Files:**

   - Clone space repository atau upload via web UI
   - Upload: app.py, requirements.txt, best.pt, README.md
   - File .streamlit/config.toml (opsional)

3. **Space akan auto-build dan deploy!**

---

## 🐳 Deploy dengan Docker (Advanced)

### Build Image:

```bash
docker build -t ppe-detection .
```

### Run Locally:

```bash
docker run -p 8501:8501 ppe-detection
```

### Deploy ke Cloud Run (Google Cloud):

```bash
# Build dan push ke Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ppe-detection

# Deploy ke Cloud Run
gcloud run deploy ppe-detection \
  --image gcr.io/YOUR_PROJECT_ID/ppe-detection \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi
```

---

## 🚂 Deploy ke Railway (Alternative)

1. **Buka https://railway.app**
2. **Connect GitHub repository**
3. **Railway akan auto-detect Streamlit**
4. **Add environment variables jika diperlukan**
5. **Deploy otomatis dari main branch**

Free tier: 500 jam/bulan, 512MB RAM

---

## 📋 Checklist Pre-Deployment

- [ ] Test aplikasi lokal (`streamlit run app.py`)
- [ ] Verifikasi semua dependencies terinstall
- [ ] Check ukuran file best.pt
- [ ] Update README.md dengan informasi TA
- [ ] Test upload berbagai format gambar
- [ ] Test dengan berbagai confidence threshold
- [ ] Pastikan download hasil berfungsi
- [ ] Commit semua changes ke Git
- [ ] Push ke GitHub
- [ ] Deploy ke platform pilihan

---

## 🔍 Troubleshooting

### Error: Model file not found

- Pastikan best.pt ada di root directory
- Check .gitignore tidak mengexclude best.pt

### Error: Out of Memory

- Gunakan platform dengan RAM lebih besar (Hugging Face Spaces)
- Atau quantize model untuk mengurangi ukuran

### Error: Module not found

- Pastikan semua dependencies ada di requirements.txt
- Test install di virtual environment baru

### Inference sangat lambat

- Platform gratis menggunakan CPU, bukan GPU
- Pertimbangkan platform berbayar dengan GPU support
- Atau gunakan model lebih kecil (YOLOv11n)

---

## 📊 Perbandingan Platform

| Platform           | RAM   | Storage | Cost      | Speed  | GPU      |
| ------------------ | ----- | ------- | --------- | ------ | -------- |
| Streamlit Cloud    | 1GB   | 1GB     | Free      | Medium | No       |
| HuggingFace Spaces | 16GB  | 50GB    | Free      | Medium | Optional |
| Railway            | 512MB | 1GB     | Free tier | Medium | No       |
| Google Cloud Run   | 2GB+  | Custom  | Pay/use   | Fast   | Optional |
| AWS App Runner     | 2GB+  | Custom  | Pay/use   | Fast   | Optional |

**Rekomendasi untuk TA:**

- Model < 1GB: **Streamlit Cloud** ✅
- Model > 1GB: **Hugging Face Spaces** ✅
- Production: **Google Cloud Run** / **AWS App Runner**

---

## 🎯 Next Steps Setelah Deploy

1. **Dapatkan Public URL** dari platform deployment
2. **Test aplikasi** dengan berbagai gambar
3. **Screenshot hasil** untuk dokumentasi TA
4. **Catat metrics** (inference time, accuracy, dll)
5. **Tulis di laporan TA:**
   - URL aplikasi
   - Platform deployment
   - Spesifikasi resource
   - Performance metrics
6. **Siapkan untuk presentasi/demo**

---

## 📝 Template Laporan TA

```
### Deployment Aplikasi

Aplikasi deteksi APD telah di-deploy menggunakan [Streamlit Cloud / Hugging Face Spaces]
dan dapat diakses secara public melalui URL:

**URL Aplikasi**: [URL_ANDA]

**Spesifikasi Deployment:**
- Platform: [Platform Name]
- RAM: [1GB / 16GB]
- CPU: [1 Core / 2 Cores]
- Model Size: [XX MB]

**Performance:**
- Average Inference Time: [X.XX seconds]
- Average FPS: [X.XX]
- Model Confidence Threshold: 0.25 (default)

**Teknologi:**
- Framework: Streamlit
- Model: YOLOv11
- Backend: Python 3.11
- Deep Learning: PyTorch
```

Good luck dengan deployment Tugas Akhir Anda! 🎓
