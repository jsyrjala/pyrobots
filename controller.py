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
        self.logger = logging.getLogger('CTRL')
        self.status = None

    def __init_event_loop__(self, status):
        """Called by simulator. Do not use!"""
        self.logger.debug("initializing")
        self.status = status.pop(0)
        self.execute()
        self.logger.debug("finished")
        
        
    def __set_status__(self, results):
        self.status = results.pop(0)
        return results

    def shoot(self, direction, distance):
        """
        Shoots the cannon to given direction and distance.
        There may be up to 3 cannon shells in the air at same time.
        Return True, if shooting was succesful, false otherwise.
        
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
        
        direction is in degrees, speed is in pixels/time-unit (integers only).
        """
        results = self.main_greenlet.switch( [self.DRIVE, [direction, speed]] )
        return self.__set_status__(results)

    def wait(self):
        """
        Skips turn.
        """
        results = self.main_greenlet.switch( [self.WAIT] )
        return self.__set_status__(results)

    def get_status(self):
        """
        Returns current status of robot
        [[x_coordinate, y_coordinate], health, speed, direction]
        """
        return self.status

        
    def execute(self):
        """
        Entry point of controller. Override this in subclass. 
        Do not exit from this method, since it counts as surrender ;-) 
        Make an infinite loop and call methods provided by this class.
        
        Calling shoot, drive, scan or wait finishes turn for current timeslice. Calling status does not affect timeslice.
        """
        
        # default behaviour is do nothing
        while True:
            self.wait()


class Shooter(Controller):
    def execute(self):
        while True:
            self.shoot(rand_int(0,360) , rand_int(100, 5000) )
        
class Driver(Controller):
    def execute(self):
        while True:
            self.drive(0, 10)
            
            location, health, speed, direction = self.get_status()
