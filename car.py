from random import random

import pygame
import math

pygame.init()

CAR_SIZE_X = 30
CAR_SIZE_Y = 50
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 600
DEG_TO_RAD = (2 * math.pi) / 360
LINE_COL = (255, 255, 255)  # white
ROAD_COL = (50, 50, 50)  # dark gray
SENSOR_COL = (200, 200, 0)  # yellow
SENSOR_ACTIVE_COL = (255, 0, 0)  # bright red
LINE_WIDTH = 5
DASH_HEIGHT = 20
DRIVER_COL = (100, 100, 200)
DRIVER_DAMAGED_COL = (150, 150, 200)
DRIVER_SECONDARY_COL = (50, 50, 200)
TRAFFIC_COL = (100, 200, 100)


def lerp(a, b, t):
    return a + (b - a) * t


def get_ray_intersection(length, angle, my_driver, my_traffic):
    for i in range(length):
        ray_point_x = my_driver.x - i * math.sin(angle)
        ray_point_y = my_driver.y - i * math.cos(angle)
        if ray_point_x < 0 or ray_point_x > SCREEN_WIDTH:
            return ray_point_x, ray_point_y, i / length
        for car in my_traffic:
            x_check = car.x - CAR_SIZE_X / 2 <= ray_point_x <= car.x + CAR_SIZE_X / 2
            y_check = car.y - CAR_SIZE_Y / 2 <= ray_point_y <= car.y + CAR_SIZE_Y / 2
            if x_check and y_check:
                return ray_point_x, ray_point_y, i / length

    return None


# 0: x; 1: y
# checks the sides of the two cars for any intersections
def get_sides_intersection(a, b, c, d):
    t_top = (d[0] - c[0]) * (a[1] - c[1]) - (d[1] - c[1]) * (a[0] - c[0])
    u_top = (c[1] - a[1]) * (a[0] - b[0]) - (c[0] - a[0]) * (a[1] - b[1])
    bottom = (d[1] - c[1]) * (b[0] - a[0]) - (d[0] - c[0]) * (b[1] - a[1])

    if bottom != 0:
        t = t_top / bottom
        u = u_top / bottom
        if 0 <= t <= 1 and 0 <= u <= 1:
            return lerp(a[0], b[0], t), lerp(a[1], b[1], t), t

    return None


def car_intersection(poly1, poly2):
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            touch = get_sides_intersection(poly1[i], poly1[(i + 1) % len(poly1)], poly2[j], poly2[(j + 1) % len(poly2)])
            if touch is not None:
                return True

    return False


def level_feed_fwd(level, given_inputs):
    for i in range(len(level.inputs)):
        level.inputs[i] = given_inputs[i]

    for i in range(len(level.outputs)):
        cum_sum = 0
        for j in range(len(level.inputs)):
            cum_sum += level.inputs[j] * level.weights[j][i]

        level.outputs[i] = 1 if cum_sum > level.biases[i] else 0

    return level.outputs


def network_feed_fwd(nn, given_inputs):
    outputs = level_feed_fwd(nn.levels[0], given_inputs)
    for i in range(1, len(nn.levels)):
        outputs = level_feed_fwd(nn.levels[i], outputs)

    return outputs


def get_primary_car(cars):
    y = cars[0].y
    primary_index = 0
    for i in range(len(cars)):
        if cars[i].y < y:
            primary_index = i

    return primary_index

