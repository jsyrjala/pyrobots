from controller import Controller
from random import randint
from constants import *

class Nord(Controller):
    """
    See http://blizzard.rwic.und.edu/~nordlie/robotics/crob/NORD.R.txt
    
    Goes to random direction until collides with something or gets hit by a shell. 
    Then goes to random direction, away from walls.
    """
    def __init__(self):
        Controller.__init__(self)
        

    def execute(self):
        dam = 0
        while True:
            dir = self.pick_rnd()
            self.drive(dir, 49)
            angle = 0
            while angle < 358:
                distance = self.scan(angle, 1)
                if 400 < distance:
                    self.shoot(angle, distance)
                    angle -= 2
                if dam != self.damage():
                    dir = self.pick_rnd()
                    self.drive(dir, 49)
                    dam = self.damage()
                angle += 1
                
    def pick_rnd(self):
        flag = 1
        while flag == 1:
            rand = randint(0,359)
            if( ((  90 < rand < 270) and (self.x_loc() < 1000)) or
                ((   0 < rand < 180) and (self.y_loc() > 9000)) or
                (( 180 < rand < 360) and (self.y_loc() < 1000)) or
                ((   0 < rand <  90) and (self.x_loc() > 9000)) or
                (( 270 < rand < 360) and (self.x_loc() > 9000)) ) :
                pass
            else:
                flag = 0
        return rand
