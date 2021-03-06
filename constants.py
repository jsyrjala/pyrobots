from math import sqrt, pi, cos, sin, floor, radians, degrees, atan, atan2, fabs
from random import randint

ARENA_MAX_WIDTH = 10000
ARENA_MAX_LENGTH = 10000
# per time unit
MAX_FORWARD_SPEED = 100
# per time unit
MAX_BACKWARD_SPEED = -75
# max speed when turning allowed
MAX_TURN_SPEED = 50

MAX_CANNON_RANGE = 7000

# speed change per time unit^2
MAX_ACCELERATION = 20

# degrees per timeunit
# normal value 15, set this to 360 to get instant turns
MAX_DIRECTION_CHANGE = 360 #15 
# cannon shell speed per timeunit
SHELL_SPEED = 1000

# number of shells in air per player (default 3)
MAX_SHELLS_IN_AIR = 1

# max scan resolution +-
MAX_SCAN_SPREAD = 10

# max damage that a robot can sustain
MAX_DAMAGE = 100

# relative_speed divisor for collision with robot
ROBOT_COLLISION_DAMAGE_DIVISOR = 25.0
# relative_speed divisor for collision with wall
WALL_COLLISION_DAMAGE_DIVISOR = 25.0

# robot size
ROBOT_RADIUS = 100
SHELL_RADIUS = 1

BLAST_MAX_DAMAGE_RADIUS = 50
BLAST_MEDIUM_DAMAGE_RADIUS = 100
BLAST_LIGHT_DAMAGE_RADIUS = 200
BLAST_MIN_DAMAGE_RADIUS = 400

BLAST_MAX_DAMAGE = 8
BLAST_MEDIUM_DAMAGE = 4
BLAST_LIGHT_DAMAGE = 2
BLAST_MIN_DAMAGE = 1

BLAST_DAMAGE = (
				(BLAST_MIN_DAMAGE_RADIUS, BLAST_MIN_DAMAGE),
				(BLAST_LIGHT_DAMAGE_RADIUS, BLAST_LIGHT_DAMAGE),
				(BLAST_MEDIUM_DAMAGE_RADIUS, BLAST_MEDIUM_DAMAGE),
                (BLAST_MAX_DAMAGE_RADIUS, BLAST_MAX_DAMAGE),
                )

import logging
logging.basicConfig(level=logging.INFO,
					format='%(levelname)-8s %(name)-6s: %(message)s')

def vector(base_location, direction, distance):
	rads = radians(direction)
	x_diff = cos(rads) * distance
	y_diff = sin(rads) * distance
	return [ round(base_location[0] + x_diff), round(base_location[1] + y_diff) ]

def round(value):
	return int(value + 0.5)

def rand_int(min, max):
	return randint(min, max)

def direction(location, target):
	"""
	Returns direction (in float degrees) from location to target.
	"""
	
	vector = [target[0] - location[0], target[1] - location[1]]
	return direction_of_vector(vector)

def angle_difference(direction, target_direction):
    """
Computes amount of degrees that is needed to add direction to get target_direction.

>>> angle_difference(10, 10)
0
>>> angle_difference(1, 10)
9
>>> angle_difference(0, 90)
90
>>> angle_difference(90, 0)
-90
>>> angle_difference(19, 5)
-14
>>> angle_difference(1,359)
-2
>>> angle_difference(350, 10)
20
    """
    diff = target_direction - direction
    norm = fabs(diff)
    low = fabs(diff - 360)
    high = fabs(diff + 360)

    if norm < low and norm < high:
        return diff
    if low < norm and low < high:
        return diff -360
    return diff + 360

def direction_of_vector(vector):
    x = vector[0]
    y = vector[1]
    return degrees(atan2(y, x))

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
