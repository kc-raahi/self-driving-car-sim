import pygame
import math

pygame.init()

CAR_SIZE_X = 30
CAR_SIZE_Y = 50
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 600
RAD_TO_DEG = (2 * math.pi) / 360
INF = math.inf

def lerp(a, b, t): return a + (b-a) * t

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
        self.img.set_colorkey((0,0,0))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.angle = 0
        self.speed = 0
        self.acc = 0.00005
        self.max_speed = 0.05 if not self.traffic else 0.04
        self.center = [self.position[0]+CAR_SIZE_X/2, self.position[1]+CAR_SIZE_Y/2]
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

    def draw(self, screen):
        img_copy = pygame.transform.rotate(self.img, self.angle)
        screen.blit(img_copy, (self.x - int(img_copy.get_width()/2), self.y - int(img_copy.get_height()/2)))


    def update(self):
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
        if 0 < self.speed < math.pow(10,-4):
            self.speed = 0

    def _turn(self):
        theta = 0
        if self.left:
            theta = 0.03
        if self.right:
            theta = -0.03
        flip = 1 if self.speed <= 0 else -1
        self.angle += theta * flip

class Road:
    def __init__(self, x, width, lane_count=3):
        self.x = x
        self.width = width
        self.lane_count = lane_count
        self.left = x-width/2
        self.right = x+width/2
        self.top = INF * -1
        self.bottom = INF

    def draw(self, screen):
        line_width = 5
        line_col = (255,255,255)    #white
        for i in range(self.lane_count+1):
            x = lerp(self.left, self.right, i / self.lane_count)
            pygame.draw.line(screen, line_col, (x, -INF), (x, INF), width=line_width)
            print(x)



if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Self-Driving Car")
    driver = Car(100, 100)
    run = True

    while run:
        screen.fill((50, 50, 50))
        driver.draw(screen)
        driver.update()

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


