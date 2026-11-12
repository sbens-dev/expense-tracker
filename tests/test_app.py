import sys
from pathlib import Path
from unittest.mock import patch
from streamlit.testing.v1 import AppTest


def test_app_runs_cleanly():
    """Verify app runs cleanly without exceptions in local preview mode."""
    app_path = Path(__file__).resolve().parent.parent / "src" / "app.py"
    at = AppTest.from_file(str(app_path))
    at.run()
    assert len(at.exception) == 0


def test_app_runs_when_root_not_in_sys_path(monkeypatch):
    """
    Guard against regression: ModuleNotFoundError: No module named 'src'.
    When sys.path does not include the project root, the app must resolve calculations.
    """
    project_root = str(Path(__file__).resolve().parent.parent)
    src_dir = str(Path(__file__).resolve().parent.parent / "src")

    # Remove project_root and empty string from sys.path
    filtered_path = [src_dir] + [
        p for p in sys.path if p != project_root and p != ""
    ]
    monkeypatch.setattr(sys, "path", filtered_path)

    # Remove cached src modules
    sys.modules.pop("src", None)
    sys.modules.pop("src.calculations", None)

    app_path = Path(__file__).resolve().parent.parent / "src" / "app.py"
    at = AppTest.from_file(str(app_path))
    at.run()
    assert len(at.exception) == 0


@patch("src.database.is_cloud_configured", return_value=True)
@patch("src.database.fetch_expenses")
def test_app_runs_in_cloud_mode(mock_fetch, mock_is_configured):
    """Verify app runs cleanly when connected to cloud."""
    mock_fetch.return_value = [
        {"amount": 25.0, "category": "Food", "description": "Dinner", "date": "2026-11-10"}
    ]
    app_path = Path(__file__).resolve().parent.parent / "src" / "app.py"
    at = AppTest.from_file(str(app_path))
    at.run()
    assert len(at.exception) == 0


def test_app_renders_delete_buttons_in_local_mode():
    """Verify delete button appears for each purchase and can be clicked."""
    app_path = Path(__file__).resolve().parent.parent / "src" / "app.py"
    at = AppTest.from_file(str(app_path))
    at.run()
    # At least one delete button should be rendered for initial sample expenses
    delete_buttons = [b for b in at.button if "🗑️" in b.label]
    assert len(delete_buttons) > 0
    # Click the first delete button and verify rerun has no exception
    delete_buttons[0].click().run()
    assert len(at.exception) == 0


@patch("src.database.is_cloud_configured", return_value=True)
@patch("src.database.fetch_expenses")
@patch("src.database.delete_expense", return_value=(True, "Deleted"))
def test_app_delete_in_cloud_mode(mock_del, mock_fetch, mock_is_configured):
    """Verify clicking delete in cloud mode invokes delete_expense."""
    mock_fetch.return_value = [
        {"id": 99, "amount": 25.0, "category": "Food", "description": "Dinner", "date": "2026-11-10"}
    ]
    app_path = Path(__file__).resolve().parent.parent / "src" / "app.py"
    at = AppTest.from_file(str(app_path))
    at.run()
    delete_buttons = [b for b in at.button if "del_99" in str(b.key)]
    assert len(delete_buttons) == 1
    delete_buttons[0].click().run()
    assert len(at.exception) == 0
    mock_del.assert_called_with(99)
