import streamlit as st
from datetime import date
from pawpal_systems import Owner, Pet, Task, DailyPlan, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown("Plan, organize, and schedule daily pet care tasks with clear priorities.")

# Session State Initialization
if "owner" not in st.session_state:
    st.session_state.owner = None

if "pets" not in st.session_state:
    st.session_state.pets = []

if "plan" not in st.session_state:
    st.session_state.plan = None

if "generated" not in st.session_state:
    st.session_state.generated = False

if "all_tasks_snapshot" not in st.session_state:
    st.session_state.all_tasks_snapshot = None

if "day_start_hour" not in st.session_state:
    st.session_state.day_start_hour = 8

PRIORITY_EMOJI = {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}

SPECIES_EMOJI = {
    "dog":     "🐶",
    "cat":     "🐱",
    "parrot":  "🦜",
    "hamster": "🐹",
    "other":   "🐾",
}

def fmt_pet(pet) -> str:
    emoji = SPECIES_EMOJI.get(pet.species, "🐾")
    return f"{emoji} {pet.name}"

TYPE_EMOJI = {
    "exercise": "🏃 Exercise",
    "feeding":  "🍽️ Feeding",
    "grooming": "✂️ Grooming",
    "medical":  "💊 Medical",
    "play":     "🎾 Play",
    "other":    "📋 Other",
}

def fmt_status(is_completed: bool) -> str:
    return "✅ Done" if is_completed else "⏳ Pending"

def create_or_reset_plan():
    if st.session_state.owner is not None:
        st.session_state.plan = DailyPlan(
            date=date.today(),
            owner=st.session_state.owner
        )
        st.session_state.generated = False
        st.session_state.all_tasks_snapshot = None

# ── Owner Details ────────────────────────────────────────────────────────────────
st.subheader("Owner Details")

with st.form("owner_form"):
    owner_name = st.text_input("Owner name", value=st.session_state.owner.name if st.session_state.owner else "")
    available_time = st.number_input(
        "Available time per day (minutes)",
        min_value=10,
        max_value=480,
        value=st.session_state.owner.available_time_per_day if st.session_state.owner else 60,
    )
    save_owner = st.form_submit_button("Save Owner Details")

if save_owner:
    # If owner details change, rebuild owner and plan
    new_owner = Owner(
        name=owner_name,
        available_time_per_day=int(available_time),
        preferences_notes=""
    )

    # Preserve already added pets if any
    for pet in st.session_state.pets:
        new_owner.add_pet(pet)

    st.session_state.owner = new_owner
    create_or_reset_plan()
    st.success("Owner details saved.")

if st.session_state.owner:
    st.info(st.session_state.owner.get_info())


st.divider()

# ── Pet Details ─────────────────────────────────────────────────────────────
st.subheader("Pet Details")

if st.session_state.owner is None:
    st.warning("Please save owner details before adding pets.")
else:
    with st.form("pet_form", clear_on_submit=True):
        pet_name = st.text_input("Pet name")
        species_display = [f"{SPECIES_EMOJI[s]} {s}" for s in ["dog", "cat", "hamster", "parrot", "other"]]
        species_choice = st.selectbox("Species", species_display)
        species = species_choice.split(" ", 1)[1]
        breed = st.text_input("Breed", value="")
        age = st.number_input("Age", min_value=0, max_value=50)
        add_pet_btn = st.form_submit_button("Add Pet")

    if add_pet_btn:
        if not pet_name.strip():
            st.error("Please enter a pet name.")
        else:
            new_pet = Pet(
                name=pet_name.strip(),
                species=species,
                breed=breed.strip() if breed.strip() else "unknown",
                age=int(age),
            )

            # Avoid duplicate pet names
            existing_pet_names = [pet.name for pet in st.session_state.pets]
            if new_pet.name in existing_pet_names:
                st.error(f"A pet named '{new_pet.name}' already exists.")
            else:
                st.session_state.pets.append(new_pet)
                st.session_state.owner.add_pet(new_pet)
                st.success(f"Pet '{new_pet.name}' added.")

if st.session_state.pets:
    st.markdown("**Saved Pets**")
    st.dataframe(
        [
            {
                "Name": pet.name,
                "Species": f"{SPECIES_EMOJI.get(pet.species, '🐾')} {pet.species}",
                "Breed": pet.breed,
                "Age": pet.age,
            }
            for pet in st.session_state.pets
        ],
        use_container_width=True,
        hide_index=True,
    )

st.divider()

# ── Task Details ─────────────────────────────────────────────────────────────────
st.subheader("Task Details")

if st.session_state.owner is None:
    st.warning("Please save owner details first.")
elif not st.session_state.pets:
    st.warning("Please add at least one pet before creating tasks.")
