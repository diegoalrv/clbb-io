from rest_framework import viewsets
from backend.models.maps import Slot
from backend.serializers.map import SlotSerializer

from django.conf import settings

class SlotViewSet(viewsets.ModelViewSet):
    serializer_class = SlotSerializer
    queryset = Slot.objects.all()

    # Definir el campo de búsqueda como 'number' en lugar de 'id'
    lookup_field = 'number'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Verificar si se está accediendo al detalle o al listado
        if self.action == 'list':
            return queryset  # Listado completo
        else:
            # Acceso al detalle por 'number'
            number_param = self.kwargs.get('number', None)
            if number_param is not None:
                queryset = queryset.filter(number=number_param)
            
            return queryset

    