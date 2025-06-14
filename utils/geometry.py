import math

def find_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def find_angle(x1, y1, x2, y2):
    try:
        theta = math.acos((y2 - y1) * (-y1) / (math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * y1))
        return int(180 / math.pi * theta)
    except:
        return 90  # Default to 90 if division by zero or domain error
