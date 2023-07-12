from refactor.constants import SCREEN_HEIGHT, CAR_POS_ONSCREEN
from refactor.utils import top_of_screen_from_car_y


class Road:
    def __init__(self, x, width, lane_count=3):
        self.x = x
        self.y = 0
        self.width = width
        self.lane_count = lane_count
        self.left = x - width / 2
        self.right = x + width / 2
        self.lines = []

    # print the road in relation to the car
    def move_viewport(self, car_y):
        # where we want the top of the screen
        new_y = top_of_screen_from_car_y(car_y)
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