import cv2
from capture_aruco import detectar_aruco
from slider import Slider
from utils import up_right_point, up_left_point

def draw_horizontal_lines(frame, cords, start_comparing = False):
    cord_1 = up_left_point(cords[0])
    cord_2 = up_right_point(cords[1])

    if not start_comparing:
        slider.slider_line = cord_1, cord_2

    # Calcular puntos finales de la línea en el borde izquierdo y derecho de la imagen
    x_left = cord_1[0]
    y_left = cord_1[1]
    x_right = cord_2[0]
    y_right = cord_2[1]
    
    # Dibujar la línea
    frame = cv2.line(frame, (x_left, y_left), (x_right, y_right), (0, 255, 0), 2)
    return frame

START_COMPARING = False

# Abre la cámara (usualmente la cámara predeterminada, 0)
cap = cv2.VideoCapture(0)
img_path = "/Users/alonsodicandia/asesorias/clbb-io/camera/images/capture/imagen.jpg"

slider = Slider()
line_color = (0, 255, 0)
middle_line_color = (0, 0, 255)
min_distance_color = (255, 0, 0)

position = ['1','2','3','4']

while True:
    # Captura el fotograma
    ret, frame = cap.read()

    # Muestra el fotograma en una ventana llamada 'Frame'
    # cv2.imshow('Frame', frame)
    image_with_aruco_marker, corners, ids = detectar_aruco(frame.copy())

    if ids is not None:
        if len(ids) == 1 and START_COMPARING:
            p1, p2 = slider.slider_line

            cv2.line(frame, p1, p2, line_color, 2)

            esquina_superior_izquierda = corners[0][0][0]
            esquina_inferior_derecha = corners[0][0][2]
            centro_x = int((esquina_superior_izquierda[0] + esquina_inferior_derecha[0]) // 2)
            centro_y = int((esquina_superior_izquierda[1] + esquina_inferior_derecha[1]) // 2)

            slider.center_one_aruco = (centro_x, centro_y)
            slider.process_upper_corners_to_get_inclination(corners[0])

            try:
                line_division = slider.subdividir_recta(p1,p2)

                print(line_division)
                distances = []

                for point in line_division:
                    x, y = point
                    distance = slider.calcular_distancia(point)
                    distances.append(distance)

                    # print(x,y)
                    cv2.line(frame, slider.center_one_aruco, (x,y), middle_line_color, 2)
                
                index_min_distance = distances.index(min(distances))
                cv2.line(frame, slider.center_one_aruco, line_division[index_min_distance], min_distance_color, 2)
                cv2.putText(frame, position[index_min_distance], (1400,300), cv2.FONT_HERSHEY_SIMPLEX, 1, min_distance_color, 5)
            except Exception as e:
                print(e)
            cv2.imshow("Video con aruco", frame)
        elif len(ids) == 2:
            images_with_circles = draw_horizontal_lines(frame, corners, START_COMPARING)
            cv2.imshow("Video con aruco", images_with_circles)
        else:
            cv2.imshow("Video con aruco", image_with_aruco_marker)
    else:
        cv2.imshow("Video con aruco", image_with_aruco_marker)

    # Rompe el bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite(img_path, frame)
        break
    elif cv2.waitKey(1) & 0xFF == ord('s'):
        START_COMPARING = True

# Libera la cámara y cierra la ventana
cap.release()
cv2.destroyAllWindows()
