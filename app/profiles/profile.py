from __future__ import annotations

import hashlib
import re
from datetime import datetime
from typing import Any


def normalize_text(value: str | None) -> str:
    if value is None:
        return ""
    normalized = re.sub(r"\s+", " ", value.strip().lower())
    return normalized


def fingerprint_for_job(title: str | None, client: str | None, description: str | None) -> str:
    raw = "|".join(
        [
            normalize_text(title),
            normalize_text(client),
            normalize_text(description),
        ]
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def parse_budget(value: Any) -> tuple[float | None, float | None]:
    if value is None:
        return None, None
    if isinstance(value, (int, float)):
        return float(value), float(value)
    if isinstance(value, str):
        digits = re.findall(r"\d+(?:\.\d+)?", value)
        if not digits:
            return None, None
        numbers = [float(d) for d in digits]
        if len(numbers) == 1:
            return numbers[0], numbers[0]
        return min(numbers), max(numbers)
    return None, None


def calculate_hourly_rate(suggested_price: float | None, estimated_hours: float | None) -> float | None:
    if suggested_price is None or estimated_hours in (None, 0):
        return None
    return suggested_price / estimated_hours


def score_opportunity(technical_match: float, skill_match: float, project_value: float, hourly_rate: float, clarity: float, client_quality: float, risk_penalty: float) -> float:
    weighted = (
        0.30 * technical_match
        + 0.20 * skill_match
        + 0.15 * project_value
        + 0.15 * hourly_rate
        + 0.10 * clarity
        + 0.10 * client_quality
        - risk_penalty
    )
    return max(0.0, min(100.0, weighted))


def project_category_from_text(text: str) -> str:
    lowered = text.lower()
    if "stm32" in lowered or "microcontroller" in lowered:
        return "Embedded / Firmware"
    if "python" in lowered and ("uart" in lowered or "serial" in lowered):
        return "UART / Python"
    if "documentation" in lowered:
        return "Documentation"
    if "automation" in lowered:
        return "Automation"
    return "General Engineering"


def project_progress(current_value: float, target_value: float) -> float:
    return min(100.0, (current_value / target_value) * 100) if target_value else 0.0
