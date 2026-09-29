from __future__ import annotations

from app.config.settings import settings


def test_ai_fallback_message_is_available_when_no_api_key() -> None:
    if not settings.ai_available:
        assert "AI mode unavailable" in settings.ai_status_message
    else:
        assert settings.ai_status_message == ""
