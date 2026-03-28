from dataclasses import dataclass, field
from typing import List
from datetime import date


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int

    def get_info(self) -> str:
        pass


@dataclass
class Task:
    name: str
    task_type: str
    duration: int
    priority: str
    pet: Pet
    is_completed: bool = False

    def mark_complete(self):
        pass

    def get_details(self) -> str:
        pass


class Owner:
    def __init__(self, name: str, available_time_per_day: int, preferences_notes: str):
        self.name = name
        self.available_time_per_day = available_time_per_day
        self.preferences_notes = preferences_notes
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        pass

    def get_info(self) -> str:
        pass


class DailyPlan:
    def __init__(self, date: date):
        self.date = date
        self.tasks: List[Task] = []
        self.total_duration: int = 0
        self.reasoning: str = ""

    def generate(self):
        pass

    def add_task(self, task: Task):
        pass

    def remove_task(self, task: Task):
        pass

    def display(self):
        pass
