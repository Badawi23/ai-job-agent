from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Float, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from app.config.settings import settings


class Base(DeclarativeBase):
    pass


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    source: Mapped[str] = mapped_column(String(64), default="manual")
    source_job_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    client_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    client_country: Mapped[str | None] = mapped_column(String(80), nullable=True)
    job_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    budget_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    budget_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    currency: Mapped[str | None] = mapped_column(String(10), default="EUR")
    hourly_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    hourly_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    experience_level: Mapped[str | None] = mapped_column(String(80), nullable=True)
    remote: Mapped[bool] = mapped_column(Boolean, default=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    deadline: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    raw_data: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    fingerprint: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class JobAnalysis(Base):
    __tablename__ = "job_analyses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    job_id: Mapped[int] = mapped_column(nullable=False, index=True)
    relevant: Mapped[bool] = mapped_column(Boolean, default=False)
    relevance_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    technical_match: Mapped[float | None] = mapped_column(Float, nullable=True)
    skill_match: Mapped[float | None] = mapped_column(Float, nullable=True)
    difficulty: Mapped[str | None] = mapped_column(String(100), nullable=True)
    estimated_hours_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    estimated_hours_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    estimated_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    suggested_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    minimum_acceptable_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    client_quality: Mapped[float | None] = mapped_column(Float, nullable=True)
    competition: Mapped[float | None] = mapped_column(Float, nullable=True)
    risk: Mapped[float | None] = mapped_column(Float, nullable=True)
    scam_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    recommendation: Mapped[str | None] = mapped_column(String(50), nullable=True)
    reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)
    matching_skills: Mapped[str | None] = mapped_column(Text, nullable=True)
    missing_skills: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    category: Mapped[str | None] = mapped_column(String(120), nullable=True)
    level: Mapped[int | None] = mapped_column(nullable=True)
    years_experience: Mapped[float | None] = mapped_column(Float, nullable=True)
    evidence: Mapped[str | None] = mapped_column(Text, nullable=True)
    preferred: Mapped[bool] = mapped_column(Boolean, default=False)


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    job_id: Mapped[int] = mapped_column(nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="NEW")
    proposed_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    estimated_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    proposal: Mapped[str | None] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    response_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    result: Mapped[str | None] = mapped_column(String(50), nullable=True)
    revenue: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    job_id: Mapped[int] = mapped_column(nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(50), default="ignore")
    reason: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


if settings.database_url.startswith("sqlite"):
    engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
else:
    engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
