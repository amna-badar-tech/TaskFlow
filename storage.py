import json
from pathlib import Path

from task import Task


class TaskStorage:
    """Handles saving and loading tasks."""

    def __init__(self, filename: str = "tasks.json"):
        self.file_path = Path(filename)

    def save(self, tasks: list[Task]) -> None:
        """Save tasks to a JSON file."""

        data = [
            task.to_dict()
            for task in tasks
        ]

        with self.file_path.open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def load(self) -> list[Task]:
        """Load tasks from JSON file."""

        if not self.file_path.exists():
            return []

        try:

            with self.file_path.open(
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            return [
                Task.from_dict(item)
                for item in data
            ]

        except (
            json.JSONDecodeError,
            KeyError,
            TypeError
        ):

            print(
                "\nWarning: Saved task data is invalid."
            )

            return []