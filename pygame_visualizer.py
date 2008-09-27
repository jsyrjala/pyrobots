from visualizer import Visualizer
from constants import *
from simulator import *
from random import randint

import sys, pygame
from pygame.locals import *

from controllers.cylon import * 
from controllers.tracker import * 
from controllers.sniper import * 
from controllers.cspotrun import *


class PyGameVisualizer(Visualizer):
    def __init__(self):
        self.size = self.width, self.height = 500, 500
        self.screen_size = self.screen_width, self.screen_height = 600, 600
        self.offset = 50
        pygame.init()
 
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("PyRobots")
    def visualize(self, sim):
        self.sim = sim
        self.handle_events()
        self.draw()
    
    def draw(self):
        self.draw_background()
        self.draw_meters()
        self.draw_explosions()
        self.draw_robots()
        self.draw_shells()
        pygame.display.flip()
        
    
    def draw_background(self):
        black = 0, 0, 0
        self.screen.fill(black)

        rect = [self.offset, self.offset, self.screen_width - 2*self.offset, self.screen_height - 2*self.offset]
        pygame.draw.rect(self.screen, [255,255,255], rect, 1)
    
    def draw_meters(self):
        y = 6
        for player in self.sim.players:
            y += 4
            robot = player.robot
            value = (self.screen_width - 2*self.offset) * min(MAX_DAMAGE,robot.damage) / MAX_DAMAGE
            rect = [self.offset, y, value, 2]
            pygame.draw.rect(self.screen, player.color, rect)
    
    def draw_robots(self):
        
        for player in self.sim.players:
            robot = player.robot
            color = player.color
            self.draw_circle(self.convert_location(robot.location), self.convert_width(robot.radius), color )
            
    def draw_shells(self):
        for shell in self.sim.shells:
            self.draw_circle(self.convert_location(shell.location), 1, shell.shooter.player.color )

    def draw_explosions(self):
        for shell in self.sim.exploding_shells:
            self.draw_circle(self.convert_location(shell.location), self.convert_width(BLAST_MIN_DAMAGE_RADIUS), shell.shooter.player.color )
        

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
    dummy1 = create_player("dummy1", Controller, [255,255,255] )
    dummy2 = create_player("dummy2", Controller, [255,255,255] )
    cylon1 = create_player("cylon1", Cylon, [255,255,255] )
    
    tracer1 = create_player("tracer1", Tracker, [40, 255, 255] )
    tracer2 = create_player("tracer2", Tracker, [140, 255, 25] )
    
    sniper1 = create_player("sniper1", Sniper, [255, 0, 0] )
    sniper2 = create_player("sniper2", Sniper, [255, 255, 0] )
    
    cspotrun = create_player("cspotrun", Cspotrun, [100, 100, 255] )
    
    dummy1.robot.location = [200, 9500]
    dummy2.robot.location = [9500, 9500]
    players = [dummy1, cylon1, tracer1, sniper1, sniper2, cspotrun]
    #players = [dummy1,  cspotrun]
    sim = Simulator(players, vis)
    
    sim.start()
