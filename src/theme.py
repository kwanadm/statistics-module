"""
theme.py
Injects CSS so the Streamlit app matches the "Analytics System Workspace"
design system (dark navy/slate background, cyan/blue gradient accents,
Inter + Fira Code, grid-paper background).
"""

import streamlit as st

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --font-mono: 'Fira Code', SFMono-Regular, Consolas, monospace;

    --color-bg-main: #0b0f19;
    --color-bg-card: #151b2b;
    --color-bg-card-hover: #1a2235;
    --color-bg-secondary: #10152280;

    --color-text-primary: #e2e8f0;
    --color-text-secondary: #8b9bb4;
    --color-text-tertiary: #64748b;

    --color-accent-cyan: #06b6d4;
    --color-accent-blue: #3b82f6;
    --color-glow: rgba(6, 182, 212, 0.3);

    --color-text-success: #22c55e;
    --color-text-danger: #f87171;
    --color-text-warning: #fbbf24;
    --color-text-info: var(--color-accent-cyan);

    --color-border: rgba(255, 255, 255, 0.08);
    --color-border-hover: var(--color-accent-cyan);

    --color-bg-info: rgba(6, 182, 212, 0.12);
    --color-bg-danger: rgba(248, 113, 113, 0.12);
    --color-bg-warning: rgba(251, 191, 36, 0.12);
    --color-bg-success: rgba(34, 197, 94, 0.12);

    --border-radius-md: 8px;
    --border-radius-lg: 10px;
    --border-radius-xl: 12px;

    --shadow-card: 0 4px 18px rgba(0,0,0,0.35);
    --shadow-hover: 0 5px 15px var(--color-glow);
}

/* Base App Styling - dark grid-paper background */
.stApp {
    background-color: var(--color-bg-main) !important;
    background-image:
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px) !important;
    background-size: 40px 40px !important;
    font-family: var(--font-sans) !important;
    color: var(--color-text-primary) !important;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: var(--color-bg-card) !important;
    border-right: 1px solid var(--color-border) !important;
}

section[data-testid="stSidebar"] * {
    color: var(--color-text-primary);
}

/* Headings - gradient text like landing page h1 */
h1 {
    font-size: 24px !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, var(--color-accent-cyan), var(--color-accent-blue));
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
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

/* Module Header Subtitle - terminal style ">" prompt */
.mod-subtitle {
    color: var(--color-text-secondary);
    font-family: var(--font-mono);
    font-size: 0.85rem;
    margin-bottom: 1rem;
}

.mod-subtitle::before {
    content: "> ";
    color: var(--color-accent-cyan);
}

/* Module Badge Tag */
.mod-tag {
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 99px;
    display: inline-block;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    background: var(--color-bg-info);
    color: var(--color-accent-cyan);
    border: 1px solid rgba(6, 182, 212, 0.3);
}

.mod-tag.onloan {
    background: var(--color-bg-danger);
    color: var(--color-text-danger);
    border: 1px solid rgba(248, 113, 113, 0.3);
}

/* Card Wrappers & Containers (Metrics, Expanders, DataFrames) */
div[data-testid="stMetric"],
div[data-testid="stExpander"],
.stDataFrame,
.stAlert,
div[data-testid="stForm"] {
    background-color: var(--color-bg-card) !important;
    border: 1px solid var(--color-border) !important;
    border-radius: var(--border-radius-xl) !important;
    box-shadow: var(--shadow-card) !important;
    padding: 16px !important;
}

div[data-testid="stExpander"]:hover,
div[data-testid="stForm"]:hover {
    border-color: var(--color-border-hover) !important;
}

/* Metric Label & Value Customization */
div[data-testid="stMetric"] label {
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    color: var(--color-text-secondary) !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 500;
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
    border: 1px solid var(--color-border);
    border-radius: var(--border-radius-md);
    font-family: var(--font-sans);
    font-weight: 600;
    font-size: 13px;
    padding: 8px 16px;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background-color: var(--color-bg-card-hover);
    border-color: var(--color-accent-cyan);
    transform: translateY(-3px);
    box-shadow: var(--shadow-hover);
}

/* Primary Accent Button Style Override - gradient like landing page */
.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, var(--color-accent-cyan), var(--color-accent-blue)) !important;
    color: #0b0f19 !important;
    border: none !important;
    font-weight: 700 !important;
}

.stButton > button[kind="primary"]:hover {
    filter: brightness(1.1);
    transform: translateY(-3px);
    box-shadow: var(--shadow-hover) !important;
}

/* Inputs & Selectboxes */
input, select, textarea, div[data-baseweb="select"] {
    border-radius: var(--border-radius-md) !important;
    font-family: var(--font-sans) !important;
    background-color: var(--color-bg-card) !important;
    color: var(--color-text-primary) !important;
}

