from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    CustomActionsViewSet,
    LayerViewSet,
    ConfigViewSet,
    DataViewSet
)

from django.db import models

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()

router.register(r'layer', LayerViewSet, basename='layer')
router.register(r'data', DataViewSet, basename='data')
router.register(r'config', ConfigViewSet , basename='config')
router.register(r'action', CustomActionsViewSet, basename='action')

urlpatterns = [
    # path('set_map_state/', CustomActionsViewSet.as_view({'get': 'receive_data_from_rfid'}), name='set_map_state'),
    # path('set_map_type/', CustomActionsViewSet.receive_data_from_buttons_page, name='set_map_type'),
] + router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)