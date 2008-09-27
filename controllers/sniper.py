from controller import Controller
from constants import *
from random import randint
from math import hypot, atan2, degrees

class Sniper(Controller):
    """
    Based on c-robots sniper.r.
    
    Head for a random corner, stay there scanning 90 angle, change to another random corner if hit.
    The idea is that in corner you need to scan only 90 angle, so you can make accurate scans fast.
    """

    # corner, number, locations, and scan start angles
    CORNERS = { 0 : ((200, 200), 0),
                1 : ((200, 10000 - 200), 270),
                2 : ((10000 - 200, 10000 - 200), 180),
                3 : ((10000 - 200, 200), 90) }

    def execute(self):
        self.corner = -1
        self.new_corner()
        self.snipe()

    def snipe(self):
        """
        Scan 90 angle back and forth, shoot targets, stop sniping when getting damage.
        """
        self.last_damage = self.damage()
        scan_dir = self.scan_start
        closest = None
        while True:
            while scan_dir < self.scan_start + 90:
                # look at direction
                range = self.scan(scan_dir, 1)
                if range and range <= MAX_CANNON_RANGE:
                    # found someone to shoot at, keep shooting while it is in our sight
                    while range:
                        closest = range
                        self.shoot(scan_dir, range)
                        range = self.scan(scan_dir, 1)
                        if self.last_damage + 15 > self.damage():
                            # getting too much damage => give up shooting and head for a new corner
                            range = None
                    # back up scan, in case the target moved        
                    scan_dir -= 10
                # scan slowly forward
                scan_dir += 2
                
                if self.last_damage != self.damage():
                    # not shooting anyone, but somebody is shooting us, time to move
                    self.new_corner()
                    self.last_damage = self.damage()
                    scan_dir = self.scan_start
                    closest = None
                    
            if not closest:
                # nobody to shoot at from this corner, so try another corner
                self.new_corner()
                self.last_damage = self.damage()
                scan_dir = self.scan_start
            else:
                # there was someone to shoot in range, but lost it, so scan again
                scan_dir = self.scan_start
                self.closest = None
                
    def new_corner(self):
        """
        Selects a random corner (different from current) and drives there.
        """
        # select a random corner
        new_corner = randint(0, 3)
        # if same as current, select another corner
        if new_corner == self.corner:
            new_corner = (new_corner + 1) % 4
        
        self.corner = new_corner
        self.corner_location, self.scan_start = self.CORNERS[self.corner]

        # find heading for desired corner        
        direction = self.plot_course(self.corner_location)

        # start driving there at full speed
        self.drive(direction, MAX_FORWARD_SPEED)

        # keep running until close to corner
        while(self.distance(self.location(), self.corner_location) > 1000 and self.speed() > 0):
            self.wait()
        
        # compute a more accurate direction and slow down to a crawl => robot can be stopped in single timestep
        direction = self.plot_course(self.corner_location)
        self.drive(direction, MAX_ACCELERATION);
        
        while(self.distance(self.location(), self.corner_location) > 200 and self.speed() > 0):
            self.wait()
        
        # stop engine and point robot to arena center for faster turning to next corner
        self.drive(self.plot_course([ARENA_MAX_WIDTH / 2, ARENA_MAX_LENGTH / 2]), 0)

    def distance(self, location_a, location_b):
        """
        Distance between two locations. Returns a float value.
        """
        return hypot(location_a[0] - location_b[0], location_a[1] - location_b[1])
        
    def plot_course(self, target_location):
        """
        Computes direction in degrees from current location to target_location
        """
        y_diff = target_location[1] - self.y_loc()
        x_diff = target_location[0] - self.x_loc()
        
        return degrees(atan2( y_diff, x_diff ))
        
    