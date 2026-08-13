import streamlit as st
import sqlite3
import os
import hashlib
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
# 2. 파일 저장 폴더
# =========================================================

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# =========================================================
# 3. 데이터베이스
# =========================================================

conn = sqlite3.connect(
    "school_system.db",
    check_same_thread=False
)

cursor = conn.cursor()


# =========================================================
# 4. 테이블 생성
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
    file_path TEXT,
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


# 학습 게시판
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
# 5. 비밀번호 암호화 함수
# =========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# =========================================================
# 6. 초기 계정 생성
# =========================================================

teacher_password = hash_password("teacher123")

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
        teacher_password,
        "teacher",
        None,
        "선생님"
    ))


# 학생 1~30번
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


# =========================================================
# 7. 세션 상태
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
# 8. 로그인
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

    if hash_password(password) != user[1]:
        return False

    st.session_state.logged_in = True
    st.session_state.user_id = user[0]
    st.session_state.role = user[2]
    st.session_state.student_number = user[3]
    st.session_state.user_name = user[4]

    return True


# =========================================================
# 9. 로그아웃
# =========================================================

def logout():

    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.student_number = None

    st.rerun()


# =========================================================
# 10. 로그인 화면
# =========================================================

if not st.session_state.logged_in:

    st.title("🏫 학교 학습 관리 시스템")

    st.write(
        "방과후 및 야간자율학습을 위한 학습 관리 공간"
    )

    st.divider()

    st.header("🔐 로그인")

    login_type = st.radio(
        "접속 유형",
        ["👨‍🎓 학생", "👨‍🏫 선생님"],
        horizontal=True
    )

    user_id = st.text_input(
        "아이디"
    )

    password = st.text_input(
        "비밀번호",
        type="password"
    )

    if st.button("🔐 로그인"):

        if login(user_id, password):

            # 선택한 화면과 실제 계정의 역할이 같은지 확인
            if login_type == "👨‍🎓 학생" and st.session_state.role != "student":

                st.session_state.logged_in = False

                st.error(
                    "학생 계정으로 로그인해주세요."
                )

            elif login_type == "👨‍🏫 선생님" and st.session_state.role != "teacher":

                st.session_state.logged_in = False

                st.error(
                    "선생님 계정으로 로그인해주세요."
                )

            else:

                st.rerun()

        else:

            st.error(
                "아이디 또는 비밀번호가 올바르지 않습니다."
            )


# =========================================================
# 11. 로그인 후
# =========================================================

