"""In-memory student task manager.

Assumptions for this prototype:
- One student manages a shared task list; there is no authentication or
  multi-student separation.
- Tasks have a title, optional description, optional due date, priority, and
  status.
- Data is held in memory and is lost when the program exits.
"""

from collections.abc import Mapping
from dataclasses import dataclass, replace
from datetime import date, datetime
from enum import Enum
import unittest


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class Task:
    task_id: int
    title: str
    description: str
    priority: TaskPriority
    due_date: date | None
    status: TaskStatus

    def to_dict(self) -> dict[str, int | str | None]:
        """Return the task in the JSON field shape defined by the API contract."""
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "due_date": self.due_date.isoformat() if self.due_date else None,
        }


class TaskNotFoundError(LookupError):
    """Raised when an operation refers to an unknown task ID."""


class TaskManager:
    """Create, read, update, and delete tasks held in memory."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def create_task(
        self,
        title: str,
        description: str = "",
        due_date: date | None = None,
        priority: TaskPriority = TaskPriority.MEDIUM,
    ) -> Task:
        """Create a task and return its assigned task record."""
        task = Task(
            task_id=self._next_id,
            title=self._validate_title(title),
            description=self._validate_description(description),
            priority=self._validate_priority(priority),
            due_date=self._validate_due_date(due_date),
            status=TaskStatus.TODO,
        )
        self._tasks[task.task_id] = task
        self._next_id += 1
        return task

    def list_tasks(self) -> tuple[Task, ...]:
        """Return all tasks in ascending task-ID order."""
        return tuple(self._tasks[task_id] for task_id in sorted(self._tasks))

    def get_task(self, task_id: int) -> Task:
        """Return one task, or raise TaskNotFoundError if it does not exist."""
        self._validate_task_id(task_id)
        try:
            return self._tasks[task_id]
        except KeyError as error:
            raise TaskNotFoundError(f"Task {task_id} was not found.") from error

    def update_task(self, task_id: int, updates: Mapping[str, object]) -> Task:
        """Update supplied fields; use None to clear an optional due date."""
        task = self.get_task(task_id)
        if not updates:
            raise ValueError("Provide at least one field to update.")

        allowed_fields = {"title", "description", "priority", "due_date", "status"}
        unknown_fields = set(updates) - allowed_fields
        if unknown_fields:
            names = ", ".join(sorted(unknown_fields))
            raise ValueError(f"Unknown task field(s): {names}.")

        validated_updates: dict[str, object] = {}
        if "title" in updates:
            validated_updates["title"] = self._validate_title(updates["title"])
        if "description" in updates:
            validated_updates["description"] = self._validate_description(
                updates["description"]
            )
        if "priority" in updates:
            validated_updates["priority"] = self._validate_priority(
                updates["priority"]
            )
        if "due_date" in updates:
            validated_updates["due_date"] = self._validate_due_date(
                updates["due_date"]
            )
        if "status" in updates:
            status = updates["status"]
            if not isinstance(status, TaskStatus):
                raise ValueError("Status must be a valid TaskStatus value.")
            validated_updates["status"] = status

        updated_task = replace(task, **validated_updates)
        self._tasks[task_id] = updated_task
        return updated_task

    def delete_task(self, task_id: int) -> Task:
        """Delete and return a task, or raise TaskNotFoundError."""
        task = self.get_task(task_id)
        del self._tasks[task_id]
        return task

    @staticmethod
    def _validate_task_id(task_id: int) -> None:
        if isinstance(task_id, bool) or not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")

    @staticmethod
    def _validate_title(title: object) -> str:
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title must contain at least one non-space character.")
        return title.strip()

    @staticmethod
    def _validate_description(description: object) -> str:
        if not isinstance(description, str):
            raise ValueError("Description must be text.")
        return description

    @staticmethod
    def _validate_priority(priority: object) -> TaskPriority:
        if not isinstance(priority, TaskPriority):
            raise ValueError("Priority must be a valid TaskPriority value.")
        return priority

    @staticmethod
    def _validate_due_date(due_date: object) -> date | None:
        if due_date is None:
            return None
        if not isinstance(due_date, date) or isinstance(due_date, datetime):
            raise ValueError("Due date must be a date or None.")
        return due_date


def _read_task_id() -> int:
    """Read a positive integer ID from the console."""
    value = input("Task ID: ").strip()
    try:
        task_id = int(value)
    except ValueError as error:
        raise ValueError("Task ID must be a positive integer.") from error
    TaskManager._validate_task_id(task_id)
    return task_id


def _read_date(prompt: str) -> date | None:
    """Read an optional ISO-format date from the console."""
    value = input(prompt).strip()
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValueError("Enter a valid date in YYYY-MM-DD format.") from error


def _print_tasks(tasks: tuple[Task, ...]) -> None:
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        due_date = task.due_date.isoformat() if task.due_date else "None"
        print(
            f"#{task.task_id} | {task.title} | {task.priority.value} "
            f"| {task.status.value} "
            f"| due: {due_date} | {task.description}"
        )


def main() -> None:
    """Run the interactive task manager."""
    manager = TaskManager()
    while True:
        print("\nStudent Task Manager")
        print("1. List tasks")
        print("2. Create task")
        print("3. Update task")
        print("4. Delete task")
        print("5. View task by ID")
        print("6. Exit")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                _print_tasks(manager.list_tasks())
            elif choice == "2":
                title = input("Title: ")
                description = input("Description (optional): ")
                priority_text = input(
                    "Priority low/medium/high (default medium): "
                ).strip()
                priority = (
                    TaskPriority(priority_text) if priority_text else TaskPriority.MEDIUM
                )
                due_date = _read_date("Due date YYYY-MM-DD (optional): ")
                task = manager.create_task(title, description, due_date, priority)
                print(f"Created task #{task.task_id}.")
            elif choice == "3":
                task_id = _read_task_id()
                print("Leave a field blank to keep its current value.")
                title = input("New title: ")
                description = input("New description (use '-' to clear): ")
                due_date_text = input(
                    "New due date YYYY-MM-DD (use '-' to clear): "
                ).strip()
                status_text = input(
                    "New status todo/in_progress/done (optional): "
                ).strip()
                priority_text = input(
                    "New priority low/medium/high (optional): "
                ).strip()

                updates: dict[str, object] = {}
                if title.strip():
                    updates["title"] = title
                if description:
                    updates["description"] = "" if description == "-" else description
                if due_date_text:
                    updates["due_date"] = (
                        None if due_date_text == "-" else date.fromisoformat(due_date_text)
                    )
                if status_text:
                    updates["status"] = TaskStatus(status_text)
                if priority_text:
                    updates["priority"] = TaskPriority(priority_text)

                task = manager.update_task(task_id, updates)
                print(f"Updated task #{task.task_id}.")
            elif choice == "4":
                task_id = _read_task_id()
                manager.delete_task(task_id)
                print(f"Deleted task #{task_id}.")
            elif choice == "5":
                task_id = _read_task_id()
                _print_tasks((manager.get_task(task_id),))
            elif choice == "6":
                print("Goodbye.")
                return
            else:
                print("Choose a number from 1 to 6.")
        except (TaskNotFoundError, ValueError) as error:
            print(f"Error: {error}")


class TaskManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = TaskManager()

    def test_create_and_read_task(self) -> None:
        task = self.manager.create_task("  Read chapter  ", "Chapter 2")
        self.assertEqual(task.task_id, 1)
        self.assertEqual(task.title, "Read chapter")
        self.assertEqual(task.status, TaskStatus.TODO)
        self.assertEqual(task.priority, TaskPriority.MEDIUM)
        self.assertEqual(self.manager.get_task(1), task)
        self.assertEqual(self.manager.list_tasks(), (task,))

    def test_create_rejects_blank_title(self) -> None:
        with self.assertRaises(ValueError):
            self.manager.create_task("  ")

    def test_task_json_shape(self) -> None:
        task = self.manager.create_task(
            "Submit report",
            description="Upload PDF",
            due_date=date(2026, 11, 3),
            priority=TaskPriority.HIGH,
        )
        self.assertEqual(
            task.to_dict(),
            {
                "id": 1,
                "title": "Submit report",
                "description": "Upload PDF",
                "priority": "high",
                "status": "todo",
                "due_date": "2026-11-03",
            },
        )

    def test_update_fields_and_clear_due_date(self) -> None:
        task = self.manager.create_task("Submit project", due_date=date(2026, 11, 1))
        updated = self.manager.update_task(
            task.task_id,
            {
                "title": "Submit final project",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.HIGH,
                "due_date": None,
            },
        )
        self.assertEqual(updated.title, "Submit final project")
        self.assertEqual(updated.status, TaskStatus.DONE)
        self.assertEqual(updated.priority, TaskPriority.HIGH)
        self.assertIsNone(updated.due_date)

    def test_update_rejects_unknown_fields_and_empty_changes(self) -> None:
        task = self.manager.create_task("Prepare notes")
        with self.assertRaises(ValueError):
            self.manager.update_task(task.task_id, {})
        with self.assertRaises(ValueError):
            self.manager.update_task(task.task_id, {"student_id": 3})

    def test_missing_task_raises_for_read_update_and_delete(self) -> None:
        with self.assertRaises(TaskNotFoundError):
            self.manager.get_task(99)
        with self.assertRaises(TaskNotFoundError):
            self.manager.update_task(99, {"title": "Updated"})
        with self.assertRaises(TaskNotFoundError):
            self.manager.delete_task(99)

    def test_delete_removes_task_and_ids_are_not_reused(self) -> None:
        first = self.manager.create_task("First")
        self.manager.delete_task(first.task_id)
        second = self.manager.create_task("Second")
        self.assertEqual(second.task_id, 2)
        self.assertEqual(self.manager.list_tasks(), (second,))


if __name__ == "__main__":
    main()