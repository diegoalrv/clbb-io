import cv2
import requests
import time
import numpy as np
from capture_aruco import detectar_aruco
from detector import Detector
from io import BytesIO
from utils import calculate_center

def main():
    START_COMPARING = True
    OLD_COMBINATION = None
    new_dims = (420, 240)

    # Abre la cámara (usualmente la cámara predeterminada, 0)
    print('Abriendo cámaras')
    cap1 = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(2)
    img_path = "./images/capture/imagen.jpg"

    # local_url = 'http://localhost:8500'
    server_url = 'http://192.168.31.120:8500'

    detector = Detector()

    lista_ids_anterior = None
    print('Comienzo escaneo')
    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        
        frame1 = cv2.resize(frame1, new_dims)
        frame2 = cv2.resize(frame2, new_dims)

        frame = cv2.hconcat([frame1, frame2])

        image_with_aruco_marker, corners, ids = detectar_aruco(frame.copy())
        ids.sort()

        # Compara las listas actual y anterior.
        if (lista_ids_anterior is not None) and (ids != lista_ids_anterior) and (len(ids) == 7):
            detector.just_slots_ids(ids.copy())
            send_states(detector, ids, server_url)  # Ejecuta la función si las listas son diferentes.

        # Actualiza la lista anterior con la lista actual.
        lista_ids_anterior = ids.copy()

        # print(ids)
        # cv2.imshow("Video con aruco", image_with_aruco_marker)

    # Libera la cámara y cierra la ventana
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()
    pass

def send_states(detector, ids, server_url):
    try:
        str_slots = ",".join(map(str, detector.slots))
        url = f'{server_url}/api/set_map_state/?slots={str_slots}'
        # Realiza la solicitud GET
        # print(url)
        # time.sleep(5)
        response = requests.get(url)
        print(response.status_code)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()