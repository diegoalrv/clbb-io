from django.db import models
from rest_framework import serializers
from .models import (
    Layer,
    LayerData,
    LayerConfig
)

class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = '__all__'

class LayerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerData
        fields = '__all__'

class LayerConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerConfig
        fields = '__all__'
