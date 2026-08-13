import streamlit as st
from datetime import date

# ========================================
# 기본 설정
# ========================================

st.set_page_config(
    page_title="학교 학습 관리 시스템",
    page_icon="🏫",
    layout="wide"
)


# ========================================
# 로그인 상태 관리
# ========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_type" not in st.session_state:
    st.session_state.user_type = None


# ========================================
# 로그인하지 않은 경우
# ========================================

if not st.session_state.logged_in:

    st.title("🏫 학교 학습 관리 시스템")
    st.write("방과후 및 야간자율학습 학습 관리")

    st.divider()

    st.header("🔐 로그인")

    user_type = st.radio(
        "사용자 유형을 선택하세요.",
        ["👨‍🏫 교사/관리자", "👨‍🎓 학생"]
    )

    password = st.text_input(
        "비밀번호",
        type="password"
    )

    if st.button("로그인"):

        # 임시 테스트용 비밀번호
        if user_type == "👨‍🏫 교사/관리자" and password == "teacher123":

            st.session_state.logged_in = True
            st.session_state.user_type = "teacher"

            st.rerun()

        elif user_type == "👨‍🎓 학생" and password == "student123":

            st.session_state.logged_in = True
            st.session_state.user_type = "student"

            st.rerun()

        else:

            st.error("비밀번호가 올바르지 않습니다.")


# ========================================
# 로그인 이후
# ========================================

else:

    st.title("🏫 학교 학습 관리 시스템")

    # ====================================
    # 교사 / 관리자
    # ====================================

    if st.session_state.user_type == "teacher":

        st.success("👨‍🏫 교사/관리자로 로그인했습니다.")

        menu = st.radio(
            "메뉴를 선택하세요.",
            [
                "📋 출결 관리",
                "📚 학습 자료",
                "🤖 AI 학습 도우미"
            ],
            horizontal=True
        )

        st.divider()

        # --------------------------------
        # 출결 관리
        # --------------------------------

        if menu == "📋 출결 관리":

            st.header("📋 출결 관리")

            st.write(
                "교사/관리자만 학생의 출결 상태를 수정할 수 있습니다."
            )

            # 날짜 선택
            selected_date = st.date_input(
                "📅 출결 날짜",
                value=date.today()
            )

            st.subheader(
                f"📅 {selected_date} 출결 현황"
            )

            # 출결 정보를 저장할 딕셔너리
            attendance = {}

            # 학생 1~30번
            for student_number in range(1, 31):

                status = st.selectbox(
                    f"{student_number}번 학생",
                    [
                        "🟢 출석",
                        "🟡 지각",
                        "🔴 결석"
                    ],
                    key=f"{selected_date}_student_{student_number}"
                )

                attendance[student_number] = status

            st.divider()

            # --------------------------------
            # 출결 통계
            # --------------------------------

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

            # --------------------------------
            # 출결 기록 확인
            # --------------------------------

            if st.button("💾 출결 기록 확인"):

                st.success(
                    f"{selected_date} 출결 정보가 입력되었습니다."
                )

                st.subheader("📋 입력된 출결 기록")

                for student_number, status in attendance.items():

                    st.write(
                        f"{student_number}번 → {status}"
                    )


        # --------------------------------
        # 학습 자료
        # --------------------------------

        elif menu == "📚 학습 자료":

            st.header("📚 학습 자료")

            st.info(
                "학습 자료 관리 기능은 다음 단계에서 개발합니다."
            )


        # --------------------------------
        # AI 학습 도우미
        # --------------------------------

        elif menu == "🤖 AI 학습 도우미":

            st.header("🤖 AI 학습 도우미")

            st.info(
                "UPSTAGE API 연결은 다음 단계에서 개발합니다."
            )


    # ====================================
    # 학생
    # ====================================

    elif st.session_state.user_type == "student":

        st.success("👨‍🎓 학생으로 로그인했습니다.")

        menu = st.radio(
            "메뉴를 선택하세요.",
            [
                "📚 학습 자료",
                "🤖 AI 학습 도우미"
            ],
            horizontal=True
        )

        st.divider()

        # --------------------------------
        # 학습 자료
        # --------------------------------

        if menu == "📚 학습 자료":

            st.header("📚 학습 자료")

            st.info(
                "학습 자료 기능은 다음 단계에서 개발합니다."
            )


        # --------------------------------
        # AI
        # --------------------------------

        elif menu == "🤖 AI 학습 도우미":

            st.header("🤖 AI 학습 도우미")

            st.info(
                "UPSTAGE API 연결은 다음 단계에서 개발합니다."
            )


    # ====================================
    # 로그아웃
    # ====================================

    st.divider()

    if st.button("🚪 로그아웃"):

        st.session_state.logged_in = False
        st.session_state.user_type = None

        st.rerun()
