from django.core.management.base import BaseCommand

from garage.google_reviews import sync_google_reviews


class Command(BaseCommand):
    help = 'Synchronise les avis Google via Google Places API (optionnel)'

    def handle(self, *args, **options):
        result = sync_google_reviews()
        if result['ok']:
            self.stdout.write(self.style.SUCCESS(
                f"{result['detail']} Note : {result.get('rating')}/5 "
                f"({result.get('review_count')} avis sur Google)."
            ))
        else:
            self.stdout.write(self.style.WARNING(result['detail']))
