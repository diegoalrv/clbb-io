from backend.models.maps import Map

# Actualiza instancias donde el campo name es 'uso_de_suelo'
instancias = Map.objects.all()

# Itera sobre cada instancia y actualiza el campo category según las condiciones dadas
for instancia in instancias:
    if instancia.slider in [1]:
        instancia.category = 'diversidad'
    elif instancia.slider in [2,3,5,6,7,8,9,11]:
        instancia.category = 'proximidad'
    elif instancia.slider in [4,10]:
        instancia.category = 'densidad'
    # Guarda los cambios en la instancia
    instancia.save()