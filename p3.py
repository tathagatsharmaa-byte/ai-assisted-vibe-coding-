"""Collect marks for five students, assign grades, and print a report."""


def grade_for(mark: float) -> str:
    """Return the grade for a mark from 0 through 100."""
    # Grade boundaries: A = 90-100, B = 80-<90, C = 70-<80,
    # D = 60-<70, and F = 0-<60.
    if mark >= 90:
        return "A"
    if mark >= 80:
        return "B"
    if mark >= 70:
        return "C"
    if mark >= 60:
        return "D"
    return "F"


def read_mark(name: str) -> float:
    """Prompt until a numeric mark between 0 and 100 is entered."""
    while True:
        value = input(f"Enter marks for {name} (0-100): ")

        try:
            mark = float(value)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if not 0 <= mark <= 100:
            print("Marks must be between 0 and 100.")
            continue

        return mark


def test_grade_boundaries() -> None:
    """Check grades at the boundary values; raises AssertionError on failure."""
    test_cases = (
        (0, "F"),
        (59.99, "F"),
        (60, "D"),
        (69.99, "D"),
        (70, "C"),
        (79.99, "C"),
        (80, "B"),
        (89.99, "B"),
        (90, "A"),
        (100, "A"),
    )

    for mark, expected_grade in test_cases:
        assert grade_for(mark) == expected_grade, (
            f"Expected {mark} to receive grade {expected_grade}"
        )


def main() -> None:
    """Collect five student records and display their grades."""
    students: list[tuple[str, float, str]] = []

    for number in range(1, 6):
        while True:
            name = input(f"Enter name of student {number}: ").strip()
            if name:
                break
            print("Name cannot be empty.")

        mark = read_mark(name)
        students.append((name, mark, grade_for(mark)))

    print("\nStudent Marks Report")
    print("-" * 46)
    print(f"{'Student':<24}{'Marks':>12}{'Grade':>10}")
    print("-" * 46)
    for name, mark, grade in students:
        print(f"{name:<24}{mark:>12.2f}{grade:>10}")
    print("-" * 46)


if __name__ == "__main__":
    main()