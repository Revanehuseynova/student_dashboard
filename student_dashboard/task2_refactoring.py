"""
task2_refactoring.py
Task 2: refactoring badly written code according to Clean Code rules.
Run:  python task2_refactoring.py     (prints both versions' results)
"""
from typing import Final

# =============================================================================
# BEFORE: breaks naming, SRP, DRY, KISS and magic-number rules
# =============================================================================
def calc(d):
    t = 0
    mx = 0
    mn = 999
    r = []
    for i in d:
        if i[1] < 0 or i[1] > 100:
            print("error")
            continue
        t = t + i[1]
        if i[1] > mx:
            mx = i[1]
        if i[1] < mn:
            mn = i[1]
        if i[1] >= 90:
            g = "A"
        elif i[1] >= 80:
            g = "B"
        elif i[1] >= 70:
            g = "C"
        elif i[1] >= 60:
            g = "D"
        else:
            g = "F"
        r.append((i[0], i[1], g))
        print(i[0] + " " + str(i[1]) + " " + g)
    print("avg " + str(t / len(r)))
    print("max " + str(mx))
    print("min " + str(mn))
    return r


# =============================================================================
# AFTER: small functions, meaningful names, constants, no repetition
# =============================================================================
MIN_SCORE: Final[int] = 0
MAX_SCORE: Final[int] = 100
GRADE_THRESHOLDS: Final[tuple[tuple[int, str], ...]] = (
    (90, "A"), (80, "B"), (70, "C"), (60, "D"),
)
LOWEST_GRADE: Final[str] = "F"


def is_valid_score(student_score: int) -> bool:
    return MIN_SCORE <= student_score <= MAX_SCORE


def calculate_grade(student_score: int) -> str:
    for minimum_score, grade in GRADE_THRESHOLDS:
        if student_score >= minimum_score:
            return grade
    return LOWEST_GRADE


def keep_valid_records(records: list[tuple[str, int]]) -> list[tuple[str, int]]:
    return [(name, score) for name, score in records if is_valid_score(score)]


def calculate_statistics(scores: list[int]) -> dict:
    if not scores:
        return {"average": 0.0, "highest": 0, "lowest": 0}
    return {
        "average": round(sum(scores) / len(scores), 1),
        "highest": max(scores),
        "lowest": min(scores),
    }


def build_report(records: list[tuple[str, int]]) -> list[dict]:
    return [
        {"name": name, "score": score, "grade": calculate_grade(score)}
        for name, score in keep_valid_records(records)
    ]


def print_report(report: list[dict], statistics: dict) -> None:
    for row in report:
        print(f"{row['name']:<8} {row['score']:<5} {row['grade']}")
    print(f"Average: {statistics['average']}  "
          f"Highest: {statistics['highest']}  Lowest: {statistics['lowest']}")


if __name__ == "__main__":
    students = [("Ali", 85), ("Leyla", 72), ("Murad", 48), ("Aysel", 91), ("Kamran", 63)]

    print("--- BEFORE ---")
    calc(students)

    print("\n--- AFTER ---")
    report = build_report(students)
    print_report(report, calculate_statistics([row["score"] for row in report]))
