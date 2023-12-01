from django.contrib import admin
from backend.models.maps import Map, MapDistribution
from backend.models.slots import Slot

@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('name', 'satelital', 'streets', 'slider', 'slug')

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'lego_image', 'aruco_marker')

@admin.register(MapDistribution)
class MapDistributionAdmin(admin.ModelAdmin):
    list_display = ('distribution', )
