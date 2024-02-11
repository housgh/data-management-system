"""
URL configuration for datamanagementsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from datamanagementsystem.views.user_registeration import UserRegistrationAPIView
from datamanagementsystem.views.organization_view import OrganizationAPIView
from datamanagementsystem.views.token_view import TokenView
from datamanagementsystem.views.entity_view import EntityAPIView, get_entity
from datamanagementsystem.views.property_view import PropertyAPIView
from datamanagementsystem.views.data_view import get_all_data, get_single
from rest_framework.routers import DefaultRouter


schema_view = get_schema_view(
    openapi.Info(
        title="Data Management System",
        default_version='v1',
        description="Multi-tenant application with dynamic schema manipulation.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'property', PropertyAPIView, basename='property')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/organization/', OrganizationAPIView.as_view(), name="create-organization"),

    path('api/entity/<int:pk>/', get_entity),
    path('api/entity/', EntityAPIView.as_view(), name="entity"),
    path('api/entity/', include(router.urls)),

    path('api/data/<str:entity_name>', get_all_data, name="data"),
    path('api/data/single/<str:entity_name>/<int:id>', get_single, name="single")
]
