import re

from rest_framework import serializers

from .models import ContactMessage, CustomerReview, NewsArticle, Service, SiteSettings

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


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            'company_name',
            'tagline_fr', 'tagline_de', 'tagline_nl',
            'about_fr', 'about_de', 'about_nl',
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
        request = self.context.get('request')
        if obj.image:
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return obj.image_url or None


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
        request = self.context.get('request')
        if obj.image:
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return obj.image_url or None


class NewsArticleDetailSerializer(NewsArticleListSerializer):
    class Meta(NewsArticleListSerializer.Meta):
        fields = NewsArticleListSerializer.Meta.fields + [
            'content_fr', 'content_de', 'content_nl',
        ]


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']

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


class CustomerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReview
        fields = [
            'id', 'author_name', 'rating', 'content',
            'source', 'review_date', 'order',
        ]
