from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# Swagger / DRF-YASG
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import api_root_view


# ---------------- Swagger Config ----------------
schema_view = get_schema_view(
    openapi.Info(
        title="Hotel Booking API",
        default_version="v1",
        description="API Documentation for Hotel Booking Project",
        contact=openapi.Contact(email="contact@hotelbooking.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# ---------------- URL Patterns ----------------
urlpatterns = [

    # Admin
    path("admin/", admin.site.urls),

    # API Root
    path("", api_root_view),

    # Apps API
    path("api/users/", include("users.urls")),
    path("api/hotels/", include("hotels.urls")),
    path("api/payments/", include("payments.urls")),

    # JWT Authentication
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Swagger Docs
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="redoc-ui",
    ),
]


# ---------------- Media Files (Images) ----------------
if settings.DEBUG:

    # Image / Media Serve
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    # Debug Toolbar
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
