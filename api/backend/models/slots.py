from django.db import models

class Slot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    number = models.PositiveIntegerField(default=0)
    project = models.CharField(max_length=500)

    def __str__(self):
        return f"Slot {self.name}"
