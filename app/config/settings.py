from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseModel):
    project_name: str = "AI Job Opportunity Agent"
    database_url: str = Field(default="sqlite:///ai_job_agent.db")
    profile_path: str = str(PROJECT_ROOT / "app" / "profiles" / "profile.json")
    ai_classifier_model: str = os.getenv("AI_CLASSIFIER_MODEL", "gpt-4o-mini")
    ai_analysis_model: str = os.getenv("AI_ANALYSIS_MODEL", "gpt-4o")
    ai_proposal_model: str = os.getenv("AI_PROPOSAL_MODEL", "gpt-4o-mini")
    base_dir: str = str(PROJECT_ROOT)

    @property
    def ai_available(self) -> bool:
        return bool(os.getenv("OPENAI_API_KEY"))

    @property
    def ai_status_message(self) -> str:
        return "AI mode unavailable — using fallback analysis." if not self.ai_available else ""


settings = Settings()
