from __future__ import annotations

from app.database.init_db import calculate_hourly_rate, parse_budget


def test_parse_budget_handles_single_and_range_values() -> None:
    lower, upper = parse_budget("€300-€400")
    assert lower == 300.0
    assert upper == 400.0

    single = parse_budget("€250")
    assert single == (250.0, 250.0)


def test_hourly_rate_calculation() -> None:
    rate = calculate_hourly_rate(350, 10)
    assert rate == 35.0
