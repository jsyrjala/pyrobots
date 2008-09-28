import logging

from constants import *

import math

class Object:
    """
    Base class for objects
    """
    def __init__(self, location):
        self.direction = 0
        self.location = location
        self.radius = 0

    def collides_with_walls(self):
        """
        Returns list of walls if current object collides with walls. Takes object's radius in consideration.
        1 = north wall, 2 = east wall, 3 = south wall, 4 = west wall.
        For exaple [1,2] => collides with both eats and north walls (is in ne corner)
        """
        walls = []
        x = self.location[0]
        y = self.location[1]
        if x < self.radius:
            walls.append(4)
        if x > (ARENA_MAX_WIDTH - self.radius):
            walls.append(2)
        if y < self.radius:
            walls.append(1)
        if y > (ARENA_MAX_LENGTH - self.radius):
            walls.append(3)
        return walls;


    def distance_to(self, location):
        """
        Returns distance to location.
        """
        x_diff = (self.location[0] - location[0])
        y_diff = (self.location[1] - location[1])
        return sqrt(x_diff * x_diff + y_diff * y_diff)

    def collides(self, object):
        return self.distance_to(object.location) < (self.radius + object.radius)

    def move(self):
        """Moves object."""
        if self.speed == 0:
            return
        self.location = vector(self.location, self.direction, self.speed)
        self.logger.debug("Move to " + str(self.location) )


class Shell(Object):
    """
    Class for cannon shells.
    """
    def __init__(self, shooter, location, direction, target ):
        Object.__init__(self,location)
        self.logger = logging.getLogger('SHELL')
        self.logger.debug ("Shell initialized at " + str(location))
        self.target = target
        self.direction = direction
        self.speed = SHELL_SPEED
        self.radius = SHELL_RADIUS
        self.shooter = shooter
        self.exploded = False

    def move(self):
        """
        Moves bullet. Returns true when the shell hit the ground.
        """
        if self.distance_to(self.target) < self.speed:
            self.location = self.target
            return True
        Object.move(self)
        return False

    def explode(self):
        """
        Called when shell explodes.
        """
        self.exploded = True
        self.shooter.shells_in_air -= 1

class Robot(Object):
    def __init__(self, location, name):
        Object.__init__(self, location)

        self.name = name
        self.speed = 0
        self.radius = ROBOT_RADIUS

        self.shells_in_air = 0
        self.target_direction = 0
        self.target_speed = 0
        self.damage = 0

        self.logger = logging.getLogger('ROBOT')
        self.logger.debug("Robot " + name + " initialized at " + str(location))
        self.scan_order = None
    def can_shoot(self):
        """
        Returns true if robot can shoot
        """
        return self.shells_in_air < MAX_SHELLS_IN_AIR

    def can_turn(self):
        """Returns true if robot can turn at current speed."""
        return math.fabs(self.speed) <= MAX_TURN_SPEED

    def shoot(self, direction, distance):
        if distance > MAX_CANNON_RANGE:
            distance = MAX_CANNON_RANGE
        if distance < 0:
            distance = 0
        distance = int(distance + 0.5)
        direction = int(direction + 0.5) % 360
        
        target = vector(self.location, direction, distance)
        self.shells_in_air += 1
        return Shell(self, [self.location[0], self.location[1]], direction, target)

    def drive(self, direction, speed):
        """
        Sets target values for robot's drive. Note changes in speed and direction are not instantenous, but they take some time.
        """
        if speed < MAX_BACKWARD_SPEED:
            speed = MAX_BACKWARD_SPEED
        if speed > MAX_FORWARD_SPEED:
            speed = MAX_BACKWARD_SPEED
        
        speed = int(speed + 0.5)
        direction = int(direction + 0.5) % 360
        self.target_speed = speed
        self.target_direction = direction
        
        direction_changed = False
        if not self.can_turn():
            # can't turn now, going too fast
            pass
        elif self.direction == self.target_direction:
            # already going to correct direction
            pass
        else:
            # change self.direction towards target_direction
            # TODO this should be true only if actual direction changes
            direction_changed = True
            pass
            
        return direction_changed
        
    def move(self):
        right_direction = False
        
        # speed requested, or needed for turning
        needed_speed = self.target_speed
        
        direction_diff = 0
        if self.direction == self.target_direction:
            # no need to turn
            pass
        elif self.can_turn():
            # change self.direction towards target_direction
            angle_diff = angle_difference(self.direction, self.target_direction)
            
            if angle_diff < -MAX_DIRECTION_CHANGE:
                angle_diff = -MAX_DIRECTION_CHANGE
            if angle_diff > MAX_DIRECTION_CHANGE:
                angle_diff = MAX_DIRECTION_CHANGE
                
            self.direction = int(self.direction + angle_diff) % 360
        else:
            # need to turn but going too fast => slow down
            needed_speed = MAX_TURN_SPEED
        
        speed_diff = needed_speed - self.speed
        
        if math.fabs(speed_diff) > MAX_ACCELERATION:
            if speed_diff < 0:
                speed_diff = -MAX_ACCELERATION
            elif speed_diff > 0:
                speed_diff = MAX_ACCELERATION
            
        # change self.speed towards target_speed
        # TODO accelerate/brake no more than MAX_ACCELERATION
        self.speed += speed_diff
        Object.move(self)

        self.handle_collisions()
    
    def handle_collisions(self):
        # check collisions with walls
        walls = self.collides_with_walls()
        if walls:
            collision_damage = int((self.speed / WALL_COLLISION_DAMAGE_DIVISOR  ) + 0.5)
            self.damage += collision_damage
            self.speed = 0
            self.target_speed = 0
            if 1 in walls:
                self.location[1] = 0 + self.radius + 1
            if 2 in walls:
                self.location[0] = ARENA_MAX_WIDTH - self.radius - 1
            if 3 in walls:
                self.location[1] = ARENA_MAX_LENGTH - self.radius - 1
            if 4 in walls:
                self.location[0] = 0 + self.radius + 1
                
    
    def status(self):
        """
        Returns robots status.
        [[x_coordinate, y_coordinate], damage, speed, direction]
        """
        return [[self.location[0], self.location[1]], self.damage, self.speed, self.direction]
        
if __name__ == '__main__':
    r = Robot([1000,1000], 'doo')

    s=r.shoot(200, 4000)

    s.move()
    s.move()
    s.move()
    s.move()
    s.move()
    s.move()
    s.move()
    s.move()
    s.move()


