"""
hypothesis_page.py
Page 5: Hypothesis Testing & Post-Hoc Result
Wires together Module 6 (recommendation), Module 7 (test execution + post-hoc),
and Module 8 (interpretation).
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from src.recommendation import recommend_test
from src import testing
from src.interpretation import generate_interpretation
from src.utils import safe_round
from src.theme import module_header


def render_page():
    module_header("MOD_01 / M6-8", "Hypothesis Testing &amp; Post-Hoc Result", "recommend, run, and interpret")
    st.caption("Modules 6, 7 & 8 — Test recommendation, execution, post-hoc analysis, and interpretation.")

    required_prereqs = ["df", "analysis_objective", "normality_results"]
    if any(k not in st.session_state for k in required_prereqs):
        st.warning("⚠️ Please complete Pages 1–4 first.")
        return

    df = st.session_state["df"]
    objective = st.session_state["analysis_objective"]

    # --- Module 6: Recommendation ---
    st.subheader("Recommended Statistical Test")
    rec = recommend_test()
    if rec["test"] is None:
        st.error("Could not determine a recommended test. Please check your objective/variable selections.")
        return

    st.success(f"**Recommended Test: {rec['test']}**")
    with st.expander("Why this test?"):
        for r in rec["reasoning"]:
            st.write(f"- {r}")

    override = st.checkbox("Manually override the recommended test")
    test_name = rec["test"]
    override_options = {
        "Compare two groups": ["Independent T-Test", "Welch T-Test", "Mann-Whitney U Test"],
        "Compare multiple groups": ["One-Way ANOVA", "Welch ANOVA", "Kruskal-Wallis Test"],
        "Determine relationship between variables": ["Pearson Correlation", "Spearman Correlation"],
        "Compare before and after condition": ["Paired T-Test", "Wilcoxon Signed-Rank Test"],
    }
    if override and objective in override_options:
        test_name = st.selectbox("Select a test to run instead", override_options[objective],
                                  index=override_options[objective].index(test_name)
                                  if test_name in override_options[objective] else 0)

    st.divider()
    if not st.button("▶️ Run Statistical Test", type="primary"):
        st.info("Click the button above to execute the selected test.")
        return

    # --- Module 7: Execution ---
    group_col = st.session_state.get("group_col")
    value_col = st.session_state.get("value_col")
    value_col_2 = st.session_state.get("value_col_2")
    before_col = st.session_state.get("before_col")
    after_col = st.session_state.get("after_col")
    posthoc = None

    try:
        if objective == "Compare two groups":
            result = testing.run_two_group_test(df, group_col, value_col, test_name)
        elif objective == "Compare multiple groups":
            result = testing.run_multi_group_test(df, group_col, value_col, test_name)
            if result["p_value"] <= 0.05:
                posthoc = testing.run_posthoc(df, group_col, value_col, test_name)
        elif objective == "Determine relationship between variables":
            result = testing.run_correlation(df, value_col, value_col_2, test_name)
        elif objective == "Compare before and after condition":
            result = testing.run_paired_test(df, before_col, after_col, test_name)
        elif objective == "Test distribution pattern":
            norm_df = st.session_state["normality_results"]
            result = {
                "test": "Shapiro-Wilk Goodness-of-Fit",
                "p_value": norm_df.iloc[0].get("Shapiro-Wilk p"),
                "statistic": None,
                "effect_size": None, "effect_size_type": "N/A", "effect_size_label": "N/A",
            }
        else:
            st.error("Unsupported objective.")
            return
    except Exception as e:
        st.error(f"⚠️ Error while executing the statistical test: {e}")
        return

    st.session_state["test_results"] = result
    st.session_state["posthoc_results"] = posthoc

    # --- Display base metrics ---
    st.subheader("Test Output")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Test", result.get("test"))
    m2.metric("Statistic", safe_round(result.get("statistic")))
    m3.metric("p-value", safe_round(result.get("p_value")))
    ci = result.get("ci95")
    ci_str = f"[{safe_round(ci[0])}, {safe_round(ci[1])}]" if ci else "N/A"
    m4.metric("95% CI", ci_str)

    st.markdown(
        f"**Effect Size ({result.get('effect_size_type', 'N/A')}):** "
        f"{safe_round(result.get('effect_size'))} — *{result.get('effect_size_label', 'N/A')}*"
    )

    # --- Post-hoc ---
    if posthoc is not None:
        st.subheader(f"Post-Hoc Analysis — {posthoc['method']}")
        st.dataframe(posthoc["table"], use_container_width=True)

    # --- Violin/Box visualization ---
    st.subheader("Group Comparison Visual")
    if objective in ("Compare two groups", "Compare multiple groups") and group_col and value_col:
        fig = px.violin(df, x=group_col, y=value_col, box=True, points="all",
                         title=f"{value_col} by {group_col}")
        st.plotly_chart(fig, use_container_width=True)
    elif objective == "Determine relationship between variables":
        fig = px.scatter(df, x=value_col, y=value_col_2, trendline="ols",
                          title=f"{value_col} vs {value_col_2}")
        st.plotly_chart(fig, use_container_width=True)
    elif objective == "Compare before and after condition":
        melt_df = df[[before_col, after_col]].melt(var_name="Condition", value_name="Value")
        fig = px.violin(melt_df, x="Condition", y="Value", box=True, points="all",
                         title=f"{before_col} vs {after_col}")
        st.plotly_chart(fig, use_container_width=True)

    # --- Module 8: Interpretation ---
    st.divider()
    st.subheader("📋 Interpretation & Business Insight")
    interp = generate_interpretation(
        objective=objective, result=result, group_col=group_col, value_col=value_col,
        value_col_2=value_col_2, before_col=before_col, after_col=after_col, posthoc=posthoc,
    )
    st.session_state["interpretation"] = interp

    st.markdown(f"**1. Decision:** {interp['decision']}")
    st.markdown(f"**2. Interpretation:** {interp['plain_english']}")
    st.markdown(f"**3. Operational Meaning:** {interp['operational_meaning']}")

    st.session_state["report_ready"] = True
    st.info("Proceed to **Report Export** in the sidebar to download your findings.")
