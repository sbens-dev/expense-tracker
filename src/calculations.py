"""
calculations.py
================
This file is the "calculator brain" for our expense tracker app.
It handles all math operations:
1. Finding the start of the current week (Sunday).
2. Adding up all money spent this week.
3. Grouping spending by category (e.g., Food, Gas).
4. Formatting numbers nicely as dollars (e.g., $15.50).
"""

from datetime import date, datetime, timedelta
from typing import Union

# The standard list of categories every purchase can belong to
CATEGORIES = [
    "Food",
    "Gas",
    "Groceries",
    "Bills",
    "Entertainment",
    "Shopping",
    "Other",
]


def _parse_date(value: Union[date, datetime, str]) -> date:
    """Helper to convert any date or text (like '2026-11-08') into a standard date object."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        # Expecting 'YYYY-MM-DD' format (e.g. from an input or database)
        return datetime.strptime(value[:10], "%Y-%m-%d").date()
    raise ValueError(f"Unsupported date format: {value}")


def get_week_start(target_date: Union[date, datetime, str]) -> date:
    """
    Finds the Sunday that begins the week for any given date.
    
    Examples:
    - Sunday, Nov 8 -> returns Sunday, Nov 8 (same day)
    - Wednesday, Nov 11 -> returns Sunday, Nov 8
    - Saturday, Nov 14 -> returns Sunday, Nov 8
    """
    current = _parse_date(target_date)
    # In Python: Monday is 0, Tuesday is 1, ..., Saturday is 5, Sunday is 6.
    # Formula gives how many days have passed since the most recent Sunday:
    days_since_sunday = (current.weekday() + 1) % 7
    return current - timedelta(days=days_since_sunday)


def calculate_weekly_total(expenses: list[dict], week_start: date) -> float:
    """
    Calculates the grand total spent during the target week (Sunday through Saturday).
    Ignores any expenses that happened before or after this 7-day period.
    """
    week_end = week_start + timedelta(days=6)
    total = 0.0

    for item in expenses:
        expense_date = _parse_date(item["date"])
        # Check if the purchase occurred between Sunday and Saturday
        if week_start <= expense_date <= week_end:
            total += float(item.get("amount", 0.0))

    return round(total, 2)


def calculate_category_breakdown(expenses: list[dict], week_start: date) -> dict[str, float]:
    """
    Groups this week's expenses by category.
    Returns a dictionary showing how much was spent in each category.
    Example: {"Food": 25.50, "Gas": 45.00, "Groceries": 0.00, ...}
    """
    week_end = week_start + timedelta(days=6)
    
    # Start every category at $0.00
    breakdown = {category: 0.0 for category in CATEGORIES}

    for item in expenses:
        expense_date = _parse_date(item["date"])
        if week_start <= expense_date <= week_end:
            category = item.get("category", "Other")
            amount = float(item.get("amount", 0.0))
            
            # If the category is recognized, add to it; otherwise group under 'Other'
            if category in breakdown:
                breakdown[category] += amount
            else:
                breakdown["Other"] += amount

    # Round all values to 2 decimal places for clean currency display
    return {cat: round(amt, 2) for cat, amt in breakdown.items()}


def format_currency(amount: float) -> str:
    """
    Formats any number into a nice dollar string.
    Example: 12.5 -> '$12.50'
             1234.567 -> '$1,234.57'
    """
    return f"${amount:,.2f}"
