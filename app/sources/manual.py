from __future__ import annotations

from abc import ABC, abstractmethod

from app.database.models import Job


class JobSource(ABC):
    @abstractmethod
    def search(self, query: str) -> list[Job]:
        raise NotImplementedError

    @abstractmethod
    def get_job(self, job_id: str) -> Job | None:
        raise NotImplementedError
