"""
FloraGuard — Frontend İskeleti (Sprint 1)
Streamlit tabanlı fotoğraf yükleme ekranı.
Sprint 2'de backend /predict endpoint'ine bağlanacaktır.

Çalıştırma:
    streamlit run src/app.py
"""

import streamlit as st

st.set_page_config(page_title="FloraGuard", page_icon="🌱", layout="centered")

# ---------------------------------------------------------------------------
# Başlık
# ---------------------------------------------------------------------------
st.title("🌱 FloraGuard")
st.caption("Bitkiniz önümüzdeki 5 gün içinde hastalanacak mı? Fotoğraf yükleyin, öğrenin.")

st.divider()

# ---------------------------------------------------------------------------
# Fotoğraf yükleme
# ---------------------------------------------------------------------------
uploaded_file = st.file_uploader(
    "Yaprak fotoğrafı yükleyin (JPEG/PNG)",
    type=["jpg", "jpeg", "png"],
    help="Net, tek yaprağı gösteren fotoğraflar en iyi sonucu verir.",
)

farmer_id = st.text_input("Çiftçi / Kullanıcı ID (opsiyonel)", value="", placeholder="ör. ciftci-042")

if uploaded_file is not None:
    st.image(uploaded_file, caption="Yüklenen görsel", use_container_width=True)

    if st.button("🔍 Analiz Et", type="primary", use_container_width=True):
        with st.spinner("Analiz ediliyor..."):
            # TODO (Sprint 2): requests.post("http://localhost:8000/predict", ...)
            st.info(
                "🔧 **Sprint 1 prototipi:** Model entegrasyonu Sprint 2'de tamamlanacaktır. "
                "Bu ekranda risk skoru, tahmini verim kaybı ve ajan tavsiyesi gösterilecektir."
            )

        # Sonuç ekranı taslağı (Sprint 2'de gerçek verilerle dolacak)
        col1, col2 = st.columns(2)
        col1.metric("Hastalık Riski (5 gün)", "—")
        col2.metric("Tahmini Verim Kaybı", "—")
        st.text_area("🤖 Ajan Tavsiyesi", value="(Sprint 2'de üretilecek)", disabled=True)
else:
    st.info("Başlamak için bir yaprak fotoğrafı yükleyin. 👆")

st.divider()
st.caption("YZTA Bootcamp 2026 — Sprint 1 Prototipi")
