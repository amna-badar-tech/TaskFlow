import os
from datetime import datetime

from task import Task
from task_manager import TaskManager


class UI:
    """Handles the terminal user interface."""

    @staticmethod
    def clear() -> None:
        """Clear the terminal."""

        os.system(
            "cls"
            if os.name == "nt"
            else "clear"
        )

    @staticmethod
    def header() -> None:
        """Display application header."""

        print("=" * 65)
        print("                    TASKFLOW")
        print("              PROFESSIONAL TASK MANAGER")
        print("=" * 65)

    @staticmethod
    def progress(
        manager: TaskManager
    ) -> None:
        """Display progress information."""

        stats = manager.statistics()

        percentage = stats["progress"]

        width = 30

        filled = int(
            width * percentage / 100
        )

        bar = (
            "█" * filled
            + "░" * (width - filled)
        )

        print(
            f"\nProgress: [{bar}] "
            f"{percentage:.1f}%"
        )

        print(
            f"Total: {stats['total']} | "
            f"Completed: {stats['completed']} | "
            f"Pending: {stats['pending']} | "
            f"Overdue: {stats['overdue']}"
        )

    @staticmethod
    def menu() -> None:
        """Display main menu."""

        print("\n" + "-" * 65)
        print("MAIN MENU")
        print("-" * 65)

        options = [
            "1. Add Task",
            "2. View All Tasks",
            "3. Mark Task as Completed",
            "4. Remove Task",
            "5. Search Tasks",
            "6. Filter by Priority",
            "7. View Statistics",
            "8. View Pending Tasks",
            "9. View Completed Tasks",
            "0. Exit"
        ]

        print("\n".join(options))

        print("-" * 65)

    @staticmethod
    def display_tasks(
        tasks: list[Task],
        manager: TaskManager,
        title: str = "TASKS"
    ) -> None:
        """Display tasks in a clean format."""

        print("\n" + "=" * 65)
        print(f"{title:^65}")
        print("=" * 65)

        if not tasks:
            print("\nNo tasks found.")
            return

        for task in tasks:

            status = (
                "✓"
                if task.completed
                else " "
            )

            print(
                f"\n[{status}] "
                f"ID: {task.task_id}"
            )

            print(
                f"    Title    : "
                f"{task.title}"
            )

            print(
                f"    Priority : "
                f"{task.priority}"
            )

            print(
                f"    Due Date : "
                f"{task.due_date or 'No deadline'}"
            )

            if manager.is_overdue(task):
                print(
                    "    Status   : OVERDUE"
                )

            print(
                f"    Created  : "
                f"{task.created_at}"
            )

        print("\n" + "=" * 65)

    @staticmethod
    def get_priority() -> str:
        """Ask user to select priority."""

        priorities = {
            "1": "High",
            "2": "Medium",
            "3": "Low"
        }

        while True:

            print("\nSelect Priority:")
            print("1. High")
            print("2. Medium")
            print("3. Low")

            choice = input(
                "Enter choice: "
            ).strip()

            if choice in priorities:
                return priorities[choice]

            print(
                "\nInvalid choice. "
                "Please select 1, 2 or 3."
            )

    @staticmethod
    def get_due_date() -> str | None:
        """Ask user for a valid due date."""

        while True:

            value = input(
                "\nDue date "
                "(YYYY-MM-DD or Enter to skip): "
            ).strip()

            if not value:
                return None

            try:

                datetime.strptime(
                    value,
                    "%Y-%m-%d"
                )

                return value

            except ValueError:

                print(
                    "\nInvalid date format."
                    "\nExample: 2026-10-05"
                )

    @staticmethod
    def get_task_id() -> int:
        """Ask user for a valid task ID."""

        while True:

            value = input(
                "Enter Task ID: "
            ).strip()

            if value.isdigit():
                return int(value)

            print(
                "Invalid ID. "
                "Please enter a number."
            )

    @staticmethod
    def pause() -> None:
        """Pause before returning to menu."""

        input(
            "\nPress Enter to continue..."
        )