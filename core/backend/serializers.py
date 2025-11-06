from django.db import models
from rest_framework import serializers
from .models import (
    GlobalVariable,
    Layer,
    State,
    Selection,
    Option,
    LayerSelection,
    Colormap,
    Data,
    LayerData,
    Texture,
)

class GlobalVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalVariable
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'
        
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'
class SelectionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Selection
        fields = '__all__'
class LayerSelectionSerializer(serializers.ModelSerializer):
    selection = SelectionSerializer(read_only=True)

    class Meta:
        model = LayerSelection
        fields = '__all__'
    
class ColormapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colormap
        fields = '__all__'

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['id', 'name', 'type', 'file']


class LayerDataSerializer(serializers.ModelSerializer):
    # data = DataSerializer()

    class Meta:
        model = LayerData
        fields = '__all__'
    
class TextureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Texture
        fields = '__all__'

class LayerSerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)
    colormap = ColormapSerializer(read_only=True)
    selections = LayerSelectionSerializer(many=True, source='layerselection_set', read_only=True)
    textures = TextureSerializer(many=True, source='texture_set', read_only=True)
    layer_data = LayerDataSerializer(many=True, source='layerdata_set', read_only=True)

    class Meta:
        model = Layer
        fields = '__all__'