class Car:
    def __init__(self, x, y, traffic=False, ctrl_type="nn"):
        self.x = x
        self.y = y
        self.position = [self.x, self.y]
        self.traffic = traffic
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.width = CAR_SIZE_X
        self.height = CAR_SIZE_Y
        self.main_car = False
        self.max_speed = 3 if not self.traffic else 2
        self.angle = 0  # degrees
        self.speed = 0  # if not self.traffic else self.max_speed
        self.acc = 0.2
        self.center = (self.x + CAR_SIZE_X / 2, self.y + CAR_SIZE_Y / 2)
        self.sensors = Sensor(self)
        self.brain = NeuralNetwork([self.sensors.num_rays, 6, 4])
        self.ctrl_type = ctrl_type
        self.alive = True
        self.primary = False
        self.corners = []
        self.dirs = []

    # retrieve the corners of the car, in list of tuples form
    def get_polygon(self, y_adj):
        self.corners = []
        rad = math.hypot(self.width, self.height) / 2
        alpha = math.atan2(self.width, self.height)
        self.corners.append((self.x - math.sin(DEG_TO_RAD * self.angle - alpha) * rad,
                             y_adj - math.cos(DEG_TO_RAD * self.angle - alpha) * rad))
        self.corners.append((self.x - math.sin(DEG_TO_RAD * self.angle + alpha) * rad,
                             y_adj - math.cos(DEG_TO_RAD * self.angle + alpha) * rad))
        self.corners.append((self.x - math.sin(math.pi + DEG_TO_RAD * self.angle - alpha) * rad,
                             y_adj - math.cos(math.pi + DEG_TO_RAD * self.angle - alpha) * rad))
        self.corners.append((self.x - math.sin(math.pi + DEG_TO_RAD * self.angle + alpha) * rad,
                             y_adj - math.cos(math.pi + DEG_TO_RAD * self.angle + alpha) * rad))

    # check if the car has hit another car or offroaded
    def assess_damage(self, my_road):
        for pt in self.corners:
            if pt[0] < 0 or pt[0] > SCREEN_WIDTH:
                return False

        for car in my_road.traffic:
            if car_intersection(self.corners, car.corners):
                return False
        return True

    def forward(self):
        self.up = True
        self.down = False

    def backward(self):
        self.up = False
        self.down = True

    def foot_off_gas(self):
        self.up = False
        self.down = False

    def turn_left(self):
        self.left = True
        self.right = False

    def turn_right(self):
        self.left = False
        self.right = True

    def straighten_wheel(self):
        self.left = False
        self.right = False

    def update_and_draw(self, my_road, my_screen):

        if self.alive:
            if self.up:
                self._accel()
            if self.down:
                self._reverse()
            if not self.up and not self.down:
                self._coast()

            self.position = [self.x, self.y]
            self.y += self.speed * math.cos(self.angle * DEG_TO_RAD)
            self.x += self.speed * math.sin(self.angle * DEG_TO_RAD)
            self._turn()
            y = self.y - my_road.y
            self.get_polygon(y)

        col = (0, 0, 0)
        if self.traffic:
            col = TRAFFIC_COL
        else:
            if self.alive:
                if self.primary:
                    col = DRIVER_COL
                else:
                    col = DRIVER_SECONDARY_COL
            else:
                col = DRIVER_DAMAGED_COL

        pygame.draw.polygon(my_screen, col, self.corners)
        if not self.traffic:
            self.sensors.update_and_draw(self.sensors.car, my_screen, my_road)
            offsets = []
            for i in range(self.sensors.num_rays):
                intersection = get_ray_intersection(self.sensors.ray_len, self.sensors.ray_angles[i],
                                                    self.sensors.car, my_road.traffic)
                p = 0 if intersection is None else 1 - intersection[2]
                offsets.append(p)
            outputs = network_feed_fwd(self.brain, offsets)
            self.dirs = outputs

    def _accel(self):
        if self.speed > self.max_speed * -1:
            self.speed -= self.acc
        else:
            self.speed = self.max_speed * -1

    def _reverse(self):
        if self.speed < self.max_speed:
            self.speed += self.acc
        else:
            self.speed = self.max_speed

    def _coast(self):
        if self.speed != 0:
            if self.speed < 0:
                self.speed += self.acc
            else:
                self.speed -= self.acc
        if 0 < self.speed < 0.2:
            self.speed = 0

    def _turn(self):
        theta = 0
        if self.left:
            theta = 1.5
        if self.right:
            theta = -1.5
        flip = 1 if self.speed <= 0 else -1
        self.angle += theta * flip


class Line:
    def __init__(self, x, y, h):
        self.x = x
        self.y = y
        self.h = h


