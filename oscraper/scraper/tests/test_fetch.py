from unittest.mock import patch
import pytest
from django.core.management import call_command
from django.test import override_settings
from oscraper.scraper.repo import ScraperRepo
from oscraper.scraper.tests.conftest import count_commits


@pytest.fixture
def repo(tmp_path):
    with override_settings(
        SCRAPER_REPO_PATH=tmp_path,
        EVENTS_URL="http://example.com/path/to/events.html",
    ):
        yield ScraperRepo(tmp_path)


@pytest.fixture
def mock_get():
    with patch("requests.get") as mock:
        yield mock


def test_fetch_events_creates_file(repo, mock_get):
    mock_get.return_value.text = "<html>test</html>"
    call_command("fetch_events")
    expected_path = repo.path / "path" / "to" / "events.html"
    assert expected_path.exists()
    assert expected_path.read_text() == "<html>test</html>"


def test_fetch_events_commits_changes(repo, mock_get):
    mock_get.return_value.text = "<html>test</html>"
    call_command("fetch_events")
    assert count_commits(repo.path) == 1


def test_fetch_events_handles_http_error(repo, mock_get):
    mock_get.return_value.raise_for_status.side_effect = Exception("HTTP Error")
    with pytest.raises(Exception, match="HTTP Error"):
        call_command("fetch_events")
