import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import (add_grade_to_students, calculate_grade,
                      calculate_statistics, validate_student_input)

SAMPLE = [{"name": n, "score": s} for n, s in
          [("Ali", 85), ("Leyla", 72), ("Murad", 48), ("Aysel", 91), ("Kamran", 63)]]


class GradeTests(unittest.TestCase):
    def test_assignment_examples(self):
        for score, grade in {91: "A", 85: "B", 72: "C", 63: "D", 48: "F"}.items():
            self.assertEqual(calculate_grade(score), grade)

    def test_boundaries(self):
        for score, grade in {100: "A", 90: "A", 89: "B", 80: "B", 79: "C",
                             70: "C", 69: "D", 60: "D", 59: "F", 0: "F"}.items():
            self.assertEqual(calculate_grade(score), grade)

    def test_out_of_range(self):
        for bad_score in (-1, 101):
            with self.assertRaises(ValueError):
                calculate_grade(bad_score)


class StatisticsTests(unittest.TestCase):
    def test_assignment_data(self):
        self.assertEqual(calculate_statistics(SAMPLE), {
            "total_students": 5, "average_score": 71.8,
            "highest_score": 91, "lowest_score": 48})

    def test_empty(self):
        self.assertEqual(calculate_statistics([])["total_students"], 0)


class OtherTests(unittest.TestCase):
    def test_add_grade_does_not_mutate(self):
        graded = add_grade_to_students(SAMPLE)
        self.assertEqual([s["grade"] for s in graded], ["B", "C", "F", "A", "D"])
        self.assertNotIn("grade", SAMPLE[0])

    def test_validation(self):
        self.assertIsNone(validate_student_input("Ali", 85))
        self.assertIsNotNone(validate_student_input("", 85))
        self.assertIsNotNone(validate_student_input("A", 85))
        self.assertIsNotNone(validate_student_input("Ali", 150))


if __name__ == "__main__":
    unittest.main()
