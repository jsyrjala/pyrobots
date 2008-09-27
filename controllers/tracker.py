from controller import *
from random import *
from math import *

class Tracker(Controller):
    """
    Taken from c++robots.
    
    Robot drives rectangular path about 2000 units from arena walls as fast as possible and scans for targets.
    """
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
        SPEED = MAX_FORWARD_SPEED
        self.drive(dir, SPEED)
        
        while True:
            tdir = dir
            location, damage, speed, direction = self.status()
            cx, cy = location
            
            # IMPROVE direction comments are not corrent?
            if cx > ARENA_MAX_WIDTH - self.BORDER:
                if cy < ARENA_MAX_LENGTH - self.BORDER:
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
            elif cy > ARENA_MAX_LENGTH - self.BORDER:
                # near north wall
                tdir = 180
            elif cy < self.BORDER:
                # near south wall
                tdir = 0
            
            # if  speed = 0, restart drive unit
            # if dir  != dir need to change direction
            if not speed or dir != tdir:
                dir = tdir
                self.drive(dir, SPEED)

            # scan for target
            range = self.scan(scan_dir, 10)
            if range:
                # found one, start shooting it
                self.cannon(scan_dir, range)
                # remember that we saw a target
                hadfix = True
            elif hadfix:
                # had target but lost it, back up the scan
                scan_dir += 40
                # forget target
                hadfix = False
            else: 
                # no target found, increment scan
                scan_dir -= 20
