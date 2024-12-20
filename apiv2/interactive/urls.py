from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from django.db import models

from rest_framework import serializers, viewsets

# from .models import 

router = DefaultRouter()

# router.register(r'indicators', viewsets.ModelViewSet, basename='indicator')

urlpatterns = [
    path('', include(router.urls)),
]