import random
import pygame
import math

from performance import dump, stop, start

pygame.init()
# random.seed(40)

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
DRIVER_SECONDARY_COL = (100, 200, 200)
TRAFFIC_COL = (100, 200, 100)


def lerp(a, b, t):
    return a + (b - a) * t


def get_ray_intersection(length, angle, my_driver, my_traffic):
    start("get_ray_intersection")
    ray_start_pt = (my_driver.x, my_driver.y)
    ray_end_pt = (my_driver.x - length * math.sin(angle), my_driver.y - length * math.cos(angle))
    pt = None

    # check surrounding traffic
    for car in my_traffic:
        # top left corner, rotate counterclockwise
        pt1 = (car.x - CAR_SIZE_X / 2, car.y - CAR_SIZE_Y / 2)
        pt2 = (car.x - CAR_SIZE_X / 2, car.y + CAR_SIZE_Y / 2)
        pt3 = (car.x + CAR_SIZE_X / 2, car.y + CAR_SIZE_Y / 2)
        pt4 = (car.x + CAR_SIZE_X / 2, car.y - CAR_SIZE_Y / 2)
        d1 = math.sqrt(math.pow(pt1[0] - my_driver.x, 2) + math.pow(pt1[1] - my_driver.y, 2))
        d2 = math.sqrt(math.pow(pt2[0] - my_driver.x, 2) + math.pow(pt2[1] - my_driver.y, 2))
        d3 = math.sqrt(math.pow(pt3[0] - my_driver.x, 2) + math.pow(pt3[1] - my_driver.y, 2))
        d4 = math.sqrt(math.pow(pt4[0] - my_driver.x, 2) + math.pow(pt4[1] - my_driver.y, 2))
        theta1 = math.atan2(pt1[1] - my_driver.y, pt1[0] - my_driver.x)
        theta2 = math.atan2(pt2[1] - my_driver.y, pt2[0] - my_driver.x)
        theta3 = math.atan2(pt3[1] - my_driver.y, pt3[0] - my_driver.x)
        theta4 = math.atan2(pt4[1] - my_driver.y, pt4[0] - my_driver.x)
        angles = sorted([theta1, theta2, theta3, theta4])
        ds = sorted([d1, d2, d3, d4])
        if angles[0] <= angle <= angles[3] and ds[0] <= length:
            x, y = 0, 0
            if theta3 > angle >= 0:                             # right side of car
                x = car.x + CAR_SIZE_X / 2
                y = my_driver.y - x * math.tan(angle)
            if angle >= theta3 and angle >= 0:                  # bottom of car
                y = car.y + CAR_SIZE_Y / 2
                x = my_driver.x - y * math.cos(angle) / math.sin(angle)
            if theta2 <= angle < 0:                             # left side of car
                x = car.x - CAR_SIZE_X / 2
                y = my_driver.y - x * math.tan(angle)
            if angle < theta2 and angle < 0:
                y = car.y + CAR_SIZE_Y / 2
                x = my_driver.x + y * math.cos(angle) / math.sin(angle)
            stop("get_ray_intersection")
            return x, y, math.sqrt(math.pow(car.x - x, 2) + math.pow(car.y - y, 2)) / length

    # check if ray intersects the sides
    left_intersection = ray_end_pt[0] < 0
    right_intersection = ray_end_pt[0] > SCREEN_WIDTH

    if left_intersection:
        y = my_driver.x * math.tan(angle)
        stop("get_ray_intersection")
        return 0, my_driver.y - y, math.sqrt(math.pow(my_driver.x, 2) + math.pow(y, 2))

    if right_intersection:
        x = SCREEN_WIDTH - my_driver.x
        y = x * math.tan(angle)
        stop("get_ray_intersection")
        return SCREEN_WIDTH, my_driver.y - y, math.sqrt(math.pow(x, 2) + math.pow(y, 2))

    stop("get_ray_intersection")
    return None


def get_ray_intersection_new(length, angle, my_driver, my_traffic):
    start("get_ray_intersection")
    ray_start_pt = (my_driver.x, my_driver.y)
    ray_end_pt = (my_driver.x - length * math.sin(angle), my_driver.y - length * math.cos(angle))
    ray = (ray_start_pt, ray_end_pt)
    pt = None

    # check surrounding traffic
    for car in my_traffic:
        x, y = 0, 0
        # top left corner, rotate counterclockwise
        pt1 = (car.x - CAR_SIZE_X / 2, car.y - CAR_SIZE_Y / 2)
        pt2 = (car.x - CAR_SIZE_X / 2, car.y + CAR_SIZE_Y / 2)
        pt3 = (car.x + CAR_SIZE_X / 2, car.y + CAR_SIZE_Y / 2)
        pt4 = (car.x + CAR_SIZE_X / 2, car.y - CAR_SIZE_Y / 2)
        left_side = pt1, pt2
        bottom = pt2, pt3
        right_side = pt3, pt4
        top = pt4, pt1
        sides = [left_side, bottom, right_side, top]
        for side in sides:
            if compute_intersection(ray_start_pt, ray_end_pt, side[0], side[1]) is not None:
                x, y = compute_intersection(ray_start_pt, ray_end_pt, side[0], side[1])
                return x, y, math.sqrt(math.pow(car.x - x, 2) + math.pow(car.y - y, 2)) / length

    # check if ray intersects the sides
    left_intersection = ray_end_pt[0] < 0
    right_intersection = ray_end_pt[0] > SCREEN_WIDTH

    if left_intersection:
        y = my_driver.x * math.tan(angle)
        stop("get_ray_intersection")
        return 0, my_driver.y - y, math.sqrt(math.pow(my_driver.x, 2) + math.pow(y, 2))

    if right_intersection:
        x = SCREEN_WIDTH - my_driver.x
        y = x * math.tan(angle)
        stop("get_ray_intersection")
        return SCREEN_WIDTH, my_driver.y - y, math.sqrt(math.pow(x, 2) + math.pow(y, 2))

    stop("get_ray_intersection")
    return None


