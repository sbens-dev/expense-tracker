# Implementation Plan: Personal Expense Tracker

## Overview
A beginner-friendly web application built with Python, Streamlit, and Supabase. The app allows users to log daily expenses (amount, note, category) and view their current week's spending (starting Sunday) both as a grand total and broken down by category. It syncs seamlessly across phone and desktop browsers.

## Architecture Decisions
- **Python + Streamlit:** Keeps the entire UI in simple, clean Python without needing to learn HTML, CSS, or JavaScript. Automatically formats well on mobile devices.
- **Supabase Cloud Database:** Serves as the centralized online storage so data is immediately shared between phone and computer.
- **Sunday-to-Saturday Week:** Week start is set to Sunday at 00:00:00 based on user requirements.
- **Offline / Local Fallback:** The app will support a local session mode if Supabase keys are not yet configured, allowing immediate testing of the UI without setup blockers.

---

## Task List

### Phase 1: Foundation & Math Brain
- [x] **Task 1: Project Setup and Dependencies**
  - Create project structure and `requirements.txt`.
- [x] **Task 2: Weekly Date & Spending Calculations (with Automated Tests)**
  - Implement Sunday-based week filtering, total calculation, and category breakdown in `src/calculations.py`.
  - Add unit tests in `tests/test_calculations.py`.

### Checkpoint: Foundation
- [x] All automated tests pass (`pytest`).
- [x] Weekly date calculation correctly identifies Sunday as week start.

### Phase 2: Interactive Screen (UI)
- [x] **Task 3: Streamlit User Interface**
  - Build the input form (amount, note, category dropdown) and summary dashboard (weekly total card, category breakdown, recent expenses list) in `src/app.py`.
  - Support instant preview with local data.

### Checkpoint: Visual UI
- [x] App launches with `streamlit run src/app.py`.
- [x] Input form and summary cards work cleanly on both desktop and mobile viewports.

### Phase 3: Cloud Sync & Polish
- [x] **Task 4: Cloud Database Integration (Supabase)**
  - Create `src/database.py` to save and load expenses from Supabase.
  - Provide `.streamlit/secrets.toml.example` with clear beginner-friendly instructions.
- [x] **Task 5: End-to-End Integration & Beginner Guide**
  - Connect `src/app.py` to `src/database.py` for live syncing.
  - Create `README.md` with simple step-by-step instructions on running the app and viewing it on a smartphone.

### Checkpoint: Complete
- [x] Entering an expense on one device saves to Supabase and updates the weekly total and category breakdown.
- [x] Full test suite passes.
- [x] Final user review.

---

### Phase 4: Feature Enhancements
- [x] **Task 6: Feature 1 — Delete Expense Button**
  - Add `delete_expense(expense_id)` to `src/database.py` (Supabase deletion and local session removal).
  - Add delete action button next to each purchase in `src/app.py`.
  - Add automated tests in `tests/test_database.py` and `tests/test_app.py`.
- [ ] **Task 7: Feature 2 — Browse Past Weeks Navigation**
  - Add week offset selector (`◀ Last Week`, `This Week`, `Next Week ▶`) in `src/app.py`.
  - Filter spending and category totals according to selected week.
- [ ] **Task 8: Feature 3 — Weekly Budget Goal & Progress Bar**
  - Add weekly budget setting and visual progress meter indicating remaining balance.
- [ ] **Task 9: Feature 4 — Visual Spending Pie Chart**
  - Add a category spending donut/pie chart to visualize proportions.

---

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Cloud database setup is confusing for a beginner | Medium | The app will work locally out of the box with sample data, and we will provide exact step-by-step setup instructions with no technical jargon. |
| Timezone differences between phone and server affecting week start | Low | Use standard date stamps and calculate week start relative to local device date. |
| User enters invalid amounts (e.g., negative numbers or letters) | Low | Streamlit `number_input` restricts input to positive numbers automatically. |

## Open Questions
- None. (All clarified: week starts on Sunday; currency is USD `$`).
