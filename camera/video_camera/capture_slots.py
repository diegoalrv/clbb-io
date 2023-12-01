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

    

    # if ids is not None:
    #     if 0 in ids and START_COMPARING:
    #         p1, p2 = slider.slider_line

    #         cv2.line(frame, p1, p2, line_color, 2)

    #         # print(corners, ids)
    #         # break
    #         index_aruco_zero = ids.index(0)
    #         # print(index_aruco_zero)
    #         esquina_superior_izquierda = corners[index_aruco_zero][0][0]
    #         esquina_inferior_derecha = corners[index_aruco_zero][0][2]
    #         centro_x = int((esquina_superior_izquierda[0] + esquina_inferior_derecha[0]) // 2)
    #         centro_y = int((esquina_superior_izquierda[1] + esquina_inferior_derecha[1]) // 2)

    #         slider.center_one_aruco = (centro_x, centro_y)
    #         # print(slider.center_one_aruco)
    #         # slider.process_upper_corners_to_get_inclination(corners[0])

    #         try:
    #             line_division = slider.subdividir_recta(p1,p2)

    #             distances = []

    #             for point in line_division:
    #                 x, y = point
    #                 distance = slider.calcular_distancia(point)
    #                 distances.append(distance)

    #                 # print(x,y)
    #                 cv2.line(frame, slider.center_one_aruco, (x,y), middle_line_color, 2)
                
    #             index_min_distance = distances.index(min(distances))
    #             cv2.line(frame, slider.center_one_aruco, line_division[index_min_distance], min_distance_color, 2)
    #             cv2.putText(frame, position[index_min_distance], (1400,300), cv2.FONT_HERSHEY_SIMPLEX, 1, min_distance_color, 5)
    #         except Exception as e:
    #             print(e)
    #         cv2.imshow("Video con aruco", frame)
    #         # continue
    #     elif 1 in ids and 2 in ids and not START_COMPARING:
    #         images_with_circles = draw_horizontal_lines(frame, corners)
    #         cv2.imshow("Video con aruco", images_with_circles)
    #         START_COMPARING = True
    #     else:
    #         cv2.imshow("Video con aruco", image_with_aruco_marker)
    # else:
    cv2.imshow("Video con aruco", image_with_aruco_marker)

    # Rompe el bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite(img_path, frame)
        break

# Libera la cámara y cierra la ventana
cap.release()
cv2.destroyAllWindows()
