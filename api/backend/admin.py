from django.contrib import admin
from backend.models.maps import Map
from backend.models.slots import Slot
from backend.models.coins import Coin
from backend.models.aestatics import AeStatic

@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('name', 'slider', 'slug','category')
    search_fields = ['name']
    
@admin.register(AeStatic)
class AeStaticAdmin(admin.ModelAdmin):
    list_display = ('name', 'slider', 'slug')
    search_fields = ['name'] 

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'aruco_id')

@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'aruco_id')