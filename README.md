# PawPal+ (Module 2 Project)

PawPal+ is a Streamlit app that helps pet owners plan and manage daily care tasks efficiently.

---

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

---

## What you will build

Your final app should:

- Let a user enter basic owner + pet info  
- Let a user add/edit tasks (duration + priority at minimum)  
- Generate a daily schedule/plan based on constraints and priorities  
- Display the plan clearly (and ideally explain the reasoning)  
- Include tests for the most important scheduling behaviors  

---

## Features (Smarter Scheduling)

The scheduling logic includes:

- Priority-based sorting with duration as a secondary key for efficient time usage  
- Task filtering by pet and completion status  
- Support for recurring tasks (daily, weekly) with automatic regeneration  
- Lightweight conflict detection for overlapping tasks per pet  

---

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

---

## Testing PawPal+

The PawPal+ system includes an automated test suite to verify scheduling, recurrence, and conflict detection behavior.

### Run tests

```bash
python -m pytest
```

### What the tests cover

- **Schedule Generation Edge Cases**
  - Handles empty task lists without errors  
  - Ensures tasks are scheduled based on priority within the available time budget  

- **Recurrence Logic**
  - Verifies that marking a "daily" task as complete creates a new task for the next day  
  - Confirms that "one-time" tasks do not recur  

- **Conflict Detection**
  - Flags tasks with overlapping dates as conflicts  
  - Detects duplicate start times (same due date and duration)  
  - Ensures non-overlapping tasks are not flagged  
  - Handles boundary cases (consecutive days) without false positives  
  - Confirms tasks for different pets are not incorrectly flagged as conflicts  

- **System Stability**
  - Prevents runtime errors (e.g., division by zero when available time is zero)  

---

### Current limitation

The current `get_conflicts()` implementation uses `due_date` as the only time dimension.  
This limits conflict detection to day-level granularity.

Intra-day conflict detection (e.g., 09:00–09:30 vs 09:30–10:00) is not supported.  
Supporting this would require adding a `start_time` field to the `Task` model.

---

### Test results

All 14 tests are passing successfully.

---

### Confidence Level

⭐⭐⭐⭐☆ (4/5)

The system is reliable for current functionality, including scheduling, recurrence, and conflict detection.  
Confidence is slightly reduced due to the absence of intra-day time-based conflict handling.

---

## Development Workflow (Optional)

1. Read the scenario and identify requirements and edge cases  
2. Draft a UML diagram (classes, attributes, methods, relationships)  
3. Convert UML into Python class stubs  
4. Implement scheduling logic incrementally  
5. Add tests to verify key behaviors  
6. Connect logic to the Streamlit UI (`app.py`)  
7. Refine UML to match the final implementation  