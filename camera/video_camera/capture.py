import cv2
import requests
import numpy as np
from capture_aruco import detectar_aruco
from slider import Slider
from detector import Detector
from io import BytesIO

from utils import calculate_center, draw_horizontal_lines

START_COMPARING = False
NUM_DIVISION = 8

# Abre la cámara (usualmente la cámara predeterminada, 0)
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
img_path = "/Users/alonsodicandia/asesorias/clbb-io/camera/images/capture/imagen.jpg"

detector = Detector()
slider = Slider()

position = [str(i) for i in range(1,NUM_DIVISION+1)]

while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    frame = cv2.hconcat([frame1, frame2])

    # Muestra el fotograma en una ventana llamada 'Frame'
    # cv2.imshow('Frame', frame)
    image_with_aruco_marker, corners, ids = detectar_aruco(frame.copy())

    if ids is not None:
        ids_copy = ids.copy()
        
        coin = detector.check_coin(ids_copy)
        detector.just_slots_ids(ids_copy)

        if 0 in ids and START_COMPARING:
            p1, p2 = slider.slider_line

            cv2.line(image_with_aruco_marker, p1, p2, detector.green, 2)

            index_aruco_zero = ids.index(0)
            centro_x, centro_y = calculate_center(corners[index_aruco_zero])

            slider.center_one_aruco = (centro_x, centro_y)

            try:
                line_division = slider.subdividir_recta(p1,p2, NUM_DIVISION)

                distances = []

                for point in line_division:
                    x, y = point
                    distance = slider.calcular_distancia(point)
                    distances.append(distance)

                    # print(x,y)
                    cv2.line(image_with_aruco_marker, slider.center_one_aruco, (x,y), detector.red, 2)
                
                index_min_distance = distances.index(min(distances))
                cv2.line(image_with_aruco_marker, slider.center_one_aruco, line_division[index_min_distance], detector.blue, 2)
            except Exception as e:
                print(e)
            cv2.imshow("Video con aruco", image_with_aruco_marker)
        elif 1 in ids and 2 in ids and not START_COMPARING:
            index_aruco_1 = ids.index(1)
            index_aruco_2 = ids.index(2)
            try:
                images_with_circles = draw_horizontal_lines(image_with_aruco_marker, corners[index_aruco_1], corners[index_aruco_2], slider)
                cv2.imshow("Video con aruco", images_with_circles)
                START_COMPARING = True
            except Exception as e:
                print(e)


        else:
            cv2.imshow("Video con aruco", image_with_aruco_marker)
    else:
        cv2.imshow("Video con aruco", image_with_aruco_marker)

    
    # Finally
    if START_COMPARING:
        response = None
        coin = None
        if coin is not None:
            url = f'http://localhost:8500/api/maps/?coin={coin}'
            print(url)
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
        try:
            url = f'http://localhost:8500/api/maps/?slider={position[index_min_distance]}&slots={",".join(map(str, detector.slots))}'
            print(url)
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
cap1.release()
cap2.release()
cv2.destroyAllWindows()
