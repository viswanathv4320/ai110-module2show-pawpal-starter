import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from datetime import date, timedelta
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


class TestGenerateEdgeCases(unittest.TestCase):
    def test_generate_no_tasks(self):
        owner = Owner("Jane", 60, "")
        plan = DailyPlan(date.today(), owner)
        plan.generate()
        self.assertEqual(plan.tasks, [])
        self.assertEqual(plan.total_duration, 0)
        self.assertIn("0", plan.reasoning)

    def test_generate_schedules_by_priority_within_budget(self):
        dog = Pet("Max", "Dog", "Labrador", 3)
        owner = Owner("Jane", 30, "")
        plan = DailyPlan(date.today(), owner)
        plan.add_task(Task("Groom", "Grooming", 20, Priority.LOW, dog))
        plan.add_task(Task("Walk", "Exercise", 20, Priority.HIGH, dog))
        plan.generate()
        # Only one 20-min task fits in 30 min; it should be the HIGH priority one
        self.assertEqual(len(plan.tasks), 1)
        self.assertEqual(plan.tasks[0].priority, Priority.HIGH)
        self.assertIn("Groom", plan.reasoning)


class TestMarkCompleteRecurrence(unittest.TestCase):
    def test_daily_recurrence_returns_next_task(self):
        dog = Pet("Max", "Dog", "Labrador", 3)
        today = date.today()
        task = Task("Feed Max", "Daily", 15, Priority.HIGH, dog,
                    recurrence="daily", due_date=today)
        next_task = task.mark_complete()
        self.assertTrue(task.is_completed)
        self.assertIsNotNone(next_task)
        self.assertEqual(next_task.due_date, today + timedelta(days=1))

    def test_once_recurrence_returns_none(self):
        dog = Pet("Max", "Dog", "Labrador", 3)
        task = Task("Vet visit", "Medical", 60, Priority.HIGH, dog, recurrence="once")
        result = task.mark_complete()
        self.assertIsNone(result)


class TestGetConflicts(unittest.TestCase):
    def test_detects_same_pet_same_date_conflict(self):
        dog = Pet("Max", "Dog", "Labrador", 3)
        owner = Owner("Jane", 120, "")
        plan = DailyPlan(date.today(), owner)
        today = date.today()
        plan.add_task(Task("Walk", "Exercise", 20, Priority.HIGH, dog, due_date=today))
        plan.add_task(Task("Groom", "Grooming", 30, Priority.MEDIUM, dog, due_date=today))
        conflicts = plan.get_conflicts()
        self.assertEqual(len(conflicts), 1)
        self.assertIn("Max", conflicts[0])

    def test_no_conflict_for_different_pets(self):
        dog = Pet("Max", "Dog", "Labrador", 3)
        cat = Pet("Luna", "Cat", "Siamese", 2)
        owner = Owner("Jane", 120, "")
        plan = DailyPlan(date.today(), owner)
        today = date.today()
        plan.add_task(Task("Walk", "Exercise", 20, Priority.HIGH, dog, due_date=today))
        plan.add_task(Task("Feed", "Daily", 10, Priority.HIGH, cat, due_date=today))
        self.assertEqual(plan.get_conflicts(), [])

    def test_no_conflict_when_due_date_is_none(self):
        dog = Pet("Max", "Dog", "Labrador", 3)
        owner = Owner("Jane", 120, "")
        plan = DailyPlan(date.today(), owner)
        plan.add_task(Task("Walk", "Exercise", 20, Priority.HIGH, dog))
        plan.add_task(Task("Groom", "Grooming", 30, Priority.MEDIUM, dog))
        self.assertEqual(plan.get_conflicts(), [])


class TestConflictDetection(unittest.TestCase):
    # NOTE: Task has no start_time field; get_conflicts() uses due_date equality as
    # a proxy for "same time slot". Tests below model each scenario accordingly.
    # Full intra-day interval checking would require adding start_time to Task.

    def setUp(self):
        self.dog = Pet("Max", "Dog", "Labrador", 3)
        self.owner = Owner("Jane", 120, "")
        self.today = date.today()

    def _make_plan(self, *tasks):
        plan = DailyPlan(self.today, self.owner)
        for t in tasks:
            plan.add_task(t)
        return plan

    def test_overlapping_intervals_flagged(self):
        # Two tasks for the same pet on the same date represent overlapping time slots.
        task_a = Task("Walk",  "Exercise", 30, Priority.HIGH,   self.dog, due_date=self.today)
        task_b = Task("Groom", "Grooming", 20, Priority.MEDIUM, self.dog, due_date=self.today)
        plan = self._make_plan(task_a, task_b)
        conflicts = plan.get_conflicts()
        self.assertEqual(len(conflicts), 1)
        self.assertIn("Walk",  conflicts[0])
        self.assertIn("Groom", conflicts[0])

    def test_duplicate_start_time_flagged(self):
        # Two tasks with the same due_date and same duration simulate identical start times.
        task_a = Task("Feed",  "Feeding",  15, Priority.HIGH, self.dog, due_date=self.today)
        task_b = Task("Brush", "Grooming", 15, Priority.HIGH, self.dog, due_date=self.today)
        plan = self._make_plan(task_a, task_b)
        conflicts = plan.get_conflicts()
        self.assertEqual(len(conflicts), 1)
        self.assertIn("Max", conflicts[0])

    def test_non_overlapping_times_not_flagged(self):
        # Tasks on different dates for the same pet do not overlap.
        task_a = Task("Walk",  "Exercise", 30, Priority.HIGH,   self.dog, due_date=self.today)
        task_b = Task("Groom", "Grooming", 20, Priority.MEDIUM, self.dog,
                      due_date=self.today + timedelta(days=1))
        plan = self._make_plan(task_a, task_b)
        self.assertEqual(plan.get_conflicts(), [])

    def test_boundary_adjacent_dates_not_flagged(self):
        # A task due today and one due tomorrow are adjacent but not overlapping;
        # get_conflicts() must not flag them as a conflict.
        # NOTE: intra-day boundary precision (e.g. 09:00–09:30 / 09:30–10:00) requires
        # a start_time field on Task — this test covers the date-level boundary.
        task_a = Task("Walk",  "Exercise", 60, Priority.HIGH,   self.dog, due_date=self.today)
        task_b = Task("Groom", "Grooming", 60, Priority.MEDIUM, self.dog,
                      due_date=self.today + timedelta(days=1))
        plan = self._make_plan(task_a, task_b)
        self.assertEqual(plan.get_conflicts(), [])


class TestDisplayZeroTime(unittest.TestCase):
    def test_display_does_not_crash_with_zero_available_time(self):
        owner = Owner("Jane", 0, "")
        plan = DailyPlan(date.today(), owner)
        try:
            plan.display()
        except ZeroDivisionError:
            self.fail("display() raised ZeroDivisionError with available_time_per_day=0")


if __name__ == "__main__":
    unittest.main()
