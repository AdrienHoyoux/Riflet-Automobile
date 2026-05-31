import json
import os
from datetime import date
from urllib.error import URLError
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand

from garage.models import CustomerReview, SiteSettings


class Command(BaseCommand):
    help = 'Synchronise les avis Google via Google Places API (optionnel)'

    def handle(self, *args, **options):
        api_key = os.getenv('GOOGLE_PLACES_API_KEY', '').strip()
        place_id = os.getenv('GOOGLE_PLACE_ID', '').strip()

        if not api_key:
            self.stdout.write(self.style.WARNING(
                'GOOGLE_PLACES_API_KEY non configurée. Utilisez les avis seedés ou configurez la clé API.'
            ))
            return

        settings = SiteSettings.load()
        if not place_id:
            place_id = settings.google_place_id

        if not place_id:
            place_id = self._find_place_id(api_key, settings)
            if place_id:
                settings.google_place_id = place_id
                settings.save(update_fields=['google_place_id'])

        if not place_id:
            self.stdout.write(self.style.ERROR('Impossible de trouver le Google Place ID.'))
            return

        details = self._fetch_place_details(api_key, place_id)
        if not details:
            self.stdout.write(self.style.ERROR('Impossible de récupérer les détails Google Places.'))
            return

        rating = details.get('rating')
        count = details.get('userRatingCount', 0)
        maps_uri = details.get('googleMapsUri', '')

        if rating is not None:
            settings.google_rating = rating
        settings.google_review_count = count
        if maps_uri:
            settings.google_maps_url = maps_uri
        settings.google_place_id = place_id
        settings.save()

        synced = 0
        for index, review in enumerate(details.get('reviews', [])):
            external_id = review.get('name') or f'{place_id}-{index}'
            text = review.get('text', {}).get('text', '').strip()
            if not text:
                continue

            author = review.get('authorAttribution', {}).get('displayName', 'Client Google')
            stars = int(review.get('rating', 5))
            publish_time = review.get('publishTime', '')
            review_date = None
            if publish_time:
                review_date = date.fromisoformat(publish_time[:10])

            CustomerReview.objects.update_or_create(
                external_id=external_id,
                defaults={
                    'author_name': author,
                    'rating': stars,
                    'content': text,
                    'source': 'google',
                    'review_date': review_date,
                    'is_published': True,
                    'order': index,
                },
            )
            synced += 1

        self.stdout.write(self.style.SUCCESS(
            f'{synced} avis Google synchronisés. Note : {settings.google_rating}/5 ({settings.google_review_count} avis).'
        ))

    def _find_place_id(self, api_key, settings):
        query = f'{settings.company_name} {settings.address} {settings.postal_code} {settings.city}'
        url = 'https://places.googleapis.com/v1/places:searchText'
        payload = json.dumps({'textQuery': query, 'languageCode': 'fr'}).encode()
        request = Request(
            url,
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'X-Goog-Api-Key': api_key,
                'X-Goog-FieldMask': 'places.id,places.displayName',
            },
            method='POST',
        )
        try:
            with urlopen(request, timeout=20) as response:
                data = json.loads(response.read().decode())
        except URLError as exc:
            self.stdout.write(self.style.ERROR(f'Erreur recherche Place ID : {exc}'))
            return ''

        places = data.get('places', [])
        return places[0]['id'] if places else ''

    def _fetch_place_details(self, api_key, place_id):
        url = f'https://places.googleapis.com/v1/places/{place_id}'
        request = Request(
            url,
            headers={
                'X-Goog-Api-Key': api_key,
                'X-Goog-FieldMask': 'rating,userRatingCount,googleMapsUri,reviews',
            },
        )
        try:
            with urlopen(request, timeout=20) as response:
                return json.loads(response.read().decode())
        except URLError as exc:
            self.stdout.write(self.style.ERROR(f'Erreur API Google Places : {exc}'))
            return None
