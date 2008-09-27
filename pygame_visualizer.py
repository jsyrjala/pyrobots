from visualizer import Visualizer
from constants import *
from simulator import *
from random import randint

import sys, pygame
from pygame.locals import *

from controllers.cylon import * 
from controllers.tracker import * 
from controllers.sniper import * 


class PyGameVisualizer(Visualizer):
    def __init__(self):
        self.size = self.width, self.height = 500, 500
        self.screen_size = self.screen_width, self.screen_height = 600, 600
        self.offset = 50
        pygame.init()
 
        self.screen = pygame.display.set_mode(self.screen_size)
        
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

        rect = [self.offset, self.offset, self.screen_width - 2*self.offset, self.screen_height - 2*self.offset]
        pygame.draw.rect(self.screen, [255,255,255], rect, 1)
        
    def draw_robots(self):
        
        for player in self.sim.players:
            robot = player.robot
            color = player.color
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
        return [  self.convert_width(location[0]) + self.offset, self.convert_height(location[1]) + self.offset ]
        
    def convert_width(self, width):
        x = float(width) * self.width / ARENA_MAX_WIDTH
        return int(x)

    def convert_height(self, height):
        y = float(height) * self.height / ARENA_MAX_LENGTH
        return int(y)

if __name__ == '__main__':
    def create_player(name, controller, color):
        robot = Robot([ randint(1000, 9000), randint(1000, 9000) ], name)
        robot.direction = randint(0,359)
        player = Player(robot, controller())
        player.color = color
        return player
        
    vis = PyGameVisualizer()
    pl0 = create_player("dummy", Controller, [255,255,255] )
    pl1 = create_player("cylon", Cylon, [255,255,255] )
    pl2 = create_player("tracer", Tracker, [40, 255, 255] )
    pl3 = create_player("sniper", Sniper, [255, 0, 0] )
    
    players = [pl1, pl2, pl3]
    sim = Simulator(players, vis)
    
    sim.start()
