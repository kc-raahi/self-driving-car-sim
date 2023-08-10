import pickle
import random

from car import Car
from constants import NUM_LANES, CAR_LENGTH
from drivers import Forward, NNDriver
from nn import Level, WLT, NeuralNetwork, create_nn
from road import Road
from universe import Universe


class SimpleController:
    def __init__(self):
        self.stepno = 0
        self.paused = False
        self.running = True
        self.step_mode = False
        self.universe = self.create_universe()

    def step(self):
        if not self.paused:
            self.stepno += 1
            self.universe.step()
            if self.step_mode:
                self.paused = True
        if self.universe.is_done():
            self.running = False

    def create_universe(self):
        universe = Universe()
        y = universe.road.get_lane_center(int(NUM_LANES / 2))
        universe.cars.extend(self.get_cars(50, y))
        traffic = create_traffic_1(5, universe.road)
        universe.cars.extend(traffic)
        return universe

    def get_cars(self, n, y):
        cars = []
        for i in range(n):
            level_0 = Level([WLT()] * 2)
            nn = NeuralNetwork([level_0])
            cars.append(Car(0, y, NNDriver(nn)))

        return cars


class GenerationController:
    """
    Pause, resume, step mode functionality. Takes # of generations, driving cars, and traffic cars.
    """
    def __init__(self, num_gens, num_cars, traffic_pattern, nn_file):
        self.num_gens = num_gens
        self.num_cars = num_cars
        self.traffic_pattern = traffic_pattern
        self.nn_file = nn_file
        self.gen_no = 0
        self.stepno = 0
        self.paused = False
        self.running = True
        self.step_mode = False
        self.max_perturb = 1
        self.universe = self.get_new_universe(None, self.traffic_pattern, self.nn_file)

    def step(self):
        """
        Updates all movement. Handles transition from one gen to the next and the end of the sim.
        """

        if not self.paused:
            self.stepno += 1
            self.universe.step()
            if self.step_mode:
                self.paused = True
        if self.universe.is_done():
            self.gen_no += 1
            self.universe = self.get_new_universe(self.universe, self.traffic_pattern,
                                                  self.nn_file)

            if self.gen_no >= self.num_gens:
                self.running = False

    def get_new_universe(self, curr_universe, traffic_pattern, nn_file):
        """
        Creates the universe object for the next generation once the current generation comes to an end.
        :param curr_universe: Contains info about the best neural network and traffic pattern to carry into the next
        gen.
        :param traffic_pattern: number corresponding to a traffic configuration (info in -h).
        :param nn_file: optional specification of which .pickle file containing a neural network the program should use.
        return: Universe object for the next generation
        """
        self.max_perturb *= 0.95
        print(self.max_perturb)
        universe = Universe()
        if curr_universe is None:
            cars = self.add_cars(universe, nn_file, None)
        else:
            cars = self.add_cars(universe, nn_file, curr_universe.primary_car)
        return self.setup_universe(universe, cars, traffic_pattern)

    def setup_universe(self, universe, cars, traffic_pattern):
        """
        For each generation, takes newly generated cars and the specified traffic pattern to place on the road.
        :param universe: the current universe.
        :param cars: generated in a previous add_cars call.
        :param traffic_pattern: specified in -h
        """
        universe.cars.extend(cars)
        traffic = load_traffic(traffic_pattern)

        universe.cars.extend(traffic)
        universe.primary_car = cars[0]
        return universe

    def add_cars(self, universe, nn_file, primary_car=None):
        """
        Creates new cars for each new generation.
        Creates the first car using an existing saved neural network or a random one.
        Creates the remaining cars based on the first neural network and a perturbation value
        (1: completely random; 0: exactly the same) that gradually decreases every generation.
        """
        cars = []
        y = universe.road.get_lane_center(int(NUM_LANES / 2))
        if primary_car is not None:
            nn = primary_car.driver.nn
        else:
            if nn_file != "":
                with open(nn_file, "rb") as f:
                    nn = pickle.load(f)
            else:
                nn = create_nn([4, 2])

        for i in range(self.num_cars):
            cars.append(Car(0, y, NNDriver(nn)))
            nn = nn.mutate(self.max_perturb)

        return cars


def create_traffic_1(num_traffic, road):
    # Upward cascading pattern
    traffic = []
    x = 100
    for i in range(num_traffic):
        y = road.get_lane_center(i % NUM_LANES)
        traffic.append(Car(x, y, Forward(), True))
        x += 3 * CAR_LENGTH
    return traffic


def create_traffic_2(num_traffic, road):
    # Downward cascading pattern
    traffic = []
    x = 100
    for i in range(num_traffic):
        y = road.get_lane_center((NUM_LANES - i) % NUM_LANES)
        traffic.append(Car(x, y, Forward(), True))
        x += 3 * CAR_LENGTH

    return traffic


def create_traffic_3(num_traffic, road):
    # Alternating 1-2 pattern
    traffic = []
    x = 100
    for i in range(num_traffic):
        if i % 2 == 0:
            y1 = road.get_lane_center(2)
            y2 = road.get_lane_center(0)
            traffic.append(Car(x, y1, Forward(), True))
            traffic.append(Car(x, y2, Forward(), True))
        else:
            y = road.get_lane_center(1)
            traffic.append(Car(x, y, Forward(), True))

        x += 3 * CAR_LENGTH

    return traffic


def create_traffic_4(num_traffic, road):
    # Random traffic Pattern
    traffic = []
    x = 100
    for i in range(num_traffic):
        y = road.get_lane_center(random.randint(0, 2))
        traffic.append(Car(x, y, Forward(), True))
        x += 3 * CAR_LENGTH

    return traffic


def load_traffic(file_name):
    with open(file_name, "rb") as f:
        traffic = pickle.load(f)

    return traffic


def load_traffic_1():
    with open("savedata/cascade_up_traffic.pickle", "rb") as f:
        t = pickle.load(f)

    return t


def load_traffic_2():
    with open("savedata/cascade_down_traffic.pickle", "rb") as f:
        t = pickle.load(f)

    return t


def load_traffic_3():
    with open("savedata/random_traffic_1.pickle", "rb") as f:
        t = pickle.load(f)

    return t


def load_traffic_4():
    with open("savedata/random_traffic_2.pickle", "rb") as f:
        t = pickle.load(f)

    return t


if __name__ == "__main__":
    t = create_traffic_4(10, Road())
    with open("savedata/random_traffic_2.pickle", "wb") as f:
        pickle.dump(t, f)
