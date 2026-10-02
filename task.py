from datetime import datetime
from typing import Optional


class Task:
    """Represents a single task."""

    def __init__(
        self,
        task_id: int,
        title: str,
        priority: str = "Medium",
        due_date: Optional[str] = None,
        completed: bool = False,
        created_at: Optional[str] = None
    ):
        self.task_id = task_id
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

        self.created_at = (
            created_at
            or datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

    def to_dict(self) -> dict:
        """Convert task object into a dictionary."""

        return {
            "task_id": self.task_id,
            "title": self.title,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task object from dictionary data."""

        return cls(
            task_id=data["task_id"],
            title=data["title"],
            priority=data.get(
                "priority",
                "Medium"
            ),
            due_date=data.get("due_date"),
            completed=data.get(
                "completed",
                False
            ),
            created_at=data.get("created_at")
        )