# PawPal+ Project Reflection

## 1. System Design
The following actions user should perform,
1) Add a pet
2) Track the meds required
3) View today's care plan

**a. Initial design**

- Briefly describe your initial UML design.
The UML models a pet care scheduling system where an Owner manages multiple Pets and views DailyPlans. Each DailyPlan represents a specific day and contains multiple Tasks. Tasks define activities like feeding or walking, and each task is associated with a specific Pet.

- What classes did you include, and what responsibilities did you assign to each?
I included four main classes:
Owner – stores basic user information, manages pets, and views daily plans.
Pet – stores details about each pet like name, species, and age.
DailyPlan – represents a schedule for a specific day and manages a list of tasks.
Task – represents individual activities like feeding or walking, including duration, priority, completion status, and the pet it is assigned to.

**b. Design changes**

- Did your design change during implementation?
Yes, the design did change slightly during implementation.

- If yes, describe at least one change and why you made it.
I removed the unused field import since it wasn’t being used.
I introduced a Priority Enum to restrict values to low, medium, and high.
I changed Task.priority from a string to the Priority Enum to ensure valid inputs.
I added a plans list and a get_plans() method in the Owner class so the Owner can actually store and retrieve daily plans.
I added an owner reference inside DailyPlan so that generate() can access constraints like available time.
I updated add_task() and remove_task() to keep total_duration consistent whenever tasks are added or removed.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Detecting conflicts when multiple tasks are scheduled for the same pet on the same day.
Tradeoff:
A nested loop is simpler and easier to read, while a grouping-based approach is more efficient but more complex. The simpler approach was chosen since the task size is small.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