div[data-baseweb="select"] > div {
    background-color: var(--color-bg-card) !important;
    border-color: var(--color-border) !important;
}

/* Code & Monospace Formatting */
code, .stCaption, [data-testid="stCaptionContainer"] {
    font-family: var(--font-mono) !important;
    color: var(--color-text-secondary) !important;
}

/* Dataframe Headers & Cells */
.stDataFrame table {
    font-size: 12px !important;
    color: var(--color-text-primary) !important;
}

.stDataFrame th {
    background-color: var(--color-bg-card-hover) !important;
    color: var(--color-text-secondary) !important;
    font-weight: 600 !important;
    font-family: var(--font-mono) !important;
}

/* ============================================================ */
/* Sidebar Nav (st.radio) styled as a real nav list              */
/* ============================================================ */
section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 2px !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    padding: 8px 12px !important;
    border-radius: var(--border-radius-md) !important;
    margin-bottom: 2px !important;
    width: 100%;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    color: var(--color-text-secondary) !important;
    transition: background 0.15s ease, color 0.15s ease;
    cursor: pointer;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background-color: var(--color-bg-card-hover) !important;
    color: var(--color-text-primary) !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
    display: none !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"],
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background-color: var(--color-bg-info) !important;
    color: var(--color-accent-cyan) !important;
    font-weight: 700 !important;
    border-left: 2px solid var(--color-accent-cyan);
}

/* ============================================================ */
/* st.success / st.info / st.warning / st.error text color       */
/* ============================================================ */
div[data-testid="stAlert"] p {
    color: var(--color-text-primary) !important;
    font-family: var(--font-mono) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

div[data-testid="stAlertContentSuccess"] {
    background-color: var(--color-bg-success) !important;
    border: 1px solid rgba(34, 197, 94, 0.3) !important;
}

div[data-testid="stAlertContentInfo"] {
    background-color: var(--color-bg-info) !important;
    border: 1px solid rgba(6, 182, 212, 0.3) !important;
}

div[data-testid="stAlertContentWarning"] {
    background-color: var(--color-bg-warning) !important;
    border: 1px solid rgba(251, 191, 36, 0.3) !important;
}

div[data-testid="stAlertContentError"] {
    background-color: var(--color-bg-danger) !important;
    border: 1px solid rgba(248, 113, 113, 0.3) !important;
}

/* ============================================================ */
/* File uploader dropzone                                        */
/* ============================================================ */
div[data-testid="stFileUploaderDropzone"] {
    background-color: var(--color-bg-card) !important;
    border: 1.5px dashed var(--color-border) !important;
    border-radius: var(--border-radius-lg) !important;
    transition: border-color 0.3s ease, background 0.3s ease;
}

div[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--color-accent-cyan) !important;
    background-color: var(--color-bg-card-hover) !important;
}

div[data-testid="stFileUploaderDropzone"] button {
    border-radius: var(--border-radius-md) !important;
}

/* ============================================================ */
/* Tabs - terminal-style underline                                */
/* ============================================================ */
button[data-baseweb="tab"] {
    font-family: var(--font-mono) !important;
    color: var(--color-text-secondary) !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--color-accent-cyan) !important;
}

div[data-baseweb="tab-highlight"] {
    background-color: var(--color-accent-cyan) !important;
}
</style>
"""


def apply_theme():
    """Injects custom CSS to match the Analytics System Workspace design."""
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def module_header(mod_number: str, title: str, subtitle: str = "select an action to proceed", is_onloan: bool = False):
    """
    Renders a unified header styled after the Analytics System Workspace landing page,
    with the ">" terminal-prompt subtitle and gradient module tag.
    """
    tag_class = "mod-tag onloan" if is_onloan else "mod-tag"
    st.markdown(
        f"""
        <div>
            <span class="{tag_class}">{mod_number} {'ON LOAN' if is_onloan else 'ACTIVE'}</span>
            <h1 style="margin-top:2px; margin-bottom:4px;">{title}</h1>
            <p class="mod-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card(content_html: str, title: str = None):
    """
    Generic dark-mode content card wrapper for use inside any page
    (profiling.py, hypothesis_page.py, report.py, etc).

    Usage:
        card("<p>Chi-square p-value: 0.032</p>", title="Test Result")
    """
    title_html = f"<h4 style='margin-top:0; margin-bottom:8px;'>{title}</h4>" if title else ""
    st.markdown(
        f"""
        <div style="background:var(--color-bg-card); border:1px solid var(--color-border);
        border-radius:var(--border-radius-xl); box-shadow:var(--shadow-card);
        padding:16px; margin-bottom:12px;">
        {title_html}{content_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
