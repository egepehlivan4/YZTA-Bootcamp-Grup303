"""
FloraGuard — Hava Durumu Veri Kaynağı
LSTM modelinin girdisi olan zaman serisini üretir.

Sprint 2 durumu: Gerçek bir hava durumu API'si (ör. OpenWeather) henüz
entegre edilmedi; konum adına göre DETERMİNİSTİK sentetik bir seri üretilir
(aynı konum + aynı gün -> aynı seri) böylece demo/test tekrarlanabilir kalır.

TODO (Sprint 3): `generate_synthetic_series` çağrısını gerçek API istemcisiyle
değiştirin — imza (location, days) -> list[dict] aynı kalmalı ki LSTM/agent
katmanları hiç değişmeden çalışmaya devam etsin.
"""

from __future__ import annotations

import hashlib
from datetime import date


def generate_synthetic_series(location: str, days: int = 14) -> list[dict]:
    seed = int(hashlib.sha256(f"{location.lower()}-{date.today()}".encode()).hexdigest(), 16) % (2**32)
    rng_state = seed

    def _next() -> float:
        nonlocal rng_state
        rng_state = (rng_state * 1103515245 + 12345) % (2**31)
        return rng_state / (2**31)

    series = []
    for day_offset in range(-days + 1, 1):
        temperature_c = 15 + _next() * 20        # 15-35°C
        humidity_pct = 40 + _next() * 55          # %40-95
        rainfall_mm = _next() ** 3 * 30           # çoğunlukla düşük, ara sıra yüksek yağış
        series.append({
            "day_offset": day_offset,
            "temperature_c": round(temperature_c, 1),
            "humidity_pct": round(humidity_pct, 1),
            "rainfall_mm": round(rainfall_mm, 1),
        })
    return series
