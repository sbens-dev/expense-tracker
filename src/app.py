"""
app.py
======
The main interactive screen for the Personal Expense Tracker.
Built with Streamlit for a clean, mobile-ready user experience.

Automatically connects to Supabase when credentials are provided in
.streamlit/secrets.toml. If not configured, it gracefully defaults to
Local Preview Mode so you can use the app immediately without barriers.
"""

import sys
from pathlib import Path
from datetime import date, timedelta

# Ensure the project root directory is always in Python's search path,
# so Streamlit can find our project files without needing extra commands.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import altair as alt

try:
    from src.calculations import (
        CATEGORIES,
        get_week_start,
        shift_week,
        calculate_weekly_total,
        calculate_category_breakdown,
        calculate_budget_status,
        prepare_chart_data,
        format_currency,
    )
    from src.database import (
        is_cloud_configured,
        save_expense,
        fetch_expenses,
        delete_expense,
    )
except ModuleNotFoundError:
    from calculations import (  # type: ignore
        CATEGORIES,
        get_week_start,
        shift_week,
        calculate_weekly_total,
        calculate_category_breakdown,
        calculate_budget_status,
        prepare_chart_data,
        format_currency,
    )
    from database import (  # type: ignore
        is_cloud_configured,
        save_expense,
        fetch_expenses,
        delete_expense,
    )

# ---------------------------------------------------------
# Page Setup & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💳",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Initialize local session memory for preview mode
if "expenses" not in st.session_state:
    today = date.today()
    sunday = get_week_start(today)
    st.session_state.expenses = [
        {
            "amount": 14.50,
            "category": "Food",
            "description": "Lunch at cafe",
            "date": sunday.strftime("%Y-%m-%d"),
        },
        {
            "amount": 45.00,
            "category": "Gas",
            "description": "Gas station fill-up",
            "date": (sunday + timedelta(days=1)).strftime("%Y-%m-%d"),
        },
    ]

if "week_offset" not in st.session_state:
    st.session_state.week_offset = 0

if "weekly_budget" not in st.session_state:
    st.session_state.weekly_budget = 300.0

# ---------------------------------------------------------
# Cloud Connection & Status Banner
# ---------------------------------------------------------
cloud_active = is_cloud_configured()

if cloud_active:
    st.success(
        "🟢 **Cloud Sync Active:** Purchases are saved online and synced across your phone and computer in real time.",
        icon="✅",
    )
    cloud_expenses = fetch_expenses()
    active_expenses = cloud_expenses if cloud_expenses is not None else []
else:
    st.info(
        "💡 **Local Preview Mode:** Expenses entered below update your numbers immediately in this browser. "
        "To sync between your phone and computer, connect your free Supabase database.",
        icon="ℹ️",
    )
    with st.expander("👉 How to connect phone sync (Supabase)"):
        st.markdown(
            """
            1. Create a free account at [supabase.com](https://supabase.com).
            2. Create a project and run the simple 5-line table setup in the **SQL Editor** (see `README.md`).
            3. Copy your **Project URL** and **anon public key** into `.streamlit/secrets.toml`.
            4. Refresh this page, and you'll see the green **Cloud Sync Active** badge!
            """
        )
    active_expenses = st.session_state.expenses

# ---------------------------------------------------------
# Header & Week Navigation
# ---------------------------------------------------------
st.title("💳 Expense Tracker")

today = date.today()
current_week_start = get_week_start(today)
selected_week_start = shift_week(current_week_start, st.session_state.week_offset)
selected_week_end = selected_week_start + timedelta(days=6)

offset = st.session_state.week_offset
if offset == 0:
    week_label = "This Week"
elif offset == -1:
    week_label = "Last Week"
elif offset < -1:
    week_label = f"{abs(offset)} Weeks Ago"
else:
    week_label = f"{offset} Week{'s' if offset > 1 else ''} Ahead"

# Clean navigation buttons
nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
with nav_col1:
    if st.button("◀ Previous", use_container_width=True, help="Go back one week"):
        st.session_state.week_offset -= 1
        st.rerun()

with nav_col2:
    if st.button("Current Week", use_container_width=True, disabled=(offset == 0), help="Jump back to this week"):
        st.session_state.week_offset = 0
        st.rerun()

with nav_col3:
    if st.button("Next ▶", use_container_width=True, help="Go forward one week"):
        st.session_state.week_offset += 1
        st.rerun()

st.caption(
    f"📅 **{week_label}:** {selected_week_start.strftime('%a, %b %d')} – {selected_week_end.strftime('%a, %b %d, %Y')}"
)

# ---------------------------------------------------------
# Weekly Summary Cards
# ---------------------------------------------------------
weekly_total = calculate_weekly_total(active_expenses, selected_week_start)
category_totals = calculate_category_breakdown(active_expenses, selected_week_start)

# Filter expenses belonging to the selected week
current_week_expenses = [
    item for item in active_expenses
    if selected_week_start <= date.fromisoformat(str(item["date"])[:10]) <= selected_week_end
]

col1, col2 = st.columns(2)
with col1:
    st.metric(
        label=f"Total Spent ({week_label})",
        value=format_currency(weekly_total),
    )
with col2:
    st.metric(
        label=f"Items Logged ({week_label})",
        value=str(len(current_week_expenses)),
    )

# ---------------------------------------------------------
# Weekly Budget Progress Meter
# ---------------------------------------------------------
budget_status = calculate_budget_status(weekly_total, st.session_state.weekly_budget)

if budget_status["is_active"]:
    st.progress(
        value=budget_status["percentage"],
        text=budget_status["status_text"],
    )

