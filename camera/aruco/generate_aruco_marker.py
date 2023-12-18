import cv2
import numpy as np

# Ruta donde se guardará el archivo PDF
ruta_pdf = "/Users/alonsodicandia/asesorias/clbb-io/camera/images/aruco_marker/"


def generate_bulk_markers(aruco_dict):
   marker_size = int(input("Enter the marker size: "))
   num_markers = int(input("Enter the number of markers to generate: "))

   for marker_id in range(num_markers):
       marker_img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)

       cv2.imwrite("{}marker_{}.png".format(ruta_pdf, marker_id), marker_img)


def main():
   aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
   generate_bulk_markers(aruco_dict)


if __name__ == "__main__":
   main()
