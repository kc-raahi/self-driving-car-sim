from refactor.car import Car
from refactor.constants import NUM_LANES
from refactor.drivers import Forward
from refactor.universe import Universe


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
            # print(self.stepno)
            # self.universe.road.left_x += 0.2

    def create_universe(self):
        universe = Universe()
        universe.cars.append(Car(0, universe.road.get_lane_center(int(NUM_LANES / 2)), Forward()))
        return universe