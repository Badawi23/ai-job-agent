from __future__ import annotations

import json
from pathlib import Path

from app.profiles.profile import ProfileManager


def test_profile_default_loads_valid_json() -> None:
    manager = ProfileManager(Path("app/profiles/profile.json"))
    profile = manager.load()
    assert "target_monthly_income" in profile
    assert "skills" in profile
    assert isinstance(profile["skills"], dict)


def test_profile_can_be_saved_and_reloaded(tmp_path) -> None:
    path = tmp_path / "profile.json"
    manager = ProfileManager(path)
    profile = {"target_monthly_income": 1200, "skills": {"STM32": 5}}
    saved = manager.save(profile)
    reloaded = manager.load()
    assert saved == profile
    assert reloaded == profile
