import streamlit as st
import sqlite3
from datetime import date


# =========================================================
# 1. 기본 설정
# =========================================================

st.set_page_config(
    page_title="학교 학습 관리 시스템",
    page_icon="🏫",
    layout="wide"
)


# =========================================================
# 2. 데이터베이스 연결
# =========================================================

conn = sqlite3.connect("school_system.db")
cursor = conn.cursor()


# 출결 테이블
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    attendance_date TEXT,
    student_id TEXT,
    student_number INTEGER,
    status TEXT,
    PRIMARY KEY (attendance_date, student_id)
)
""")

# 학습 자료 테이블
cursor.execute("""
CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    subject TEXT,
    description TEXT,
    file_name TEXT
)
""")

conn.commit()


# =========================================================
# 3. 임시 계정 정보
# =========================================================
#
# ⚠️ 현재는 1차 프로토타입용
# 실제 서비스에서는 비밀번호를 코드에 직접 저장하면 안 됨.
#

TEACHER_ID = "teacher"
TEACHER_PASSWORD = "teacher123"


# 학생 계정
# 나중에 실제 학생 계정 구조로 변경할 예정

STUDENTS = {

    "student01": {
        "password": "student123",
        "number": 1,
        "name": "1번 학생"
    },

    "student02": {
        "password": "student123",
        "number": 2,
        "name": "2번 학생"
    },

    "student03": {
        "password": "student123",
        "number": 3,
        "name": "3번 학생"
    },

    "student04": {
        "password": "student123",
        "number": 4,
        "name": "4번 학생"
    },

    "student05": {
        "password": "student123",
        "number": 5,
        "name": "5번 학생"
    },

    "student06": {
        "password": "student123",
        "number": 6,
        "name": "6번 학생"
    },

    "student07": {
        "password": "student123",
        "number": 7,
        "name": "7번 학생"
    },

    "student08": {
        "password": "student123",
        "number": 8,
        "name": "8번 학생"
    },

    "student09": {
        "password": "student123",
        "number": 9,
        "name": "9번 학생"
    },

    "student10": {
        "password": "student123",
        "number": 10,
        "name": "10번 학생"
    },

    "student11": {
        "password": "student123",
        "number": 11,
        "name": "11번 학생"
    },

    "student12": {
        "password": "student123",
        "number": 12,
        "name": "12번 학생"
    },

    "student13": {
        "password": "student123",
        "number": 13,
        "name": "13번 학생"
    },

    "student14": {
        "password": "student123",
        "number": 14,
        "name": "14번 학생"
    },

    "student15": {
        "password": "student123",
        "number": 15,
        "name": "15번 학생"
    },

    "student16": {
        "password": "student123",
        "number": 16,
        "name": "16번 학생"
    },

    "student17": {
        "password": "student123",
        "number": 17,
        "name": "17번 학생"
    },

    "student18": {
        "password": "student123",
        "number": 18,
        "name": "18번 학생"
    },

    "student19": {
        "password": "student123",
        "number": 19,
        "name": "19번 학생"
    },

    "student20": {
        "password": "student123",
        "number": 20,
        "name": "20번 학생"
    },

    "student21": {
        "password": "student123",
        "number": 21,
        "name": "21번 학생"
    },

    "student22": {
        "password": "student123",
        "number": 22,
        "name": "22번 학생"
    },

    "student23": {
        "password": "student123",
        "number": 23,
        "name": "23번 학생"
    },

    "student24": {
        "password": "student123",
        "number": 24,
        "name": "24번 학생"
    },

    "student25": {
        "password": "student123",
        "number": 25,
        "name": "25번 학생"
    },

    "student26": {
        "password": "student123",
        "number": 26,
        "name": "26번 학생"
    },

    "student27": {
        "password": "student123",
        "number": 27,
        "name": "27번 학생"
    },

    "student28": {
        "password": "student123",
        "number": 28,
        "name": "28번 학생"
    },

    "student29": {
        "password": "student123",
        "number": 29,
        "name": "29번 학생"
    },

    "student30": {
        "password": "student123",
        "number": 30,
        "name": "30번 학생"
    }
}


# =========================================================
# 4. 로그인 상태
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "student_id" not in st.session_state:
    st.session_state.student_id = None


# =========================================================
# 5. 로그인 함수
# =========================================================

def login(role, user_id, password):

    # ------------------------------
    # 선생님 로그인
    # ------------------------------

    if role == "teacher":

        if (
            user_id == TEACHER_ID
            and password == TEACHER_PASSWORD
        ):

            st.session_state.logged_in = True
            st.session_state.role = "teacher"
            st.session_state.student_id = None

            return True


    # ------------------------------
    # 학생 로그인
    # ------------------------------

    elif role == "student":

        if user_id in STUDENTS:

            if STUDENTS[user_id]["password"] == password:

                st.session_state.logged_in = True
                st.session_state.role = "student"
                st.session_state.student_id = user_id

                return True

    return False


# =========================================================
# 6. 로그아웃 함수
# =========================================================

def logout():

    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.student_id = None

    st.rerun()


# =========================================================
# 7. 로그인 화면
# =========================================================

if not st.session_state.logged_in:

    st.title("🏫 학교 학습 관리 시스템")

    st.write(
        "방과후 및 야간자율학습 학습 관리 시스템"
    )

    st.divider()

    st.header("로그인")

    role = st.radio(
        "접속할 화면을 선택하세요.",
        [
            "👨‍🎓 학생",
            "👨‍🏫 선생님"
        ],
        horizontal=True
    )

    st.divider()

    user_id = st.text_input(
        "아이디"
    )

    password = st.text_input(
        "비밀번호",
        type="password"
    )

    if st.button("🔐 로그인"):

        if role == "👨‍🎓 학생":

            success = login(
                "student",
                user_id,
                password
            )

        else:

            success = login(
                "teacher",
                user_id,
                password
            )

        if success:

            st.rerun()

        else:

            st.error(
                "아이디 또는 비밀번호가 올바르지 않습니다."
            )


# =========================================================
# 8. 로그인 이후
# =========================================================

else:

    # =====================================================
    # 학생 화면
    # =====================================================

    if st.session_state.role == "student":

        student_id = st.session_state.student_id

        student_info = STUDENTS[student_id]

        student_number = student_info["number"]

        student_name = student_info["name"]


        st.title("🏫 학교 학습 관리 시스템")

        st.success(
            f"👨‍🎓 {student_name}님 로그인"
        )

        # -----------------------------------------------
        # 학생 메뉴
        # -----------------------------------------------

        menu = st.radio(
            "메뉴",
            [
                "📋 내 출결",
                "📚 학습 자료실",
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
                f"현재 로그인한 학생: **{student_number}번**"
            )

            selected_date = st.date_input(
                "확인할 날짜",
                value=date.today()
            )

            date_text = str(selected_date)


            cursor.execute(
                """
                SELECT status
                FROM attendance
                WHERE attendance_date = ?
                AND student_id = ?
                """,
                (
                    date_text,
                    student_id
                )
            )

            result = cursor.fetchone()


            if result:

                status = result[0]

                if status == "🟢 출석":

                    st.success(
                        f"🟢 {selected_date} → 출석"
                    )

                elif status == "🟡 지각":

                    st.warning(
                        f"🟡 {selected_date} → 지각"
                    )

                elif status == "🔴 결석":

                    st.error(
                        f"🔴 {selected_date} → 결석"
                    )

            else:

                st.info(
                    "해당 날짜의 출결 기록이 없습니다."
                )


        # =================================================
        # 학생 학습 자료
        # =================================================

        elif menu == "📚 학습 자료실":

            st.header("📚 학습 자료실")

            st.info(
                "선생님이 등록한 학습 자료를 확인할 수 있습니다."
            )

            cursor.execute(
                """
                SELECT title, subject, description, file_name
                FROM materials
                ORDER BY id DESC
                """
            )

            materials = cursor.fetchall()


            if materials:

                for material in materials:

                    title = material[0]
                    subject = material[1]
                    description = material[2]
                    file_name = material[3]

                    with st.expander(
                        f"📄 {title} ({subject})"
                    ):

                        st.write(
                            description
                        )

                        if file_name:

                            st.caption(
                                f"첨부파일: {file_name}"
                            )

            else:

                st.info(
                    "등록된 학습 자료가 없습니다."
                )


        # =================================================
        # 학생 AI
        # =================================================

        elif menu == "🤖 AI 학습 도우미":

            st.header("🤖 AI 학습 도우미")

            st.info(
                "🚧 AI 학습 도우미는 추후 UPSTAGE API를 연결하여 제작합니다."
            )


    # =====================================================
    # 선생님 화면
    # =====================================================

    elif st.session_state.role == "teacher":

        st.title("🏫 학교 학습 관리 시스템")

        st.success(
            "👨‍🏫 선생님 계정으로 로그인했습니다."
        )


        menu = st.radio(
            "메뉴",
            [
                "📋 전체 출결 관리",
                "📚 학습 자료실",
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


            st.subheader(
                f"📅 {selected_date}"
            )


            # ---------------------------------------------
            # 현재 저장된 출결 불러오기
            # ---------------------------------------------

            cursor.execute(
                """
                SELECT student_id, status
                FROM attendance
                WHERE attendance_date = ?
                """,
                (date_text,)
            )

            saved_data = cursor.fetchall()


            saved_attendance = {

                student_id: status

                for student_id, status
                in saved_data

            }


            # ---------------------------------------------
            # 학생별 출결 입력
            # ---------------------------------------------

            attendance = {}


            for student_id, student_info in STUDENTS.items():

                student_number = student_info["number"]

                student_name = student_info["name"]

                options = [
                    "🟢 출석",
                    "🟡 지각",
                    "🔴 결석"
                ]


                default_status = saved_attendance.get(
                    student_id,
                    "🟢 출석"
                )


                default_index = options.index(
                    default_status
                )


                status = st.selectbox(

                    f"{student_number}번 학생",

                    options,

                    index=default_index,

                    key=f"attendance_{date_text}_{student_id}"

                )


                attendance[student_id] = status


            st.divider()


            # ---------------------------------------------
            # 통계
            # ---------------------------------------------

            present_count = list(
                attendance.values()
            ).count("🟢 출석")


            late_count = list(
                attendance.values()
            ).count("🟡 지각")


            absent_count = list(
                attendance.values()
            ).count("🔴 결석")


            st.subheader("📊 출결 통계")


            col1, col2, col3 = st.columns(3)


            col1.metric(
                "🟢 출석",
                f"{present_count}명"
            )


            col2.metric(
                "🟡 지각",
                f"{late_count}명"
            )


            col3.metric(
                "🔴 결석",
                f"{absent_count}명"
            )


            st.divider()


            # ---------------------------------------------
            # 저장
            # ---------------------------------------------

            if st.button(
                "💾 전체 출결 저장"
            ):

                for student_id, status in attendance.items():

                    student_number = STUDENTS[
                        student_id
                    ]["number"]


                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO attendance
                        (
                            attendance_date,
                            student_id,
                            student_number,
                            status
                        )
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            date_text,
                            student_id,
                            student_number,
                            status
                        )
                    )


                conn.commit()


                st.success(
                    f"✅ {selected_date} 전체 학생 출결이 저장되었습니다."
                )


        # =================================================
        # 선생님 학습 자료
        # =================================================

        elif menu == "📚 학습 자료실":

            st.header("📚 학습 자료실")

            st.write(
                "선생님은 학습 자료를 등록하고 관리할 수 있습니다."
            )


            title = st.text_input(
                "자료 제목"
            )


            subject = st.selectbox(
                "과목",
                [
                    "수학",
                    "물리학",
                    "화학",
                    "생명과학",
                    "영어",
                    "국어",
                    "기타"
                ]
            )


            description = st.text_area(
                "자료 설명"
            )


            uploaded_file = st.file_uploader(
                "학습 자료 업로드",
                type=[
                    "pdf",
                    "txt",
                    "png",
                    "jpg",
                    "jpeg"
                ]
            )


            if st.button(
                "📤 학습 자료 등록"
            ):

                if title and uploaded_file:

                    cursor.execute(
                        """
                        INSERT INTO materials
                        (
                            title,
                            subject,
                            description,
                            file_name
                        )
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            title,
                            subject,
                            description,
                            uploaded_file.name
                        )
                    )


                    conn.commit()


                    st.success(
                        "학습 자료가 등록되었습니다."
                    )

                else:

                    st.warning(
                        "자료 제목과 파일을 입력해주세요."
                    )


            st.divider()

            st.subheader(
                "📚 등록된 자료"
            )


            cursor.execute(
                """
                SELECT title, subject, description, file_name
                FROM materials
                ORDER BY id DESC
                """
            )


            materials = cursor.fetchall()


            if materials:

                for material in materials:

                    with st.expander(
                        f"📄 {material[0]} ({material[1]})"
                    ):

                        st.write(
                            material[2]
                        )

                        st.caption(
                            f"첨부파일: {material[3]}"
                        )

            else:

                st.info(
                    "아직 등록된 학습 자료가 없습니다."
                )


        # =================================================
        # 선생님 AI
        # =================================================

        elif menu == "🤖 AI 학습 도우미":

            st.header("🤖 AI 학습 도우미")

            st.info(
                "🚧 AI 학습 도우미는 추후 UPSTAGE API를 연결하여 제작합니다."
            )


    # =====================================================
    # 로그아웃
    # =====================================================

    st.divider()

    if st.button("🚪 로그아웃"):

        logout()
