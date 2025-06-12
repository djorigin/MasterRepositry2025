from django.core.management.base import BaseCommand
from systemcore.models import Country
import csv
import os

class Command(BaseCommand):
    help = 'Import countries from a CSV file into the Country model.'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join('systemcore', 'fixtures', 'countries.csv')
        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f"CSV file not found: {csv_path}"))
            return

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                obj, created = Country.objects.get_or_create(
                    name=row['name'],
                    iso_code=row['iso_code']
                )
                if created:
                    count += 1
            self.stdout.write(self.style.SUCCESS(f"Imported {count} countries."))