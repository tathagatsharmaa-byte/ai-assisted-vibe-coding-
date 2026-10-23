"""Collect marks for five students and display their grades."""


def grade_for(mark: float) -> str:
    """Return the grade for a mark from 0 through 100."""
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
    """Read and validate one student's mark, retrying invalid entries."""
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


def main() -> None:
    students: list[tuple[str, float, str]] = []

    for number in range(1, 6):
        while True:
            name = input(f"Enter name of student {number}: ").strip()
            if name:
                break
            print("Name cannot be empty.")

        mark = read_mark(name)
        students.append((name, mark, grade_for(mark)))

    print("\nStudent Results")
    print("-" * 42)
    print(f"{'Name':<24}{'Marks':>10}{'Grade':>8}")
    print("-" * 42)
    for name, mark, grade in students:
        print(f"{name:<24}{mark:>10.2f}{grade:>8}")
    print("-" * 42)


if __name__ == "__main__":
    main()