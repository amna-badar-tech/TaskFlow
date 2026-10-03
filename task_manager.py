from datetime import datetime

from task import Task
from storage import TaskStorage


class TaskManager:
    """ Manages task operations."""

    PRIORITY_ORDER = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    def __init__(self):
        self.storage = TaskStorage()
        self.tasks = self.storage.load()

    def _save(self) -> None:
        """Save current tasks."""

        self.storage.save(self.tasks)

    def _generate_id(self) -> int:
        """Generate the next available task ID."""

        if not self.tasks:
            return 1

        return max(
            task.task_id
            for task in self.tasks
        ) + 1

    def add_task(
        self,
        title: str,
        priority: str,
        due_date: str | None
    ) -> Task:
        """Create and store a new task."""

        task = Task(
            task_id=self._generate_id(),
            title=title,
            priority=priority,
            due_date=due_date
        )

        self.tasks.append(task)
        self._save()

        return task

    def get_task(
        self,
        task_id: int
    ) -> Task | None:
        """Find a task by ID."""

        return next(
            (
                task
                for task in self.tasks
                if task.task_id == task_id
            ),
            None
        )

    def complete_task(
        self,
        task_id: int
    ) -> bool | None:
        """Mark a task as completed."""

        task = self.get_task(task_id)

        if task is None:
            return False

        if task.completed:
            return None

        task.completed = True
        self._save()

        return True

    def remove_task(
        self,
        task_id: int
    ) -> bool:
        """Remove a task."""

        task = self.get_task(task_id)

        if task is None:
            return False

        self.tasks.remove(task)
        self._save()

        return True

    def search(
        self,
        keyword: str
    ) -> list[Task]:
        """Search tasks by title."""

        keyword = keyword.lower().strip()

        return [
            task
            for task in self.tasks
            if keyword in task.title.lower()
        ]

    def filter_by_priority(
        self,
        priority: str
    ) -> list[Task]:
        """Filter tasks by priority."""

        return [
            task
            for task in self.tasks
            if task.priority == priority
        ]

    def get_sorted_tasks(self) -> list[Task]:
        """Sort tasks by status, priority and due date."""

        return sorted(
            self.tasks,
            key=lambda task: (
                task.completed,
                self.PRIORITY_ORDER[
                    task.priority
                ],
                task.due_date or "9999-12-31"
            )
        )

    def get_pending_tasks(self) -> list[Task]:
        """Return incomplete tasks."""

        return [
            task
            for task in self.tasks
            if not task.completed
        ]

    def get_completed_tasks(self) -> list[Task]:
        """Return completed tasks."""

        return [
            task
            for task in self.tasks
            if task.completed
        ]

    def is_overdue(
        self,
        task: Task
    ) -> bool:
        """Check whether a task is overdue."""

        if task.completed or not task.due_date:
            return False

        try:

            due_date = datetime.strptime(
                task.due_date,
                "%Y-%m-%d"
            ).date()

            return due_date < datetime.now().date()

        except ValueError:
            return False

    def statistics(self) -> dict:
        """Calculate task statistics."""

        total = len(self.tasks)

        completed = len(
            self.get_completed_tasks()
        )

        pending = total - completed

        overdue = sum(
            self.is_overdue(task)
            for task in self.tasks
        )

        progress = (
            (completed / total) * 100
            if total
            else 0
        )

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "overdue": overdue,
            "progress": progress
        }
