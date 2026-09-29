from __future__ import annotations

from app.database.init_db import score_opportunity


def test_score_opportunity_is_capped_between_zero_and_hundred() -> None:
    score = score_opportunity(100, 90, 100, 100, 100, 90, 0)
    assert 0 <= score <= 100

    low_score = score_opportunity(0, 0, 0, 0, 0, 0, 50)
    assert low_score == 0
