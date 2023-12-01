import cv2
import requests
import numpy as np
from capture_aruco import detectar_aruco
from slider import Slider
from utils import up_right_point, up_left_point
from io import BytesIO

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
        for id in ids:
            if id >= 3:
                index = ids.index(id)
                esquina_superior_izquierda = corners[index][0][0]
                esquina_inferior_derecha = corners[index][0][2]
                centro_x = int((esquina_superior_izquierda[0] + esquina_inferior_derecha[0]) // 2)
                centro_y = int((esquina_superior_izquierda[1] + esquina_inferior_derecha[1]) // 2)

                # Especifica la URL a la que deseas hacer la solicitud GET
                url = f'http://localhost:8500/api/slots/{id}/'

                # Realiza la solicitud GET
                response = requests.get(url)

                # Verifica si la solicitud fue exitosa (código de estado 200)
                if response.status_code == 200:
                    # Imprime el contenido de la respuesta
                    data = response.json()
                    cv2.putText(frame, data["name"], (centro_x,centro_y), cv2.FONT_HERSHEY_SIMPLEX, 2, middle_line_color, 3)

        if 0 in ids and START_COMPARING:
            p1, p2 = slider.slider_line

            cv2.line(frame, p1, p2, line_color, 2)

            index_aruco_zero = ids.index(0)
            esquina_superior_izquierda = corners[index_aruco_zero][0][0]
            esquina_inferior_derecha = corners[index_aruco_zero][0][2]
            centro_x = int((esquina_superior_izquierda[0] + esquina_inferior_derecha[0]) // 2)
            centro_y = int((esquina_superior_izquierda[1] + esquina_inferior_derecha[1]) // 2)

            slider.center_one_aruco = (centro_x, centro_y)

            try:
                line_division = slider.subdividir_recta(p1,p2)

                distances = []

                for point in line_division:
                    x, y = point
                    distance = slider.calcular_distancia(point)
                    distances.append(distance)

                    # print(x,y)
                    cv2.line(frame, slider.center_one_aruco, (x,y), middle_line_color, 2)
                
                index_min_distance = distances.index(min(distances))
                cv2.line(frame, slider.center_one_aruco, line_division[index_min_distance], min_distance_color, 2)
            except Exception as e:
                print(e)
            cv2.imshow("Video con aruco", frame)
        elif 1 in ids and 2 in ids and not START_COMPARING:
            images_with_circles = draw_horizontal_lines(frame, corners)
            cv2.imshow("Video con aruco", images_with_circles)
            START_COMPARING = True
        else:
            cv2.imshow("Video con aruco", image_with_aruco_marker)
    else:
        cv2.imshow("Video con aruco", image_with_aruco_marker)

    
    # Finally
    if START_COMPARING:
        try:
            url = f'http://localhost:8500/api/maps/?slider={position[index_min_distance]}&slot={data["number"]}'
            # Realiza la solicitud GET
            response = requests.get(url)

            # Verifica si la solicitud fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Imprime el contenido de la respuesta
                data = response.json()
                data = data[0]
                image_url = data["image"]
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_data = BytesIO(response.content)
                    map_image = cv2.imdecode(np.frombuffer(image_data.read(), np.uint8), cv2.IMREAD_COLOR)
                    cv2.imshow('Map image', map_image)
        except:
            print("No hay endpoint")
    # Rompe el bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite(img_path, frame)
        break

# Libera la cámara y cierra la ventana
cap.release()
cv2.destroyAllWindows()
