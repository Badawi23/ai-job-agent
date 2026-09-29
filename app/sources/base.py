from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.config.settings import settings


class ProfileManager:
    def __init__(self, profile_path: str | Path | None = None) -> None:
        self.profile_path = Path(profile_path or settings.profile_path)
        self.profile_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, Any]:
        if not self.profile_path.exists():
            return self._default_profile()
        with self.profile_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def save(self, profile: dict[str, Any]) -> dict[str, Any]:
        self.profile_path.write_text(json.dumps(profile, indent=2), encoding="utf-8")
        return profile

    def update(self, **kwargs: Any) -> dict[str, Any]:
        profile = self.load()
        profile.update(kwargs)
        return self.save(profile)

    @staticmethod
    def _default_profile() -> dict[str, Any]:
        return {
            "target_monthly_income": 1000,
            "minimum_project_price": 150,
            "ideal_project_price_min": 200,
            "ideal_project_price_max": 600,
            "max_project_duration_days": 14,
            "languages": ["English", "German", "Arabic"],
            "skills": {
                "Embedded C": 5,
                "STM32": 4,
                "PIC18": 5,
                "UART": 5,
                "I2C": 5,
                "SPI": 4,
                "Python": 3,
                "Git": 4,
                "Firmware": 5,
                "Technical Documentation": 4,
            },
        }


profile_manager = ProfileManager()


def load_profile() -> dict[str, Any]:
    return profile_manager.load()


def save_profile(profile: dict[str, Any]) -> dict[str, Any]:
    return profile_manager.save(profile)
