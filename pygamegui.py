import pygame
from constants import *
from geometry import Pt

class PygameGui:
    """
    Contains all Pygame/Drawing functionality.
    """
    def __init__(self, controller):
        self.controller = controller
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Self-Driving Car")
        self.clock = pygame.time.Clock()

    def update(self):
        """
        Updates car and road movement. Pause/Resume/Step mode functionality.
        """
        self.clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.controller.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.controller.paused = True
                elif event.key == pygame.K_r:
                    self.controller.paused = False
                    self.controller.step_mode = False
                elif event.key == pygame.K_q:
                    self.controller.running = False
                elif event.key == pygame.K_s:
                    self.controller.step_mode = True
                    self.controller.paused = False
        self.draw()
        pygame.display.update()

    def draw(self):
        """
        Draws the road and every car, both belonging to the GUI's controller's universe.
        """
        # frame = self.controller.universe.frame
        # path = f"frames\\screenshot00{frame}.png" if frame < 10 else \
        #     f"frames\\screenshot0{frame}.png" if frame < 100 else f"frames\\screenshot{frame}.png"
        # pygame.image.save(self.screen, path)
        self.draw_road(self.controller.universe.road)
        self.draw_cars(self.controller.universe.cars)

    def draw_cars(self, cars):
        """
        draw the cars of the universe. For the primary car, draw the sensors.
        """
        pc = self.controller.universe.primary_car
        for car in cars:
            if car != pc:
                self.draw_outline_car(car)

        if pc is not None:
            self.draw_outline_car(pc)
            self.draw_sensors(pc)

    def draw_outline_car(self, car):
        # Draws an extra white outline around each car for clarity.
        color = car.get_color()
        corners = car.get_corners()
        self.fill_rect(corners, color)
        self.draw_rect(corners, 1, CAR_OUTLINE_COLOR)

    def draw_sensors(self, car):
        # Draws calculated sensors for primary car.
        car_center = Pt(car.x, car.y)
        for s in car.sensors:
            if s.intersection is None:
                p = s.current_endpoint
                color = SENSOR_COLOR
            else:
                p = s.intersection
                color = SENSOR_READ_COLOR
            line = (car_center, p)
            self.draw_line(line, 1, color)

    def draw_road(self, road):
        self.screen.fill(ROAD_COLOR)
        for line in road.get_lines():
            self.draw_line(line, width=MARKER_WIDTH, color=MARKER_COLOR)

    def draw_rect(self, corners, param, color, width=1):
        points = [self.to_screen_pt(p).as_tuple() for p in corners]
        pygame.draw.polygon(self.screen, color, points, width=width)

    def fill_rect(self, corners, color):
        points = [self.to_screen_pt(p).as_tuple() for p in corners]
        pygame.draw.polygon(self.screen, color, points)

    def draw_line(self, line, width, color):
        [p1, p2] = [self.to_screen_pt(p) for p in line]
        pygame.draw.line(self.screen, color, (p1.x, p1.y), (p2.x, p2.y), width)

    def to_screen_pt(self, p):
        screen_x = p.x - self.controller.universe.road.left_x
        screen_y = SCREEN_HEIGHT - p.y
        return Pt(screen_x, screen_y)



