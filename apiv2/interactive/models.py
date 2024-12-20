from django.db import models

# Create your models here.

class InterfaceState(models.Model):
    state = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.state


class Indicator(models.Model):
    name = models.CharField(max_length=255)
    value = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name