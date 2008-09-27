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

    def collides_with_wall(self):
        """
        Returns true if current object collides with walls. Takes object's radius in consideration.
        """
        x = location[0]
        if x < self.radius or x > (ARENA_MAX_WIDTH - self.radius):
            return True
        y = location[1]
        if y < self.radius or y > (ARENA_MAX_LENGTH - self.radius):
            return True
        return False


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

    def can_shoot(self):
        """
        Returns true if robot can shoot
        """
        return self.shells_in_air <= MAX_SHELLS_IN_AIR

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
            # TODO turn at no more than MAX_DIRECTION_CHANGE degrees
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
        if self.speed != self.target_speed:
            pass
            #print (speed_diff, self.speed, self.target_speed, self.name, direction_diff) 
            
    
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


