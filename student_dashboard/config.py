"""
config.py
Central place for every constant used by the Student Performance Dashboard.
Keeping them here removes magic numbers from the rest of the code.
"""
import os
from typing import Final

# --- Database ---------------------------------------------------------------
DB_SERVER: Final[str] = os.getenv("DB_SERVER", r".\SQLEXPRESS")
DB_NAME: Final[str] = os.getenv("DB_NAME", "UniversityDB")
PREFERRED_ODBC_DRIVERS: Final[tuple[str, ...]] = (
    "ODBC Driver 18 for SQL Server",
    "ODBC Driver 17 for SQL Server",
    "SQL Server",
)

# --- Scores and grades ------------------------------------------------------
MIN_SCORE: Final[int] = 0
MAX_SCORE: Final[int] = 100
DEFAULT_FORM_SCORE: Final[int] = 70

EXCELLENT_SCORE: Final[int] = 90   # A
GOOD_SCORE: Final[int] = 80        # B
SATISFACTORY_SCORE: Final[int] = 70  # C
PASSING_SCORE: Final[int] = 60     # D

GRADE_A: Final[str] = "A"
GRADE_B: Final[str] = "B"
GRADE_C: Final[str] = "C"
GRADE_D: Final[str] = "D"
GRADE_F: Final[str] = "F"

# --- Validation -------------------------------------------------------------
MIN_NAME_LENGTH: Final[int] = 2
MAX_NAME_LENGTH: Final[int] = 100

# --- UI ---------------------------------------------------------------------
APP_TITLE: Final[str] = "Student Performance Dashboard"
APP_ICON: Final[str] = "🎓"
