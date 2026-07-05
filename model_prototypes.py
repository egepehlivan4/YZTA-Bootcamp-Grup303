"""
FloraGuard — Model Prototipleri (Sprint 1)
PyTorch tabanlı, EĞİTİLMEMİŞ CNN ve LSTM iskeletleri.
Amaç: Mimari boyutlarının doğrulanması (dummy veriyle ileri besleme).
Sprint 2'de gerçek veri setleriyle eğitim yapılacaktır.

Çalıştırma:
    python src/model_prototypes.py
"""

import torch
import torch.nn as nn

# ---------------------------------------------------------------------------
# 1) CNN Prototipi — Yaprak görüntüsünden hastalık sınıflandırma
# ---------------------------------------------------------------------------

class LeafCNN(nn.Module):
    """
    Basit baseline CNN.
    Girdi:  (batch, 3, 128, 128) RGB yaprak görüntüsü
    Çıktı:  (batch, num_classes) sınıf logit'leri (ör. sağlıklı / hastalık A / hastalık B)

    Not: Sprint 2'de transfer learning (ResNet/EfficientNet) ile değiştirilmesi
    değerlendirilecektir; bu sınıf mimari doğrulama içindir.
    """

    def __init__(self, num_classes: int = 3):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),                # 128 -> 64
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),                # 64 -> 32
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),        # (batch, 64, 1, 1)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(x))


# ---------------------------------------------------------------------------
# 2) LSTM Prototipi — Zaman serisinden 5 günlük hastalık riski
# ---------------------------------------------------------------------------

class WeatherLSTM(nn.Module):
    """
    Basit baseline LSTM.
    Girdi:  (batch, seq_len, num_features)
            ör. son 14 günün [sıcaklık, nem, yağış] verisi -> num_features=3
    Çıktı:  (batch, 1) — 5 günlük hastalık riski (0-1 arası, sigmoid)
    """

    def __init__(self, num_features: int = 3, hidden_size: int = 32, num_layers: int = 1):
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
        _, (h_n, _) = self.lstm(x)      # h_n: (num_layers, batch, hidden)
        return self.head(h_n[-1])       # son katmanın gizli durumu


# ---------------------------------------------------------------------------
# 3) Ensemble taslağı — Sprint 2'de geliştirilecek
# ---------------------------------------------------------------------------

def naive_ensemble(cnn_logits: torch.Tensor, lstm_risk: torch.Tensor,
                   w_cnn: float = 0.5, w_lstm: float = 0.5) -> torch.Tensor:
    """
    Basit ağırlıklı ortalama ensemble (taslak).
    CNN logit'lerinden 'hastalıklı' olasılığı softmax ile alınır,
    LSTM risk skoru ile ağırlıklı ortalaması hesaplanır.
    """
    cnn_prob_diseased = torch.softmax(cnn_logits, dim=1)[:, 1:].sum(dim=1, keepdim=True)
    return w_cnn * cnn_prob_diseased + w_lstm * lstm_risk


# ---------------------------------------------------------------------------
# Dummy veri ile doğrulama
# ---------------------------------------------------------------------------

def run_smoke_test() -> None:
    """Her iki modelin dummy girdilerle çalıştığını (boyut uyumu) doğrular."""
    torch.manual_seed(42)

    # --- CNN ---
    cnn = LeafCNN(num_classes=3)
    dummy_images = torch.randn(4, 3, 128, 128)          # 4 adet sahte yaprak görüntüsü
    cnn_out = cnn(dummy_images)
    print(f"[CNN ] girdi {tuple(dummy_images.shape)} -> çıktı {tuple(cnn_out.shape)}")

    # --- LSTM ---
    lstm = WeatherLSTM(num_features=3)
    dummy_series = torch.randn(4, 14, 3)                # 4 örnek, 14 günlük, 3 özellik
    lstm_out = lstm(dummy_series)
    print(f"[LSTM] girdi {tuple(dummy_series.shape)} -> çıktı {tuple(lstm_out.shape)}")

    # --- Ensemble taslağı ---
    combined = naive_ensemble(cnn_out, lstm_out)
    print(f"[ENS ] birleşik risk skoru: {tuple(combined.shape)}")
    print(f"       örnek skorlar: {combined.squeeze(1).tolist()}")

    print("\n✅ Smoke test başarılı — mimariler dummy veriyle çalışıyor (modeller EĞİTİLMEMİŞTİR).")


if __name__ == "__main__":
    run_smoke_test()
