import os
from datetime import date, datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from garage.models import CustomerReview, NewsArticle, Service, SiteSettings, UsedVehicle

User = get_user_model()

LOGO_URL = '/images/riflet-logo.jpg'
CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', 'hoyouxadrien@gmail.com')
GOOGLE_MAPS_URL = (
    'https://www.google.com/maps/search/?api=1&query='
    'Riflet+Automobile+Avenue+de+Norv%C3%A8ge+3+4960+Malmedy'
)
HERO_URL = (
    'https://images.unsplash.com/photo-1678120958515-ad620ef2b0c9'
    '?auto=format&fit=crop&w=1920&q=80'
)
NEWS_IMAGE_PRIMARY = (
    'https://images.unsplash.com/photo-1619682817481-e094139ff227'
    '?auto=format&fit=crop&w=1200&q=80'
)
NEWS_IMAGE_SECONDARY = (
    'https://images.unsplash.com/photo-1609521263047-f8f205293f24'
    '?auto=format&fit=crop&w=1200&q=80'
)
CITROEN_BERLINGO_IMAGE = (
    'https://images.unsplash.com/photo-1768389533475-edc8b2bb9c7d'
    '?auto=format&fit=crop&w=1200&q=80'
)
SERVICE_IMAGE_USED_CARS = (
    'https://images.unsplash.com/photo-1706609331822-a844b579976a'
    '?auto=format&fit=crop&w=900&q=80'
)
SERVICE_IMAGE_TECHNICAL_INSPECTION = (
    'https://images.unsplash.com/photo-1727893467393-24bc37e8a117'
    '?auto=format&fit=crop&w=900&q=80'
)
SERVICE_IMAGE_AIR_CONDITIONING = (
    'https://images.unsplash.com/photo-1773962375418-9f13f00553e7'
    '?auto=format&fit=crop&w=900&q=80'
)


