import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from swxsoc.util import util


@pytest.fixture
def mock_requests():
    """Fixture to mock requests methods."""
    with (
        patch("requests.get") as mock_get,
        patch("requests.post") as mock_post,
        patch("requests.delete") as mock_delete,
    ):
        yield mock_get, mock_post, mock_delete


def test_query_annotations(mock_requests):
    mock_get, _, _ = mock_requests

    # Define mock response
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "id": 1,
            "time": 1663351800000,
            "text": "Solar flare",
            "tags": ["meddea", "test"],
        }
    ]
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call function
    start_time = datetime(2024, 9, 16, 13, 30, 0)
    end_time = datetime(2024, 9, 16, 13, 35, 0)
    result = util.query_annotations(
        start_time=start_time,
        end_time=end_time,
        dashboard_name="Test Dashboard",
        panel_name="Test Panel",
        tags=["test"],
    )

    # Assertions
    assert result == [
        {
            "id": 1,
            "time": 1663351800000,
            "text": "Solar flare",
            "tags": ["meddea", "test"],
        }
    ]
    mock_get.assert_called_once()


def test_create_annotation(mock_requests):
    _, mock_post, _ = mock_requests

    # Define mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": 123}
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    # Call function
    start_time = datetime(2024, 9, 16, 13, 30, 0)
    end_time = datetime(2024, 9, 16, 13, 35, 0)
    result = util.create_annotation(
        start_time=start_time,
        end_time=end_time,
        text="Observed solar flare",
        tags=["meddea", "test"],
        dashboard_name="Test Dashboard",
        panel_name="Test Panel",
    )

    # Assertions
    assert result == {"id": 123}
    mock_post.assert_called_once()


def test_remove_annotation_by_id(mock_requests):
    _, _, mock_delete = mock_requests

    # Define mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_delete.return_value = mock_response

    # Call function
    result = util.remove_annotation_by_id(123)

    # Assertions
    assert result is True
    mock_delete.assert_called_once()
