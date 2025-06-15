import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Fetches the orienteering.ro events page"

    def handle(self, *args, **options):
        response = requests.get("http://www.orienteering.ro/welcomeROM.html")
        response.raise_for_status()
        self.stdout.write(response.text)
