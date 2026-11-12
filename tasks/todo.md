# Tasks: Personal Expense Tracker

## Phase 1: Foundation & Math Brain

### Task 1: Project Setup and Dependencies
- **Description:** Prepare the project folders and create `requirements.txt` with the necessary tools (`streamlit`, `supabase`, `pytest`).
- **Acceptance criteria:**
  - [x] `requirements.txt` is created with required packages.
  - [x] Folder structure (`src/`, `tests/`, `.streamlit/`) is created.
- **Verification:**
  - [x] Dependencies install cleanly via `pip install -r requirements.txt`.
- **Dependencies:** None
- **Files likely touched:**
  - `requirements.txt`
- **Estimated scope:** XS (1 file)

---

### Task 2: Weekly Date & Spending Calculations (with Automated Tests)
- **Description:** Build the calculation functions that handle the math (adding up the weekly total and grouping spending by category), making sure Sunday is always the start of the week. Write automated tests to prove the math is accurate.
- **Acceptance criteria:**
  - [x] `get_week_start(date)` correctly finds Sunday for any given date.
  - [x] `calculate_weekly_total(expenses, week_start)` returns the exact dollar sum of expenses in the current week.
  - [x] `calculate_category_breakdown(expenses, week_start)` returns spending grouped by category (`Food`, `Gas`, etc.).
  - [x] Unit tests in `tests/test_calculations.py` verify calculations with multiple sample expenses.
- **Verification:**
  - [x] `pytest tests/test_calculations.py` passes with 100% green tests.
- **Dependencies:** Task 1
- **Files likely touched:**
  - `src/calculations.py`
  - `tests/test_calculations.py`
- **Estimated scope:** S (2 files)

---

## Checkpoint: Foundation
- [x] All automated tests pass (`pytest`).
- [x] Weekly date calculation correctly identifies Sunday as week start.

---

## Phase 2: Interactive Screen (UI)

### Task 3: Streamlit User Interface
- **Description:** Create the visual webpage in `src/app.py`. Includes the expense entry form (dollar amount, note, category dropdown) and the weekly dashboard (total money spent this week, category breakdown, and list of purchases). Includes local preview mode so you can test it immediately in your browser.
- **Acceptance criteria:**
  - [x] Header shows clean app title and current week range (e.g., "Week of Sun, Nov 8").
  - [x] Form has inputs for Amount ($), Note/Description, and Category dropdown (`Food`, `Gas`, `Groceries`, `Bills`, `Entertainment`, `Shopping`, `Other`).
  - [x] Weekly total is prominently displayed as a large number card.
  - [x] Category breakdown displays clearly below the total.
  - [x] Works nicely in both mobile and desktop viewports.
- **Verification:**
  - [x] Launch `streamlit run src/app.py` and manually verify entering an item updates the screen.
- **Dependencies:** Task 2
- **Files likely touched:**
  - `src/app.py`
- **Estimated scope:** M (1-2 files)

---

## Checkpoint: Visual UI
- [x] App launches and displays cleanly.
- [x] Adding an expense locally updates the weekly grand total and category breakdown.

---

## Phase 3: Cloud Sync & Polish

### Task 4: Cloud Database Integration (Supabase)
- **Description:** Create helper functions in `src/database.py` to save an expense and fetch expenses from Supabase. Provide `.streamlit/secrets.toml.example` with clear instructions on how to insert private database keys.
- **Acceptance criteria:**
  - [x] `save_expense(...)` inserts an expense record with amount, note, category, and date.
  - [x] `fetch_expenses()` retrieves all recorded expenses.
  - [x] App gracefully falls back to local storage if Supabase credentials are not provided yet.
- **Verification:**
  - [x] Unit/mock tests verify saving and loading operations.
- **Dependencies:** Task 3
- **Files likely touched:**
  - `src/database.py`
  - `.streamlit/secrets.toml.example`
- **Estimated scope:** S (2 files)

---

### Task 5: End-to-End Integration & Beginner Guide
- **Description:** Connect the user interface to Supabase so entries are saved directly to the cloud and synced in real time. Write a beginner-friendly `README.md` guide explaining how to open the app on your computer and phone.
- **Acceptance criteria:**
  - [x] Entering an expense on the screen saves to Supabase and instantly updates the weekly totals.
  - [x] `README.md` explains in everyday language how to run the app and how to connect it to your phone.
- **Verification:**
  - [x] All `pytest` tests pass.
  - [x] Manual test: Add an item and verify it persists across app reloads.
- **Dependencies:** Task 4
- **Files likely touched:**
  - `src/app.py`
  - `README.md`
- **Estimated scope:** S (2 files)

---

## Checkpoint: Complete
- [x] Entering an expense updates the weekly total and category breakdown in real time.
- [x] Sync across devices is enabled via Supabase.
- [x] Full test suite passes.
- [x] Ready for final review.
