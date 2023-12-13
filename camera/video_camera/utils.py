import cv2 

def calculate_center(cord):
    esquina_superior_izquierda = cord[0][0]
    esquina_inferior_derecha = cord[0][2]
    centro_x = int((esquina_superior_izquierda[0] + esquina_inferior_derecha[0]) // 2)
    centro_y = int((esquina_superior_izquierda[1] + esquina_inferior_derecha[1]) // 2)

    return (centro_x, centro_y)

def draw_horizontal_lines(frame, cord1, cord2, slider, start_comparing = False):
    
    cord_1 = calculate_center(cord1)
    cord_2 = calculate_center(cord2)

    if not start_comparing:
        slider.slider_line = cord_1, cord_2

    x_1 = cord_1[0] + 40
    y_1 = cord_1[1]
    x_2 = cord_2[0] - 40
    y_2 = cord_2[1]
    
    # Dibujar la línea
    frame = cv2.line(frame, (x_1, y_1), (x_2, y_2), (0, 255, 0), 2)
    return frame