"""Display entered marks and whether each is within the valid 0-100 range."""


def describe_mark(value: str) -> tuple[str, str]:
    """Return the entered value and its status without assigning a grade."""
    text = value.strip()

    try:
        mark = float(text)
    except ValueError:
        return text or "(blank)", "Invalid input (not a number)"

    # Explicitly compare against the inclusive valid range.
    if not 0 <= mark <= 100:
        return text, "Invalid input (outside 0-100)"
    if mark == 0:
        return text, "Lowest valid mark"
    if mark == 100:
        return text, "Highest valid mark"

    # Marks between the endpoints are valid; no grade is calculated.
    return text, "Valid mark (between 0 and 100)"


def main() -> None:
    """Read comma-separated marks and print one table row per entry."""
    entered_marks = input(
        "Enter marks separated by commas (for example, 0, 45, 100, 105): "
    )
    results = [describe_mark(value) for value in entered_marks.split(",")]

    name_width = max(len("Mark entered"), *(len(mark) for mark, _ in results))
    status_width = max(len("Result"), *(len(status) for _, status in results))

    print("\nMark Report")
    print(f"+-{'-' * name_width}-+-{'-' * status_width}-+")
    print(f"| {'Mark entered':<{name_width}} | {'Result':<{status_width}} |")
    print(f"+-{'-' * name_width}-+-{'-' * status_width}-+")
    for mark, status in results:
        print(f"| {mark:<{name_width}} | {status:<{status_width}} |")
    print(f"+-{'-' * name_width}-+-{'-' * status_width}-+")


if __name__ == "__main__":
    main()