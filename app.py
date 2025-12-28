import streamlit as st
from ultralytics import YOLO
from PIL import Image
import cv2
import tempfile
import os
import time
import pandas as pd
import plotly.express as px

# Config halaman
st.set_page_config(page_title="YOLOv11 PPE Detection", layout="wide")

# Variabel config
max_size = 10  # MB
model_files = {
    "YOLOv9": "yolov9.pt",
    "YOLOv10": "yolov10.pt",
    "YOLOv11": "yolov11.pt"
}

# Definisi kelas APD dan Non-APD berdasarkan SH-17 PPE Dataset
apd_classes = [
    'helmet', 'ear-mufs', 'face-guard', 'face-mask', 
    'glasses', 'gloves', 'medical-suit', 'shoes', 
    'safety-suit', 'safety-vest'
]

non_apd_classes = [
    'person', 'ear', 'face', 'foot', 'tool', 
    'hands', 'head'
]

st.title("🦺 Sistem Deteksi Alat Pelindung Diri (APD)")
st.caption("Aplikasi deployment model YOLOv9, YOLOv10, dan YOLOv11 untuk deteksi APD")

# Load semua model (pake cache biar ga reload terus)
@st.cache_resource
def get_models():
    models = {}
    for name, file_path in model_files.items():
        if not os.path.exists(file_path):
            st.warning(f"Model {name} ({file_path}) ga ketemu!")
        else:
            models[name] = YOLO(file_path)
    if not models:
        st.error("Ga ada model yang bisa diload!")
        st.stop()
    return models

models = get_models()

# Info model
with st.expander("ℹ️ Info Model"):
    st.write(f"**Model Tersedia**: {', '.join(models.keys())}")
    st.write("**Dataset**: SH-17 PPE Dataset")
    st.write("**Output**: Bounding Box + Label + Confidence")

st.markdown("---")

# Step 1: Setting threshold dan model
st.header("1️⃣ Atur Deteksi")
col_a, col_b = st.columns(2)
with col_a:
    mode = st.radio("Mode Deteksi", ["Single Model", "All Models (Perbandingan 3 Model)"], horizontal=True)

with col_b:
    threshold = st.slider("Confidence Threshold", 0.1, 1.0, 0.25, 0.05)

if mode == "Single Model":
    selected_model = st.selectbox("Pilih Model", list(models.keys()))
    models_to_use = {selected_model: models[selected_model]}
else:
    st.info("Mode perbandingan: Akan menjalankan deteksi dengan YOLOv9, YOLOv10, dan YOLOv11 secara bersamaan")
    models_to_use = models

st.markdown("---")

# Step 2: Upload gambar
st.header("2️⃣ Upload Gambar")
file = st.file_uploader("📤 Pilih gambar", type=["jpg", "jpeg", "png"])

