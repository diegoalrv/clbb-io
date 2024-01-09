import cv2
import cv2.aruco as aruco
import numpy as np

def detectar_aruco(imagen_path):
    # Cargar la imagen
    if type(imagen_path) is str:
        imagen = cv2.imread(imagen_path)
    else:
        imagen = imagen_path
    
    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Configurar el diccionario de marcadores ArUco
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

    # Detectar marcadores ArUco en la imagen
    corners, ids, rejectedImgPoints = aruco.detectMarkers(imagen_gris, aruco_dict)

    # Dibujar los marcadores detectados
    imagen_resultado = imagen.copy()
    if ids is not None:
        aruco.drawDetectedMarkers(imagen_resultado, corners, ids)
    
    if ids is not None:
        ids = list(map(lambda sublist: sublist[0], ids))

    return imagen_resultado, corners, ids

if __name__ == "__main__":
    imagen_path = "./camera/images/capture/imagen.jpg"  # Reemplaza con la ruta de tu imagen
    imagen_resultado, _ = detectar_aruco(imagen_path)
    # Mostrar la imagen con los marcadores detectados
    cv2.imshow('Marcadores ArUco Detectados', imagen_resultado)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
