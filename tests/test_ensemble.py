import pytest

from src.models.ensemble import EnsembleWeights, combine_risk_scores


def test_combine_risk_scores_weighted_average():
    weights = EnsembleWeights(w_cnn=0.6, w_lstm=0.4)
    result = combine_risk_scores(cnn_diseased_probability=0.8, lstm_risk_5d=0.2, weights=weights)

    assert result["risk_score"] == pytest.approx(0.6 * 0.8 + 0.4 * 0.2)
    assert result["cnn_component"] == 0.8
    assert result["lstm_component"] == 0.2


def test_ensemble_weights_must_sum_to_one():
    with pytest.raises(ValueError):
        EnsembleWeights(w_cnn=0.7, w_lstm=0.7)


@pytest.mark.parametrize("bad_value", [-0.1, 1.1])
def test_combine_risk_scores_rejects_out_of_range_inputs(bad_value):
    weights = EnsembleWeights(w_cnn=0.5, w_lstm=0.5)
    with pytest.raises(ValueError):
        combine_risk_scores(cnn_diseased_probability=bad_value, lstm_risk_5d=0.5, weights=weights)
