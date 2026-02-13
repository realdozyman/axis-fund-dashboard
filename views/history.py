"""Page 2: 펀드결성 히스토리 (fund_history tab)."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components import kpi_card, fmt_억, fmt_억1
from config import PRIMARY, ACCENT, LIGHT, MUTED
from data import load_history


def render():
    df = load_history()

    if df.empty:
        st.warning("History 데이터를 불러올 수 없습니다.")
        return

    st.markdown(
        '<div class="page-header">펀드결성 히스토리</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-sub">Axis Fund Formation History</div>',
        unsafe_allow_html=True,
    )

    # ── KPI Cards ────────────────────────────────────────────────────────
    total_funds = len(df)
    total_commitment = df["약정총액"].sum() if "약정총액" in df.columns else 0
    active = len(df[df["상태"] == "진행중"]) if "상태" in df.columns else 0
    closed = len(df[df["상태"] == "회수완료"]) if "상태" in df.columns else 0

    st.markdown(
        '<div style="display:grid; grid-template-columns: repeat(4,1fr); gap:12px;">',
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("누적 결성", f"{total_funds}개")
    with c2:
        kpi_card("누적 약정총액", fmt_억(total_commitment))
    with c3:
        kpi_card("운용중", f"{active}개")
    with c4:
        kpi_card("회수완료", f"{closed}개")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 연도별 결성 추이 + 누적 약정총액 차트 ────────────────────────────
    st.markdown("#### 연도별 결성 추이")

    if "결성일" in df.columns:
        chart_df = df.copy()
        chart_df["결성연도"] = pd.to_datetime(chart_df["결성일"], errors="coerce").dt.year
        chart_df = chart_df.dropna(subset=["결성연도"])
        chart_df["결성연도"] = chart_df["결성연도"].astype(int)

        yearly = (
            chart_df.groupby(["결성연도", "상태"])["약정총액"]
            .sum()
            .unstack(fill_value=0)
            .sort_index()
        )

        cum_total = chart_df.groupby("결성연도")["약정총액"].sum().sort_index().cumsum()

        fig = go.Figure()

        # Stacked bars
        if "진행중" in yearly.columns:
            fig.add_trace(go.Bar(
                x=yearly.index,
                y=yearly["진행중"] / 1e8,
                name="운용중",
                marker_color=ACCENT,
            ))
        if "회수완료" in yearly.columns:
            fig.add_trace(go.Bar(
                x=yearly.index,
                y=yearly["회수완료"] / 1e8,
                name="회수완료",
                marker_color=LIGHT,
            ))

        # Cumulative line on secondary axis
        fig.add_trace(go.Scatter(
            x=cum_total.index,
            y=cum_total.values / 1e8,
            name="누적 약정총액",
            yaxis="y2",
            line=dict(color=PRIMARY, width=4),
            mode="lines+markers+text",
            marker=dict(size=7),
            text=[f"{v:,.0f}" for v in cum_total.values / 1e8],
            textposition="top center",
            textfont=dict(size=11, color=PRIMARY),
        ))

        fig.update_layout(
            barmode="stack",
            yaxis=dict(title=dict(text="신규 결성 (억원)", font=dict(size=12, color=MUTED))),
            yaxis2=dict(
                title=dict(text="누적 약정총액 (억원)", font=dict(size=12, color=MUTED)),
                overlaying="y",
                side="right",
            ),
            xaxis=dict(dtick=1),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40, l=60, r=60, b=40),
            height=380,
            font=dict(family="Inter, sans-serif", size=12),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor="#EEF1F5")

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Raw Data Table ───────────────────────────────────────────────────
    st.markdown("#### 전체 펀드 결성 이력")

    display_df = df.copy()
    if "약정총액" in display_df.columns:
        display_df["약정총액"] = display_df["약정총액"].apply(fmt_억1)

    drop_cols = [c for c in display_df.columns if c.startswith("_")]
    display_df = display_df.drop(columns=drop_cols, errors="ignore")

    st.dataframe(display_df, use_container_width=True, hide_index=True)
