from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    GlobalVariableViewSet,
    CustomActionsViewSet,
    LayerViewSet,
    StateViewSet,
    SelectionViewSet,
    OptionViewSet,
    LayerSelectionViewSet,
    ColormapViewSet,
    DataViewSet,
    LayerDataViewSet,
    TextureViewSet
)

from django.db import models

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()

router.register(r'global', GlobalVariableViewSet, basename='global')
router.register(r'layer', LayerViewSet, basename='layer')
router.register(r'state', StateViewSet, basename='state')
router.register(r'selection', SelectionViewSet, basename='selection')
router.register(r'option', OptionViewSet, basename='option')
router.register(r'layerselection', LayerSelectionViewSet, basename='layerselection')
router.register(r'colormap', ColormapViewSet, basename='colormap')
router.register(r'data', DataViewSet, basename='data')
router.register(r'layerdata', LayerDataViewSet, basename='layerdata')
router.register(r'texture', TextureViewSet, basename='texture')
router.register(r'action', CustomActionsViewSet, basename='action')

urlpatterns = [
    # path('set_map_state/', CustomActionsViewSet.as_view({'get': 'receive_data_from_rfid'}), name='set_map_state'),
    # path('set_map_type/', CustomActionsViewSet.receive_data_from_buttons_page, name='set_map_type'),
] + router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)