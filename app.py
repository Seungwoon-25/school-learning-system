import streamlit as st
from datetime import date

# -------------------------
# 기본 설정
# -------------------------

st.set_page_config(
    page_title="학교 학습 관리 시스템",
    page_icon="🏫",
    layout="wide"
)

# -------------------------
# 제목
# -------------------------

st.title("🏫 학교 학습 관리 시스템")
st.write("방과후 및 야간자율학습 학습 관리")

st.divider()

# -------------------------
# 메뉴
# -------------------------

menu = st.radio(
    "메뉴를 선택하세요.",
    ["📋 출결 관리", "📚 학습 자료", "🤖 AI 학습 도우미"],
    horizontal=True
)

st.divider()

# -------------------------
# 출결 관리
# -------------------------

if menu == "📋 출결 관리":

    st.header("📋 출결 관리")

    selected_date = st.date_input(
        "📅 출결 날짜",
        value=date.today()
    )

    st.write(f"**{selected_date} 출결 현황**")

    attendance = {}

    for student_number in range(1, 31):

        status = st.selectbox(
            f"{student_number}번 학생",
            ["🟢 출석", "🟡 지각", "🔴 결석"],
            key=f"student_{student_number}"
        )

        attendance[student_number] = status

    st.divider()

    # 출결 통계
    present_count = list(attendance.values()).count("🟢 출석")
    late_count = list(attendance.values()).count("🟡 지각")
    absent_count = list(attendance.values()).count("🔴 결석")

    col1, col2, col3 = st.columns(3)

    col1.metric("🟢 출석", f"{present_count}명")
    col2.metric("🟡 지각", f"{late_count}명")
    col3.metric("🔴 결석", f"{absent_count}명")

    st.divider()

    if st.button("💾 출결 기록 확인"):

        st.success("현재 출결 정보가 정상적으로 입력되었습니다.")

        st.write("### 📊 출결 기록")

        for student_number, status in attendance.items():
            st.write(f"{student_number}번 → {status}")


# -------------------------
# 학습 자료
# -------------------------

elif menu == "📚 학습 자료":

    st.header("📚 학습 자료")

    st.info("학습 자료 관리 기능은 다음 단계에서 개발합니다.")

    subject = st.selectbox(
        "과목을 선택하세요.",
        ["수학", "물리학", "화학", "생명과학", "기타"]
    )

    st.write(f"현재 선택한 과목: **{subject}**")

    uploaded_file = st.file_uploader(
        "학습 자료를 업로드하세요.",
        type=["pdf", "txt", "png", "jpg"]
    )

    if uploaded_file is not None:
        st.success(f"'{uploaded_file.name}' 파일이 업로드되었습니다.")


# -------------------------
# AI 학습 도우미
# -------------------------

elif menu == "🤖 AI 학습 도우미":

    st.header("🤖 AI 학습 도우미")

    st.info("UPSTAGE API 연결은 다음 단계에서 진행합니다.")

    question = st.text_area(
        "학습에 관해 궁금한 내용을 입력하세요."
    )

    if st.button("💬 질문하기"):

        if question:
            st.write("질문:", question)
            st.warning("현재는 AI API가 연결되지 않았습니다.")
        else:
            st.warning("질문을 먼저 입력해주세요.")
