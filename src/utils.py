"""
utils.py
Shared helper functions used across the Statistical Intelligence Platform (SIP).
"""

import numpy as np
import pandas as pd


def detect_variable_types(df: pd.DataFrame):
    """
    Auto-detect numerical vs categorical variables.

    A column is treated as numerical if it has a numeric dtype AND has more
    than a handful of unique values (to avoid coded categorical integers like
    0/1 flags being treated as continuous). Everything else (object, category,
    bool, or low-cardinality numeric) is treated as categorical.
    """
    numerical_cols = []
    categorical_cols = []

    for col in df.columns:
        series = df[col]
        if pd.api.types.is_numeric_dtype(series):
            n_unique = series.nunique(dropna=True)
            if n_unique > 10:
                numerical_cols.append(col)
            else:
                categorical_cols.append(col)
        else:
            categorical_cols.append(col)

    return numerical_cols, categorical_cols


def iqr_outlier_scan(df: pd.DataFrame, numerical_cols: list, k: float = 1.5):
    """
    Run an IQR-based outlier scan on each numerical column.

    Returns a summary DataFrame with counts/percentages of outliers per
    column, plus a dict mapping column -> boolean mask of outlier rows.
    """
    summary_rows = []
    outlier_masks = {}

    for col in numerical_cols:
        series = df[col].dropna()
        if series.empty:
            continue
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - k * iqr
        upper_bound = q3 + k * iqr

        mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        outlier_masks[col] = mask

        n_outliers = int(mask.sum())
        pct_outliers = (n_outliers / len(df)) * 100 if len(df) > 0 else 0

        summary_rows.append({
            "Variable": col,
            "Q1": round(q1, 4),
            "Q3": round(q3, 4),
            "IQR": round(iqr, 4),
            "Lower Bound": round(lower_bound, 4),
            "Upper Bound": round(upper_bound, 4),
            "Outlier Count": n_outliers,
            "Outlier %": round(pct_outliers, 2),
            "Severity": _severity_label(pct_outliers),
        })

    summary_df = pd.DataFrame(summary_rows)
    return summary_df, outlier_masks


def _severity_label(pct_outliers: float) -> str:
    if pct_outliers == 0:
        return "None"
    elif pct_outliers < 2:
        return "Low"
    elif pct_outliers < 5:
        return "Moderate"
    else:
        return "Severe"


def has_severe_outliers(outlier_summary: pd.DataFrame, col: str) -> bool:
    """Check whether a given column has severe/moderate outlier contamination."""
    if outlier_summary is None or outlier_summary.empty:
        return False
    row = outlier_summary[outlier_summary["Variable"] == col]
    if row.empty:
        return False
    severity = row.iloc[0]["Severity"]
    return severity in ("Moderate", "Severe")


def p_value_badge(p_value: float, alpha: float = 0.05) -> str:
    """Return a human readable pass/fail badge string for a p-value."""
    if p_value is None or (isinstance(p_value, float) and np.isnan(p_value)):
        return "N/A"
    return "✅ Assumption Satisfied" if p_value > alpha else "⚠️ Assumption Violated"


def safe_round(value, digits=4):
    try:
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return "N/A"
        return round(float(value), digits)
    except (TypeError, ValueError):
        return value


def effect_size_label_cohens_d(d: float) -> str:
    d = abs(d)
    if d < 0.2:
        return "Negligible"
    elif d < 0.5:
        return "Small"
    elif d < 0.8:
        return "Medium"
    else:
        return "Large"


def effect_size_label_eta_squared(eta_sq: float) -> str:
    if eta_sq < 0.01:
        return "Negligible"
    elif eta_sq < 0.06:
        return "Small"
    elif eta_sq < 0.14:
        return "Medium"
    else:
        return "Large"


def effect_size_label_correlation(r: float) -> str:
    r = abs(r)
    if r < 0.1:
        return "Negligible"
    elif r < 0.3:
        return "Small"
    elif r < 0.5:
        return "Medium"
    else:
        return "Large"
