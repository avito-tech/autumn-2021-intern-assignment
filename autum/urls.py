from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.services.router')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt'), name='login'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
