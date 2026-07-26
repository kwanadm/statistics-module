"""
Statistical Intelligence Platform (SIP)
Automated Statistical Analysis and Decision Support System — Phase 1

Entry point: sidebar navigation across the 6 core pages. Session state
(`st.session_state`) is used throughout so the uploaded dataset and derived
results persist as the user moves between pages without needing to re-upload.
"""

import streamlit as st

from src import data_handler, profiling, objective_selection, assumptions, hypothesis_page, report
from src.theme import apply_theme

st.set_page_config(
    page_title="MOD_01 — Hypothesis Testing",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

PAGES = {
    "1. Data Upload & Preview": data_handler,
    "2. Dataset Profiling & Outliers": profiling,
    "3. Analysis Objective Selection": objective_selection,
    "4. Assumption Checking": assumptions,
    "5. Hypothesis Testing & Post-Hoc Result": hypothesis_page,
    "6. Report Export": report,
}


def main():
    with st.sidebar:
        st.markdown(
            '<span class="mod-tag">MOD_01 (ACTIVE)</span>',
            unsafe_allow_html=True,
        )
        st.title("📊 SIP")
        st.caption("Statistical Intelligence Platform")
        st.divider()
        selected_page = st.radio("Navigate", list(PAGES.keys()), label_visibility="collapsed")
        st.divider()

        if "dataset_name" in st.session_state:
            st.success(f"Active dataset:\n**{st.session_state['dataset_name']}**")
        else:
            st.info("No dataset loaded yet.")

        st.caption("Phase 1 — Automated Hypothesis Testing Engine")

    PAGES[selected_page].render_page()


if __name__ == "__main__":
    main()
