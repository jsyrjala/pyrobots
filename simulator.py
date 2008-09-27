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
        robot.player = self
        self.active = True

class Simulator:
    def __init__(self, players, visualizer = None):
        """Initialized Simulator"""
        self.players = players
        self.active_players = list(players)
        self.shells = []
        self.exploding_shells = []
        self.logger = logging.getLogger('SIMULATOR')
        self.logger.info("initialized")
        self.order_results = {}
        self.visualizer = visualizer
        self.timestep_count = 0
        
    def start(self):
        self.greenlet = greenlet(self.simulate)
        for player in self.players:
            player.greenlet = greenlet(player.controller.__init_event_loop__)
            player.controller.main_greenlet = self.greenlet
        
        while True:
            value = self.greenlet.switch()
            # a controller greenlet has died due a bug
            if len(self.active_players) < 2:
                break;

        self.logger.info("Winner is %s" % self.active_players[0].robot.name)
        while True:
            if self.visualizer:
                self.visualizer.visualize(self)
            time.sleep(0.2)

    def simulate(self):
        while( len(self.active_players) > 1 and not self.stopping()):
            self.timestep()
            
    def timestep(self):
        self.timestep_count += 1
        # orders for current timestep
        orders = {}
        
        
        # results for orders in previous timestep
        if self.visualizer:
            self.visualizer.visualize(self)

        self.exploding_shells = []


        # get orders for robots
        for player in self.active_players:
            # first thing in results is robot's status
            prev_results = [ player.robot.status() ]
            if self.order_results.has_key(player):
                prev_results.append(self.order_results[player] )

            new_order = self.get_order(player,  prev_results)
            if new_order:
                orders[player] = new_order

        # handle flying shells
        self.move_shells()
 
        # execute orders
        for player in self.active_players:
            robot = player.robot
            if orders.has_key(player):
                result = self.execute_order(robot, orders[player])
                self.order_results[player] = result
            robot.move()

    def move_shells(self):
        """
        Move flying shells and handle explosions.
        """
        finished_shells = []        
        for shell in self.shells:
            if shell.move():
                shell.explode()
                self.exploding_shells.append(shell)
                self.shells.remove(shell)

        for shell in self.exploding_shells:
            for player in self.active_players:
                robot = player.robot
                distance = shell.distance_to(robot.location)
                damage = 0
                for blast in BLAST_DAMAGE:
                    if distance > blast[0]:
                        break;
                    damage = blast[1]
                
                robot.damage += damage
                    
                if robot.damage > MAX_DAMAGE:
                    # robot died
                    player.active = False
                    self.active_players.remove(player)
                    self.logger.info("%s destroyed at %d" % (robot.name, self.timestep_count))
    
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


    def scan_order(self, current_robot, scan_direction, spread):
        shortest_distance = None
        for player in self.active_players:
            robot = player.robot
            if current_robot == robot:
                continue
            
            direction_vector = direction(current_robot.location, robot.location)
            if fabs(angle_difference(direction_vector, scan_direction)) > spread:
                continue
            
            dist = current_robot.distance_to(robot.location)
            if not shortest_distance or shortest_distance > dist:
                shortest_distance = dist
        return shortest_distance


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
