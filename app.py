import streamlit as st
from ultralytics import YOLO
from PIL import Image
import cv2
import tempfile
import os
import time
import pandas as pd

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="YOLOv11 PPE Detection",
    layout="centered"
)

# ===============================
# CONSTANTS
# ===============================
MAX_FILE_SIZE_MB = 10  # Maximum upload file size in MB
ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png"]
MODEL_PATH = "best.pt"

st.title("🦺 Sistem Deteksi Alat Pelindung Diri (APD)")
st.caption("Aplikasi deployment model YOLOv11 untuk deteksi APD pada citra statis")

# ===============================
# LOAD MODEL
# ===============================
@st.cache_resource
def load_model():
    try:
        if not os.path.exists(MODEL_PATH):
            st.error(f"❌ File model '{MODEL_PATH}' tidak ditemukan!")
            st.stop()
        return YOLO(MODEL_PATH)
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        st.stop()

model = load_model()

# ===============================
# ABOUT MODEL (UX INFO)
# ===============================
with st.expander("ℹ️ Tentang Model"):
    st.write("""
    **Arsitektur** : YOLOv11  
    **Task** : Object Detection  
    **Dataset** : SH-17 PPE Dataset  
    **Output** : Bounding Box, Label Kelas, Confidence Score  

    Model ini dideploy dalam bentuk aplikasi web sederhana untuk 
    memudahkan proses inferensi dan demonstrasi hasil penelitian Tugas Akhir.
    """)

st.markdown("---")

# ===============================
# STEP 1 — CONFIGURATION
# ===============================
st.header("1️⃣ Konfigurasi Deteksi")

conf_threshold = st.slider(
    "Confidence Threshold",
    min_value=0.10,
    max_value=1.00,
    value=0.25,
    step=0.05,
    help="Nilai minimum confidence agar objek APD ditampilkan"
)

st.markdown("---")

# ===============================
# STEP 2 — UPLOAD IMAGE
# ===============================
st.header("2️⃣ Upload Gambar")

uploaded_file = st.file_uploader(
    "📤 Pilih file gambar",
    type=ALLOWED_EXTENSIONS,
    help=f"Gunakan gambar dengan objek APD terlihat jelas (Max: {MAX_FILE_SIZE_MB}MB)"
)

# ===============================
# INFERENCE
# ===============================
if uploaded_file is not None:
    # Validate file size
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error(f"❌ File terlalu besar! Ukuran maksimum: {MAX_FILE_SIZE_MB}MB. Ukuran file Anda: {file_size_mb:.2f}MB")
        st.stop()
    
    try:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Gambar Input", use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error membaca gambar: {str(e)}")
        st.stop()

    if st.button("🔍 Jalankan Deteksi"):
        with st.spinner("Model sedang melakukan inferensi..."):
            img_path = None
            try:
                # simpan sementara
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    image.save(tmp.name)
                    img_path = tmp.name

                # ===============================
                # MODEL INFERENCE
                # ===============================
                start_time = time.time()
                results = model.predict(
                    source=img_path,
                    conf=conf_threshold,
                    verbose=False
                )
                end_time = time.time()

                inference_time = end_time - start_time
                fps = 1 / inference_time if inference_time > 0 else 0
            except Exception as e:
                st.error(f"❌ Error saat inferensi: {str(e)}")
                if img_path and os.path.exists(img_path):
                    os.remove(img_path)
                st.stop()

            try:
                # ===============================
                # VISUAL OUTPUT
                # ===============================
                result_img = results[0].plot()
                result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)

                st.markdown("---")
                st.header("3️⃣ Hasil Deteksi")

                st.image(
                    result_img,
                    caption="Hasil Deteksi APD",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ Error saat memvisualisasi hasil: {str(e)}")
                if img_path and os.path.exists(img_path):
                    os.remove(img_path)
                st.stop()

            # ===============================
            # EXECUTIVE SUMMARY
            # ===============================
            total_det = len(results[0].boxes)
            st.success(
                f"Deteksi selesai — {total_det} objek APD teridentifikasi "
                f"dengan confidence ≥ {conf_threshold}"
            )

            # ===============================
            # KPI METRICS
            # ===============================
            st.subheader("📈 Inference Metrics")

            col1, col2, col3 = st.columns(3)
            col1.metric("Jumlah Deteksi", total_det)
            col2.metric("Inference Time (s)", f"{inference_time:.3f}")
            col3.metric("FPS (estimasi)", f"{fps:.2f}")

            # ===============================
            # CONFIDENCE LEVEL FUNCTION
            # ===============================
            def conf_level(c):
                if c >= 0.75:
                    return "🟢 Tinggi"
                elif c >= 0.50:
                    return "🟡 Sedang"
                else:
                    return "🔴 Rendah"

            # ===============================
            # DETECTION TABLE
            # ===============================
            st.subheader("📊 Detail Hasil Deteksi")

            if total_det == 0:
                st.info("Tidak ada objek APD yang terdeteksi.")
            else:
                data = []
                for box in results[0].boxes:
                    cls_id = int(box.cls[0])
                    conf   = float(box.conf[0])
                    label  = model.names[cls_id]

                    data.append({
                        "Class": label,
                        "Confidence": round(conf, 3),
                        "Level": conf_level(conf)
                    })

                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)

                # ===============================
                # EXPORT RESULTS
                # ===============================
                st.subheader("⬇️ Unduh Hasil")

                try:
                    # save image
                    result_path = "hasil_deteksi.jpg"
                    Image.fromarray(result_img).save(result_path)

                    with open(result_path, "rb") as f:
                        st.download_button(
                            label="📥 Download Gambar Hasil",
                            data=f,
                            file_name="hasil_deteksi.jpg",
                            mime="image/jpeg"
                        )

                    # save csv
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="📥 Download CSV Deteksi",
                        data=csv,
                        file_name="hasil_deteksi.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.warning(f"⚠️ Error saat menyimpan hasil: {str(e)}")

            # Cleanup temporary file
            if img_path and os.path.exists(img_path):
                try:
                    os.remove(img_path)
                except:
                    pass  # Ignore cleanup errors

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption("© 2025 | Deployment YOLOv11 – Tugas Akhir Informatika")
