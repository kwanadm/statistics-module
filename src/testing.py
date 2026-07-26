"""
testing.py
Module 7: Statistical Test & Post-Hoc Execution
"""

import numpy as np
import pandas as pd
from scipy import stats
import pingouin as pg
import scikit_posthocs as sp
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from src.utils import effect_size_label_cohens_d, effect_size_label_eta_squared, effect_size_label_correlation


def _cohens_d(a, b):
    a, b = np.asarray(a), np.asarray(b)
    n1, n2 = len(a), len(b)
    pooled_std = np.sqrt(((n1 - 1) * np.var(a, ddof=1) + (n2 - 1) * np.var(b, ddof=1)) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0.0
    return (np.mean(a) - np.mean(b)) / pooled_std


def _rank_biserial_mw(a, b, u_stat):
    n1, n2 = len(a), len(b)
    return 1 - (2 * u_stat) / (n1 * n2)


def run_two_group_test(df: pd.DataFrame, group_col: str, value_col: str, test_name: str):
    groups = list(df.groupby(group_col))
    (g1_name, g1_df), (g2_name, g2_df) = groups[0], groups[1]
    a = g1_df[value_col].dropna().values
    b = g2_df[value_col].dropna().values

    result = {"test": test_name, "group_labels": (str(g1_name), str(g2_name))}

    if test_name == "Independent T-Test":
        t_res = pg.ttest(a, b, correction=False)
        result["statistic"] = t_res["T"].values[0]
        result["p_value"] = t_res["p_val"].values[0]
        result["ci95"] = tuple(t_res["CI95"].values[0])
        d = _cohens_d(a, b)
        result["effect_size"] = d
        result["effect_size_type"] = "Cohen's d"
        result["effect_size_label"] = effect_size_label_cohens_d(d)

    elif test_name == "Welch T-Test":
        t_res = pg.ttest(a, b, correction=True)
        result["statistic"] = t_res["T"].values[0]
        result["p_value"] = t_res["p_val"].values[0]
        result["ci95"] = tuple(t_res["CI95"].values[0])
        d = _cohens_d(a, b)
        result["effect_size"] = d
        result["effect_size_type"] = "Cohen's d"
        result["effect_size_label"] = effect_size_label_cohens_d(d)

    elif test_name == "Mann-Whitney U Test":
        u_stat, p_val = stats.mannwhitneyu(a, b, alternative="two-sided")
        result["statistic"] = u_stat
        result["p_value"] = p_val
        result["ci95"] = None
        r = _rank_biserial_mw(a, b, u_stat)
        result["effect_size"] = r
        result["effect_size_type"] = "Rank-Biserial r"
        result["effect_size_label"] = effect_size_label_correlation(r)

    result["group_data"] = {str(g1_name): a, str(g2_name): b}
    return result


def run_multi_group_test(df: pd.DataFrame, group_col: str, value_col: str, test_name: str):
    groups = df.groupby(group_col)
    group_data = {str(name): sub[value_col].dropna().values for name, sub in groups}
    samples = list(group_data.values())

    result = {"test": test_name, "group_data": group_data}

    if test_name == "One-Way ANOVA":
        aov = pg.anova(data=df, dv=value_col, between=group_col, detailed=True)
        row = aov.iloc[0]
        result["statistic"] = row["F"]
        result["p_value"] = row["p-unc"]
        eta_sq = row["np2"] if "np2" in aov.columns else np.nan
        result["effect_size"] = eta_sq
        result["effect_size_type"] = "Eta-squared (partial)"
        result["effect_size_label"] = effect_size_label_eta_squared(eta_sq) if not np.isnan(eta_sq) else "N/A"

    elif test_name == "Welch ANOVA":
        aov = pg.welch_anova(data=df, dv=value_col, between=group_col)
        row = aov.iloc[0]
        result["statistic"] = row["F"]
        result["p_value"] = row["p-unc"]
        eta_sq = row["np2"] if "np2" in aov.columns else np.nan
        result["effect_size"] = eta_sq
        result["effect_size_type"] = "Eta-squared (partial)"
        result["effect_size_label"] = effect_size_label_eta_squared(eta_sq) if not np.isnan(eta_sq) else "N/A"

    elif test_name == "Kruskal-Wallis Test":
        h_stat, p_val = stats.kruskal(*samples)
        result["statistic"] = h_stat
        result["p_value"] = p_val
        n = sum(len(s) for s in samples)
        eta_sq_h = (h_stat - len(samples) + 1) / (n - len(samples)) if n > len(samples) else np.nan
        result["effect_size"] = eta_sq_h
        result["effect_size_type"] = "Epsilon-squared (approx.)"
        result["effect_size_label"] = effect_size_label_eta_squared(eta_sq_h) if not np.isnan(eta_sq_h) else "N/A"

    return result


def run_posthoc(df: pd.DataFrame, group_col: str, value_col: str, test_name: str):
    """Run Tukey HSD (after significant ANOVA) or Dunn's test w/ Bonferroni (after significant Kruskal-Wallis)."""
    if test_name in ("One-Way ANOVA", "Welch ANOVA"):
        tukey = pairwise_tukeyhsd(endog=df[value_col].dropna(),
                                   groups=df.loc[df[value_col].notna(), group_col])
        tukey_df = pd.DataFrame(data=tukey._results_table.data[1:], columns=tukey._results_table.data[0])
        return {"method": "Tukey's HSD", "table": tukey_df}

    elif test_name == "Kruskal-Wallis Test":
        dunn_df = sp.posthoc_dunn(df, val_col=value_col, group_col=group_col, p_adjust="bonferroni")
        return {"method": "Dunn's Test (Bonferroni-corrected)", "table": dunn_df}

    return None


def run_correlation(df: pd.DataFrame, col_a: str, col_b: str, method: str):
    sub = df[[col_a, col_b]].dropna()
    if method == "Pearson Correlation":
        r, p = stats.pearsonr(sub[col_a], sub[col_b])
    else:
        r, p = stats.spearmanr(sub[col_a], sub[col_b])

    n = len(sub)
    # Fisher z CI for correlation
    if abs(r) < 1 and n > 3:
        z = np.arctanh(r)
        se = 1 / np.sqrt(n - 3)
        ci_low, ci_high = np.tanh(z - 1.96 * se), np.tanh(z + 1.96 * se)
    else:
        ci_low, ci_high = np.nan, np.nan

    return {
        "test": method,
        "statistic": r,
        "p_value": p,
        "ci95": (ci_low, ci_high),
        "effect_size": r,
        "effect_size_type": "Correlation coefficient (r)",
        "effect_size_label": effect_size_label_correlation(r),
        "n": n,
    }


def run_paired_test(df: pd.DataFrame, before_col: str, after_col: str, test_name: str):
    sub = df[[before_col, after_col]].dropna()
    before, after = sub[before_col].values, sub[after_col].values
    diff = after - before

    result = {"test": test_name}

    if test_name == "Paired T-Test":
        t_res = pg.ttest(after, before, paired=True)
        result["statistic"] = t_res["T"].values[0]
        result["p_value"] = t_res["p_val"].values[0]
        result["ci95"] = tuple(t_res["CI95"].values[0])
        d = np.mean(diff) / np.std(diff, ddof=1) if np.std(diff, ddof=1) != 0 else 0.0
        result["effect_size"] = d
        result["effect_size_type"] = "Cohen's d (paired)"
        result["effect_size_label"] = effect_size_label_cohens_d(d)

    elif test_name == "Wilcoxon Signed-Rank Test":
        w_stat, p_val = stats.wilcoxon(after, before)
        result["statistic"] = w_stat
        result["p_value"] = p_val
        result["ci95"] = None
        n = len(diff)
        z_approx = stats.norm.ppf(1 - p_val / 2) if p_val > 0 else np.nan
        r = z_approx / np.sqrt(n) if n > 0 and not np.isnan(z_approx) else np.nan
        result["effect_size"] = r
        result["effect_size_type"] = "Matched-pairs rank-biserial r (approx.)"
        result["effect_size_label"] = effect_size_label_correlation(r) if not np.isnan(r) else "N/A"

    result["diff_data"] = diff
    return result
