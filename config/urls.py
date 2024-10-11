from django.contrib import admin
from django.urls import path, include
from config import settings

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from rest_framework import permissions

# Define the schema view for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="QUIZHUB API",
        default_version="v1",
        description="API documentation for QUIZ App",
        terms_of_service="https://www.yourcompany.com/terms/",
        contact=openapi.Contact(email="contact@yourcompany.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tags/', include('quizhub.urls')),
    path('api/users/', include('users.urls')),

     path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger.yaml", schema_view.without_ui(cache_timeout=0), name="schema-yaml"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
