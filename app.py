"""
FloraGuard — Kök Frontend Girişi (geriye dönük uyumluluk için ince sarmalayıcı)
Gerçek arayüz `src/ui/streamlit_app.py` içindedir (katmanlı mimari).

Çalıştırma:
    streamlit run app.py
    # veya doğrudan: streamlit run src/ui/streamlit_app.py
"""

import runpy

runpy.run_module("src.ui.streamlit_app", run_name="__main__")