else:
    plan = st.session_state.plan

    with st.form("task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            task_title = st.text_input("Task title")
            task_type = st.selectbox(
                "Task type",
                ["exercise", "feeding", "grooming", "medical", "play", "other"],
            )
            pet_options = [f"{SPECIES_EMOJI.get(pet.species, '🐾')} {pet.name}" for pet in st.session_state.pets]
            pet_choice = st.selectbox("Pet", pet_options)
            task_pet_name = pet_choice.split(" ", 1)[1]
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
            recurrence = st.selectbox("Frequency", ["once", "daily", "weekly"])
            due_date = st.date_input("Due date", value=date.today())

        add_task_btn = st.form_submit_button("Add Task")

    if add_task_btn:
        if not task_title.strip():
            st.error("Please enter a task title.")
        else:
            selected_pet = next(
                (pet for pet in st.session_state.pets if pet.name == task_pet_name),
                None,
            )

            if selected_pet is None:
                st.error("Selected pet not found.")
            else:
                plan.add_task(
                    Task(
                        name=task_title.strip(),
                        task_type=task_type,
                        duration=int(duration),
                        priority=Priority(priority),
                        pet=selected_pet,
                        recurrence=recurrence,
                        due_date=due_date,
                    )
                )
                st.session_state.generated = False
                st.session_state.all_tasks_snapshot = None
                st.success(f"Task '{task_title}' added.")

st.divider()

# ── Task List ────────────────────────────────────
st.subheader("Tasks")

plan = st.session_state.plan
display_tasks = (
    st.session_state.all_tasks_snapshot
    if st.session_state.generated and st.session_state.all_tasks_snapshot is not None
    else plan.tasks if plan else []
)

if not display_tasks:
    st.info("No tasks added yet.")
else:
    st.dataframe(
        [
            {
                "Task": t.name,
                "Type": TYPE_EMOJI.get(t.task_type, f"📋 {t.task_type}"),
                "Duration (min)": t.duration,
                "Priority": PRIORITY_EMOJI[t.priority.value],
                "Score": t.weight_score(),
                "Pet": fmt_pet(t.pet),
                "Frequency": t.recurrence,
                "Due Date": str(t.due_date) if t.due_date else "—",
                "Status": fmt_status(t.is_completed),
            }
            for t in display_tasks
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.caption("Score = weighted priority (urgency + task type + pet age + recurrence). Higher score → scheduled first.")

    conflicts = plan.get_conflicts() if plan else []
    if conflicts:
        st.markdown("**Scheduling conflicts**")
        for msg in conflicts:
            st.warning(msg)
    else:
        st.success("No scheduling conflicts found.")

    pending = [t for t in plan.tasks if not t.is_completed] if plan else []
    if pending:
        st.markdown("**Mark tasks complete**")
        for task in pending:
            task_key = f"complete_{task.name}_{task.pet.name}_{task.due_date}_{task.duration}"
            if st.button(f"✓ Mark '{task.name}' complete", key=task_key):
                next_task = task.mark_complete()
                if next_task:
                    plan.add_task(next_task)
                st.session_state.generated = False
                st.session_state.all_tasks_snapshot = None
                st.rerun()

st.divider()

# ── Schedule Generation ────────────────────────────────────────────────────────
st.subheader("Create Schedule")
st.caption(
    "Tasks are ranked by weighted score (urgency, type, pet age, recurrence), "
    "then fitted into your available time with real clock-time slots."
)

if plan is None:
    st.warning("Please save owner details first.")
elif not plan.tasks:
    st.info("Add tasks before generating a schedule.")
else:
    day_start_hour = st.slider(
        "Day starts at (hour)",
        min_value=5,
        max_value=12,
        value=st.session_state.day_start_hour,
        format="%d:00",
        help="The first task will be placed at this hour.",
    )
    st.session_state.day_start_hour = day_start_hour

    if st.button("Generate Schedule"):
        st.session_state.all_tasks_snapshot = list(plan.tasks)
        plan.generate(day_start_minutes=day_start_hour * 60)
        st.session_state.generated = True

if st.session_state.generated and plan:
    if plan.tasks:
        st.markdown("### Scheduled Tasks")

        scheduled_rows = []
        for idx, task in enumerate(plan.tasks, start=1):
            scheduled_rows.append(
                {
                    "#": idx,
                    "Time Slot": task.time_slot(),
                    "Task": task.name,
                    "Type": TYPE_EMOJI.get(task.task_type, f"📋 {task.task_type}"),
                    "Duration (min)": task.duration,
                    "Priority": PRIORITY_EMOJI[task.priority.value],
                    "Score": task.weight_score(),
                    "Pet": fmt_pet(task.pet),
                    "Frequency": task.recurrence,
                    "Due Date": str(task.due_date) if task.due_date else "—",
                    "Status": fmt_status(task.is_completed),
                }
            )

        st.dataframe(
            scheduled_rows,
            use_container_width=True,
            hide_index=True,
        )

        if plan.reasoning:
            st.markdown("**Why this plan?**")
            st.info(plan.reasoning)
    else:
        st.info(
            "No tasks were scheduled. Try increasing available time or reducing task durations."
        )