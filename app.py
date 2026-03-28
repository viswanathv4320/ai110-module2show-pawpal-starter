import streamlit as st
from pawpal_systems import Owner, Pet, Task, DailyPlan, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value="Jordan")
available_time = st.number_input("Available time (minutes/day)", min_value=10, max_value=480, value=120)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Create or update Owner in session_state
if (
    "owner" not in st.session_state
    or st.session_state.owner.name != owner_name
    or st.session_state.owner.available_time_per_day != available_time
):
    st.session_state.owner = Owner(name=owner_name, available_time_per_day=available_time, preferences_notes="")
    st.session_state.plan = None  # reset plan when owner changes

# Create or update Pet in session_state
if "pet" not in st.session_state or st.session_state.pet.name != pet_name or st.session_state.pet.species != species:
    st.session_state.pet = Pet(name=pet_name, species=species, breed="unknown", age=0)
    st.session_state.plan = None  # reset plan when pet changes

# Create DailyPlan once (or after reset)
if "plan" not in st.session_state or st.session_state.plan is None:
    from datetime import date
    st.session_state.plan = DailyPlan(date=date.today(), owner=st.session_state.owner)

plan = st.session_state.plan

st.markdown("### Tasks")
st.caption("Add tasks — they are stored in the DailyPlan object.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_type = st.selectbox("Task type", ["exercise", "feeding", "grooming", "medical", "play", "other"])
with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col4:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    task = Task(
        name=task_title,
        task_type=task_type,
        duration=int(duration),
        priority=Priority(priority),
        pet=st.session_state.pet,
    )
    plan.add_task(task)

if plan.tasks:
    st.write("Current tasks:")
    st.table([
        {"task": t.name, "duration (min)": t.duration, "priority": t.priority.value, "pet": t.pet.name}
        for t in plan.tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generates the daily plan based on available time and task priorities.")

if st.button("Generate schedule"):
    plan.generate()
    st.success(plan.reasoning)
    if plan.tasks:
        st.table([
            {"task": t.name, "duration (min)": t.duration, "priority": t.priority.value, "pet": t.pet.name}
            for t in plan.tasks
        ])
