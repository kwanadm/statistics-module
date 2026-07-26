"""
theme.py
Injects CSS so the app matches the Analytics System Workspace landing page
(dark navy background, cyan/blue gradient accents, Fira Code + Inter fonts).
"""

import streamlit as st

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@400;600;800&display=swap');

:root {
    --bg-main: #0b0f19;
    --bg-card: #151b2b;
    --text-main: #e2e8f0;
    --text-muted: #8b9bb4;
    --accent-cyan: #06b6d4;
    --accent-blue: #3b82f6;
    --glow: rgba(6, 182, 212, 0.3);
}

/* App background + grid pattern, matching the landing page */
.stApp {
    background-color: var(--bg-main);
    background-image:
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    font-family: 'Inter', sans-serif;
    color: var(--text-main);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: var(--bg-card);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Headings get the cyan -> blue gradient text treatment */
h1 {
    font-weight: 800 !important;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
h2, h3 { color: var(--text-main) !important; }

/* Module tag ("MOD_01" style) helper class */
.mod-tag {
    font-family: 'Fira Code', monospace;
    font-size: 0.8rem;
    color: var(--accent-cyan);
    display: block;
    margin-bottom: 4px;
    letter-spacing: 0.05em;
}

/* Terminal-style subtitle */
.mod-subtitle {
    color: var(--text-muted);
    font-family: 'Fira Code', monospace;
    font-size: 0.9rem;
}

/* Cards: metrics, dataframes, expanders get the module-btn look */
div[data-testid="stMetric"], div[data-testid="stExpander"], .stDataFrame, .stAlert {
    background-color: var(--bg-card) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
}

/* Primary buttons -> cyan glow on hover, matching .module-btn:hover */
.stButton > button {
    background-color: var(--bg-card);
    color: var(--text-main);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    transition: all 0.2s ease-in-out;
}
.stButton > button:hover {
    border-color: var(--accent-cyan);
    box-shadow: 0 5px 15px var(--glow);
    transform: translateY(-2px);
    color: var(--accent-cyan);
}

/* Code / mono accents (e.g. dataset name, values) */
code, .stCaption, [data-testid="stCaptionContainer"] {
    font-family: 'Fira Code', monospace !important;
    color: var(--text-muted) !important;
}
</style>
"""


def apply_theme():
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def module_header(mod_number: str, title: str, subtitle: str = "select an action to proceed"):
    """Render a landing-page-style module header: MOD_01 tag + gradient title + terminal subtitle."""
    st.markdown(
        f"""
        <span class="mod-tag">{mod_number} (ACTIVE)</span>
        <h1 style="margin-bottom:4px;">{title}</h1>
        <p class="mod-subtitle">&gt; {subtitle}</p>
        """,
        unsafe_allow_html=True,
    )
