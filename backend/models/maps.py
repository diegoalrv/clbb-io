from django.db import models
from django.utils.text import slugify
from uuid import uuid4

from backend.models.slots import Slot

class MapBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='data/map/images/')  
    slug = models.SlugField(unique=True, max_length=250, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(MapBase, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Map(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=250)
    base = models.ForeignKey(MapBase, on_delete=models.CASCADE)
    slider = models.PositiveIntegerField()  # Campo entero positivo
    group = models.CharField(max_length=50)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)

    def __str__(self):
        return f"Map {self.id}"


