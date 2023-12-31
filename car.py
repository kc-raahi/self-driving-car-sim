import math

from constants import *
from geometry import Pt, transpose_line, rotate_line_about_origin, rotate_about_origin, transpose
from utils import deg_to_rad, clamp


class Sensor:
    def __init__(self, angle):
        self.angle = angle
        endpoint_x = SENSOR_LENGTH * math.cos(deg_to_rad(angle))
        endpoint_y = SENSOR_LENGTH * math.sin(deg_to_rad(angle))
        self.origin_endpoint = Pt(endpoint_x, endpoint_y)
        self.current_endpoint = self.origin_endpoint
        self.offset = 0
        self.intersection = None


class Car:
    def __init__(self, x, y, driver, traffic=False):
        self.x = x
        self.y = y

        self.driver = driver
        self.traffic = traffic
        self.acc = 0
        self.ang_acc = 0
        self.speed = 0
        self.max_speed = CAR_MAX_SPEED if not self.traffic else CAR_MAX_SPEED * 0.6
        self.angle = 0
        w = CAR_WIDTH
        h = CAR_LENGTH
        self.corners = [        # bottom left counterclockwise
            Pt(-h / 2, -w / 2),
            Pt(-h / 2, w / 2),
            Pt(h / 2, w / 2),
            Pt(h / 2, -w / 2)
        ]
        self.sensors = [
            Sensor(angle) for angle in SENSOR_ANGLES
        ]
        self.damaged = False
        self.primary = False

    def step(self):
        """
        Updates an individual car's position on the road.
        Checks if the car is damaged (no movement allowed if so).
        Changes the position of the car according to its acceleration (speeding up/slowing down)
        and angular acceleration (turning).
        Updates sensor positions.
        """
        self.primary = False
        if self.damaged:
            return
        acc, ang_acc = self.driver.drive(self)
        self.angle += ang_acc * CAR_ANG_ACC_STEP
        self.speed += acc * CAR_ACC_STEP
        self.speed = clamp(self.speed, -self.max_speed, self.max_speed)
        self.x += self.speed * math.cos(deg_to_rad(self.angle))
        self.y += self.speed * math.sin(deg_to_rad(self.angle))
        for s in self.sensors:
            temp_endpoint = rotate_about_origin(s.origin_endpoint, self.angle)
            s.current_endpoint = transpose(temp_endpoint, self.x, self.y)

    def get_corners(self):
        corners = []
        for p in self.corners:
            tmp_corner = rotate_about_origin(p, self.angle)
            final_corner = transpose(tmp_corner, self.x, self.y)
            corners.append(final_corner)

        return corners

    def get_color(self):
        if self.traffic:
            return TRAFFIC_COLOR
        else:
            if self.damaged:
                return DRIVER_DAMAGED_COLOR
            else:
                if self.primary:
                    return DRIVER_COLOR
                else:
                    return DRIVER_SECONDARY_COLOR
