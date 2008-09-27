from controller import Controller
from random import randint
from constants import *

class Dirtyh(Controller):
    """
    See http://blizzard.rwic.und.edu/~nordlie/robotics/crob/DIRTYH.R.txt
    """
    def __init__(self):
        Controller.__init__(self)

    def execute(self):
        self.dam = self.damage()
        while True:
            self.current = self.damage()
            if self.current > self.dam:
                self.move()
                self.dam = self.damage()
            else:
                self.rapid()
    
    def move(self):
        
        x = self.x_loc()
        y = self.y_loc()
        
        think = 0
        if ( x < 5000) and (y < 5000):
            self.drive(randint(0, 90), 100)
            while(think < 50):
                think += 1
                self.wait()
                
        elif (x < 5000) and (y > 4990):
            self.drive(randint(0, 90) + 270, 100)
            while(think < 50):
                think += 1
                self.wait()
                
        elif (x > 4990) and (y < 5000):
            self.drive(randint(0, 90) + 90, 100)
            while(think < 50):
                think += 1
                self.wait()
                
        elif (x > 499) and (y > 4990):
            self.drive(randint(0, 90) + 180, 100)
            while(think < 50):
                think += 1
                self.wait()
        
        self.drive(0, 0)
        
    def rapid(self):
        
        distance = 0
        dam2 = self.damage()
        bordum = 0
        while True:
            if bordum > 10:
                bordum = 0
                self.move()
                
            if distance < 40:
                heading = randint(0, 359)
            else:
                bordum += 1
                self.shoot(heading, distance)
            
            distance = self.scan(heading, 5)
            while(not distance):
                heading += 5
                
                if(heading > 360):
                    heading -= 360
                current2 = self.damage()
                
                if dam2 != current2:
                    self.move()
                    return
                    
                bordum += 1
                distance = self.scan(heading, 5)
                

        current2 = self.damage()
        if(dam2 != current2):
            self.move()
            return