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
        self.angle = 0
        self.speed = 0
        self.acc = 0.2
        self.max_speed = 3 if not self.traffic else 2
        self.center = [self.position[0]+CAR_SIZE_X/2, self.position[1]+CAR_SIZE_Y/2]
        self.sensors = []
        self.drawing_sensors = []
        self.alive = True

    def draw(self, screen, x, y):
        pygame.draw.rect(screen, (100,100,200), (x, y, self.width, self.height))

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            print("Key pressed")
            if event.key == pygame.K_UP:
                print("Up pressed")
                if self.speed > self.max_speed * -1:
                    self.speed -= self.acc
                else:
                    self.speed = self.max_speed * -1

            if event.key == pygame.K_DOWN:
                print("Down pressed")
                if self.speed < self.max_speed:
                    self.speed += self.acc
                else:
                    self.speed = self.max_speed

        if event.type == pygame.KEYUP:
            print("Keystroke released")
            while self.speed != 0:
                if self.speed < 0:
                    self.speed += self.acc
                else:
                    self.speed -= self.acc


        self.y += self.speed


if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Self-Driving Car")
    driver = Car(100, 100, CAR_SIZE_X, CAR_SIZE_Y)
    run = True

    while run:
        keys = pygame.key.get_pressed()
        screen.fill((50, 50, 50))
        driver.draw(screen, driver.x, driver.y)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                driver.update(event)
        pygame.display.update()
        #pygame.display.flip()

    pygame.quit()


