from refactor.constants import *
from refactor.geometry import Pt, transpose, transpose_line


class Road:
    def __init__(self):
        self.left_x = 0
        self.length = SCREEN_WIDTH
        self.top_line_y = SCREEN_HEIGHT - MARKER_WIDTH / 2
        self.bottom_line_y = MARKER_WIDTH / 2
        self.marker_interval = MARKER_LENGTH * 2
        self.mid_ys = []
        for i in range(NUM_LANES):
            self.mid_ys.append(i * (MARKER_WIDTH + LANE_WIDTH) + LANE_WIDTH / 2)
        self.marker_ys = []
        for i in range(NUM_LANES - 1):
            self.marker_ys.append(MARKER_WIDTH + (i + 1) * (LANE_WIDTH + MARKER_WIDTH) - MARKER_WIDTH / 2)
        self.markers = []
        x = 0
        while x < SCREEN_WIDTH + 2 * MARKER_LENGTH:
            for y in self.marker_ys:
                left_pt = Pt(x, y)
                right_pt = Pt(x + MARKER_LENGTH, y)
                self.markers.append((left_pt, right_pt))
            x += self.marker_interval

    def get_lines(self):
        lines = []
        bottom_line = (Pt(self.left_x, self.bottom_line_y), Pt(self.left_x + self.length, self.bottom_line_y))
        top_line = (Pt(self.left_x, self.top_line_y), Pt(self.left_x + self.length, self.top_line_y))
        f = self.left_x // self.marker_interval
        transp_x = f * self.marker_interval
        for line in self.markers:
            lines.append(transpose_line(line, transp_x, 0))

        lines.append(bottom_line)
        lines.append(top_line)
        # print(lines[0])
        return lines

    def get_lane_center(self, lane_index):
        lane_width = SCREEN_HEIGHT / NUM_LANES
        return self.bottom_line_y + lane_width / 2 + lane_index * lane_width
