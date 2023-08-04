from refactor.constants import SCREEN_WIDTH
from refactor.road import Road


class Universe:
    def __init__(self):
        self.road = Road()
        self.cars = []

    def step(self):
        for car in self.cars:
            car.step()

        self.primary_car = self.find_primary_car()
        self.road.left_x = self.primary_car.x - 0.1 * SCREEN_WIDTH

    def find_primary_car(self):
        return max([c for c in self.cars if not c.traffic], key=lambda c: c.x)

