import pytest

from src.agent.memory import FarmerMemory


def test_add_and_read_history(tmp_path):
    memory = FarmerMemory(db_path=tmp_path / "test.db")

    memory.add_record(
        farmer_id="ciftci1", crop_type="domates", location="Antalya",
        disease_probability=0.72, estimated_yield_loss_pct=18.5, advice="Sulamayı azaltın.",
    )

    history = memory.get_recent_history("ciftci1")
    assert len(history) == 1
    assert history[0]["disease_probability"] == 0.72
    assert history[0]["crop_type"] == "domates"


def test_summarize_for_agent_handles_empty_history(tmp_path):
    memory = FarmerMemory(db_path=tmp_path / "test.db")
    summary = memory.summarize_for_agent("bilinmeyen-ciftci")
    assert "bulunamadı" in summary


def test_history_ordered_most_recent_first(tmp_path):
    memory = FarmerMemory(db_path=tmp_path / "test.db")
    for i in range(3):
        memory.add_record(
            farmer_id="ciftci1", crop_type="domates", location="Antalya",
            disease_probability=0.1 * i, estimated_yield_loss_pct=1.0 * i,
        )

    history = memory.get_recent_history("ciftci1", limit=10)
    assert len(history) == 3
    assert history[0]["disease_probability"] == pytest.approx(0.2)