# Adjust or customize weekly budget goal
with st.expander("🎯 Set Weekly Budget Goal"):
    new_budget = st.number_input(
        "Weekly Budget ($)",
        min_value=0.0,
        max_value=100000.0,
        value=float(st.session_state.weekly_budget),
        step=25.0,
        format="%.2f",
        help="Set your weekly spending target (set to $0.00 to hide the budget bar)",
    )
    if new_budget != st.session_state.weekly_budget:
        st.session_state.weekly_budget = float(new_budget)
        st.rerun()

st.divider()

# ---------------------------------------------------------
# Add Expense Form
# ---------------------------------------------------------
st.subheader("➕ Add an Expense")

with st.form("add_expense_form", clear_on_submit=True):
    col_amount, col_cat = st.columns([1, 1])
    with col_amount:
        amount_input = st.number_input(
            "Amount ($)",
            min_value=0.01,
            max_value=100000.0,
            step=1.00,
            format="%.2f",
            help="Type in the dollar amount of your purchase",
        )
    with col_cat:
        category_input = st.selectbox(
            "Category",
            options=CATEGORIES,
            index=0,
            help="Choose what kind of purchase this was",
        )

    col_desc, col_date = st.columns([2, 1])
    with col_desc:
        desc_input = st.text_input(
            "Description / Note",
            placeholder="e.g., Grocery run, Coffee, Electric bill",
            help="Short note to remind you what you bought",
        )
    with col_date:
        date_input = st.date_input(
            "Date",
            value=today,
            help="Date of the purchase (defaults to today)",
        )

    submitted = st.form_submit_button("Save Expense", type="primary", use_container_width=True)

    if submitted:
        if amount_input <= 0:
            st.error("Please enter an amount greater than $0.00.")
        else:
            date_str = date_input.strftime("%Y-%m-%d")
            note = desc_input.strip() if desc_input else category_input

            if cloud_active:
                ok, msg = save_expense(
                    amount=float(amount_input),
                    category=category_input,
                    description=note,
                    expense_date=date_str,
                )
                if ok:
                    st.success(f"Added {format_currency(amount_input)} to **{category_input}** (Saved to Cloud)!")
                    st.rerun()
                else:
                    st.error(msg)
            else:
                new_item = {
                    "amount": float(amount_input),
                    "category": category_input,
                    "description": note,
                    "date": date_str,
                }
                st.session_state.expenses.append(new_item)
                st.success(f"Added {format_currency(new_item['amount'])} to **{category_input}** (Saved Locally)!")
                st.rerun()

st.divider()

# ---------------------------------------------------------
# Category Breakdown & Visual Chart
# ---------------------------------------------------------
st.subheader(f"📊 Spending by Category ({week_label})")

chart_items = prepare_chart_data(category_totals)

if chart_items:
    # 1. Category metric cards
    cat_cols = st.columns(min(len(chart_items), 4))
    for i, item in enumerate(chart_items):
        col = cat_cols[i % len(cat_cols)]
        col.metric(label=item["category"], value=format_currency(item["amount"]))

    # 2. Visual Donut / Pie Chart
    df_chart = pd.DataFrame(chart_items)
    df_chart["FormattedAmount"] = df_chart["amount"].apply(lambda x: format_currency(x))

    donut_chart = (
        alt.Chart(df_chart)
        .mark_arc(innerRadius=45, stroke="#fff")
        .encode(
            theta=alt.Theta(field="amount", type="quantitative"),
            color=alt.Color(
                field="category",
                type="nominal",
                legend=alt.Legend(title="Category", orient="bottom"),
            ),
            tooltip=[
                alt.Tooltip("category:N", title="Category"),
                alt.Tooltip("FormattedAmount:N", title="Total Spent"),
            ],
        )
        .properties(height=280)
    )
    st.altair_chart(donut_chart, use_container_width=True)
else:
    st.write(f"No spending recorded in any category for {week_label.lower()}.")

st.divider()

# ---------------------------------------------------------
# Recent Expenses List
# ---------------------------------------------------------
st.subheader(f"📋 Purchases ({week_label})")

if current_week_expenses:
    sorted_expenses = sorted(
        current_week_expenses, key=lambda x: str(x["date"]), reverse=True
    )
    for i, exp in enumerate(sorted_expenses):
        with st.container():
            c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
            desc_text = exp.get("description") or exp.get("category", "Expense")
            date_text = str(exp.get("date", ""))[:10]
            c1.markdown(f"**{desc_text}**<br><small style='color:gray'>{date_text}</small>", unsafe_allow_html=True)
            c2.markdown(f"<span style='background-color:#f0f2f6;padding:3px 8px;border-radius:4px;'>{exp['category']}</span>", unsafe_allow_html=True)
            c3.markdown(f"<div style='text-align:right;font-weight:bold;'>{format_currency(float(exp['amount']))}</div>", unsafe_allow_html=True)
            
            # Delete button (trash can)
            btn_key = f"del_{exp.get('id', i)}_{i}"
            if c4.button("🗑️", key=btn_key, help="Delete this purchase"):
                if cloud_active and "id" in exp:
                    ok, msg = delete_expense(exp["id"])
                    if ok:
                        st.success("Deleted purchase!")
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    if exp in st.session_state.expenses:
                        st.session_state.expenses.remove(exp)
                    elif i < len(st.session_state.expenses):
                        st.session_state.expenses.pop(i)
                    st.success("Deleted purchase!")
                    st.rerun()
            st.write("")
else:
    st.info("No purchases recorded for this week yet. Use the form above to add one!")

# Test tools available only in local preview mode
if not cloud_active:
    with st.expander("🛠️ Test Tools"):
        if st.button("Reset to Empty List"):
            st.session_state.expenses = []
            st.rerun()
