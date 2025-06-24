from django.core.management.base import BaseCommand
from oscraper.cms.models import Event, HomePage
from datetime import datetime


class Command(BaseCommand):
    help = "Creates draft Event pages from scraped events"

    def handle(self, *args, **options):
        home = HomePage.objects.get()
        events = self.get_events()

        for event_data in events:
            if Event.objects.filter(original_text=event_data["text"]).exists():
                continue

            event = Event(
                title=event_data["name"],
                organiser=event_data["organiser"],
                location=event_data["location"] or "",
                start_date=datetime.strptime(
                    event_data["start_date"], "%Y-%m-%d"
                ).date(),
                end_date=datetime.strptime(event_data["end_date"], "%Y-%m-%d").date(),
                original_text=event_data["text"],
                live=False,
            )
            home.add_child(instance=event)
            event.save_revision()

            self.stdout.write(self.style.SUCCESS(f"Imported event: {event!r}"))

    def get_events(self):
        from oscraper.scraper.extract import extract_events
        from django.conf import settings
        from pathlib import Path
        from urllib.parse import urlparse

        path = Path(urlparse(settings.EVENTS_URL).path.lstrip("/"))
        file_path = Path(settings.SCRAPER_REPO_PATH) / path
        content = file_path.read_text(encoding="iso-8859-1")
        return extract_events(content)
