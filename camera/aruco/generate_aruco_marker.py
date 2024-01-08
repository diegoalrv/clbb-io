import cv2
import numpy as np
import os

# Ruta donde se guardará el archivo PDF
ruta_pdf = "./images"

def create_output_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Folder '{path}' created.")
    else:
        print(f"Folder '{path}' already exists.")

def generate_bulk_markers(aruco_dict):

   create_output_folder(ruta_pdf)

   marker_size = int(input("Enter the marker size: "))
   num_markers = int(input("Enter the number of markers to generate: "))

   for marker_id in range(num_markers):
       marker_img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)

       cv2.imwrite("{}/marker_{}.png".format(ruta_pdf, marker_id), marker_img)

def main():
   aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
   generate_bulk_markers(aruco_dict)

if __name__ == "__main__":
   main()
