"""Axis Investment Fund Dashboard — Main Entry Point."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st

from components import inject_css
from config import PRIMARY, MUTED

st.set_page_config(
    page_title="액시스 펀드현황",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f"""
    <div style="padding: 20px 0 16px 0; margin-bottom: 20px; border-bottom: 1px solid #EEF1F5;">
        <div style="font-size: 20px; font-weight: 700; color: {PRIMARY};">
            AXIS Investment
        </div>
        <div style="font-size: 12px; color: {MUTED}; margin-top: 2px;">
            Fund Management Dashboard
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "메뉴",
        ["펀드 종합현황", "펀드결성 히스토리"],
        label_visibility="collapsed",
    )

    st.markdown(
        f"""
    <div style="position: fixed; bottom: 16px; left: 16px; font-size: 11px; color: {MUTED};">
        Data: Google Sheets (auto-refresh)
    </div>
    """,
        unsafe_allow_html=True,
    )

# ── Page Router ──────────────────────────────────────────────────────────────
if page == "펀드 종합현황":
    from views.summary import render

    render()
else:
    from views.history import render

    render()
