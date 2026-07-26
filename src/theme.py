"""
theme.py
Injects CSS so the Streamlit app matches the AirAsia Operations Suite design system
(Modern Slate/Navy background, Blue/Red operational accents, Inter + Tabler Icons style).
"""

import streamlit as st

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --font-mono: 'JetBrains Mono', SFMono-Regular, Consolas, monospace;
    
    --color-text-primary: #1e293b;
    --color-text-secondary: #475569;
    --color-text-tertiary: #94a3b8;
    
    --color-text-success: #16a34a;
    --color-text-danger: #dc2626;
    --color-text-warning: #d97706;
    --color-text-info: #2563eb;
    
    --color-border-secondary: #e2e8f0;
    --color-border-tertiary: #cbd5e1;
    
    --color-bg-app: #eef4fb;
    --color-bg-card: #ffffff;
    --color-bg-secondary: #f8fafc;
    --color-bg-info: #eff6ff;
    --color-bg-danger: #fee2e2;
    --color-bg-warning: #fef3c7;
    --color-bg-success: #f0fdf4;
    
    --border-radius-md: 8px;
    --border-radius-lg: 12px;
    --border-radius-xl: 16px;
    
    --shadow-card: 0 4px 18px rgba(0,0,0,0.06);
    --shadow-hover: 0 10px 30px rgba(0,0,0,0.08);
}

/* Base App Styling */
.stApp {
    background-color: var(--color-bg-app) !important;
    font-family: var(--font-sans) !important;
    color: var(--color-text-primary) !important;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: var(--color-bg-card) !important;
    border-right: 1px solid var(--color-border-secondary) !important;
}

/* Headings */
h1 {
    font-size: 24px !important;
    font-weight: 800 !important;
    color: var(--color-text-primary) !important;
    letter-spacing: -0.02em;
}

h2 {
    font-size: 18px !important;
    font-weight: 700 !important;
    color: var(--color-text-primary) !important;
}

h3, h4 {
    color: var(--color-text-primary) !important;
    font-weight: 600 !important;
}

/* Module Header Subtitle */
.mod-subtitle {
    color: var(--color-text-secondary);
    font-size: 0.85rem;
    margin-bottom: 1rem;
}

/* Module Badge Tag */
.mod-tag {
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 99px;
    display: inline-block;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    background: var(--color-bg-info);
    color: var(--color-text-info);
}

.mod-tag.onloan {
    background: var(--color-bg-danger);
    color: var(--color-text-danger);
}

/* Card Wrappers & Containers (Metrics, Expanders, DataFrames) */
div[data-testid="stMetric"], 
div[data-testid="stExpander"], 
.stDataFrame, 
.stAlert,
div[data-testid="stForm"] {
    background-color: var(--color-bg-card) !important;
    border: none !important;
    border-radius: var(--border-radius-xl) !important;
    box-shadow: var(--shadow-card) !important;
    padding: 16px !important;
}

/* Metric Label & Value Customization */
div[data-testid="stMetric"] label {
    font-size: 11px !important;
    color: var(--color-text-tertiary) !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}

div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    font-size: 26px !important;
    font-weight: 700 !important;
    color: var(--color-text-primary) !important;
}

