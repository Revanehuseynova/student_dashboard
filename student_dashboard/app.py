"""
app.py
Streamlit UI layer. Talks only to services.py and database.py.
"""
import pandas as pd
import streamlit as st

import config
import database
import services

FLASH_KEY = "flash_message"


def show_flash_message() -> None:
    """Show a success message that survives st.rerun()."""
    message = st.session_state.pop(FLASH_KEY, None)
    if message:
        st.success(message)


def handle_add_student(student_name: str, student_score: int) -> None:
    error_message = services.validate_student_input(student_name, student_score)
    if error_message:
        st.error(error_message)
        return
    try:
        database.add_student(student_name, student_score)
    except Exception as error:
        st.error(f"Could not save the student: {error}")
        return
    grade = services.calculate_grade(student_score)
    st.session_state[FLASH_KEY] = f"{student_name.strip()} added (grade {grade})."
    st.rerun()


def render_add_student_form() -> None:
    st.subheader("Add Student")
    with st.form("add_student_form", clear_on_submit=True):
        student_name = st.text_input("Student Name")
        student_score = st.number_input(
            "Score", min_value=config.MIN_SCORE, max_value=config.MAX_SCORE,
            value=config.DEFAULT_FORM_SCORE, step=1,
        )
        if st.form_submit_button("Add Student"):
            handle_add_student(student_name, int(student_score))


def render_statistics(students: list[dict]) -> None:
    stats = services.calculate_statistics(students)
    labels_and_values = [
        ("Total Students", stats["total_students"]),
        ("Average Score", f"{stats['average_score']:.1f}"),
        ("Highest Score", stats["highest_score"]),
        ("Lowest Score", stats["lowest_score"]),
    ]
    for column, (label, value) in zip(st.columns(len(labels_and_values)), labels_and_values):
        column.metric(label, value)


def render_student_table(all_students: list[dict]) -> None:
    st.subheader("Students")
    search_text = st.text_input("Search Student")
    students = database.get_student(search_text) if search_text.strip() else all_students

    if not students:
        st.info("No students found.")
        return
    table = pd.DataFrame(services.add_grade_to_students(students))
    st.dataframe(
        table[["name", "score", "grade"]].rename(columns=str.title),
        hide_index=True,
    )


def render_score_chart(students: list[dict]) -> None:
    if not students:
        return
    st.subheader("Scores")
    chart_data = pd.DataFrame(students).set_index("name")[["score"]]
    st.bar_chart(chart_data)


def main() -> None:
    st.set_page_config(page_title=config.APP_TITLE, page_icon=config.APP_ICON, layout="wide")
    st.title(f"{config.APP_ICON} {config.APP_TITLE}")
    show_flash_message()

    try:
        students = database.get_students()
    except Exception as error:
        st.error(f"Cannot connect to SQL Server ({config.DB_SERVER} / {config.DB_NAME}): {error}")
        return

    render_statistics(students)
    st.divider()
    form_column, table_column = st.columns([1, 2], gap="large")
    with form_column:
        render_add_student_form()
    with table_column:
        render_student_table(students)
    render_score_chart(students)


main()
