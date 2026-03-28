import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from datetime import date
from pawpal_systems import Owner, Pet, Task, DailyPlan, Priority


class TestMarkComplete(unittest.TestCase):
    def test_mark_complete_changes_status(self):
        dog = Pet("Max", "Dog", "Labrador", 3)
        task = Task("Feed Max", "Daily", 15, Priority.HIGH, dog)

        self.assertFalse(task.is_completed)
        task.mark_complete()
        self.assertTrue(task.is_completed)


class TestTaskAddition(unittest.TestCase):
    def test_add_task_increases_plan_task_count(self):
        dog = Pet("Max", "Dog", "Labrador", 3)
        owner = Owner("John", 60, "")
        plan = DailyPlan(date.today(), owner)

        self.assertEqual(len(plan.tasks), 0)
        plan.add_task(Task("Feed Max", "Daily", 15, Priority.HIGH, dog))
        self.assertEqual(len(plan.tasks), 1)


if __name__ == "__main__":
    unittest.main()
