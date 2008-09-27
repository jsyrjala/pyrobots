from controller import Controller
from constants import *

class Cspotrun(Controller):
    # Originally by Andres Nelson
    # http://blizzard.rwic.und.edu/~nordlie/robotics/crob/CSPOTRUN.R.txt
    def __init__(self):
        Controller.__init__(self)
        
    def execute(self):
        heading = 0
        direction = 90
        
        while True:
            self.drive(direction, MAX_FORWARD_SPEED)
            
            if( (heading == 0 and self.y_loc() > 5750) or
                (heading == 1 and self.x_loc() < 1500) or
                (heading == 2 and self.y_loc() < 4250) or
                (heading == 3 and self.x_loc() > 8500)):
                self.drive(direction, 50)
                heading = (heading + 1) % 4
                direction += 90
                
            else:
                for dir in xrange(0, 360, 30):
                    distance = self.scan(dir, 10)
                    if(distance):
                        self.shoot(dir, distance)
                        break;
                
        