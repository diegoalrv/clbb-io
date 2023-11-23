import cv2
from capture_aruco import detectar_aruco

def up_left_point(coordenada):
    up_left = min(coordenada[0], key=lambda punto: punto[0] + punto[1])

    return (int(up_left[0]), int(up_left[1]))

def draw_lines(frame, cords):
    for cord in cords:
        up_left = up_left_point(cord)
        height, width, _ = frame.shape
        
        # Calcular puntos finales de la línea en el borde izquierdo y derecho de la imagen
        x_left = up_left[0]
        y_left = 0
        x_right = up_left[0]
        y_right = height
        
        # Dibujar la línea
        frame = cv2.line(frame, (x_left, y_left), (x_right, y_right), (0, 255, 0), 2)
    return frame

# Abre la cámara (usualmente la cámara predeterminada, 0)
cap = cv2.VideoCapture(0)
img_path = "/Users/alonsodicandia/asesorias/clbb-io/camera/images/capture/imagen.jpg"

LINES = False


while True:
    # Captura el fotograma
    ret, frame = cap.read()

    # Muestra el fotograma en una ventana llamada 'Frame'
    # cv2.imshow('Frame', frame)
    if not LINES:
        image_with_aruco_marker, corners, ids = detectar_aruco(frame.copy())

    if len(corners) == 4:
        LINES = True
        print(corners)

        images_with_circles = draw_lines(frame, corners)
        cv2.imshow("Video with lines", images_with_circles)
    else:
        if LINES:
            images_with_circles = draw_lines(frame, corners)
            cv2.imshow("Video con circulos", images_with_circles)
        else:
            cv2.imshow("Video con aruco", image_with_aruco_marker)

    # Rompe el bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite(img_path, frame)
        break

# Libera la cámara y cierra la ventana
cap.release()
cv2.destroyAllWindows()
