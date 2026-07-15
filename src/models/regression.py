"""
FloraGuard — Regresyon Modülü (Tahmini Verim Kaybı %)
Ensemble risk skorunu ve ürün tipini girdi alıp scikit-learn tabanlı bir
regresyon modeliyle "%verim kaybı" tahmini üretir.

Üretim artığı (artifact) `artifacts/yield_regressor.joblib` dosyasında saklanır.
Artifact yoksa (ör. ilk kurulum, henüz eğitim yapılmadı) sistemin çökmemesi için
yorumlanabilir bir HEURISTIC formüle geri düşer (graceful degradation) ve
log'da `train_regression.py` çalıştırılması önerilir.
"""

from __future__ import annotations

import logging
from pathlib import Path

import joblib

logger = logging.getLogger(__name__)

# Eğitim scriptiyle (train_regression.py) birebir aynı sırada olmalı.
KNOWN_CROPS: tuple[str, ...] = ("domates", "biber", "salatalik", "patates", "bugday")


class YieldLossRegressor:
    """Risk skoru (+ürün tipi) -> tahmini verim kaybı yüzdesi."""

    def __init__(self, artifact_path: Path):
        self.artifact_path = artifact_path
        self._pipeline = None
        self._load()

    def _load(self) -> None:
        if self.artifact_path.exists():
            self._pipeline = joblib.load(self.artifact_path)
            logger.info("Regresyon modeli yüklendi: %s", self.artifact_path)
        else:
            logger.warning(
                "Regresyon artifact'ı bulunamadı (%s). Heuristic fallback formülü "
                "kullanılacak. Gerçek model için: `python -m src.models.train_regression`",
                self.artifact_path,
            )

    @property
    def is_trained_model_loaded(self) -> bool:
        return self._pipeline is not None

    def predict(self, risk_score: float, crop_type: str = "domates") -> dict:
        if not 0.0 <= risk_score <= 1.0:
            raise ValueError(f"risk_score 0-1 aralığında olmalı, gelen değer: {risk_score}")

        crop_type = crop_type.lower().strip()
        if crop_type not in KNOWN_CROPS:
            logger.info("Bilinmeyen ürün tipi '%s' — genel (domates) katsayısıyla devam ediliyor.", crop_type)
            crop_type = "domates"

        if self._pipeline is not None:
            import pandas as pd

            X = pd.DataFrame([{"risk_score": risk_score, "crop_type": crop_type}])
            pct = float(self._pipeline.predict(X)[0])
            model_used = "sklearn-gbr"
        else:
            pct = self._heuristic_formula(risk_score, crop_type)
            model_used = "heuristic-fallback"

        pct = max(0.0, min(100.0, pct))
        return {"estimated_yield_loss_pct": round(pct, 2), "model_used": model_used}

    @staticmethod
    def _heuristic_formula(risk_score: float, crop_type: str) -> float:
        """
        Eğitilmiş model yokken kullanılan basit, açıklanabilir yaklaşım:
        verim kaybı ~ risk^1.5 * 100, ürün duyarlılık katsayısıyla ölçeklenir.
        """
        crop_sensitivity = {
            "domates": 1.0,
            "biber": 0.9,
            "salatalik": 1.1,
            "patates": 0.8,
            "bugday": 0.6,
        }
        sensitivity = crop_sensitivity.get(crop_type, 1.0)
        return (risk_score ** 1.5) * 100 * sensitivity
