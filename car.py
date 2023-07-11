import pygame
import math

pygame.init()

CAR_SIZE_X = 30
CAR_SIZE_Y = 50
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 600
RAD_TO_DEG = (2 * math.pi) / 360
INF = 100000
LINE_COL = (255, 255, 255)  # white
ROAD_COL = (50, 50, 50)  # dark gray
LINE_WIDTH = 5
DASH_HEIGHT = 20


def lerp(a, b, t): return a + (b - a) * t


class Car:
    def __init__(self, x, y, traffic=False):
        self.x = x
        self.y = y
        self.position = [self.x, self.y]
        self.traffic = traffic
        self.gas = False
        self.rev = False
        self.left = False
        self.right = False
        self.imgname = "driver.png" if not self.traffic else "traffic.png"
        self.img = pygame.image.load(self.imgname)
        self.img.set_colorkey((0, 0, 0))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.angle = 0
        self.speed = 0
        self.acc = 0.2
        self.max_speed = 3 if not self.traffic else 2
        self.center = [self.position[0] + CAR_SIZE_X / 2, self.position[1] + CAR_SIZE_Y / 2]
        self.sensors = []
        self.drawing_sensors = []
        self.alive = True

    def forward(self):
        self.gas = True
        self.rev = False

    def backward(self):
        self.gas = False
        self.rev = True

    def foot_off_gas(self):
        self.gas = False
        self.rev = False

    def turn_left(self):
        self.left = True
        self.right = False

    def turn_right(self):
        self.left = False
        self.right = True

    def update_and_draw(self, my_road):
        if self.gas:
            self._accel()
        if self.rev:
            self._reverse()
        if not self.gas and not self.rev:
            self._coast()

        self.position = [self.x, self.y]
        self.y += self.speed * math.cos(self.angle * RAD_TO_DEG)
        self.x += self.speed * math.sin(self.angle * RAD_TO_DEG)
        self._turn()
        img_copy = pygame.transform.rotate(self.img, self.angle)
        y = self.y - my_road.y
        screen.blit(img_copy, (self.x - int(img_copy.get_width() / 2), y - int(img_copy.get_height() / 2)))

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


class Road:
    def __init__(self, x, width, lane_count=3):
        self.x = x
        self.y = 0
        self.width = width
        self.lane_count = lane_count
        self.left = x - width / 2
        self.right = x + width / 2
        self.top = INF * -1
        self.bottom = INF
        self.lines = []

    def move_viewport(self, car_y):
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

    # https://stackoverflow.com/questions/29582596/pygame-translate-surface-a-given-amount
    def scroll(self, my_screen, car):
        temp = my_screen.copy()
        my_screen.fill(ROAD_COL)
        my_screen.blit(temp, (0, -car.y + SCREEN_HEIGHT * 0.9))


if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Self-Driving Car")
    road = Road(SCREEN_WIDTH / 2, SCREEN_WIDTH * 0.9)
    road.set_lines()
    driver = Car(road.get_lane_center(int(road.lane_count / 2)), SCREEN_HEIGHT * 0.9)  # int(lanes/2)+(width/lanes)
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        screen.fill(ROAD_COL)
        road.move_viewport(driver.y)
        road.draw(screen)
        driver.update_and_draw(road)

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
