from __future__ import annotations

from app.sources.base import JobSource


class SearchEngineSource(JobSource):
    def search(self, query: str):
        return []

    def get_job(self, job_id: str):
        return None
