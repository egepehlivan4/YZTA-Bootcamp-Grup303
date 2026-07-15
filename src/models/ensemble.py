"""
FloraGuard — Ensemble Katmanı
CNN (görüntü) ve LSTM (zaman serisi) çıktılarını tek bir risk skorunda birleştirir.
Bu skor, regresyon modülünün girdisi ve agent'ın tavsiye ürettiği ana sinyaldir.

Neden ağırlıklı ortalama (ve neden burada durur)?
İki farklı modalitenin olasılık çıktısını birleştirmenin en yorumlanabilir yolu
ağırlıklı ortalamadır — çiftçiye/danışmana "%55 görüntü + %45 hava durumu" gibi
açıklanabilir bir gerekçe sunar. Sprint 3'te stacking/meta-learner değerlendirilebilir,
ama şimdilik yorumlanabilirlik doğruluktan daha değerli (bootcamp MVP önceliği).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EnsembleWeights:
    w_cnn: float
    w_lstm: float

    def __post_init__(self):
        total = self.w_cnn + self.w_lstm
        if not 0.99 <= total <= 1.01:
            raise ValueError(f"Ensemble ağırlıkları 1.0'a toplanmalı, toplam={total}")


def combine_risk_scores(
    cnn_diseased_probability: float,
    lstm_risk_5d: float,
    weights: EnsembleWeights,
) -> dict:
    """
    İki modelin 0-1 aralığındaki olasılık/risk çıktısını ağırlıklı ortalamayla birleştirir.

    Args:
        cnn_diseased_probability: CNNPredictor.predict(...)["diseased_probability"]
        lstm_risk_5d: LSTMPredictor.predict(...)["risk_5d"]
        weights: EnsembleWeights(w_cnn, w_lstm)

    Returns:
        EnsembleResult şemasıyla uyumlu dict.
    """
    for name, value in (("cnn_diseased_probability", cnn_diseased_probability), ("lstm_risk_5d", lstm_risk_5d)):
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} 0-1 aralığında olmalı, gelen değer: {value}")

    risk_score = weights.w_cnn * cnn_diseased_probability + weights.w_lstm * lstm_risk_5d

    return {
        "risk_score": round(risk_score, 4),
        "cnn_component": round(cnn_diseased_probability, 4),
        "lstm_component": round(lstm_risk_5d, 4),
        "w_cnn": weights.w_cnn,
        "w_lstm": weights.w_lstm,
    }