class Sensor:

    def __init__(self, car, num_rays=5, ray_len=150, ray_spread=math.pi / 2):
        self.car = car
        self.num_rays = num_rays
        self.ray_len = ray_len
        self.ray_spread = ray_spread
        self.rays = []
        self.intersections = []
        self.draw = True if not car.traffic else False
        self.ray_angles = []
        for i in range(num_rays):
            self.ray_angles.append(lerp(self.ray_spread / 2, -self.ray_spread / 2, i / (self.num_rays - 1)) +
                                   car.angle * DEG_TO_RAD)

    def update_and_draw(self, car, my_screen, my_road):
        self.rays = []
        y = car.y - my_road.y
        for i in range(self.num_rays):
            self.intersections.append(False)
            ray_angle = self.ray_angles[i] + car.angle * DEG_TO_RAD
            a = (car.x, y)
            b = (car.x - self.ray_len * math.sin(ray_angle), y - self.ray_len * math.cos(ray_angle))
            self.rays.append((a, b))
            intersection = get_ray_intersection(self.ray_len, ray_angle, car, my_road.traffic)
            self.intersections[i] = intersection is not None

            col = SENSOR_COL if not self.intersections[i] else SENSOR_ACTIVE_COL
            if car.primary:
                pygame.draw.line(my_screen, col, a, b, width=2)


class Road:
    def __init__(self, x, width, lane_count=3):
        self.x = x
        self.y = 0
        self.width = width
        self.lane_count = lane_count
        self.left = x - width / 2
        self.right = x + width / 2
        self.lines = []
        self.traffic = []

    # print the road in relation to the car
    def move_viewport(self, car_y):
        # where we want the top of the screen
        new_y = car_y - 0.9 * SCREEN_HEIGHT
        delta = new_y - self.y
        for line in self.lines:
            line_y_new = line.y - delta
            # keeps line within viewport
            if line_y_new < new_y:
                line_y_new = new_y + SCREEN_HEIGHT - (new_y - line_y_new)
            if line_y_new > new_y + SCREEN_HEIGHT:
                line_y_new = line_y_new - SCREEN_HEIGHT
            line.y = line_y_new
        self.y = new_y

    def set_lines(self):
        for i in range(self.lane_count + 1):
            x = lerp(self.left, self.right, i / self.lane_count)
            step = DASH_HEIGHT if i == 0 or i == self.lane_count else DASH_HEIGHT * 2
            for j in range(int(self.y), int(self.y) + SCREEN_HEIGHT, step):
                self.lines.append(Line(x, j, DASH_HEIGHT))

    def draw(self, my_screen):
        for line in self.lines:
            line_v_y = line.y - self.y
            pygame.draw.line(my_screen, LINE_COL, (line.x, line_v_y), (line.x, line_v_y + DASH_HEIGHT),
                             width=LINE_WIDTH)

    def get_lane_center(self, lane_index):
        lane_width = self.width / self.lane_count
        return self.left + lane_width / 2 + lane_index * lane_width


class Level:
    def __init__(self, num_inputs, num_outputs):
        self.inputs = [0] * num_inputs
        self.outputs = [0] * num_outputs
        self.biases = []
        self.weights = [[]] * num_inputs

        for weight in self.weights:
            for j in range(num_outputs):
                weight.append(random() * 2 - 1)

        for i in range(num_outputs):
            self.biases.append(random() * 2 - 1)


class NeuralNetwork:
    def __init__(self, neuron_counts):
        self.levels = []
        for i in range(len(neuron_counts) - 1):
            self.levels.append(Level(neuron_counts[i], neuron_counts[i + 1]))


if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Self-Driving Car")
    road = Road(SCREEN_WIDTH / 2, SCREEN_WIDTH * 0.9)
    road.set_lines()
    drivers = []
    for i in range(100):
        drivers.append(Car(road.get_lane_center(int(road.lane_count / 2)), SCREEN_HEIGHT * 0.9))

    t = Car(road.get_lane_center(1), 100, traffic=True)
    road.traffic.append(t)
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        screen.fill(ROAD_COL)
        driver = drivers[get_primary_car(drivers)]
        driver.primary = True
        road.move_viewport(driver.y)
        road.draw(screen)
        for d in drivers:
            d.update_and_draw(road, screen)
            d.alive = driver.assess_damage(road)
        t.update_and_draw(road, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if driver.ctrl_type == "keys":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        driver.forward()
                    elif event.key == pygame.K_DOWN:
                        driver.backward()
                    if event.key == pygame.K_LEFT and driver.speed != 0:
                        driver.turn_left()
                    elif event.key == pygame.K_RIGHT and driver.speed != 0:
                        driver.turn_right()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        driver.foot_off_gas()
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        driver.straighten_wheel()

            else:
                driver.up = driver.dirs[0]
                driver.left = driver.dirs[1]
                driver.right = driver.dirs[2]
                driver.down = driver.dirs[3]

        driver.primary = False

        pygame.display.update()

    pygame.quit()
