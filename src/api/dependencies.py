"""
FloraGuard — FastAPI Dependency Injection
Ağır nesneler (CNN/LSTM modelleri, regresyon pipeline'ı, LLM ajanı) uygulama
başlangıcında (`main.py::lifespan`) BİR KEZ oluşturulup `app.state` üzerinde
saklanır. Bu modüldeki fonksiyonlar, route handler'ların bu tekil örneklere
`Depends(...)` ile erişmesini sağlar — her istekte yeniden model yüklemeyi önler.
"""

from __future__ import annotations

from fastapi import Request

from src.agent.memory import FarmerMemory
from src.agent.orchestrator import OrchestratorService


def get_memory(request: Request) -> FarmerMemory:
    return request.app.state.memory


def get_orchestrator(request: Request) -> OrchestratorService:
    return request.app.state.orchestrator
