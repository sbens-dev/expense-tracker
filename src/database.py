"""
database.py
===========
Handles saving and loading purchases from our private online filing cabinet (Supabase).

If Supabase keys are not set up yet, the app gracefully lets you know and uses
local temporary memory so the screen never crashes.
"""

import os
from typing import Optional, Tuple, Union
import streamlit as st
from supabase import create_client, Client
from src.calculations import CATEGORIES


def get_cloud_credentials() -> Tuple[Optional[str], Optional[str]]:
    """
    Safely retrieves the Supabase URL and Key without exposing them.
    Checks .streamlit/secrets.toml first, then system environment variables.
    """
    url = None
    key = None

    # Check Streamlit secrets
    try:
        if "supabase" in st.secrets:
            url = st.secrets["supabase"].get("url")
            key = st.secrets["supabase"].get("key")
    except Exception:
        # st.secrets might be unavailable during certain test environments
        pass

    # Fallback to environment variables
    if not url:
        url = os.environ.get("SUPABASE_URL")
    if not key:
        key = os.environ.get("SUPABASE_KEY")

    # Guard: Check if the user left the placeholder values unchanged
    if url and "your-project-id" in url:
        url = None
    if key and "your-anon-public-key" in key:
        key = None

    return url, key


def is_cloud_configured() -> bool:
    """Returns True if valid Supabase connection details are present."""
    url, key = get_cloud_credentials()
    return bool(url and key)


def get_client() -> Optional[Client]:
    """Creates a secure client connection to Supabase if configured."""
    url, key = get_cloud_credentials()
    if not url or not key:
        return None
    try:
        return create_client(url, key)
    except Exception as e:
        # Log to console, but never expose raw credentials to the user interface
        st.warning(f"Could not connect to online database: {e}")
        return None


def save_expense(
    amount: float,
    category: str,
    description: str,
    expense_date: str,
) -> Tuple[bool, str]:
    """
    Saves an expense to Supabase.
    
    Security & Validation:
    - Amount must be a positive number.
    - Category must match an approved category.
    - Description is trimmed and length-capped.
    - Date must be present.
    """
    # Boundary validation
    if amount <= 0:
        return False, "Amount must be greater than $0.00."

    safe_category = category if category in CATEGORIES else "Other"
    safe_description = (description or safe_category).strip()[:200]
    safe_date = str(expense_date)[:10]

    client = get_client()
    if not client:
        return False, "Online database is not configured. Saved in local preview mode instead."

    try:
        data = {
            "amount": float(amount),
            "category": safe_category,
            "description": safe_description,
            "date": safe_date,
        }
        client.table("expenses").insert(data).execute()
        return True, "Expense saved to cloud successfully!"
    except Exception as e:
        return False, f"Failed to save online: {e}"


def fetch_expenses() -> Optional[list[dict]]:
    """
    Retrieves all expenses from the online Supabase database.
    Returns None if cloud is not configured, so the app knows to use local session memory.
    """
    client = get_client()
    if not client:
        return None

    try:
        response = client.table("expenses").select("*").order("date", desc=True).execute()
        return response.data if response and hasattr(response, "data") else []
    except Exception as e:
        st.error(f"Error loading expenses from cloud: {e}")
        return []


def delete_expense(expense_id: Union[int, str, None]) -> Tuple[bool, str]:
    """
    Deletes an expense from Supabase by its unique ID.
    
    Security & Validation:
    - ID must be provided and valid (positive number).
    """
    if expense_id is None:
        return False, "Invalid expense ID."

    try:
        numeric_id = int(expense_id)
        if numeric_id <= 0:
            return False, "Invalid expense ID."
    except (ValueError, TypeError):
        return False, "Invalid expense ID."

    client = get_client()
    if not client:
        return False, "Online database is not configured."

    try:
        client.table("expenses").delete().eq("id", numeric_id).execute()
        return True, "Expense deleted successfully!"
    except Exception as e:
        return False, f"Failed to delete online: {e}"
