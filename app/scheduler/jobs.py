from __future__ import annotations

from fastapi import FastAPI

from app.config.settings import settings
from app.database.init_db import init_db
from app.profiles.profile import load_profile

app = FastAPI(title=settings.project_name)


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.project_name}


@app.get("/api/profile")
def get_profile() -> dict:
    return load_profile()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
