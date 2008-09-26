from math import sqrt, pi, cos, sin, floor, radians
from random import randint

ARENA_MAX_WIDTH = 10000
ARENA_MAX_LENGTH = 10000
# per time unit
MAX_FORWARD_SPEED = 100
# per time unit
MAX_BACKWARD_SPEED = -75
# max speed when turning allowed
MAX_TURN_SPEED = 50

# speed change per time unit^2
MAX_ACCELERATION = 20

# per timeunit
MAX_DIRECTION_CHANGE = 15 
# per timeunit
SHELL_SPEED = 1000

#
MAX_SHELLS_IN_AIR = 3

#
MAX_SCAN_SPREAD = 10

MAX_HEALTH = 100

# relative_speed divisor for collision with robot
robot_collision_damage_divisor = 25
# relative_speed divisor for collision with wall
wall_collision_damage_divisor = 25

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

BLAST_DAMAGE = ((BLAST_MAX_DAMAGE_RADIUS, BLAST_MAX_DAMAGE),
				(BLAST_MEDIUM_DAMAGE_RADIUS, BLAST_MEDIUM_DAMAGE),
				(BLAST_LIGHT_DAMAGE_RADIUS, BLAST_LIGHT_DAMAGE),
				(BLAST_MIN_DAMAGE_RADIUS, BLAST_MIN_DAMAGE))

import logging
logging.basicConfig(level=logging.DEBUG,
					format='%(levelname)-8s %(name)-6s: %(message)s')

def vector(base_location, direction, distance):
	rads = radians(direction)
	x_diff = sin(rads) * distance
	y_diff = cos(rads) * distance
	return [ round(base_location[0] + x_diff), round(base_location[1] + y_diff) ]

def round(value):
	return int(value + 0.5)

#def degrees_to_radians(degrees):
#	return degrees/180.0*pi

def rand_int(min, max):
	return randint(min, max)
