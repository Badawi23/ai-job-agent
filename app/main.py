from __future__ import annotations

from app.sources.base import JobSource


class UpworkAdapter(JobSource):
    def search(self, query: str):
        return []

    def get_job(self, job_id: str):
        return None


class FreelancerAdapter(JobSource):
    def search(self, query: str):
        return []

    def get_job(self, job_id: str):
        return None


class CompanyWebsiteAdapter(JobSource):
    def search(self, query: str):
        return []

    def get_job(self, job_id: str):
        return None
