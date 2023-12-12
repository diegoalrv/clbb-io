from rest_framework import viewsets
from django.db.models import Q
from backend.models.maps import Map
from backend.serializers.map import MapSerializer

class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Obtén los parámetros de consulta
        slider_param = self.request.query_params.get('slider', None)
        slots_param = self.request.query_params.get('slots', None)

        coin_param = self.request.query_params.get('coin', None)

        # Filtra por slider si el parámetro está presente
        if slider_param is not None and slots_param is not None:
            slots_param = slots_param.split(',')
            queryset = queryset.filter(
                Q(slider=slider_param) &   
                Q(slot1__aruco_id=slots_param[0]) &
                Q(slot2__aruco_id=slots_param[1]) &
                Q(slot3__aruco_id=slots_param[2]) &
                Q(slot4__aruco_id=slots_param[3]) &
                Q(slot5__aruco_id=slots_param[4]) &
                Q(slot6__aruco_id=slots_param[5]) &
                Q(slot7__aruco_id=slots_param[6])
            )

        elif coin_param is not None:
            queryset = queryset.filter(coin__number=coin_param)

        return queryset