# Kalau ada file yang diupload
if file is not None:
    # Cek ukuran file
    size_mb = file.size / (1024 * 1024)
    if size_mb > max_size:
        st.error(f"File terlalu besar! Max {max_size}MB")
        st.stop()
    
    # Baca gambar
    img = Image.open(file).convert("RGB")
    st.image(img, caption="Gambar Input", use_container_width=True)

    # Tombol deteksi
    if st.button("🔍 Jalankan Deteksi", type="primary"):
        with st.spinner("Lagi proses deteksi..."):
            # Simpan gambar ke temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            img.save(temp_file.name)
            temp_file.close()
            temp_path = temp_file.name
            
            st.markdown("---")
            st.header("3️⃣ Hasil Deteksi")
            
            # Loop untuk setiap model
            for idx, (model_name, model) in enumerate(models_to_use.items()):
                if len(models_to_use) > 1:
                    st.markdown(f"### 🤖 {model_name}")
                
                # Jalanin model
                t1 = time.time()
                res = model.predict(source=temp_path, conf=threshold, verbose=False)
                t2 = time.time()
                waktu = t2 - t1
                
                # Visualisasi hasil
                img_hasil = res[0].plot()
                img_hasil = cv2.cvtColor(img_hasil, cv2.COLOR_BGR2RGB)
                
                st.image(img_hasil, use_container_width=True)
                
                # Hitung jumlah deteksi
                jumlah = len(res[0].boxes)
                fps = 1/waktu if waktu > 0 else 0
                
                # Tampilkan metrics
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Deteksi", jumlah)
                c2.metric("Waktu", f"{waktu:.3f}s")
                c3.metric("FPS", f"{fps:.2f}")
                
                # Bikin tabel deteksi
                if jumlah == 0:
                    st.info("Ga ada objek yang terdeteksi")
                else:
                    with st.expander(f"📊 Detail Deteksi {model_name}", expanded=(len(models_to_use)==1)):
                        # Bikin list data
                        detections = []
                        apd_count = 0
                        non_apd_count = 0
                        
                        for box in res[0].boxes:
                            id_kelas = int(box.cls[0])
                            conf = float(box.conf[0])
                            nama_kelas = model.names[id_kelas]
                            
                            # Tentuin level
                            if conf >= 0.75:
                                lvl = "🟢 Tinggi"
                            elif conf >= 0.50:
                                lvl = "🟡 Sedang"
                            else:
                                lvl = "🔴 Rendah"
                            
                            # Kategorisasi APD vs Non-APD
                            if nama_kelas.lower() in apd_classes:
                                kategori = "✅ APD"
                                apd_count += 1
                            elif nama_kelas.lower() in non_apd_classes:
                                kategori = "❌ Non-APD"
                                non_apd_count += 1
                            else:
                                kategori = "❓ Lainnya"
                            
                            detections.append({
                                "Kategori": kategori,
                                "Kelas": nama_kelas,
                                "Confidence": round(conf, 3),
                                "Level": lvl
                            })
                        
                        df = pd.DataFrame(detections)
                        
                        # Summary APD vs Non-APD
                        st.markdown("#### 🎯 Summary Kategori")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("✅ APD", apd_count)
                        col2.metric("❌ Non-APD", non_apd_count)
                        col3.metric("📊 Total", jumlah)
                        
                        st.dataframe(df, use_container_width=True)
                        
                        # Chart statistik
                        st.markdown("#### 📈 Statistik")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            # Pie chart APD vs Non-APD
                            kategori_data = df['Kategori'].value_counts()
                            fig1 = px.pie(values=kategori_data.values, names=kategori_data.index, 
                                          title="APD vs Non-APD", hole=0.3,
                                          color_discrete_sequence=['#00D26A', '#FF4B4B', '#FFD700'])
                            st.plotly_chart(fig1, use_container_width=True)
                        
                        with col2:
                            # Pie chart distribusi kelas
                            kelas_count = df['Kelas'].value_counts()
                            fig2 = px.pie(values=kelas_count.values, names=kelas_count.index, 
                                          title="Distribusi Kelas", hole=0.3)
                            st.plotly_chart(fig2, use_container_width=True)
                        
                        with col3:
                            # Bar chart confidence
                            fig3 = px.bar(df, x='Kelas', y='Confidence', 
                                          title="Confidence per Objek",
                                          color='Kategori')
                            st.plotly_chart(fig3, use_container_width=True)
                        
                        # Download hasil
                        st.markdown("#### ⬇️ Download Hasil")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Save image
                            hasil_path = f"hasil_{model_name.lower()}.jpg"
                            Image.fromarray(img_hasil).save(hasil_path)
                            with open(hasil_path, "rb") as f:
                                st.download_button(
                                    f"📥 Download Gambar ({model_name})", 
                                    f, 
                                    f"hasil_{model_name.lower()}.jpg", 
                                    "image/jpeg",
                                    key=f"img_{model_name}"
                                )
                        
                        with col2:
                            # Save CSV
                            csv_data = df.to_csv(index=False).encode("utf-8")
                            st.download_button(
                                f"📥 Download CSV ({model_name})", 
                                csv_data, 
                                f"hasil_{model_name.lower()}.csv", 
                                "text/csv",
                                key=f"csv_{model_name}"
                            )
                
                # Tambah separator jika multiple models
                if len(models_to_use) > 1 and idx < len(models_to_use) - 1:
                    st.markdown("---")
            
            # Hapus file temporary
            try:
                os.remove(temp_path)
            except:
                pass  # Ga masalah kalau gagal hapus
