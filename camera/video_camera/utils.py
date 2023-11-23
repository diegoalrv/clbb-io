def up_left_point(coordenada):
    up_left = min(coordenada[0], key=lambda punto: punto[0] + punto[1])
    return (int(up_left[0]), int(up_left[1]))

def up_right_point(coordenada):
    up_right = max(coordenada[0], key=lambda punto: punto[0] - punto[1])
    return (int(up_right[0]), int(up_right[1]))

def low_left_point(coordenada):
    low_left = max(coordenada[0], key=lambda punto: punto[0] - punto[1])
    return (int(low_left[0]), int(low_left[1]))

def low_right_point(coordenada):
    low_right = max(coordenada[0], key=lambda punto: (punto[0], punto[1]))
    return (int(low_right[0]), int(low_right[1]))