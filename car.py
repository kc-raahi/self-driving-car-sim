import pygame

pygame.init()

CAR_SIZE_X = 30
CAR_SIZE_Y = 50
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 600


class Car:
    def __init__(self, x, y, width, height, traffic=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.position = [0, 0]
        self.traffic = traffic
        self.gas = False
        self.rev = False
        self.angle = 0
        self.speed = 0
        self.acc = 0.00005
        self.max_speed = 0.05 if not self.traffic else 0.04
        self.center = [self.position[0]+CAR_SIZE_X/2, self.position[1]+CAR_SIZE_Y/2]
        self.sensors = []
        self.drawing_sensors = []
        self.alive = True

    def draw(self, screen, x, y):
        pygame.draw.rect(screen, (100,100,200), (x, y, self.width, self.height))

    def update(self):
        if self.gas:
            self.accel()
        if self.rev:
            self.reverse()
        if not self.gas and not self.rev:
            self.coast()

        self.y += self.speed


    def accel(self):
        if self.speed > self.max_speed * -1:
            self.speed -= self.acc
        else:
            self.speed = self.max_speed * -1

    def reverse(self):
        if self.speed < self.max_speed:
            self.speed += self.acc
        else:
            self.speed = self.max_speed

    def coast(self):
        while self.speed != 0:
            if self.speed < 0:
                self.speed += self.acc
            else:
                self.speed -= self.acc

if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Self-Driving Car")
    driver = Car(100, 100, CAR_SIZE_X, CAR_SIZE_Y)
    run = True

    while run:
        keys = pygame.key.get_pressed()
        screen.fill((50, 50, 50))
        driver.draw(screen, driver.x, driver.y)
        driver.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    driver.gas = True
                elif event.key == pygame.K_DOWN:
                    driver.rev = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    driver.gas = False
                elif event.key == pygame.K_DOWN:
                    driver.rev = False
        pygame.display.update()

    pygame.quit()


