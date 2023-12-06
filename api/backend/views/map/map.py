from rest_framework import viewsets
from backend.models.maps import Map
from backend.serializers.map import MapSerializer

class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Obtén los parámetros de consulta
        slider_param = self.request.query_params.get('slider', None)
        slot_param = self.request.query_params.get('slot', None)

        coin_param = self.request.query_params.get('coin', None)

        # Filtra por slider si el parámetro está presente
        if slider_param is not None and slot_param is not None:
            queryset = queryset.filter(slider=slider_param, slot__number=slot_param)

        elif coin_param is not None:
            queryset = queryset.filter(coin__number=coin_param)

        return queryset
