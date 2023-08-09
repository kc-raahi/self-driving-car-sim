import math
import pickle

from constants import SCREEN_WIDTH, CAR_LENGTH, SENSOR_LENGTH, FRAME_THRESHOLD
from geometry import Pt, dist, line_segment_intersection
from road import Road


class Universe:
    def __init__(self):
        self.road = Road()
        self.cars = []
        self.traffic_ahead_of_pc = 0
        self.traffic_ahead_static = 0
        self.min_traffic_ahead_static = 0
        self.frame = 0



    def step(self):
        for car in self.cars:
            car.step()

        self.frame += 1
        self.primary_car = self.find_primary_car()
        self.road.left_x = self.primary_car.x - 0.5 * SCREEN_WIDTH
        self.update_sensors_and_damage()

    def find_primary_car(self):
        return max([c for c in self.cars if not c.traffic], key=lambda c: c.x)

    def is_done(self):
        """
        Checks if current generation should end for the next generation to begin.
        """
        if self.all_cars_crashed():
            return True

        pc_ahead, num_traffic_ahead = self.primary_car_ahead_of_all_traffic()

        if pc_ahead:
            with open("savedata\\nn.pickle", "wb") as f:
                pickle.dump(self.primary_car.driver.nn, f)
            return True
        if num_traffic_ahead == self.traffic_ahead_of_pc:
            self.traffic_ahead_static += 1
        else:
            self.traffic_ahead_static = 0
            self.traffic_ahead_of_pc = num_traffic_ahead
        if self.traffic_ahead_static > 500:
            return True

        if self.frame != self.frame % FRAME_THRESHOLD:
            self.frame %= FRAME_THRESHOLD
            return True

        return False

    def update_sensors_and_damage(self):
        for car in self.cars:
            if car.traffic or car.damaged:
                continue
            relevant_traffic = [t for t in self.cars if t.traffic and abs(t.x - car.x) <= CAR_LENGTH + SENSOR_LENGTH]
            lines = self.get_relevant_lines_for_car(car, relevant_traffic)
            self.update_car_sensors(car, lines)
            self.update_car_damage(car, lines)

    def update_car_sensors(self, car, lines):

        for s in car.sensors:
            p = Pt(car.x, car.y)
            sensor_line = (p, s.current_endpoint)
            self.update_single_sensor(s, p, sensor_line, lines)

    def get_relevant_lines_for_car(self, car, relevant_traffic):
        lines = self.get_traffic_lines(relevant_traffic)
        low_line, high_line = self.get_road_lines(car)
        lines.append(high_line)
        lines.append(low_line)
        return lines

    def get_road_lines(self, car):
        low_x = car.x - (CAR_LENGTH + SENSOR_LENGTH)
        high_x = car.x + CAR_LENGTH + SENSOR_LENGTH
        low_y = self.road.bottom_line_y
        high_y = self.road.top_line_y
        return (Pt(low_x, low_y), Pt(high_x, low_y)), (Pt(low_x, high_y), Pt(high_x, high_y))

    def get_traffic_lines(self, relevant_traffic):
        lines = []
        for t in relevant_traffic:
            [c1, c2, c3, c4] = t.get_corners()
            lines.append((c1, c2))
            lines.append((c2, c3))
            lines.append((c3, c4))
            lines.append((c4, c1))
        return lines

    def update_single_sensor(self, s, car_center, sensor_line, lines):
        closest_intersection = None
        final_dist = math.inf
        for line in lines:
            intersection = line_segment_intersection(sensor_line, line)
            d = math.inf if intersection is None else dist(car_center, intersection)
            if d < final_dist:
                final_dist = d
                closest_intersection = intersection

        s.intersection = closest_intersection
        s.offset = 1 - (final_dist / SENSOR_LENGTH) if closest_intersection is not None else 0

    def update_car_damage(self, car, lines):
        [c1, c2, c3, c4] = car.get_corners()
        driver_lines = [(c1, c2), (c2, c3), (c3, c4), (c4, c1)]

        for dl in driver_lines:
            for line in lines:
                isec = line_segment_intersection(dl, line)
                if isec is not None:
                    car.damaged = True
                    break
            if car.damaged:
                break

    def all_cars_crashed(self):
        alive_cars = [c for c in self.cars if not c.damaged and not c.traffic]
        return len(alive_cars) == 0

    def primary_car_ahead_of_all_traffic(self):
        traffic_ahead_of_pc = [t for t in self.cars if t.traffic and t.x > self.primary_car.x]
        return len(traffic_ahead_of_pc) == 0, len(traffic_ahead_of_pc)

