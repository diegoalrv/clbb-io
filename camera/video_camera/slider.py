import math
from utils import up_right_point, up_left_point

class Slider:
    def __init__(self):
        self._left_point = (None, None)
        self._right_point = (None, None)

        # reference to a center of the just one aruco marker, reference to the slider aruco
        self.center = None

        self.delta_x = None
        self.delta_y = None
        self.angle = None

    @property
    def center_one_aruco(self):
        return self.center

    @property
    def slider_line(self):
        return (self._left_point, self._right_point)

    @center_one_aruco.setter
    def center_one_aruco(self, point: tuple):
        self.center = point

    @slider_line.setter
    def slider_line(self, two_points: tuple):
        left = two_points[0]
        right = two_points[1]
        self._left_point = left
        self._right_point = right
    
    def process_upper_corners_to_get_inclination(self, corner):
        up_left = up_left_point(corner)
        up_right = up_right_point(corner)

        y1, x1 = up_left
        y2, x2 = up_right

        # Calcular la diferencia en y y la diferencia en x
        delta_y = y2 - y1
        delta_x = x2 - x1

        self.delta_x = delta_x
        self.delta_y = delta_y

        # Calcular el ángulo de inclinación en radianes
        angulo_radianes = math.atan2(delta_y, delta_x)

        # # Convertir el ángulo a grados
        # angulo_grados = math.degrees(angulo_radianes)

        self.angle = angulo_radianes
    
    def obtain_new_point(self, third_point):
        # Calcular el ángulo de inclinación en radianes
        angulo_radianes = self.angle

        # Calcular el desplazamiento en y basado en el ángulo y la diferencia en x
        desplazamiento_y = self.delta_x * math.tan(angulo_radianes)

        # Calcular el nuevo punto en la recta utilizando el tercer punto
        nuevo_x = int(third_point[1] + self.delta_x)
        nuevo_y = int(third_point[0] + desplazamiento_y)

        return nuevo_y, nuevo_x

    def subdividir_recta(self, point1, point2):
        def obtener_menor_tupla(tupla1, tupla2):
            x1, y1 = tupla1
            x2, y2 = tupla2

            if y1 < y2 and x1 < x2:
                return tupla1, tupla2
            else:
                return tupla2, tupla1
            
        def make_int_tuple(t):
            return (int(t[0]), int(t[1]))
            
        point1, point2 = obtener_menor_tupla(point1, point2)
        print(point1, point2)

        # Calcular el point medio de la recta
        middle_point = ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)
        print(f"middle: {middle_point}")

        # Calcular dos points adicionales equidistantes
        first_point = ((point1[0] + (abs(point1[0] - middle_point[0]) / 4)),(point1[1] + (abs(point1[1] - middle_point[1]) / 4)))
        second_poitn = ((point1[0] + (3 * abs(point1[0] - middle_point[0]) / 4)),(point1[1] + (3 * abs(point1[1] - middle_point[1]) / 4)))
        third_point = ((point1[0] + (5 * abs(point1[0] - middle_point[0]) / 4)),(point1[1] + (5 * abs(point1[1] - middle_point[1]) / 4)))
        fourth_point = ((point1[0] + (7 * abs(point1[0] - middle_point[0]) / 4)),(point1[1] + (7 * abs(point1[1] - middle_point[1]) / 4)))

        return make_int_tuple(first_point), make_int_tuple(second_poitn), make_int_tuple(third_point), make_int_tuple(fourth_point)

