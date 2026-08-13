# =========================================================
# 5. 비밀번호 처리
# =========================================================

import hashlib


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def check_password(input_password, saved_password):
    """
    기존 평문 비밀번호와
    SHA-256 암호화 비밀번호를 모두 허용
    """

    # 새 방식
    if saved_password == hash_password(input_password):
        return True

    # 기존 방식
    if saved_password == input_password:
        return True

    return False


# =========================================================
# 6. 초기 계정 생성
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
# 8. 로그인 함수
# =========================================================

def login(user_id, password):

    # 빈칸 검사
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


    # 아이디가 존재하지 않음
    if user is None:
        return False


    db_user_id = user[0]
    db_password = user[1]
    db_role = user[2]
    db_student_number = user[3]
    db_name = user[4]


    # 비밀번호 확인
    if not check_password(
        password,
        db_password
    ):
        return False


    # 로그인 정보 저장
    st.session_state.logged_in = True

    st.session_state.user_id = db_user_id

    st.session_state.role = db_role

    st.session_state.student_number = (
        db_student_number
    )

    st.session_state.user_name = db_name


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
        "🔐 로그인",
        use_container_width=True
    ):

        if login(
            user_id,
            password
        ):

            st.success(
                f"{st.session_state.user_name}님, "
                "환영합니다!"
            )

            st.rerun()

        else:

            st.error(
                "아이디 또는 비밀번호가 올바르지 않습니다."
            )


    st.divider()

    with st.expander("🧪 테스트 계정"):

        st.write(
            "**학생**  \n"
            "아이디: `student01`  \n"
            "비밀번호: `student123`"
        )

        st.write("---")

        st.write(
            "**선생님**  \n"
            "아이디: `teacher`  \n"
            "비밀번호: `teacher123`"
        )