/* Primary & Secondary Buttons */
.stButton > button {
    background-color: var(--color-bg-card);
    color: var(--color-text-primary);
    border: 1px solid var(--color-border-tertiary);
    border-radius: var(--border-radius-md);
    font-family: var(--font-sans);
    font-weight: 600;
    font-size: 13px;
    padding: 8px 16px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: var(--color-bg-secondary);
    border-color: var(--color-border-secondary);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* Primary Accent Button Style Override */
.stButton > button[kind="primary"] {
    background-color: var(--color-text-info) !important;
    color: #ffffff !important;
    border: none !important;
}

.stButton > button[kind="primary"]:hover {
    background-color: #1d4ed8 !important;
    color: #ffffff !important;
}

/* Inputs & Selectboxes */
input, select, textarea, div[data-baseweb="select"] {
    border-radius: var(--border-radius-md) !important;
    font-family: var(--font-sans) !important;
}

/* Code & Monospace Formatting */
code, .stCaption, [data-testid="stCaptionContainer"] {
    font-family: var(--font-mono) !important;
    color: var(--color-text-secondary) !important;
}

/* Dataframe Headers & Cells */
.stDataFrame table {
    font-size: 12px !important;
}

.stDataFrame th {
    background-color: var(--color-bg-secondary) !important;
    color: var(--color-text-secondary) !important;
    font-weight: 600 !important;
}

/* ============================================================ */
/* NEW: Sidebar Nav (st.radio) styled as a real nav list         */
/* ============================================================ */
section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 2px !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    padding: 8px 12px !important;
    border-radius: var(--border-radius-md) !important;
    margin-bottom: 2px !important;
    width: 100%;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--color-text-secondary) !important;
    transition: background 0.15s ease, color 0.15s ease;
    cursor: pointer;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background-color: var(--color-bg-secondary) !important;
    color: var(--color-text-primary) !important;
}

/* hide the native radio circle, keep only the label as a nav row */
section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
    display: none !important;
}

/* highlight the active/selected nav item */
section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"],
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background-color: var(--color-bg-info) !important;
    color: var(--color-text-info) !important;
    font-weight: 700 !important;
}

/* ============================================================ */
/* NEW: st.success / st.info / st.warning / st.error text color  */
/* ============================================================ */
div[data-testid="stAlert"] p {
    color: var(--color-text-primary) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

div[data-testid="stAlertContentSuccess"] {
    background-color: var(--color-bg-success) !important;
}

div[data-testid="stAlertContentInfo"] {
    background-color: var(--color-bg-info) !important;
}

div[data-testid="stAlertContentWarning"] {
    background-color: var(--color-bg-warning) !important;
}

div[data-testid="stAlertContentError"] {
    background-color: var(--color-bg-danger) !important;
}

/* ============================================================ */
/* NEW: File uploader dropzone                                   */
/* ============================================================ */
div[data-testid="stFileUploaderDropzone"] {
    background-color: var(--color-bg-secondary) !important;
    border: 1.5px dashed var(--color-border-tertiary) !important;
    border-radius: var(--border-radius-lg) !important;
    transition: border-color 0.15s ease, background 0.15s ease;
}

div[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--color-text-info) !important;
    background-color: var(--color-bg-info) !important;
}

div[data-testid="stFileUploaderDropzone"] button {
    border-radius: var(--border-radius-md) !important;
}
</style>
"""


def apply_theme():
    """Injects custom CSS to match the AirAsia Operations Suite design."""
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def module_header(mod_number: str, title: str, subtitle: str = "Select an action to proceed", is_onloan: bool = False):
    """
    Renders a unified header styled after the AirAsia Operations Suite workspace page.
    """
    tag_class = "mod-tag onloan" if is_onloan else "mod-tag"
    st.markdown(
        f"""
        <div>
            <span class="{tag_class}">{mod_number} OPERATIONAL</span>
            <h1 style="margin-top:2px; margin-bottom:4px;">{title}</h1>
            <p class="mod-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card(content_html: str, title: str = None):
    """
    Generic content card wrapper for use inside any page
    (profiling.py, hypothesis_page.py, report.py, etc).

    Usage:
        card("<p>Chi-square p-value: 0.032</p>", title="Test Result")
    """
    title_html = f"<h4 style='margin-top:0; margin-bottom:8px;'>{title}</h4>" if title else ""
    st.markdown(
        f"""
        <div style="background:var(--color-bg-card); border-radius:var(--border-radius-xl);
        box-shadow:var(--shadow-card); padding:16px; margin-bottom:12px;">
        {title_html}{content_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
