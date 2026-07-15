"""
FloraGuard — Streamlit Arayüzü (Sprint 2)
FastAPI backend'ine (auth + predict + history) bağlanan tam istemci.
UI katmanı hiçbir iş mantığı içermez; yalnızca HTTP çağrıları yapar ve sonucu
görselleştirir (katman ayrımı — tüm zeka backend/agent tarafında).

Çalıştırma:
    streamlit run src/ui/streamlit_app.py
"""

import os
from datetime import datetime

import requests
import streamlit as st

API_BASE_URL = os.environ.get("FLORAGUARD_API_URL", "http://localhost:8000")

st.set_page_config(page_title="FloraGuard", page_icon="🌱", layout="centered")


# ---------------------------------------------------------------------------
# Oturum durumu
# ---------------------------------------------------------------------------

def _init_session_state() -> None:
    st.session_state.setdefault("access_token", None)
    st.session_state.setdefault("username", None)
    st.session_state.setdefault("role", None)


def _auth_headers() -> dict:
    return {"Authorization": f"Bearer {st.session_state['access_token']}"}


def _login(username: str, password: str) -> bool:
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/token",
            data={"username": username, "password": password},
            timeout=10,
        )
    except requests.ConnectionError:
        st.error(f"API'ye ulaşılamadı ({API_BASE_URL}). Backend çalışıyor mu?")
        return False

    if response.status_code != 200:
        st.error("Kullanıcı adı veya şifre hatalı.")
        return False

    payload = response.json()
    st.session_state["access_token"] = payload["access_token"]
    st.session_state["username"] = username
    st.session_state["role"] = payload["role"]
    return True


def _logout() -> None:
    for key in ("access_token", "username", "role"):
        st.session_state[key] = None


# ---------------------------------------------------------------------------
# Giriş ekranı
# ---------------------------------------------------------------------------

_init_session_state()

st.title("🌱 FloraGuard")
st.caption("Bitkiniz önümüzdeki 5 gün içinde hastalanacak mı? Fotoğraf yükleyin, öğrenin.")

if not st.session_state["access_token"]:
    st.divider()
    st.subheader("🔐 Giriş Yap")
    st.caption(
        "Demo hesaplar — Çiftçi: `ciftci1` / `ciftci123` · "
        "Danışman: `danisman1` / `danisman123` · Admin: `admin1` / `admin123`"
    )
    with st.form("login_form"):
        username = st.text_input("Kullanıcı adı")
        password = st.text_input("Şifre", type="password")
        submitted = st.form_submit_button("Giriş Yap", type="primary", use_container_width=True)

    if submitted:
        if _login(username, password):
            st.rerun()
    st.stop()


# ---------------------------------------------------------------------------
# Üst bilgi çubuğu (giriş yapılmışsa)
# ---------------------------------------------------------------------------

col_user, col_logout = st.columns([4, 1])
col_user.success(f"Giriş yapıldı: **{st.session_state['username']}** ({st.session_state['role']})")
if col_logout.button("Çıkış", use_container_width=True):
    _logout()
    st.rerun()

st.divider()

# ---------------------------------------------------------------------------
# Analiz formu
# ---------------------------------------------------------------------------

st.subheader("📸 Yeni Analiz")

default_farmer_id = st.session_state["username"] if st.session_state["role"] == "farmer" else ""
farmer_id = st.text_input("Çiftçi ID", value=default_farmer_id, placeholder="ör. ciftci1")
location = st.text_input("Konum (şehir/ilçe)", placeholder="ör. Antalya")
crop_type = st.selectbox("Ürün Tipi", ["domates", "biber", "salatalik", "patates", "bugday"])

uploaded_file = st.file_uploader(
    "Yaprak fotoğrafı yükleyin (JPEG/PNG)",
    type=["jpg", "jpeg", "png"],
    help="Net, tek yaprağı gösteren fotoğraflar en iyi sonucu verir.",
)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Yüklenen görsel", use_container_width=True)

    analyze_disabled = not farmer_id or not location
    if st.button("🔍 Analiz Et", type="primary", use_container_width=True, disabled=analyze_disabled):
        with st.spinner("Orkestratör Ajan çalışıyor: CNN + LSTM + Ensemble + Regresyon..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/predict",
                    headers=_auth_headers(),
                    files={"image": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)},
                    data={"farmer_id": farmer_id, "location": location, "crop_type": crop_type},
                    timeout=120,
                )
            except requests.ConnectionError:
                st.error(f"API'ye ulaşılamadı ({API_BASE_URL}). Backend çalışıyor mu?")
                response = None

        if response is not None:
            if response.status_code == 200:
                result = response.json()
                st.divider()
                col1, col2 = st.columns(2)
                col1.metric("Hastalık Riski (5 gün)", f"%{result['disease_probability'] * 100:.0f}")
                col2.metric("Tahmini Verim Kaybı", f"%{result['estimated_yield_loss_pct']:.1f}")
                st.caption(f"CNN sınıflandırması: **{result['cnn_top_class']}**")
                st.text_area("🤖 Ajan Tavsiyesi", value=result["advice"], disabled=True, height=100)
            else:
                st.error(f"Analiz başarısız oldu ({response.status_code}): {response.text}")

st.divider()

# ---------------------------------------------------------------------------
# Geçmiş
# ---------------------------------------------------------------------------

st.subheader("📜 Geçmiş Kayıtlar")
history_farmer_id = st.text_input("Geçmişini görüntülemek istediğiniz Çiftçi ID", value=default_farmer_id)

if st.button("Geçmişi Getir"):
    try:
        response = requests.get(
            f"{API_BASE_URL}/history/{history_farmer_id}", headers=_auth_headers(), timeout=10,
        )
    except requests.ConnectionError:
        st.error(f"API'ye ulaşılamadı ({API_BASE_URL}).")
        response = None

    if response is not None:
        if response.status_code == 200:
            records = response.json()
            if not records:
                st.info("Bu çiftçi için henüz kayıt yok.")
            else:
                for record in records:
                    ts = datetime.fromisoformat(record["timestamp"]).strftime("%Y-%m-%d %H:%M")
                    with st.expander(f"{ts} — %{record['disease_probability'] * 100:.0f} risk"):
                        st.write(f"**Ürün:** {record['crop_type']} · **Konum:** {record['location']}")
                        st.write(f"**Tahmini verim kaybı:** %{record['estimated_yield_loss_pct']:.1f}")
                        if record.get("advice"):
                            st.write(f"**Tavsiye:** {record['advice']}")
        else:
            st.error(f"Geçmiş alınamadı ({response.status_code}): {response.text}")

st.divider()
st.caption("YZTA Bootcamp 2026 — Sprint 2: Entegrasyon ve Zeka")
