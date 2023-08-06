import random

from refactor.constants import SENSOR_ANGLES


class Forward:
    def drive(self, car):
        return 1, 0


class NNDriver:
    def __init__(self, nn):
        self.nn = nn

    def drive(self, car):
        sensor_inputs = [s.offset for s in car.sensors]
        outputs = self.nn.feed_fwd(sensor_inputs)
        return 1, outputs[1]