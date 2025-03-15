from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TyreViewSet


# router = DefaultRouter()
# router.register(r'tyres', TyreViewSet)


urlpatterns = [
    # path('', include(router.urls)),
    path('tyres/', TyreViewSet.as_view({'get': 'list', 'post': 'create'}), name='brand-list'),
    path('tyres/<int:pk>/', TyreViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='brand-detail'),
]
