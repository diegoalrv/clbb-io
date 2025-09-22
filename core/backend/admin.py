from django.contrib import admin

from .models import (
    Layer,
    Data,
    Config
)

admin.site.register(Layer)
admin.site.register(Data)
admin.site.register(Config)
