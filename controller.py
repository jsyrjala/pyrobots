from greenlet import greenlet
from constants import *


class Controller:
    """
    Controller is a base class for robot controllers. It is designed for subclassing.
    """
    SHOOT = 1
    SCAN  = 2
    DRIVE = 3
    WAIT  = 4

    def __init__(self):
        self.__status__ = None

    def __init_event_loop__(self, status):
        """Called by simulator. Do not use!"""
        self.__status__ = status.pop(0)
        self.execute()

    def __set_status__(self, results):
        self.__status__ = results.pop(0)
        return results

    def shoot(self, direction, distance):
        """
        Shoots the cannon to given direction and distance.
        There may be up to 3 cannon shells in the air at same time.
        Return True, if shooting was succesful, False otherwise.
        
        direction is in degrees, distance is in pixels (integers only).
        
        TODO speed affects accuracy?
        """
        results = self.main_greenlet.switch( [self.SHOOT, [direction, distance]] )
        return self.__set_status__(results)

    def scan(self, direction, spread):
        """
        Scans an arc from direction-spread to direction+spread looking for other robots.
        If robot is found within scanning arc, distance to nearest robot is returned.
        If no robots are found, None is returned.
        Spreads larger than MAX_SCAN_SPREAD are truncated.
        
        direction and spread are in degrees (integers only).
        """
        results = self.main_greenlet.switch( [self.SCAN, [direction, spread]] )
        return self.__set_status__(results)

    def drive(self, direction, speed):
        """
        Changes direction and speed of the robot. Robot will continue moving until collision or new drive command.
        Maximum forward speed is MAX_FORWARD_SPEED pixels/time-unit.
        Maximum backward speed is MAX_BACKWARD_SPEED pixels/time-unit.
        Maximum acceleration is MAX_ACCELERATION pixels/time-unit^2.
        Maximum speed where turning is allowed is MAX_TURN_SPEED pixels/time-unit. 
        If speed is too high for turning, robot will slow down, turn and go back to its target speed.
        
        Returns True if direction was changed, False if direction was not changed due to high speed.
        
        direction is in degrees, speed is in pixels/time-unit (integers only).
        """
        results = self.main_greenlet.switch( [self.DRIVE, [direction, speed]] )
        return self.__set_status__(results)

    def wait(self):
        """
        Skips a turn.
        """
        results = self.main_greenlet.switch( [self.WAIT] )
        return self.__set_status__(results)

    def status(self):
        """
        Returns current status of robot in format
        [[x_coordinate, y_coordinate], health, speed, direction]
        """
        return self.__status__

    def speed(self):
        """
        Returns current speed of the robot. Speed may not always be same as in last drive() 
        command because of acceleration and collisions.
        """
        return self.__status__[2]

    def direction(self):
        """
        Returns current direction of robot in degrees. Direction may not always be same as in last drive() 
        command because of turning speed.
        """
        return self.__status__[3]
    
    def location(self):
        """
        Returns robot's current location as [x, y].
        """
        return self.__status__[0]

    def x_loc(self):
        """
        Returns current x coordinate of the robot.
        """
        return self.__status__[0][0]

    def y_loc(self):
        """
        Returns current y coordinate of the robot.
        """
        return self.__status__[0][1]

    def damage(self):
        """
        Returns current damage of the robot. 0 = no damage, 100 = destroyed.
        """
        return self.__status__[1]
        
    def execute(self):
        """
        Entry point of controller. Override this in subclass. 
        Do not exit or throw execptions from this method, since that counts as surrender ;-) 
        Make an infinite loop and call methods provided by this class.
        
        Calling shoot, drive, scan or wait finishes turn for current timeslice. Calling status does not affect timeslice.
        """
        
        # default behaviour is do nothing
        while True:
            self.wait()
