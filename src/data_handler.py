"""
data_handler.py
Module 1: Data Ingestion & State Management (Page 1)
"""

import streamlit as st
import pandas as pd

from src.theme import module_header

SUPPORTED_TYPES = ["csv", "xlsx"]


def _reset_downstream_state():
    """Clear any results computed from a previous dataset when a new file is loaded."""
    keys_to_clear = [
        "numerical_cols", "categorical_cols", "outlier_summary", "outlier_masks",
        "analysis_objective", "group_col", "value_col", "value_col_2",
        "before_col", "after_col", "normality_results", "homogeneity_results",
        "test_recommendation", "test_results", "posthoc_results",
        "interpretation", "report_ready",
    ]
    for k in keys_to_clear:
        if k in st.session_state:
            del st.session_state[k]


def render_page():
    module_header("MOD_01", "Data Upload &amp; Preview", "secure local file ingestion")
    st.caption("Module 1 — Secure local file ingestion with in-memory state management.")

    uploaded_file = st.file_uploader(
        "Drag and drop your dataset here (CSV or Excel)",
        type=SUPPORTED_TYPES,
        help="Your file is processed in-memory for this session only and is not stored permanently.",
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.lower().endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            if df.empty:
                st.error("⚠️ The uploaded file is empty. Please upload a valid dataset.")
                return

            if df.shape[1] == 0:
                st.error("⚠️ No columns detected. The file may be corrupted or in the wrong format.")
                return

            # Only reset downstream state if this is actually a new file
            is_new_file = (
                "dataset_name" not in st.session_state
                or st.session_state.get("dataset_name") != uploaded_file.name
                or st.session_state.get("_df_shape") != df.shape
            )
            if is_new_file:
                _reset_downstream_state()

            st.session_state["df"] = df
            st.session_state["dataset_name"] = uploaded_file.name
            st.session_state["_df_shape"] = df.shape

            st.success(f"✅ Dataset **{uploaded_file.name}** loaded successfully.")

        except pd.errors.EmptyDataError:
            st.error("⚠️ The file appears to be empty or unreadable.")
            return
        except pd.errors.ParserError:
            st.error("⚠️ Could not parse the file. Please check the file format and try again.")
            return
        except Exception as e:
            st.error(f"⚠️ An unexpected error occurred while reading the file: {e}")
            return

    if "df" in st.session_state:
        df = st.session_state["df"]
        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric("Dataset Name", st.session_state["dataset_name"])
        col2.metric("Number of Rows", f"{df.shape[0]:,}")
        col3.metric("Number of Columns", f"{df.shape[1]:,}")

        st.subheader("Preview — First 10 Rows")
        st.dataframe(df.head(10), use_container_width=True)

        st.info("Proceed to **Dataset Profiling & Outliers** in the sidebar to continue.")
    else:
        st.info("👆 Upload a CSV or Excel file to begin your analysis.")
