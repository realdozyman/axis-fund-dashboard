"""Axis Investment Fund Dashboard — Main Entry Point."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st

# ── 1. 페이지 설정 (반드시 최상단) ────────────────────────────────────────
st.set_page_config(
    page_title="액시스 펀드현황",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto",
)

# ── 2. 메타 태그 (구글 검색 노출 방지) ────────────────────────────────────
st.markdown("""
<head>
    <meta name="description" content="액시스인베스트먼트 펀드 운용 현황 대시보드">
    <meta name="robots" content="noindex, nofollow">
</head>
""", unsafe_allow_html=True)

# ── 3. CSS 및 기타 설정 ───────────────────────────────────────────────────
from components import inject_css
from config import PRIMARY, MUTED

inject_css()

# ── 4. 패스워드 인증 ──────────────────────────────────────────────────────
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
        st.title("🔒 액시스인베스트먼트 펀드 현황")
        st.markdown("내부 데이터 보호를 위해 비밀번호를 입력해주세요.")
        st.text_input(
            "Password", 
            type="password", 
            on_change=password_entered, 
            key="password",
            placeholder="비밀번호 입력"
        )
        return False
    
    # 비밀번호 틀린 경우
    elif not st.session_state["password_correct"]:
        st.title("🔒 액시스인베스트먼트 펀드 현황")
        st.text_input(
            "Password", 
            type="password", 
            on_change=password_entered, 
            key="password",
            placeholder="비밀번호 입력"
        )
        st.error("❌ 비밀번호가 올바르지 않습니다")
        return False
    
    # 인증 성공
    else:
        return True

# ── 5. 인증 확인 ──────────────────────────────────────────────────────────
if not check_password():
    st.stop()  # 인증 실패 시 여기서 중단

# ── 6. 인증 성공 후 메인 대시보드 ──────────────────────────────────────────
# Sidebar
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

# Page Router
if page == "펀드 종합현황":
    from views.summary import render
    render()
else:
    from views.history import render
    render()