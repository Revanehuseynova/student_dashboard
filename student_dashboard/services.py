"""
services.py
Business logic: grading, statistics and input validation.
No database or Streamlit code lives here, so everything is easy to unit-test.
"""
import config


def is_valid_score(student_score: float) -> bool:
    return config.MIN_SCORE <= student_score <= config.MAX_SCORE


def calculate_grade(student_score: float) -> str:
    if not is_valid_score(student_score):
        raise ValueError(
            f"Score must be between {config.MIN_SCORE} and {config.MAX_SCORE}, "
            f"got {student_score}."
        )
    if student_score >= config.EXCELLENT_SCORE:
        return config.GRADE_A
    if student_score >= config.GOOD_SCORE:
        return config.GRADE_B
    if student_score >= config.SATISFACTORY_SCORE:
        return config.GRADE_C
    if student_score >= config.PASSING_SCORE:
        return config.GRADE_D
    return config.GRADE_F


def calculate_statistics(students: list[dict]) -> dict:
    if not students:
        return {"total_students": 0, "average_score": 0.0,
                "highest_score": 0, "lowest_score": 0}
    scores = [student["score"] for student in students]
    return {
        "total_students": len(scores),
        "average_score": round(sum(scores) / len(scores), 1),
        "highest_score": max(scores),
        "lowest_score": min(scores),
    }


def add_grade_to_students(students: list[dict]) -> list[dict]:
    """Return copies of the students with an extra "grade" key."""
    return [{**student, "grade": calculate_grade(student["score"])} for student in students]


def validate_student_input(student_name: str, student_score: float) -> str | None:
    """Return an error message, or None when the input is valid."""
    cleaned_name = student_name.strip()
    if len(cleaned_name) < config.MIN_NAME_LENGTH:
        return f"Name must have at least {config.MIN_NAME_LENGTH} characters."
    if len(cleaned_name) > config.MAX_NAME_LENGTH:
        return f"Name must have at most {config.MAX_NAME_LENGTH} characters."
    if not is_valid_score(student_score):
        return f"Score must be between {config.MIN_SCORE} and {config.MAX_SCORE}."
    return None
