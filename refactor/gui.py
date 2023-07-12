import pygame
from constants import CAR_SIZE_X, CAR_SIZE_Y, SCREEN_WIDTH, SCREEN_HEIGHT
from utils import to_screen_y

class Gui:

    def __init__(self):
        self.viewport_top_y = 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Self-Driving Car")

    def set_viewport_top_y(self, y):
        self.viewport_top_y = y

    def load_img(self, path):
        image = pygame.image.load(path)
        image.set_colorkey((0, 0, 0))
        return pygame.transform.scale(image, (CAR_SIZE_X, CAR_SIZE_Y))

    def draw_car(self, img, pos, angle):
        x, y = pos
        img_copy = pygame.transform.rotate(img, angle)
        y = to_screen_y(y, self.viewport_top_y)
        self.screen.blit(img_copy, (x - int(img_copy.get_width() / 2), y - int(img_copy.get_height() / 2)))
