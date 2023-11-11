import cv2

def listar_camaras():
    # Itera sobre las cámaras desde 0 hasta un número arbitrario
    for i in range(10):
        # Intenta abrir la cámara
        cap = cv2.VideoCapture(i)
        
        # Verifica si la cámara se abrió correctamente
        if cap.isOpened():
            print(f"Cámara {i}: Disponible")
            cap.release()
        else:
            print(f"Cámara {i}: No disponible")

if __name__ == "__main__":
    listar_camaras()
