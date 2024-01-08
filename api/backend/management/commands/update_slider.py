from django.core.management.base import BaseCommand
from backend.models import Map
import re

class Command(BaseCommand):
    help = 'Update the slider field for Map objects based on pattern and slider value'

    def add_arguments(self, parser):
        parser.add_argument('pattern', type=str, help='Pattern to match (e.g., "proximidad_cultura_*", "educacion_*")')
        parser.add_argument('slider_value', type=int, help='New slider value (integer)')

    def handle(self, *args, **kwargs):
        pattern = kwargs['pattern']
        slider_value = kwargs['slider_value']
        
        # Filtra objetos con nombres que coinciden con el patrón y slider igual al valor actual
        maps_to_update = Map.objects.filter(
            name__startswith=pattern
        )
        
        # Actualiza el campo slider para los objetos seleccionados
        for map_obj in maps_to_update:
            map_obj.slider = slider_value
            map_obj.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated slider for Map: {map_obj}'))
