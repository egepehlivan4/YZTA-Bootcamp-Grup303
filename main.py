"""
FloraGuard — Kök Backend Girişi (geriye dönük uyumluluk için ince sarmalayıcı)
Gerçek uygulama `src/api/main.py` içindedir (katmanlı mimari).

Çalıştırma:
    uvicorn main:app --reload
    # veya doğrudan: uvicorn src.api.main:app --reload
"""

from src.api.main import app

__all__ = ["app"]
