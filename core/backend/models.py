from django.db import models

# --- Global Variables ---

class GlobalVariable(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=50)
    value = models.JSONField(null=True)

    def __str__(self):
        return f"GlobalVariable {self.key} = {self.value}"

# --- Core Layer and State Models ---

class Layer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True, null=True)
    type = models.CharField(null=True, max_length=50, help_text="e.g., 'trip', 'polygon', 'sdf'")
    icon = models.CharField(blank=True, null=True, help_text="Base64 encoded SVG or icon name")
    order = models.IntegerField(default=0)
    exclusive = models.BooleanField(default=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        help_text="Used to group layers together."
    )

    def __str__(self):
        return self.name

class State(models.Model):
    # One-to-One relationship to Layer for core state (visibility)
    layer = models.OneToOneField(
        Layer,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='state'
    )
    is_on = models.BooleanField(default=False)

    def __str__(self):
        return f"State for {self.layer.name}"

# --- Configuration/Behavior Models ---

class Selection(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, help_text="User-facing name of the selector, e.g., 'Day of Week'")
    exclusive = models.BooleanField(
        default=True,
        help_text="If True, only one option can be selected (radio button)."
    )
    # The layers that use this selection mechanism
    layers = models.ManyToManyField(
        Layer,
        through='LayerSelection',
        related_name='selectors'
    )

    def __str__(self):
        return self.name

class Option(models.Model):
    id = models.AutoField(primary_key=True)
    selection = models.ForeignKey(
        Selection,
        on_delete=models.CASCADE,
        related_name='options'
    )
    name = models.CharField(max_length=100)
    icon = models.CharField(blank=True, null=True, help_text="Base64 encoded SVG or icon name")
    is_on = models.BooleanField(
        default=False,
        help_text="The selected state for this option within its Selection."
    )

    def __str__(self):
        return f"{self.name} ({self.selection.name})"

class LayerSelection(models.Model):
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    selection = models.ForeignKey(Selection, on_delete=models.CASCADE)
    key = models.CharField(
        max_length=50,
        help_text="Application-level key for the selector (e.g., 'column', 'day')."
    )

    class Meta:
        # Ensures a layer can only use a selector key once
        unique_together = ('layer', 'key')

    def __str__(self):
        return f"{self.layer.name} uses {self.selection.name} as '{self.key}'"

class Colormap(models.Model):
    # One-to-One relationship to Layer for colormap config
    layer = models.OneToOneField(
        Layer,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='colormap'
    )
    name = models.CharField(max_length=50, help_text="e.g., 'viridis', 'magma'")
    # column_ranges = models.JSONField(
    #     default=dict,
    #     help_text="e.g., {\n\"columnA\": {\n\"default_min\": 0.0,\n\"default_max\": 100.0,\n\"current_min\": 5.0,\n\"current_max\": 68.0\n}\n}"
    # )
   
    # NOTE: It's highly recommended to use a JSONField here to store min/max per column/field
    # for flexibility (as discussed previously), but using your DBML fields:
    default_min = models.FloatField(default=0.0)
    default_max = models.FloatField(default=1.0)
    current_min = models.FloatField(default=0.0)
    current_max = models.FloatField(default=1.0)
    fallback = models.CharField(max_length=9, default='#ffffff', help_text="Fallback color in HEX (e.g., '#ff0000')")
   
    def __str__(self):
        return f"Colormap for {self.layer.name} ({self.name})"

# --- Data Models (Separated) ---

class Data(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, help_text="File type: e.g., 'geojson', 'parquet'")
    file = models.FileField(upload_to='data/')  # stored in MEDIA_ROOT/data/
   
    # Layers that use this data file
    layers = models.ManyToManyField(
        Layer,
        through='LayerData',
        related_name='data_files'
    )

    def __str__(self):
        return self.name

class LayerData(models.Model):
    id = models.AutoField(primary_key=True)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    props = models.JSONField(
        default=dict,
        help_text="e.g., {\n\"column\": \"value\"\n}"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Link {self.layer.name} to {self.data.name}"

class Texture(models.Model):
    id = models.AutoField(primary_key=True)
    layer = models.ForeignKey(
        Layer,
        on_delete=models.CASCADE,
        related_name='textures',
        help_text="The layer this texture belongs to."
    )
    key = models.CharField(
        max_length=50,
        help_text="Application key for the texture (e.g., 'u_texture0')."
    )
    format = models.CharField(max_length=50, help_text="e.g., 'R32F', 'RG32F'")
    type = models.CharField(max_length=50, help_text="e.g., '2d', '3d'")
    data_format = models.CharField(max_length=50, help_text="e.g., 'bin', 'png'")

    file = models.FileField(upload_to='data/')  # stored in MEDIA_ROOT/data/

    class Meta:
        # A layer can only have one texture with a given key
        unique_together = ('layer', 'key')
   
    def __str__(self):
        return f"Texture {self.key} for {self.layer.name}"