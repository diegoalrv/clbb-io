from django.contrib import admin

from .models import (
    Layer,
    LayerData,
    LayerConfig
)

admin.site.register(Layer)
admin.site.register(LayerData)
admin.site.register(LayerConfig)
