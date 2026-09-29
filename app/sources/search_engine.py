from __future__ import annotations

from app.database.models import Job
from app.sources.base import JobSource


class ManualSource(JobSource):
    def search(self, query: str) -> list[Job]:
        return []

    def get_job(self, job_id: str) -> Job | None:
        return None

    def create_job_from_payload(self, payload: dict) -> Job:
        return Job(
            source="manual",
            source_job_id=str(payload.get("source_job_id") or payload.get("title", "manual-job")),
            title=payload["title"],
            description=payload.get("description", ""),
            url=payload.get("url"),
            client_name=payload.get("client_name"),
            currency=payload.get("currency", "EUR"),
            budget_min=float(payload["budget_min"]) if payload.get("budget_min") is not None else None,
            budget_max=float(payload["budget_max"]) if payload.get("budget_max") is not None else None,
            remote=bool(payload.get("remote", True)),
            job_type=payload.get("job_type"),
            experience_level=payload.get("experience_level"),
            raw_data=payload,
        )
