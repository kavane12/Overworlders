# Various helper function used by multiple AI types

import math

# Convert radians to degrees
def deg(angle):
    return angle * 180 / math.pi

# Convert degrees to radians
def rad(angle):
    return angle * math.pi / 180

# Converts an angle to a value between -180 and 180 degrees
def angleMod(angle):    
    angle %= 360
    if angle > 180:
        angle -= 360
    return angle

# Finds relative angle to object given distances
# Returns result in radians
def relativeAngle(dx, dz):
    return -math.atan2(dx, dz)

# Finds relative distance to object given distances
def relativeDistance(dx, dz):
    return math.sqrt(dx**2 + dz**2)