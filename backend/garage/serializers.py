import re

from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import AdminMfaDevice, ContactMessage, CustomerReview, NewsArticle, Service, SiteSettings, UsedVehicle, VehicleImage, WhyChooseItem


class FlexibleURLField(serializers.CharField):
    """Accepte une URL absolue, un chemin relatif (/images/...) ou /media/...."""

    def __init__(self, **kwargs):
        kwargs.setdefault('allow_blank', True)
        kwargs.setdefault('max_length', 500)
        super().__init__(**kwargs)


from .media_urls import public_media_url


PHONE_REGEX = re.compile(
    r'^(?:'
    r'\+32[\s./-]?(?:\d[\s./-]?){8,12}|'
    r'0032[\s./-]?(?:\d[\s./-]?){8,12}|'
    r'\+33[\s./-]?(?:\d[\s./-]?){8,11}|'
    r'0033[\s./-]?(?:\d[\s./-]?){8,11}|'
    r'\+352[\s./-]?(?:\d[\s./-]?){6,11}|'
    r'00352[\s./-]?(?:\d[\s./-]?){6,11}|'
    r'\+31[\s./-]?(?:\d[\s./-]?){8,11}|'
    r'0031[\s./-]?(?:\d[\s./-]?){8,11}|'
    r'0[\s./-]?(?:\d[\s./-]?){8,11}|'
    r'[26]\d[\s./-]?(?:\d[\s./-]?){6,9}'
    r')$'
)


def resolve_model_image(request, obj):
    if obj.image:
        return public_media_url(obj.image.url)
    return public_media_url(obj.image_url)


def resolve_vehicle_image(image_obj):
    if image_obj.image:
        return public_media_url(image_obj.image.url)
    return public_media_url(image_obj.image_url)


def vehicle_gallery_urls(vehicle):
    gallery = list(vehicle.gallery_images.all())
    if gallery:
        return [url for url in (resolve_vehicle_image(item) for item in gallery) if url]
    primary = resolve_model_image(None, vehicle)
    return [primary] if primary else []


def vehicle_gallery_storage_urls(vehicle):
    gallery = list(vehicle.gallery_images.all())
    if gallery:
        urls = []
        for item in gallery:
            if item.image_url:
                urls.append(item.image_url)
            elif item.image:
                urls.append(item.image.url)
        return urls
    if vehicle.image_url:
        return [vehicle.image_url]
    if vehicle.image:
        return [vehicle.image.url]
    return []


def sync_vehicle_gallery(vehicle, urls):
    cleaned = [url.strip() for url in urls if url and str(url).strip()]
    vehicle.gallery_images.all().delete()
    for order, url in enumerate(cleaned):
        VehicleImage.objects.create(vehicle=vehicle, image_url=url, order=order)

    first_url = cleaned[0] if cleaned else ''
    vehicle.image_url = first_url
    if first_url:
        vehicle.image = None
    vehicle.save(update_fields=['image_url', 'image'])


SITE_CONTENT_FIELDS = [
    'about_title_fr', 'about_title_de', 'about_title_nl',
    'about_subtitle_fr', 'about_subtitle_de', 'about_subtitle_nl',
    'about_image_url',
    'home_services_title_fr', 'home_services_title_de', 'home_services_title_nl',
    'home_services_subtitle_fr', 'home_services_subtitle_de', 'home_services_subtitle_nl',
    'home_why_title_fr', 'home_why_title_de', 'home_why_title_nl',
    'services_title_fr', 'services_title_de', 'services_title_nl',
    'services_subtitle_fr', 'services_subtitle_de', 'services_subtitle_nl',
]


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            'company_name',
            'tagline_fr', 'tagline_de', 'tagline_nl',
            'about_fr', 'about_de', 'about_nl',
            *SITE_CONTENT_FIELDS,
            'address', 'city', 'postal_code', 'country',
            'phone', 'email', 'facebook_url',
            'monday_hours', 'tuesday_hours', 'wednesday_hours',
            'thursday_hours', 'friday_hours', 'saturday_hours', 'sunday_hours',
            'latitude', 'longitude',
            'logo_url', 'hero_image_url',
            'google_rating', 'google_review_count', 'google_maps_url',
        ]


class ServiceSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'title_fr', 'title_de', 'title_nl',
            'description_fr', 'description_de', 'description_nl',
            'icon', 'image', 'order',
        ]

    def get_image(self, obj):
        return resolve_model_image(self.context.get('request'), obj)


class NewsArticleListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = [
            'id', 'slug',
            'title_fr', 'title_de', 'title_nl',
            'description_fr', 'description_de', 'description_nl',
            'image', 'published_at',
        ]

    def get_image(self, obj):
        return resolve_model_image(self.context.get('request'), obj)


class NewsArticleDetailSerializer(NewsArticleListSerializer):
    class Meta(NewsArticleListSerializer.Meta):
        fields = NewsArticleListSerializer.Meta.fields + [
            'content_fr', 'content_de', 'content_nl',
        ]


class WhyChooseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyChooseItem
        fields = ['id', 'text_fr', 'text_de', 'text_nl', 'order']


class ContactMessageSerializer(serializers.ModelSerializer):
    vehicle_slug = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message', 'vehicle_slug']

    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError('Le message doit contenir au moins 10 caractères.')
        return value

    def validate_phone(self, value):
        value = value.strip()
        if value and not PHONE_REGEX.match(value):
            raise serializers.ValidationError(
                'Numéro de téléphone invalide. Exemples : 080 39 99 81 (BE), '
                '06 12 34 56 78 (FR), 621 123 456 (LU), 06 12345678 (NL).'
            )
        return value

    def validate(self, attrs):
        slug = (attrs.pop('vehicle_slug', '') or '').strip()
        if not slug:
            attrs['vehicle'] = None
            return attrs

        try:
            vehicle = UsedVehicle.objects.get(slug=slug, is_active=True)
        except UsedVehicle.DoesNotExist:
            raise serializers.ValidationError({
                'vehicle_slug': 'Ce véhicule est introuvable ou n\'est plus disponible.',
            })

        if vehicle.is_sold:
            raise serializers.ValidationError({
                'vehicle_slug': 'Ce véhicule a été vendu. Le formulaire de contact n\'est plus disponible pour cette annonce.',
            })

        attrs['vehicle'] = vehicle
        return attrs


class CustomerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReview
        fields = [
            'id', 'author_name', 'rating', 'content',
            'source', 'review_date', 'order',
        ]


class PublicReviewSubmitSerializer(serializers.Serializer):
    author_name = serializers.CharField(max_length=120)
    rating = serializers.IntegerField(min_value=1, max_value=5)
    content = serializers.CharField()
    company = serializers.CharField(required=False, allow_blank=True, default='')

    def validate_author_name(self, value):
        name = value.strip()
        if len(name) < 2:
            raise serializers.ValidationError('Indiquez votre prénom ou nom (2 caractères minimum).')
        return name

    def validate_content(self, value):
        content = value.strip()
        if len(content) < 10:
            raise serializers.ValidationError('Votre avis doit contenir au moins 10 caractères.')
        if len(content) > 2000:
            raise serializers.ValidationError('Votre avis ne peut pas dépasser 2000 caractères.')
        return content

    def validate(self, attrs):
        if attrs.get('company', '').strip():
            attrs['_honeypot'] = True
        return attrs

    def create(self, validated_data):
        if validated_data.pop('_honeypot', False):
            return None

        validated_data.pop('company', None)
        return CustomerReview.objects.create(
            author_name=validated_data['author_name'],
            rating=validated_data['rating'],
            content=validated_data['content'],
            source='website',
            is_published=False,
            order=999,
        )


class UsedVehicleSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = UsedVehicle
        fields = [
            'id', 'slug', 'brand', 'model_name', 'year', 'mileage',
            'fuel_type', 'transmission', 'price',
            'title_fr', 'title_de', 'title_nl',
            'description_fr', 'description_de', 'description_nl',
            'image', 'images', 'is_sold', 'order',
        ]

    def get_images(self, obj):
        return vehicle_gallery_urls(obj)

    def get_image(self, obj):
        images = self.get_images(obj)
        return images[0] if images else None


class AdminSiteSettingsSerializer(serializers.ModelSerializer):
    logo_url = FlexibleURLField(required=False)
    hero_image_url = FlexibleURLField(required=False)
    about_image_url = FlexibleURLField(required=False)
    facebook_url = FlexibleURLField(required=False)
    google_maps_url = FlexibleURLField(required=False)

    class Meta:
        model = SiteSettings
        fields = [
            'company_name',
            'tagline_fr', 'tagline_de', 'tagline_nl',
            'about_fr', 'about_de', 'about_nl',
            *SITE_CONTENT_FIELDS,
            'address', 'city', 'postal_code', 'country',
            'phone', 'email', 'facebook_url',
            'monday_hours', 'tuesday_hours', 'wednesday_hours',
            'thursday_hours', 'friday_hours', 'saturday_hours', 'sunday_hours',
            'latitude', 'longitude',
            'logo_url', 'hero_image_url',
            'google_rating', 'google_review_count', 'google_maps_url',
        ]


class AdminNewsArticleSerializer(serializers.ModelSerializer):
    image_url = FlexibleURLField(required=False)
    image = serializers.ImageField(required=False, allow_null=True)
    image_preview = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = [
            'id', 'slug',
            'title_fr', 'title_de', 'title_nl',
            'description_fr', 'description_de', 'description_nl',
            'content_fr', 'content_de', 'content_nl',
            'image', 'image_url', 'image_preview', 'is_published', 'published_at',
        ]
        read_only_fields = ['slug', 'image_preview']

    def get_image_preview(self, obj):
        return resolve_model_image(self.context.get('request'), obj)


class AdminCustomerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReview
        fields = [
            'id', 'author_name', 'rating', 'content', 'source',
            'review_date', 'is_published', 'order',
        ]
        read_only_fields = ['is_published', 'order']

    def create(self, validated_data):
        validated_data.setdefault('source', 'manual')
        validated_data.setdefault('is_published', False)
        validated_data.setdefault('order', 999)
        return super().create(validated_data)


class AdminUsedVehicleSerializer(serializers.ModelSerializer):
    image_url = FlexibleURLField(required=False)
    image = serializers.ImageField(required=False, allow_null=True)
    image_preview = serializers.SerializerMethodField()
    gallery_urls = serializers.ListField(
        child=FlexibleURLField(),
        required=False,
        write_only=True,
    )
    gallery = serializers.SerializerMethodField()

    class Meta:
        model = UsedVehicle
        fields = [
            'id', 'slug', 'brand', 'model_name', 'year', 'mileage',
            'fuel_type', 'transmission', 'price',
            'title_fr', 'title_de', 'title_nl',
            'description_fr', 'description_de', 'description_nl',
            'image', 'image_url', 'image_preview', 'gallery', 'gallery_urls',
            'is_active', 'is_sold', 'order',
        ]
        read_only_fields = ['slug', 'image_preview', 'gallery']

    def validate_price(self, value):
        if value is not None and value > Decimal('9999999999.99'):
            raise serializers.ValidationError('Le prix ne peut pas dépasser 9 999 999 999,99 € (10 chiffres).')
        return value

    def get_image_preview(self, obj):
        images = vehicle_gallery_urls(obj)
        return images[0] if images else resolve_model_image(self.context.get('request'), obj)

    def get_gallery(self, obj):
        return vehicle_gallery_storage_urls(obj)

    def create(self, validated_data):
        gallery_urls = validated_data.pop('gallery_urls', None)
        instance = super().create(validated_data)
        if gallery_urls is not None:
            sync_vehicle_gallery(instance, gallery_urls)
        elif instance.image_url or instance.image:
            storage_urls = vehicle_gallery_storage_urls(instance)
            if storage_urls:
                sync_vehicle_gallery(instance, storage_urls)
        return instance

    def update(self, instance, validated_data):
        gallery_urls = validated_data.pop('gallery_urls', None)
        instance = super().update(instance, validated_data)
        if gallery_urls is not None:
            sync_vehicle_gallery(instance, gallery_urls)
        return instance


class AdminServiceSerializer(serializers.ModelSerializer):
    image_url = FlexibleURLField(required=False)
    image = serializers.ImageField(required=False, allow_null=True)
    image_preview = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id',
            'title_fr', 'title_de', 'title_nl',
            'description_fr', 'description_de', 'description_nl',
            'icon', 'image', 'image_url', 'image_preview', 'order', 'is_active',
        ]
        read_only_fields = ['image_preview']

    def get_image_preview(self, obj):
        return resolve_model_image(self.context.get('request'), obj)


class AdminWhyChooseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyChooseItem
        fields = ['id', 'text_fr', 'text_de', 'text_nl', 'order', 'is_active']


class AdminContactMessageSerializer(serializers.ModelSerializer):
    vehicle = serializers.SerializerMethodField()

    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'phone', 'subject', 'message',
            'vehicle', 'is_read', 'created_at',
        ]
        read_only_fields = ['name', 'email', 'phone', 'subject', 'message', 'vehicle', 'created_at']

    def get_vehicle(self, obj):
        if not obj.vehicle_id:
            return None
        vehicle = obj.vehicle
        return {
            'id': vehicle.id,
            'slug': vehicle.slug,
            'title_fr': vehicle.title_fr,
            'brand': vehicle.brand,
            'model_name': vehicle.model_name,
            'year': vehicle.year,
            'is_sold': vehicle.is_sold,
        }


class AdminStaffUserSerializer(serializers.ModelSerializer):
    mfa_enabled = serializers.SerializerMethodField()
    is_current_user = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'email',
            'is_superuser',
            'date_joined',
            'last_login',
            'mfa_enabled',
            'is_current_user',
        ]
        read_only_fields = fields

    def get_mfa_enabled(self, obj):
        return AdminMfaDevice.objects.filter(user=obj, is_enabled=True).exists()

    def get_is_current_user(self, obj):
        request = self.context.get('request')
        return bool(request and request.user.pk == obj.pk)


class AdminStaffUserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)

    def validate_username(self, value):
        User = get_user_model()
        username = value.strip()
        if not username:
            raise serializers.ValidationError('Identifiant requis.')
        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError('Cet identifiant existe déjà.')
        return username

    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'].strip(),
            password=validated_data['password'],
            is_staff=True,
            is_active=True,
            is_superuser=False,
        )
        return user