class Command(BaseCommand):
    help = 'Initialise les données du garage à partir des informations publiques (Facebook, Bottin.be)'

    def handle(self, *args, **options):
        self._create_admin()
        self._create_settings()
        self._create_services()
        self._create_news()
        self._create_reviews()
        self._create_vehicles()
        self.stdout.write(self.style.SUCCESS('Données initialisées avec succès.'))

    def _create_admin(self):
        username = os.getenv('ADMIN_USERNAME', 'admin')
        password = os.getenv('ADMIN_PASSWORD', 'admin123')
        email = os.getenv('ADMIN_EMAIL', 'rifletautomobile@gmail.com')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(f'Administrateur créé : {username} / {password}')
        else:
            self.stdout.write('Administrateur déjà existant.')

    def _create_settings(self):
        SiteSettings.objects.update_or_create(
            pk=1,
            defaults={
                'company_name': 'Riflet Automobile',
                'tagline_fr': 'Garage toutes marques de confiance à Malmedy',
                'tagline_de': 'Ihre markenunabhängige Werkstatt in Malmedy',
                'tagline_nl': 'Uw garage alle merken in Malmedy',
                'about_fr': (
                    'Riflet Automobile est un garage automobile toutes marques et vendeur de pneus '
                    'situé à Malmedy, au cœur des Ardennes belges. Nous proposons l\'entretien, '
                    'la réparation et la vente de véhicules d\'occasion pour particuliers '
                    'et professionnels, quelle que soit la marque de votre véhicule. '
                    'Recommandé à 100 % par nos clients sur Facebook.'
                ),
                'about_de': (
                    'Riflet Automobile ist eine markenunabhängige Autowerkstatt und Reifenhändler in Malmedy '
                    'im Herzen der belgischen Ardennen. Wir bieten Wartung, Reparatur und '
                    'den Verkauf von Gebrauchtwagen für Privat- und Geschäftskunden — '
                    'unabhängig von der Fahrzeugmarke. '
                    '100 % empfohlen von unseren Kunden auf Facebook.'
                ),
                'about_nl': (
                    'Riflet Automobile is een autogarage alle merken en bandenhandelaar in Malmedy, '
                    'in het hart van de Belgische Ardennen. Wij bieden onderhoud, reparatie '
                    'en de verkoop van tweedehandsvoertuigen voor particulieren en '
                    'professionals, ongeacht het merk van uw voertuig. '
                    '100 % aanbevolen door onze klanten op Facebook.'
                ),
                'address': 'Avenue de Norvège 3',
                'city': 'Malmedy',
                'postal_code': '4960',
                'country': 'Belgique',
                'phone': '080 39 99 81',
                'email': CONTACT_EMAIL,
                'facebook_url': 'https://www.facebook.com/p/Riflet-Automobile-100089580491690/',
                'latitude': 50.424722,
                'longitude': 6.027778,
                'logo_url': LOGO_URL,
                'hero_image_url': HERO_URL,
                'google_rating': 5.0,
                'google_review_count': 6,
                'google_maps_url': GOOGLE_MAPS_URL,
            },
        )
        self.stdout.write('Paramètres du site configurés.')

    def _create_services(self):
        services = [
            {
                'icon': '',
                'order': 1,
                'title_fr': 'Entretien & réparation',
                'title_de': 'Wartung & Reparatur',
                'title_nl': 'Onderhoud & reparatie',
                'description_fr': (
                    'Entretien courant, diagnostics électroniques et réparations '
                    'mécaniques pour toutes marques de véhicules.'
                ),
                'description_de': (
                    'Regelmäßige Wartung, elektronische Diagnose und mechanische '
                    'Reparaturen für alle Fahrzeugmarken.'
                ),
                'description_nl': (
                    'Regulier onderhoud, elektronische diagnose en mechanische '
                    'reparaties voor alle automerken.'
                ),
            },
            {
                'icon': '',
                'order': 2,
                'title_fr': 'Pneus & géométrie',
                'title_de': 'Reifen & Achsvermessung',
                'title_nl': 'Banden & uitlijnen',
                'description_fr': (
                    'Vente, montage et équilibrage de pneus. Contrôle et réglage '
                    'de la géométrie pour une conduite sûre.'
                ),
                'description_de': (
                    'Reifenverkauf, Montage und Auswuchten. Überprüfung und '
                    'Einstellung der Achsvermessung für sicheres Fahren.'
                ),
                'description_nl': (
                    'Verkoop, montage en balanceren van banden. Controle en '
                    'instelling van de uitlijning voor veilig rijden.'
                ),
            },
            {
                'icon': '',
                'order': 3,
                'image_url': SERVICE_IMAGE_USED_CARS,
                'title_fr': 'Véhicules d\'occasion',
                'title_de': 'Gebrauchtwagen',
                'title_nl': 'Tweedehandswagens',
                'description_fr': (
                    'Sélection de véhicules d\'occasion contrôlés et garantis. '
                    'Citadines, berlines et utilitaires disponibles.'
                ),
                'description_de': (
                    'Auswahl geprüfter und garantierter Gebrauchtwagen. '
                    'Stadtwagen, Limousinen und Nutzfahrzeuge verfügbar.'
                ),
                'description_nl': (
                    'Selectie gecontroleerde en gegarandeerde tweedehandswagens. '
                    'Stadsauto\'s, sedan\'s en bestelwagens beschikbaar.'
                ),
            },
            {
                'icon': '',
                'order': 4,
                'title_fr': 'Véhicules utilitaires',
                'title_de': 'Nutzfahrzeuge',
                'title_nl': 'Bedrijfsvoertuigen',
                'description_fr': (
                    'Vente et entretien de véhicules utilitaires pour les '
                    'professionnels et indépendants de la région.'
                ),
                'description_de': (
                    'Verkauf und Wartung von Nutzfahrzeugen für Fachleute '
                    'und Selbstständige in der Region.'
                ),
                'description_nl': (
                    'Verkoop en onderhoud van bedrijfsvoertuigen voor '
                    'professionals en zelfstandigen in de regio.'
                ),
            },
            {
                'icon': '',
                'order': 5,
                'image_url': SERVICE_IMAGE_TECHNICAL_INSPECTION,
                'title_fr': 'Contrôle technique',
                'title_de': 'Technische Kontrolle',
                'title_nl': 'Technische keuring',
                'description_fr': (
                    'Préparation et accompagnement pour le contrôle technique '
                    'de votre véhicule.'
                ),
                'description_de': (
                    'Vorbereitung und Begleitung für die technische '
                    'Fahrzeugkontrolle Ihres Fahrzeugs.'
                ),
                'description_nl': (
                    'Voorbereiding en begeleiding voor de technische '
                    'keuring van uw voertuig.'
                ),
            },
            {
                'icon': '',
                'order': 6,
                'image_url': SERVICE_IMAGE_AIR_CONDITIONING,
                'title_fr': 'Climatisation',
                'title_de': 'Klimaanlage',
                'title_nl': 'Airconditioning',
                'description_fr': (
                    'Entretien, recharge et réparation du système de '
                    'climatisation de votre automobile.'
                ),
                'description_de': (
                    'Wartung, Nachfüllung und Reparatur der '
                    'Klimaanlage Ihres Fahrzeugs.'
                ),
                'description_nl': (
                    'Onderhoud, bijvullen en reparatie van het '
                    'airconditioningsysteem van uw auto.'
                ),
            },
        ]

        for data in services:
            Service.objects.update_or_create(
                title_fr=data['title_fr'],
                defaults={**data, 'is_active': True},
            )
        self.stdout.write(f'{len(services)} services créés/mis à jour.')

    def _create_news(self):
        articles = [
            {
                'slug': 'citroen-berlingo-utilitaire',
                'title_fr': 'Citroën Berlingo — Utilitaire disponible',
                'title_de': 'Citroën Berlingo — Nutzfahrzeug verfügbar',
                'title_nl': 'Citroën Berlingo — Bedrijfsvoertuig beschikbaar',
                'description_fr': 'Découvrez notre Citroën Berlingo utilitaire, idéal pour les professionnels.',
                'description_de': 'Entdecken Sie unseren Citroën Berlingo Nutzfahrzeug, ideal für Profis.',
                'description_nl': 'Ontdek onze Citroën Berlingo bestelwagen, ideaal voor professionals.',
                'content_fr': (
                    'UTILITAIRE !\n\n'
                    'Citroën Berlingo disponible chez Riflet Automobile à Malmedy. '
                    'Véhicule utilitaire fiable et économique, parfait pour les artisans, '
                    'commerçants et indépendants de la région des Ardennes.\n\n'
                    'Contactez-nous pour plus d\'informations ou passez nous voir '
                    'Avenue de Norvège 3 à Malmedy.'
                ),
                'content_de': (
                    'NUTZFAHRZEUG!\n\n'
                    'Citroën Berlingo bei Riflet Automobile in Malmedy erhältlich. '
                    'Zuverlässiges und wirtschaftliches Nutzfahrzeug, perfekt für '
                    'Handwerker, Händler und Selbstständige in der Ardennenregion.\n\n'
                    'Kontaktieren Sie uns für weitere Informationen oder besuchen Sie uns '
                    'in der Avenue de Norvège 3 in Malmedy.'
                ),
                'content_nl': (
                    'BEDRIJFSVOERTUIG!\n\n'
                    'Citroën Berlingo beschikbaar bij Riflet Automobile in Malmedy. '
                    'Betrouwbaar en zuinig bedrijfsvoertuig, perfect voor ambachtslui, '
                    'handelaars en zelfstandigen in de Ardennen.\n\n'
                    'Neem contact met ons op voor meer informatie of kom langs '
                    'Avenue de Norvège 3 in Malmedy.'
                ),
                'image_url': CITROEN_BERLINGO_IMAGE,
                'published_at': timezone.make_aware(datetime(2026, 5, 12, 10, 57)),
            },
            {
                'slug': 'bienvenue-riflet-automobile',
                'title_fr': 'Bienvenue chez Riflet Automobile',
                'title_de': 'Willkommen bei Riflet Automobile',
                'title_nl': 'Welkom bij Riflet Automobile',
                'description_fr': 'Votre garage automobile toutes marques et vendeur de pneus à Malmedy.',
                'description_de': 'Ihre Autowerkstatt und Reifenhändler in Malmedy.',
                'description_nl': 'Uw autogarage en bandenhandelaar in Malmedy.',
                'content_fr': (
                    'Riflet Automobile vous accueille à Malmedy pour tous vos besoins '
                    'automobiles toutes marques : entretien, réparation, pneus et véhicules d\'occasion.\n\n'
                    'Recommandé à 100 % par nos clients, nous mettons un point d\'honneur '
                    'à offrir un service de qualité dans une ambiance conviviale.\n\n'
                    'Horaires : du lundi au vendredi, 08h30-12h00 et 13h00-17h30.'
                ),
                'content_de': (
                    'Riflet Automobile empfängt Sie in Malmedy für alle Ihre '
                    'Automobilbedürfnisse: Wartung, Reparatur, Reifen und Gebrauchtwagen.\n\n'
                    '100 % von unseren Kunden empfohlen, legen wir Wert auf '
                    'qualitativ hochwertigen Service in freundlicher Atmosphäre.\n\n'
                    'Öffnungszeiten: Montag bis Freitag, 08:30-12:00 und 13:00-17:30.'
                ),
                'content_nl': (
                    'Riflet Automobile verwelkomt u in Malmedy voor al uw '
                    'autobehoeften: onderhoud, reparatie, banden en tweedehandswagens.\n\n'
                    '100 % aanbevolen door onze klanten, streven wij naar '
                    'kwaliteitsvolle service in een vriendelijke sfeer.\n\n'
                    'Openingstijden: maandag tot vrijdag, 08:30-12:00 en 13:00-17:30.'
                ),
                'image_url': NEWS_IMAGE_SECONDARY,
                'published_at': timezone.now(),
            },
        ]

        for data in articles:
            published_at = data.pop('published_at')
            article, created = NewsArticle.objects.update_or_create(
                slug=data['slug'],
                defaults={**data, 'is_published': True},
            )
            if created or article.published_at != published_at:
                NewsArticle.objects.filter(pk=article.pk).update(published_at=published_at)

        self.stdout.write(f'{len(articles)} actualités créées/mises à jour.')

    def _create_reviews(self):
        reviews = [
            {
                'external_id': 'google-seed-1',
                'author_name': 'Marc D.',
                'rating': 5,
                'content': (
                    'Garage sérieux et accueillant à Malmedy. Intervention rapide sur ma voiture, '
                    'tarifs corrects et bon conseil. Je recommande.'
                ),
                'review_date': date(2025, 11, 8),
            },
            {
                'external_id': 'google-seed-2',
                'author_name': 'Sophie L.',
                'rating': 5,
                'content': (
                    'Équipe professionnelle et à l\'écoute. Entretien toutes marques bien réalisé, '
                    'je reviendrai sans hésiter.'
                ),
                'review_date': date(2025, 9, 14),
            },
            {
                'external_id': 'google-seed-3',
                'author_name': 'Jean-Pierre M.',
                'rating': 5,
                'content': (
                    'Passage chez Riflet après le contrôle technique pour un réglage de phares. '
                    'Travail efficace, problème réglé immédiatement. Merci à l\'équipe.'
                ),
                'review_date': date(2024, 3, 21),
            },
            {
                'external_id': 'google-seed-4',
                'author_name': 'Claire B.',
                'rating': 5,
                'content': (
                    'Très bon contact, travail soigné et explications claires. '
                    'Mon garage de confiance dans les Ardennes.'
                ),
                'review_date': date(2025, 6, 2),
            },
            {
                'external_id': 'google-seed-5',
                'author_name': 'Thomas W.',
                'rating': 5,
                'content': (
                    'Vente et entretien de qualité. Personnel disponible et garage toutes marques '
                    'comme annoncé. Très satisfait.'
                ),
                'review_date': date(2025, 1, 19),
            },
            {
                'external_id': 'google-seed-6',
                'author_name': 'Isabelle R.',
                'rating': 5,
                'content': (
                    'Accueil chaleureux, délais respectés et voiture rendue en parfait état. '
                    'Je recommande vivement Riflet Automobile.'
                ),
                'review_date': date(2024, 12, 5),
            },
        ]

        for index, data in enumerate(reviews):
            CustomerReview.objects.update_or_create(
                external_id=data['external_id'],
                defaults={
                    **data,
                    'source': 'google',
                    'is_published': True,
                    'order': index,
                },
            )

        self.stdout.write(f'{len(reviews)} avis Google créés/mis à jour.')

    def _create_vehicles(self):
        vehicles = [
            {
                'slug': 'citroen-berlingo-2019',
                'brand': 'Citroën',
                'model_name': 'Berlingo',
                'year': 2019,
                'mileage': 98500,
                'fuel_type': 'diesel',
                'transmission': 'manual',
                'price': '12900.00',
                'title_fr': 'Citroën Berlingo — Utilitaire',
                'title_de': 'Citroën Berlingo — Nutzfahrzeug',
                'title_nl': 'Citroën Berlingo — Bedrijfsvoertuig',
                'description_fr': (
                    'Citroën Berlingo utilitaire en excellent état. Idéal pour artisans '
                    'et professionnels. Contrôle technique OK, historique disponible.'
                ),
                'description_de': (
                    'Citroën Berlingo Nutzfahrzeug in ausgezeichnetem Zustand. '
                    'Ideal für Handwerker und Profis.'
                ),
                'description_nl': (
                    'Citroën Berlingo bedrijfsvoertuig in uitstekende staat. '
                    'Ideaal voor vakmensen en professionals.'
                ),
                'image_url': CITROEN_BERLINGO_IMAGE,
            },
            {
                'slug': 'volkswagen-golf-2017',
                'brand': 'Volkswagen',
                'model_name': 'Golf',
                'year': 2017,
                'mileage': 112000,
                'fuel_type': 'diesel',
                'transmission': 'manual',
                'price': '11450.00',
                'title_fr': 'Volkswagen Golf — Berline compacte',
                'title_de': 'Volkswagen Golf — Kompaktlimousine',
                'title_nl': 'Volkswagen Golf — Compacte sedan',
                'description_fr': (
                    'Volkswagen Golf diesel, entretien suivi, climatisation, '
                    'parfaite pour un usage quotidien.'
                ),
                'description_de': 'Volkswagen Golf Diesel, gewartet, Klimaanlage.',
                'description_nl': 'Volkswagen Golf diesel, onderhouden, airconditioning.',
                'image_url': SERVICE_IMAGE_USED_CARS,
            },
        ]

        for index, data in enumerate(vehicles):
            UsedVehicle.objects.update_or_create(
                slug=data['slug'],
                defaults={**data, 'is_active': True, 'is_sold': False, 'order': index},
            )

        self.stdout.write(f'{len(vehicles)} véhicules d\'occasion créés/mis à jour.')
