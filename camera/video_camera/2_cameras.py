import cv2

def capture_images(camera_indexes):
    # Abre las cámaras
    cap1 = cv2.VideoCapture(camera_indexes[0])
    cap2 = cv2.VideoCapture(camera_indexes[1])

    if not cap1.isOpened() or not cap2.isOpened():
        print("Error opening one or more cameras")
        return

    while True:
        # Captura frames de ambas cámaras
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            print("Error reading frames from one or more cameras")
            break

        # Procesa los frames aquí según tus necesidades
        # ...

        concatenated_frame = cv2.hconcat([frame1, frame2])

        # Muestra el frame concatenado
        cv2.imshow("Concatenated Frames", concatenated_frame)

        if cv2.waitKey(30) == 27:
            break  # Presiona 'Esc' para salir

    # Libera los recursos al finalizar
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Especifica los índices de las cámaras
    camera_indexes = [0, 1]  # Puedes ajustar estos valores según las cámaras que estés utilizando

    # Inicia la captura de imágenes
    capture_images(camera_indexes)
