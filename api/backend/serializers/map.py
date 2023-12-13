from rest_framework import serializers
from backend.models.maps import Map
from backend.serializers.slot import SlotSerializer

class MapSerializer(serializers.ModelSerializer):
    slot1 = SlotSerializer()
    slot2 = SlotSerializer()
    slot3 = SlotSerializer()
    slot4 = SlotSerializer()
    slot5 = SlotSerializer()
    slot6 = SlotSerializer()
    slot7 = SlotSerializer()

    class Meta:
        model = Map
        fields = '__all__'

from backend.models.maps import TestImage

class TestImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestImage
        fields = ('image',)
