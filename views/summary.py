"""Page 1: 펀드 종합현황 (Summary tab)."""

import streamlit as st

from components import kpi_card, division_card, fmt_억, fmt_억1, fmt_pct
from config import DIVISION_COLORS
from data import load_summary


def _extract_portfolios(group) -> list[str]:
    """Extract unique portfolio company names from a division group."""
    if "투자대상 기업" not in group.columns:
        return []
    raw = group["투자대상 기업"].dropna().astype(str)
    names = set()
    for val in raw:
        for sep in [",", "/", "·", "\n"]:
            if sep in val:
                val = val.replace(sep, "|")
        for name in val.split("|"):
            name = name.strip()
            if name and name != "nan" and name != "-":
                names.add(name)
    return sorted(names)


def render():
    df = load_summary()

    if df.empty:
        st.warning("Summary 데이터를 불러올 수 없습니다.")
        return

    st.markdown(
        '<div class="page-header">펀드 종합현황</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-sub">Axis Investment Fund Overview</div>',
        unsafe_allow_html=True,
    )

    # ── KPI Cards ────────────────────────────────────────────────────────
    total_aum = df["펀드결성총액"].sum() if "펀드결성총액" in df.columns else 0
    fund_count = len(df)
    annual_fee = df["보수료(1년)"].sum() if "보수료(1년)" in df.columns else 0
    avg_rate = df["관리보수율"].mean() if "관리보수율" in df.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("총 AUM", fmt_억(total_aum))
    with c2:
        kpi_card("운용 펀드", f"{fund_count}개")
    with c3:
        kpi_card("연간 관리보수", fmt_억(annual_fee))
    with c4:
        kpi_card("평균 보수율", fmt_pct(avg_rate))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Enhanced Division Cards ──────────────────────────────────────────
    if "담당" in df.columns:
        div_cols = st.columns(df["담당"].nunique())

        for i, (name, group) in enumerate(df.groupby("담당", sort=True)):
            aum = group["펀드결성총액"].sum() if "펀드결성총액" in group.columns else 0
            aum_pct = (aum / total_aum * 100) if total_aum > 0 else 0
            count = len(group)
            fee = group["보수료(1년)"].sum() if "보수료(1년)" in group.columns else 0

            project_count = 0
            blind_count = 0
            if "구분" in group.columns:
                project_count = group["구분"].astype(str).str.contains("프로젝트", na=False).sum()
                blind_count = group["구분"].astype(str).str.contains("블라인드", na=False).sum()

            portfolios = _extract_portfolios(group)
            color = DIVISION_COLORS.get(name, "#2E86DE")

            with div_cols[i]:
                division_card(
                    title=name,
                    aum=fmt_억(aum),
                    aum_pct=aum_pct,
                    count=count,
                    fee=fmt_억(fee),
                    project_count=project_count,
                    blind_count=blind_count,
                    portfolios=portfolios,
                    color=color,
                )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Raw Data Table ───────────────────────────────────────────────────
    st.markdown("#### 펀드 상세 데이터")

    display_df = df.copy()

    # Drop unnecessary columns
    for col in ["결성일", "만기일", "Co-Gp 비율"]:
        if col in display_df.columns:
            display_df = display_df.drop(columns=[col])

    # Format money columns in 백만원
    for col in ["펀드결성총액", "펀드잔액", "당사출자금"]:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(fmt_억1)
    if "보수료(1년)" in display_df.columns:
        display_df["보수료(1년)"] = display_df["보수료(1년)"].apply(fmt_억1)
    for col in ["출자비율", "관리보수율", "GP 보수 수익률"]:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(fmt_pct)

    col_config = {
        "펀드결성총액": st.column_config.Column(width=120),
        "펀드잔액": st.column_config.Column(width=120),
        "당사출자금": st.column_config.Column(width=120),
    }

    st.dataframe(display_df, use_container_width=True, hide_index=True, column_config=col_config)
