from datetime import date
import pytest
from src.calculations import (
    CATEGORIES,
    get_week_start,
    shift_week,
    calculate_weekly_total,
    calculate_category_breakdown,
    calculate_budget_status,
    format_currency,
)


def test_categories_list():
    """Verify that the standard categories and Other exist."""
    assert "Food" in CATEGORIES
    assert "Gas" in CATEGORIES
    assert "Groceries" in CATEGORIES
    assert "Bills" in CATEGORIES
    assert "Entertainment" in CATEGORIES
    assert "Shopping" in CATEGORIES
    assert "Other" in CATEGORIES


def test_get_week_start_when_date_is_sunday():
    """If the date is already Sunday, week start should be the same day."""
    # 2026-11-08 was a Sunday
    test_sunday = date(2026, 11, 8)
    assert get_week_start(test_sunday) == date(2026, 11, 8)


def test_get_week_start_when_date_is_midweek():
    """If the date is Wednesday, week start should be the preceding Sunday."""
    # 2026-11-11 is a Wednesday
    test_wednesday = date(2026, 11, 11)
    assert get_week_start(test_wednesday) == date(2026, 11, 8)


def test_get_week_start_when_date_is_saturday():
    """If the date is Saturday, week start should be the Sunday 6 days earlier."""
    # 2026-11-14 is a Saturday
    test_saturday = date(2026, 11, 14)
    assert get_week_start(test_saturday) == date(2026, 11, 8)


def test_calculate_weekly_total():
    """Verify only expenses within Sunday to Saturday of the target week are included."""
    week_start = date(2026, 11, 8)
    expenses = [
        # Inside current week (Sunday Nov 8 - Saturday Nov 14)
        {"amount": 15.50, "category": "Food", "date": "2026-11-08"},
        {"amount": 42.00, "category": "Gas", "date": "2026-11-10"},
        {"amount": 28.25, "category": "Food", "date": "2026-11-14"},
        # Outside current week (previous week)
        {"amount": 50.00, "category": "Bills", "date": "2026-11-07"},
        # Outside current week (next week)
        {"amount": 19.99, "category": "Shopping", "date": "2026-11-15"},
    ]

    total = calculate_weekly_total(expenses, week_start)
    # Expected: 15.50 + 42.00 + 28.25 = 85.75
    assert total == 85.75


def test_calculate_weekly_total_empty():
    """Empty expenses should return 0.0 total."""
    assert calculate_weekly_total([], date(2026, 11, 8)) == 0.0


def test_calculate_category_breakdown():
    """Verify spending is grouped correctly by category for the current week."""
    week_start = date(2026, 11, 8)
    expenses = [
        {"amount": 10.00, "category": "Food", "date": "2026-11-09"},
        {"amount": 15.50, "category": "Food", "date": "2026-11-11"},
        {"amount": 45.00, "category": "Gas", "date": "2026-11-10"},
        {"amount": 80.00, "category": "Bills", "date": "2026-11-12"},
        # Outside current week: should be ignored
        {"amount": 99.00, "category": "Food", "date": "2026-11-01"},
    ]

    breakdown = calculate_category_breakdown(expenses, week_start)

    assert breakdown["Food"] == 25.50
    assert breakdown["Gas"] == 45.00
    assert breakdown["Bills"] == 80.00
    assert breakdown["Groceries"] == 0.0
    assert breakdown["Other"] == 0.0


def test_format_currency():
    """Verify dollar amounts are formatted with $ and two decimal places."""
    assert format_currency(0) == "$0.00"
    assert format_currency(12.5) == "$12.50"
    assert format_currency(1234.567) == "$1,234.57"


def test_shift_week():
    """Verify moving backward and forward by weeks from a Sunday."""
    base_sunday = date(2026, 11, 8)
    # 1 week back
    assert shift_week(base_sunday, -1) == date(2026, 11, 1)
    # 2 weeks back
    assert shift_week(base_sunday, -2) == date(2026, 10, 25)
    # 1 week forward
    assert shift_week(base_sunday, 1) == date(2026, 11, 15)
    # 0 offset
    assert shift_week(base_sunday, 0) == date(2026, 11, 8)


def test_calculate_budget_status_under_budget():
    """Verify budget math when user is under their weekly target."""
    status = calculate_budget_status(total_spent=150.0, budget=300.0)
    assert status["is_active"] is True
    assert status["percentage"] == 0.5
    assert status["remaining"] == 150.0
    assert status["is_over"] is False
    assert "$150.00 left" in status["status_text"]


def test_calculate_budget_status_over_budget():
    """Verify budget math when spending exceeds target."""
    status = calculate_budget_status(total_spent=350.0, budget=300.0)
    assert status["is_active"] is True
    assert status["percentage"] == 1.0
    assert status["remaining"] == -50.0
    assert status["is_over"] is True
    assert "exceeded" in status["status_text"]


def test_calculate_budget_status_disabled_when_zero():
    """When budget is 0.0 or negative, budget tracking is inactive."""
    status = calculate_budget_status(total_spent=100.0, budget=0.0)
    assert status["is_active"] is False


