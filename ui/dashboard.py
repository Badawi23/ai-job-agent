from __future__ import annotations

import streamlit as st

from app.profiles.profile import load_profile, save_profile


def render_profile_editor() -> None:
    st.subheader("Editable Profile")
    profile = load_profile()
    skills = profile.get("skills", {})

    with st.form("profile_editor_form"):
        profile["target_monthly_income"] = st.number_input("Target monthly income (€)", value=int(profile.get("target_monthly_income", 1000)))
        profile["minimum_project_price"] = st.number_input("Minimum project price (€)", value=int(profile.get("minimum_project_price", 150)))
        profile["ideal_project_price_min"] = st.number_input("Ideal project price min (€)", value=int(profile.get("ideal_project_price_min", 200)))
        profile["ideal_project_price_max"] = st.number_input("Ideal project price max (€)", value=int(profile.get("ideal_project_price_max", 600)))
        profile["max_project_duration_days"] = st.number_input("Max project duration (days)", value=int(profile.get("max_project_duration_days", 14)))
        profile["languages"] = st.multiselect("Languages", ["English", "German", "Arabic", "French", "Spanish"], default=profile.get("languages", ["English", "German", "Arabic"]))

        skill_editor = {}
        for name, level in skills.items():
            skill_editor[name] = st.slider(f"{name}", 1, 5, int(level))
        profile["skills"] = skill_editor

        submitted = st.form_submit_button("Save profile")
        if submitted:
            save_profile(profile)
            st.success("Profile updated successfully.")
