import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from oscraper.scraper.repo import ScraperRepo
from pathlib import Path
from urllib.parse import urlparse


class Command(BaseCommand):
    help = "Fetches the orienteering.ro events page and saves it to the repo"

    def handle(self, *args, **options):
        response = requests.get(settings.EVENTS_URL)
        response.raise_for_status()
        repo = ScraperRepo(settings.SCRAPER_REPO_PATH)
        path = Path(urlparse(settings.EVENTS_URL).path.lstrip("/"))
        target_path = repo.path / path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(response.text)
        committed = repo.commit_if_changed()
        if committed:
            self.stdout.write(self.style.SUCCESS(f"Saved and committed {path}"))
        else:
            self.stdout.write("No changes to commit")
