import math


def get_distance(x1: float, y1: float, x2: float, y2: float):
    x = x1 - x2
    y = y1 - y2
    return math.sqrt(x * x + y * y)
