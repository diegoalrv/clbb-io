from rest_framework import viewsets
from django.db.models import Q
from backend.models.maps import Map
from backend.models.coins import Coin
from backend.serializers.map import MapSerializer

IDS = {
    '13': 0,
    '14': 1,
    '15': 2,
    '16': 3,
    '17': 4,
    '18': 5,
    '19': 6
}

class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # print(self.request.query_params)

        # Obtén los parámetros de consulta
        slider_param = self.request.query_params.get('slider', None)
        slots_param = self.request.query_params.get('slots', None)
        coin_param = self.request.query_params.get('coin', None)

        if coin_param is not None:
            coin = Coin.objects.get(aruco_id=coin_param)

        # Filtra por slider si el parámetro está presente
        if slider_param is not None and slots_param is not None:
            slots_param = sorted(slots_param.split(','))
            for num in slots_param:
                if int(num) >= 20:
                    slots_param.remove(num)
                    slots_param.insert(IDS[str(int(num)-7)], num)
            queryset = queryset.filter(
                Q(slider=slider_param) &   
                Q(coin = coin if coin_param is not None else None) &
                Q(slot1__aruco_id=slots_param[0]) &
                Q(slot2__aruco_id=slots_param[1]) &
                Q(slot3__aruco_id=slots_param[2]) &
                Q(slot4__aruco_id=slots_param[3]) &
                Q(slot5__aruco_id=slots_param[4]) &
                Q(slot6__aruco_id=slots_param[5]) &
                Q(slot7__aruco_id=slots_param[6])
            )

        # Filtra por los slots activos
        elif slots_param is not None:
            slots_param = sorted(slots_param.split(','))
            for num in slots_param:
                if int(num) >= 20:
                    slots_param.remove(num)
                    slots_param.insert(IDS[str(int(num)-7)], num)
            queryset = queryset.filter(
                Q(slot1__aruco_id=slots_param[0]) &
                Q(slot2__aruco_id=slots_param[1]) &
                Q(slot3__aruco_id=slots_param[2]) &
                Q(slot4__aruco_id=slots_param[3]) &
                Q(slot5__aruco_id=slots_param[4]) &
                Q(slot6__aruco_id=slots_param[5]) &
                Q(slot7__aruco_id=slots_param[6])
            )

        elif coin_param is not None:
            queryset = queryset.filter(coin=coin)

        return queryset
   
from backend.models.maps import TestImage
from backend.serializers.map import TestImageSerializer

class TestImageViewSet(viewsets.ModelViewSet):
    queryset = TestImage.objects.all()
    serializer_class = TestImageSerializer