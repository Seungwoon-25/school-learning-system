import streamlit as st
import sqlite3
import hashlib
import os
from datetime import datetime, date


# =========================================================
# 1. 기본 설정
# =========================================================

st.set_page_config(
    page_title="방과후 학습 관리 시스템",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# 2. Apple-inspired 디자인 CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       기본 폰트 및 전체 화면
       ===================================================== */

    html,
    body,
    [class*="css"] {
        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "SF Pro Display",
            "SF Pro Text",
            "Inter",
            system-ui,
            sans-serif;
    }

    .stApp {
        background: #ffffff;
        color: #1d1d1f;
    }

    .main {
        padding-top: 0 !important;
    }

    .block-container {
        max-width: 1440px;
        padding-top: 0.5rem;
        padding-bottom: 4rem;
    }


    /* =====================================================
       상단 네비게이션
       ===================================================== */

    .top-nav {
        width: 100%;
        background: #000000;
        color: #ffffff;
        padding: 12px 28px;
        margin-bottom: 0;
    }

    .top-nav-inner {
        max-width: 1440px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .top-nav-title {
        font-size: 14px;
        font-weight: 600;
        letter-spacing: -0.2px;
    }

    .top-nav-subtitle {
        font-size: 12px;
        font-weight: 400;
        color: #cccccc;
        letter-spacing: -0.1px;
    }


    /* =====================================================
       Hero 영역
       ===================================================== */

    .hero {
        background: #ffffff;
        text-align: center;
        padding: 90px 24px 80px 24px;
    }

    .hero-dark {
        background: #272729;
        color: #ffffff;
        text-align: center;
        padding: 80px 24px;
    }

    .hero-parchment {
        background: #f5f5f7;
        text-align: center;
        padding: 80px 24px;
    }

    .hero-eyebrow {
        font-size: 14px;
        font-weight: 600;
        color: #0066cc;
        margin-bottom: 16px;
        letter-spacing: -0.2px;
    }

    .hero-title {
        font-size: 56px;
        line-height: 1.07;
        font-weight: 600;
        letter-spacing: -1.2px;
        margin: 0;
        color: #1d1d1f;
    }

    .hero-title-dark {
        font-size: 48px;
        line-height: 1.08;
        font-weight: 600;
        letter-spacing: -1px;
        margin: 0;
        color: #ffffff;
    }

    .hero-description {
        max-width: 700px;
        margin: 22px auto 0 auto;
        font-size: 21px;
        line-height: 1.45;
        font-weight: 400;
        color: #6e6e73;
        letter-spacing: -0.2px;
    }

    .hero-description-dark {
        max-width: 700px;
        margin: 22px auto 0 auto;
        font-size: 21px;
        line-height: 1.45;
        font-weight: 400;
        color: #cccccc;
        letter-spacing: -0.2px;
    }


    /* =====================================================
       섹션
       ===================================================== */

    .section-light {
        background: #ffffff;
        padding: 72px 40px;
    }

    .section-parchment {
        background: #f5f5f7;
        padding: 72px 40px;
    }

    .section-dark {
        background: #272729;
        color: #ffffff;
        padding: 72px 40px;
    }

    .section-dark-2 {
        background: #2a2a2c;
        color: #ffffff;
        padding: 72px 40px;
    }

    .section-title {
        font-size: 40px;
        line-height: 1.1;
        font-weight: 600;
        letter-spacing: -0.7px;
        margin-bottom: 12px;
        color: #1d1d1f;
    }

    .section-title-dark {
        font-size: 40px;
        line-height: 1.1;
        font-weight: 600;
        letter-spacing: -0.7px;
        margin-bottom: 12px;
        color: #ffffff;
    }

    .section-description {
        font-size: 17px;
        line-height: 1.47;
        color: #6e6e73;
        max-width: 760px;
    }

    .section-description-dark {
        font-size: 17px;
        line-height: 1.47;
        color: #cccccc;
        max-width: 760px;
    }


    /* =====================================================
       정보 카드
       ===================================================== */

    .info-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 18px;
        padding: 28px;
        min-height: 150px;
    }

    .info-card-parchment {
        background: #f5f5f7;
        border: 1px solid #e0e0e0;
        border-radius: 18px;
        padding: 28px;
        min-height: 150px;
    }

    .info-card-title {
        font-size: 21px;
        font-weight: 600;
        line-height: 1.2;
        color: #1d1d1f;
        margin-bottom: 10px;
    }

    .info-card-text {
        font-size: 17px;
        line-height: 1.47;
        color: #6e6e73;
    }


    /* =====================================================
       출결 카드
       ===================================================== */

    .attendance-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 16px;
    }

    .attendance-card-dark {
        background: #2a2a2c;
        border: 1px solid #444444;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 16px;
    }

    .student-number {
        font-size: 28px;
        font-weight: 600;
        letter-spacing: -0.4px;
        color: #1d1d1f;
    }

    .student-name {
        font-size: 17px;
        color: #6e6e73;
        margin-top: 4px;
    }


    /* =====================================================
       통계
       ===================================================== */

    .metric-card {
        background: #f5f5f7;
        border-radius: 18px;
        padding: 28px 24px;
        text-align: center;
        min-height: 130px;
    }

    .metric-number {
        font-size: 40px;
        font-weight: 600;
        line-height: 1.1;
        letter-spacing: -0.7px;
        color: #1d1d1f;
    }

    .metric-label {
        margin-top: 8px;
        font-size: 14px;
        color: #6e6e73;
    }


    /* =====================================================
       자료 카드
       ===================================================== */

    .material-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 18px;
        padding: 28px;
        margin-bottom: 18px;
    }

    .material-title {
        font-size: 21px;
        font-weight: 600;
        color: #1d1d1f;
        letter-spacing: -0.3px;
    }

    .material-description {
        margin-top: 10px;
        font-size: 17px;
        line-height: 1.47;
        color: #6e6e73;
    }

    .material-meta {
        margin-top: 18px;
        font-size: 14px;
        color: #7a7a7a;
    }


    /* =====================================================
       대화방
       ===================================================== */

    .message-card {
        background: #f5f5f7;
        border-radius: 18px;
        padding: 20px 24px;
        margin-bottom: 12px;
    }

    .message-user {
        font-size: 14px;
        font-weight: 600;
        color: #0066cc;
        margin-bottom: 6px;
    }

    .message-text {
        font-size: 17px;
        line-height: 1.47;
        color: #1d1d1f;
    }

    .message-time {
        margin-top: 10px;
        font-size: 12px;
        color: #7a7a7a;
    }


    /* =====================================================
       버튼
       ===================================================== */

    .stButton > button {
        border-radius: 9999px !important;
        min-height: 44px !important;
        padding: 8px 22px !important;
        font-size: 15px !important;
        font-weight: 400 !important;
        letter-spacing: -0.2px !important;
        transition: transform 0.12s ease !important;
    }

    .stButton > button:active {
        transform: scale(0.95);
    }

    /* Primary 버튼 */
    .stButton > button[kind="primary"] {
        background: #0066cc !important;
        color: #ffffff !important;
        border: none !important;
    }

    /* 일반 버튼 */
    .stButton > button[kind="secondary"] {
        background: #ffffff !important;
        color: #0066cc !important;
        border: 1px solid #0066cc !important;
    }


    /* =====================================================
       입력창
       ===================================================== */

    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] > div,
    .stDateInput input {
        border-radius: 11px !important;
        border: 1px solid #e0e0e0 !important;
        background: #ffffff !important;
        color: #1d1d1f !important;
        font-size: 17px !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stDateInput input:focus {
        border-color: #0071e3 !important;
        box-shadow: 0 0 0 1px #0071e3 !important;
    }


    /* =====================================================
       파일 업로더
       ===================================================== */

    [data-testid="stFileUploader"] {
        background: #f5f5f7;
        border-radius: 18px;
        padding: 8px;
    }


    /* =====================================================
       탭
       ===================================================== */

    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 1px solid #e0e0e0;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        font-weight: 600;
        color: #6e6e73;
        padding: 12px 4px;
    }

    .stTabs [aria-selected="true"] {
        color: #0066cc !important;
    }


    /* =====================================================
       사이드바 최소화
       ===================================================== */

    [data-testid="stSidebar"] {
        background: #f5f5f7;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }


    /* =====================================================
       Divider
       ===================================================== */

    hr {
        border: none !important;
        border-top: 1px solid #f0f0f0 !important;
        margin: 32px 0 !important;
    }


    /* =====================================================
       알림
       ===================================================== */

    [data-testid="stAlert"] {
        border-radius: 11px !important;
    }


    /* =====================================================
       Expander
       ===================================================== */

    [data-testid="stExpander"] {
        border: 1px solid #e0e0e0 !important;
        border-radius: 18px !important;
        background: #ffffff !important;
    }


    /* =====================================================
       Footer
       ===================================================== */

    .footer {
        background: #f5f5f7;
        padding: 64px 32px;
        text-align: center;
        margin-top: 0;
    }

    .footer-title {
        font-size: 14px;
        font-weight: 600;
        color: #333333;
    }

    .footer-text {
        margin-top: 8px;
        font-size: 12px;
        color: #7a7a7a;
        line-height: 1.5;
    }


    /* =====================================================
       반응형
       ===================================================== */

    @media (max-width: 1068px) {

        .hero-title {
            font-size: 40px;
        }

        .hero-title-dark {
            font-size: 40px;
        }

        .section-title,
        .section-title-dark {
            font-size: 34px;
        }

        .section-light,
        .section-parchment,
        .section-dark,
        .section-dark-2 {
            padding: 56px 24px;
        }
    }


    @media (max-width: 640px) {

        .block-container {
            padding-left: 12px;
            padding-right: 12px;
        }

        .top-nav {
            padding: 12px 16px;
        }

        .hero {
            padding: 56px 20px 48px 20px;
        }

        .hero-dark,
        .hero-parchment {
            padding: 48px 20px;
        }

        .hero-title {
            font-size: 34px;
            letter-spacing: -0.7px;
        }

        .hero-title-dark {
            font-size: 34px;
        }

        .hero-description,
        .hero-description-dark {
            font-size: 18px;
        }

        .section-light,
        .section-parchment,
        .section-dark,
        .section-dark-2 {
            padding: 48px 16px;
        }

        .section-title,
        .section-title-dark {
            font-size: 30px;
        }

        .info-card,
        .info-card-parchment,
        .attendance-card,
        .attendance-card-dark,
        .material-card {
            padding: 20px;
        }

        .metric-number {
            font-size: 34px;
        }
    }


    @media (max-width: 419px) {

        .hero-title {
            font-size: 28px;
        }

        .hero-title-dark {
            font-size: 28px;
        }

        .section-title,
        .section-title-dark {
            font-size: 28px;
        }

        .hero-description,
        .hero-description-dark {
            font-size: 17px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 3. 데이터베이스
# =========================================================

DB_FILE = "school.db"
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

conn = sqlite3.connect(
    DB_FILE,
    check_same_thread=False
)

cursor = conn.cursor()


# =========================================================
# 4. 테이블 생성
# =========================================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        student_number INTEGER,
        name TEXT NOT NULL
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        attendance_date TEXT NOT NULL,
        status TEXT NOT NULL,
        confirmed INTEGER DEFAULT 0,
        confirmed_by TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        UNIQUE(student_id, attendance_date)
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        filename TEXT,
        stored_filename TEXT,
        uploader_id TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """
)

conn.commit()


# =========================================================
# 5. 비밀번호
# =========================================================

def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def check_password(input_password, saved_password):
    return hash_password(input_password) == saved_password


# =========================================================
# 6. 기본 계정 생성
# =========================================================

def create_default_accounts():

    # -----------------------------------------------------
    # 선생님 계정
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT user_id
        FROM users
        WHERE user_id = ?
        """,
        ("teacher",)
    )

    if cursor.fetchone() is None:

        cursor.execute(
            """
            INSERT INTO users
            (
                user_id,
                password,
                role,
                student_number,
                name
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "teacher",
                hash_password("teacher123"),
                "teacher",
                None,
                "선생님"
            )
        )

    # -----------------------------------------------------
    # 학생 1~30번
    # -----------------------------------------------------

    for number in range(1, 31):

        student_id = f"student{number:02d}"

        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE user_id = ?
            """,
            (student_id,)
        )

        if cursor.fetchone() is None:

            cursor.execute(
                """
                INSERT INTO users
                (
                    user_id,
                    password,
                    role,
                    student_number,
                    name
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    student_id,
                    hash_password("student123"),
                    "student",
                    number,
                    f"{number}번 학생"
                )
            )

    conn.commit()


create_default_accounts()


# =========================================================
# 7. 세션 상태
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "role" not in st.session_state:
    st.session_state.role = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "student_number" not in st.session_state:
    st.session_state.student_number = None


# =========================================================
# 8. 로그인
# =========================================================

def login(user_id, password):

    if not user_id or not password:
        return False

    cursor.execute(
        """
        SELECT
            user_id,
            password,
            role,
            student_number,
            name
        FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    if user is None:
        return False

    db_user_id = user[0]
    db_password = user[1]
    db_role = user[2]
    db_student_number = user[3]
    db_name = user[4]

    if not check_password(password, db_password):
        return False

    st.session_state.logged_in = True
    st.session_state.user_id = db_user_id
    st.session_state.role = db_role
    st.session_state.student_number = db_student_number
    st.session_state.user_name = db_name

    return True


# =========================================================
# 9. 로그아웃
# =========================================================

def logout():

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.role = None
    st.session_state.user_name = None
    st.session_state.student_number = None

    st.rerun()


# =========================================================
# 10. 상단 네비게이션
# =========================================================

def show_top_nav():

    if st.session_state.logged_in:

        if st.session_state.role == "student":
            role_text = "학생"

        elif st.session_state.role == "teacher":
            role_text = "선생님"

        else:
            role_text = "사용자"

        st.markdown(
            f"""
            <div class="top-nav">
                <div class="top-nav-inner">
                    <div class="top-nav-title">
                        🏫 방과후 학습 관리
                    </div>

                    <div class="top-nav-subtitle">
                        {st.session_state.user_name} · {role_text}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="top-nav">
                <div class="top-nav-inner">
                    <div class="top-nav-title">
                        🏫 방과후 학습 관리
                    </div>

                    <div class="top-nav-subtitle">
                        After School Learning
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# 11. 로그인 화면
# =========================================================

def show_login():

    show_top_nav()

    st.markdown(
        """
        <div class="hero">

            <div class="hero-eyebrow">
                AFTER SCHOOL LEARNING
            </div>

            <h1 class="hero-title">
                방과후 학습 관리 시스템
            </h1>

            <div class="hero-description">
                방과후 자습과 야간자율학습의 출결을 관리하고
                <br>
                학습 자료를 함께 공유하는 공간입니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-parchment">',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(
        [1, 1.3, 1]
    )

    with col2:

        st.markdown(
            """
            <div style="
                text-align:center;
                margin-bottom:32px;
            ">
                <div style="
                    font-size:34px;
                    font-weight:600;
                    letter-spacing:-0.6px;
                    color:#1d1d1f;
                ">
                    로그인
                </div>

                <div style="
                    margin-top:10px;
                    font-size:17px;
                    color:#6e6e73;
                ">
                    계정 정보를 입력해주세요.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        user_id = st.text_input(
            "아이디",
            placeholder="아이디"
        )

        password = st.text_input(
            "비밀번호",
            type="password",
            placeholder="비밀번호"
        )

        if st.button(
            "로그인",
            use_container_width=True,
            type="primary"
        ):

            if login(user_id, password):

                st.success(
                    f"{st.session_state.user_name}님, 환영합니다."
                )

                st.rerun()

            else:

                st.error(
                    "아이디 또는 비밀번호가 올바르지 않습니다."
                )

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )

        with st.expander("테스트 계정 안내"):

            st.markdown(
                """
                **학생**

                아이디: `student01`  
                비밀번호: `student123`

                **선생님**

                아이디: `teacher`  
                비밀번호: `teacher123`
                """
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="footer">

            <div class="footer-title">
                방과후 학습 관리 시스템
            </div>

            <div class="footer-text">
                출결 · 학습 자료 · 공부 대화방
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 12. 학생 출결
# =========================================================

def student_attendance():

    st.markdown(
        """
        <div class="hero-parchment">

            <div class="hero-eyebrow">
                ATTENDANCE
            </div>

            <div class="hero-title"
                 style="font-size:40px;">
                나의 출결
            </div>

            <div class="hero-description">
                오늘의 출결 상태를 기록하고
                지난 출결 기록을 확인할 수 있습니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-light">',
        unsafe_allow_html=True
    )

    today = date.today().isoformat()

    st.markdown(
        """
        <div class="section-title">
            오늘 출결 신청
        </div>
        """,
        unsafe_allow_html=True
    )

    cursor.execute(
        """
        SELECT
            status,
            confirmed
        FROM attendance
        WHERE student_id = ?
        AND attendance_date = ?
        """,
        (
            st.session_state.user_id,
            today
        )
    )

    today_record = cursor.fetchone()

    current_status = None
    current_confirmed = 0

    if today_record:

        current_status = today_record[0]
        current_confirmed = today_record[1]

    if current_confirmed == 1:

        st.success(
            f"오늘 출결은 **{current_status}**로 "
            "선생님에 의해 최종 확정되었습니다."
        )

    else:

        status_options = [
            "출석",
            "지각",
            "결석"
        ]

        default_index = 0

        if current_status in status_options:

            default_index = status_options.index(
                current_status
            )

        selected_status = st.radio(
            "출결 상태를 선택하세요.",
            status_options,
            index=default_index,
            horizontal=True
        )

        if st.button(
            "오늘 출결 저장",
            type="primary"
        ):

            now = datetime.now().isoformat()

            if today_record:

                cursor.execute(
                    """
                    UPDATE attendance
                    SET
                        status = ?,
                        updated_at = ?
                    WHERE student_id = ?
                    AND attendance_date = ?
                    """,
                    (
                        selected_status,
                        now,
                        st.session_state.user_id,
                        today
                    )
                )

            else:

                cursor.execute(
                    """
                    INSERT INTO attendance
                    (
                        student_id,
                        attendance_date,
                        status,
                        confirmed,
                        confirmed_by,
                        created_at,
                        updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        st.session_state.user_id,
                        today,
                        selected_status,
                        0,
                        None,
                        now,
                        now
                    )
                )

            conn.commit()

            st.success(
                "오늘 출결이 저장되었습니다."
            )

            st.rerun()

    st.divider()

    st.markdown(
        """
        <div class="section-title">
            나의 출결 기록
        </div>
        """,
        unsafe_allow_html=True
    )

    cursor.execute(
        """
        SELECT
            attendance_date,
            status,
            confirmed
        FROM attendance
        WHERE student_id = ?
        ORDER BY attendance_date DESC
        """,
        (
            st.session_state.user_id,
        )
    )

    records = cursor.fetchall()

    if not records:

        st.info(
            "아직 출결 기록이 없습니다."
        )

    else:

        for attendance_date, status, confirmed in records:

            if confirmed:
                confirmation = "최종 확정"
            else:
                confirmation = "확인 대기"

            st.markdown(
                f"""
                <div class="attendance-card">

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                        gap:20px;
                        flex-wrap:wrap;
                    ">

                        <div>
                            <div class="student-number"
                                 style="font-size:21px;">
                                {attendance_date}
                            </div>

                            <div class="student-name">
                                {status}
                            </div>
                        </div>

                        <div style="
                            font-size:14px;
                            color:#6e6e73;
                        ">
                            {confirmation}
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# 13. 공부 자료방
# =========================================================

def study_room():

    st.markdown(
        """
        <div class="hero-dark">

            <div class="hero-eyebrow">
                STUDY SPACE
            </div>

            <div class="hero-title-dark">
                공부 자료방
            </div>

            <div class="hero-description-dark">
                학습 자료를 공유하고
                서로의 공부 내용을 자유롭게 이야기하는 공간입니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(
        [
            "공부 자료",
            "대화방"
        ]
    )

    # =====================================================
    # 자료
    # =====================================================

    with tab1:

        st.markdown(
            '<div class="section-parchment">',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="section-title">
                자료 업로드
            </div>

            <div class="section-description">
                수업 자료나 함께 공부할 수 있는 파일을 공유해주세요.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        title = st.text_input(
            "자료 제목",
            key="material_title"
        )

        description = st.text_area(
            "자료 설명",
            key="material_description"
        )

        uploaded_file = st.file_uploader(
            "파일 선택",
            key="material_file"
        )

        if st.button(
            "자료 업로드",
            type="primary"
        ):

            if not title:

                st.warning(
                    "자료 제목을 입력해주세요."
                )

            elif uploaded_file is None:

                st.warning(
                    "파일을 선택해주세요."
                )

            else:

                original_filename = uploaded_file.name

                timestamp = datetime.now().strftime(
                    "%Y%m%d%H%M%S%f"
                )

                stored_filename = (
                    f"{timestamp}_{original_filename}"
                )

                file_path = os.path.join(
                    UPLOAD_DIR,
                    stored_filename
                )

                with open(
                    file_path,
                    "wb"
                ) as f:

                    f.write(
                        uploaded_file.getbuffer()
                    )

                cursor.execute(
                    """
                    INSERT INTO materials
                    (
                        title,
                        description,
                        filename,
                        stored_filename,
                        uploader_id,
                        created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        title,
                        description,
                        original_filename,
                        stored_filename,
                        st.session_state.user_id,
                        datetime.now().isoformat()
                    )
                )

                conn.commit()

                st.success(
                    "자료가 업로드되었습니다."
                )

                st.rerun()

        st.divider()

        st.markdown(
            """
            <div class="section-title"
                 style="font-size:34px;">
                등록된 자료
            </div>
            """,
            unsafe_allow_html=True
        )

        cursor.execute(
            """
            SELECT
                id,
                title,
                description,
                filename,
                stored_filename,
                uploader_id,
                created_at
            FROM materials
            ORDER BY id DESC
            """
        )

        materials = cursor.fetchall()

        if not materials:

            st.info(
                "등록된 자료가 없습니다."
            )

        else:

            for material in materials:

                (
                    material_id,
                    title,
                    description,
                    filename,
                    stored_filename,
                    uploader_id,
                    created_at
                ) = material

                st.markdown(
                    '<div class="material-card">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="material-title">
                        📄 {title}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if description:

                    st.markdown(
                        f"""
                        <div class="material-description">
                            {description}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown(
                    f"""
                    <div class="material-meta">
                        작성자: {uploader_id}
                        &nbsp; · &nbsp;
                        파일: {filename}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                file_path = os.path.join(
                    UPLOAD_DIR,
                    stored_filename
                )

                if os.path.exists(file_path):

                    with open(
                        file_path,
                        "rb"
                    ) as file:

                        st.download_button(
                            "파일 다운로드",
                            data=file.read(),
                            file_name=filename,
                            key=f"download_{material_id}"
                        )

                else:

                    st.error(
                        "파일을 찾을 수 없습니다."
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =====================================================
    # 대화방
    # =====================================================

    with tab2:

        st.markdown(
            '<div class="section-light">',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="section-title">
                공부 대화방
            </div>

            <div class="section-description">
                공부하면서 궁금했던 점이나
                다른 친구들과 나누고 싶은 내용을 작성해보세요.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        message = st.text_area(
            "메시지를 입력하세요",
            key="chat_message"
        )

        if st.button(
            "메시지 작성",
            type="primary"
        ):

            if not message.strip():

                st.warning(
                    "메시지를 입력해주세요."
                )

            else:

                cursor.execute(
                    """
                    INSERT INTO messages
                    (
                        user_id,
                        message,
                        created_at
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        st.session_state.user_id,
                        message.strip(),
                        datetime.now().isoformat()
                    )
                )

                conn.commit()

                st.rerun()

        st.divider()

        cursor.execute(
            """
            SELECT
                user_id,
                message,
                created_at
            FROM messages
            ORDER BY id DESC
            LIMIT 100
            """
        )

        messages = cursor.fetchall()

        if not messages:

            st.info(
                "아직 대화가 없습니다."
            )

        else:

            for user_id, message, created_at in messages:

                if user_id == st.session_state.user_id:

                    name = st.session_state.user_name

                else:

                    cursor.execute(
                        """
                        SELECT name
                        FROM users
                        WHERE user_id = ?
                        """,
                        (user_id,)
                    )

                    user = cursor.fetchone()

                    name = (
                        user[0]
                        if user
                        else user_id
                    )

                st.markdown(
                    f"""
                    <div class="message-card">

                        <div class="message-user">
                            {name}
                        </div>

                        <div class="message-text">
                            {message}
                        </div>

                        <div class="message-time">
                            {created_at}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# =========================================================
# 14. 선생님 출결 관리
# =========================================================

def teacher_attendance():

    st.markdown(
        """
        <div class="hero-dark">

            <div class="hero-eyebrow">
                TEACHER
            </div>

            <div class="hero-title-dark">
                전체 출결 관리
            </div>

            <div class="hero-description-dark">
                학생들의 출결을 확인하고
                최종 상태를 확정할 수 있습니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-parchment">',
        unsafe_allow_html=True
    )

    selected_date = st.date_input(
        "확인할 날짜",
        value=date.today()
    )

    selected_date_str = selected_date.isoformat()

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # 전체 통계
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM attendance
        WHERE attendance_date = ?
        AND status = '출석'
        """,
        (selected_date_str,)
    )

    present_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM attendance
        WHERE attendance_date = ?
        AND status = '지각'
        """,
        (selected_date_str,)
    )

    late_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM attendance
        WHERE attendance_date = ?
        AND status = '결석'
        """,
        (selected_date_str,)
    )

    absent_count = cursor.fetchone()[0]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-number">
                    {present_count}
                </div>

                <div class="metric-label">
                    출석
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-number">
                    {late_count}
                </div>

                <div class="metric-label">
                    지각
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-number">
                    {absent_count}
                </div>

                <div class="metric-label">
                    결석
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # -----------------------------------------------------
    # 학생 전체 목록
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="section-title"
             style="font-size:34px;">
            학생별 출결
        </div>
        """,
        unsafe_allow_html=True
    )

    cursor.execute(
        """
        SELECT
            user_id,
            student_number,
            name
        FROM users
        WHERE role = 'student'
        ORDER BY student_number
        """
    )

    students = cursor.fetchall()

    for student_id, student_number, name in students:

        cursor.execute(
            """
            SELECT
                status,
                confirmed,
                confirmed_by
            FROM attendance
            WHERE student_id = ?
            AND attendance_date = ?
            """,
            (
                student_id,
                selected_date_str
            )
        )

        record = cursor.fetchone()

        if record:

            current_status = record[0]
            confirmed = record[1]
            confirmed_by = record[2]

        else:

            current_status = "출석"
            confirmed = 0
            confirmed_by = None

        st.markdown(
            '<div class="attendance-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="student-number">
                {student_number}번
            </div>

            <div class="student-name">
                {name}
            </div>
            """,
            unsafe_allow_html=True
        )

        status_options = [
            "출석",
            "지각",
            "결석"
        ]

        if current_status not in status_options:
            current_status = "출석"

        selected_status = st.selectbox(
            "출결 상태",
            status_options,
            index=status_options.index(
                current_status
            ),
            key=f"status_{student_id}_{selected_date_str}"
        )

        if confirmed:

            st.success(
                f"최종 확정됨 ({confirmed_by})"
            )

        else:

            st.info(
                "아직 출결이 확정되지 않았습니다."
            )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "출결 저장",
                key=f"save_{student_id}_{selected_date_str}"
            ):

                now = datetime.now().isoformat()

                if record:

                    cursor.execute(
                        """
                        UPDATE attendance
                        SET
                            status = ?,
                            updated_at = ?
                        WHERE student_id = ?
                        AND attendance_date = ?
                        """,
                        (
                            selected_status,
                            now,
                            student_id,
                            selected_date_str
                        )
                    )

                else:

                    cursor.execute(
                        """
                        INSERT INTO attendance
                        (
                            student_id,
                            attendance_date,
                            status,
                            confirmed,
                            confirmed_by,
                            created_at,
                            updated_at
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            student_id,
                            selected_date_str,
                            selected_status,
                            0,
                            None,
                            now,
                            now
                        )
                    )

                conn.commit()

                st.success(
                    f"{name} 학생의 출결을 저장했습니다."
                )

                st.rerun()

        with col2:

            if not confirmed:

                if st.button(
                    "출결 최종 확정",
                    key=f"confirm_{student_id}_{selected_date_str}",
                    type="primary"
                ):

                    now = datetime.now().isoformat()

                    if record:

                        cursor.execute(
                            """
                            UPDATE attendance
                            SET
                                status = ?,
                                confirmed = 1,
                                confirmed_by = ?,
                                updated_at = ?
                            WHERE student_id = ?
                            AND attendance_date = ?
                            """,
                            (
                                selected_status,
                                st.session_state.user_id,
                                now,
                                student_id,
                                selected_date_str
                            )
                        )

                    else:

                        cursor.execute(
                            """
                            INSERT INTO attendance
                            (
                                student_id,
                                attendance_date,
                                status,
                                confirmed,
                                confirmed_by,
                                created_at,
                                updated_at
                            )
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                student_id,
                                selected_date_str,
                                selected_status,
                                1,
                                st.session_state.user_id,
                                now,
                                now
                            )
                        )

                    conn.commit()

                    st.success(
                        f"{name} 학생의 출결을 최종 확정했습니다."
                    )

                    st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# 15. 학생 화면
# =========================================================

def student_page():

    show_top_nav()

    st.markdown(
        f"""
        <div class="hero">

            <div class="hero-eyebrow">
                STUDENT
            </div>

            <div class="hero-title">
                안녕하세요, {st.session_state.user_name}님.
            </div>

            <div class="hero-description">
                오늘의 출결을 확인하고
                공부 자료를 살펴보세요.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(
        [4, 1]
    )

    with col2:

        if st.button(
            "로그아웃",
            use_container_width=True
        ):

            logout()

    attendance_tab, study_tab = st.tabs(
        [
            "출결",
            "공부 자료방"
        ]
    )

    with attendance_tab:

        student_attendance()

    with study_tab:

        study_room()

    st.markdown(
        """
        <div class="footer">

            <div class="footer-title">
                방과후 학습 관리 시스템
            </div>

            <div class="footer-text">
                학생 학습 공간
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 16. 선생님 화면
# =========================================================

def teacher_page():

    show_top_nav()

    st.markdown(
        f"""
        <div class="hero">

            <div class="hero-eyebrow">
                TEACHER
            </div>

            <div class="hero-title">
                안녕하세요, {st.session_state.user_name}님.
            </div>

            <div class="hero-description">
                학생들의 출결과 학습 자료를 관리하세요.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(
        [4, 1]
    )

    with col2:

        if st.button(
            "로그아웃",
            use_container_width=True
        ):

            logout()

    attendance_tab, study_tab = st.tabs(
        [
            "전체 출결 관리",
            "공부 자료방"
        ]
    )

    with attendance_tab:

        teacher_attendance()

    with study_tab:

        study_room()

    st.markdown(
        """
        <div class="footer">

            <div class="footer-title">
                방과후 학습 관리 시스템
            </div>

            <div class="footer-text">
                선생님 관리 공간
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 17. 프로그램 실행
# =========================================================

if not st.session_state.logged_in:

    show_login()

else:

    if st.session_state.role == "student":

        student_page()

    elif st.session_state.role == "teacher":

        teacher_page()

    else:

        st.error(
            "알 수 없는 사용자 권한입니다."
        )

        logout()
