from django.db import models
from django.utils.text import slugify
from uuid import uuid4

from backend.models.slots import Slot

DISTRIBUTION_CHOICES = [
    ('hexagonal', 'Hexagonal'),
    ('square', 'Manzana'),
    ('grid', 'Grilla'),
]

class MapDistribution(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    distribution = models.CharField(
        max_length=50,
        choices=DISTRIBUTION_CHOICES,
        default='square',
        blank=False,
        null=False
    )

    def __str__(self):
        return self.distribution
    
class Map(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=250)
    satelital = models.BooleanField(blank=False, null=False) # Satital view
    streets = models.BooleanField(blank=False, null=False) # Street on map
    slider = models.PositiveIntegerField()  # Campo entero positivo
    distribution = models.ForeignKey(MapDistribution, on_delete=models.CASCADE) # Referece to Hexagonal, grid or square
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=250, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Map, self).save(*args, **kwargs)

    def __str__(self):
        return f"Map {self.name}"
    



