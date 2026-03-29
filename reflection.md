# PawPal+ Project Reflection

## 1. System Design
The following actions user should perform,
1) Add a pet - Enter details about your pet, such as name, species, breed, and age.
2) Add tasks - Provide the tasks that need to be done, including duration, priority, frequency, and due date.
3) Generate and view today’s plan - Create a daily schedule and view the ordered plan based on priorities and available time.

**a. Initial design**

The UML models a pet care scheduling system where an Owner manages multiple Pets and views DailyPlans. Each DailyPlan represents a specific day and contains multiple Tasks. Tasks define activities like feeding or walking, and each task is associated with a specific Pet.

I included four main classes:
Owner – stores basic user information, manages pets, and views daily plans.
Pet – stores details about each pet like name, species, and age.
DailyPlan – represents a schedule for a specific day and manages a list of tasks.
Task – represents individual activities like feeding or walking, including duration, priority, completion status, and the pet it is assigned to.

**b. Design changes**

The design did change slightly during implementation.

I removed the unused field import since it wasn’t being used.
I introduced a Priority Enum to restrict values to low, medium, and high.
I changed Task.priority from a string to the Priority Enum to ensure valid inputs.
I added a plans list and a get_plans() method in the Owner class so the Owner can actually store and retrieve daily plans.
I added an owner reference inside DailyPlan so that generate() can access constraints like available time.
I updated add_task() and remove_task() to keep total_duration consistent whenever tasks are added or removed.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers available time, task priority, and urgency.

The most important constraint is the owner’s available time, so only tasks that fit within that time are scheduled. Tasks are then ordered by priority (high, medium, low).

Urgency is also considered through weighted scoring, where tasks due sooner, medical tasks, and tasks for older pets are given higher importance.

**b. Tradeoffs**

Detecting conflicts when multiple tasks are scheduled for the same pet on the same day.
Tradeoff:
A nested loop is simpler and easier to read, while a grouping-based approach is more efficient but more complex. The simpler approach was chosen since the task size is small.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI tools mainly for design brainstorming, debugging, and improving the structure of the code. I used it to think through how to model the classes, refine the scheduling logic, and fix issues in the Streamlit app.

The most helpful prompts were specific and focused, such as asking to fix a particular bug, improve UI behavior, or validate whether my logic made sense. I avoided vague prompts and instead described exactly what my code was doing and what I wanted to change.

**b. Judgment and verification**

One moment where I did not accept an AI suggestion directly was when it suggested changes to my scheduling logic and task completion flow. The suggestion introduced assumptions about how tasks should be handled that did not match my existing backend design.

Instead of applying it blindly, I checked how my current classes and methods actually worked, especially around mark_complete() and how tasks were added back for recurrence. I compared the AI suggestion with my implementation and only adopted the parts that aligned with my design.

To verify the changes, I tested the behavior in the app and also relied on my existing test cases to make sure nothing broke. This helped me ensure that the final implementation was correct and consistent with my system.

---

## 4. Testing and Verification

**a. What you tested**

I tested key behaviors like task scheduling, conflict detection, task completion, and recurrence handling.

I checked whether tasks were correctly selected based on priority and available time, whether conflicts were flagged properly, and whether recurring tasks were generated correctly after marking tasks as complete.

These tests were important to make sure the system behaves as expected in real scenarios. Since the app involves multiple interacting components (tasks, pets, scheduling logic), testing helped ensure that changes in one part did not break other parts and that the overall planning logic remained reliable.

**b. Confidence**

I am fairly confident that the scheduler works correctly for the main cases I designed it for. It can add tasks, prioritize them, fit them within the available time, detect basic conflicts, and handle recurring tasks when they are marked complete.

If I had more time, I would test more edge cases such as tasks with the same score, multiple recurring tasks across several days, duplicate task names, very large numbers of tasks, and more detailed time-based conflicts within the same day. I would also test more cases around editing or removing tasks after a schedule has already been generated.

---

## 5. Reflection

**a. What went well**

The part I am most satisfied with is the initial design phase where I created the classes and structured the system. I had always struggled with understanding how to properly implement object-oriented programming, but working on this project helped me apply those concepts in a practical way. Defining classes like Owner, Pet, Task, and DailyPlan and seeing how they interact made everything much clearer. It was very satisfying to see the design come together and actually work in the app.

**b. What you would improve**

If I had another iteration, I would improve the scheduling system by making it more realistic and flexible. Right now, it creates a good daily plan, but I would like to support true time-based scheduling with actual start and end times instead of just ordering tasks. I would also improve conflict detection, allow users to edit or remove tasks more easily, and make better use of owner preferences in scheduling decisions. Overall, I would focus on making the app feel more complete and closer to a real pet care planner.

**c. Key takeaway**

One important thing I learned is that designing a system requires clear thinking about how different parts interact, not just writing code. Breaking the problem into classes like Owner, Pet, Task, and DailyPlan helped me understand how to structure the solution properly.

I also learned that AI tools are most helpful when used carefully. Instead of accepting suggestions directly, I needed to verify them against my own design and test them. This helped me use AI as a support tool rather than relying on it blindly.

