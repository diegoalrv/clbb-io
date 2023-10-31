from rest_framework.routers import DefaultRouter
from django.urls import path, include
from backend.views.map.map import MapViewSet

router = DefaultRouter()
router.register(r'maps', MapViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
