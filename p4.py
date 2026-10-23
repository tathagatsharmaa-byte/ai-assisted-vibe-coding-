"""Calculate an arithmetic mean from validated marks."""


def calculate_average(marks: list[int | float]) -> float:
    """Return the mean of marks, without modifying the supplied list.

    Raises:
        TypeError: If marks is not a list or contains a non-numeric mark.
        ValueError: If marks is empty or contains a mark outside 0-100.
    """
    if not isinstance(marks, list):
        raise TypeError("marks must be provided as a list")
    if not marks:
        raise ValueError("marks cannot be empty")

    for mark in marks:
        # bool is an int subclass, but True/False are not valid marks.
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise TypeError("each mark must be an integer or a float")
        if not 0 <= mark <= 100:
            raise ValueError("each mark must be between 0 and 100")

    return sum(marks) / len(marks)


if __name__ == "__main__":
    import unittest

    class CalculateAverageTests(unittest.TestCase):
        def test_normal_marks(self) -> None:
            self.assertEqual(calculate_average([70, 80, 90]), 80)

        def test_boundary_marks(self) -> None:
            self.assertEqual(calculate_average([0, 100]), 50)
            self.assertEqual(calculate_average([0]), 0)
            self.assertEqual(calculate_average([100]), 100)

        def test_original_list_is_unchanged(self) -> None:
            marks = [25, 75]
            original = marks.copy()
            calculate_average(marks)
            self.assertEqual(marks, original)

        def test_empty_list_is_rejected(self) -> None:
            with self.assertRaises(ValueError):
                calculate_average([])

        def test_out_of_range_marks_are_rejected(self) -> None:
            for mark in (-1, 101):
                with self.subTest(mark=mark):
                    with self.assertRaises(ValueError):
                        calculate_average([mark])

        def test_non_numeric_mark_is_rejected(self) -> None:
            with self.assertRaises(TypeError):
                calculate_average([80, "90"])  # type: ignore[list-item]

        def test_non_list_is_rejected(self) -> None:
            with self.assertRaises(TypeError):
                calculate_average((80, 90))  # type: ignore[arg-type]

    unittest.main()