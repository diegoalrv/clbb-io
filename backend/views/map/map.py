from rest_framework import viewsets
from backend.models.maps import Map
from backend.serializers.map import MapSerializer

class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
