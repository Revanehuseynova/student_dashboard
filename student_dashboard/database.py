"""
database.py
Database layer. The only module that talks to SQL Server (UniversityDB).
Returns plain dictionaries: {"id": int, "name": str, "score": int}.
"""
from contextlib import closing

import pyodbc

import config


def _find_odbc_driver() -> str:
    installed_drivers = pyodbc.drivers()
    for driver in config.PREFERRED_ODBC_DRIVERS:
        if driver in installed_drivers:
            return driver
    raise RuntimeError("No SQL Server ODBC driver found. Install ODBC Driver 17 or 18.")


def _build_connection_string() -> str:
    return (
        f"DRIVER={{{_find_odbc_driver()}}};"
        f"SERVER={config.DB_SERVER};"
        f"DATABASE={config.DB_NAME};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )


def create_connection() -> pyodbc.Connection:
    return pyodbc.connect(_build_connection_string(), autocommit=True)


def _row_to_student(row) -> dict:
    return {"id": row.Id, "name": row.Name, "score": int(row.Score)}


def _fetch_results(procedure_call: str, *parameters) -> list[dict]:
    with closing(create_connection()) as connection:
        rows = connection.execute(procedure_call, *parameters).fetchall()
    return [_row_to_student(row) for row in rows]


def get_students() -> list[dict]:
    """Return every student (stored procedure without a filter)."""
    return _fetch_results("EXEC dbo.GetStudentResult")


def get_student(student_name: str) -> list[dict]:
    """Return students whose name contains `student_name` (may be several)."""
    return _fetch_results("EXEC dbo.GetStudentResult @StudentName = ?", student_name.strip())


def add_student(student_name: str, student_score: int) -> None:
    with closing(create_connection()) as connection:
        connection.execute("EXEC dbo.AddStudent @Name = ?, @Score = ?",
                           student_name.strip(), student_score)