else:

    st.title("🏫 학교 학습 관리 시스템")

    st.caption(
        f"로그인 사용자: {st.session_state.user_name}"
    )


    # =====================================================
    # 학생 화면
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
                f"**{st.session_state.student_number}번 학생**"
            )

            today = date.today()

            st.subheader("📝 오늘의 출결")

            status = st.radio(
                "출결 상태",
                [
                    "🟢 출석",
                    "🟡 지각",
                    "🔴 결석"
                ],
                horizontal=True
            )


            if st.button("💾 출결 제출"):

                cursor.execute("""
                INSERT OR REPLACE INTO attendance
                (
                    attendance_date,
                    student_id,
                    student_number,
                    status,
                    confirmed
                )
                VALUES (?, ?, ?, ?, ?)
                """, (
                    str(today),
                    st.session_state.user_id,
                    st.session_state.student_number,
                    status,
                    0
                ))

                conn.commit()

                st.success(
                    "출결이 제출되었습니다."
                )


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


            if records:

                for record in records:

                    attendance_date = record[0]
                    attendance_status = record[1]
                    confirmed = record[2]

                    if confirmed:

                        confirmation = "✅ 선생님 확인"

                    else:

                        confirmation = "⏳ 확인 대기"


                    st.write(
                        f"**{attendance_date}**  |  "
                        f"{attendance_status}  |  "
                        f"{confirmation}"
                    )

            else:

                st.info(
                    "출결 기록이 없습니다."
                )


        # =================================================
        # 학생 자료실
        # =================================================

        elif menu == "📚 학습 자료실":

            st.header("📚 학습 자료실")

            st.write(
                "학생과 선생님이 학습 자료를 공유할 수 있습니다."
            )

            st.subheader("📤 학습 자료 업로드")


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


            if st.button("📤 자료 업로드"):

                if not title:

                    st.warning(
                        "자료 제목을 입력해주세요."
                    )

                elif uploaded_file is None:

                    st.warning(
                        "파일을 선택해주세요."
                    )

                else:

                    # 파일명 앞에 시간 정보를 붙여 중복 방지
                    timestamp = datetime.now().strftime(
                        "%Y%m%d%H%M%S"
                    )

                    safe_filename = (
                        f"{timestamp}_"
                        f"{uploaded_file.name}"
                    )

                    file_path = os.path.join(
                        UPLOAD_FOLDER,
                        safe_filename
                    )


                    # 실제 파일 저장
                    with open(
                        file_path,
                        "wb"
                    ) as f:

                        f.write(
                            uploaded_file.getbuffer()
                        )


                    # DB 저장
                    cursor.execute("""
                    INSERT INTO materials
                    (
                        title,
                        subject,
                        description,
                        file_name,
                        file_path,
                        author_id,
                        author_name,
                        upload_date
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        title,
                        subject,
                        description,
                        uploaded_file.name,
                        file_path,
                        st.session_state.user_id,
                        st.session_state.user_name,
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M"
                        )
                    ))

                    conn.commit()


                    st.success(
                        "✅ 학습 자료가 업로드되었습니다."
                    )

                    st.rerun()


            st.divider()

            st.subheader("📚 공유된 학습 자료")


            cursor.execute("""
            SELECT
                id,
                title,
                subject,
                description,
                file_name,
                file_path,
                author_name,
                upload_date
            FROM materials
            ORDER BY id DESC
            """)

            materials = cursor.fetchall()


            if materials:

                for material in materials:

                    material_id = material[0]
                    title = material[1]
                    subject = material[2]
                    description = material[3]
                    file_name = material[4]
                    file_path = material[5]
                    author_name = material[6]
                    upload_date = material[7]


                    with st.expander(
                        f"📄 {title}"
                    ):

                        st.write(
                            f"**과목:** {subject}"
                        )

                        st.write(
                            f"**설명:** {description}"
                        )

                        st.write(
                            f"**작성자:** {author_name}"
                        )

                        st.caption(
                            f"등록일: {upload_date}"
                        )


                        # 파일이 실제로 존재하는 경우
                        if os.path.exists(file_path):

                            with open(
                                file_path,
                                "rb"
                            ) as file:

                                st.download_button(
                                    label="⬇️ 파일 다운로드",
                                    data=file.read(),
                                    file_name=file_name,
                                    key=f"download_{material_id}"
                                )

                        else:

                            st.error(
                                "파일을 찾을 수 없습니다."
                            )

            else:

                st.info(
                    "아직 공유된 학습 자료가 없습니다."
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
                            f"{notice[2]} | {notice[3]}"
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
                "학습 내용을 서로 공유하고 질문하는 공간입니다."
            )


            post_title = st.text_input(
                "게시글 제목"
            )

            post_content = st.text_area(
                "게시글 내용"
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

                    st.rerun()

                else:

                    st.warning(
                        "제목과 내용을 모두 입력해주세요."
                    )


            st.divider()

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
                            f"{post[2]} | {post[3]}"
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
                "UPSTAGE API 연결 예정입니다."
            )


    # =====================================================
    # 선생님 화면
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
        # 전체 출결
        # =================================================

        if menu == "📋 전체 출결 관리":

            st.header("📋 전체 학생 출결 관리")


            selected_date = st.date_input(
                "출결 날짜",
                value=date.today()
            )

            date_text = str(selected_date)


            # ---------------------------------------------
            # 모든 학생 가져오기
            # ---------------------------------------------

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


            # ---------------------------------------------
            # 해당 날짜 출결 가져오기
            # ---------------------------------------------

            cursor.execute("""
            SELECT
                student_id,
                status,
                confirmed
            FROM attendance
            WHERE attendance_date = ?
            """, (date_text,))

            records = cursor.fetchall()


            attendance_dict = {

                record[0]: {
                    "status": record[1],
                    "confirmed": record[2]
                }

                for record in records
            }


            # ---------------------------------------------
            # 학생별 관리
            # ---------------------------------------------

            st.subheader(
                f"📅 {selected_date}"
            )


            for student in students:

                student_id = student[0]
                student_number = student[1]
                student_name = student[2]


                current = attendance_dict.get(
                    student_id
                )


                if current:

                    current_status = current["status"]

                    confirmed = current["confirmed"]

                else:

                    current_status = "🟢 출석"

                    confirmed = 0


                options = [
                    "🟢 출석",
                    "🟡 지각",
                    "🔴 결석"
                ]


                index = options.index(
                    current_status
                )


                col1, col2, col3 = st.columns(
                    [1, 2, 1]
                )


                with col1:

                    st.write(
                        f"**{student_number}번**"
                    )


                with col2:

                    new_status = st.selectbox(
                        "출결",
                        options,
                        index=index,
                        key=f"teacher_{date_text}_{student_id}"
                    )


                with col3:

                    if confirmed:

                        st.success(
                            "확인됨"
                        )

                    else:

                        st.warning(
                            "미확인"
                        )


                # 변경된 값을 세션에 저장
                if (
                    f"edit_{student_id}"
                    not in st.session_state
                ):

                    st.session_state[
                        f"edit_{student_id}"
                    ] = new_status


                st.session_state[
                    f"edit_{student_id}"
                ] = new_status


            st.divider()


            # ---------------------------------------------
            # 전체 저장
            # ---------------------------------------------

            if st.button(
                "💾 전체 출결 저장"
            ):

                for student in students:

                    student_id = student[0]
                    student_number = student[1]

                    new_status = st.session_state.get(
                        f"edit_{student_id}",
                        "🟢 출석"
                    )


                    cursor.execute("""
                    INSERT OR REPLACE INTO attendance
                    (
                        attendance_date,
                        student_id,
                        student_number,
                        status,
                        confirmed
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """, (
                        date_text,
                        student_id,
                        student_number,
                        new_status,
                        1
                    ))


                conn.commit()


                st.success(
                    "✅ 전체 학생 출결이 저장되었습니다."
                )

                st.rerun()


            # ---------------------------------------------
            # 통계
            # ---------------------------------------------

            cursor.execute("""
            SELECT status
            FROM attendance
            WHERE attendance_date = ?
            """, (date_text,))

            statuses = [
                row[0]
                for row in cursor.fetchall()
            ]


            st.subheader("📊 출결 통계")


            col1, col2, col3 = st.columns(3)


            col1.metric(
                "🟢 출석",
                f"{statuses.count('🟢 출석')}명"
            )


            col2.metric(
                "🟡 지각",
                f"{statuses.count('🟡 지각')}명"
            )


            col3.metric(
                "🔴 결석",
                f"{statuses.count('🔴 결석')}명"
            )


        # =================================================
        # 선생님 자료실
        # =================================================

        elif menu == "📚 학습 자료실":

            st.header("📚 학습 자료실")

            st.write(
                "학생과 선생님 모두 자료를 공유할 수 있습니다."
            )


            # 학생 화면과 동일한 업로드 기능
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
                ],
                key="teacher_subject"
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
                ],
                key="teacher_file"
            )


            if st.button(
                "📤 자료 업로드"
            ):

                if title and uploaded_file:

                    timestamp = datetime.now().strftime(
                        "%Y%m%d%H%M%S"
                    )

                    safe_filename = (
                        f"{timestamp}_"
                        f"{uploaded_file.name}"
                    )

                    file_path = os.path.join(
                        UPLOAD_FOLDER,
                        safe_filename
                    )


                    with open(
                        file_path,
                        "wb"
                    ) as f:

                        f.write(
                            uploaded_file.getbuffer()
                        )


                    cursor.execute("""
                    INSERT INTO materials
                    (
                        title,
                        subject,
                        description,
                        file_name,
                        file_path,
                        author_id,
                        author_name,
                        upload_date
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        title,
                        subject,
                        description,
                        uploaded_file.name,
                        file_path,
                        st.session_state.user_id,
                        st.session_state.user_name,
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M"
                        )
                    ))


                    conn.commit()


                    st.success(
                        "✅ 자료가 업로드되었습니다."
                    )

                    st.rerun()

                else:

                    st.warning(
                        "자료 제목과 파일을 입력해주세요."
                    )


            st.divider()

            st.subheader(
                "📚 공유된 자료"
            )


            cursor.execute("""
            SELECT
                id,
                title,
                subject,
                description,
                file_name,
                file_path,
                author_name,
                upload_date
            FROM materials
            ORDER BY id DESC
            """)


            materials = cursor.fetchall()


            if materials:

                for material in materials:

                    with st.expander(
                        f"📄 {material[1]}"
                    ):

                        st.write(
                            f"과목: {material[2]}"
                        )

                        st.write(
                            material[3]
                        )

                        st.caption(
                            f"작성자: {material[6]} | "
                            f"{material[7]}"
                        )


                        if os.path.exists(
                            material[5]
                        ):

                            with open(
                                material[5],
                                "rb"
                            ) as f:

                                st.download_button(
                                    "⬇️ 다운로드",
                                    f.read(),
                                    file_name=material[4],
                                    key=f"teacher_download_{material[0]}"
                                )

            else:

                st.info(
                    "등록된 자료가 없습니다."
                )


        # =================================================
        # 공지사항
        # =================================================

        elif menu == "📢 공지사항":

            st.header("📢 공지사항")


            title = st.text_input(
                "공지 제목"
            )

            content = st.text_area(
                "공지 내용"
            )


            if st.button(
                "📢 공지 등록"
            ):

                if title and content:

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
                        title,
                        content,
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

                    st.rerun()

                else:

                    st.warning(
                        "제목과 내용을 입력해주세요."
                    )


        # =================================================
        # 게시판
        # =================================================

        elif menu == "💬 학습 게시판":

            st.header("💬 학습 게시판")

            st.write(
                "학생과 선생님이 학습 내용을 공유하는 공간입니다."
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
                            f"{post[2]} | {post[3]}"
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
    # 로그아웃
    # =====================================================

    st.divider()

    if st.button("🚪 로그아웃"):

        logout()