def compute_intersection(p1, q1, p2, q2):
    A1 = q1[1] - p1[1]
    B1 = p1[0] - q1[0]
    C1 = A1 * p1[0] + B1 * p1[1]

    A2 = q2[1] - p2[1]
    B2 = p2[0] - q2[0]
    C2 = A2 * p2[0] + B2 * p2[1]

    determinant = A1 * B2 - A2 * B1

    if determinant == 0:  # Lines are parallel
        return None

    x = (B2 * C1 - B1 * C2) / determinant
    y = (A1 * C2 - A2 * C1) / determinant

    intersection = (x, y)
    if on_segment(p1, intersection, q1) and on_segment(p2, intersection, q2):
        return intersection

    return None


def on_segment(p, q, r):
    return (max(p[0], r[0]) >= q[0] >= min(p[0], r[0]) and
            max(p[1], r[1]) >= q[1] >= min(p[1], r[1]))


def orientation(p, q, r):
    return (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])


def do_segments_intersect(segment1, segment2):
    p1, q1 = segment1
    p2, q2 = segment2

    return compute_intersection(p1, q1, p2, q2)


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
    car = None
    for i in range(len(cars)):
        if cars[i].y < y:
            primary_index = i
            y = cars[i].y

    return cars[primary_index]


def get_primary_car_index(cars):
    y = cars[0].y
    primary_index = 0
    for i in range(len(cars)):
        if cars[i].y < y:
            primary_index = i
            y = cars[i].y

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
        self.max_speed = 3 if not self.traffic else -2
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

        start("b")
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

        start("b.1")
        pygame.draw.polygon(my_screen, col, self.corners)
        pygame.draw.polygon(my_screen, (255, 255, 255), self.corners, width=1)
        stop("b.1")
        start("b.2")
        if not self.traffic:
            start("b.2.3")
            self.sensors.update_and_draw(self.sensors.car, my_screen, my_road)
            stop("b.2.3")
            offsets = []
            for i in range(self.sensors.num_rays):
                intersection = get_ray_intersection(self.sensors.ray_len, self.sensors.ray_angles[i],
                                                    self.sensors.car, my_road.traffic)
                p = 0 if intersection is None else 1 - intersection[2]
                offsets.append(p)
            start("b.2.2")
            outputs = network_feed_fwd(self.brain, offsets)
            stop("b.2.2")
            self.dirs = outputs
        stop("b.2")
        stop("b")

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
                weight.append(random.random() * 2 - 1)

        for i in range(num_outputs):
            self.biases.append(random.random() * 2 - 1)


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
    # ct = 0
    best_pos = 10000
    no_improvement_ct = 0
    while run:
        start("run")
        # ct += 1
        clock.tick(60)
        screen.fill(ROAD_COL)
        # main_driver = drivers[get_primary_car_index(drivers)]
        # main_driver.primary = True
        road.draw(screen)
        t.update_and_draw(road, screen)
        pci = get_primary_car_index(drivers)
        road.move_viewport(drivers[pci].y)
        new_best_pos = drivers[pci].y
        if new_best_pos < best_pos:
            no_improvement_ct = 0
            best_pos = min(best_pos, new_best_pos)
        else:
            no_improvement_ct += 1
            if no_improvement_ct > 3:
                break
        for i in range(len(drivers)):
            d = drivers[i]
            if i == pci:
                d.primary = True
            else:
                d.primary = False
            start("update_and_draw")
            d.update_and_draw(road, screen)
            stop("update_and_draw")
            start("assess_damage")
            d.alive = d.assess_damage(road)
            stop("assess_damage")
            d.up = d.dirs[0]
            d.left = d.dirs[1]
            d.right = d.dirs[2]
            d.down = d.dirs[3]

        drivers[pci].primary = False
        start("update")
        pygame.display.update()
        stop("update")
        stop("run")
        # if ct > 100:
          #   break

    dump()
    pygame.quit()
