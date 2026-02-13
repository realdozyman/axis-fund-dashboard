"""Google Sheets data loader with auto-refresh caching."""

import pandas as pd
import streamlit as st

from config import SUMMARY_CSV, HISTORY_CSV, CACHE_TTL


@st.cache_data(ttl=CACHE_TTL)
def load_summary() -> pd.DataFrame:
    """Load Summary tab from Google Sheets."""
    df = pd.read_csv(SUMMARY_CSV)

    # Numeric columns (comma-formatted strings -> float)
    for col in ["펀드결성총액", "펀드잔액", "당사출자금", "보수료(1년)"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .apply(pd.to_numeric, errors="coerce")
            )

    # Percentage columns ("2.0%" -> 2.0)
    for col in ["출자비율", "Co-Gp 비율", "관리보수율", "GP 보수 수익률"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("%", "", regex=False)
                .apply(pd.to_numeric, errors="coerce")
            )

    return df


@st.cache_data(ttl=CACHE_TTL)
def load_history() -> pd.DataFrame:
    """Load fund_history tab from Google Sheets."""
    df = pd.read_csv(HISTORY_CSV)

    if "약정총액" in df.columns:
        df["약정총액"] = (
            df["약정총액"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .apply(pd.to_numeric, errors="coerce")
        )

    if "회수일" in df.columns:
        df["상태"] = df["회수일"].apply(
            lambda x: "진행중"
            if str(x).strip() in ("진행중", "nan", "")
            else "회수완료"
        )

    return df
