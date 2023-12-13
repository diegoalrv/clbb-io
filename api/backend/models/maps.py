from django.db import models
from django.utils.text import slugify
from uuid import uuid4

from backend.models.slots import Slot
from backend.models.coins import Coin
    
class Map(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=250)
    slider = models.PositiveIntegerField()  # Campo entero positivo
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=250, blank=True)
    image = models.ImageField(upload_to='maps/')

    slot1 = models.ForeignKey(Slot, on_delete=models.CASCADE, blank=True, null=True, related_name='slot1')
    slot2 = models.ForeignKey(Slot, on_delete=models.CASCADE, blank=True, null=True, related_name='slot2')
    slot3 = models.ForeignKey(Slot, on_delete=models.CASCADE, blank=True, null=True, related_name='slot3')
    slot4 = models.ForeignKey(Slot, on_delete=models.CASCADE, blank=True, null=True, related_name='slot4')
    slot5 = models.ForeignKey(Slot, on_delete=models.CASCADE, blank=True, null=True, related_name='slot5')
    slot6 = models.ForeignKey(Slot, on_delete=models.CASCADE, blank=True, null=True, related_name='slot6')
    slot7 = models.ForeignKey(Slot, on_delete=models.CASCADE, blank=True, null=True, related_name='slot7')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Map, self).save(*args, **kwargs)

    def __str__(self):
        return f"Map {self.name}"
    

class TestImage(models.Model):
    image = models.ImageField(upload_to='test/')