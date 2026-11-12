# Spec: Personal Expense Tracker

## Objective
A simple, beginner-friendly web application where you can quickly record daily purchases, assign a category (such as Food or Gas), and see your total spending and category breakdown for the current week. 

The app works cleanly in web browsers on both smartphones and computers, staying automatically synchronized between devices.

### Target User
Personal use for an individual wanting a fast, hassle-free way to track daily spending on the go and at home.

### Core User Stories
1. **Quick Entry:** As a user, I can enter a dollar amount, a short note/description (e.g., "Lunch with Sarah"), and choose a category from a dropdown menu.
2. **Category Selection:** As a user, I can pick from a preset list of common categories (`Food`, `Gas`, `Groceries`, `Bills`, `Entertainment`, `Shopping`, `Other`).
3. **Weekly Overview:** As a user, when I open the app on either my phone or computer, I immediately see:
   - The grand total of money spent this week.
   - A breakdown showing how much money was spent in each category this week.
4. **Recent History:** As a user, I can view a list of this week's expenses so I can verify what I've entered.
5. **Real-time Sync:** As a user, when I enter an expense on my phone, it appears on my computer without extra steps.

---

## Tech Stack
- **Language:** **Python 3.11+** (chosen for its clean, human-readable syntax that looks like everyday English).
- **User Interface (Screen Builder):** **Streamlit** (automatically builds clean, mobile-friendly buttons, forms, and summary cards without needing web design skills).
- **Online Database (Cloud Filing Cabinet):** **Supabase** (free, secure online database that keeps phone and computer in sync).
- **Configuration & Secrets:** `.streamlit/secrets.toml` (keeps your private database keys safe and separate from code).

---

## Commands
When you are ready to run and test the app:

- **Install Dependencies:** `pip install streamlit supabase pytest`
- **Run the App Locally:** `streamlit run src/app.py`
- **Run Automated Tests:** `pytest`

---

## Project Structure
```text
expense-tracker/
├── .streamlit/
│   └── secrets.toml          # Private connection keys for your online Supabase database
├── src/
│   ├── app.py                # Main web application (screens, input forms, and weekly summary)
│   ├── database.py           # Helper functions to save and load expenses from Supabase
│   └── calculations.py       # Helper functions to calculate weekly totals and category sums
├── tests/
│   └── test_calculations.py    # Automated checks to verify the math
├── requirements.txt          # List of tools needed to run the app
├── SPEC.md                   # This project blueprint
└── README.md                 # Simple instructions on how to set up and run the app
```

---

## Code Style & Conventions
- **Simplicity First:** All code should be clean, short, and well-commented with plain-English notes.
- **Readable Naming:** Functions and variables must have obvious, plain-English names (e.g., `calculate_weekly_total()`, `get_expenses_for_week()`, `category`).
- **Friendly Validation:** Amounts must be positive numbers; missing descriptions or categories are handled with helpful messages.

Example snippet:
```python
# A simple example showing how readable the code will be:
def calculate_weekly_total(expenses: list[dict]) -> float:
    """Add up the total cost of all expenses in the current week."""
    return sum(item["amount"] for item in expenses)
```

---

## Testing Strategy
- **Unit Testing:** Automated checks using `pytest` to test the math calculations (verifying that adding up $15.50 for Food and $30.00 for Gas correctly results in $45.50 total and $15.50 in Food).
- **Manual Verification:** 
  1. Open the app in both a phone-sized window and a desktop browser.
  2. Add an expense ("$12.50", "Coffee", "Food").
  3. Verify the grand total updates immediately.
  4. Verify the "Food" category total updates immediately.
  5. Check on the other device to confirm it shows up automatically.

---

## Boundaries
- **Always do:**
  - Keep code readable and easy for a beginner to follow.
  - Test calculation logic thoroughly before marking anything done.
  - Provide plain-English explanations for any instructions.
- **Ask first:**
  - Adding any new library or tool outside of Streamlit and Supabase.
  - Changing the structure of how data is stored.
- **Never do:**
  - Never put secret database passwords or API keys directly into public code (always use `.streamlit/secrets.toml`).
  - Never add complex features (like bank logins, receipt scanning, or complex monthly budgeting) that were not requested.

---

## Success Criteria
1. The app displays cleanly on both mobile browsers and desktop browsers.
2. A user can enter a dollar amount, a description, and select a category from a preset list (`Food`, `Gas`, `Groceries`, `Bills`, `Entertainment`, `Shopping`, `Other`).
3. An expense submitted on one device is saved to Supabase and immediately visible on any other connected device.
4. The app calculates and prominently displays:
   - The grand total spent in the current week (Sunday through Saturday).
   - A breakdown showing total spent per category in USD ($).
5. All calculations are verified by automated tests.

---

## Resolved Decisions
1. **Week start day:** The spending week starts on **Sunday** (Sunday 00:00 through Saturday 23:59).
2. **Currency symbol:** **$** (US Dollar) is used for all amounts.
