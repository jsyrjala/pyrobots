from controller import *
from random import *
from math import *

class Tracker(Controller):
    BORDER = 2000
    def __init__(self):
        Controller.__init__(self)
        self.logger = logging.getLogger('Tracker')
    
    def cannon(self, direction, distance):
        if distance > 200 and distance <= 7000:
            self.shoot(direction, distance)
    
    def execute(self):
        # current scan direction
        scan_dir = 0
        # current direction
        dir = 90
        # range to enemy
        range = 0
        # fix on opponent from the last scan
        hadfix = False
        
        # start moving immediately
        self.drive(dir, 50)
        
        while True:
            tdir = dir
            location, health, speed, direction = self.status()
            cx, cy = location
            
            if cx > 10000 - self.BORDER:
                if cy < 10000 - self.BORDER:
                    # near east wall
                    tdir = 90
                else:
                    # near northeast corner
                    tdir = 180
            elif cx < self.BORDER:
                if cy < self.BORDER:
                    # near southwest corner
                    tdir = 0
                else:
                    # near west wall
                    tdir = 270
            elif cy > 10000 - self.BORDER:
                # near north wall
                tdir = 180
            elif cy < self.BORDER:
                # near south wall
                tdir = 0
            
            if not speed or dir != tdir:
                dir = tdir
                self.drive(dir, 50)

            range = self.scan(scan_dir, 10)
            if range:
                self.cannon(scan_dir, range)
                hadfix = True
            elif hadfix:
                scan_dir += 40
                hadfix = False
            else: 
                scan_dir -= 20

# TODO
 #                 // if speed() == 0,    restart the drive unit...
 #     // if dir != tdir,     we need to change direction...
 #     if (!speed() || dir != tdir)
 #        drive(dir=tdir,100);

#      if ((range=scan(sdir,10))) {   // scan for a target...
#         shoot(sdir,range);          //   got one.  shoot it!
#        hadfix=1;                   //   remember we saw a target
#      }
#      else if (hadfix) {             //   did we lose a target?
#         sdir += 40;                 //        back up the scan
#         hadfix=0;                   //        forget we had a target
#      }
#      else
#         sdir -= 20;                 //   increment the scan

            