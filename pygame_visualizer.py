from visualizer import Visualizer
from constants import *
from simulator import *

import sys, pygame
from pygame.locals import *

class PyGameVisualizer(Visualizer):
    def __init__(self):
        self.size = self.width, self.height = 500, 500
        pygame.init()
 
        self.screen = pygame.display.set_mode(self.size)
        
    def visualize(self, sim):
        self.sim = sim
        self.handle_events()
        self.draw()
    
    def draw(self):
    
        
        self.draw_background()
        self.draw_robots()
        self.draw_shells()
        pygame.display.flip()
        
    
    def draw_background(self):
        black = 0, 0, 0
        self.screen.fill(black)
    
    def draw_robots(self):
        color = [100,200,100]
        for player in self.sim.players:
            robot = player.robot
            self.draw_circle(self.convert_location(robot.location), self.convert_width(robot.radius), color )
            
    def draw_shells(self):
        color = [250, 250, 250]
        for shell in self.sim.shells:
            self.draw_circle(self.convert_location(shell.location), self.convert_width(shell.radius), color )

    def draw_circle(self, position, radius, color):
        pygame.draw.circle(self.screen, color, position, radius )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                sys.exit()

    def convert_location(self, location):
        
        
        return [  self.convert_width(location[0]), self.convert_height(location[1]) ]
        
    def convert_width(self, width):
        x = float(width) * self.width / ARENA_MAX_WIDTH
        return int(x)

    def convert_height(self, height):
        y = float(height) * self.height / ARENA_MAX_LENGTH
        return int(y)
        
if __name__ == '__main__':
    vis = PyGameVisualizer()
    
    r1 = Robot([1000,500], 'R1')
    r2 = Robot([5000,1000], 'R2')
    pl1 = Player(r1, Shooter() )
    pl2 = Player(r2, Driver() )
    print str(pl2)
    sim = Simulator([pl1, pl2], vis)
    sim.start()
