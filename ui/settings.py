from __future__ import annotations

import streamlit as st


def render_sidebar() -> None:
    st.sidebar.title("AI Opportunity Agent")
    st.sidebar.caption("Human-in-the-loop freelance sourcing")
    st.sidebar.page_link("ui/dashboard.py", label="Dashboard")
