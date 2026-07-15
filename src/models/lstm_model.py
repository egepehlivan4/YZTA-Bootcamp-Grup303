"""
FloraGuard — LSTM Modülü (Hava/Nem Zaman Serisi)
Sprint 1'deki `model_prototypes.py::WeatherLSTM` mimarisi buraya taşındı ve
`LSTMPredictor` inference sarmalayıcısı ile üretim kullanımı için hazırlandı.
"""

from __future__ import annotations

import logging
from pathlib import Path

import torch
import torch.nn as nn

logger = logging.getLogger(__name__)

NUM_FEATURES = 3  # [sıcaklık, nem, yağış]


class WeatherLSTM(nn.Module):
    """
    Baseline LSTM. Girdi: (batch, seq_len, 3) — son N günün [sıcaklık, nem, yağış] verisi.
    Çıktı: (batch, 1) — 5 günlük hastalık riski (0-1 arası, sigmoid).
    """

    def __init__(self, num_features: int = NUM_FEATURES, hidden_size: int = 32, num_layers: int = 1):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=num_features,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
        )
        self.head = nn.Sequential(
            nn.Linear(hidden_size, 1),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        _, (h_n, _) = self.lstm(x)
        return self.head(h_n[-1])


class LSTMPredictor:
    """Zaman serisi ön-işleme + model çıkarımını tek arayüzde toplar."""

    def __init__(self, weights_path: Path | None = None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = WeatherLSTM(num_features=NUM_FEATURES).to(self.device)

        if weights_path and weights_path.exists():
            state_dict = torch.load(weights_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
            logger.info("LSTM ağırlıkları yüklendi: %s", weights_path)
        else:
            logger.warning(
                "LSTM ağırlık dosyası bulunamadı (%s) — model EĞİTİLMEMİŞ rastgele "
                "ağırlıklarla çalışıyor.",
                weights_path,
            )
        self.model.eval()

    @torch.inference_mode()
    def predict(self, series: list[dict]) -> dict:
        """
        `series`: [{"temperature_c": .., "humidity_pct": .., "rainfall_mm": ..}, ...]
        En az 1 gün gerekir; öneri: son 14 gün.
        """
        if not series:
            raise ValueError("LSTM için boş zaman serisi geçilemez.")

        rows = [
            [point["temperature_c"], point["humidity_pct"], point["rainfall_mm"]]
            for point in series
        ]
        tensor = torch.tensor([rows], dtype=torch.float32, device=self.device)  # (1, seq_len, 3)

        risk = self.model(tensor).squeeze().item()
        return {"risk_5d": round(float(risk), 4)}
