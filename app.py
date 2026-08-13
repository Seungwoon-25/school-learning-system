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
    layout="wide"
)


# =========================================================
# 2. 데이터베이스
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
# 3. 테이블 생성
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    student_number INTEGER,
    name TEXT NOT NULL
)
""")


cursor.execute("""
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
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    filename TEXT,
    stored_filename TEXT,
    uploader_id TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")


conn.commit()


# =========================================================
# 4. 비밀번호
# =========================================================

def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def check_password(input_password, saved_password):
    return hash_password(input_password) == saved_password


# =========================================================
# 5. 기본 계정 생성
# =========================================================

def create_default_accounts():

    # -----------------------------
    # 선생님
    # -----------------------------

    cursor.execute("""
    SELECT user_id
    FROM users
    WHERE user_id = ?
    """, ("teacher",))

    if cursor.fetchone() is None:

        cursor.execute("""
        INSERT INTO users
        (
            user_id,
            password,
            role,
            student_number,
            name
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            "teacher",
            hash_password("teacher123"),
            "teacher",
            None,
            "선생님"
        ))


    # -----------------------------
    # 학생 1~30번
    # -----------------------------

    for number in range(1, 31):

        student_id = f"student{number:02d}"

        cursor.execute("""
        SELECT user_id
        FROM users
        WHERE user_id = ?
        """, (student_id,))

        if cursor.fetchone() is None:

            cursor.execute("""
            INSERT INTO users
            (
                user_id,
                password,
                role,
                student_number,
                name
            )
            VALUES (?, ?, ?, ?, ?)
            """, (
                student_id,
                hash_password("student123"),
                "student",
                number,
                f"{number}번 학생"
            ))

    conn.commit()


create_default_accounts()


# =========================================================
# 6. 세션 상태
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
# 7. 로그인
# =========================================================

def login(user_id, password):

    if not user_id or not password:
        return False

    cursor.execute("""
    SELECT
        user_id,
        password,
        role,
        student_number,
        name
    FROM users
    WHERE user_id = ?
    """, (user_id,))

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
# 8. 로그아웃
# =========================================================

def logout():

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.role = None
    st.session_state.user_name = None
    st.session_state.student_number = None

    st.rerun()


# =========================================================
# 9. 로그인 화면
# =========================================================

def show_login():

    st.title("🏫 방과후 학습 관리 시스템")

    st.write(
        "방과후 자습 및 야간자율학습 출결·학습 자료 관리 시스템"
    )

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.subheader("🔐 로그인")

        user_id = st.text_input(
            "아이디",
            placeholder="아이디를 입력하세요"
        )

        password = st.text_input(
            "비밀번호",
            type="password",
            placeholder="비밀번호를 입력하세요"
        )

        if st.button(
            "로그인",
            use_container_width=True,
            type="primary"
        ):

            if login(user_id, password):

                st.success(
                    f"{st.session_state.user_name}님, 환영합니다!"
                )

                st.rerun()

            else:

                st.error(
                    "아이디 또는 비밀번호가 올바르지 않습니다."
                )

        st.divider()

        with st.expander("🧪 테스트 계정"):

            st.write("**학생**")
            st.code(
                "아이디: student01\n"
                "비밀번호: student123"
            )

            st.write("**선생님**")
            st.code(
                "아이디: teacher\n"
                "비밀번호: teacher123"
            )


# =========================================================
# 10. 학생 출결
# =========================================================

def student_attendance():

    st.header("📋 나의 출결")

    today = date.today().isoformat()

    st.subheader("오늘 출결 신청")

    current_status = None
    current_confirmed = 0

    cursor.execute("""
    SELECT
        status,
        confirmed
    FROM attendance
    WHERE student_id = ?
    AND attendance_date = ?
    """, (
        st.session_state.user_id,
        today
    ))

    today_record = cursor.fetchone()

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

                cursor.execute("""
                UPDATE attendance
                SET
                    status = ?,
                    updated_at = ?
                WHERE student_id = ?
                AND attendance_date = ?
                """, (
                    selected_status,
                    now,
                    st.session_state.user_id,
                    today
                ))

            else:

                cursor.execute("""
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
                """, (
                    st.session_state.user_id,
                    today,
                    selected_status,
                    0,
                    None,
                    now,
                    now
                ))

            conn.commit()

            st.success("오늘 출결이 저장되었습니다.")

            st.rerun()


    st.divider()

    st.subheader("📅 나의 출결 기록")

    cursor.execute("""
    SELECT
        attendance_date,
        status,
        confirmed
    FROM attendance
    WHERE student_id = ?
    ORDER BY attendance_date DESC
    """, (
        st.session_state.user_id,
    ))

    records = cursor.fetchall()

    if not records:

        st.info("아직 출결 기록이 없습니다.")

    else:

        for attendance_date, status, confirmed in records:

            if status == "출석":
                icon = "🟢"
            elif status == "지각":
                icon = "🟡"
            else:
                icon = "🔴"

            if confirmed:
                confirmation = "✅ 확정"
            else:
                confirmation = "⏳ 확인 대기"

            st.write(
                f"**{attendance_date}**  "
                f"{icon} {status}  "
                f"{confirmation}"
            )


# =========================================================
# 11. 공부 자료방
# =========================================================

def study_room():

    st.header("📚 공부 자료방")

    tab1, tab2 = st.tabs([
        "📁 공부 자료",
        "💬 대화방"
    ])


    # =====================================================
    # 자료
    # =====================================================

    with tab1:

        st.subheader("📤 자료 업로드")

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

                st.warning("자료 제목을 입력해주세요.")

            elif uploaded_file is None:

                st.warning("파일을 선택해주세요.")

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

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                cursor.execute("""
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
                """, (
                    title,
                    description,
                    original_filename,
                    stored_filename,
                    st.session_state.user_id,
                    datetime.now().isoformat()
                ))

                conn.commit()

                st.success("자료가 업로드되었습니다.")

                st.rerun()


        st.divider()

        st.subheader("📚 등록된 자료")

        cursor.execute("""
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
        """)

        materials = cursor.fetchall()

        if not materials:

            st.info("등록된 자료가 없습니다.")

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

                with st.container(border=True):

                    st.markdown(
                        f"### 📄 {title}"
                    )

                    if description:

                        st.write(description)

                    st.caption(
                        f"작성자: {uploader_id} | "
                        f"파일: {filename}"
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
                                "⬇️ 파일 다운로드",
                                data=file.read(),
                                file_name=filename,
                                key=f"download_{material_id}"
                            )

                    else:

                        st.error(
                            "파일을 찾을 수 없습니다."
                        )


    # =====================================================
    # 대화방
    # =====================================================

    with tab2:

        st.subheader("💬 공부 대화방")

        message = st.text_area(
            "메시지를 입력하세요",
            key="chat_message"
        )

        if st.button(
            "메시지 작성",
            type="primary"
        ):

            if not message.strip():

                st.warning("메시지를 입력해주세요.")

            else:

                cursor.execute("""
                INSERT INTO messages
                (
                    user_id,
                    message,
                    created_at
                )
                VALUES (?, ?, ?)
                """, (
                    st.session_state.user_id,
                    message.strip(),
                    datetime.now().isoformat()
                ))

                conn.commit()

                st.rerun()


        st.divider()

        cursor.execute("""
        SELECT
            user_id,
            message,
            created_at
        FROM messages
        ORDER BY id DESC
        LIMIT 100
        """)

        messages = cursor.fetchall()

        if not messages:

            st.info("아직 대화가 없습니다.")

        else:

            for user_id, message, created_at in messages:

                if user_id == st.session_state.user_id:
                    name = st.session_state.user_name
                else:
                    cursor.execute("""
                    SELECT name
                    FROM users
                    WHERE user_id = ?
                    """, (user_id,))

                    user = cursor.fetchone()

                    name = user[0] if user else user_id

                st.markdown(
                    f"**{name}**  \n"
                    f"{message}"
                )

                st.caption(created_at)

                st.divider()


# =========================================================
# 12. 선생님 출결 관리
# =========================================================

def teacher_attendance():

    st.header("📊 전체 출결 관리")

    selected_date = st.date_input(
        "확인할 날짜",
        value=date.today()
    )

    selected_date_str = selected_date.isoformat()


    # -----------------------------------------------------
    # 전체 통계
    # -----------------------------------------------------

    cursor.execute("""
    SELECT
        COUNT(*)
    FROM attendance
    WHERE attendance_date = ?
    AND status = '출석'
    """, (selected_date_str,))

    present_count = cursor.fetchone()[0]


    cursor.execute("""
    SELECT
        COUNT(*)
    FROM attendance
    WHERE attendance_date = ?
    AND status = '지각'
    """, (selected_date_str,))

    late_count = cursor.fetchone()[0]


    cursor.execute("""
    SELECT
        COUNT(*)
    FROM attendance
    WHERE attendance_date = ?
    AND status = '결석'
    """, (selected_date_str,))

    absent_count = cursor.fetchone()[0]


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🟢 출석",
            present_count
        )

    with col2:
        st.metric(
            "🟡 지각",
            late_count
        )

    with col3:
        st.metric(
            "🔴 결석",
            absent_count
        )


    st.divider()


    # -----------------------------------------------------
    # 학생 전체 목록
    # -----------------------------------------------------

    cursor.execute("""
    SELECT
        user_id,
        student_number,
        name
    FROM users
    WHERE role = 'student'
    ORDER BY student_number
    """)

    students = cursor.fetchall()


    for student_id, student_number, name in students:

        cursor.execute("""
        SELECT
            status,
            confirmed,
            confirmed_by
        FROM attendance
        WHERE student_id = ?
        AND attendance_date = ?
        """, (
            student_id,
            selected_date_str
        ))

        record = cursor.fetchone()

        if record:

            current_status = record[0]
            confirmed = record[1]
            confirmed_by = record[2]

        else:

            current_status = "출석"
            confirmed = 0
            confirmed_by = None


        with st.container(border=True):

            st.markdown(
                f"### {student_number}번 — {name}"
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
                    f"✅ 최종 확정됨"
                    f" ({confirmed_by})"
                )

            else:

                st.warning(
                    "⏳ 아직 출결이 확정되지 않았습니다."
                )


            col1, col2 = st.columns(2)


            with col1:

                if st.button(
                    "💾 출결 저장",
                    key=f"save_{student_id}_{selected_date_str}"
                ):

                    now = datetime.now().isoformat()

                    if record:

                        cursor.execute("""
                        UPDATE attendance
                        SET
                            status = ?,
                            updated_at = ?
                        WHERE student_id = ?
                        AND attendance_date = ?
                        """, (
                            selected_status,
                            now,
                            student_id,
                            selected_date_str
                        ))

                    else:

                        cursor.execute("""
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
                        """, (
                            student_id,
                            selected_date_str,
                            selected_status,
                            0,
                            None,
                            now,
                            now
                        ))

                    conn.commit()

                    st.success(
                        f"{name} 학생의 출결을 저장했습니다."
                    )

                    st.rerun()


            with col2:

                if not confirmed:

                    if st.button(
                        "✅ 출결 최종 확정",
                        key=f"confirm_{student_id}_{selected_date_str}"
                    ):

                        now = datetime.now().isoformat()

                        if record:

                            cursor.execute("""
                            UPDATE attendance
                            SET
                                status = ?,
                                confirmed = 1,
                                confirmed_by = ?,
                                updated_at = ?
                            WHERE student_id = ?
                            AND attendance_date = ?
                            """, (
                                selected_status,
                                st.session_state.user_id,
                                now,
                                student_id,
                                selected_date_str
                            ))

                        else:

                            cursor.execute("""
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
                            """, (
                                student_id,
                                selected_date_str,
                                selected_status,
                                1,
                                st.session_state.user_id,
                                now,
                                now
                            ))

                        conn.commit()

                        st.success(
                            f"{name} 학생의 출결을 최종 확정했습니다."
                        )

                        st.rerun()


# =========================================================
# 13. 학생 화면
# =========================================================

def student_page():

    st.sidebar.title("👨‍🎓 학생")

    st.sidebar.write(
        f"**{st.session_state.user_name}**"
    )

    st.sidebar.write(
        f"{st.session_state.student_number}번"
    )

    if st.sidebar.button(
        "🚪 로그아웃",
        use_container_width=True
    ):

        logout()


    st.title("🏫 학생 학습 관리")

    attendance_tab, study_tab = st.tabs([
        "📋 출결",
        "📚 공부 자료방"
    ])


    with attendance_tab:
        student_attendance()


    with study_tab:
        study_room()


# =========================================================
# 14. 선생님 화면
# =========================================================

def teacher_page():

    st.sidebar.title("👨‍🏫 선생님")

    st.sidebar.write(
        f"**{st.session_state.user_name}**"
    )

    if st.sidebar.button(
        "🚪 로그아웃",
        use_container_width=True
    ):

        logout()


    st.title("🏫 선생님 관리 시스템")

    attendance_tab, study_tab = st.tabs([
        "📊 전체 출결 관리",
        "📚 공부 자료방"
    ])


    with attendance_tab:
        teacher_attendance()


    with study_tab:
        study_room()


# =========================================================
# 15. 프로그램 실행
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
