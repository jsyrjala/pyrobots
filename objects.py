import logging

from constants import *

import math

class Object:
    def __init__(self, location):
        self.direction = 0
        self.location = location

    def collides_with_wall(self):
        x = location[0]
        if x < self.radius or x > (ARENA_MAX_WIDTH - self.radius):
            return True
        y = location[1]
        if y < self.radius or y > (ARENA_MAX_LENGTH - self.radius):
            return True
        return False


    def distance_to(self, location):
        x_diff = (self.location[0] - location[0])
        y_diff = (self.location[1] - location[1])
        return sqrt(x_diff * x_diff + y_diff * y_diff)

    def collides(self, object):
        return self.distance_to(object.location) < (self.radius + object.radius)

    def move(self):
        """Moves object. Returns true if target found"""
        if self.speed == 0:
            return False
        self.location = vector(self.location, self.direction, self.speed)
        self.logger.debug("Move to " + str(self.location) )
        return False




class Shell(Object):
    def __init__(self, shooter, location, direction, target ):
        Object.__init__(self,location)
        self.logger = logging.getLogger('SHELL')
        self.logger.debug ("Shell initialized at " + str(location))
        self.target = target
        self.direction = direction
        self.speed = SHELL_SPEED
        self.radius = SHELL_RADIUS
        self.shooter = shooter

    def move(self):
        if self.distance_to(self.target) < self.speed:
            self.location = self.target
            return True
        Object.move(self)
        return False

    def explode(self):
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
        self.health = MAX_HEALTH

        self.logger = logging.getLogger('ROBOT')
        self.logger.debug("Robot " + name + " initialized at " + str(location))

    def can_shoot(self):
        """
        Returns true if robot can shoot
        """
        return self.shells_in_air <= MAX_SHELLS_IN_AIR

    def can_turn(self):
        """Returns true if robot can turn at current speed"""
        return math.fabs(self.speed) <= MAX_TURN_SPEED

    def shoot(self, direction, distance):
        target = vector(self.location, direction, distance)
        self.shells_in_air += 1
        return Shell(self, [self.location[0], self.location[1]], direction, target)

    def drive(self, direction, speed):
        if speed < MAX_BACKWARD_SPEED:
            speed = MAX_BACKWARD_SPEED
        if speed > MAX_FORWARD_SPEED:
            speed = MAX_BACKWARD_SPEED
        
        direction = direction % 360
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
            # TODO turn at no more than MAX_DIRECTION_CHANGE degrees
            direction_changed = True
            pass
        return direction_changed
        
    def move(self):
        if not self.can_turn():
            # can't turn now, going too fast
            pass
        else:
            # change self.direction towards target_direction
            # TODO turn at no more than MAX_DIRECTION_CHANGE degrees
            self.direction = self.target_direction
            pass
        
        # change self.speed towards target_speed
        # TODO accelerate/brake no more than MAX_ACCELERATION
        self.speed = self.target_speed
        Object.move(self)
        
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


