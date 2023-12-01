from django.contrib import admin
from backend.models.maps import Map
from backend.models.slots import Slot

@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('name', 'slider', 'slug')

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'number')