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