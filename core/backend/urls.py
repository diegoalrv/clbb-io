from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from django.db import models

from rest_framework import serializers, viewsets

router = DefaultRouter()

router.register(r'indicators', viewsets.ModelViewSet, basename='indicator')
router.register(r'states', viewsets.ModelViewSet, basename='state')
router.register(r'indicator_data', viewsets.ModelViewSet, basename='indicator_data')
router.register(r'indicator_images', viewsets.ModelViewSet , basename='indicator_image')
router.register(r'indicator_geojson', viewsets.ModelViewSet , basename='indicator_geojson')
router.register(r'dashboard_feed_state', viewsets.ModelViewSet , basename='dashboard_feed_state')
router.register(r'layer_config', viewsets.ModelViewSet , basename='layer_config')

from .views import check_and_send_data

urlpatterns = [
    path('', include(router.urls)),
    path('check', check_and_send_data, name='check'),
]