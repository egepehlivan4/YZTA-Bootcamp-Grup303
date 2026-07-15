from src.models.regression import YieldLossRegressor


def test_heuristic_fallback_used_when_no_artifact(tmp_path):
    regressor = YieldLossRegressor(artifact_path=tmp_path / "does_not_exist.joblib")

    assert regressor.is_trained_model_loaded is False

    result = regressor.predict(risk_score=0.8, crop_type="domates")
    assert result["model_used"] == "heuristic-fallback"
    assert 0.0 <= result["estimated_yield_loss_pct"] <= 100.0


def test_higher_risk_never_yields_lower_loss(tmp_path):
    regressor = YieldLossRegressor(artifact_path=tmp_path / "does_not_exist.joblib")

    low_risk = regressor.predict(risk_score=0.1, crop_type="domates")
    high_risk = regressor.predict(risk_score=0.9, crop_type="domates")

    assert high_risk["estimated_yield_loss_pct"] > low_risk["estimated_yield_loss_pct"]


def test_unknown_crop_type_falls_back_gracefully(tmp_path):
    regressor = YieldLossRegressor(artifact_path=tmp_path / "does_not_exist.joblib")
    result = regressor.predict(risk_score=0.5, crop_type="uzay-domatesi")
    assert 0.0 <= result["estimated_yield_loss_pct"] <= 100.0
