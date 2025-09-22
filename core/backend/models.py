from django.db import models

class Layer(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class LayerData(models.Model):
    id = models.AutoField(primary_key=True)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE, related_name='data')
    file = models.FileField(upload_to='parquets/')  # stored in MEDIA_ROOT/parquets/
    # data = models.JSONField()

    def __str__(self):
        return f"Data {self.id}"
    
class LayerConfig(models.Model):
    id = models.AutoField(primary_key=True)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE, related_name='config')
    config = models.JSONField(default=dict)

    def __str__(self):
        return f"LayerConfig {self.id}"

