from django.contrib import admin

from .models import (
    GlobalVariable,
    Layer,
    State,
    Selection,
    Option,
    LayerSelection,
    Colormap,
    Data,
    LayerData,
    Texture,
)

admin.site.register(GlobalVariable)
admin.site.register(Layer)
admin.site.register(State)
admin.site.register(Selection)
admin.site.register(Option)
admin.site.register(LayerSelection)
admin.site.register(Colormap)
admin.site.register(Data)
admin.site.register(LayerData)
admin.site.register(Texture)
