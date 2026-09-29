from __future__ import annotations

import json

import streamlit as st

from app.profiles.profile import load_profile, save_profile


def render_settings_panel() -> None:
    st.subheader("Settings")
    profile = load_profile()
    with st.form("settings_form"):
        target_income = st.number_input("Target monthly income (€)", min_value=0, value=int(profile.get("target_monthly_income", 1000)))
        min_project_price = st.number_input("Minimum project price (€)", min_value=0, value=int(profile.get("minimum_project_price", 150)))
        max_duration = st.number_input("Max project duration (days)", min_value=1, value=int(profile.get("max_project_duration_days", 14)))
        submitted = st.form_submit_button("Save settings")
        if submitted:
            profile["target_monthly_income"] = target_income
            profile["minimum_project_price"] = min_project_price
            profile["max_project_duration_days"] = max_duration
            save_profile(profile)
            st.success("Settings saved.")
