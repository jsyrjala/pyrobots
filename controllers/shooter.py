from controller import Controller
from random import randint
from constants import *

class Shooter(Controller):
    """
    Shoots randomly.
    """
    def __init__(self):
        Controller.__init__(self)

    def execute(self):
        while True:
            self.shoot(randint(0,360), randint(500, MAX_CANNON_RANGE) )