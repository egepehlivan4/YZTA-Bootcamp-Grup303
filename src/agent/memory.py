"""
FloraGuard — Agent Hafızası (Memory)
Çiftçinin geçmiş tahmin kayıtlarını SQLite'ta tutar. Orkestratör Ajan, tavsiye
üretmeden önce bu modülü bir "tool" aracılığıyla sorgulayarak bağlam kazanır
(ör. "geçen ay da yüksek nem riski vardı, sulama azaltılmıştı").

Neden SQLite (Chroma değil)? Buradaki hafıza yapısal/sayısaldır (tarih, risk
skoru, ürün tipi) — semantik benzerlik aramasına değil, filtrelenebilir sorgulara
ihtiyaç var. Serbest metin notları için embedding tabanlı arama (Chroma) ileride
bu modülün yanına eklenebilir; arayüz (get_recent_history) değişmeden kalır.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from src.data.database import get_connection

_SCHEMA = """
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    crop_type TEXT NOT NULL,
    location TEXT NOT NULL,
    disease_probability REAL NOT NULL,
    estimated_yield_loss_pct REAL NOT NULL,
    advice TEXT
);
CREATE INDEX IF NOT EXISTS idx_predictions_farmer ON predictions(farmer_id, timestamp DESC);
"""


class FarmerMemory:
    """Çiftçi geçmişi için okuma/yazma arayüzü. Tek sorumluluk: kalıcılık."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        with get_connection(self.db_path) as conn:
            conn.executescript(_SCHEMA)

    def add_record(
        self,
        farmer_id: str,
        crop_type: str,
        location: str,
        disease_probability: float,
        estimated_yield_loss_pct: float,
        advice: str | None = None,
        timestamp: datetime | None = None,
    ) -> int:
        timestamp = timestamp or datetime.now(timezone.utc)
        with get_connection(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO predictions
                    (farmer_id, timestamp, crop_type, location, disease_probability,
                     estimated_yield_loss_pct, advice)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (farmer_id, timestamp.isoformat(), crop_type, location,
                 disease_probability, estimated_yield_loss_pct, advice),
            )
            return cursor.lastrowid

    def get_recent_history(self, farmer_id: str, limit: int = 5) -> list[dict]:
        with get_connection(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT id, farmer_id, timestamp, crop_type, location,
                       disease_probability, estimated_yield_loss_pct, advice
                FROM predictions
                WHERE farmer_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (farmer_id, limit),
            ).fetchall()
            return [dict(row) for row in rows]

    def summarize_for_agent(self, farmer_id: str, limit: int = 5) -> str:
        """
        Agent prompt'una gömülecek kısa, okunabilir özet üretir.
        Ham JSON yerine düz metin vermek, LLM'in bağlamı doğru yorumlamasını kolaylaştırır.
        """
        history = self.get_recent_history(farmer_id, limit=limit)
        if not history:
            return f"'{farmer_id}' için geçmiş kayıt bulunamadı (ilk analiz)."

        lines = [f"'{farmer_id}' için son {len(history)} kayıt:"]
        for record in history:
            date = record["timestamp"][:10]
            lines.append(
                f"- {date}: risk=%{record['disease_probability'] * 100:.0f}, "
                f"verim kaybı=%{record['estimated_yield_loss_pct']:.1f}, "
                f"ürün={record['crop_type']}, konum={record['location']}"
            )
        return "\n".join(lines)
