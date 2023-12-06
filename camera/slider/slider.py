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

    def subdividir_recta(self, point1, point2, num_divisiones=4):
        def obtener_menor_punto(tupla1, tupla2):
            # x = min([tupla1, tupla2], key=lambda punto: punto[0])
            # y = min([tupla1, tupla2], key=lambda punto: punto[1])

            x1, y1 = tupla1
            x2, y2 = tupla2

            xr, yr = None, None

            if x1 < x2:
                xr = x1
                yr = y1
            elif x2 < x1:
                xr = x2
                yr = y2
            else:
                xr = x1
                yr = y1
                
            return xr, yr
        
        def make_int_tuple(t):
            return (int(t[0]), int(t[1]))

        # Calcular el point medio de la recta
        middle_point = ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)

        # print(point1, point2)
        work_point = obtener_menor_punto(point1, point2)

        direction = 1

        if work_point == point1:
            if work_point[1] > point2[1]:
                direction = -1
        elif work_point == point2:
            if work_point[1] > point1[1]:
                direction = -1

        division_factor = 2 * num_divisiones

        points = []
        for i in range(1, division_factor+1, 2):
            x = work_point[0] + (i * abs(work_point[0] - middle_point[0]) / num_divisiones)
            y = work_point[1] + (direction * i * abs(work_point[1] - middle_point[1]) / num_divisiones)
            points.append(make_int_tuple((x, y)))
        return points
    
    def calcular_distancia(self, punto1):
        punto2 = self.center_one_aruco
        
        x1, y1 = punto1
        x2, y2 = punto2

        distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distancia

