from controller import *
from random import *
from math import *

class Cylon(Controller):

    def __init__(self):
        Controller.__init__(self)
        self.logger = logging.getLogger('Cylon')
        
    def execute(self):
        while True:
            self.goto(randint(500, 9000), randint(500, 9000))
            
    def goto(self, x, y):
        status = self.get_status()
        
        location, health, speed, direction = self.get_status()
        dir = int(degrees(atan2(y - location[1], x - location[0]))) % 360
        
        orig_dist = hypot(x - location[0], y - location[1]);

        sc = 0;
        sd = 1;
        SPEED = 49
        self.drive(dir, SPEED);
        location, health, speed, direction = self.get_status()
        
        
        dist = hypot(x - location[0], y - location[1]);
        while fabs(speed) > 0 and dist > 200 :
            location, health, speed, direction = self.get_status()
            dist = hypot(x - location[0], y - location[1]);
                        
            if fabs(sc) == 45:
                sd *= -1
            sc += 3*sd
            range = self.scan(dir + sc, 5)
            location, health, speed, direction = self.get_status()
            
            if range > 200 and range < 7000:
                self.shoot(dir + sc, range)
                
            # point robot towards target if needed
            location, health, speed, direction = self.get_status()
            tdir = int(degrees(atan2(y - location[1], x - location[0]))) % 360
            
            if tdir != dir:
                dir = tdir
                self.drive(dir, SPEED)
    
        # stop robot
        self.drive(dir, 0)
        
        while fabs(speed) > 0:
            location, health, speed, direction = self.get_status()
            self.wait()
