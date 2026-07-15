"""
FloraGuard — Regresyon Modeli Eğitim Scripti (offline)
`YieldLossRegressor`'ın kullandığı joblib artifact'ını üretir.

Şu an gerçek saha verisi (gerçek hasat/verim kaybı ölçümleri) mevcut olmadığından,
üretim ortamına geçişte kolayca değiştirilebilecek şekilde İZOLE bir sentetik veri
üreteci kullanılır (bkz. `_make_synthetic_dataset`). Gerçek veri geldiğinde bu
fonksiyonu bir CSV/DB okuyacak şekilde değiştirmek yeterlidir — pipeline aynı kalır.

Çalıştırma:
    python -m src.models.train_regression
"""

from __future__ import annotations

import logging

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.config import get_settings
from src.models.regression import KNOWN_CROPS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _make_synthetic_dataset(n_samples: int = 4000, seed: int = 42) -> pd.DataFrame:
    """
    TODO (gerçek veri geldiğinde): Bu fonksiyonu saha/hasat verisi okuyacak
    şekilde değiştirin (ör. `pd.read_csv("data/yield_loss_history.csv")`).
    """
    rng = np.random.default_rng(seed)
    crop_sensitivity = {"domates": 1.0, "biber": 0.9, "salatalik": 1.1, "patates": 0.8, "bugday": 0.6}

    risk_score = rng.uniform(0, 1, n_samples)
    crop_type = rng.choice(KNOWN_CROPS, n_samples)
    sensitivity = np.array([crop_sensitivity[c] for c in crop_type])
    noise = rng.normal(0, 4, n_samples)

    yield_loss_pct = np.clip((risk_score ** 1.5) * 100 * sensitivity + noise, 0, 100)

    return pd.DataFrame({
        "risk_score": risk_score,
        "crop_type": crop_type,
        "yield_loss_pct": yield_loss_pct,
    })


def build_pipeline() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[("crop_ohe", OneHotEncoder(handle_unknown="ignore"), ["crop_type"])],
        remainder="passthrough",
    )
    return Pipeline(steps=[
        ("preprocess", preprocessor),
        ("regressor", GradientBoostingRegressor(n_estimators=150, max_depth=3, random_state=42)),
    ])


def main() -> None:
    settings = get_settings()
    df = _make_synthetic_dataset()

    X, y = df[["risk_score", "crop_type"]], df["yield_loss_pct"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    mae = mean_absolute_error(y_test, pipeline.predict(X_test))
    logger.info("Test MAE: %.2f puan (verim kaybı yüzdesi)", mae)

    settings.regression_artifact_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, settings.regression_artifact_path)
    logger.info("Model kaydedildi: %s", settings.regression_artifact_path)


if __name__ == "__main__":
    main()
