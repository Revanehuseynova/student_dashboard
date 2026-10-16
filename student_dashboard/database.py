
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "students.db"


def create_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with create_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Score INTEGER NOT NULL CHECK (Score BETWEEN 0 AND 100)
            )
        """)

        count = connection.execute(
            "SELECT COUNT(*) FROM Students"
        ).fetchone()[0]

        if count == 0:
            connection.executemany(
                "INSERT INTO Students (Name, Score) VALUES (?, ?)",
                [
                    ("Ali", 85),
                    ("Leyla", 72),
                    ("Murad", 48),
                    ("Aysel", 91),
                    ("Kamran", 63),
                ],
            )


def get_students():
    initialize_database()
    with create_connection() as connection:
        rows = connection.execute(
            "SELECT Id, Name, Score FROM Students ORDER BY Id"
        ).fetchall()

    return [
        {"id": row["Id"], "name": row["Name"], "score": row["Score"]}
        for row in rows
    ]


def get_student(student_name: str):
    initialize_database()
    with create_connection() as connection:
        rows = connection.execute(
            "SELECT Id, Name, Score FROM Students WHERE Name LIKE ? ORDER BY Id",
            (f"%{student_name.strip()}%",),
        ).fetchall()

    return [
        {"id": row["Id"], "name": row["Name"], "score": row["Score"]}
        for row in rows
    ]


def add_student(student_name: str, student_score: int):
    initialize_database()
    with create_connection() as connection:
        connection.execute(
            "INSERT INTO Students (Name, Score) VALUES (?, ?)",
            (student_name.strip(), student_score),
        )
