import streamlit as st
import datetime

st.set_page_config(page_title="시험 5주 대비 플래너", layout="wide")

# --- 세션 상태 초기화 ---
if "exam_date" not in st.session_state:
    st.session_state.exam_date = datetime.date.today()

if "planner" not in st.session_state:
    st.session_state.planner = {}

# --- 시험 날짜 입력 ---
st.title("📘 시험 대비 5주 플래너")

st.session_state.exam_date = st.date_input(
    "시험 날짜를 선택하세요", 
    st.session_state.exam_date
)

today = datetime.date.today()
d_day = (st.session_state.exam_date - today).days
st.markdown(f"## 🗓️ D-{d_day if d_day >= 0 else 'Day'}")

# --- 5주 플래너 ---
weeks = 5

for week in range(1, weeks + 1):
    with st.expander(f"📌 {week}주차 계획", expanded=True):
        # 과목별 큰 계획
        subjects = st.text_area(
            f"{week}주차 과목별 해야할 일 (줄바꿈으로 구분)", 
            value="\n".join(st.session_state.planner.get(week, {}).get("subjects", [])),
            key=f"week{week}_subjects"
        )

        if week not in st.session_state.planner:
            st.session_state.planner[week] = {"subjects": [], "days": {}}

        st.session_state.planner[week]["subjects"] = subjects.split("\n") if subjects else []

        # --- 일별 세부 계획 ---
        for day in range(1, 8):
            st.markdown(f"**{week}주차 {day}일차 (Day {(week-1)*7+day})**")

            todos_key = f"week{week}_day{day}_todos"
            todos_val = st.session_state.planner[week]["days"].get(day, {}).get("todos", "")

            todos = st.text_area(
                f"할 일 (쉼표로 구분)", 
                value=todos_val,
                key=todos_key
            )

            if day not in st.session_state.planner[week]["days"]:
                st.session_state.planner[week]["days"][day] = {"todos": "", "done": []}

            st.session_state.planner[week]["days"][day]["todos"] = todos

            if todos:
                todo_list = [t.strip() for t in todos.split(",") if t.strip()]
                done_list = st.session_state.planner[week]["days"][day].get("done", [False]*len(todo_list))

                new_done_list = []
                for i, task in enumerate(todo_list):
                    done = st.checkbox(
                        task, 
                        value=done_list[i] if i < len(done_list) else False, 
                        key=f"week{week}_day{day}_task{i}"
                    )
                    if done:
                        st.markdown(f"- ~~{task}~~")
                    else:
                        st.markdown(f"- {task}")
                    new_done_list.append(done)

                st.session_state.planner[week]["days"][day]["done"] = new_done_list
