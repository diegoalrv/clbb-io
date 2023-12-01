from django.db import models
from django.utils.text import slugify
from uuid import uuid4

from backend.models.slots import Slot
    
class Map(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=250)
    slider = models.PositiveIntegerField()  # Campo entero positivo
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=250, blank=True)
    image = models.ImageField(upload_to='maps/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Map, self).save(*args, **kwargs)

    def __str__(self):
        return f"Map {self.name}"
    



