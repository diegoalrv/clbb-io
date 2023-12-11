from django.contrib import admin
from backend.models.maps import Map
from backend.models.slots import Slot
from backend.models.coins import Coin

@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('name', 'slider', 'slug')

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'aruco_id')

@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'number')