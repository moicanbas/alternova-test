from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls import handler404
from apps.core.views import custom_404

handler404 = custom_404

schema_view = get_schema_view(
    openapi.Info(
        title="Sistema de Calificación de Notas Universidad Nacional",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('apps.accounts.urls')),
    path('api/v1/masters/', include('apps.core.urls')),
    path('api/v1/calificaciones/', include('apps.calificaciones.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', RedirectView.as_view(url='/docs/', permanent=False)),
]
