from django.contrib import admin

from .models import ContactMessage, CustomerReview, NewsArticle, Service, SiteSettings, UsedVehicle, WhyChooseItem


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identité', {
            'fields': (
                'company_name',
                ('tagline_fr', 'tagline_de', 'tagline_nl'),
                ('about_fr', 'about_de', 'about_nl'),
                ('logo_url', 'hero_image_url'),
            ),
        }),
        ('Page À propos', {
            'fields': (
                ('about_title_fr', 'about_title_de', 'about_title_nl'),
                ('about_subtitle_fr', 'about_subtitle_de', 'about_subtitle_nl'),
                'about_image_url',
            ),
        }),
        ('Accueil — sections', {
            'fields': (
                ('home_services_title_fr', 'home_services_title_de', 'home_services_title_nl'),
                ('home_services_subtitle_fr', 'home_services_subtitle_de', 'home_services_subtitle_nl'),
                ('home_why_title_fr', 'home_why_title_de', 'home_why_title_nl'),
            ),
        }),
        ('Page Services', {
            'fields': (
                ('services_title_fr', 'services_title_de', 'services_title_nl'),
                ('services_subtitle_fr', 'services_subtitle_de', 'services_subtitle_nl'),
            ),
        }),
        ('Coordonnées', {
            'fields': (
                'address',
                ('postal_code', 'city', 'country'),
                ('phone', 'email', 'facebook_url'),
                ('latitude', 'longitude'),
            ),
        }),
        ('Google', {
            'fields': (
                'google_rating',
                'google_review_count',
                'google_maps_url',
                'google_place_id',
            ),
        }),
        ('Horaires', {
            'fields': (
                'monday_hours',
                'tuesday_hours',
                'wednesday_hours',
                'thursday_hours',
                'friday_hours',
                'saturday_hours',
                'sunday_hours',
            ),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title_fr', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title_fr', 'title_de', 'title_nl')
    fieldsets = (
        ('Titres', {'fields': ('title_fr', 'title_de', 'title_nl')}),
        ('Descriptions', {'fields': ('description_fr', 'description_de', 'description_nl')}),
        ('Affichage', {'fields': ('icon', 'image', 'image_url', 'order', 'is_active')}),
    )


@admin.register(WhyChooseItem)
class WhyChooseItemAdmin(admin.ModelAdmin):
    list_display = ('text_fr', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('text_fr', 'text_de', 'text_nl')


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title_fr', 'slug', 'is_published', 'published_at')
    list_filter = ('is_published', 'published_at')
    search_fields = ('title_fr', 'title_de', 'title_nl', 'slug')
    prepopulated_fields = {'slug': ('title_fr',)}
    date_hierarchy = 'published_at'
    fieldsets = (
        ('Titres', {'fields': ('title_fr', 'title_de', 'title_nl')}),
        ('Contenus', {'fields': ('content_fr', 'content_de', 'content_nl')}),
        ('Média & publication', {
            'fields': ('slug', 'image', 'image_url', 'is_published', 'published_at'),
        }),
    )


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'rating', 'source', 'review_date', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    list_filter = ('source', 'is_published', 'rating')
    search_fields = ('author_name', 'content')
    ordering = ('order', '-review_date')


@admin.register(UsedVehicle)
class UsedVehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model_name', 'year', 'price', 'is_active', 'is_sold', 'order')
    list_editable = ('is_active', 'is_sold', 'order')
    list_filter = ('is_active', 'is_sold', 'fuel_type', 'brand')
    search_fields = ('brand', 'model_name', 'title_fr')
    prepopulated_fields = {'slug': ('title_fr',)}
    fieldsets = (
        ('Véhicule', {'fields': ('brand', 'model_name', 'year', 'mileage', 'fuel_type', 'transmission', 'price')}),
        ('Titres', {'fields': ('title_fr', 'title_de', 'title_nl')}),
        ('Descriptions', {'fields': ('description_fr', 'description_de', 'description_nl')}),
        ('Affichage', {'fields': ('slug', 'image', 'image_url', 'is_active', 'is_sold', 'order')}),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    list_editable = ('is_read',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
