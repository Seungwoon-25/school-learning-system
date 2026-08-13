import streamlit as st
import sqlite3
from datetime import date, datetime


# =========================================================
# 1. 기본 설정
# =========================================================

st.set_page_config(
    page_title="학교 학습 관리 시스템",
    page_icon="🏫",
    layout="wide"
)


# =========================================================
# 2. 데이터베이스
# =========================================================

conn = sqlite3.connect(
    "school_system.db",
    check_same_thread=False
)

cursor = conn.cursor()


# =========================================================
# 3. 데이터베이스 테이블 생성
# =========================================================

# 사용자
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    student_number INTEGER,
    name TEXT NOT NULL
)
""")


# 출결
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    attendance_date TEXT,
    student_id TEXT,
    student_number INTEGER,
    status TEXT,
    submitted_by TEXT,
    confirmed INTEGER DEFAULT 0,
    PRIMARY KEY (attendance_date, student_id)
)
""")


# 학습 자료
cursor.execute("""
CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    subject TEXT,
    description TEXT,
    file_name TEXT,
    author_id TEXT,
    author_name TEXT,
    upload_date TEXT
)
""")


# 공지사항
cursor.execute("""
CREATE TABLE IF NOT EXISTS notices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    author_id TEXT,
    author_name TEXT,
    created_date TEXT
)
""")


