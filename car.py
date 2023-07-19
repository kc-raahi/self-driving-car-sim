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
TRAFFIC_COL = (100, 200, 100)


def lerp(a, b, t):
    return a + (b - a) * t


def get_ray_intersection(ray, length, angle, my_driver, my_traffic):
    if ray[1][0] < 0 or ray[1][0] > SCREEN_WIDTH:
        return True
    for i in range(length):
        for car in my_traffic:
            ray_point_x = my_driver.x - i * math.sin(angle)
            ray_point_y = my_driver.y - i * math.cos(angle)
            x_check = car.x - CAR_SIZE_X / 2 <= ray_point_x <= car.x + CAR_SIZE_X / 2
            y_check = car.y - CAR_SIZE_Y / 2 <= ray_point_y <= car.y + CAR_SIZE_Y / 2
            if x_check and y_check:
                return True

    return False

# 0: x; 1: y
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


class Car:
    def __init__(self, x, y, traffic=False):
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
        self.angle = 0  # degrees
        self.speed = 0
        self.acc = 0.2
        self.max_speed = 3 if not self.traffic else 2
        self.center = (self.x + CAR_SIZE_X / 2, self.y + CAR_SIZE_Y / 2)
        self.sensors = []
        self.drawing_sensors = []
        self.alive = True
        self.corners = []

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
                self.alive = False

        for car in my_road.traffic:
            if car_intersection(self.corners, car.corners):
                self.alive = False

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

    def update_and_draw(self, my_road, my_screen):
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
        col = DRIVER_COL if not self.traffic else TRAFFIC_COL
        self.get_polygon(y)
        pygame.draw.polygon(my_screen, col, self.corners)

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

    def __init__(self, car, num_rays=4, ray_len=100, ray_spread=math.pi / 2):
        self.car = car
        self.num_rays = num_rays
        self.ray_len = ray_len
        self.ray_spread = ray_spread
        self.rays = []
        self.intersections = []

    def update_and_draw(self, car, my_screen, my_road):
        self.rays = []
        y = car.y - my_road.y
        for i in range(self.num_rays):
            self.intersections.append(False)
            ray_angle = lerp(self.ray_spread / 2, -self.ray_spread / 2, i / (self.num_rays - 1)) + car.angle * \
                        DEG_TO_RAD
            a = (car.x, y)
            b = (car.x - self.ray_len * math.sin(ray_angle), y - self.ray_len * math.cos(ray_angle))
            self.rays.append((a, b))
            self.intersections[i] = get_ray_intersection(self.rays[i], self.ray_len, ray_angle, car, my_road.traffic)

            col = SENSOR_COL if not self.intersections[i] else SENSOR_ACTIVE_COL
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


if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Self-Driving Car")
    road = Road(SCREEN_WIDTH / 2, SCREEN_WIDTH * 0.9)
    road.set_lines()
    driver = Car(road.get_lane_center(int(road.lane_count / 2)), SCREEN_HEIGHT * 0.9)  # int(lanes/2)+(width/lanes)
    t = Car(road.get_lane_center(0), 100, traffic=True)
    road.traffic.append(t)
    sensor = Sensor(driver)
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        screen.fill(ROAD_COL)
        road.move_viewport(driver.y)
        road.draw(screen)
        driver.update_and_draw(road, screen)
        t.update_and_draw(road, screen)
        sensor.update_and_draw(driver, screen, road)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
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
                if event.key == pygame.K_LEFT:
                    driver.left = False
                if event.key == pygame.K_RIGHT:
                    driver.right = False

        pygame.display.update()

    pygame.quit()
