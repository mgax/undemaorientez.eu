import logging
import sys
from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
from urllib.parse import urlparse
import json
from oscraper.scraper.extract import extract_events


# Add DEEP_DEBUG level (5)
logging.addLevelName(5, "DEEP_DEBUG")


class Command(BaseCommand):
    help = "Extracts and prints event paragraphs with dates from the scraped HTML file, dropping links."

    def handle(self, *args, **options):
        # Create a debug handler that prints to stderr
        debug_handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter("\033[90m%(levelname)s: %(message)s\033[0m")
        debug_handler.setFormatter(formatter)

        # Get the extract logger and add the handler
        extract_logger = logging.getLogger("oscraper.scraper.extract")
        extract_logger.addHandler(debug_handler)

        # Set log level based on verbosity
        if options["verbosity"] >= 3:
            extract_logger.setLevel(5)  # DEEP_DEBUG
        elif options["verbosity"] >= 2:
            extract_logger.setLevel(logging.DEBUG)

        self.stdout.write("Extracting events...")
        path = Path(urlparse(settings.EVENTS_URL).path.lstrip("/"))
        file_path = Path(settings.SCRAPER_REPO_PATH) / path
        content = file_path.read_text(encoding="utf-8")
        events = extract_events(content)
        self.stdout.write(json.dumps(events, indent=2))
