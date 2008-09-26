from greenlet import greenlet
from constants import *


class Controller:
    SHOOT = 1
    SCAN  = 2
    DRIVE = 3
    WAIT  = 4
    def __init__(self):
        pass
        
    def shoot(self, direction, distance):
        return self.main_greenlet.switch( [self.SHOOT, [direction, distance]] )

    def scan(self, direction, spread):
        return self.main_greenlet.switch( [self.SCAN, [direction, spread]] )

    def drive(self, direction, speed):
        return self.main_greenlet.switch( [self.DRIVE, [direction, speed]] )

    def wait(self):
        return self.main_greenlet.switch( [self.WAIT] )

    def status(self):
        return status

    def init(self, dummy):
        """Called by simulator. Do not use!"""
        self.execute()
        
    def execute(self):
        """Entry point of controller. Override this in subclass."""
        pass


class Shooter(Controller):
    def execute(self):
        while True:
            self.shoot(rand_int(0,360) , rand_int(100, 5000) )
        
class Driver(Controller):
    def execute(self):
        while True:
            self.drive(rand_int(0, 360), rand_int(MAX_BACKWARD_SPEED, MAX_FORWARD_SPEED))
            self.shoot(rand_int(0,360) , rand_int(100, 5000) )