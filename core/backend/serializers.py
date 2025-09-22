from django.db import models
from rest_framework import serializers
from .models import (
    Layer,
    Data,
    Config
)

class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = '__all__'

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = '__all__'
