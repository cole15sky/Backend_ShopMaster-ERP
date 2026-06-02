from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),

    # All API endpoints under 'api/'
    path(
        "api/",
        include(
            [
                # JWT Auth
                path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
                path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

                # App endpoints
                path("products/", include("products.urls")),
                path("inventory/", include("inventory.urls")),
                path("sales/", include("sales.urls")),
                path("customers/", include("customers.urls")),
                path("qr/", include("qr.urls")),
                path("users/", include("users.urls")),
                path("organizations/", include("organizations.urls")),

                # API schema / documentation
                path("schema/", SpectacularAPIView.as_view(), name="schema"),
                path(
                    "swagger/",
                    SpectacularSwaggerView.as_view(url_name="schema"),
                    name="swagger-ui",
                ),
                path(
                    "redoc/",
                    SpectacularRedocView.as_view(url_name="schema"),
                    name="redoc",
                ),
            ]
        ),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)