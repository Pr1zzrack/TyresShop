from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.Blacktyres.urls')),
    path('api/swagger/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
