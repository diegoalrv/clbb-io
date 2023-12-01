from rest_framework import viewsets
from backend.models.maps import Slot
from backend.serializers.map import SlotSerializer

from django.conf import settings

print(settings.BASE_DIR)
class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer