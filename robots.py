#!/usr/bin/env python
import sys
import getopt

from random import randint
from objects import Robot
from pygame_visualizer import PyGameVisualizer
from simulator import Player, Simulator

import controllers

def main():
    opts, args = getopt.getopt(sys.argv[1:], "", ["help"])

    players = []
    player_no = 0

    for type in args:
        players.append(create_player(type, player_no))
        player_no += 1
        
    vis = PyGameVisualizer()
    sim = Simulator(players, vis)
    sim.start()

def create_player(type, player_no):
    controller = create_controller(type)
    robot = Robot([ randint(1000, 9000), randint(1000, 9000) ], type)
    
    player = Player(robot, controller)
    player.color = create_color(type, player_no)
    return player
    
def create_color(type, player_no):
    colors = [  (0, 0, 255),
                (255,0,0),
                (0,255,0),
                (255,255,0),
                (255,0,255),
                (0,255,255)]
    if len(colors)-1 > player_no:
        return colors[player_no]    

    return [randint(0, 255), randint(0, 255), randint(0, 255)]
    
def create_controller(type):
    found_type = filter(lambda(file): file == type, dir(controllers))
    if not found_type:
        print("not found %s" % type)
        sys.exit(1)
    exec "from controllers." + type +" import *" in globals()
    
    class_name = type.capitalize()
    
    try:
        return eval('%s()' % class_name )
    except NameError:
        print "Not found class %s in controllers/%s.py" % (class_name, type)
        sys.exit(1)
    
    

if __name__ == "__main__":
    main()


