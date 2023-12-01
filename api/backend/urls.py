from rest_framework.routers import DefaultRouter
from django.urls import path, include
from backend.views.map.map import MapViewSet
from backend.views.slots.slots import SlotViewSet

router = DefaultRouter()
router.register(r'maps', MapViewSet)
router.register(r'slots', SlotViewSet)

urlpatterns = [
    path('', include(router.urls)),
]