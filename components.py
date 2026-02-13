"""UI components: CSS, KPI cards, enhanced division cards, formatters."""

import pandas as pd
import streamlit as st

from config import PRIMARY, ACCENT, LIGHT, MUTED, TEXT


# ── Global CSS ───────────────────────────────────────────────────────────────


def inject_css():
    st.markdown(
        """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp {
        background-color: #F8F9FA;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ── KPI Card ── */
    .kpi-card {
        background: #fff;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        border-left: 4px solid """
        + ACCENT
        + """;
        margin-bottom: 12px;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .kpi-label {
        font-size: 11px;
        color: """
        + MUTED
        + """;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 700;
        color: """
        + PRIMARY
        + """;
        line-height: 1.2;
    }
    .kpi-sub {
        font-size: 11px;
        color: """
        + MUTED
        + """;
        margin-top: 4px;
    }

    /* ── Enhanced Division Card ── */
    .div-card {
        background: #fff;
        border-radius: 12px;
        padding: 22px 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        margin-bottom: 12px;
        min-height: 380px;
        display: flex;
        flex-direction: column;
    }
    .div-title {
        font-size: 16px;
        font-weight: 700;
        color: """
        + PRIMARY
        + """;
        margin-bottom: 16px;
    }
    .div-aum-row {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 6px;
    }
    .div-aum-value {
        font-size: 22px;
        font-weight: 700;
        color: """
        + PRIMARY
        + """;
    }
    .div-aum-pct {
        font-size: 13px;
        font-weight: 600;
        color: """
        + ACCENT
        + """;
    }
    .div-bar-bg {
        width: 100%;
        height: 6px;
        background: #EEF1F5;
        border-radius: 3px;
        margin-bottom: 16px;
    }
    .div-bar-fill {
        height: 6px;
        border-radius: 3px;
    }
    .div-stats {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-bottom: 16px;
    }
    .div-stat {
        display: flex;
        justify-content: space-between;
    }
    .div-label { font-size: 12px; color: """
        + MUTED
        + """; }
    .div-value { font-size: 13px; font-weight: 600; color: """
        + TEXT
        + """; }
    .div-separator {
        border-top: 1px solid #EEF1F5;
        margin: 8px 0;
    }
    .div-port-title {
        font-size: 11px;
        font-weight: 600;
        color: """
        + MUTED
        + """;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    .div-port-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
    }
    .div-port-tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 500;
        background: #EEF4FB;
        color: """
        + PRIMARY
        + """;
    }

    /* ── Section header ── */
    .page-header {
        font-size: 28px;
        font-weight: 700;
        color: """
        + PRIMARY
        + """;
        margin-bottom: 2px;
    }
    .page-sub {
        font-size: 14px;
        color: """
        + MUTED
        + """;
        margin-bottom: 24px;
    }

    /* ── Status badge ── */
    .badge-active {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        background: #E8F4FD;
        color: #2E86DE;
    }
    .badge-closed {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        background: #F0F0F0;
        color: #7F8C8D;
    }

    /* ── Misc ── */
    .stDataFrame { border-radius: 8px; overflow: hidden; }
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        background: transparent;
    }

    @media (max-width: 768px) {
        .kpi-value { font-size: 20px; }
        .kpi-card { padding: 14px 16px; }
        .div-card { padding: 14px 16px; }
        .div-aum-value { font-size: 18px; }
        .page-header { font-size: 22px; }
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


# ── Formatters ───────────────────────────────────────────────────────────────


def fmt_억(val) -> str:
    if pd.isna(val) or val == 0:
        return "-"
    억 = val / 1e8
    if abs(억) >= 1:
        return f"{억:,.0f}억"
    만 = val / 1e4
    return f"{만:,.0f}만"


def fmt_억1(val) -> str:
    """소숫점 한자리 억원 (예: 50.3억원)"""
    if pd.isna(val) or val == 0:
        return "-"
    억 = val / 1e8
    return f"{억:,.1f}억원"


def fmt_pct(val) -> str:
    if pd.isna(val):
        return "-"
    return f"{val:.1f}%"


# ── KPI Card ─────────────────────────────────────────────────────────────────


def kpi_card(label: str, value: str, sub: str = ""):
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    st.markdown(
        f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {sub_html}
    </div>
    """,
        unsafe_allow_html=True,
    )


# ── Enhanced Division Card ───────────────────────────────────────────────────


def division_card(
    title: str,
    aum: str,
    aum_pct: float,
    count: int,
    fee: str,
    project_count: int,
    blind_count: int,
    portfolios: list[str],
    color: str,
):
    tags_html = "".join(
        f'<span class="div-port-tag">{name}</span>' for name in portfolios
    )

    st.markdown(
        f"""
    <div class="div-card" style="border-left: 4px solid {color};">
        <div class="div-title">{title}</div>
        <div class="div-aum-row">
            <span class="div-aum-value">{aum}</span>
            <span class="div-aum-pct">전체 {aum_pct:.1f}%</span>
        </div>
        <div class="div-bar-bg">
            <div class="div-bar-fill" style="width: {min(aum_pct, 100):.1f}%; background: {color};"></div>
        </div>
        <div class="div-stats">
            <div class="div-stat">
                <span class="div-label">펀드 수</span>
                <span class="div-value">{count}개</span>
            </div>
            <div class="div-stat">
                <span class="div-label">연 보수료</span>
                <span class="div-value">{fee}</span>
            </div>
            <div class="div-stat">
                <span class="div-label">프로젝트</span>
                <span class="div-value">{project_count}개</span>
            </div>
            <div class="div-stat">
                <span class="div-label">블라인드</span>
                <span class="div-value">{blind_count}개</span>
            </div>
        </div>
        <div class="div-separator"></div>
        <div class="div-port-title">주요 포트폴리오</div>
        <div class="div-port-tags">
            {tags_html}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
