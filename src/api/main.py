"""
FloraGuard — FastAPI Uygulama Girişi
Tüm katmanları (models, agent, security) birleştirip HTTP üzerinden dışa açar.
Ağır nesneler (modeller, LLM ajanı) `lifespan` içinde BİR KEZ oluşturulup
`app.state`'e yazılır (bkz. api/dependencies.py).

Çalıştırma:
    uvicorn src.api.main:app --reload
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.agent.memory import FarmerMemory
from src.agent.orchestrator import OrchestratorService
from src.api.routes import auth, history, predict, weather
from src.config import get_settings
from src.models.cnn_model import CNNPredictor
from src.models.lstm_model import LSTMPredictor
from src.models.regression import YieldLossRegressor
from src.security.users_db import init_users_table, seed_demo_users

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info("FloraGuard API başlatılıyor (ortam: %s)...", settings.environment)

    init_users_table(settings.db_path)
    seed_demo_users(settings.db_path)

    memory = FarmerMemory(settings.db_path)
    cnn_predictor = CNNPredictor(settings.cnn_num_classes, settings.cnn_class_names, settings.cnn_weights_path)
    lstm_predictor = LSTMPredictor(settings.lstm_weights_path)
    regressor = YieldLossRegressor(settings.regression_artifact_path)

    app.state.memory = memory
    app.state.orchestrator = OrchestratorService(settings, cnn_predictor, lstm_predictor, regressor, memory)

    logger.info("FloraGuard API hazır.")
    yield
    logger.info("FloraGuard API kapatılıyor.")


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        description="Bitki hastalığı tahmin sistemi — tahmine dayalı karar destek API'si",
        version=settings.app_version,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_allow_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(predict.router)
    app.include_router(history.router)
    app.include_router(weather.router)

    @app.get("/health", tags=["health"])
    def health_check() -> dict:
        return {"status": "ok", "service": "floraguard-api", "version": settings.app_version}

    return app


app = create_app()
