from django.urls import path

from .views import (
    ContactCreateView,
    NewsDetailView,
    NewsListView,
    ReviewListView,
    ServiceListView,
    SiteSettingsView,
)

urlpatterns = [
    path('settings/', SiteSettingsView.as_view(), name='site-settings'),
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news-detail'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('contact/', ContactCreateView.as_view(), name='contact-create'),
]
