import pytest
from django.core.management import call_command
from oscraper.cms.models import Event, HomePage
from datetime import date


TEST_EVENT = {
    "text": "Test Event (Test Location, Test Club, 2024-05-01)",
    "name": "Test Event",
    "organiser": "Test Club",
    "location": "Test Location",
    "start_date": "2024-05-01",
    "end_date": "2024-05-01",
    "wre_count": 0,
}


@pytest.fixture
def home(db):
    return HomePage.objects.get()


def test_import_events_creates_draft_pages(home, monkeypatch):
    def mock_extract_events(*args, **kwargs):
        return [TEST_EVENT]

    monkeypatch.setattr("oscraper.scraper.extract.extract_events", mock_extract_events)
    call_command("import_events")

    event = Event.objects.get(original_text=TEST_EVENT["text"])
    assert event.organiser == TEST_EVENT["organiser"]
    assert event.location == TEST_EVENT["location"]
    assert event.start_date == date(2024, 5, 1)
    assert event.end_date == date(2024, 5, 1)
    assert not event.live
    assert event.get_parent().specific == home


def test_import_events_skips_duplicates(home, monkeypatch):
    existing_event = Event(
        title="Existing Event",
        organiser="Test Club",
        location="Test Location",
        start_date=date(2024, 5, 1),
        end_date=date(2024, 5, 1),
        original_text=TEST_EVENT["text"],
    )
    home.add_child(instance=existing_event)

    def mock_extract_events(*args, **kwargs):
        return [TEST_EVENT]

    monkeypatch.setattr("oscraper.scraper.extract.extract_events", mock_extract_events)
    call_command("import_events")

    assert Event.objects.count() == 1
    assert Event.objects.get(original_text=TEST_EVENT["text"]) == existing_event
