from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, timedelta
from enum import Enum


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int

    def get_info(self) -> str:
        """Return a formatted summary of the pet's name, species, breed, and age."""
        return f"{self.name} ({self.species}, {self.breed}, {self.age} years old)"


@dataclass
class Task:
    name: str
    task_type: str
    duration: int
    priority: Priority
    pet: Pet
    is_completed: bool = False
    recurrence: str = "once"          # "once" | "daily" | "weekly"
    due_date: Optional[date] = field(default=None)

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as completed. Returns a new Task for the next occurrence if recurring."""
        self.is_completed = True
        intervals = {"daily": timedelta(days=1), "weekly": timedelta(days=7)}
        if self.recurrence in intervals:
            next_due = (self.due_date or date.today()) + intervals[self.recurrence]
            return Task(self.name, self.task_type, self.duration, self.priority,
                        self.pet, recurrence=self.recurrence, due_date=next_due)
        return None

    def get_details(self) -> str:
        """Return a formatted one-line summary of the task including priority, pet, duration, and status."""
        status = "Done" if self.is_completed else "Pending"
        due = f" | due {self.due_date}" if self.due_date else ""
        recur = f" | {self.recurrence}" if self.recurrence != "once" else ""
        return (
            f"[{self.priority.value.upper()}] {self.name} ({self.task_type}) "
            f"for {self.pet.name} — {self.duration} min — {status}{recur}{due}"
        )


class Owner:
    def __init__(self, name: str, available_time_per_day: int, preferences_notes: str):
        self.name = name
        self.available_time_per_day = available_time_per_day
        self.preferences_notes = preferences_notes
        self.pets: List[Pet] = []
        self.plans: List["DailyPlan"] = []

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_info(self) -> str:
        """Return a formatted summary of the owner's name, available time, pets, and notes."""
        pet_names = ", ".join(p.name for p in self.pets) if self.pets else "none"
        return (
            f"Owner: {self.name} | Available: {self.available_time_per_day} min/day | "
            f"Pets: {pet_names} | Notes: {self.preferences_notes}"
        )

    def get_plans(self) -> List["DailyPlan"]:
        """Return all daily plans associated with this owner."""
        return self.plans


class DailyPlan:
    def __init__(self, date: date, owner: Owner):
        self.date = date
        self.owner = owner
        self.tasks: List[Task] = []
        self.total_duration: int = 0
        self.reasoning: str = ""

    def generate(self):
        """Sort tasks by priority and schedule as many as fit within the owner's available time."""
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        self.tasks.sort(key=lambda t: (priority_order[t.priority], t.duration))

        avail = self.owner.available_time_per_day
        scheduled, skipped = [], []
        time_used = 0
        for task in self.tasks:
            if time_used + task.duration <= avail:
                scheduled.append(task)
                time_used += task.duration
            else:
                skipped.append(task)

        self.tasks = scheduled
        self.total_duration = time_used

        self.reasoning = f"Scheduled {len(scheduled)} task(s) using {time_used} of {avail} min available."
        if skipped:
            skipped_names = ", ".join(t.name for t in skipped)
            self.reasoning += f" Skipped {len(skipped)} low-priority task(s) due to time limits: {skipped_names}"

    def add_task(self, task: Task):
        """Add a task to the plan and update the total duration."""
        self.tasks.append(task)
        self.total_duration += task.duration

    def filter_by_status(self, completed: bool) -> List[Task]:
        """Return tasks matching the given completion status."""
        return [t for t in self.tasks if t.is_completed == completed]

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return all scheduled tasks for the given pet name."""
        return [t for t in self.tasks if t.pet.name == pet_name]

    def get_conflicts(self) -> List[str]:
        """Return warning messages for tasks sharing the same pet and due_date."""
        warnings = []
        for i, a in enumerate(self.tasks):
            for b in self.tasks[i + 1:]:
                if a.pet.name == b.pet.name and a.due_date is not None and a.due_date == b.due_date:
                    warnings.append(
                        f"Conflict: '{a.name}' and '{b.name}' both scheduled "
                        f"for {a.pet.name} on {a.due_date}"
                    )
        return warnings


    def remove_task(self, task: Task):
        """Remove a task from the plan and update the total duration."""
        self.tasks.remove(task)
        self.total_duration -= task.duration

    def display(self):
        """Print the daily plan as a formatted box with tasks grouped by priority and a time bar."""
        WIDTH = 52
        formatted_date = self.date.strftime("%B %d, %Y")
        priority_icons = {Priority.HIGH: "!!",  Priority.MEDIUM: " ~", Priority.LOW: "  "}

        print("┌" + "─" * WIDTH + "┐")
        title = "PawPal — Today's Schedule"
        print("│" + title.center(WIDTH) + "│")
        subtitle = f"{self.owner.name}  ·  {formatted_date}"
        print("│" + subtitle.center(WIDTH) + "│")
        print("├" + "─" * WIDTH + "┤")

        if not self.tasks:
            print("│" + "  No tasks scheduled.".ljust(WIDTH) + "│")
        else:
            current_priority = None
            for task in self.tasks:
                if task.priority != current_priority:
                    current_priority = task.priority
                    label = f"  [ {task.priority.value.upper()} ]"
                    print("│" + label.ljust(WIDTH) + "│")
                icon = priority_icons[task.priority]
                status = "✓" if task.is_completed else "○"
                line = f"  {icon} {status} {task.name:<22} {task.pet.name:<8} {task.duration:>3} min"
                print("│" + line.ljust(WIDTH) + "│")

        print("├" + "─" * WIDTH + "┤")

        avail = self.owner.available_time_per_day
        used = self.total_duration
        filled = int((used / avail) * 20) if avail else 0
        bar = "█" * filled + "░" * (20 - filled)
        time_line = f"  Time: {used}/{avail} min  [{bar}]"
        print("│" + time_line.ljust(WIDTH) + "│")

        if self.reasoning:
            import textwrap
            for chunk in textwrap.wrap(f"  {self.reasoning}", WIDTH):
                print("│" + chunk.ljust(WIDTH) + "│")

        print("└" + "─" * WIDTH + "┘")
