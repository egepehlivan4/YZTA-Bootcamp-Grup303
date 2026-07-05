"""
FloraGuard — Backend API İskeleti (Sprint 1)
FastAPI tabanlı; endpoint'ler şimdilik stub (taslak) yanıt döner.
Sprint 2'de Orkestratör Ajan ve modeller bu katmana bağlanacaktır.

Çalıştırma:
    uvicorn src.main:app --reload
"""

from datetime import datetime

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

app = FastAPI(
    title="FloraGuard API",
    description="Bitki hastalığı tahmin sistemi — tahmine dayalı karar destek API'si",
    version="0.1.0",
)


# ---------------------------------------------------------------------------
# Şemalar (Pydantic)
# ---------------------------------------------------------------------------

class PredictionResponse(BaseModel):
    """CNN + LSTM ensemble çıktısını temsil eden taslak yanıt şeması."""
    disease_probability: float  # 0.0 – 1.0 arası, 5 günlük hastalık riski
    estimated_yield_loss_pct: float  # regresyon modülünden gelecek
    advice: str  # Orkestratör Ajan'ın üreteceği tavsiye metni
    model_version: str


class HistoryRecord(BaseModel):
    """Çiftçi geçmiş kaydı — agent hafızasının temel birimi."""
    farmer_id: str
    timestamp: datetime
    disease_probability: float
    notes: str | None = None


# ---------------------------------------------------------------------------
# Endpoint'ler
# ---------------------------------------------------------------------------

@app.get("/health")
def health_check() -> dict:
    """Servis ayakta mı? Deployment smoke testleri bu endpoint'i kullanır."""
    return {"status": "ok", "service": "floraguard-api", "version": "0.1.0"}


@app.post("/predict", response_model=PredictionResponse)
async def predict(image: UploadFile = File(...), farmer_id: str = "anonymous") -> PredictionResponse:
    """
    Yaprak fotoğrafını alır; (Sprint 2'de) Orkestratör Ajan üzerinden
    CNN + LSTM ensemble'ını tetikleyip risk skoru ve tavsiye döner.

    Sprint 1 durumu: STUB — sabit örnek yanıt döner.
    """
    if image.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(status_code=415, detail="Yalnızca JPEG/PNG desteklenir.")

    # TODO (Sprint 2): orchestrator.run(image, farmer_id) çağrısı buraya bağlanacak
    return PredictionResponse(
        disease_probability=0.0,
        estimated_yield_loss_pct=0.0,
        advice="[STUB] Model entegrasyonu Sprint 2'de tamamlanacaktır.",
        model_version="prototype-0",
    )


@app.get("/history/{farmer_id}", response_model=list[HistoryRecord])
def get_history(farmer_id: str) -> list[HistoryRecord]:
    """
    Çiftçinin geçmiş tahmin kayıtlarını döner (agent hafızasının okuma ucu).

    Sprint 1 durumu: STUB — boş liste döner.
    TODO (Sprint 2): Veritabanı (SQLite/PostgreSQL) bağlantısı.
    """
    return []


@app.get("/weather/{location}")
def get_weather_series(location: str) -> dict:
    """
    LSTM modeline girdi olacak hava durumu zaman serisini döner.

    Sprint 1 durumu: STUB.
    TODO (Sprint 2): Gerçek hava durumu API entegrasyonu.
    """
    return {"location": location, "series": [], "note": "Sprint 2'de API bağlanacak"}
