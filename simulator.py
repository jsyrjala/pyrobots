from constants import *
from objects import *
from controller import *
from greenlet import greenlet
from pygame_visualizer import *
import time
class Player:
    def __init__(self, robot, controller):
        self.robot = robot
        self.controller = controller

class Simulator:
    def __init__(self, players, visualizer = None):
        """Initialized Simulator"""
        self.players = players
        self.shells = []
        self.logger = logging.getLogger('SIMULATOR')
        self.logger.info("initialized")
        self.order_results = {}
        self.visualizer = visualizer
        
    def start(self):
        self.greenlet = greenlet(self.simulate)
        for player in self.players:
            player.greenlet = greenlet(player.controller.__init_event_loop__)
            player.controller.main_greenlet = self.greenlet
        self.greenlet.switch()
            
        
    def simulate(self):
        while( len(self.players) > 1 and not self.stopping()):
            self.timestep()
            
    def timestep(self):
        # orders for current timestep
        orders = {}
        # results for orders in previous timestep
        if self.visualizer:
            self.visualizer.visualize(self)
            
        # get orders for robots
        for player in self.players:
            # first thing in results is robot's status
            prev_results = [ player.robot.status() ]
            if self.order_results.has_key(player):
                prev_results.append(self.order_results[player] )

            new_order = self.get_order(player,  prev_results)
            if new_order:
                orders[player] = new_order

        # handle flying shells
        finished_shells = []        
        for shell in self.shells:
            if shell.move():
                shell.explode()
                self.shells.remove(shell)
 
        # execute orders
        for player in self.players:
            robot = player.robot
            if orders.has_key(player):
                result = self.execute_order(robot, orders[player])
                self.order_results[player] = result
            robot.move()



    
    def execute_order(self, robot, order):
        """
        order = [cmd_type, [param1, param2, paramN]]
        """
        command = order[0]
        if command == Controller.SHOOT:
            return self.shoot_order(robot, order[1][0], order[1][1])
        elif command == Controller.SCAN:
            return self.scan_order(robot, order[1][0], order[1][1])

        elif command == Controller.DRIVE:
            return self.drive_order(robot, order[1][0], order[1][1])
        elif command == Controller.WAIT:
            pass
        

    def get_order(self, player, results):
        return player.greenlet.switch(results)

    def shoot_order(self, robot, direction, distance):
        if robot.can_shoot():
            self.logger.debug(robot.name + " shooting.")
            self.shells.append(robot.shoot(direction, distance))
            return True
        self.logger.debug(robot.name + " tried to shoot in vain.")
        return False

    def drive_order(self, robot, direction, speed):
        self.logger.debug(robot.name + " driving.")
        return robot.drive(direction, speed)


    def scan_order(self, robot, direction, speed):
        pass


    def stopping(self):
        # TODO kill game after N steps if no resolution before
        pass


if __name__ == '__main__':
    
    r1 = Robot([1000,500], 'R1')
    r2 = Robot([5000,1000], 'R2')
    pl1 = Player(r1, Shooter() )
    pl2 = Player(r2, Driver() )
    sim = Simulator([pl1, pl2])
    sim.start()
