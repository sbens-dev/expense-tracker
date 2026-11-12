from unittest.mock import MagicMock, patch
import pytest
from src.database import (
    is_cloud_configured,
    get_cloud_credentials,
    save_expense,
    fetch_expenses,
)


@patch("streamlit.secrets", {})
def test_is_cloud_configured_false_by_default(monkeypatch):
    """When no credentials are set, cloud is not configured."""
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_KEY", raising=False)
    assert not is_cloud_configured()


@patch("streamlit.secrets", {})
def test_get_cloud_credentials_ignores_placeholders(monkeypatch):
    """Placeholder example text should not be treated as real credentials."""
    monkeypatch.setenv("SUPABASE_URL", "https://your-project-id.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "your-anon-public-key-here")
    url, key = get_cloud_credentials()
    assert url is None
    assert key is None
    assert not is_cloud_configured()


def test_save_expense_rejects_non_positive_amount():
    """Negative or zero dollar amounts must be rejected."""
    success, msg = save_expense(0.0, "Food", "Zero lunch", "2026-11-12")
    assert not success
    assert "greater than $0.00" in msg

    success_neg, _ = save_expense(-5.0, "Gas", "Negative gas", "2026-11-12")
    assert not success_neg


@patch("streamlit.secrets", {})
def test_save_expense_graceful_fallback_when_not_configured(monkeypatch):
    """When cloud is not configured, save_expense returns a clear fallback message."""
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_KEY", raising=False)
    success, msg = save_expense(12.50, "Food", "Coffee", "2026-11-12")
    assert not success
    assert "local preview mode" in msg


@patch("streamlit.secrets", {})
def test_fetch_expenses_returns_none_when_unconfigured(monkeypatch):
    """When cloud is not configured, fetch_expenses returns None to signal local mode."""
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_KEY", raising=False)
    assert fetch_expenses() is None


@patch("src.database.get_client")
def test_save_expense_success_with_mocked_supabase(mock_get_client):
    """Verify data is formatted and inserted when Supabase client is connected."""
    mock_client = MagicMock()
    mock_table = MagicMock()
    mock_insert = MagicMock()
    
    mock_client.table.return_value = mock_table
    mock_table.insert.return_value = mock_insert
    mock_insert.execute.return_value = MagicMock()
    mock_get_client.return_value = mock_client

    success, msg = save_expense(24.50, "Gas", "Fuel fill", "2026-11-12")
    assert success
    assert "successfully" in msg

    mock_client.table.assert_called_with("expenses")
    call_args = mock_table.insert.call_args[0][0]
    assert call_args["amount"] == 24.50
    assert call_args["category"] == "Gas"
    assert call_args["description"] == "Fuel fill"
    assert call_args["date"] == "2026-11-12"


@patch("src.database.get_client")
def test_fetch_expenses_success_with_mocked_supabase(mock_get_client):
    """Verify data is fetched properly when client is connected."""
    mock_client = MagicMock()
    mock_table = MagicMock()
    mock_select = MagicMock()
    mock_order = MagicMock()
    mock_response = MagicMock()

    sample_data = [
        {"id": 1, "amount": 10.0, "category": "Food", "date": "2026-11-12"}
    ]
    mock_response.data = sample_data
    mock_order.execute.return_value = mock_response
    mock_select.order.return_value = mock_order
    mock_table.select.return_value = mock_select
    mock_client.table.return_value = mock_table
    mock_get_client.return_value = mock_client

    result = fetch_expenses()
    assert result == sample_data
    mock_client.table.assert_called_with("expenses")
