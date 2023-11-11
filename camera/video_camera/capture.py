import cv2
from capture_aruco import detectar_aruco

# Abre la cámara (usualmente la cámara predeterminada, 0)
cap = cv2.VideoCapture(0)
img_path = "/Users/alonsodicandia/asesorias/clbb-io/camera/images/capture/imagen.jpg"

while True:
    # Captura el fotograma
    ret, frame = cap.read()

    # Muestra el fotograma en una ventana llamada 'Frame'
    # cv2.imshow('Frame', frame)
    image_with_aruco_marker = detectar_aruco(frame)
    cv2.imshow("Video con aruco", image_with_aruco_marker)

    # Rompe el bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite(img_path, frame)
        break

# Libera la cámara y cierra la ventana
cap.release()
cv2.destroyAllWindows()
