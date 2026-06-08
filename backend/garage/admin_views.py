from django.contrib.auth import authenticate, get_user_model
from django.core.files.storage import default_storage
from django.core import signing
from django.utils import timezone
from rest_framework import generics, parsers, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .google_reviews import MAX_FEATURED_REVIEWS, set_featured_reviews, sync_google_reviews
from .mfa import (
    create_pending_token,
    generate_qr_base64,
    generate_totp_secret,
    get_totp_uri,
    verify_pending_token,
    verify_totp,
)
from .models import AdminMfaDevice, ContactMessage, CustomerReview, NewsArticle, Service, SiteSettings, UsedVehicle, WhyChooseItem
from .serializers import (
    AdminContactMessageSerializer,
    AdminCustomerReviewSerializer,
    AdminNewsArticleSerializer,
    AdminServiceSerializer,
    AdminSiteSettingsSerializer,
    AdminStaffUserCreateSerializer,
    AdminStaffUserSerializer,
    AdminUsedVehicleSerializer,
    AdminWhyChooseItemSerializer,
)


class AdminUploadView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    ALLOWED_FOLDERS = {'news', 'vehicles', 'settings', 'services'}
    MAX_SIZE = 5 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}

    def post(self, request):
        import os
        import uuid

        folder = request.data.get('folder', 'settings')
        if folder not in self.ALLOWED_FOLDERS:
            return Response({'detail': 'Dossier invalide.'}, status=status.HTTP_400_BAD_REQUEST)

        uploaded = request.FILES.get('file')
        if not uploaded:
            return Response({'detail': 'Fichier requis.'}, status=status.HTTP_400_BAD_REQUEST)

        if uploaded.size > self.MAX_SIZE:
            return Response(
                {'detail': 'Fichier trop volumineux (maximum 5 Mo).'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not uploaded.content_type.startswith('image/'):
            return Response({'detail': 'Le fichier doit être une image.'}, status=status.HTTP_400_BAD_REQUEST)

        ext = os.path.splitext(uploaded.name)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            return Response({'detail': 'Format non supporté (jpg, png, webp, gif).'}, status=status.HTTP_400_BAD_REQUEST)

        filename = f'{uuid.uuid4().hex}{ext}'
        saved_path = default_storage.save(f'{folder}/{filename}', uploaded)
        url = default_storage.url(saved_path)
        return Response({
            'url': url,
            'absolute_url': request.build_absolute_uri(url),
        }, status=status.HTTP_201_CREATED)


class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is None or not user.is_staff:
            return Response(
                {'detail': 'Identifiants incorrects ou accès refusé.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        device = AdminMfaDevice.objects.filter(user=user, is_enabled=True).first()
        if device:
            return Response({
                'mfa_required': True,
                'pending_token': create_pending_token(user.pk),
                'username': user.username,
            })

        token, _ = Token.objects.get_or_create(user=user)
        mfa_enabled = AdminMfaDevice.objects.filter(user=user, is_enabled=True).exists()
        return Response({
            'token': token.key,
            'username': user.username,
            'mfa_enabled': mfa_enabled,
        })


class AdminLoginMfaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        pending_token = request.data.get('pending_token', '').strip()
        code = request.data.get('code', '').strip()

        if not pending_token or not code:
            return Response({'detail': 'Code requis.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = verify_pending_token(pending_token)
        except signing.BadSignature:
            return Response(
                {'detail': 'Session expirée. Reconnectez-vous.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        User = get_user_model()
        user = User.objects.filter(pk=user_id, is_staff=True).first()
        if user is None:
            return Response({'detail': 'Accès refusé.'}, status=status.HTTP_401_UNAUTHORIZED)

        device = AdminMfaDevice.objects.filter(user=user, is_enabled=True).first()
        if device is None:
            return Response({'detail': 'MFA non activée.'}, status=status.HTTP_400_BAD_REQUEST)

        if not verify_totp(device.secret, code):
            return Response({'detail': 'Code incorrect.'}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'mfa_enabled': True,
        })


class AdminLogoutView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({'detail': 'Déconnexion réussie.'})


class AdminMeView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        mfa_enabled = AdminMfaDevice.objects.filter(user=request.user, is_enabled=True).exists()
        return Response({
            'id': request.user.pk,
            'username': request.user.username,
            'mfa_enabled': mfa_enabled,
            'is_superuser': request.user.is_superuser,
        })


class AdminPasswordChangeView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        current_password = request.data.get('current_password', '')
        new_password = request.data.get('new_password', '')
        confirm_password = request.data.get('confirm_password', '')

        if len(new_password) < 8:
            return Response(
                {'detail': 'Le nouveau mot de passe doit contenir au moins 8 caractères.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_password != confirm_password:
            return Response(
                {'detail': 'Les deux mots de passe ne correspondent pas.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=request.user.username, password=current_password)
        if user is None:
            return Response(
                {'detail': 'Mot de passe actuel incorrect.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if current_password == new_password:
            return Response(
                {'detail': 'Le nouveau mot de passe doit être différent de l\'actuel.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save(update_fields=['password'])

        return Response({'detail': 'Mot de passe modifié avec succès.'})


class AdminSiteSettingsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        settings = SiteSettings.load()
        return Response(AdminSiteSettingsSerializer(settings, context={'request': request}).data)

    def patch(self, request):
        settings = SiteSettings.load()
        serializer = AdminSiteSettingsSerializer(
            settings,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AdminNewsListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminNewsArticleSerializer
    queryset = NewsArticle.objects.all().order_by('-published_at')
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]


class AdminNewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminNewsArticleSerializer
    queryset = NewsArticle.objects.all()
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]


class AdminReviewListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminCustomerReviewSerializer
    pagination_class = None

    def get_queryset(self):
        return CustomerReview.objects.all().order_by('-review_date', '-created_at')


class AdminReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminCustomerReviewSerializer
    queryset = CustomerReview.objects.all()


class AdminReviewSyncView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        result = sync_google_reviews()
        status_code = status.HTTP_200_OK if result['ok'] else status.HTTP_400_BAD_REQUEST
        return Response(result, status=status_code)


class AdminReviewSelectionView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        review_ids = request.data.get('review_ids', [])
        if not isinstance(review_ids, list):
            return Response({'detail': 'Liste d\'identifiants invalide.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            count = set_featured_reviews(review_ids)
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'detail': f'{count} avis affichés sur l\'accueil.',
            'count': count,
            'max': MAX_FEATURED_REVIEWS,
        })


class AdminVehicleListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminUsedVehicleSerializer
    queryset = UsedVehicle.objects.all().order_by('order', '-created_at')
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]


class AdminVehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminUsedVehicleSerializer
    queryset = UsedVehicle.objects.all()
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]


class AdminServiceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminServiceSerializer
    queryset = Service.objects.all().order_by('order', 'title_fr')
    pagination_class = None
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]


class AdminServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminServiceSerializer
    queryset = Service.objects.all()
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]


class AdminWhyChooseItemListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminWhyChooseItemSerializer
    queryset = WhyChooseItem.objects.all().order_by('order', 'pk')
    pagination_class = None


class AdminWhyChooseItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminWhyChooseItemSerializer
    queryset = WhyChooseItem.objects.all()


class AdminMessageListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminContactMessageSerializer
    queryset = ContactMessage.objects.all().order_by('-created_at')


class AdminMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminContactMessageSerializer
    queryset = ContactMessage.objects.all()


class AdminMfaStatusView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        device = AdminMfaDevice.objects.filter(user=request.user).first()
        return Response({
            'enabled': bool(device and device.is_enabled),
            'pending_setup': bool(device and not device.is_enabled),
        })


class AdminMfaSetupView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        device = AdminMfaDevice.objects.filter(user=request.user, is_enabled=True).first()
        if device:
            return Response({'detail': 'MFA déjà activée.'}, status=status.HTTP_400_BAD_REQUEST)

        pending = AdminMfaDevice.objects.filter(user=request.user, is_enabled=False).first()
        if pending:
            pending.delete()

        secret = generate_totp_secret()
        device = AdminMfaDevice.objects.create(
            user=request.user,
            secret=secret,
            is_enabled=False,
        )
        otpauth_url = get_totp_uri(device.secret, request.user.username)
        return Response({
            'secret': device.secret,
            'qr_code': generate_qr_base64(otpauth_url),
            'otpauth_url': otpauth_url,
        })


class AdminMfaEnableView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        code = request.data.get('code', '').strip()
        device = AdminMfaDevice.objects.filter(user=request.user, is_enabled=False).order_by('-created_at').first()

        if device is None:
            return Response(
                {'detail': 'Lancez d\'abord la configuration MFA.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not verify_totp(device.secret, code):
            return Response({'detail': 'Code incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        device.is_enabled = True
        device.confirmed_at = timezone.now()
        device.save(update_fields=['is_enabled', 'confirmed_at'])

        return Response({
            'detail': 'Authentification à deux facteurs activée.',
            'enabled': True,
        })


class AdminMfaDisableView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        password = request.data.get('password', '')
        code = request.data.get('code', '').strip()

        user = authenticate(request, username=request.user.username, password=password)
        if user is None:
            return Response({'detail': 'Mot de passe incorrect.'}, status=status.HTTP_401_UNAUTHORIZED)

        device = AdminMfaDevice.objects.filter(user=user, is_enabled=True).first()
        if device is None:
            return Response({'detail': 'MFA non activée.'}, status=status.HTTP_400_BAD_REQUEST)

        if not verify_totp(device.secret, code):
            return Response({'detail': 'Code incorrect.'}, status=status.HTTP_401_UNAUTHORIZED)

        device.delete()
        return Response({
            'detail': 'Authentification à deux facteurs désactivée.',
            'enabled': False,
        })


class AdminUserListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        User = get_user_model()
        users = User.objects.filter(is_staff=True).order_by('username')
        serializer = AdminStaffUserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminStaffUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        output = AdminStaffUserSerializer(user, context={'request': request})
        return Response(output.data, status=status.HTTP_201_CREATED)


class AdminUserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        User = get_user_model()
        target = User.objects.filter(pk=pk, is_staff=True).first()
        if target is None:
            return Response({'detail': 'Compte introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        if target.pk == request.user.pk:
            return Response(
                {'detail': 'Vous ne pouvez pas supprimer votre propre compte.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if target.is_superuser:
            return Response(
                {'detail': 'Le compte administrateur principal ne peut pas être supprimé ici.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        remaining = User.objects.filter(is_staff=True).exclude(pk=target.pk).count()
        if remaining < 1:
            return Response(
                {'detail': 'Impossible de supprimer le dernier compte administrateur.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Token.objects.filter(user=target).delete()
        AdminMfaDevice.objects.filter(user=target).delete()
        target.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
