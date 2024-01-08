from django.core.management.base import BaseCommand
from backend.models import Map

class Command(BaseCommand):
    help = 'Set the coin field to null for all Map objects'

    def handle(self, *args, **kwargs):
        maps_with_coins = Map.objects.exclude(coin__isnull=True)
        
        for map_obj in maps_with_coins:
            map_obj.coin = None
            map_obj.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully set coin to null for Map: {map_obj}'))
