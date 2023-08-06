import pickle
import random

from car import Car
from constants import NUM_LANES, CAR_LENGTH
from drivers import Forward, NNDriver
from nn import Level, WLT, NeuralNetwork
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
        traffic = create_traffic(5, universe.road)
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
    def __init__(self, num_gens, num_cars, num_traffic):
        self.num_gens = num_gens
        self.num_cars = num_cars
        self.num_traffic = num_traffic
        self.gen_no = 0
        self.stepno = 0
        self.paused = False
        self.running = True
        self.step_mode = False
        self.max_perturb = 1
        self.universe = self.get_new_universe(None)


    def step(self):
        if not self.paused:
            self.stepno += 1
            self.universe.step()
            if self.step_mode:
                self.paused = True
        if self.universe.is_done():
            self.gen_no += 1
            self.universe = self.get_new_universe(self.universe)
            if self.gen_no > self.num_gens:
                self.running = False

    def get_new_universe(self, curr_universe):
        self.max_perturb = 0.95 * self.max_perturb
        print(self.max_perturb)
        universe = Universe()
        if curr_universe is None:
            cars = self.add_cars(universe, None)
        else:
            with open("nn.pickle", "wb") as f:
                pickle.dump(curr_universe.primary_car.driver.nn, f, pickle.HIGHEST_PROTOCOL)
            cars = self.add_cars(universe, curr_universe.primary_car)
        return self.setup_universe(universe, cars)

    def setup_universe(self, universe, cars):
        # y = universe.road.get_lane_center(int(NUM_LANES / 2))
        # universe.cars.extend(self.get_cars(50, y))
        universe.cars.extend(cars)
        traffic = create_traffic_4(10, universe.road)
        universe.cars.extend(traffic)
        universe.primary_car = cars[0]
        return universe

    def add_cars(self, universe, primary_car=None):
        cars = []
        y = universe.road.get_lane_center(int(NUM_LANES / 2))
        if primary_car is not None:
            nn = primary_car.driver.nn
        else:
            level_0 = Level([WLT() for i in range(2)])
            nn = NeuralNetwork([level_0])
            # with open("nn.pickle", "rb") as f:
            #     nn = pickle.load(f)

        for i in range(1, self.num_cars):
            cars.append(Car(0, y, NNDriver(nn)))
            nn = nn.mutate(self.max_perturb)

        return cars


def create_traffic(num_traffic, road):
    traffic = []
    x = 100
    for i in range(num_traffic):
        y = road.get_lane_center(i % NUM_LANES)
        traffic.append(Car(x, y, Forward(), True))
        x += 3 * CAR_LENGTH
    return traffic


def create_traffic_2(num_traffic, road):
    traffic = []
    x = 100
    for i in range(num_traffic):
        y = road.get_lane_center((NUM_LANES - i) % NUM_LANES)
        traffic.append(Car(x, y, Forward(), True))
        x += 3 * CAR_LENGTH

    return traffic

def create_traffic_3(num_traffic, road):
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
    traffic = []
    x = 100
    for i in range(num_traffic):
        y = road.get_lane_center(random.randint(0, 2))
        traffic.append(Car(x, y, Forward(), True))
        x += 3 * CAR_LENGTH

    return traffic


def load_traffic_1():
    with open("traffic1.pickle", "rb") as f:
        t = pickle.load(f)

    return t


def load_traffic_2():
    with open("traffic2.pickle", "rb") as f:
        t = pickle.load(f)

    return t


if __name__ == "__main__":
    t = create_traffic_4(10, Road())
    with open("traffic2.pickle", "wb") as f:
        pickle.dump(t, f)
