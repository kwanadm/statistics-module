"""
interpretation.py
Module 8: Result Interpretation Engine
"""

from src.utils import safe_round


def generate_interpretation(objective: str, result: dict, group_col: str = None,
                             value_col: str = None, value_col_2: str = None,
                             before_col: str = None, after_col: str = None,
                             posthoc: dict = None, alpha: float = 0.05):
    """
    Translate statistical output into:
    1. Decision
    2. Plain-English Interpretation
    3. Operational Meaning
    """
    p_value = result.get("p_value")
    test_name = result.get("test")
    effect_label = result.get("effect_size_label", "N/A")
    effect_type = result.get("effect_size_type", "")
    significant = p_value is not None and p_value <= alpha

    decision = (
        f"Reject the null hypothesis (p = {safe_round(p_value)} ≤ {alpha})."
        if significant else
        f"Fail to reject the null hypothesis (p = {safe_round(p_value)} > {alpha})."
    )

    # --- Plain English Interpretation ---
    if objective in ("Compare two groups", "Compare multiple groups"):
        subject = f"'{value_col}' across levels of '{group_col}'"
        if significant:
            plain_english = (
                f"Using the {test_name}, there is a statistically significant difference in {subject} "
                f"(p = {safe_round(p_value)}). The magnitude of this difference is considered "
                f"**{effect_label.lower()}** ({effect_type} = {safe_round(result.get('effect_size'))})."
            )
        else:
            plain_english = (
                f"Using the {test_name}, no statistically significant difference was found in {subject} "
                f"(p = {safe_round(p_value)}). Any observed differences are likely due to random variation."
            )

    elif objective == "Determine relationship between variables":
        if significant:
            direction = "positive" if result.get("statistic", 0) > 0 else "negative"
            plain_english = (
                f"Using the {test_name}, there is a statistically significant {direction} relationship between "
                f"'{value_col}' and '{value_col_2}' (r = {safe_round(result.get('statistic'))}, p = {safe_round(p_value)}). "
                f"The strength of this relationship is **{effect_label.lower()}**."
            )
        else:
            plain_english = (
                f"Using the {test_name}, no statistically significant relationship was found between "
                f"'{value_col}' and '{value_col_2}' (p = {safe_round(p_value)})."
            )

    elif objective == "Compare before and after condition":
        subject = f"'{before_col}' vs '{after_col}'"
        if significant:
            plain_english = (
                f"Using the {test_name}, there is a statistically significant change between {subject} "
                f"(p = {safe_round(p_value)}). The effect size is **{effect_label.lower()}** "
                f"({effect_type} = {safe_round(result.get('effect_size'))})."
            )
        else:
            plain_english = (
                f"Using the {test_name}, no statistically significant change was detected between {subject} "
                f"(p = {safe_round(p_value)})."
            )

    else:
        plain_english = f"Test performed: {test_name}. p = {safe_round(p_value)}."

    # --- Operational Meaning ---
    operational_meaning = []
    if objective in ("Compare two groups", "Compare multiple groups") and significant:
        operational_meaning.append(
            f"Since '{group_col}' groups differ meaningfully on '{value_col}', treat these groups as "
            "operationally distinct rather than interchangeable when making resourcing, scheduling, "
            "or performance-management decisions."
        )
        if posthoc is not None:
            operational_meaning.append(
                f"Refer to the {posthoc['method']} results below to pinpoint exactly which group pairs "
                "drive this difference before taking targeted action."
            )
    elif objective == "Determine relationship between variables" and significant:
        operational_meaning.append(
            f"Because '{value_col}' and '{value_col_2}' move together, monitoring or improving one may "
            "have a measurable knock-on effect on the other — worth factoring into forecasting or planning."
        )
    elif objective == "Compare before and after condition" and significant:
        operational_meaning.append(
            f"The intervention/condition change appears to have a real, measurable effect on "
            f"'{after_col}' relative to '{before_col}' — worth formally adopting or investigating further "
            "if the direction is favorable."
        )
    else:
        operational_meaning.append(
            "No strong evidence of a real effect was found. Avoid making operational changes based on this "
            "result alone — consider collecting more data or revisiting the analysis with different variables."
        )

    return {
        "decision": decision,
        "plain_english": plain_english,
        "operational_meaning": " ".join(operational_meaning),
        "significant": significant,
    }
