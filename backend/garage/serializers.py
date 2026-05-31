from rest_framework import serializers

from .models import ContactMessage, CustomerReview, NewsArticle, Service, SiteSettings


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


class CustomerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReview
        fields = [
            'id', 'author_name', 'rating', 'content',
            'source', 'review_date', 'order',
        ]
