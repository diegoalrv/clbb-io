from django.db import models

class Layer(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Data(models.Model):
    id = models.AutoField(primary_key=True)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE, related_name='data')
    key = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    props = models.JSONField(default=dict)
    file = models.FileField(upload_to='data/')  # stored in MEDIA_ROOT/data/

    def __str__(self):
        return f"Data {self.id}"

# class Texture(models.Model):
#     id = models.AutoField(primary_key=True)
#     layer = models.ForeignKey(Layer, on_delete=models.CASCADE, related_name='data')
#     key = models.CharField(max_length=100)
#     format = models.CharField(max_length=100)
#     type = models.CharField(max_length=100)
#     file = models.FileField(upload_to='textures/')  # stored in MEDIA_ROOT/data/

#     def __str__(self):
#         return f"Texture {self.id}"

class Config(models.Model):
    id = models.AutoField(primary_key=True)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE, related_name='config')
    modules = models.JSONField(default=dict)
    props = models.JSONField(default=dict)

    def __str__(self):
        return f"Config {self.id}"
