import math

from constants import CAR_SIZE_Y, CAR_SIZE_X, ACCELERATION, MAX_SPEED_DRIVER, MAX_SPEED_TRAFFIC, ANGLE_CHANGE, \
    DEG_TO_RAD
from utils import clamp

class Car:
    def __init__(self, gui, x, y, traffic=False):
        self.x = x
        self.y = y
        self.traffic = traffic
        self.imgname = "../driver.png" if not self.traffic else "../traffic.png"
        self.gui = gui
        self.img = self.gui.load_img(self.imgname)
        self.traffic = traffic
        self.width = CAR_SIZE_X
        self.height = CAR_SIZE_Y
        self.angle = 0
        self.speed = 0
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.acc = ACCELERATION
        self.max_speed = MAX_SPEED_DRIVER if not self.traffic else MAX_SPEED_TRAFFIC
        self.sensors = []
        self.drawing_sensors = []
        self.alive = True

    def pos(self):
        return self.x, self.y

    def center(self):
        return self.x + self.width / 2, self.y + CAR_SIZE_Y / 2

    def update_up(self):
        self.speed += ACCELERATION
        self.speed = clamp(self.speed, -self.max_speed, self.max_speed)

    def update_down(self):
        self.speed -= ACCELERATION
        self.speed = clamp(self.speed, -self.max_speed, self.max_speed)

    def update_left(self):
        self.angle += ANGLE_CHANGE

    def update_right(self):
        self.angle -= ANGLE_CHANGE

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
            theta = ANGLE_CHANGE
        if self.right:
            theta = -ANGLE_CHANGE
        flip = 1 if self.speed <= 0 else -1
        self.angle += theta * flip

    def update(self, my_road):
        if self.up:
            self.update_up()
        if self.down:
            self.update_down()
        if not self.up and not self.down:
            self._coast()

        self.y += self.speed * math.cos(self.angle * DEG_TO_RAD)
        self.x += self.speed * math.sin(self.angle * DEG_TO_RAD)
        self._turn()


    def draw(self):
        self.gui.draw_car(self.img, self.pos(), self.angle)