# 게시판
cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    author_id TEXT,
    author_name TEXT,
    created_date TEXT
)
""")


conn.commit()


# =========================================================
# 4. 초기 계정 생성
# =========================================================

# 선생님 계정이 없다면 생성
cursor.execute("""
SELECT * FROM users
WHERE user_id = ?
""", ("teacher",))

teacher_exists = cursor.fetchone()


if teacher_exists is None:

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
        "teacher123",
        "teacher",
        None,
        "선생님"
    ))


# 학생 1~30번 계정 생성
for number in range(1, 31):

    student_id = f"student{number:02d}"

    cursor.execute("""
    SELECT * FROM users
    WHERE user_id = ?
    """, (student_id,))

    exists = cursor.fetchone()


    if exists is None:

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
            "student123",
            "student",
            number,
            f"{number}번 학생"
        ))


conn.commit()


# =========================================================
# 5. 로그인 상태
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "student_number" not in st.session_state:
    st.session_state.student_number = None


# =========================================================
# 6. 로그인 함수
# =========================================================

def login(user_id, password):

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


    if db_password != password:
        return False


    st.session_state.logged_in = True
    st.session_state.role = db_role
    st.session_state.user_id = db_user_id
    st.session_state.user_name = db_name
    st.session_state.student_number = db_student_number

    return True


# =========================================================
# 7. 로그아웃
# =========================================================

def logout():

    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.student_number = None

    st.rerun()


# =========================================================
# 8. 로그인 화면
# =========================================================

if not st.session_state.logged_in:

    st.title("🏫 학교 학습 관리 시스템")

    st.write(
        "방과후 및 야간자율학습을 위한 학습 관리 공간"
    )

    st.divider()

    st.header("🔐 로그인")

    user_id = st.text_input(
        "아이디"
    )

    password = st.text_input(
        "비밀번호",
        type="password"
    )


    if st.button("로그인"):

        if login(user_id, password):

            st.rerun()

        else:

            st.error(
                "아이디 또는 비밀번호가 올바르지 않습니다."
            )


# =========================================================
# 9. 로그인 이후
# =========================================================

else:

    st.title("🏫 학교 학습 관리 시스템")

    st.caption(
        f"현재 로그인: {st.session_state.user_name}"
    )


    # =====================================================
    # 학생
    # =====================================================

    if st.session_state.role == "student":

        menu = st.radio(
            "메뉴",
            [
                "📋 내 출결",
                "📚 학습 자료실",
                "📢 공지사항",
                "💬 학습 게시판",
                "🤖 AI 학습 도우미"
            ],
            horizontal=True
        )

        st.divider()


        # =================================================
        # 학생 출결
        # =================================================

        if menu == "📋 내 출결":

            st.header("📋 내 출결")

            st.write(
                f"학생 번호: **{st.session_state.student_number}번**"
            )


            # -------------------------------
            # 오늘 출결 제출
            # -------------------------------

            st.subheader("📝 오늘의 출결 제출")

            today = date.today()

            status = st.radio(
                "현재 출결 상태를 선택하세요.",
                [
                    "🟢 출석",
                    "🟡 지각",
                    "🔴 결석"
                ],
                horizontal=True
            )


            if st.button("출결 제출"):

                cursor.execute("""
                INSERT OR REPLACE INTO attendance
                (
                    attendance_date,
                    student_id,
                    student_number,
                    status,
                    submitted_by,
                    confirmed
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    str(today),
                    st.session_state.user_id,
                    st.session_state.student_number,
                    status,
                    "student",
                    0
                ))

                conn.commit()

                st.success(
                    "출결이 제출되었습니다. 선생님의 확인을 기다리고 있습니다."
                )


            st.divider()


            # -------------------------------
            # 내 출결 기록
            # -------------------------------

            st.subheader("📅 내 출결 기록")


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


            if records:

                for record in records:

                    attendance_date = record[0]
                    status = record[1]
                    confirmed = record[2]


                    if confirmed == 1:

                        check_text = "✅ 선생님 확인"

                    else:

                        check_text = "⏳ 확인 대기"


                    st.write(
                        f"**{attendance_date}** | "
                        f"{status} | {check_text}"
                    )

            else:

                st.info(
                    "아직 출결 기록이 없습니다."
                )


        # =================================================
        # 학습 자료실
        # =================================================

        elif menu == "📚 학습 자료실":

            st.header("📚 학습 자료실")

            st.write(
                "학생과 선생님이 학습 자료를 공유하는 공간입니다."
            )


            # -------------------------------
            # 자료 업로드
            # -------------------------------

            st.subheader("📤 학습 자료 공유")


            title = st.text_input(
                "자료 제목"
            )


            subject = st.selectbox(
                "과목",
                [
                    "국어",
                    "영어",
                    "수학",
                    "물리학",
                    "화학",
                    "생명과학",
                    "지구과학",
                    "기타"
                ]
            )


            description = st.text_area(
                "자료 설명"
            )


            uploaded_file = st.file_uploader(
                "파일 선택",
                type=[
                    "pdf",
                    "docx",
                    "pptx",
                    "xlsx",
                    "txt",
                    "png",
                    "jpg",
                    "jpeg"
                ]
            )


            if st.button("📤 자료 등록"):

                if title and uploaded_file:

                    cursor.execute("""
                    INSERT INTO materials
                    (
                        title,
                        subject,
                        description,
                        file_name,
                        author_id,
                        author_name,
                        upload_date
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        title,
                        subject,
                        description,
                        uploaded_file.name,
                        st.session_state.user_id,
                        st.session_state.user_name,
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M"
                        )
                    ))

                    conn.commit()

                    st.success(
                        "학습 자료가 등록되었습니다."
                    )

                else:

                    st.warning(
                        "자료 제목과 파일을 입력해주세요."
                    )


            st.divider()


            # -------------------------------
            # 자료 목록
            # -------------------------------

            st.subheader("📚 공유된 학습 자료")


            cursor.execute("""
            SELECT
                title,
                subject,
                description,
                author_name,
                upload_date,
                file_name
            FROM materials
            ORDER BY id DESC
            """)


            materials = cursor.fetchall()


            if materials:

                for material in materials:

                    with st.expander(
                        f"📄 {material[0]}"
                    ):

                        st.write(
                            f"**과목:** {material[1]}"
                        )

                        st.write(
                            f"**설명:** {material[2]}"
                        )

                        st.write(
                            f"**작성자:** {material[3]}"
                        )

                        st.caption(
                            f"등록일: {material[4]}"
                        )

                        st.caption(
                            f"파일: {material[5]}"
                        )

            else:

                st.info(
                    "아직 공유된 자료가 없습니다."
                )


        # =================================================
        # 공지사항
        # =================================================

        elif menu == "📢 공지사항":

            st.header("📢 공지사항")


            cursor.execute("""
            SELECT
                title,
                content,
                author_name,
                created_date
            FROM notices
            ORDER BY id DESC
            """)


            notices = cursor.fetchall()


            if notices:

                for notice in notices:

                    with st.expander(
                        f"📢 {notice[0]}"
                    ):

                        st.write(
                            notice[1]
                        )

                        st.caption(
                            f"작성자: {notice[2]} | "
                            f"{notice[3]}"
                        )

            else:

                st.info(
                    "등록된 공지사항이 없습니다."
                )


        # =================================================
        # 학습 게시판
        # =================================================

        elif menu == "💬 학습 게시판":

            st.header("💬 학습 게시판")

            st.write(
                "학생과 선생님이 학습에 관해 자유롭게 이야기할 수 있습니다."
            )


            # -------------------------------
            # 글 작성
            # -------------------------------

            st.subheader("✏️ 글 작성")


            post_title = st.text_input(
                "제목"
            )


            post_content = st.text_area(
                "내용"
            )


            if st.button("📝 게시글 등록"):

                if post_title and post_content:

                    cursor.execute("""
                    INSERT INTO posts
                    (
                        title,
                        content,
                        author_id,
                        author_name,
                        created_date
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """, (
                        post_title,
                        post_content,
                        st.session_state.user_id,
                        st.session_state.user_name,
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M"
                        )
                    ))

                    conn.commit()

                    st.success(
                        "게시글이 등록되었습니다."
                    )

                else:

                    st.warning(
                        "제목과 내용을 입력해주세요."
                    )


            st.divider()


            # -------------------------------
            # 게시글 목록
            # -------------------------------

            st.subheader("📚 학습 이야기")


            cursor.execute("""
            SELECT
                title,
                content,
                author_name,
                created_date
            FROM posts
            ORDER BY id DESC
            """)


            posts = cursor.fetchall()


            if posts:

                for post in posts:

                    with st.expander(
                        f"💬 {post[0]}"
                    ):

                        st.write(
                            post[1]
                        )

                        st.caption(
                            f"작성자: {post[2]} | "
                            f"{post[3]}"
                        )

            else:

                st.info(
                    "아직 게시글이 없습니다."
                )


        # =================================================
        # AI
        # =================================================

        elif menu == "🤖 AI 학습 도우미":

            st.header("🤖 AI 학습 도우미")

            st.info(
                "🚧 다음 단계에서 UPSTAGE API를 연결합니다."
            )


    # =====================================================
    # 선생님
    # =====================================================

    elif st.session_state.role == "teacher":

        menu = st.radio(
            "메뉴",
            [
                "📋 전체 출결 관리",
                "📚 학습 자료실",
                "📢 공지사항",
                "💬 학습 게시판",
                "🤖 AI 학습 도우미"
            ],
            horizontal=True
        )

        st.divider()


        # =================================================
        # 전체 출결 관리
        # =================================================

        if menu == "📋 전체 출결 관리":

            st.header("📋 전체 학생 출결 관리")


            selected_date = st.date_input(
                "출결 날짜",
                value=date.today()
            )


            date_text = str(selected_date)


            cursor.execute("""
            SELECT
                student_number,
                status,
                confirmed
            FROM attendance
            WHERE attendance_date = ?
            ORDER BY student_number
            """, (
                date_text,
            ))


            attendance_records = cursor.fetchall()


            if attendance_records:

                for record in attendance_records:

                    student_number = record[0]
                    status = record[1]
                    confirmed = record[2]


                    if confirmed == 1:

                        confirmation = "✅ 확인"

                    else:

                        confirmation = "⏳ 학생 제출"


                    st.write(
                        f"**{student_number}번** | "
                        f"{status} | {confirmation}"
                    )


                st.divider()


                st.subheader("📊 출결 통계")


                statuses = [
                    record[1]
                    for record in attendance_records
                ]


                present = statuses.count("🟢 출석")
                late = statuses.count("🟡 지각")
                absent = statuses.count("🔴 결석")


                col1, col2, col3 = st.columns(3)


                col1.metric(
                    "🟢 출석",
                    f"{present}명"
                )


                col2.metric(
                    "🟡 지각",
                    f"{late}명"
                )


                col3.metric(
                    "🔴 결석",
                    f"{absent}명"
                )


                st.divider()


                # -----------------------------------------
                # 선생님 확인
                # -----------------------------------------

                student_number = st.number_input(
                    "확인할 학생 번호",
                    min_value=1,
                    max_value=30,
                    step=1
                )


                if st.button(
                    "✅ 출결 확인 처리"
                ):

                    cursor.execute("""
                    UPDATE attendance
                    SET confirmed = 1
                    WHERE attendance_date = ?
                    AND student_number = ?
                    """, (
                        date_text,
                        student_number
                    ))


                    conn.commit()


                    st.success(
                        f"{student_number}번 학생의 출결을 확인했습니다."
                    )

                    st.rerun()


            else:

                st.info(
                    "선택한 날짜의 출결 기록이 없습니다."
                )


        # =================================================
        # 선생님 자료실
        # =================================================

        elif menu == "📚 학습 자료실":

            st.header("📚 학습 자료실")

            st.write(
                "학생과 선생님이 함께 자료를 공유합니다."
            )

            st.info(
                "자료 업로드 기능은 학생 자료실과 동일한 구조로 추가할 수 있습니다."
            )


        # =================================================
        # 선생님 공지사항
        # =================================================

        elif menu == "📢 공지사항":

            st.header("📢 공지사항 관리")


            notice_title = st.text_input(
                "공지 제목"
            )


            notice_content = st.text_area(
                "공지 내용"
            )


            if st.button("📢 공지 등록"):

                if notice_title and notice_content:

                    cursor.execute("""
                    INSERT INTO notices
                    (
                        title,
                        content,
                        author_id,
                        author_name,
                        created_date
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """, (
                        notice_title,
                        notice_content,
                        st.session_state.user_id,
                        st.session_state.user_name,
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M"
                        )
                    ))


                    conn.commit()


                    st.success(
                        "공지사항이 등록되었습니다."
                    )

                else:

                    st.warning(
                        "제목과 내용을 입력해주세요."
                    )


        # =================================================
        # 선생님 게시판
        # =================================================

        elif menu == "💬 학습 게시판":

            st.header("💬 학습 게시판 관리")

            st.write(
                "학생들과 학습 내용을 공유하고 대화할 수 있습니다."
            )


            cursor.execute("""
            SELECT
                title,
                content,
                author_name,
                created_date
            FROM posts
            ORDER BY id DESC
            """)


            posts = cursor.fetchall()


            if posts:

                for post in posts:

                    with st.expander(
                        f"💬 {post[0]}"
                    ):

                        st.write(
                            post[1]
                        )

                        st.caption(
                            f"작성자: {post[2]} | "
                            f"{post[3]}"
                        )

            else:

                st.info(
                    "게시글이 없습니다."
                )


        # =================================================
        # AI
        # =================================================

        elif menu == "🤖 AI 학습 도우미":

            st.header("🤖 AI 학습 도우미")

            st.info(
                "🚧 UPSTAGE API 연결 예정"
            )


    # =====================================================
    # 로그아웃
    # =====================================================

    st.divider()


    if st.button("🚪 로그아웃"):

        logout()
