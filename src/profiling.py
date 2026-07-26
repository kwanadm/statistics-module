"""
profiling.py
Module 2: Automated Data Profiling & Outlier Detection (Page 2)
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from src.utils import detect_variable_types, iqr_outlier_scan
from src.theme import module_header


def render_page():
    module_header("MOD_01 / M2", "Dataset Profiling &amp; Outliers", "structural profiling + IQR outlier scan")
    st.caption("Module 2 — Structural profiling and IQR-based outlier detection.")

    if "df" not in st.session_state:
        st.warning("⚠️ Please upload a dataset first (Page 1).")
        return

    df = st.session_state["df"]

    # --- Dataset Information ---
    st.subheader("Dataset Information")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{df.shape[0]:,}")
    c2.metric("Columns", f"{df.shape[1]:,}")
    c3.metric("Missing Values", f"{int(df.isna().sum().sum()):,}")
    c4.metric("Duplicate Rows", f"{int(df.duplicated().sum()):,}")

    with st.expander("Column Data Types"):
        dtype_df = pd.DataFrame({
            "Column": df.columns,
            "Data Type": [str(t) for t in df.dtypes],
            "Missing": df.isna().sum().values,
            "Missing %": (df.isna().sum().values / len(df) * 100).round(2) if len(df) else 0,
        })
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    # --- Variable Detection ---
    numerical_cols, categorical_cols = detect_variable_types(df)
    st.session_state["numerical_cols"] = numerical_cols
    st.session_state["categorical_cols"] = categorical_cols

    st.subheader("Detected Variable Types")
    vcol1, vcol2 = st.columns(2)
    with vcol1:
        st.markdown("**🔢 Numerical Variables**")
        st.write(numerical_cols if numerical_cols else "None detected")
    with vcol2:
        st.markdown("**🏷️ Categorical Variables**")
        st.write(categorical_cols if categorical_cols else "None detected")

    if not numerical_cols:
        st.warning("No numerical variables detected — most hypothesis tests require at least one numerical variable.")

    # --- Outlier Detection ---
    st.subheader("Outlier Detection (IQR Method)")
    if numerical_cols:
        outlier_summary, outlier_masks = iqr_outlier_scan(df, numerical_cols)
        st.session_state["outlier_summary"] = outlier_summary
        st.session_state["outlier_masks"] = outlier_masks

        st.dataframe(outlier_summary, use_container_width=True, hide_index=True)

        severe_cols = outlier_summary[outlier_summary["Severity"].isin(["Moderate", "Severe"])]
        if not severe_cols.empty:
            st.warning(
                f"⚠️ Severe/Moderate outliers detected in: **{', '.join(severe_cols['Variable'].tolist())}**. "
                "This will influence test recommendations later (favoring non-parametric methods)."
            )
        else:
            st.success("✅ No severe outlier contamination detected in numerical variables.")

        st.markdown("#### Exploratory Visuals")
        selected_var = st.selectbox("Select a numerical variable to visualize", numerical_cols)
        if selected_var:
            col_a, col_b = st.columns(2)
            with col_a:
                fig_box = px.box(df, y=selected_var, points="outliers", title=f"Boxplot — {selected_var}")
                st.plotly_chart(fig_box, use_container_width=True)
            with col_b:
                fig_density = px.histogram(
                    df, x=selected_var, marginal="rug", histnorm="probability density",
                    title=f"Density — {selected_var}"
                )
                st.plotly_chart(fig_density, use_container_width=True)
    else:
        st.info("No numerical variables available for outlier scanning.")

    st.info("Proceed to **Analysis Objective Selection** in the sidebar to continue.")
