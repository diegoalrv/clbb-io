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

    # Abre la cámara (usualmente la cámara predeterminada, 0)
    cap1 = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(2)
    img_path = "./images/capture/imagen.jpg"

    local_url = 'http://localhost:8500/api/maps'
    # server_url = 'http://192.168.31.120'
    server_url = 'http://localhost'
    api_port = '8500'
    dash_port = '8900'
    img_port = '9001'

    detector = Detector()

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        frame = cv2.hconcat([frame1, frame2])

        image_with_aruco_marker, corners, ids = detectar_aruco(frame.copy())
        print(ids)
        
        # Finally
        if START_COMPARING:
            response = None
            if len(detector.slots) < 7:
                continue
            else:
                str_slots = ",".join(map(str, detector.slots))
                url = f'{local_url}:{api_port}/?slots={str_slots}'
            try:
                # Realiza la solicitud GET
                print(url)
                response = requests.get(url)

                # Verifica si la solicitud fue exitosa (código de estado 200)
                if response.status_code == 200:
                    # Imprime el contenido de la respuesta
                    data = response.json()
                    try:
                        data = data[0]
                        slot_combination = data["name"][-7:]
                        if OLD_COMBINATION != slot_combination:
                            data_json = requests.get(f'{server_url}:{api_port}/media/json/{slot_combination}.json')
                            json_data = data_json.json()
                            # print(json_data)
                            post_json = requests.post(f'{server_url}:{dash_port}/receive_data', json=json_data)

                            OLD_COMBINATION = slot_combination
                    except:
                        continue

                    image_url = data["image"]
                    # print(image_url)
                    body = {"new_image_url": image_url}
                    post_image = requests.post(f'{server_url}:{img_port}/update_image', json=body)
                    # print(post_image.status_code)

            except Exception as e:
                print(e)
        # Rompe el bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite(img_path, frame)
            break

    # Libera la cámara y cierra la ventana
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()