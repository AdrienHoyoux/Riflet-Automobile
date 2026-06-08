import json
import os
from datetime import date
from urllib.error import URLError
from urllib.request import Request, urlopen

from .models import CustomerReview, SiteSettings

MAX_FEATURED_REVIEWS = 6


def sync_google_reviews():
    """Synchronise les avis Google Places dans la base (sans les publier automatiquement)."""
    api_key = os.getenv('GOOGLE_PLACES_API_KEY', '').strip()
    place_id = os.getenv('GOOGLE_PLACE_ID', '').strip()

    if not api_key:
        return {
            'ok': False,
            'detail': 'Clé API Google Places non configurée (GOOGLE_PLACES_API_KEY).',
            'synced': 0,
        }

    settings = SiteSettings.load()
    if not place_id:
        place_id = settings.google_place_id

    if not place_id:
        place_id = _find_place_id(api_key, settings)
        if place_id:
            settings.google_place_id = place_id
            settings.save(update_fields=['google_place_id'])

    if not place_id:
        return {
            'ok': False,
            'detail': 'Impossible de trouver le Google Place ID.',
            'synced': 0,
        }

    details = _fetch_place_details(api_key, place_id)
    if not details:
        return {
            'ok': False,
            'detail': 'Impossible de récupérer les avis Google.',
            'synced': 0,
        }

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

        obj, created = CustomerReview.objects.update_or_create(
            external_id=external_id,
            defaults={
                'author_name': author,
                'rating': stars,
                'content': text,
                'source': 'google',
                'review_date': review_date,
            },
        )
        if created:
            obj.is_published = False
            obj.order = 999
            obj.save(update_fields=['is_published', 'order'])
        synced += 1

    return {
        'ok': True,
        'detail': f'{synced} avis synchronisés depuis Google.',
        'synced': synced,
        'rating': float(settings.google_rating),
        'review_count': settings.google_review_count,
    }


def set_featured_reviews(review_ids):
    """Publie les avis sélectionnés sur l'accueil (diaporama)."""
    ids = [int(pk) for pk in review_ids]
    existing = set(
        CustomerReview.objects.filter(pk__in=ids).values_list('pk', flat=True),
    )
    if len(existing) != len(ids):
        raise ValueError('Un ou plusieurs avis sont introuvables.')

    CustomerReview.objects.update(is_published=False)
    for order, pk in enumerate(ids):
        CustomerReview.objects.filter(pk=pk).update(is_published=True, order=order)

    return len(ids)


def _find_place_id(api_key, settings):
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
    except URLError:
        return ''

    places = data.get('places', [])
    return places[0]['id'] if places else ''


def _fetch_place_details(api_key, place_id):
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
    except URLError:
        return None
