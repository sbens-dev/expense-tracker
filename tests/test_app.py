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
