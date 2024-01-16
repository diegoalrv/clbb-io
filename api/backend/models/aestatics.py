from django.db import models
from django.utils.text import slugify
from uuid import uuid4

class AeStatic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=250)
    slider = models.PositiveIntegerField(blank=True, null=True)  # Campo entero positivo
    slug = models.SlugField(unique=True, max_length=250, blank=True)
    aestatic_file = models.ImageField(upload_to='aestatic_file/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(AeStatic, self).save(*args, **kwargs)

    def __str__(self):
        return f"AeStatic {self.name}" 

