"""
recommendation.py
Module 6: Automated Hypothesis Test Recommendation
"""

import streamlit as st
from src.utils import has_severe_outliers


def recommend_test():
    """
    Rule-based recommendation engine based on:
    - Analysis objective
    - Normality assumption result
    - Homogeneity of variance result
    - Presence of severe outliers

    Returns a dict: {"test": str, "reasoning": [list of str]}
    """
    objective = st.session_state.get("analysis_objective")
    is_normal = st.session_state.get("is_normal", False)
    homogeneity = st.session_state.get("homogeneity_results")
    outlier_summary = st.session_state.get("outlier_summary")
    value_col = st.session_state.get("value_col")

    reasoning = []
    severe_outliers = has_severe_outliers(outlier_summary, value_col) if value_col else False
    if severe_outliers:
        reasoning.append(f"Severe outlier contamination detected in '{value_col}'.")

    equal_variance = homogeneity.get("equal_variance") if homogeneity else None

    if objective == "Compare two groups":
        if is_normal and not severe_outliers:
            if equal_variance:
                test = "Independent T-Test"
                reasoning.append("Data is normally distributed with equal variance and no severe outliers.")
            else:
                test = "Welch T-Test"
                reasoning.append("Data is normally distributed but variances are unequal (Levene's test significant).")
        else:
            test = "Mann-Whitney U Test"
            if not is_normal:
                reasoning.append("Data violates the normality assumption (Shapiro-Wilk significant).")
            if severe_outliers:
                reasoning.append("Severe outliers present — a non-parametric test is more robust.")

    elif objective == "Compare multiple groups":
        if is_normal and not severe_outliers:
            if equal_variance:
                test = "One-Way ANOVA"
                reasoning.append("Data is normally distributed with equal variance across groups.")
            else:
                test = "Welch ANOVA"
                reasoning.append("Data is normally distributed but variances are unequal across groups.")
        else:
            test = "Kruskal-Wallis Test"
            if not is_normal:
                reasoning.append("Data violates the normality assumption.")
            if severe_outliers:
                reasoning.append("Severe outliers present — a non-parametric test is more robust.")

    elif objective == "Determine relationship between variables":
        if is_normal:
            test = "Pearson Correlation"
            reasoning.append("Both variables are approximately normally distributed.")
        else:
            test = "Spearman Correlation"
            reasoning.append("At least one variable violates normality — using rank-based correlation.")

    elif objective == "Compare before and after condition":
        if is_normal and not severe_outliers:
            test = "Paired T-Test"
            reasoning.append("The difference (After - Before) is normally distributed with no severe outliers.")
        else:
            test = "Wilcoxon Signed-Rank Test"
            if not is_normal:
                reasoning.append("The difference (After - Before) violates normality.")
            if severe_outliers:
                reasoning.append("Severe outliers present in the difference scores.")

    elif objective == "Test distribution pattern":
        test = "Shapiro-Wilk / Anderson-Darling Goodness-of-Fit"
        reasoning.append("Distribution pattern is assessed directly via normality tests already run in Module 4.")

    else:
        test = None
        reasoning.append("No analysis objective selected.")

    result = {"test": test, "reasoning": reasoning}
    st.session_state["test_recommendation"] = result
    return result
