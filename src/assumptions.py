"""
assumptions.py
Module 4: Normality Testing Engine
Module 5: Homogeneity of Variance Test
(Page 4)
"""

import streamlit as st
import numpy as np
import pandas as pd
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go

from src.utils import p_value_badge, safe_round
from src.theme import module_header


def _run_normality_tests(series: pd.Series, label: str):
    series = series.dropna()
    result = {"Group": label, "n": len(series)}
    if len(series) < 3:
        result["Shapiro-Wilk p"] = np.nan
        result["Anderson-Darling Stat"] = np.nan
        result["Normal?"] = "N/A (n < 3)"
        return result, series

    # Shapiro-Wilk (works best for n < ~5000)
    try:
        sample = series if len(series) <= 5000 else series.sample(5000, random_state=42)
        shapiro_stat, shapiro_p = stats.shapiro(sample)
    except Exception:
        shapiro_p = np.nan

    # Anderson-Darling
    try:
        ad_result = stats.anderson(series, dist="norm")
        ad_stat = ad_result.statistic
        # Compare against the 5% significance level critical value
        crit_5pct = ad_result.critical_values[2] if len(ad_result.critical_values) > 2 else ad_result.critical_values[-1]
        ad_normal = ad_stat < crit_5pct
    except Exception:
        ad_stat = np.nan
        ad_normal = None

    result["Shapiro-Wilk p"] = safe_round(shapiro_p)
    result["Anderson-Darling Stat"] = safe_round(ad_stat)
    result["Normal?"] = p_value_badge(shapiro_p) if not np.isnan(shapiro_p) else ("✅ Normal (AD)" if ad_normal else "⚠️ Not Normal (AD)")
    return result, series


def _qq_plot(series: pd.Series, title: str):
    series = series.dropna()
    if len(series) < 3:
        return None
    # With fit=False, scipy.stats.probplot returns (osm, osr): theoretical vs sample quantiles
    osm_vals, osr_vals = stats.probplot(series, dist="norm", fit=False)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=osm_vals, y=osr_vals, mode="markers", name="Sample Quantiles"))
    min_v, max_v = min(osm_vals), max(osm_vals)
    fig.add_trace(go.Scatter(x=[min_v, max_v], y=[min_v, max_v], mode="lines", name="Reference Line",
                              line=dict(dash="dash", color="red")))
    fig.update_layout(title=title, xaxis_title="Theoretical Quantiles", yaxis_title="Sample Quantiles")
    return fig


def render_page():
    module_header("MOD_01 / M4-5", "Assumption Checking", "normality + homogeneity of variance")
    st.caption("Module 4 & 5 — Normality and Homogeneity of Variance testing.")

    if "df" not in st.session_state or "analysis_objective" not in st.session_state:
        st.warning("⚠️ Please complete Page 1–3 first (upload data & set an objective).")
        return

    df = st.session_state["df"]
    objective = st.session_state["analysis_objective"]

    normality_results = []
    groups_data = {}

    st.subheader("Normality Testing")

    if objective in ("Compare two groups", "Compare multiple groups"):
        group_col = st.session_state.get("group_col")
        value_col = st.session_state.get("value_col")
        if not group_col or not value_col:
            st.warning("⚠️ Missing variable selection from Page 3.")
            return
        for g, sub in df.groupby(group_col):
            res, series = _run_normality_tests(sub[value_col], str(g))
            normality_results.append(res)
            groups_data[str(g)] = series

    elif objective == "Compare before and after condition":
        before_col = st.session_state.get("before_col")
        after_col = st.session_state.get("after_col")
        diff = df[after_col] - df[before_col]
        res, series = _run_normality_tests(diff, "Difference (After - Before)")
        normality_results.append(res)
        groups_data["Difference"] = series

    elif objective == "Determine relationship between variables":
        value_col = st.session_state.get("value_col")
        value_col_2 = st.session_state.get("value_col_2")
        for col in (value_col, value_col_2):
            res, series = _run_normality_tests(df[col], col)
            normality_results.append(res)
            groups_data[col] = series

    elif objective == "Test distribution pattern":
        value_col = st.session_state.get("value_col")
        res, series = _run_normality_tests(df[value_col], value_col)
        normality_results.append(res)
        groups_data[value_col] = series

    normality_df = pd.DataFrame(normality_results)
    st.dataframe(normality_df, use_container_width=True, hide_index=True)
    st.session_state["normality_results"] = normality_df

    overall_normal = True
    for r in normality_results:
        p = r.get("Shapiro-Wilk p")
        if isinstance(p, (int, float)) and not np.isnan(p):
            if p <= 0.05:
                overall_normal = False
        elif "Not Normal" in str(r.get("Normal?", "")):
            overall_normal = False
    st.session_state["is_normal"] = overall_normal

    st.markdown("#### Visual Diagnostics")
    label_choice = st.selectbox("Select group/variable to visualize", list(groups_data.keys()))
    if label_choice:
        series = groups_data[label_choice]
        c1, c2 = st.columns(2)
        with c1:
            fig_hist = px.histogram(series, nbins=30, title=f"Histogram — {label_choice}")
            st.plotly_chart(fig_hist, use_container_width=True)
        with c2:
            fig_qq = _qq_plot(series, f"Q-Q Plot — {label_choice}")
            if fig_qq:
                st.plotly_chart(fig_qq, use_container_width=True)
            else:
                st.info("Not enough data points for a Q-Q plot.")

    # --- Homogeneity of Variance (only relevant for group comparisons) ---
    if objective in ("Compare two groups", "Compare multiple groups"):
        st.divider()
        st.subheader("Homogeneity of Variance (Levene's Test)")
        group_col = st.session_state.get("group_col")
        value_col = st.session_state.get("value_col")
        samples = [sub[value_col].dropna().values for _, sub in df.groupby(group_col)]
        samples = [s for s in samples if len(s) > 1]

        if len(samples) >= 2:
            levene_stat, levene_p = stats.levene(*samples)
            st.metric("Levene's Test p-value", safe_round(levene_p))
            st.write(p_value_badge(levene_p))
            st.session_state["homogeneity_results"] = {
                "statistic": levene_stat, "p_value": levene_p,
                "equal_variance": levene_p > 0.05,
            }
        else:
            st.warning("⚠️ Not enough groups with sufficient data to run Levene's Test.")
            st.session_state["homogeneity_results"] = {"statistic": np.nan, "p_value": np.nan, "equal_variance": None}
    else:
        st.session_state["homogeneity_results"] = None

    st.info("Proceed to **Hypothesis Testing & Post-Hoc Result** in the sidebar to continue.")
