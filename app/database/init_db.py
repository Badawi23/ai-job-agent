from __future__ import annotations

from app.database.database import SessionLocal
from app.database.models import Base, Job


def init_db() -> None:
    Base.metadata.create_all(bind=SessionLocal.kw["bind"])
