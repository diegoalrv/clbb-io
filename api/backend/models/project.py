from django.db import models
from uuid import uuid4

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=500)
    streets = models.BooleanField()
    squares = models.BooleanField()
    land_use = models.BooleanField()
    green_area = models.BooleanField()
    amenities = models.BooleanField()
    
    def __str__(self):
        return f"Slot {self.name}"


