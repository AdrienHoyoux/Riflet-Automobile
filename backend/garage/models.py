from django.db import models
from django.utils.text import slugify


class TranslatedModelMixin(models.Model):
    """Champs multilingues FR / DE / NL pour le contenu éditable."""

    title_fr = models.CharField('Titre (FR)', max_length=255)
    title_de = models.CharField('Titre (DE)', max_length=255, blank=True)
    title_nl = models.CharField('Titre (NL)', max_length=255, blank=True)

    description_fr = models.TextField('Description (FR)', blank=True)
    description_de = models.TextField('Description (DE)', blank=True)
    description_nl = models.TextField('Description (NL)', blank=True)

    class Meta:
        abstract = True

    def get_title(self, lang='fr'):
        return getattr(self, f'title_{lang}', None) or self.title_fr

    def get_description(self, lang='fr'):
        return getattr(self, f'description_{lang}', None) or self.description_fr


class SiteSettings(models.Model):
    """Informations générales du garage (singleton)."""

    company_name = models.CharField('Nom', max_length=255, default='Riflet Automobile')
    tagline_fr = models.CharField('Slogan (FR)', max_length=255, blank=True)
    tagline_de = models.CharField('Slogan (DE)', max_length=255, blank=True)
    tagline_nl = models.CharField('Slogan (NL)', max_length=255, blank=True)

    about_fr = models.TextField('À propos (FR)', blank=True)
    about_de = models.TextField('À propos (DE)', blank=True)
    about_nl = models.TextField('À propos (NL)', blank=True)

    about_title_fr = models.CharField('Titre page À propos (FR)', max_length=255, blank=True)
    about_title_de = models.CharField('Titre page À propos (DE)', max_length=255, blank=True)
    about_title_nl = models.CharField('Titre page À propos (NL)', max_length=255, blank=True)
    about_subtitle_fr = models.CharField('Sous-titre page À propos (FR)', max_length=500, blank=True)
    about_subtitle_de = models.CharField('Sous-titre page À propos (DE)', max_length=500, blank=True)
    about_subtitle_nl = models.CharField('Sous-titre page À propos (NL)', max_length=500, blank=True)
    about_image_url = models.CharField('URL image page À propos', max_length=500, blank=True)

    home_services_title_fr = models.CharField('Titre section services accueil (FR)', max_length=255, blank=True)
    home_services_title_de = models.CharField('Titre section services accueil (DE)', max_length=255, blank=True)
    home_services_title_nl = models.CharField('Titre section services accueil (NL)', max_length=255, blank=True)
    home_services_subtitle_fr = models.CharField('Sous-titre section services accueil (FR)', max_length=500, blank=True)
    home_services_subtitle_de = models.CharField('Sous-titre section services accueil (DE)', max_length=500, blank=True)
    home_services_subtitle_nl = models.CharField('Sous-titre section services accueil (NL)', max_length=500, blank=True)

    home_why_title_fr = models.CharField('Titre « Pourquoi nous choisir » (FR)', max_length=255, blank=True)
    home_why_title_de = models.CharField('Titre « Pourquoi nous choisir » (DE)', max_length=255, blank=True)
    home_why_title_nl = models.CharField('Titre « Pourquoi nous choisir » (NL)', max_length=255, blank=True)

    services_title_fr = models.CharField('Titre page Services (FR)', max_length=255, blank=True)
    services_title_de = models.CharField('Titre page Services (DE)', max_length=255, blank=True)
    services_title_nl = models.CharField('Titre page Services (NL)', max_length=255, blank=True)
    services_subtitle_fr = models.CharField('Sous-titre page Services (FR)', max_length=500, blank=True)
    services_subtitle_de = models.CharField('Sous-titre page Services (DE)', max_length=500, blank=True)
    services_subtitle_nl = models.CharField('Sous-titre page Services (NL)', max_length=500, blank=True)

    address = models.CharField('Adresse', max_length=255)
    city = models.CharField('Ville', max_length=100)
    postal_code = models.CharField('Code postal', max_length=20)
    country = models.CharField('Pays', max_length=100, default='Belgique')

    phone = models.CharField('Téléphone', max_length=30)
    email = models.EmailField('E-mail')
    facebook_url = models.URLField('Facebook', blank=True)

    monday_hours = models.CharField('Lundi', max_length=100, default='08:30 - 12:00 | 13:00 - 17:30')
    tuesday_hours = models.CharField('Mardi', max_length=100, default='08:30 - 12:00 | 13:00 - 17:30')
    wednesday_hours = models.CharField('Mercredi', max_length=100, default='08:30 - 12:00 | 13:00 - 17:30')
    thursday_hours = models.CharField('Jeudi', max_length=100, default='08:30 - 12:00 | 13:00 - 17:30')
    friday_hours = models.CharField('Vendredi', max_length=100, default='08:30 - 12:00 | 13:00 - 17:30')
    saturday_hours = models.CharField('Samedi', max_length=100, default='Fermé')
    sunday_hours = models.CharField('Dimanche', max_length=100, default='Fermé')

    latitude = models.DecimalField('Latitude', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('Longitude', max_digits=9, decimal_places=6, null=True, blank=True)

    logo_url = models.CharField('URL logo', max_length=500, blank=True)
    hero_image_url = models.CharField('URL image hero', max_length=500, blank=True)

    google_rating = models.DecimalField('Note Google', max_digits=2, decimal_places=1, default=5.0)
    google_review_count = models.PositiveIntegerField('Nombre d\'avis Google', default=0)
    google_maps_url = models.URLField('Lien Google Maps', blank=True)
    google_place_id = models.CharField('Google Place ID', max_length=255, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Paramètres du site'
        verbose_name_plural = 'Paramètres du site'

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Service(TranslatedModelMixin):
    icon = models.CharField('Icône (emoji ou nom)', max_length=50, default='🔧')
    image = models.ImageField('Image', upload_to='services/', blank=True, null=True)
    image_url = models.CharField('URL image externe', max_length=500, blank=True)
    order = models.PositiveIntegerField('Ordre', default=0)
    is_active = models.BooleanField('Actif', default=True)

    class Meta:
        ordering = ['order', 'title_fr']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.title_fr


class NewsArticle(TranslatedModelMixin):
    slug = models.SlugField('Slug', max_length=255, unique=True, blank=True)
    content_fr = models.TextField('Contenu (FR)')
    content_de = models.TextField('Contenu (DE)', blank=True)
    content_nl = models.TextField('Contenu (NL)', blank=True)

    image = models.ImageField('Image', upload_to='news/', blank=True, null=True)
    image_url = models.CharField('URL image externe', max_length=500, blank=True)
    is_published = models.BooleanField('Publié', default=True)
    published_at = models.DateTimeField('Date de publication', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Actualité'
        verbose_name_plural = 'Actualités'

    def __str__(self):
        return self.title_fr

    def get_content(self, lang='fr'):
        return getattr(self, f'content_{lang}', None) or self.content_fr

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_fr) or 'actualite'
            slug = base
            counter = 1
            while NewsArticle.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    name = models.CharField('Nom', max_length=150)
    email = models.EmailField('E-mail')
    phone = models.CharField('Téléphone', max_length=30, blank=True)
    subject = models.CharField('Sujet', max_length=255)
    message = models.TextField('Message')
    vehicle = models.ForeignKey(
        'UsedVehicle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contact_messages',
        verbose_name='Véhicule concerné',
    )
    is_read = models.BooleanField('Lu', default=False)
    created_at = models.DateTimeField('Reçu le', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Message de contact'
        verbose_name_plural = 'Messages de contact'

    def __str__(self):
        return f'{self.name} — {self.subject}'


class UsedVehicle(TranslatedModelMixin):
    FUEL_CHOICES = [
        ('petrol', 'Essence'),
        ('diesel', 'Diesel'),
        ('electric', 'Électrique'),
        ('hybrid', 'Hybride'),
        ('lpg', 'LPG'),
    ]
    TRANSMISSION_CHOICES = [
        ('manual', 'Manuelle'),
        ('automatic', 'Automatique'),
    ]

    slug = models.SlugField('Slug', max_length=255, unique=True, blank=True)
    brand = models.CharField('Marque', max_length=80)
    model_name = models.CharField('Modèle', max_length=80)
    year = models.PositiveIntegerField('Année')
    mileage = models.PositiveIntegerField('Kilométrage (km)')
    fuel_type = models.CharField('Carburant', max_length=20, choices=FUEL_CHOICES, default='diesel')
    transmission = models.CharField('Boîte', max_length=20, choices=TRANSMISSION_CHOICES, default='manual')
    price = models.DecimalField('Prix (€)', max_digits=12, decimal_places=2)
    image = models.ImageField('Image', upload_to='vehicles/', blank=True, null=True)
    image_url = models.CharField('URL image externe', max_length=500, blank=True)
    is_active = models.BooleanField('Visible sur le site', default=True)
    is_sold = models.BooleanField('Vendu', default=False)
    order = models.PositiveIntegerField('Ordre', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Véhicule d\'occasion'
        verbose_name_plural = 'Véhicules d\'occasion'

    def __str__(self):
        return f'{self.brand} {self.model_name} ({self.year})'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f'{self.brand}-{self.model_name}-{self.year}') or 'vehicule'
            slug = base
            counter = 1
            while UsedVehicle.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(
        UsedVehicle,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        verbose_name='Véhicule',
    )
    image = models.ImageField('Image', upload_to='vehicles/gallery/', blank=True, null=True)
    image_url = models.CharField('URL image externe', max_length=500, blank=True)
    order = models.PositiveIntegerField('Ordre', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Photo véhicule'
        verbose_name_plural = 'Photos véhicule'

    def __str__(self):
        return f'Photo {self.order + 1} — {self.vehicle}'


class WhyChooseItem(models.Model):
    text_fr = models.CharField('Texte (FR)', max_length=500)
    text_de = models.CharField('Texte (DE)', max_length=500, blank=True)
    text_nl = models.CharField('Texte (NL)', max_length=500, blank=True)
    order = models.PositiveIntegerField('Ordre', default=0)
    is_active = models.BooleanField('Actif', default=True)

    class Meta:
        ordering = ['order', 'pk']
        verbose_name = 'Argument « Pourquoi nous choisir »'
        verbose_name_plural = 'Arguments « Pourquoi nous choisir »'

    def __str__(self):
        return self.text_fr[:60]


class CustomerReview(models.Model):
    SOURCE_CHOICES = [
        ('google', 'Google'),
        ('facebook', 'Facebook'),
        ('manual', 'Manuel'),
        ('website', 'Site web'),
    ]

    author_name = models.CharField('Auteur', max_length=120)
    rating = models.PositiveSmallIntegerField('Note', default=5)
    content = models.TextField('Commentaire')
    source = models.CharField('Source', max_length=20, choices=SOURCE_CHOICES, default='google')
    external_id = models.CharField('ID externe', max_length=255, blank=True, unique=True, null=True)
    review_date = models.DateField('Date de l\'avis', null=True, blank=True)
    is_published = models.BooleanField('Publié', default=True)
    order = models.PositiveIntegerField('Ordre', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-review_date', '-created_at']
        verbose_name = 'Avis client'
        verbose_name_plural = 'Avis clients'

    def __str__(self):
        return f'{self.author_name} ({self.rating}/5)'


class AdminMfaDevice(models.Model):
    """Authentification TOTP (Google Authenticator, etc.) pour l'admin du site."""

    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='mfa_device',
        verbose_name='Utilisateur',
    )
    secret = models.CharField('Secret TOTP', max_length=64)
    is_enabled = models.BooleanField('Activée', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField('Confirmée le', null=True, blank=True)

    class Meta:
        verbose_name = 'MFA administrateur'
        verbose_name_plural = 'MFA administrateurs'

    def __str__(self):
        status = 'activée' if self.is_enabled else 'en attente'
        return f'MFA {self.user.username} ({status})'
