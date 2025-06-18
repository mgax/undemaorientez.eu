from django.core.management.base import BaseCommand
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.translation import activate
from django.conf import settings
import json
from pathlib import Path
from datetime import datetime


class Command(BaseCommand):
    help = "Generate an Atom feed from extracted events"

    def handle(self, *args, **options):
        # Set Romanian locale
        activate("ro")

        # Read the events from the test data file
        data_file = (
            Path(__file__).parent.parent.parent
            / "tests"
            / "data"
            / "extract_result.json"
        )
        with open(data_file) as f:
            events = json.load(f)

        # Convert date strings to date objects for template rendering
        for event in events:
            event["start_date"] = datetime.strptime(
                event["start_date"], "%Y-%m-%d"
            ).date()
            event["end_date"] = datetime.strptime(event["end_date"], "%Y-%m-%d").date()

        # Generate the Atom feed using the template
        context = {
            "now": timezone.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "events": events,
            "settings": settings,
        }

        # Render the template and write to stdout
        self.stdout.write(render_to_string("scraper/feed.xml", context))
