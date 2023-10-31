from rest_framework import serializers
from backend.models.maps import Map
from backend.serializers.slot import SlotSerializer

class MapSerializer(serializers.ModelSerializer):
    slot = SlotSerializer()

    class Meta:
        model = Map
        fields = '__all__'
