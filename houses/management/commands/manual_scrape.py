from django.core.management.base import BaseCommand
from houses.utils import scrape_funda


class Command(BaseCommand):
    def handle(self, *args, **options):
        scrape_funda()
