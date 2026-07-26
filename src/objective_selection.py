"""
objective_selection.py
Module 3: Analysis Objective Selection (Page 3)
"""

import streamlit as st

from src.theme import module_header

OBJECTIVES = [
    "Compare two groups",
    "Compare multiple groups",
    "Determine relationship between variables",
    "Compare before and after condition",
    "Test distribution pattern",
]


def render_page():
    module_header("MOD_01 / M3", "Analysis Objective Selection", "tell SIP what you're trying to find out")
    st.caption("Module 3 — Tell SIP what you're trying to find out.")

    if "df" not in st.session_state:
        st.warning("⚠️ Please upload a dataset first (Page 1).")
        return

    df = st.session_state["df"]
    numerical_cols = st.session_state.get("numerical_cols", [])
    categorical_cols = st.session_state.get("categorical_cols", [])

    if not numerical_cols:
        st.warning("⚠️ No numerical variables were detected. Please revisit Page 2 — Profiling.")
        return

    objective = st.radio("What type of analysis do you want to perform?", OBJECTIVES, index=None)

    if objective is None:
        st.info("Select an analysis objective to continue.")
        return

    st.session_state["analysis_objective"] = objective
    st.divider()

    if objective in ("Compare two groups", "Compare multiple groups"):
        st.subheader("Select Variables")
        if not categorical_cols:
            st.warning("⚠️ No categorical (grouping) variables detected in your dataset.")
            return
        group_col = st.selectbox("Grouping variable (categorical)", categorical_cols)
        value_col = st.selectbox("Value variable (numerical)", numerical_cols)

        n_groups = df[group_col].nunique(dropna=True) if group_col else 0
        if objective == "Compare two groups" and n_groups != 2:
            st.warning(
                f"⚠️ '{group_col}' has {n_groups} unique groups. "
                "'Compare two groups' expects exactly 2. Consider filtering the data or choosing "
                "'Compare multiple groups' instead."
            )
        if objective == "Compare multiple groups" and n_groups < 2:
            st.warning(f"⚠️ '{group_col}' needs at least 2 groups. It currently has {n_groups}.")

        st.session_state["group_col"] = group_col
        st.session_state["value_col"] = value_col
        st.caption(f"Groups detected in **{group_col}**: {sorted(df[group_col].dropna().unique().tolist())}")

    elif objective == "Determine relationship between variables":
        st.subheader("Select Variables")
        if len(numerical_cols) < 2:
            st.warning("⚠️ Need at least 2 numerical variables for a relationship analysis.")
            return
        value_col = st.selectbox("Variable A (numerical)", numerical_cols, key="rel_a")
        remaining = [c for c in numerical_cols if c != value_col]
        value_col_2 = st.selectbox("Variable B (numerical)", remaining, key="rel_b")
        st.session_state["value_col"] = value_col
        st.session_state["value_col_2"] = value_col_2

    elif objective == "Compare before and after condition":
        st.subheader("Select Variables")
        if len(numerical_cols) < 2:
            st.warning("⚠️ Need at least 2 numerical columns representing 'before' and 'after' measurements.")
            return
        before_col = st.selectbox("Before condition (numerical)", numerical_cols, key="before")
        remaining = [c for c in numerical_cols if c != before_col]
        after_col = st.selectbox("After condition (numerical)", remaining, key="after")
        st.session_state["before_col"] = before_col
        st.session_state["after_col"] = after_col

    elif objective == "Test distribution pattern":
        st.subheader("Select Variable")
        value_col = st.selectbox("Numerical variable to test", numerical_cols)
        st.session_state["value_col"] = value_col

    st.success(f"✅ Objective set: **{objective}**")
    st.info("Proceed to **Assumption Checking** in the sidebar to continue.")
