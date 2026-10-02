from task_manager import TaskManager
from ui import UI


class TaskFlow:
    """Main controller for the TaskFlow application."""

    def __init__(self):
        self.manager = TaskManager()

    def add_task(self):
        """Create a new task."""

        print("\n" + "=" * 65)
        print("ADD NEW TASK")
        print("=" * 65)

        title = input("\nEnter task title: ").strip()

        if not title:
            print("\nTask title cannot be empty.")
            return

        priority = UI.get_priority()
        due_date = UI.get_due_date()

        task = self.manager.add_task(
            title,
            priority,
            due_date
        )

        print(
            f"\n✓ Task added successfully!"
            f"\nTask ID: {task.task_id}"
        )

    def view_tasks(self):
        """Display all tasks."""

        tasks = self.manager.get_sorted_tasks()

        UI.display_tasks(
            tasks,
            self.manager,
            "ALL TASKS"
        )

    def complete_task(self):
        """Mark a selected task as completed."""

        if not self.manager.tasks:
            print("\nNo tasks available.")
            return

        self.view_tasks()

        task_id = UI.get_task_id()

        result = self.manager.complete_task(task_id)

        if result is True:
            print("\n✓ Task marked as completed!")

        elif result is None:
            print("\nTask is already completed.")

        else:
            print("\nTask not found.")

    def remove_task(self):
        """Remove a selected task."""

        if not self.manager.tasks:
            print("\nNo tasks available.")
            return

        self.view_tasks()

        task_id = UI.get_task_id()

        task = self.manager.get_task(task_id)

        if task is None:
            print("\nTask not found.")
            return

        confirmation = input(
            f'\nRemove "{task.title}"? (y/n): '
        ).strip().lower()

        if confirmation == "y":
            self.manager.remove_task(task_id)
            print("\n✓ Task removed successfully!")

        else:
            print("\nTask removal cancelled.")

    def search_tasks(self):
        """Search tasks by keyword."""

        keyword = input(
            "\nEnter keyword: "
        ).strip()

        if not keyword:
            print("\nSearch keyword cannot be empty.")
            return

        results = self.manager.search(keyword)

        UI.display_tasks(
            results,
            self.manager,
            f'SEARCH: "{keyword}"'
        )

    def filter_tasks(self):
        """Filter tasks by priority."""

        priority = UI.get_priority()

        results = self.manager.filter_by_priority(
            priority
        )

        UI.display_tasks(
            results,
            self.manager,
            f"{priority.upper()} PRIORITY TASKS"
        )

    def show_statistics(self):
        """Display task statistics."""

        stats = self.manager.statistics()

        print("\n" + "=" * 65)
        print("TASK STATISTICS")
        print("=" * 65)

        print(f"\nTotal Tasks     : {stats['total']}")
        print(f"Completed Tasks : {stats['completed']}")
        print(f"Pending Tasks   : {stats['pending']}")
        print(f"Overdue Tasks   : {stats['overdue']}")
        print(
            f"Completion Rate : "
            f"{stats['progress']:.1f}%"
        )

    def show_pending_tasks(self):
        """Display pending tasks."""

        tasks = self.manager.get_pending_tasks()

        UI.display_tasks(
            tasks,
            self.manager,
            "PENDING TASKS"
        )

    def show_completed_tasks(self):
        """Display completed tasks."""

        tasks = self.manager.get_completed_tasks()

        UI.display_tasks(
            tasks,
            self.manager,
            "COMPLETED TASKS"
        )

    def run(self):
        """Run the main application loop."""

        while True:

            UI.clear()
            UI.header()
            UI.progress(self.manager)
            UI.menu()

            choice = input(
                "\nEnter your choice: "
            ).strip()

            if choice == "1":
                self.add_task()

            elif choice == "2":
                self.view_tasks()

            elif choice == "3":
                self.complete_task()

            elif choice == "4":
                self.remove_task()

            elif choice == "5":
                self.search_tasks()

            elif choice == "6":
                self.filter_tasks()

            elif choice == "7":
                self.show_statistics()

            elif choice == "8":
                self.show_pending_tasks()

            elif choice == "9":
                self.show_completed_tasks() 

            elif choice == "0":
                print("\nTasks saved successfully.")
                print("Thank you for using TaskFlow!")
                print("Goodbye!")
                break

            else:
                print(
                    "\nInvalid option. "
                    "Please select a valid option."
                )

            UI.pause()


if __name__ == "__main__":
    app = TaskFlow()
    app.run()