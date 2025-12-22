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
st.set_page_config(page_title="YOLOv11 PPE Detection", layout="centered")

# Variabel config
max_size = 10  # MB
model_file = "best.pt"

st.title("🦺 Sistem Deteksi Alat Pelindung Diri (APD)")
st.caption("Aplikasi deployment model YOLOv11 untuk deteksi APD")

# Load model (pake cache biar ga reload terus)
@st.cache_resource
def get_model():
    if not os.path.exists(model_file):
        st.error("Model ga ketemu!")
        st.stop()
    return YOLO(model_file)

model = get_model()

# Info model
with st.expander("ℹ️ Info Model"):
    st.write("**Arsitektur**: YOLOv11")
    st.write("**Dataset**: SH-17 PPE Dataset")
    st.write("**Output**: Bounding Box + Label + Confidence")

st.markdown("---")

# Step 1: Setting threshold
st.header("1️⃣ Atur Confidence Threshold")
threshold = st.slider("Confidence Threshold", 0.1, 1.0, 0.25, 0.05)

st.markdown("---")

# Step 2: Upload gambar
st.header("2️⃣ Upload Gambar")
file = st.file_uploader("📤 Pilih gambar", type=["jpg", "jpeg", "png"])


# ===============================
# STEP 3: DETEKSI
# ===============================
if uploaded_file is not None:
    # Validasi ukuran file
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error(f"❌ File terlalu besar! Max: {MAX_FILE_SIZE_MB}MB, ukuran file: {file_size_mb:.2f}MB")
        st.stop()
    
    # Baca gambar yang diupload
    try:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Gambar Input", use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error membaca gambar: {str(e)}")
        st.stop()

    # Tombol untuk mulai deteksi
    if st.button("🔍 Jalankan Deteksi", type="primary"):
        with st.spinner("Sedang melakukan deteksi..."):
  Kalau ada file yang diupload
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
            
            # Jalanin model
            t1 = time.time()
            res = model.predict(source=temp_file.name, conf=threshold, verbose=False)
            t2 = time.time()
            waktu = t2 - t1
            
            # Visualisasi hasil
            img_hasil = res[0].plot()
            img_hasil = cv2.cvtColor(img_hasil, cv2.COLOR_BGR2RGB)
            
            st.markdown("---")
            st.header("3️⃣ Hasil Deteksi")
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
                st.subheader("📊 Detail Deteksi")
                
                # Bikin list data
                detections = []
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
                    
                    detections.append({
                        "Kelas": nama_kelas,
                        "Confidence": round(conf, 3),
                        "Level": lvl
                    })
                
                df = pd.DataFrame(detections)
                
                # Filter by class
                kelas_unik = df['Kelas'].unique().tolist()
                if len(kelas_unik) > 1:
                    pilihan = st.multiselect("Filter Kelas:", ["Semua"] + kelas_unik, default=["Semua"])
                    if "Semua" not in pilihan:
                        df = df[df['Kelas'].isin(pilihan)]
                
                st.dataframe(df, use_container_width=True)
                
                # Chart statistik
                st.subheader("📈 Statistik")
                col1, col2 = st.columns(2)
                
                with col1:
                    # Pie chart distribusi kelas
                    kelas_count = df['Kelas'].value_counts()
                    fig1 = px.pie(values=kelas_count.values, names=kelas_count.index, 
                                  title="Distribusi Kelas", hole=0.3)
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    # Bar chart confidence
                    fig2 = px.bar(df, x='Kelas', y='Confidence', 
                                  title="Confidence per Objek",
                                  color='Confidence')
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Download hasil
                st.subheader("⬇️ Download Hasil")
                col1, col2 = st.columns(2)
                
                with col1:
                    # Save image
                    hasil_path = "hasil_deteksi.jpg"
                    Image.fromarray(img_hasil).save(hasil_path)
                    with open(hasil_path, "rb") as f:
                        st.download_button("📥 Download Gambar", f, "hasil_deteksi.jpg", "image/jpeg")
                
                with col2:
                    # Save CSV
                    csv_data = df.to_csv(index=False).encode("utf-8")
                    st.download_button("📥 Download CSV", csv_data, "hasil_deteksi.csv", "text/csv")
            
            # Hapus file temporary
            os.remove(temp_file.name)
