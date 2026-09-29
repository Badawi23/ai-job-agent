from __future__ import annotations

from datetime import datetime

import streamlit as st

from app.database.database import SessionLocal
from app.database.models import Job
from app.database.repositories import list_jobs
from app.profiles.profile import load_profile
from app.profiles.profile import save_profile
from app.sources.manual import ManualSource
from app.database.init_db import fingerprint_for_job
from app.database.repositories import init_db
from app.database.models import Base


st.set_page_config(page_title="AI Opportunity Agent", page_icon="💼", layout="wide")


def _metric_card(title: str, value: str, delta: str | None = None) -> None:
    st.markdown(f"<div style='padding:12px;border:1px solid #e5e5e5;border-radius:8px;background:#0f172a;color:#f8fafc'><div style='font-size:12px;color:#94a3b8'>{title}</div><div style='font-size:28px;font-weight:700'>{value}</div>{f'<div style="font-size:12px;color:#a5f3fc">{delta}</div>' if delta else ''}</div>", unsafe_allow_html=True)


def _empty_placeholder() -> None:
    st.info("No jobs loaded yet. Use the manual job entry form to create your first opportunity.")


def main() -> None:
    init_db()
    profile = load_profile()
    st.title("AI OPPORTUNITY AGENT")
    st.caption("Human-in-the-loop project discovery and evaluation")

    target = profile.get("target_monthly_income", 1000)
    current = 650
    progress = round((current / target) * 100)

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Monthly target", f"€{target}")
    col_b.metric("Current", f"€{current}")
    col_c.metric("Progress", f"{progress}%")

    jobs = list_jobs(limit=20)
    total_jobs = len(jobs)
    relevant_jobs = sum(1 for job in jobs if job.budget_min or job.budget_max)
    average_budget = round(sum((job.budget_min or 0) for job in jobs) / max(1, total_jobs), 2)

    kpi_cols = st.columns(6)
    with kpi_cols[0]:
        _metric_card("Jobs scanned", str(total_jobs), "")
    with kpi_cols[1]:
        _metric_card("Relevant jobs", str(relevant_jobs), "")
    with kpi_cols[2]:
        _metric_card("Applications", "0", "")
    with kpi_cols[3]:
        _metric_card("Interviews", "0", "")
    with kpi_cols[4]:
        _metric_card("Projects won", "0", "")
    with kpi_cols[5]:
        _metric_card("Revenue", f"€{current}", "")

    st.markdown("---")

    manual_source = ManualSource()
    with st.expander("Manual job entry", expanded=True):
        with st.form("manual_job_form"):
            title = st.text_input("Job title")
            description = st.text_area("Description")
            client_name = st.text_input("Client")
            url = st.text_input("URL")
            budget_min = st.number_input("Budget min (€)", value=0.0, min_value=0.0, step=50.0)
            budget_max = st.number_input("Budget max (€)", value=0.0, min_value=0.0, step=50.0)
            remote = st.checkbox("Remote-friendly", value=True)
            job_type = st.selectbox("Project type", ["Freelance", "Contract", "Retainer", "Consulting"])
            submitted = st.form_submit_button("Add job")
            if submitted and title and description:
                payload = {
                    "title": title,
                    "description": description,
                    "client_name": client_name,
                    "url": url,
                    "budget_min": budget_min,
                    "budget_max": budget_max,
                    "remote": remote,
                    "job_type": job_type,
                    "experience_level": "mid",
                    "source_job_id": f"manual-{datetime.utcnow().timestamp()}",
                }
                with SessionLocal() as db:
                    job = manual_source.create_job_from_payload(payload)
                    job.fingerprint = fingerprint_for_job(job.title, job.client_name, job.description)
                    existing = db.query(Job).filter(Job.fingerprint == job.fingerprint).first()
                    if existing is None:
                        db.add(job)
                        db.commit()
                        st.success("Manual job added to the dashboard.")
                    else:
                        st.warning("This job already exists in the database.")

    st.subheader("Opportunities")
    if not jobs:
        _empty_placeholder()
    else:
        job_rows = []
        for job in jobs:
            suggested_value = (job.budget_min or job.budget_max or 0) or 0
            job_rows.append(
                {
                    "Score": 85,
                    "Title": job.title,
                    "Budget": f"€{int(suggested_value)}",
                    "Hours": "10-20",
                    "€/hour": "€35-50",
                    "Technical match": "High",
                    "Risk": "Low",
                    "Source": job.source,
                    "Date": job.created_at.strftime("%Y-%m-%d") if job.created_at else "N/A",
                }
            )
        st.dataframe(job_rows, use_container_width=True)

    st.markdown("---")
    st.subheader("Profile Summary")
    st.json(profile)


if __name__ == "__main__":
    main()
