"""Axis Investment Fund Dashboard — Main Entry Point."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from datetime import datetime

# ── 1. 페이지 설정 (반드시 최상단) ────────────────────────────────────────
st.set_page_config(
    page_title="Login",           # ← 기밀 노출 방지: 중립적 타이틀로 변경
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="auto",
)

# ── 2. 메타 태그 강화 (구글 검색 노출 완전 차단) ──────────────────────────
st.markdown("""
<head>
    <meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
    <meta name="googlebot" content="noindex, nofollow, noarchive, nosnippet">
    <meta name="description" content="">
</head>
""", unsafe_allow_html=True)

# ── 3. CSS 및 기타 설정 ───────────────────────────────────────────────────
from components import inject_css
from config import PRIMARY, MUTED

inject_css()

# ── 4. 패스워드 인증 ──────────────────────────────────────────────────────
# ※ 인증 전에는 어떠한 기밀 정보도 렌더링하지 않음
def check_password():
    """패스워드 인증 (Streamlit Secrets 사용)"""

    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    # 인증되지 않은 경우
    if "password_correct" not in st.session_state:
        st.markdown(f"""
        <div style="
            max-width: 400px;
            margin: 80px auto 0 auto;
            padding: 40px 32px;
            background: white;
            border-radius: 16px;
            border: 1px solid #EEF1F5;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            text-align: center;
        ">
            <div style="font-size: 32px; margin-bottom: 12px;">🔒</div>
            <div style="font-size: 20px; font-weight: 700; color: {PRIMARY}; margin-bottom: 8px;">
                AXIS Investment
            </div>
            <div style="font-size: 14px; color: {MUTED}; margin-bottom: 24px;">
                내부 접근 전용 시스템입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.text_input(
            "Password",
            type="password",
            on_change=password_entered,
            key="password",
            placeholder="비밀번호 입력",
            label_visibility="collapsed",
        )
        st.stop()

    # 비밀번호 틀린 경우
    elif not st.session_state["password_correct"]:
        st.markdown(f"""
        <div style="
            max-width: 400px;
            margin: 80px auto 0 auto;
            padding: 40px 32px;
            background: white;
            border-radius: 16px;
            border: 1px solid #EEF1F5;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            text-align: center;
        ">
            <div style="font-size: 32px; margin-bottom: 12px;">🔒</div>
            <div style="font-size: 20px; font-weight: 700; color: {PRIMARY}; margin-bottom: 8px;">
                AXIS Investment
            </div>
            <div style="font-size: 14px; color: {MUTED}; margin-bottom: 24px;">
                내부 접근 전용 시스템입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.error("❌ 비밀번호가 올바르지 않습니다")
        st.text_input(
            "Password",
            type="password",
            on_change=password_entered,
            key="password",
            placeholder="비밀번호 입력",
            label_visibility="collapsed",
        )
        st.stop()

# 인증 확인 (이 줄 이후부터만 기밀 데이터 렌더링)
check_password()

# ── 5. 인증 성공 후: 페이지 타이틀을 실제 타이틀로 교체 ──────────────────
st.markdown("""
<script>document.title = "액시스인베스트먼트 펀드현황";</script>
""", unsafe_allow_html=True)

# ── 6. 인증 성공 후 웰컴 헤더 카드 ─────────────────────────────────────────
st.markdown(f"""
<div style="
    padding: 48px 32px;
    background: linear-gradient(135deg, #667eea 0%, {PRIMARY} 100%);
    border-radius: 16px;
    color: white;
    margin-bottom: 32px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1 style="margin: 0 0 8px 0; font-size: 36px; font-weight: 700;">
                📊 펀드 운용 현황
            </h1>
            <p style="margin: 0; font-size: 16px; opacity: 0.9;">
                Axis Investment Fund Management Dashboard
            </p>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 14px; opacity: 0.85; margin-bottom: 4px;">
                Last Updated
            </div>
            <div style="font-size: 20px; font-weight: 600;">
                {datetime.now().strftime('%Y.%m.%d')}
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 빠른 요약 카드
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="padding: 24px; background: white; border-radius: 12px; border: 2px solid #EEF1F5; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);">
        <div style="color: {MUTED}; font-size: 14px; margin-bottom: 8px;">📈 Dashboard Status</div>
        <div style="font-size: 24px; font-weight: 700; color: {PRIMARY};">Active</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="padding: 24px; background: white; border-radius: 12px; border: 2px solid #EEF1F5; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);">
        <div style="color: {MUTED}; font-size: 14px; margin-bottom: 8px;">🔄 Data Sync</div>
        <div style="font-size: 24px; font-weight: 700; color: {PRIMARY};">Real-time</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="padding: 24px; background: white; border-radius: 12px; border: 2px solid #EEF1F5; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);">
        <div style="color: {MUTED}; font-size: 14px; margin-bottom: 8px;">📅 Reporting Period</div>
        <div style="font-size: 24px; font-weight: 700; color: {PRIMARY};">{datetime.now().strftime('%Y')}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── 7. 메인 대시보드 (인증 성공 후에만 표시) ────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 20px 0 16px 0; margin-bottom: 20px; border-bottom: 1px solid #EEF1F5;">
        <div style="font-size: 20px; font-weight: 700; color: {PRIMARY};">
            AXIS Investment
        </div>
        <div style="font-size: 12px; color: {MUTED}; margin-top: 2px;">
            Fund Management Dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "메뉴",
        ["펀드 종합현황", "펀드결성 히스토리"],
        label_visibility="collapsed",
    )

    st.markdown(f"""
    <div style="position: fixed; bottom: 16px; left: 16px; font-size: 11px; color: {MUTED};">
        Data: Google Sheets (auto-refresh)
    </div>
    """, unsafe_allow_html=True)

# Page Router
if page == "펀드 종합현황":
    from views.summary import render
    render()
else:
    from views.history import render
    render()