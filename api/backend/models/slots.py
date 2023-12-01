from django.db import models
from uuid import uuid4
from .project import Project

class Slot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=500)
    number = models.PositiveIntegerField(default=0)
    # project = models.ForeignKey(Project, on_delete=models.CASCADE)
    lego_image = models.ImageField(upload_to='lego/', null=True, blank=True)
    aruco_marker = models.ImageField(upload_to='aruco_markers/', null=True, blank=True)

    def __str__(self):
        return f"Slot {self.name}"


