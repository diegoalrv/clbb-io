import cv2
import requests
from capture_aruco import detectar_aruco

# Abre la cámara (usualmente la cámara predeterminada, 0)
cap = cv2.VideoCapture(0)

green = (0, 255, 0)
red = (0, 0, 255)
blue = (255, 0, 0)

while True:
    # Captura el fotograma
    ret, frame = cap.read()

    # Muestra el fotograma en una ventana llamada 'Frame'
    # cv2.imshow('Frame', frame)
    image_with_aruco_marker, corners, ids = detectar_aruco(frame.copy())

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
                cv2.putText(image_with_aruco_marker, data["name"], (centro_x,centro_y), cv2.FONT_HERSHEY_SIMPLEX, 2, red, 3)

    
    cv2.imshow("Video con aruco", image_with_aruco_marker)

    # Rompe el bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra la ventana
cap.release()
cv2.destroyAllWindows()
