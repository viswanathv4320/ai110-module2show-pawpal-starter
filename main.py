from pawpal_systems import Owner, Pet, Task, DailyPlan, Priority
from datetime import date

# Create an owner
owner = Owner("John Doe", 60, "Prefers morning routines")

# Create pets
dog = Pet("Max", "Dog", "Labrador", 3)
cat = Pet("Luna", "Cat", "Persian", 2)
parrot = Pet("Shelly", "Parrot", "African Grey", 1)
hamster = Pet("Nibbles", "Hamster", "Syrian", 1)

# Add pets to owner
owner.add_pet(dog)
owner.add_pet(cat)
owner.add_pet(parrot)
owner.add_pet(hamster)

# Create tasks
task1 = Task("Feed Max", "Daily", 15, Priority.HIGH, dog)
task2 = Task("Medicate Luna", "Health", 10, Priority.HIGH, cat)
task3 = Task("Trim Parrot's nails", "Grooming", 5, Priority.MEDIUM, parrot)
task4 = Task("Exercise Hamster", "Exercise", 20, Priority.LOW, hamster)

# Build and display the daily plan
plan = DailyPlan(date.today(), owner)
plan.add_task(task1)
plan.add_task(task2)
plan.add_task(task3)
plan.add_task(task4)
plan.generate()

plan.display()

# Mark one task complete to make status filtering interesting
task2.mark_complete()

# All tasks (sorted by priority after generate())
print("\n--- All Scheduled Tasks ---")
for task in plan.tasks:
    print(task.get_details())

# Filter by pet name
print("\n--- Tasks for Max ---")
for task in plan.filter_by_pet("Max"):
    print(task.get_details())

# Filter by completion status
print("\n--- Pending Tasks ---")
for task in plan.filter_by_status(completed=False):
    print(task.get_details())

print("\n--- Completed Tasks ---")
for task in plan.filter_by_status(completed=True):
    print(task.get_details())

# Conflict detection — two tasks for Max on the same due_date
conflict_date = date(2026, 4, 1)
task5 = Task("Walk Max", "Exercise", 20, Priority.MEDIUM, dog, due_date=conflict_date)
task6 = Task("Bathe Max", "Grooming", 15, Priority.LOW, dog, due_date=conflict_date)
plan.add_task(task5)
plan.add_task(task6)

print("\n--- Conflict Warnings ---")
warnings = plan.get_conflicts()
if warnings:
    for w in warnings:
        print(w)
else:
    print("No conflicts found.")