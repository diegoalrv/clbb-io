from django.db import models
from uuid import uuid4

class Coin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=500)
    aruco_id = models.PositiveIntegerField(default=0)
    aruco_marker = models.ImageField(upload_to='aruco_markers/', null=True, blank=True)

    def __str__(self):
        return f"Coin {self.name}"


