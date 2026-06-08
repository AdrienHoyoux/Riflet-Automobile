from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ContactMessage, CustomerReview, NewsArticle, Service, SiteSettings, UsedVehicle, WhyChooseItem
from .notifications import notify_contact_message
from .serializers import (
    ContactMessageSerializer,
    CustomerReviewSerializer,
    NewsArticleDetailSerializer,
    NewsArticleListSerializer,
    ServiceSerializer,
    SiteSettingsSerializer,
    UsedVehicleSerializer,
    WhyChooseItemSerializer,
)


class SiteSettingsView(APIView):
    def get(self, request):
        settings = SiteSettings.load()
        serializer = SiteSettingsSerializer(settings)
        return Response(serializer.data)


class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(is_active=True)


class WhyChooseItemListView(generics.ListAPIView):
    serializer_class = WhyChooseItemSerializer
    pagination_class = None

    def get_queryset(self):
        return WhyChooseItem.objects.filter(is_active=True)


class NewsListView(generics.ListAPIView):
    serializer_class = NewsArticleListSerializer

    def get_queryset(self):
        return NewsArticle.objects.filter(is_published=True)


class NewsDetailView(generics.RetrieveAPIView):
    serializer_class = NewsArticleDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return NewsArticle.objects.filter(is_published=True)


class ContactCreateView(generics.CreateAPIView):
    serializer_class = ContactMessageSerializer
    queryset = ContactMessage.objects.all()

    def perform_create(self, serializer):
        contact = serializer.save()
        notify_contact_message(contact)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'detail': 'Votre message a bien été envoyé. Nous vous répondrons rapidement.'},
            status=status.HTTP_201_CREATED,
        )


class ReviewListView(generics.ListAPIView):
    serializer_class = CustomerReviewSerializer

    def get_queryset(self):
        return CustomerReview.objects.filter(is_published=True).order_by('order')[:6]


class VehicleListView(generics.ListAPIView):
    serializer_class = UsedVehicleSerializer

    def get_queryset(self):
        return UsedVehicle.objects.filter(is_active=True)


class VehicleDetailView(generics.RetrieveAPIView):
    serializer_class = UsedVehicleSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return UsedVehicle.objects.filter(is_active=True)
