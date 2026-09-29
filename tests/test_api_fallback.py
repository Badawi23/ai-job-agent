from __future__ import annotations

from app.database.init_db import fingerprint_for_job, normalize_text


def test_normalization_removes_case_and_spacing_noise() -> None:
    text = "  Embedded   C   Firmware   "
    assert normalize_text(text) == "embedded c firmware"


def test_fingerprint_is_stable_for_same_job() -> None:
    first = fingerprint_for_job("STM32 Firmware", "Acme Labs", "Need UART debugging")
    second = fingerprint_for_job("STM32 Firmware", "Acme Labs", "Need UART debugging")
    assert first == second
