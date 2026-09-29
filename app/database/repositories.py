from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import Base, Job, JobAnalysis, Skill


def init_database() -> None:
    Base.metadata.create_all(bind=SessionLocal.kw["bind"])


def upsert_job(job: Job) -> Job:
    with SessionLocal() as db:
        existing = db.scalar(select(Job).where(Job.fingerprint == job.fingerprint))
        if existing is not None:
            return existing
        db.add(job)
        db.commit()
        db.refresh(job)
        return job


def list_jobs(limit: int = 100) -> list[Job]:
    with SessionLocal() as db:
        return db.scalars(select(Job).order_by(Job.created_at.desc()).limit(limit)).all()


def get_job_by_id(job_id: int) -> Job | None:
    with SessionLocal() as db:
        return db.get(Job, job_id)


def save_analysis(job_id: int, analysis: dict[str, Any]) -> JobAnalysis:
    with SessionLocal() as db:
        record = JobAnalysis(job_id=job_id, **analysis)
        db.add(record)
        db.commit()
        db.refresh(record)
        return record


def list_skills() -> list[Skill]:
    with SessionLocal() as db:
        return db.scalars(select(Skill).order_by(Skill.name)).all()


def create_skill(skill: Skill) -> Skill:
    with SessionLocal() as db:
        db.add(skill)
        db.commit()
        db.refresh(skill)
        return skill
