import random

from constants import SENSOR_ANGLES


class Forward:
    def drive(self, car):
        return 1, 0


class NNDriver:
    def __init__(self, nn):
        self.nn = nn

    def drive(self, car):
        """
        Gets readings from the sensors.
        Feeds the readings through the neural network and to the car's acceleration and angular acceleration.
        """
        sensor_inputs = [s.offset for s in car.sensors]
        outputs = self.nn.feed_fwd(sensor_inputs)
        return 1, outputs[1]
    